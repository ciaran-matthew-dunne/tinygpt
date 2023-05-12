# A small Python program for interfacing with the OpenAI API.
# See https://platform.openai.com/docs/api-reference/chat
import os
import sys
import time
import re
import openai

history = [
  {"name": "Foo", "conv": []}, 
  {"name": "Bar", "conv": []}, 
  {"name": "Baz", "conv": []}
]

# A *configuration* is a dict-triple of a string, a chat, and a system message. 
default_config = {
  "model": "gpt-3.5-turbo",
  "chat":  history[0],
  "sys_prompt": "You are a chatbot." 
}

##### API interaction.
def auth_api() :
  openai.api_key = os.getenv("OPENAI_KEY")
auth_api()

# Return list of available models
def get_models():
  return [ mdl["id"] for mdl in openai.Model.list()['data'] ]

# Returns a generator object yielding incoming fragments of GPT call. 
def call_gpt(cfg):
  response = openai.ChatCompletion.create(model=cfg['model'], messages=cfg['chat']['conv'], stream=True)
  for chunk in response:
    msg = chunk["choices"][0]["delta"].get('content','\n')
    yield msg

#### Handling the generator.
# Print generator to standard output.
def resp_stoud_md(gen):
  print("```")
  for m in gen:
    print(m, end='',flush=True)
  print("\n")

# Convert generator to string (i.e., no streaming).
def resp_str(gen):
  return ''.join(gen)

## Conversation management.
def add_msg(conv, role, msg):
  conv.append({"role": role, "content": msg})

def chat(cfg, resp_handler, msg):
  add_msg(cfg["chat"]["conv"], "user", msg)
  resp_handler(call_gpt(cfg))

ch = lambda x : chat(default_config, resp_stoud_md, x)

# def resp_file(cfg, path, msg)
#   with open(path, 'rw+'):

# def chat_file(cfg, path):
#   with open(path, "r") as f:
#     lines = f.read()
#     match = re.compile(r"\*-([\s\S]*?)-\*").search(lines)
#     prompt = match.group(1)
#     n = lines.count("\n", 0, match.start()) + 1
#   chat(cfg, lambda g : resp_file(path, n, g), prompt)

# Hack for sublimetext syntax markdown highlighting
sys.ps1 = '''```python
>> '''
