from openai import OpenAI
from .common import Spinner

# Initialize LM Studio client
CLIENT = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL = "mradermacher/glm-4-9b-chat-1m-GGUF"
