import tinyGPT, sublime, sublime_plugin

prompt_re = r"\*-([\s\S]*?)-\*"

def get_prompts() 
view.substr(sublime.Region(0, view.find(prompt_re, 0).end()))

# Grabs all prompts from file and prints response.  
class ChatSublimeCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if view is not None and view.file_name().endswith('.md'):
            cfg = {...} # your configuration dictionary
            chat(cfg, lambda g : resp_sublime(view, g), prompt)

def resp_sublime(view, gen):
    edit = view.begin_edit()
    try:
      # Write delimiter timestamp before GPT response
      timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      sublime.set_timeout_async(lambda: append_text(f"\n*- BEGIN GPT at {timestamp} -*"), 0)
      # 
      for msg in gen:
          view.insert(edit, view.size(), msg)
          view.run_command("move_to", {"to": "eof"})
      sublime.set_timeout(lambda: view.show(view.size()), 0)
    finally:
        view.end_edit(edit)





def chat_sublime(cfg, view):
  def append_text(text):
    edit = view.begin_edit()
    view.insert(edit, view.size(), text)
    view.end_edit(edit)

  # Get prompt from file
  prompt = 

  # Stream GPT response
  for resp_frag in call_gpt(cfg):
    sublime.set_timeout_async(lambda: append_text(resp_frag), 0)
  # Write delimiter after GPT response
  sublime.set_timeout_async(lambda: append_text(f"\n*- END GPT -*\n\n"), 0)


# For usage:
# view = sublime.active_window().active_view()
# chat_sublime(default_config, view)