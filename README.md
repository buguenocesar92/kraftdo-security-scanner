# KraftDo Security Scanner

Escanea todos los repos de KraftDo con gitleaks y notifica por Telegram
si detecta secretos, tokens o credenciales expuestas.

## Cuándo corre

- **Pre-push**: antes de cada `git push` en todos los repos
- **Cron diario**: todos los días a las 2:00 AM

## Instalación

### 1. Crear bot de Telegram

1. Abrir Telegram → buscar `@BotFather`
2. Enviar `/newbot` → seguir instrucciones
3. Copiar el token que te da (formato: `1234567890:ABCdef...`)
4. Enviarle cualquier mensaje a tu nuevo bot
5. Abrir en el browser: `https://api.telegram.org/bot{TU_TOKEN}/getUpdates`
6. Copiar el `id` del campo `chat` — ese es tu CHAT_ID

### 2. Instalar

    cd ~/Dev
    git clone https://github.com/buguenocesar92/kraftdo-security-scanner.git
    cd kraftdo-security-scanner
    ./install.sh

### 3. Configurar

    nano .env
    # Pegar TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID

### 4. Probar

    python3 scanner.py cron

## Alertas

**Todo limpio (diario):**
```
✅ KraftDo Security — Todo limpio
📅 21/04/2026 02:00
🔍 Escaneados: 13 repos
✅ Limpios: 13
```

**Secreto detectado:**
```
🚨 SECRETOS DETECTADOS — KraftDo Security
📅 21/04/2026 14:32 | Modo: pre-push

❌ kraftdo-nfc-app
  • generic-api-key en test-kraftdo.js
    Secreto: 4532ddb4...

⚡ Acción: revisar y rotar credenciales
```

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram |
| `TELEGRAM_CHAT_ID` | ID de tu chat con el bot |
| `DEV_DIR` | Ruta de tus repos (default: ~/Dev) |
| `GITLEAKS_PATH` | Ruta de gitleaks (default: gitleaks) |

## Archivos

```
kraftdo-security-scanner/
├── scanner.py      ← script principal
├── install.sh      ← instalador (cron + pre-push hooks)
├── .env.example    ← template de configuración
├── .env            ← tu configuración (no se sube al repo)
├── scanner.log     ← log del cron
└── README.md
```
