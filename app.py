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
        # inicia GST-TCP.py e captura logs stdout/stderr
        process = subprocess.Popen(
            ["python", "GST-TCP.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # lê a saída em tempo real e repassa para os logs do Render
        for line in process.stdout:
            print(f"[GST-TCP] {line.strip()}")

    except Exception as e:
        logging.error(f"Erro ao iniciar GST-TCP.py: {e}")

if __name__ == "__main__":
    # Thread 1 → script do bot
    threading.Thread(target=start_gst, daemon=True).start()

    # Thread 2 → servidor Flask (para Render)
    port = int(os.environ.get("PORT", 5000))
    print(f"🌍 Servidor Flask rodando na porta {port}")
    app.run(host="0.0.0.0", port=port)
