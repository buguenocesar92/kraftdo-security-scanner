#!/usr/bin/env python3
import os, sys, json, subprocess, requests
from datetime import datetime

DEV_DIR   = os.getenv("DEV_DIR", os.path.expanduser("~/Dev"))
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")
GITLEAKS  = os.getenv("GITLEAKS_PATH", "gitleaks")

REPOS = [
    "kraftdo-nfc-app", "kraftdo-cms", "kraftdo_handoff", "kraftdo_meme",
    "screenshots-bot", "chile-tv", "kraftdo-base", "KraftDo_Sistema_v18_completo",
    "investigador", "KraftDo_Funko", "kraftdo-wp-studio", "buguenocesar92", "tools",
]

def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("[WARN] Telegram no configurado")
        return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"[ERROR] Telegram: {e}")

def escanear_repo(ruta):
    resultado = {"repo": os.path.basename(ruta), "leaks": [], "error": None}
    if not os.path.exists(ruta):
        resultado["error"] = "no existe"
        return resultado
    try:
        subprocess.run([GITLEAKS, "detect", f"--source={ruta}", "--no-banner",
            "--report-format=json", "--report-path=/tmp/gl_report.json", "-q"],
            capture_output=True, text=True)
        if os.path.exists("/tmp/gl_report.json"):
            with open("/tmp/gl_report.json") as f:
                contenido = f.read().strip()
                if contenido and contenido != "null":
                    resultado["leaks"] = json.loads(contenido) or []
            os.remove("/tmp/gl_report.json")
    except Exception as e:
        resultado["error"] = str(e)
    return resultado

def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "cron"
    print(f"\n=== KraftDo Security Scanner [{modo}] ===\n")

    # Cargar .env si existe
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        for line in open(env_file):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    global BOT_TOKEN, CHAT_ID
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

    resultados = []
    for repo in REPOS:
        ruta = os.path.join(os.path.expanduser("~/Dev"), repo)
        r = escanear_repo(ruta)
        resultados.append(r)
        estado = "LEAK" if r["leaks"] else ("ERROR" if r["error"] else "OK")
        print(f"[{estado}] {r['repo']}")

    leaks = [r for r in resultados if r["leaks"]]
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    if leaks:
        msg = f"SECRETOS DETECTADOS KraftDo Security\n{fecha} | {modo}\n\n"
        for r in leaks:
            msg += f"REPO: {r['repo']}\n"
            for l in r["leaks"][:3]:
                msg += f"  - {l.get('RuleID','?')} en {l.get('File','?')}\n"
        msg += "\nAccion: revisar y rotar credenciales"
        print(f"\n{msg}")
        send_telegram(msg)
        sys.exit(1)
    elif modo == "cron":
        ok_count = len([r for r in resultados if not r["leaks"] and not r["error"]])
        msg = f"KraftDo Security - Todo limpio\n{fecha}\nEscaneados: {len(resultados)} repos\nLimpios: {ok_count}"
        print(f"\n{msg}")
        send_telegram(msg)

    print("\nCompletado - sin problemas")
    sys.exit(0)

if __name__ == "__main__":
    main()
