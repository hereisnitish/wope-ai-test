import os
from typing import List, Dict, Any
import shutil
from pathlib import Path
from dotenv import load_dotenv
from crewai.tools import tool
from .openai_page_generator import make_website
from ..models import PortfolioTemplate, Project, Page, Section, Chunk
import openai
import re
from langchain_openai import ChatOpenAI
from langsmith import Client
from langchain_openai import OpenAIEmbeddings
from django.db.models import FloatField
from django.db.models.expressions import RawSQL
from django.db import transaction
from bs4 import BeautifulSoup
import uuid
import hashlib

# client = openai.OpenAI()
client = ChatOpenAI(model="gpt-5", temperature=0)
langsmith_client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"))


BASE_PROJECT_DIR = os.path.join("AIAPP")

#utility functions
def get_user_input(prompt: str) -> str:
    print(f"\n🤖 {prompt}")
    return input("👤 You: ").strip()



#All tools

@tool("get_existing_components")
def get_existing_components(categories: List[str]) -> List[PortfolioTemplate]:
    """Get existing portfolio template components by categories list."""

    
    
    for category in categories:
        query_text = f"Get me {category} components"
        data = get_vector_data(query_text, category)
        
        # Add category info to each component for identification
        

    return {f"components for {category} created successfully"}

def html_file_creator(data):
    file_path = "result.html"
    content = data[0].get("content", "")
    
    # Skip processing if content is empty
    if not content or not content.strip():
        print("⚠️ No content found, skipping HTML file creation.")
        return

    # Remove <style> blocks (they go to CSS file)
    content_no_style = re.sub(r"<style.*?>.*?</style>", "", content, flags=re.DOTALL|re.IGNORECASE)

    # Capture valid HTML blocks (section/nav/header/footer) - capture the full block
    block_pattern = r"<(section|nav|header|footer)[^>]*>.*?</\1>"
    blocks = [match.group(0) for match in re.finditer(block_pattern, content_no_style, flags=re.DOTALL|re.IGNORECASE)]

    # Create base HTML if file doesn't exist
    if not os.path.exists(file_path):
        base_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Result Page</title>
  <link rel="stylesheet" href="result.css">
</head>
<body>
</body>
</html>
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(base_html)

    # Read existing HTML content
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Insert only unique blocks before </body>
    new_blocks_added = 0
    for block in blocks:
        if block not in html_content:
            # Insert before </body> tag
            html_content = html_content.replace("</body>", f"{block}\n</body>")
            new_blocks_added += 1

    # Write the updated content back to file
    if new_blocks_added > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ {new_blocks_added} unique HTML blocks appended into {file_path}.")
    else:
        print(f"ℹ️ No new unique blocks found to add to {file_path}.")
    

def create_css_for_html(html_content):
    
    llm = ChatOpenAI(model="gpt-5", temperature=0)
    
    instructions=f"""
You are an assistant that generates CSS for a given HTML component.

Instructions:
- Analyze the HTML component and generate the CSS for the component.
- Your response must contain only the code for the component—no explanations, comments, or extra text.
- The component should be visually appealing, production-ready, and responsive.
- The code you provide will be inserted directly into an existing CSS file, so ensure it works standalone.
- Keep your code clean and well-structured.

HTML:
{html_content}
"""
    
    response = llm.invoke(instructions)
    return response.content
    


