import generator
import json
import shortener
import translator

f = open("new-api/data.json")
data = json.load(f)
f.close()

# Aca va todo lo que es generator

text = open('first output.txt', 'r').read().split("\n\n")

# Aca va todo lo que es translator