import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from AIApp.models import PortfolioTemplate


class Command(BaseCommand):
    help = 'Populate PortfolioTemplate model with JSON data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing templates before adding new ones',
        )
        parser.add_argument(
            '--json-file',
            type=str,
            help='Path to JSON file (optional, defaults to embedded data)',
        )

    def handle(self, *args, **options):
        # JSON data embedded in the command
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
        if options['json_file']:
            try:
                with open(options['json_file'], 'r', encoding='utf-8') as file:
                    templates_data = json.load(file)
                self.stdout.write(
                    self.style.SUCCESS(f'Loaded data from {options["json_file"]}')
                )
            except FileNotFoundError:
                raise CommandError(f'File {options["json_file"]} not found')
            except json.JSONDecodeError as e:
                raise CommandError(f'Invalid JSON in file: {e}')

        # Clear existing templates if requested
        if options['clear']:
            deleted_count = PortfolioTemplate.objects.count()
            PortfolioTemplate.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Cleared {deleted_count} existing templates')
            )

        created_count = 0
        updated_count = 0
        error_count = 0

        try:
            with transaction.atomic():
                for category, templates in templates_data.items():
                    self.stdout.write(f'\nProcessing category: {category}')
                    
                    for template_data in templates:
                        try:
                            # Generate file path template
                            file_path_template = f"Portfolio/{category}/Example1/{template_data['name']}"
                            
                            # Check if template already exists
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
                                self.stdout.write(
                                    self.style.SUCCESS(f'  ✓ Created: {template_data["name"]}')
                                )
                            else:
                                # Update existing template
                                template_obj.category = category
                                template_obj.display_name = template_data['display_name']
                                template_obj.description = template_data['description']
                                template_obj.file_path_template = file_path_template
                                template_obj.save()
                                
                                updated_count += 1
                                self.stdout.write(
                                    self.style.WARNING(f'  ↻ Updated: {template_data["name"]}')
                                )
                                
                        except Exception as e:
                            error_count += 1
                            self.stdout.write(
                                self.style.ERROR(f'  ✗ Error with {template_data["name"]}: {str(e)}')
                            )

        except Exception as e:
            raise CommandError(f'Transaction failed: {str(e)}')

        # Print summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'📊 SUMMARY:'))
        self.stdout.write(self.style.SUCCESS(f'  Created: {created_count} templates'))
        self.stdout.write(self.style.WARNING(f'  Updated: {updated_count} templates'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  Errors: {error_count} templates'))
        
        total_templates = PortfolioTemplate.objects.count()
        self.stdout.write(self.style.SUCCESS(f'  Total templates in database: {total_templates}'))
        self.stdout.write('='*50)

        if error_count == 0:
            self.stdout.write(
                self.style.SUCCESS('🎉 Templates population completed successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Templates population completed with some errors.')
            )
