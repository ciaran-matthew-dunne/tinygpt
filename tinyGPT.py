# A small Python program for interfacing with the OpenAI API.
# See https://platform.openai.com/docs/api-reference/chat
import os
import sys
import time
import re
import openai

##### API interaction.
def auth_api() :
  openai.api_key = os.getenv("OPENAI_KEY")

def get_models():
  return [ mdl["id"] for mdl in openai.Model.list()['data'] ]

def add_msg(chat, role, msg):
  chat.append({"role": role, "content": msg})

# Returns a generator object yielding incoming fragments of GPT call.
# When generator is finished, the response is added to the chat.
def complete_chat(chat, model):
  response = openai.ChatCompletion.create(model=model, messages=chat, stream=True)
  compl = ""
  for chunk in response:
    msg = chunk["choices"][0]["delta"].get('content','\n')
    compl += msg
    yield msg
  add_msg(chat, "assistant", compl)

def chat_stream(chat, msg):
  add_msg(chat, "user", msg)
  gen = complete_chat(chat, "gpt-3.5-turbo")
  print("```")
  for m in gen:
    print(m, end='',flush=True)
  print("\n")

sys.ps1 = '''```python\n>> ''' # Hack for ST4 markdown highlighting
auth_api()
  
  