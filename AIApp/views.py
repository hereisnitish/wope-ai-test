from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import sys
import traceback
from .Crew.main import DjangoProjectGeneratorCrew


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

