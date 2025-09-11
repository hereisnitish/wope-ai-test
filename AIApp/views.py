from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import sys
import traceback
from .Crew.main import DjangoProjectGeneratorCrew
from openai import OpenAI


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
        
        # Enhance the user prompt using advanced prompt engineering
        enhanced_prompt = generate_good_prompt(user_prompt)
        print(f"🚀 Using enhanced prompt: {enhanced_prompt}")
        
        # Import crew components (doing this locally to avoid import errors at module level)
        try:
            
            # Create and run the crew
            crewai_crew = DjangoProjectGeneratorCrew()
            crew_object = crewai_crew.crew()
            
            print("🔧 Crew created successfully, starting execution...")
            
            # Execute the crew with the enhanced prompt
            response = crew_object.kickoff(inputs=dict(user_prompt=enhanced_prompt))
            with open("outputs/response.json", "w") as f:
                json.dump(response.model_dump(), f, indent=2)
            with open("outputs/response.md", "w") as f:
                f.write(response.raw if hasattr(response, "raw") else str(response))
                
            
            print("✅ Crew execution completed!")
            
            # Extract the response content
            response_content = response.raw if hasattr(response, 'raw') else str(response)
            
            return JsonResponse({
                'success': True,
                'response': response_content,
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


def generate_good_prompt(user_prompt):
    """
    Enhanced prompt generation function that analyzes and improves user prompts
    using advanced prompt engineering techniques.
    
    Args:
        user_prompt (str): The original user prompt to enhance
        
    Returns:
        str: Enhanced and optimized prompt
    """
    try:
        client = OpenAI()
        
        # Enhanced system prompt for prompt optimization
        system_prompt = """You are an expert prompt engineer specializing in optimizing user prompts for AI systems. 
        Your task is to analyze and enhance user prompts to make them more effective, clear, and likely to produce better results.

        Return ONLY the enhanced prompt, no explanations or meta-commentary."""
        
        # Create the enhancement prompt
        enhancement_prompt = f"""
        Original User Prompt: "{user_prompt}"
        
        Please enhance this prompt using the guidelines above. Make it more effective, specific, and likely to produce high-quality results.
        Focus on making it clear, actionable, and comprehensive while maintaining the user's original intent.
        """
        
        # Use the correct OpenAI API method
        response = client.chat.completions.create(
            model="gpt-4o",  # Using available model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": enhancement_prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
            top_p=0.9
        )
        
        enhanced_prompt = response.choices[0].message.content.strip()
        
        print(f"🎯 Original prompt: {user_prompt}")
        print(f"✨ Enhanced prompt: {enhanced_prompt}")
        
        return enhanced_prompt
        
    except Exception as e:
        print(f"❌ Error enhancing prompt: {e}")
        # Return original prompt if enhancement fails
        return user_prompt