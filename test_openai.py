

from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1-mini",
    input="Say OK"
)

print(resp.output_text)