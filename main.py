import generator
import json
import os
import shortener
import translator
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

client = OpenAI(api_key=os.environ["OPEN_AI_API"])

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def print_to_file(text, output_dir, filename):
    with open(output_dir + f"{filename}.txt", 'w') as f:
        print(text, file=f)

output_path = "./output/"
f = open("new-api/data.json")
data = json.load(f)
f.close()


def get_next_folder_number(output_dir):
    existing_folders = [name for name in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, name))]
    
    if not existing_folders:
        return 1
    
    folder_numbers = [int(folder_name) for folder_name in existing_folders]
    max_number = max(folder_numbers)
    
    return max_number + 1

book_id = get_next_folder_number(output_path)
book_path = output_path + f"{book_id}"

opener = generator.parse_data(data)

titles = generator.gen_titles(opener)

contents = generator.gen_book(titles)

base_text = titles["title"] + "\n"
for index, p in enumerate(contents):
    base_text = base_text + titles['subtitles'][index] + "\n"
    base_text = base_text + p + "\n"

print_to_file(base_text, book_path, "base")

base = open(book_path + 'base.txt', 'r')
base_file = base.read().split("\n\n")
base.close

translated= ""
for capitulo in translator.gen_translation(base_file):
    translated = translated + capitulo + "\n" 

print_to_file(translated, book_path, "spanish")