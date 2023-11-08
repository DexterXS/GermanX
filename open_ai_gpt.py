import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "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"

# задаем модель и промпт
model_engine = "gpt-3.5-turbo"
prompt = "Write word whith Auto"

# задаем макс кол-во слов
max_tokens = 40

# генерируем ответ
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=40,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# выводим ответ
print(completion.choices[0].text)