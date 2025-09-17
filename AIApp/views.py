from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import sys
import traceback
import logging
from pathlib import Path
from .Crew.main import DjangoProjectGeneratorCrew
from .models import *
from openai import OpenAI
from django.db.models import FloatField
from django.db.models.expressions import RawSQL

logger = logging.getLogger(__name__)


def ensure_file_creation(file_path, content, is_json=False):
    """
    Robust file creation with proper error handling.
    
    Args:
        file_path (str): Path to the file to create/write
        content: Content to write to the file
        is_json (bool): Whether to write as JSON format
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    try:
        # Convert to Path object for better handling
        path = Path(file_path)
        
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content based on type
        if is_json:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(content))
        
        print(f"✅ Successfully created/updated file: {file_path}")
        return True, None
        
    except OSError as e:
        error_msg = f"File system error creating {file_path}: {str(e)}"
        print(f"❌ {error_msg}")
        return False, error_msg
    except json.JSONEncodeError as e:
        error_msg = f"JSON encoding error for {file_path}: {str(e)}"
        print(f"❌ {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error creating {file_path}: {str(e)}"
        print(f"❌ {error_msg}")
        return False, error_msg


def chat(request):
    return render(request, 'chat.html')

@csrf_exempt
@require_http_methods(["POST"])
def process_prompt(request):
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        user_prompt = data.get('prompt', '').strip()
        
        if not user_prompt:
            return JsonResponse({
                'success': False, 
                'error': 'No prompt provided'
            })
        
        print(f"🎯 Processing prompt: {user_prompt}")
        
        # Import crew components (doing this locally to avoid import errors at module level)
        try:
            
            # Create and run the crew
            crewai_crew = DjangoProjectGeneratorCrew()
            crew_object = crewai_crew.crew()
            
            print("🔧 Crew created successfully, starting execution...")
            
            # Execute the crew with the user prompt
            response = crew_object.kickoff(inputs=dict(user_prompt=user_prompt))
            
            # Save response using robust file creation
            json_success, json_error = ensure_file_creation(
                "outputs/response.json", 
                response.model_dump(), 
                is_json=True
            )
            
            md_content = response.raw if hasattr(response, "raw") else str(response)
            md_success, md_error = ensure_file_creation(
                "outputs/response.md", 
                md_content, 
                is_json=False
            )
            
            # Log any file creation issues but don't fail the request
            if not json_success:
                print(f"⚠️ Warning: Could not save JSON file - {json_error}")
            if not md_success:
                print(f"⚠️ Warning: Could not save Markdown file - {md_error}")
            
            print("✅ Crew execution completed!")
            
            # Extract the response content
            response_content = response.raw if hasattr(response, 'raw') else str(response)
            
            return JsonResponse({
                'success': True,
                'response': response_content,
                'prompt': user_prompt
            })
            
        except ImportError as e:
            print(f"Import error: {e}")
            return JsonResponse({
                'success': False,
                'error': f'Failed to import crew components: {str(e)}'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
        
    except Exception as e:
        print(f"❌ Error processing prompt: {e}")
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })


