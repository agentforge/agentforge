from typing import Any, Dict

class Respond:
    def __init__(self):
        pass

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        service = APIService()
        response = self.service.call_llm(context)
        if "choices" not in response:
            return {"error": response} # return error

        text = response["choices"][0]["text"]
        response["choices"][0]["text"] = self.agent.process_completion(text, form_data) 
        self.agent.save_response(response["choices"][0]["text"])
        self.agent.memory.remember(prompt, response["choices"][0]["text"], app)

        form_data["prompt"] = prompt
        return response
