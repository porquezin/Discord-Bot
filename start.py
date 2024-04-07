import threading
import os

def run_discord_bot():
    os.system("python3 bot.py")

def run_flask_app():
    os.system("python3 api.py")

if __name__ == "__main__":
    discord_thread = threading.Thread(target=run_discord_bot)
    flask_thread = threading.Thread(target=run_flask_app)

    flask_thread.start()
    discord_thread.start()

    flask_thread.join()
    discord_thread.join()
