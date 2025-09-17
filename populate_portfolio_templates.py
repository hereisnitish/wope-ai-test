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



BASE_DIR = PROJECT_ROOT / 'Portfolio'

def read_html_content(file_path):
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
            for category_dir in BASE_DIR.iterdir():
                if not category_dir.is_dir():
                    continue
                
                category = category_dir.name
                print(f"\n📁 Processing category: {category}")

                for example_dir in category_dir.iterdir():
                    if not example_dir.is_dir():
                        continue

                    html_file = None
                    for file in example_dir.iterdir():
                        if file.suffix == '.html' and 'consolidated' not in file.name:
                            html_file = file
                            break

                    if not html_file:
                        print(f"✗ No valid HTML file found in {example_dir}")
                        error_count += 1
                        continue

                    name = html_file.stem
                    display_name = f"{name.replace('_', ' ').title()} ({category})"
                    description = f"{category} component example from {example_dir.name}"
                    file_path_template = str(html_file.relative_to(BASE_DIR.parent))
                    content = read_html_content(html_file)

                    # Generate embedding
                    embedding = generate_embedding(content)

                    if not embedding:
                        print(f"✗ Skipping {name} due to embedding error")
                        error_count += 1
                        continue

                    try:
                        template_obj, created = PortfolioTemplate.objects.get_or_create(
                            name=name,
                            defaults={
                                'category': category,
                                'display_name': display_name,
                                'description': description,
                                'file_path_template': file_path_template,
                                'content': content,
                                'embedding': embedding,
                                'is_active': True
                            }
                        )

                        if created:
                            created_count += 1
                            print(f"  ✓ Created: {name}")
                        else:
                            template_obj.category = category
                            template_obj.display_name = display_name
                            template_obj.description = description
                            template_obj.file_path_template = file_path_template
                            template_obj.content = content
                            template_obj.embedding = embedding
                            template_obj.save()
                            updated_count += 1
                            print(f"  ↻ Updated: {name}")

                    except Exception as e:
                        error_count += 1
                        print(f"  ✗ Error processing {name}: {e}")

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
