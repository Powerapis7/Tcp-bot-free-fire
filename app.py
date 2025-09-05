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
        script_path = os.path.join(os.getcwd(), "GST-TCP.py")
        if not os.path.exists(script_path):
            print(f"[ERRO] Não achei o arquivo: {script_path}")
            return

        print(f"[INFO] Iniciando GST-TCP.py em {script_path}...")

        process = subprocess.Popen(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(f"[GST-TCP] {line.strip()}")

    except Exception as e:
        logging.error(f"Erro ao iniciar GST-TCP.py: {e}")

if __name__ == "__main__":
    # Thread 1 → script do bot
    threading.Thread(target=start_gst, daemon=True).start()

    # Thread 2 → servidor Flask
    port = int(os.environ.get("PORT", 5000))
    print(f"🌍 Servidor Flask rodando na porta {port}")
    app.run(host="0.0.0.0", port=port)__name__
