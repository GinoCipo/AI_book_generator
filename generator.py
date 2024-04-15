import json
import os
from main import client, completion_with_backoff

def names_to_string(names):
    if len(names) == 0:
        return ""
    elif len(names) == 1:
        return names[0]
    else:
        return ", ".join(names[:-1]) + " and " + names[-1]

def parse_data(data):
    if data["Minds"] == []:
        topic = data["Topic"]
        opener = f"Write the title for a book about {topic}. Also, write the titles for: An introduction, between 1 and 3 chapters (describing the main concepts about {topic}), final chapter remarking points in common between them and a conclusion. Answer in .json format: {{'title': (title), 'subtitles': [(all of the subtitles)] }}. Don't send ANYTHING besides .json response."
    else:
        minds = names_to_string(data["Minds"])
        topic = data["Topic"]
        mindQuantity = len(data["Minds"])
        opener = f"Write the title for a book about {topic}. Book covers ideas from {minds}. Also, write the titles for: An introduction, {mindQuantity} chapters (describing the main ideas from the minds), final chapter remarking points in common between them and a conclusion. Answer in .json format: {{'title': (title), 'subtitles': [(all of the subtitles)] }}. Don't send ANYTHING besides .json response."
    return opener

def gen_titles(opener):
    titles = completion_with_backoff(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a book writing assistant."},
            {"role": "user", "content": opener}
        ]
    )
    return json.loads(titles.choices[0].message.content)

def gen_book(titles):
    prompts = []
    contents = []

    for index, subtitle in enumerate(titles['subtitles']):
        if index == 0:
            intro_prompt = f"Write the content for {subtitle}. DON'T write any subtitle when starting. Be brief and concise. 1 paragraph max."
            prompts.append(intro_prompt)
            intro_completion = completion_with_backoff(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a skillful book writer. With the task of writing a book titled {titles['title']}"},
                    {"role": "user", "content": intro_prompt}
                ]
            )
            contents.append(intro_completion.choices[0].message.content)
        elif index == len(titles['subtitles'])-1:
            conclusion_prompt = f"Write the content for {subtitle}. DON'T write any subtitle when starting. Be brief and concise. 2 paragraph max."
            prompts.append(conclusion_prompt)
            conclusion_completion = completion_with_backoff(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a skillful book writer. With the task of writing a book titled {titles['title']}"},
                    {"role": "user", "content": conclusion_prompt}
                ]
            )
            contents.append(conclusion_completion.choices[0].message.content)
        else:
            chapter_prompt = f"Write the content for {subtitle}. DON'T write any subtitle when starting. Be detailed. 3 paragraph max."
            prompts.append(chapter_prompt)
            chapter_completion = completion_with_backoff(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a skillful book writer. With the task of writing a book titled {titles['title']}"},
                    {"role": "user", "content": chapter_prompt}
                ]
            )
            contents.append(chapter_completion.choices[0].message.content)
    
    return contents
    
if __name__ == "__main__":
    print("This module is used to generate the contents of the audiobook in english. This shall be used first.")