from src import handler
from dotenv import load_dotenv

load_dotenv()
test_event = {}
handler.handle(test_event,"")