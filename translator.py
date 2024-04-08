from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

text = open('first output.txt', 'r').read().split("\n\n")

client = OpenAI(api_key="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")

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

translations = [completion_with_backoff(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an english to spanish translator. You will return the spanish translation of the content you get."},
        {"role": "user", "content": chapter}
    ]
).choices[0].message.content for chapter in text]

with open('second output.txt', 'w') as f:
    for cap in translations:
        print(cap, file=f)