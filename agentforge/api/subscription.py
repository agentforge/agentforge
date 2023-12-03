import os
from fastapi import APIRouter, HTTPException
from agentforge.interfaces.mongodb import MongoDBKVStore as DB
from agentforge.config import DbConfig
import time
from pydantic import BaseModel
from supertokens_python.recipe.session.asyncio import get_session
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from fastapi import Depends, Request
from agentforge.utils import logger
import stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

from typing import List, Dict, Any

class UserEmail(BaseModel):
    email: str

router = APIRouter()

db_config = DbConfig.from_env()
db = DB(db_config)  # Initialize your DB class here

def update_stripe_info(user_id, session_id):
    # Retrieve the checkout session from Stripe
    session = stripe.checkout.Session.retrieve(session_id)
    
    # Assuming 'user_id' is the ObjectId of the user document you want to update
    # You can update only the fields that have changed or the entire stripe object
    update_fields = {
        'stripe': session, # This replaces the entire stripe field with the new session object
        # To update individual fields within the stripe object, use dot notation:
        # 'stripe.plan_status': 'new_plan_status',
        # 'stripe.other_field': 'new_value',
    }
    
    # Update the user's document in the database
    result = db.set("users", user_id, update_fields)

    return result.modified_count  # Returns the number of documents modified


# Function to retrieve the payment methods and append them to user_obj
def append_payment_methods_to_user(user_obj: Dict[str, Any], customer_id: str) -> None:
    try:
        # Retrieve the list of payment methods for the customer
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id,
            type="card"  # or 'bank_account', etc., based on the payment methods you're interested in
        )

        # Initialize an empty list for payment methods
        user_obj["payment_methods"] = []

        # Iterate over the retrieved payment methods and append them to the user_obj
        for payment_method in payment_methods.auto_paging_iter():
            # You can choose which payment method details to append
            user_obj["payment_methods"].append({
                "id": payment_method.id,
                "brand": payment_method.card.brand,
                "last4": payment_method.card.last4,
                "exp_month": payment_method.card.exp_month,
                "exp_year": payment_method.card.exp_year
            })

    except stripe.error.StripeError as e:
        # Handle error
        print(f"An error occurred: {e}")

async def get_user(request: Request, filter: Dict[str, Any] = {}):
    logger.info(request)
    session = await get_session(request)

    if session is None:
        raise HTTPException(status_code=401, detail="User session not found.")

    user_id = session.get_user_id()
    filter['supertokens_id'] = user_id
    cursor = db.get_many("users", filter)  # This returns a Cursor
    user_data_list = list(cursor)  # Convert Cursor to list of dictionaries

    if not user_data_list:
        raise HTTPException(status_code=401, detail="user not found/has not paid")

    # raw user data private to the server
    return user_data_list[0]  # Get the first item (should only be one)

### STRIPE API ###
### Cancel the user's subscription without delaying until the end of the billing period
@router.post('/cancel-subscription')
async def cancel_subscription(request: Request):
    user_data = await get_user(request, {"stripe.payment_status": "paid"})

    # Fetch the user's subscription from the database.
    # This is a placeholder for your database call:
    subscription_id = user_data['stripe']['subscription']
    try:
        stripe.Subscription.delete(subscription_id)
        print(user_data['id'])
        print(user_data['stripe']['id'])
        mod_cnt = update_stripe_info(user_data['id'], user_data['stripe']['id'])
        print(mod_cnt)
        if mod_cnt == 0:
            logger.info(f"Failed to update stripe info for session_id {user_data['stripe']['id']}")
            return {'success': True, 'message': "Something went wrong."}
        return {'success': True}
    except stripe.error.StripeError as e:
        # Handle the error
        return {'success': False, 'message': str(e)}

### Get the Subscription for the user if one such exists
@router.post("/get-subscription")
async def check_subscription(request: Request):
    user_data = await get_user(request, {"stripe.payment_status": "paid"})

    # obj with cleaned data to be sent back to user
    user_obj = {}

    user_email = user_data.get("email")
    print(user_email)

    # export data to be sent to the user
    user_obj["customer_id"] = user_data["stripe"]["customer"]
    customer_id = user_obj["customer_id"]
    customer = stripe.Customer.retrieve(customer_id)

    user_obj["expires_at"] = user_data["stripe"]["expires_at"]
    user_obj["payment_status"] = user_data["stripe"]["payment_status"]
    user_obj["status"] = user_data["stripe"]["status"]
    append_payment_methods_to_user(user_obj, customer_id)
    user_obj["email"] = user_email
    user_obj["name"] = customer.name
    user_obj["postal_code"] = customer.address.postal_code
    if "role" in user_data and user_data["role"] == "admin":
        user_obj["role"] = "admin"
    else:
        user_obj["role"] = "user"

    invoices = stripe.Invoice.list(customer=customer_id, limit=3)
    invoices_final = [{
            "date": invoice.created,
            "amount": invoice.total / 100,  # Convert from cents to dollars
            "status": invoice.status,
            "description": invoice.description or "Invoice for subscription"
        } for invoice in invoices.data]

    subscriptions = stripe.Subscription.list(customer=customer_id, status='active', limit=1, expand=["data.plan.product"])
    if subscriptions.data:
        latest_subscription = subscriptions.data[0]
        print(latest_subscription.plan)
        user_obj["latest_subscription"] = {
            "id": latest_subscription.id,
            "current_period_end": latest_subscription.current_period_end,
            "plan": latest_subscription.plan.id,
            "product": {
                "id": latest_subscription.plan.product.id,
                "name": latest_subscription.plan.product.name,
                # Add any other product details you need here
            },
            "session_id": user_data["stripe"]["id"],
            "cost": '{:.2f}'.format(user_data["stripe"]["amount_total"] / 100),
            "invoices": invoices_final,
            "cancel_at_period_end": latest_subscription.cancel_at_period_end,
            # Include other relevant subscription details here
        }
        
        # update expiry in DB if needed:
        if user_obj["expires_at"] != latest_subscription.current_period_end:
            user_obj["expires_at"] = latest_subscription.current_period_end
            db.set("users", user_data["id"], {"stripe.expires_at": latest_subscription.current_period_end})
    else:
        return {"message": "No active subscriptions found", "active": False, "user": user_obj, "status": 200}

    return {"message": "subscription active", "active": True, "user": user_obj, "status": 200}