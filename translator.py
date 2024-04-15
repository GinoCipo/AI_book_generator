import os
from main import client, completion_with_backoff
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

def gen_translation(base_text):
    translations = [completion_with_backoff(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an english to spanish translator. You will return the spanish translation of the content you get."},
            {"role": "user", "content": chapter}
        ]
    ).choices[0].message.content for chapter in base_text]
    return translations
