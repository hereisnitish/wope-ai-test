"""
Django management command to search the vector database.

This command allows you to search for similar HTML documents using
semantic search capabilities.

Usage:
    python manage.py search_vector_db "modern portfolio design"
    python manage.py search_vector_db "contact form" --category Contact
    python manage.py search_vector_db "hero section" --limit 5
    python manage.py search_vector_db "about me" --threshold 0.8
"""

import logging
from django.core.management.base import BaseCommand, CommandError
from AIApp.pg_vector import VectorSearchManager, get_vector_stats

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Search the vector database for similar HTML documents'

    def add_arguments(self, parser):
        parser.add_argument(
            'query',
            type=str,
            help='Search query text'
        )
        parser.add_argument(
            '--category',
            type=str,
            help='Filter by category (Hero, About, Contact, etc.)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum number of results (default: 10)'
        )
        parser.add_argument(
            '--threshold',
            type=float,
            default=0.7,
            help='Minimum similarity threshold (0.0-1.0, default: 0.7)'
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show database statistics before searching'
        )

    def handle(self, *args, **options):
        """Main command handler."""
        try:
            # Set up logging
            logging.basicConfig(level=logging.INFO)
            
            # Show statistics if requested
            if options['stats']:
                self.show_statistics()
                self.stdout.write("")
            
            # Perform the search
            query = options['query']
            category = options['category']
            limit = options['limit']
            threshold = options['threshold']
            
            self.stdout.write(f"Searching for: '{query}'")
            if category:
                self.stdout.write(f"Category filter: {category}")
            self.stdout.write(f"Similarity threshold: {threshold}")
            self.stdout.write(f"Result limit: {limit}")
            self.stdout.write("=" * 60)
            
            # Execute search
            results = VectorSearchManager.search_similar_documents(
                query=query,
                category=category,
                limit=limit,
                similarity_threshold=threshold
            )
            
            # Display results
            if not results:
                self.stdout.write(
                    self.style.WARNING("No similar documents found")
                )
                return
            
            self.stdout.write(f"Found {len(results)} similar documents:\n")
            
            for i, result in enumerate(results, 1):
                self.display_result(i, result)
            
            # Show search summary
            self.stdout.write("\n" + "=" * 60)
            self.stdout.write(f"Search completed: {len(results)} results")
            
            if results:
                best_match = results[0]
                self.stdout.write(
                    f"Best match: {best_match['title']} "
                    f"(similarity: {best_match['similarity']:.3f})"
                )
                
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise CommandError(f"Search failed: {str(e)}")

    def display_result(self, index: int, result: dict):
        """Display a single search result."""
        self.stdout.write(f"{index:2d}. {result['title']}")
        self.stdout.write(f"    Category: {result['category']}")
        self.stdout.write(f"    Template: {result['template_name']}")
        self.stdout.write(f"    Similarity: {result['similarity']:.3f}")
        self.stdout.write(f"    Distance: {result['distance']:.3f}")
        self.stdout.write(f"    File: {result['file_path']}")
        
        # Show preview of text content
        text_preview = result['text_content'][:200]
        if len(result['text_content']) > 200:
            text_preview += "..."
        
        self.stdout.write(f"    Preview: {text_preview}")
        self.stdout.write("")

    def show_statistics(self):
        """Display database statistics."""
        try:
            stats = get_vector_stats()
            
            self.stdout.write("Vector Database Statistics:")
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
