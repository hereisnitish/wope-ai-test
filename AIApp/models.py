from django.db import models
from pgvector.django import VectorField
from django.core.exceptions import ValidationError

class PortfolioTemplate(models.Model):
    """
    Model to store portfolio template information with categories, names, 
    display names, descriptions and file paths.
    """
    
    category = models.CharField(
        max_length=50,
        help_text="Template category (Hero, About, Portfolio, Services, etc.)"
    )
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique template identifier name"
    )
    
    display_name = models.CharField(
        max_length=150,
        help_text="Human-readable display name for the template"
    )
    
    description = models.TextField(
        help_text="Brief description of the template functionality"
    )
    
    file_path_template = models.CharField(
        max_length=500,
        help_text="File path template location"
    )
    content = models.TextField(
        help_text="The full HTML, CSS, and JavaScript code for the component"
    )
    css_content = models.TextField(
        blank=True,
        null=True,
        help_text="The CSS content specific to this template section"
    )
    embedding = VectorField(dimensions=1536)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'portfolio_templates'
        verbose_name = 'Portfolio Template'
        verbose_name_plural = 'Portfolio Templates'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['name']),
            models.Index(fields=['is_active'])
        ]
    
    def __str__(self):
        return f"{self.category} - {self.display_name}"
    
    def __repr__(self):
        return f"<PortfolioTemplate: {self.name} ({self.category})>"
    
    def clean(self):
        if self.embedding and len(self.embedding) != 1536:
            raise ValidationError("Embedding must have exactly 1536 dimensions.")


class Project(models.Model):
    """
    Model to store project information for HTML file embeddings.
    This is the top-level entity that contains multiple pages.
    """
    
    project_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique identifier for the project"
    )
    
    project_name = models.CharField(
        max_length=200,
        help_text="Human-readable name for the project"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the project"
    )
    
    html_file_path = models.CharField(
        max_length=500,
        help_text="Path to the main HTML file"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'html_projects'
        verbose_name = 'HTML Project'
        verbose_name_plural = 'HTML Projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project_id']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at'])
        ]
    
    def __str__(self):
        return f"Project: {self.project_name} ({self.project_id})"
    
    def __repr__(self):
        return f"<Project: {self.project_id}>"


class Page(models.Model):
    """
    Model to store page information within a project.
    Each project can have multiple pages.
    """
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='pages',
        help_text="The project this page belongs to"
    )
    
    page_id = models.CharField(
        max_length=100,
        help_text="Unique identifier for the page within the project"
    )
    
    page_name = models.CharField(
        max_length=200,
        help_text="Human-readable name for the page"
    )
    
    page_type = models.CharField(
        max_length=50,
        choices=[
            ('home', 'Home'),
            ('about', 'About'),
            ('portfolio', 'Portfolio'),
            ('contact', 'Contact'),
            ('blog', 'Blog'),
            ('services', 'Services'),
            ('other', 'Other')
        ],
        default='other',
        help_text="Type of the page"
    )
    
    html_content = models.TextField(
        help_text="The HTML content of the page"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'html_pages'
        verbose_name = 'HTML Page'
        verbose_name_plural = 'HTML Pages'
        unique_together = ['project', 'page_id']
        ordering = ['project', 'page_id']
        indexes = [
            models.Index(fields=['project', 'page_id']),
            models.Index(fields=['page_type']),
            models.Index(fields=['is_active'])
        ]
    
    def __str__(self):
        return f"Page: {self.page_name} ({self.page_id}) in {self.project.project_name}"
    
    def __repr__(self):
        return f"<Page: {self.page_id} in {self.project.project_id}>"


class Section(models.Model):
    """
    Model to store section information within a page.
    Each page can have multiple sections.
    """
    
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='sections',
        help_text="The page this section belongs to"
    )
    
    section_id = models.CharField(
        max_length=100,
        help_text="Unique identifier for the section within the page"
    )
    
    section_name = models.CharField(
        max_length=200,
        help_text="Human-readable name for the section"
    )
    
    section_type = models.CharField(
        max_length=50,
        choices=[
            ('header', 'Header'),
            ('hero', 'Hero'),
            ('about', 'About'),
            ('portfolio', 'Portfolio'),
            ('skills', 'Skills'),
            ('experience', 'Experience'),
            ('contact', 'Contact'),
            ('footer', 'Footer'),
            ('other', 'Other')
        ],
        default='other',
        help_text="Type of the section"
    )
    
    html_content = models.TextField(
        help_text="The HTML content of the section"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of the section within the page"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'html_sections'
        verbose_name = 'HTML Section'
        verbose_name_plural = 'HTML Sections'
        unique_together = ['page', 'section_id']
        ordering = ['page', 'order', 'section_id']
        indexes = [
            models.Index(fields=['page', 'section_id']),
            models.Index(fields=['section_type']),
            models.Index(fields=['order']),
            models.Index(fields=['is_active'])
        ]
    
    def __str__(self):
        return f"Section: {self.section_name} ({self.section_id}) in {self.page.page_name}"
    
    def __repr__(self):
        return f"<Section: {self.section_id} in {self.page.page_id}>"


class Chunk(models.Model):
    """
    Model to store chunk information within a section.
    Each section can have multiple chunks for embedding storage.
    """
    
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='chunks',
        help_text="The section this chunk belongs to"
    )
    
    chunk_id = models.CharField(
        max_length=100,
        help_text="Unique identifier for the chunk within the section"
    )
    
    chunk_name = models.CharField(
        max_length=200,
        help_text="Human-readable name for the chunk"
    )
    
    html_content = models.TextField(
        help_text="The HTML content of the chunk"
    )
    
    text_content = models.TextField(
        help_text="The plain text content extracted from HTML for embedding"
    )
    
    embedding = VectorField(
        dimensions=1536,
        help_text="Vector embedding of the chunk content"
    )
    
    chunk_size = models.PositiveIntegerField(
        help_text="Size of the chunk in characters"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of the chunk within the section"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'html_chunks'
        verbose_name = 'HTML Chunk'
        verbose_name_plural = 'HTML Chunks'
        unique_together = ['section', 'chunk_id']
        ordering = ['section', 'order', 'chunk_id']
        indexes = [
            models.Index(fields=['section', 'chunk_id']),
            models.Index(fields=['chunk_size']),
            models.Index(fields=['order']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Chunk: {self.chunk_name} ({self.chunk_id}) in {self.section.section_name}"
    
    def __repr__(self):
        return f"<Chunk: {self.chunk_id} in {self.section.section_id}>"
    
    def clean(self):
        if self.embedding and len(self.embedding) != 1536:
            raise ValidationError("Embedding must have exactly 1536 dimensions.")



