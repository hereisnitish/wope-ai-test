"""
Django management command to populate the vector database with HTML content.

This command processes HTML files from the Portfolio directory and creates
vector embeddings for semantic search capabilities.

Usage:
    python manage.py populate_vector_db
    python manage.py populate_vector_db --portfolio-dir /path/to/portfolio
    python manage.py populate_vector_db --category Hero
    python manage.py populate_vector_db --clear-existing
"""

import os
import logging
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from AIApp.pg_vector import HTMLVectorProcessor, HTMLVectorDocument, setup_pgvector_extension

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Populate the vector database with HTML content from portfolio files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--portfolio-dir',
            type=str,
            default='Portfolio',
            help='Path to the portfolio directory (default: Portfolio)'
        )
        parser.add_argument(
            '--category',
            type=str,
            help='Process only specific category (Hero, About, Contact, etc.)'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing vector documents before processing'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without actually doing it'
        )
        parser.add_argument(
            '--setup-extension',
            action='store_true',
            help='Set up pgvector extension and indexes'
        )

    def handle(self, *args, **options):
        """Main command handler."""
        try:
            # Set up logging
            logging.basicConfig(level=logging.INFO)
            
            # Setup pgvector extension if requested
            if options['setup_extension']:
                self.stdout.write("Setting up pgvector extension...")
                setup_pgvector_extension()
                self.stdout.write(
                    self.style.SUCCESS("pgvector extension setup completed")
                )
                return
            
            # Clear existing data if requested
            if options['clear_existing']:
                self.clear_existing_data()
            
            # Get portfolio directory path
            portfolio_dir = options['portfolio_dir']
            if not os.path.isabs(portfolio_dir):
                portfolio_dir = os.path.join(settings.BASE_DIR, portfolio_dir)
            
            if not os.path.exists(portfolio_dir):
                raise CommandError(f"Portfolio directory not found: {portfolio_dir}")
            
            # Process files
            if options['dry_run']:
                self.dry_run_processing(portfolio_dir, options['category'])
            else:
                self.process_files(portfolio_dir, options['category'])
                
        except Exception as e:
            logger.error(f"Command failed: {str(e)}")
            raise CommandError(f"Command failed: {str(e)}")

    def clear_existing_data(self):
        """Clear existing vector documents."""
        self.stdout.write("Clearing existing vector documents...")
        
        count = HTMLVectorDocument.objects.count()
        HTMLVectorDocument.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f"Cleared {count} existing documents")
        )

    def dry_run_processing(self, portfolio_dir: str, category: str = None):
        """Show what files would be processed without actually processing them."""
        self.stdout.write("DRY RUN - Files that would be processed:")
        self.stdout.write("=" * 50)
        
        portfolio_path = Path(portfolio_dir)
        processed_count = 0
        
        for html_file in portfolio_path.rglob("*.html"):
            # Determine category from directory structure
            relative_path = html_file.relative_to(portfolio_path)
            file_category = relative_path.parts[0] if len(relative_path.parts) > 1 else "General"
            
            # Skip if category filter is specified
            if category and file_category != category:
                continue
            
            # Get file size
            file_size = html_file.stat().st_size
            
            self.stdout.write(f"  {file_category:15} | {html_file.name:30} | {file_size:8} bytes")
            processed_count += 1
        
        self.stdout.write("=" * 50)
        self.stdout.write(f"Total files to process: {processed_count}")
        
        if category:
            self.stdout.write(f"Filtered by category: {category}")

    def process_files(self, portfolio_dir: str, category: str = None):
        """Process HTML files and create vector documents."""
        self.stdout.write(f"Processing HTML files from: {portfolio_dir}")
        
        if category:
            self.stdout.write(f"Filtering by category: {category}")
        
        try:
            # Process the portfolio directory
            documents = HTMLVectorProcessor.process_portfolio_directory(portfolio_dir)
            
            # Filter by category if specified
            if category:
                documents = [doc for doc in documents if doc.category == category]
            
            # Display results
            self.stdout.write("\nProcessing Results:")
            self.stdout.write("=" * 50)
            
            # Group by category
            by_category = {}
            for doc in documents:
                if doc.category not in by_category:
                    by_category[doc.category] = []
                by_category[doc.category].append(doc)
            
            total_processed = 0
            for cat, docs in by_category.items():
                self.stdout.write(f"\n{cat} ({len(docs)} documents):")
                for doc in docs:
                    self.stdout.write(f"  ✓ {doc.title} ({doc.file_size} bytes)")
                    total_processed += 1
            
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully processed {total_processed} documents")
            )
            
            # Show statistics
            self.show_statistics()
            
        except Exception as e:
            logger.error(f"Failed to process files: {str(e)}")
            raise CommandError(f"Failed to process files: {str(e)}")

    def show_statistics(self):
        """Display database statistics."""
        try:
            from AIApp.pg_vector import get_vector_stats
            
            stats = get_vector_stats()
            
            self.stdout.write("\nDatabase Statistics:")
            self.stdout.write("-" * 30)
            self.stdout.write(f"Total documents: {stats.get('total_documents', 0)}")
            self.stdout.write(f"Average embedding dimension: {stats.get('avg_embedding_dimension', 0)}")
            
            if stats.get('by_category'):
                self.stdout.write("\nDocuments by category:")
                for cat, count in stats['by_category'].items():
                    self.stdout.write(f"  {cat}: {count}")
                    
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"Could not retrieve statistics: {str(e)}")
            )

    def get_file_info(self, file_path: Path) -> dict:
        """Get information about a file."""
        try:
            stat = file_path.stat()
            return {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'exists': True
            }
        except FileNotFoundError:
            return {
                'size': 0,
                'modified': 0,
                'exists': False
            }
