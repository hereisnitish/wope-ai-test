#!/usr/bin/env python
"""
Standalone script to populate PortfolioTemplate model with JSON data.
This can be used as an alternative to the Django management command.

Usage:
    python populate_portfolio_templates.py
    
Make sure to set DJANGO_SETTINGS_MODULE environment variable if needed.
"""

import os
import sys
import json
import django
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WopeAIProject.settings')
django.setup()

from django.db import transaction
from AIApp.models import PortfolioTemplate


def populate_templates(clear_existing=False, json_file_path=None):
    """
    Populate PortfolioTemplate model with JSON data.
    
    Args:
        clear_existing (bool): Clear existing templates before adding new ones
        json_file_path (str): Path to JSON file (optional, defaults to embedded data)
    
    Returns:
        dict: Summary of operation results
    """
    
    # Embedded JSON data
    templates_data = {
        "Hero": [
            {
                "name": "hero1",
                "display_name": "Simple Welcome Hero",
                "description": "Clean and minimal hero section with welcome message, subtitle, and contact button. Perfect for a straightforward introduction."
            },
            {
                "name": "hero2", 
                "display_name": "Image Background Hero",
                "description": "Hero section with background image overlay, personal introduction, and call-to-action button linking to work portfolio."
            }
        ],
        "About": [
            {
                "name": "about1",
                "display_name": "Stats-Based About",
                "description": "Professional about section featuring personal introduction with key statistics cards showing projects completed, years of experience, and happy clients."
            },
            {
                "name": "about2",
                "display_name": "Profile & Skills About", 
                "description": "Comprehensive about section with profile image, social media links, skills overview with icons, and downloadable CV button."
            }
        ],
        "Skills": [
            {
                "name": "skills1",
                "display_name": "Category Grid Skills",
                "description": "Interactive skills section organized in categories (Frontend, Backend, Tools) with hover tooltips and detailed descriptions for each technology."
            },
            {
                "name": "skills2",
                "display_name": "Progress Bar Skills", 
                "description": "Visual skills representation using animated progress bars with percentage levels, plus summary cards highlighting specialization areas."
            }
        ],
        "Projects": [
            {
                "name": "projects1",
                "display_name": "Filterable Project Grid",
                "description": "Interactive project showcase with filtering tabs by category (Web Apps, Mobile, Design), hover overlays with preview/code links, and technology tags."
            },
            {
                "name": "projects2",
                "display_name": "Masonry Project Gallery",
                "description": "Pinterest-style masonry layout for projects with modal popup system for detailed project information and navigation between projects."
            }
        ],
        "Testimonials": [
            {
                "name": "testimonials1",
                "display_name": "Client Testimonial Cards",
                "description": "Grid layout of client testimonials featuring quote icons, client feedback, profile photos, company information, and 5-star ratings."
            }
        ],
        "Contact": [
            {
                "name": "contact1",
                "display_name": "Traditional Contact Form",
                "description": "Classic contact section with contact information cards (email, phone, location) and fully validated contact form with error handling."
            },
            {
                "name": "contact2", 
                "display_name": "Modern Contact Cards",
                "description": "Contemporary contact design with interactive contact method cards, social media integration, and quick contact modal popup."
            }
        ],
        "Footer": [
            {
                "name": "footer1",
                "display_name": "Standard Business Footer",
                "description": "Comprehensive footer with brand section, quick navigation links, service listings, contact information, and social media icons with back-to-top button."
            },
            {
                "name": "footer2",
                "display_name": "Premium Newsletter Footer",
                "description": "Advanced footer featuring newsletter subscription, company statistics, enhanced social media cards, contact details with availability hours, and floating visual elements."
            }
        ]
    }

    # Load from file if specified
    if json_file_path:
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                templates_data = json.load(file)
            print(f"✓ Loaded data from {json_file_path}")
        except FileNotFoundError:
            print(f"✗ Error: File {json_file_path} not found")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Error: Invalid JSON in file: {e}")
            return None

    # Clear existing templates if requested
    if clear_existing:
        deleted_count = PortfolioTemplate.objects.count()
        PortfolioTemplate.objects.all().delete()
        print(f"⚠️  Cleared {deleted_count} existing templates")

    created_count = 0
    updated_count = 0
    error_count = 0
    errors = []

    try:
        with transaction.atomic():
            for category, templates in templates_data.items():
                print(f"\n📁 Processing category: {category}")
                
                for template_data in templates:
                    try:
                        # Generate file path template following the pattern
                        file_path_template = f"Portfolio/{category}/Example1/{template_data['name']}"
                        
                        # Check if template already exists (by name)
                        template_obj, created = PortfolioTemplate.objects.get_or_create(
                            name=template_data['name'],
                            defaults={
                                'category': category,
                                'display_name': template_data['display_name'],
                                'description': template_data['description'],
                                'file_path_template': file_path_template,
                                'is_active': True,
                            }
                        )
                        
                        if created:
                            created_count += 1
                            print(f"  ✓ Created: {template_data['name']}")
                        else:
                            # Update existing template
                            template_obj.category = category
                            template_obj.display_name = template_data['display_name']
                            template_obj.description = template_data['description']
                            template_obj.file_path_template = file_path_template
                            template_obj.save()
                            
                            updated_count += 1
                            print(f"  ↻ Updated: {template_data['name']}")
                            
                    except Exception as e:
                        error_count += 1
                        error_msg = f"Error with {template_data['name']}: {str(e)}"
                        errors.append(error_msg)
                        print(f"  ✗ {error_msg}")

    except Exception as e:
        print(f"✗ Transaction failed: {str(e)}")
        return None

    # Print summary
    print('\n' + '='*60)
    print('📊 POPULATION SUMMARY:')
    print(f'  ✅ Created: {created_count} templates')
    print(f'  🔄 Updated: {updated_count} templates')
    if error_count > 0:
        print(f'  ❌ Errors: {error_count} templates')
    
    total_templates = PortfolioTemplate.objects.count()
    print(f'  📈 Total templates in database: {total_templates}')
    print('='*60)

    if error_count == 0:
        print('🎉 Templates population completed successfully!')
    else:
        print('⚠️  Templates population completed with some errors:')
        for error in errors:
            print(f'    - {error}')

    return {
        'created': created_count,
        'updated': updated_count,
        'errors': error_count,
        'total': total_templates,
        'error_details': errors
    }


def main():
    """Main function to run the script."""
    print("🚀 Starting Portfolio Template Population")
    print("="*60)
    
    # You can modify these parameters as needed
    result = populate_templates(
        clear_existing=False,  # Set to True to clear existing templates
        json_file_path=None    # Set to file path to load from external JSON
    )
    
    if result:
        print(f"\n📋 Operation completed successfully!")
        return 0
    else:
        print(f"\n❌ Operation failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
