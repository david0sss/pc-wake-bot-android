#!/data/data/com.termux/files/usr/bin/bash

echo "========================================"
echo "🧹 Clearing Telegram Command Queue"
echo "========================================"

cd "$(dirname "$0")"

python3 -c "
import requests
import os

# Read token from bot file
try:
    with open('pc_wake_bot.py', 'r') as f:
        content = f.read()
        import re
        token_match = re.search(r'TOKEN\s*=\s*[\"\\']([^\"\\']+)[\"\\']', content)
        if token_match:
            TOKEN = token_match.group(1)
            print(f'Found token: {TOKEN[:10]}...')
            
            # Get last update ID
            url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('result'):
                    updates = data['result']
                    if updates:
                        last_id = updates[-1]['update_id']
                        # Clear queue
                        params = {'offset': last_id + 1}
                        requests.get(url, params=params, timeout=5)
                        print(f'✅ Queue cleared, last ID: {last_id}')
                    else:
                        print('✅ Queue already empty')
                else:
                    print('❌ Telegram API error')
            else:
                print(f'❌ HTTP error: {response.status_code}')
        else:
            print('❌ Could not find token in bot file')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Remove last update file
rm -f last_update_id.txt
echo "Removed last_update_id.txt"
echo "========================================"
