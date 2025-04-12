import os
import json
from google import genai
from google.genai import types

def generate_weather_response(weather_json):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    
    json_input = json.dumps(weather_json)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=json_input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.9,
        max_output_tokens=400,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Given the weather data in the JSON, summarize the weather conditions in a clear and concise manner. The summary should include a general weather condition, current_temperatur, feels_like_temperature, max and min temperatuere and mention city. Ignore icon and country data. Use symbols for temperature units"""),
        ],
    )
    output = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        output += chunk.text
    return output