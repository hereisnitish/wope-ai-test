import os
import subprocess
import json
import base64
import requests
from typing import List
import shutil
from dotenv import load_dotenv
from crewai.tools import tool
from .openai_page_generator import make_website
from ..models import PortfolioTemplate

#utility functions
def get_user_input(prompt: str) -> str:
    print(f"\n🤖 {prompt}")
    return input("👤 You: ").strip()



#All tools

@tool("get_existing_components")
def get_existing_components(category: str) -> List[PortfolioTemplate]:
    """Get existing portfolio template components by category. Returns a list of templates with their details."""
    
    response = PortfolioTemplate.objects.filter(category=category)
    
    data = [
        {
            "name": item.name,
            "display_name": item.display_name,
            "description": item.description,
            "file_path_template": item.file_path_template
        } for item in response
    ]

    return data


@tool("ask_user")
def ask_user(question: str) -> str:
	"""Ask the user a question and get their response. Use this tool to gather requirements and preferences interactively."""
	return get_user_input(question)


@tool("create_new_component")
def create_new_component(category: str, name: str, display_name: str, description: str) -> str:
    """Create a new component and return the file path."""
    path_name  =   make_website(website_input=f"Make me {display_name} component for {description}", filename=f"{name}.html")
    return path_name