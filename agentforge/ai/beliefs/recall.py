from typing import Any, Dict
from agentforge.ai.agents.context import Context
from agentforge.utils import logger
from agentforge.ai.reasoning.zeroshot import ZeroShotClassifier

### BELIEFS: Recalls a memory given the context
class Recall:
    def __init__(self):
        self.z = ZeroShotClassifier()
    
    def execute(self, context: Context) -> Dict[str, Any]:
        msgs, msg_cnt = context.get_messages(prefix="", postfix="", n=2)
        memories = context.memory.recall(
            context.get('input.user_id'),
            context.get('model.persona.name'),
            msgs,
        )
        knowledge = context.memory.knowledge(
            context.get('input.user_id'),
            context.get('model.persona.name'),
            context.get('instruction'),
            collection='knowledge',
            n=1
        )

        ### GREENSAGE SPECIFIC
        z_val = self.z.classify("### Instruction: Is the user asking for a cannabis strain recommendation? Respond with Yes or No. ### Input: {{user_input}} ### Response: ", ["Yes", "No"], {"user_input": context.get('instruction')}, context)
        logger.info(f"STRAIN QUESTION: {z_val}")
        if z_val == "Yes":
            extra_data = context.memory.knowledge(
                context.get('input.user_id'),
                context.get('model.persona.name'),
                context.get('instruction'),
                collection='strains',
                n=5
            )
        else:
            extra_data = None

        # working = context.memory.session_history(
        #     context.get('input.user_id'),
        #     context.get('model.persona.name'),
        #     context.get('input.id'),
        #     n=4
        # )
        logger.info(f"RECALLING {context.get('instruction')}")
        context.set('recall', memories)
        context.set('knowledge', knowledge)
        context.set('additional_knowledge', extra_data)
        return context