def css_file_creator(data):
    file_path = "result.css"
    content = data[0].get("css_content", "") or data[0].get("css_content", "")
    
    if not content:
        generated_css = create_css_for_html(data[0].get("content", ""))
        # Save generated CSS to DB
        obj = PortfolioTemplate.objects.filter(name=data[0].get("name")).first()
        if obj:
            obj.css_content = generated_css
            obj.save()
            print(f"💾 CSS saved to DB for component: {obj.name}")

        content = generated_css
    
    variable_content = '''
    
    
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* CSS Custom Properties (Variables) */
:root {
    /* Color Palette */
    --primary-color: #6c63ff;       /* Vibrant Indigo */
    --primary-dark: #4b47d6;        /* Deeper Indigo */
    --primary-light: #a5b4fc;       /* Light Indigo */
    --secondary-color: #00c9a7;     /* Aqua Teal */
    --accent-color: #ffb347;        /* Soft Amber */
    
    /* Text Colors */
    --text-primary: #1a1a2e;        /* Deep Navy */
    --text-secondary: #4e4e6a;      /* Muted Indigo-Gray */
    --text-light: #a0aec0;          /* Soft Gray */
    
    /* Background Colors */
    --bg-primary: #ffffff;          /* Pure White */
    --bg-secondary: #f7f9fc;        /* Light Neutral */
    --bg-card: #ffffff;             /* Card Background */
    --bg-dark: #1a1a2e;             /* Matching Deep Navy */
    --border-color: #e2e8f0;        /* Neutral Border */
    
    /* Gradients */
    --gradient-primary: linear-gradient(135deg, #6c63ff, #48c6ef);  /* Indigo → Sky Blue */
    --gradient-secondary: linear-gradient(135deg, #00c9a7, #92fe9d);/* Aqua → Soft Green */
    --gradient-accent: linear-gradient(135deg, #ffb347, #ffcc70);   /* Amber → Light Gold */
    
    /* Shadows */
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
    
    /* Typography */
    --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    --spacing-3xl: 4rem;
    
    /* Border Radius */
    --radius-sm: 0.375rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-2xl: 1.5rem;
    
    /* Transitions */
    --transition-fast: 150ms ease-in-out;
    --transition-base: 250ms ease-in-out;
    --transition-slow: 350ms ease-in-out;
}
    
    '''
    
    # Skip processing if content is empty
    if not content or not content.strip():
        print("⚠️ No CSS content found, skipping CSS file creation.")
        return

    # Extract inside of <style> tags if present
    css_content = re.sub(r"</?style.*?>", "", content, flags=re.DOTALL|re.IGNORECASE).strip()

    # Ensure file exists
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(variable_content)

    with open(file_path, "r", encoding="utf-8") as f:
        existing_css = f.read()

    # Append only if not duplicate
    if css_content not in existing_css:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(css_content + "\n\n")
        print(f"✅ Unique CSS content appended to {file_path}.")
    else:
        print(f"⚠️ CSS already exists in {file_path}, skipped.")



def get_vector_data(query_text= "footer",category= "footer"):

    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

    query_vector = embeddings_model.embed_query(query_text)
        
    
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
                "content":t.content,
                "css_content":t.css_content
            })
    
    # Only create files if we have data
    if data:
        html_file_creator(data)
        css_file_creator(data)
    else:
        print("⚠️ No matching components found, skipping file creation.")
    
    return f"component {category} created successfully"


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
    # save_css_file()
    return str(output_path)

# =============================================================================
# HTML PARSING AND TEXT EXTRACTION FUNCTIONS
# =============================================================================

