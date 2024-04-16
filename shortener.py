import re

def maxlen (paragraph):
    sentences = [s + "." for s in paragraph.split(".")]
    array = []
    accumulated = ""
    for index, sentence in enumerate(sentences):
        if len(accumulated) + len(sentence) <= 500:
            accumulated += sentence
        else: 
            array.append(accumulated)
            accumulated = sentence
        if index == len(sentences)-1:
            array.append(accumulated)
    return array

text = open('second output.txt', 'r').read().split('\n\n')

with open('third output.txt', 'w') as f:
    for chapter in text:
        split = chapter.split("\n\n")
        content = [maxlen(paragraph) for paragraph in split]
        for c in content: 
            for p in c: 
                q = p.replace("..", ".")
                print(q, file=f)
