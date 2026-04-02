from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

DB_FILE = "database.sqlite3"
DATA_FOLDER = "data"

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Old database removed. Training new database.")
else:
    print("No database found. Creating new database.")

english_bot = ChatBot(
    'Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Sorry, I do not understand. Please ask a banking-related question.',
            'maximum_similarity_threshold': 0.75
        }
    ]
)

trainer = ListTrainer(english_bot)

if os.path.exists(DATA_FOLDER):
    for file_name in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, file_name)

        if os.path.isfile(file_path):
            print(f"Training using {file_name}")

            with open(file_path, encoding='utf-8', errors='ignore') as file:
                convData = [line.strip() for line in file.readlines() if line.strip()]

            if convData:
                trainer.train(convData)
                print(f"Training completed for {file_name}")
            else:
                print(f"Skipped empty file: {file_name}")
else:
    print("Data folder not found.")