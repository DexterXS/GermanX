import openai
import os


class MyChatGPT:
    def __init__(self, model_engine="davinci-002"):
        self.model_engine = model_engine

    def set_api_key(self):
        openai.api_key = os.getenv("API_CHATGPT")
    def generate_answer(self, input_text='test', max_tokens=0):
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=input_text,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return completion.choices[0].text.strip()


my_chat_gpt = MyChatGPT()
answer = my_chat_gpt.generate_answer(input_text="Как называется чат джипити?")