def extract_text_from_html(html_content: str) -> str:
    """Extract clean text content from HTML for embedding."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text and clean it up
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def parse_html_sections(html_content: str) -> List[Dict[str, Any]]:
    """Parse HTML content and extract sections."""
    soup = BeautifulSoup(html_content, 'html.parser')
    sections = []
    
    # Define section types and their corresponding HTML tags
    section_mapping = {
        'header': ['header', 'nav'],
        'hero': ['section.hero', 'div.hero', 'section.banner'],
        'about': ['section.about', 'div.about'],
        'portfolio': ['section.portfolio', 'div.portfolio', 'section.projects'],
        'skills': ['section.skills', 'div.skills'],
        'experience': ['section.experience', 'div.experience'],
        'contact': ['section.contact', 'div.contact'],
        'footer': ['footer']
    }
    
    section_order = 0
    
    for section_type, selectors in section_mapping.items():
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                if element.get_text().strip():  # Only include non-empty sections
                    section_id = f"{section_type}_{section_order}"
                    sections.append({
                        'section_id': section_id,
                        'section_name': f"{section_type.title()} Section",
                        'section_type': section_type,
                        'html_content': str(element),
                        'text_content': extract_text_from_html(str(element)),
                        'order': section_order
                    })
                    section_order += 1
    
    # If no specific sections found, create a general section
    if not sections:
        sections.append({
            'section_id': 'main_content',
            'section_name': 'Main Content',
            'section_type': 'other',
            'html_content': html_content,
            'text_content': extract_text_from_html(html_content),
            'order': 0
        })
    
    return sections

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """Split text into chunks for embedding."""
    if len(text) <= chunk_size:
        return [{
            'chunk_id': hashlib.md5(text.encode()).hexdigest()[:8],
            'chunk_name': 'Full Content',
            'html_content': text,
            'text_content': text,
            'chunk_size': len(text),
            'order': 0
        }]
    
    chunks = []
    start = 0
    chunk_order = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text_content = text[start:end]
        
        # Try to break at sentence boundary
        if end < len(text):
            last_period = chunk_text_content.rfind('.')
            last_exclamation = chunk_text_content.rfind('!')
            last_question = chunk_text_content.rfind('?')
            
            last_sentence_end = max(last_period, last_exclamation, last_question)
            if last_sentence_end > start + chunk_size // 2:  # Don't make chunks too small
                end = start + last_sentence_end + 1
                chunk_text_content = text[start:end]
        
        chunk_id = hashlib.md5(chunk_text_content.encode()).hexdigest()[:8]
        
        chunks.append({
            'chunk_id': chunk_id,
            'chunk_name': f'Chunk {chunk_order + 1}',
            'html_content': chunk_text_content,  # For HTML chunks, we'll use the same content
            'text_content': chunk_text_content,
            'chunk_size': len(chunk_text_content),
            'order': chunk_order
        })
        
        start = end - overlap
        chunk_order += 1
    
    return chunks

# =============================================================================
# DATABASE OPERATIONS
# =============================================================================

@transaction.atomic
def create_project(project_id: str, project_name: str, description: str, html_file_path: str) -> Project:
    """Create a new project in the database."""
    project, created = Project.objects.get_or_create(
        project_id=project_id,
        defaults={
            'project_name': project_name,
            'description': description,
            'html_file_path': html_file_path
        }
    )
    
    if created:
        print(f"✅ Created new project: {project_name} ({project_id})")
    else:
        print(f"ℹ️ Project already exists: {project_name} ({project_id})")
    
    return project

@transaction.atomic
def create_page(project: Project, page_id: str, page_name: str, page_type: str, html_content: str) -> Page:
    """Create a new page in the database."""
    page, created = Page.objects.get_or_create(
        project=project,
        page_id=page_id,
        defaults={
            'page_name': page_name,
            'page_type': page_type,
            'html_content': html_content
        }
    )
    
    if created:
        print(f"✅ Created new page: {page_name} ({page_id})")
    else:
        print(f"ℹ️ Page already exists: {page_name} ({page_id})")
    
    return page

@transaction.atomic
def create_section(page: Page, section_data: Dict[str, Any]) -> Section:
    """Create a new section in the database."""
    section, created = Section.objects.get_or_create(
        page=page,
        section_id=section_data['section_id'],
        defaults={
            'section_name': section_data['section_name'],
            'section_type': section_data['section_type'],
            'html_content': section_data['html_content'],
            'order': section_data['order']
        }
    )
    
    if created:
        print(f"✅ Created new section: {section_data['section_name']} ({section_data['section_id']})")
    else:
        print(f"ℹ️ Section already exists: {section_data['section_name']} ({section_data['section_id']})")
    
    return section

@transaction.atomic
def create_chunk_with_embedding(section: Section, chunk_data: Dict[str, Any], embedding: List[float]) -> Chunk:
    """Create a new chunk with embedding in the database."""
    chunk, created = Chunk.objects.get_or_create(
        section=section,
        chunk_id=chunk_data['chunk_id'],
        defaults={
            'chunk_name': chunk_data['chunk_name'],
            'html_content': chunk_data['html_content'],
            'text_content': chunk_data['text_content'],
            'embedding': embedding,
            'chunk_size': chunk_data['chunk_size'],
            'order': chunk_data['order']
        }
    )
    
    if created:
        print(f"✅ Created new chunk with embedding: {chunk_data['chunk_name']} ({chunk_data['chunk_id']})")
    else:
        # Update embedding if chunk exists but embedding is different
        if chunk.embedding != embedding:
            chunk.embedding = embedding
            chunk.save()
            print(f"🔄 Updated embedding for chunk: {chunk_data['chunk_name']} ({chunk_data['chunk_id']})")
        else:
            print(f"ℹ️ Chunk already exists: {chunk_data['chunk_name']} ({chunk_data['chunk_id']})")
    
    return chunk

# =============================================================================
# EMBEDDING GENERATION
# =============================================================================

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for text using OpenAI."""
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings_model.embed_query(text)

# =============================================================================
# MAIN ORCHESTRATION FUNCTION
# =============================================================================

