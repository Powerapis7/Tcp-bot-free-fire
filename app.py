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

        # subprocess sem bloqueio e com captura completa de stdout e stderr
        process = subprocess.Popen(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # thread para ler stdout
        def log_stdout():
            for line in process.stdout:
                print(f"[GST-TCP stdout] {line.strip()}")

        # thread para ler stderr
        def log_stderr():
            for line in process.stderr:
                print(f"[GST-TCP stderr] {line.strip()}")

        threading.Thread(target=log_stdout, daemon=True).start()
        threading.Thread(target=log_stderr, daemon=True).start()

        # opcional: espera o processo acabar (não bloqueia Flask)
        # process.wait()

    except Exception as e:
        logging.error(f"[ERRO] Exceção ao iniciar GST-TCP.py: {e}")

if __name__ == "__main__":
    # Thread 1 → script do bot
    threading.Thread(target=start_gst, daemon=True).start()

    # Thread 2 → servidor Flask para manter serviço ativo no Render
    port = int(os.environ.get("PORT", 5000))
    print(f"🌍 Servidor Flask rodando na porta {port}")
    app.run(host="0.0.0.0", port=port)
