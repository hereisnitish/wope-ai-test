import os
from typing import List
import shutil
from pathlib import Path
from dotenv import load_dotenv
from crewai.tools import tool
from .openai_page_generator import make_website
from ..models import PortfolioTemplate
import openai


from django.db.models import FloatField
from django.db.models.expressions import RawSQL



BASE_PROJECT_DIR = os.path.join("AIAPP")

#utility functions
def get_user_input(prompt: str) -> str:
    print(f"\n🤖 {prompt}")
    return input("👤 You: ").strip()



#All tools

@tool("get_existing_components")
def get_existing_components(category: str) -> List[PortfolioTemplate]:
    """Get existing portfolio template components by category."""

    query_text = f"Get me {category} components"
    data = get_vector_data(query_text)

    return data



def get_vector_data(query_text= "footer"):
    # text from user
    threshold = 0.2

    # Step 1: Get embedding vector from OpenAI

    client = openai.OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query_text
    )
    query_vector = response.data[0].embedding
    threshold = 0.2
    results = PortfolioTemplate.objects.annotate(
    similarity=RawSQL(
        "1 - (embedding <=> %s::vector)",  # <=> is cosine distance in pgvector
        (query_vector,),
        output_field=FloatField()
    )
    ).filter(similarity__gte=threshold).order_by('-similarity')
    
    data = []
    for t in results:
        if t.similarity >= 0.4:
            data.append({
                "name": t.name,
                "display_name": t.display_name,
                "description": t.description,
                "file_path_template": t.file_path_template,
                "content":t.content
            })

    return data


@tool("create_css_file")
def create_css_file(css_content: str) -> str:
    """Create a CSS file and return the file path. Don't include <style> tag in the css file."""
    path_name  =  make_website(website_input=f"Make me {css_content} css file", filename=f"styles.css")
    return path_name


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
    <link rel="stylesheet" href="style.css" />
    
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
    <link rel="stylesheet" href="style.css" />
</head>
<body>
{html_content}
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")
    return str(output_path)


def save_css_file():
    BASE_PROJECT_DIR = os.path.join("AIApp")

    # Define source and destination paths relative to BASE_PROJECT_DIR
    source_file = os.path.join(BASE_PROJECT_DIR, 'typography', 'style.css')
    destination_file = os.path.join(BASE_PROJECT_DIR, 'Crew', 'outputs', 'style.css')

    # Create the destination directory if it doesn't exist
    os.makedirs(os.path.dirname(destination_file), exist_ok=True)

    # Copy the file
    try:
        shutil.copy2(source_file, destination_file)
        print(f"File copied successfully from {source_file} to {destination_file}")
    except FileNotFoundError:
        print("Source file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None




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
    save_css_file()
    return str(output_path)