@tool("save_html_to_database_with_embeddings")
def save_html_to_database_with_embeddings():
    """
    Parse HTML file and save to database with embeddings.
    
    Args:
        html_file_path: Path to the HTML file
        project_name: Name for the project
        project_description: Description of the project
        page_name: Name for the page
        page_type: Type of page (home, about, portfolio, contact, blog, services, other)
    
    Returns:
        Success message with details
    """
    try:
        html_file_path= "result.html"
        project_name=  "Project 1"
        project_description = "Project 1 Description"
        page_name = "Main Page"
        page_type = "home"
        # Read HTML file
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate unique project ID
        project_id = hashlib.md5(f"{project_name}_{html_file_path}".encode()).hexdigest()[:12]
        page_id = hashlib.md5(f"{page_name}_{project_id}".encode()).hexdigest()[:12]
        
        # Create project
        project = create_project(
            project_id=project_id,
            project_name=project_name,
            description=project_description,
            html_file_path=html_file_path
        )
        
        # Create page
        page = create_page(
            project=project,
            page_id=page_id,
            page_name=page_name,
            page_type=page_type,
            html_content=html_content
        )
        
        # Parse sections from HTML
        sections_data = parse_html_sections(html_content)
        print(f"📄 Found {len(sections_data)} sections in HTML")
        
        total_chunks = 0
        
        # Process each section
        for section_data in sections_data:
            # Create section
            section = create_section(page, section_data)
            
            # Create chunks for this section
            chunks_data = chunk_text(section_data['text_content'])
            print(f"📦 Created {len(chunks_data)} chunks for section: {section_data['section_name']}")
            
            # Process each chunk
            for chunk_data in chunks_data:
                # Generate embedding for the chunk
                embedding = generate_embedding(chunk_data['text_content'])
                
                # Create chunk with embedding
                create_chunk_with_embedding(section, chunk_data, embedding)
                total_chunks += 1
        
        return f"""
✅ Successfully saved HTML to database with embeddings!

📊 Summary:
- Project: {project_name} ({project_id})
- Page: {page_name} ({page_id})
- Sections: {len(sections_data)}
- Total Chunks with Embeddings: {total_chunks}
- File: {html_file_path}
        """
        
    except Exception as e:
        return f"❌ Error saving HTML to database: {str(e)}"

# # =============================================================================
# # UTILITY FUNCTIONS FOR SEARCHING EMBEDDINGS
# # =============================================================================

# @tool("search_chunks_by_similarity")
# def search_chunks_by_similarity(
#     query_text: str,
#     project_id: str = None,
#     page_type: str = None,
#     section_type: str = None,
#     limit: int = 5,
#     threshold: float = 0.7
# ) -> List[Dict[str, Any]]:
#     """
#     Search for similar chunks using vector similarity.
    
#     Args:
#         query_text: Text to search for
#         project_id: Filter by specific project (optional)
#         page_type: Filter by page type (optional)
#         section_type: Filter by section type (optional)
#         limit: Maximum number of results
#         threshold: Minimum similarity threshold
    
#     Returns:
#         List of similar chunks with metadata
#     """
#     try:
#         # Generate embedding for query
#         query_embedding = generate_embedding(query_text)
        
#         # Build base queryset
#         queryset = Chunk.objects.filter(is_active=True)
        
#         # Apply filters
#         if project_id:
#             queryset = queryset.filter(section__page__project__project_id=project_id)
#         if page_type:
#             queryset = queryset.filter(section__page__page_type=page_type)
#         if section_type:
#             queryset = queryset.filter(section__section_type=section_type)
        
#         # Add similarity calculation
#         results = queryset.annotate(
#             similarity=RawSQL(
#                 "1 - (embedding <=> %s::vector)",
#                 (query_embedding,),
#                 output_field=FloatField()
#             )
#         ).filter(similarity__gte=threshold).order_by('-similarity')[:limit]
        
#         # Format results
#         similar_chunks = []
#         for chunk in results:
#             similar_chunks.append({
#                 'chunk_id': chunk.chunk_id,
#                 'chunk_name': chunk.chunk_name,
#                 'text_content': chunk.text_content[:200] + "..." if len(chunk.text_content) > 200 else chunk.text_content,
#                 'similarity': float(chunk.similarity),
#                 'project_name': chunk.section.page.project.project_name,
#                 'page_name': chunk.section.page.page_name,
#                 'section_name': chunk.section.section_name,
#                 'section_type': chunk.section.section_type
#             })
        
#         return similar_chunks
        
#     except Exception as e:
#         return [{"error": f"Search failed: {str(e)}"}]

# @tool("get_project_statistics")
# def get_project_statistics(project_id: str = None) -> Dict[str, Any]:
#     """
#     Get statistics for a project or all projects.
    
#     Args:
#         project_id: Specific project ID (optional)
    
#     Returns:
#         Dictionary with project statistics
#     """
#     try:
#         if project_id:
#             projects = Project.objects.filter(project_id=project_id, is_active=True)
#         else:
#             projects = Project.objects.filter(is_active=True)
        
#         stats = {
#             'total_projects': projects.count(),
#             'projects': []
#         }
        
#         for project in projects:
#             pages = project.pages.filter(is_active=True)
#             sections = Section.objects.filter(page__in=pages, is_active=True)
#             chunks = Chunk.objects.filter(section__in=sections, is_active=True)
            
#             project_stats = {
#                 'project_id': project.project_id,
#                 'project_name': project.project_name,
#                 'total_pages': pages.count(),
#                 'total_sections': sections.count(),
#                 'total_chunks': chunks.count(),
#                 'chunks_with_embeddings': chunks.exclude(embedding__isnull=True).count()
#             }
            
#             stats['projects'].append(project_stats)
        
#         return stats
        
#     except Exception as e:
#         return {"error": f"Failed to get statistics: {str(e)}"}    