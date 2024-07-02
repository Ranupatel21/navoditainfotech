#Import Libraries and Load spaCy Model
import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Load spaCy model
nlp = spacy.load('en_core_web_sm')
# Initialize ChatBot
chatbot = ChatBot(
    'AssistantBot',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation'
    ]
)

# Create a trainer for the chatbot
trainer = ListTrainer(chatbot)

# Train the chatbot with some basic conversations
trainer.train([
    "Hi, how can I help you?",
    "I would like to book a flight.",
    "Sure, I can help you with that. Where would you like to go?",
    "I want to go to New York.",
    "When are you planning to travel?",
    "I plan to travel next Monday.",
    "Let me check the available flights for you."
])
def process_input(user_input):
    # Process the user input using spaCy
    doc = nlp(user_input)

    # Analyze the entities and intent (simple example)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print("Entities:", entities)

    # Generate a response from the chatbot
    response = chatbot.get_response(user_input)
    return response

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = process_input(user_input)
    print("Bot:", response)
import requests

def get_weather(city):
    api_key = "your_api_key"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        return "Sorry, I couldn't find the weather for that location."

    weather = data['current']['condition']['text']
    temperature = data['current']['temp_c']
    return f"The current weather in {city} is {weather} with a temperature of {temperature}°C."

# Modify process_input to handle weather queries
def process_input(user_input):
    doc = nlp(user_input)

    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity
            city = ent.text
            weather = get_weather(city)
            return weather

    response = chatbot.get_response(user_input)
    return response

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = process_input(user_input)
    print("Bot:", response)

