#!/data/data/com.termux/files/usr/bin/bash

echo "========================================"
echo "🚀 Starting PC Wake Bot"
echo "Time: $(date)"
echo "========================================"

cd "$(dirname "$0")"

# Stop if already running
echo "Stopping old processes..."
pkill -f "python.*pc_wake_bot" 2>/dev/null
pkill -f "supervisor_temp.sh" 2>/dev/null
sleep 2

# Remove old files
rm -f bot.pid
rm -f supervisor.log 2>/dev/null

# Check dependencies
echo "Checking dependencies..."
if [ ! -f "/data/data/com.termux/files/usr/bin/wakeonlan" ]; then
    echo "Installing wakeonlan..."
    pkg install wakeonlan -y
fi

if ! python -c "import requests" 2>/dev/null; then
    echo "Installing requests..."
    pip install requests
fi

echo ""
echo "Starting bot with auto-restart..."

# Create supervisor script
cat > supervisor_temp.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

cd "$(dirname "$0")"

RESTART_COUNT=0
MAX_RESTARTS=20

while [ $RESTART_COUNT -lt $MAX_RESTARTS ]; do
    RESTART_COUNT=$((RESTART_COUNT + 1))
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Start attempt #$RESTART_COUNT"
    echo "Time: $(date)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Start bot
    python pc_wake_bot.py
    EXIT_CODE=$?
    
    echo ""
    echo "Bot exited with code: $EXIT_CODE"
    
    case $EXIT_CODE in
        0)
            echo "✅ Normal stop (/stop command)"
            break
            ;;
        100)
            echo "🔄 Restart requested (/restart command)"
            
            if [ $RESTART_COUNT -ge $MAX_RESTARTS ]; then
                echo "⚠️ Max restarts reached ($MAX_RESTARTS)"
                break
            fi
            
            echo "⏳ Waiting 5 seconds..."
            sleep 5
            ;;
        101)
            echo "💥 Bot crashed"
            
            if [ $RESTART_COUNT -ge $MAX_RESTARTS ]; then
                echo "⚠️ Max restarts reached ($MAX_RESTARTS)"
                break
            fi
            
            echo "⏳ Waiting 10 seconds..."
            sleep 10
            ;;
        *)
            echo "⚠️ Unknown exit code: $EXIT_CODE"
            break
            ;;
    esac
done

echo ""
echo "👋 Supervisor stopped"
echo "Total starts: $RESTART_COUNT"
EOF

chmod +x supervisor_temp.sh

# Start supervisor in background
nohup ./supervisor_temp.sh > supervisor.log 2>&1 &

sleep 3

echo "✅ Bot started!"
echo ""
echo "To view logs:"
echo "  tail -f bot.log"
echo "  tail -f supervisor.log"
echo ""
echo "Telegram commands:"
echo "  /wake    - Wake up PC"
echo "  /status  - Bot status"
echo "  /restart - Restart bot"
echo "  /stop    - Stop bot"
echo ""
echo "To stop: ./stop_bot.sh"
echo "========================================"
