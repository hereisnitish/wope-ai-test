import os
import re
import webbrowser
from pathlib import Path

import openai
from openai.types.responses import ResponseInputParam

client = openai.OpenAI()

def get_response_output_text(input: str | ResponseInputParam):
    client = openai.OpenAI()
    response = client.responses.create(
        model="gpt-5",
        instructions="""
You are an assistant that generates HTML components.

Instructions:
- Use HTML, CSS, Tailwind CSS, and JavaScript to build the component.
- Your response must contain only the code for the component—no explanations, comments, or extra text.
- The component should be visually appealing, production-ready, and responsive.
- The code you provide will be inserted directly into an existing HTML page, so ensure it works standalone and does not include <html>, <head>, or <body> tags.
- Keep your code clean and well-structured.

Example output:
```html
<script src="script.js">
  console.log("Hello World");
</script>
<style>
  .component {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
  }
</style>
<div class="component">
  <h1>Hello World</h1>
</div>
```
""",
        input=input,
    )
    return response.output_text


def extract_html_from_text(text: str):
    """Extract an HTML code block from text; fallback to first code block, else full text."""
    html_block = re.search(r"```html\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if html_block:
        result = html_block.group(1)
        return result
    any_block = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if any_block:
        result = any_block.group(1)
        return result
    return text


def save_html(html: str, filename: str) -> Path:
    """Save HTML to outputs/ directory and return the path."""
    try:
        base_dir = Path(__file__).parent
    except NameError:
        base_dir = Path.cwd()

    folder = "outputs"
    outputs_dir = base_dir / folder
    outputs_dir.mkdir(parents=True, exist_ok=True)

    output_path = outputs_dir / filename
    output_path.write_text(html, encoding="utf-8")
    return output_path



def make_website(*, website_input: str | ResponseInputParam, filename: str = "website.html"):
    response_text = get_response_output_text(website_input)
    html = extract_html_from_text(response_text)
    output_path = save_html(html, filename)

    return output_path


# make_website(
#     website_input="Make me landing page for a retro-games store. Retro-arcade noir some might say",
#     filename="retro_dark.html",
# )

