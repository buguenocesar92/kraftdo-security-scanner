#!/bin/bash
set -e
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"
SCANNER="$INSTALL_DIR/scanner.py"

echo ""
echo "=== KraftDo Security Scanner - Instalador ==="
echo ""

pip install requests --break-system-packages -q
ok "requests instalado"

chmod +x "$SCANNER"
ok "scanner.py ejecutable"

if [ ! -f "$INSTALL_DIR/.env" ]; then
    cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"
    warn ".env creado - editar con tus tokens:"
    echo "  nano $INSTALL_DIR/.env"
else
    ok ".env ya existe"
fi

# Cron diario 2AM
CRON_CMD="0 2 * * * cd $INSTALL_DIR && /usr/bin/python3 $SCANNER cron >> $INSTALL_DIR/scanner.log 2>&1"
(crontab -l 2>/dev/null | grep -v "kraftdo-security-scanner\|kraftdo_security"; echo "$CRON_CMD") | crontab -
ok "cron diario instalado (2:00 AM)"

# Pre-push hooks
REPOS=("kraftdo-nfc-app" "kraftdo-cms" "kraftdo_handoff" "kraftdo_meme"
       "screenshots-bot" "chile-tv" "kraftdo-base" "KraftDo_Sistema_v18_completo"
       "investigador" "KraftDo_Funko" "kraftdo-wp-studio" "buguenocesar92" "dev-tools")

for repo in "${REPOS[@]}"; do
    REPO_PATH="$HOME/Dev/$repo"
    HOOK_PATH="$REPO_PATH/.git/hooks/pre-push"
    if [ -d "$REPO_PATH/.git" ]; then
        cat > "$HOOK_PATH" << HOOK
#!/bin/bash
set -a
[ -f $INSTALL_DIR/.env ] && source $INSTALL_DIR/.env
set +a
python3 $SCANNER pre-push
exit \$?
HOOK
        chmod +x "$HOOK_PATH"
        ok "pre-push hook en $repo"
    fi
done

echo ""
echo "=== Listo ==="
echo ""
echo "Proximos pasos:"
echo "1. Crear bot: @BotFather en Telegram -> /newbot"
echo "2. Configurar: nano $INSTALL_DIR/.env"
echo "3. Probar: python3 $SCANNER cron"
echo ""
