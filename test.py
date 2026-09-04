from openai import OpenAI
import os

endpoint = "https://openai-test-creds.openai.azure.com/openai/v1"
deployment_name = "gpt-4.1"
api_key = os.getenv("AZURE_OPENAI_KEY")  # set this in your environment, don't hardcode it

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)

print(completion.choices[0].message.content)