import google.genai as genai
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        prompt = ""
        for msg in self.messages:
            prompt += f"{msg['role']} : {msg['content']}\n"

        response = client.models.generate_content(model=GEMINI_FLASH, contents=prompt)
        return response.text