import os
import subprocess
import json
import base64
import requests
from typing import List
import shutil
from pathlib import Path
from dotenv import load_dotenv
from crewai.tools import tool
from .openai_page_generator import make_website
from ..models import PortfolioTemplate

#utility functions
def get_user_input(prompt: str) -> str:
    print(f"\n🤖 {prompt}")
    return input("👤 You: ").strip()



#All tools

@tool("get_existing_components")
def get_existing_components() -> List[PortfolioTemplate]:
    """Get all existing portfolio template components. Returns a list of templates with their details."""

    response = PortfolioTemplate.objects.all()

    data = [
        {
            "name": item.name,
            "display_name": item.display_name,
            "description": item.description,
            "file_path_template": item.file_path_template
        } for item in response
    ]

    return data


@tool("ask_user")
def ask_user(question: str) -> str:
	"""Ask the user a question and get their response. Use this tool to gather requirements and preferences interactively."""
	return get_user_input(question)


@tool("create_new_component")
def create_new_component(category: str, name: str, display_name: str, description: str) -> str:
    """Create a new component in html format and return the file path."""
    path_name  =  make_website(website_input=f"Make me {display_name} component for {description}", filename=f"{name}.html")
    return path_name


@tool("combine_components")
def combine_components(component_paths: List[str], page_title: str = "Generated Page") -> str:
    """Combine multiple HTML components into a single complete HTML page."""
    combined_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
        }}
        .component {{
            margin-bottom: 0;
        }}
    </style>
</head>
<body>
"""

    for path in component_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                component_content = f.read()
                # Extract body content if it's a complete HTML file
                if '<body>' in component_content:
                    body_start = component_content.find('<body>') + 6
                    body_end = component_content.find('</body>')
                    if body_end != -1:
                        component_content = component_content[body_start:body_end]

                combined_html += f'<div class="component">{component_content}</div>\n'
        except Exception as e:
            print(f"Error reading component {path}: {e}")

    combined_html += """
</body>
</html>"""

    # Save the combined HTML directly without using make_website
    try:
        base_dir = Path(__file__).parent
    except NameError:
        base_dir = Path.cwd()

    folder = "outputs"
    outputs_dir = base_dir / folder
    outputs_dir.mkdir(parents=True, exist_ok=True)

    output_path = outputs_dir / "complete_page.html"
    output_path.write_text(combined_html, encoding="utf-8")
    return str(output_path)


@tool("save_final_html")
def save_final_html(html_content: str, filename: str = "final_page.html") -> str:
    """Save the final HTML content to a file."""
    try:
        base_dir = Path(__file__).parent
    except NameError:
        base_dir = Path.cwd()

    folder = "outputs"
    outputs_dir = base_dir / folder
    outputs_dir.mkdir(parents=True, exist_ok=True)

    output_path = outputs_dir / filename

    # Ensure the content is proper HTML
    if not html_content.strip().startswith('<!DOCTYPE html>'):
        if '<html' in html_content:
            html_content = f"<!DOCTYPE html>\n{html_content}"
        else:
            html_content = f"""<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
{html_content}
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")
    return str(output_path)


@tool("copy_html_file")
def copy_html_file(source_file_path: str, destination_filename: str = "final_page.html") -> str:
    """Copy an existing HTML file to a new location with a new name."""
    try:
        base_dir = Path(__file__).parent
    except NameError:
        base_dir = Path.cwd()

    folder = "outputs"
    outputs_dir = base_dir / folder
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # Read the source file
    source_path = Path(source_file_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_file_path}")

    html_content = source_path.read_text(encoding="utf-8")

    # Save to destination
    output_path = outputs_dir / destination_filename
    output_path.write_text(html_content, encoding="utf-8")
    return str(output_path)