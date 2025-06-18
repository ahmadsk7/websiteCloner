import google.generativeai as genai
from typing import Dict, Any

# Configure the Gemini API
genai.configure(api_key='AIzaSyBhI4bazKcFI8fXbiyj9ylxhafFiZO62zw')

def generate_html(design_context: Dict[str, Any]) -> str:
    # Use the Gemini model to generate HTML
    model = genai.GenerativeModel('gemini-pro')
    
    # Create a prompt that includes all the design context
    prompt = f"""
    Generate a cloned version of the website with the following design context:
    
    URL: {design_context['url']}
    
    Meta Information:
    {design_context['meta']}
    
    Layout Structure:
    {design_context['layout']}
    
    Styles:
    - Inline styles: {design_context['styles']['inline']}
    - External stylesheets: {design_context['styles']['external']}
    
    Assets:
    - Images: {design_context['assets']['images']}
    - Scripts: {design_context['assets']['scripts']}
    - Fonts: {design_context['assets']['fonts']}
    
    Original HTML:
    {design_context['html']}
    
    Please generate a complete HTML document that closely matches the original website's design and functionality.
    Include all necessary CSS and JavaScript references.
    """
    
    response = model.generate_content(prompt)
    return response.text 