import os
import threading
import logging
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot rodando no Render!"

def start_gst():
    try:
        # roda GST-TCP.py como subprocesso
        subprocess.run(["python", "GST-TCP.py"])
    except Exception as e:
        logging.error(f"Erro ao iniciar GST-TCP.py: {e}")

if __name__ == "__main__":
    # Thread 1 → script do bot
    threading.Thread(target=start_gst).start()

    # Thread 2 → servidor Flask (para Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
