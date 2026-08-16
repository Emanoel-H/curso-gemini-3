import google.genai as genai
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model=GEMINI_FLASH,
    contents="Hello World"
)

print(response.text)