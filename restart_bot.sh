#!/data/data/com.termux/files/usr/bin/bash

echo "========================================"
echo "🔄 Restarting PC Wake Bot"
echo "========================================"

cd "$(dirname "$0")"

# Stop first
./stop_bot.sh

sleep 2

# Start again
./start_bot.sh
