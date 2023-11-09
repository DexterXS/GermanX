from gpt4all import GPT4All
model = GPT4All("mistral-7b-openorca.Q4_0.gguf")
with model.chat_session():
    response1 = model.generate(prompt='Напиши на немецком предложение используя глагол Können', temp=0)
    print(model.current_chat_session)