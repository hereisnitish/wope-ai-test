from django.db import models


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
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.category} - {self.display_name}"
    
    def __repr__(self):
        return f"<PortfolioTemplate: {self.name} ({self.category})>"
