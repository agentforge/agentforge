#!/bin/bash

# Step 1: Install SuperTokens
# Note: Update this with the specific installation instructions for your OS if different
echo "Installing SuperTokens..."
# Add instructions to install SuperTokens for your specific OS

# Step 2: Start PostgreSQL Docker container
# echo "Starting PostgreSQL container..."
# docker run \
#   -e POSTGRES_USER=supertokens_user \
#   -e POSTGRES_PASSWORD=thisBeOurPostgresPassward0453 \
#   --network=host \
#   -p 5432:5432 \
#   -d postgres \
#   -c listen_addresses=0.0.0.0

# Waiting for PostgreSQL to start
# echo "Waiting for PostgreSQL to start..."
# sleep 10

# Step 3: Setup Database and User
echo "Setting up database and user..."
# PGPASSWORD=thisBeOurPostgresPassward0453 psql -U supertokens_user -h localhost -d postgres -c "CREATE DATABASE supertokens;"
# PGPASSWORD=thisBeOurPostgresPassward0453 psql -U supertokens_user -h localhost -d postgres -c "CREATE USER supertokens_user WITH ENCRYPTED PASSWORD 'thisBeOurPostgresPassward0453';"
PGPASSWORD=thisBeOurPostgresPassward0453 psql -U supertokens_user -h localhost -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE supertokens TO supertokens_user;"


# Step 4: Update SuperTokens config.yaml
# echo "Updating SuperTokens configuration..."
# CONFIG_PATH="/usr/lib/supertokens/config.yaml"
# echo "postgresql_connection_uri: \"postgresql://supertokens_user:somePassword@localhost:5432/supertokens\"" >> $CONFIG_PATH

# Step 5: Start SuperTokens
# echo "Starting SuperTokens..."
# supertokens start

# Step 6: Verify Setup
echo "Verifying setup..."
sleep 5 # Wait for SuperTokens to start
curl http://localhost:3567/hello

echo "Setup complete."