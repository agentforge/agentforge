from typing import Any, Dict

class Respond:
    def __init__(self, avatar, agent, service, thoughts):
        self.avatar = avatar
        self.agent = agent
        self.service = service
        self.thoughts = thoughts

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = context['prompt']
        form_data = context['form_data']
        app = context['app']

        form_data["avatar"] = self.avatar.get_avatar(form_data["avatar"])
        self.agent.configure(form_data)
        self.agent.memory.recall(prompt)
        self.agent.save_speech(prompt)

        formatted_prompt = self.agent.process_prompt(instruction=prompt, config=form_data)
        form_data["prompt"] = formatted_prompt
        if "reflection" in self.thoughts and self.thoughts["reflection"] is not None:
            form_data["avatar"]["prompt_context"]["reflection"] = self.thoughts["reflection"]

        response = self.service.call_llm(form_data)
        if "choices" not in response:
            return {"error": response} # return error

        text = response["choices"][0]["text"]
        response["choices"][0]["text"] = self.agent.process_completion(text, form_data) 
        self.agent.save_response(response["choices"][0]["text"])
        self.agent.memory.remember(prompt, response["choices"][0]["text"], app)

        form_data["prompt"] = prompt
        return response
