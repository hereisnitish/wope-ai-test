import os
import sys
import json
import django
from pathlib import Path
import openai
client = openai.OpenAI()
# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WopeAIProject.settings')
django.setup()

from django.db import transaction
from AIApp.models import PortfolioTemplate
from django.conf import settings



BASE_DIR = PROJECT_ROOT / 'websites/components'

def read_html_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"✗ Error reading {file_path}: {e}")
        return ""
    
def read_css_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"✗ Error reading {file_path}: {e}")
        return ""

def generate_embedding(text):
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"✗ Embedding generation failed: {e}")
        return None

def read_js_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"✗ Error reading {file_path}: {e}")
        return ""

def extract_category_from_filename(filename):
    """Extract category from filename like 'about_section.html' -> 'about'"""
    # Remove file extension
    name = filename.split('.')[0]
    # Split by underscore and take the first part
    parts = name.split('_')
    if len(parts) > 1:
        return parts[0]
    return name

def group_files_by_base_name(files):
    """Group files by their base name (without extension and version number)"""
    grouped = {}
    
    for file in files:
        if not file.is_file():
            continue
            
        # Get base name without extension
        base_name = file.stem
        
        # Remove version numbers (e.g., about_section1 -> about_section)
        import re
        base_name_clean = re.sub(r'\d+$', '', base_name)
        
        if base_name_clean not in grouped:
            grouped[base_name_clean] = {}
        
        # Determine file type
        if file.suffix == '.html':
            grouped[base_name_clean]['html'] = file
        elif file.suffix == '.css':
            grouped[base_name_clean]['css'] = file
        elif file.suffix == '.js':
            grouped[base_name_clean]['js'] = file
    
    return grouped

def populate_templates(clear_existing=False):
    if clear_existing:
        deleted_count = PortfolioTemplate.objects.count()
        PortfolioTemplate.objects.all().delete()
        print(f"⚠️  Cleared {deleted_count} existing templates")

    created_count = 0
    updated_count = 0
    error_count = 0

    try:
        with transaction.atomic():
            # Get all files in the components directory
            all_files = list(BASE_DIR.iterdir())
            
            # Group files by their base names
            grouped_files = group_files_by_base_name(all_files)
            
            print(f"\n📁 Found {len(grouped_files)} component groups to process")

            for base_name, files in grouped_files.items():
                # Skip files that don't have HTML content
                if 'html' not in files:
                    print(f"✗ Skipping {base_name}: No HTML file found")
                    error_count += 1
                    continue
                
                html_file = files['html']
                css_file = files.get('css')
                js_file = files.get('js')
                
                # Extract category from filename
                category = extract_category_from_filename(html_file.name)
                
                print(f"\n📁 Processing: {base_name} (category: {category})")

                # Read file contents
                content = read_html_content(html_file)
                css_content = read_css_content(css_file) if css_file else ""
                js_content = read_js_content(js_file) if js_file else ""
                
                # Combine all content for embedding
                combined_content = content
                if css_content:
                    combined_content += f"\n\n<!-- CSS -->\n<style>\n{css_content}\n</style>"
                if js_content:
                    combined_content += f"\n\n<!-- JavaScript -->\n<script>\n{js_content}\n</script>"

                # Generate embedding from combined content
                embedding = generate_embedding(combined_content)

                if not embedding:
                    print(f"✗ Skipping {base_name} due to embedding error")
                    error_count += 1
                    continue

                # Create display name and description
                display_name = f"{base_name.replace('_', ' ').title()} ({category})"
                description = f"{category} component - {base_name.replace('_', ' ')}"
                file_path_template = str(html_file.relative_to(BASE_DIR.parent))

                try:
                    template_obj, created = PortfolioTemplate.objects.get_or_create(
                        name=base_name,
                        defaults={
                            'category': category,
                            'display_name': display_name,
                            'description': description,
                            'file_path_template': file_path_template,
                            'content': combined_content,
                            'css_content': css_content,
                            'embedding': embedding,
                            'is_active': True
                        }
                    )

                    if created:
                        created_count += 1
                        print(f"  ✓ Created: {base_name}")
                    else:
                        template_obj.category = category
                        template_obj.display_name = display_name
                        template_obj.description = description
                        template_obj.file_path_template = file_path_template
                        template_obj.content = combined_content
                        template_obj.css_content = css_content
                        template_obj.embedding = embedding
                        template_obj.save()
                        updated_count += 1
                        print(f"  ↻ Updated: {base_name}")

                except Exception as e:
                    error_count += 1
                    print(f"  ✗ Error processing {base_name}: {e}")

    except Exception as e:
        print(f"✗ Transaction failed: {e}")
        return

    print("\n" + "="*60)
    print("📊 POPULATION SUMMARY")
    print(f"  ✅ Created: {created_count}")
    print(f"  🔄 Updated: {updated_count}")
    print(f"  ❌ Errors: {error_count}")
    print("="*60)

def main():
    print("🚀 Starting Portfolio Template Population")
    print("="*60)
    populate_templates(clear_existing=False)

if __name__ == "__main__":
    main()
