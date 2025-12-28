#!/data/data/com.termux/files/usr/bin/bash

echo "========================================"
echo "🛑 Stopping PC Wake Bot"
echo "========================================"

cd "$(dirname "$0")"

# Stop supervisor
echo "Stopping supervisor..."
pkill -f "supervisor_temp.sh" 2>/dev/null

# Stop bot
if [ -f "bot.pid" ]; then
    PID=$(cat bot.pid 2>/dev/null)
    if [ ! -z "$PID" ] && kill -0 $PID 2>/dev/null; then
        echo "Stopping bot (PID: $PID)..."
        kill $PID 2>/dev/null
        sleep 2
    fi
    rm -f bot.pid
fi

# Force stop if any processes remain
pkill -f "python.*pc_wake_bot" 2>/dev/null
sleep 1

echo ""
echo "✅ All processes stopped!"
echo ""
echo "Logs available in:"
echo "  bot.log - Bot activity"
echo "  crash.log - Error reports"
echo "  supervisor.log - Supervisor output"
echo "========================================"
