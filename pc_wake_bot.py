#!/data/data/com.termux/files/usr/bin/python3
"""
PC Wake Bot for Android (Termux)
Telegram bot to wake up your PC using Wake-on-LAN
"""

import subprocess
import requests
import time
import os
import sys
import socket
import struct
import atexit
import signal

# ===== USER SETTINGS =====
# Replace these values with your own
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"      # Get from @BotFather on Telegram
USER_ID = YOUR_TELEGRAM_USER_ID_HERE         # Get from @userinfobot on Telegram
MAC = "YOUR_PC_MAC_ADDRESS_HERE"            # Format: "AA:BB:CC:DD:EE:FF"
# ==========================

# File paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "bot.log")
PID_FILE = os.path.join(SCRIPT_DIR, "bot.pid")
CRASH_LOG = os.path.join(SCRIPT_DIR, "crash.log")
COMMAND_FILE = os.path.join(SCRIPT_DIR, "last_update_id.txt")
START_TIME = time.time()

# Exit codes for supervisor
EXIT_NORMAL = 0
EXIT_RESTART = 100
EXIT_CRASH = 101

def log(msg, error=False):
    """Log messages to file and console"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    
    # Print to console
    print(log_msg)
    
    # Write to log file
    try:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(log_msg + "\n")
            if error:
                import traceback
                f.write(traceback.format_exc() + "\n")
    except:
        pass

def save_pid():
    """Save current process ID to file"""
    try:
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
        log(f"Saved PID: {os.getpid()}")
    except Exception as e:
        log(f"Error saving PID: {e}", True)

def remove_pid():
    """Remove PID file if it belongs to current process"""
    try:
        if os.path.exists(PID_FILE):
            with open(PID_FILE, "r") as f:
                saved_pid = f.read().strip()
                if saved_pid == str(os.getpid()):
                    os.remove(PID_FILE)
                    log("PID file removed")
    except:
        pass

def save_last_update_id(update_id):
    """Save last processed Telegram update ID"""
    try:
        with open(COMMAND_FILE, "w") as f:
            f.write(str(update_id))
    except:
        pass

def load_last_update_id():
    """Load last processed Telegram update ID"""
    try:
        if os.path.exists(COMMAND_FILE):
            with open(COMMAND_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    return int(content)
    except:
        pass
    return 0

def cleanup():
    """Cleanup resources on exit"""
    remove_pid()
    log("Bot stopped")

def signal_handler(signum, frame):
    """Handle termination signals"""
    log(f"Received signal {signum}, stopping...")
    cleanup()
    sys.exit(EXIT_NORMAL)

# Register signal handlers
atexit.register(cleanup)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def send_message(text):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {'chat_id': USER_ID, 'text': text}
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            return True
        else:
            log(f"Telegram API error: {response.status_code}")
            return False
    except Exception as e:
        log(f"Error sending message: {e}")
        return False

def wake_pc_python(mac_address):
    """Send Wake-on-LAN using Python socket"""
    try:
        # Clean MAC address
        mac_clean = mac_address.replace(':', '').replace('-', '')
        
        if len(mac_clean) != 12:
            log(f"Invalid MAC address: {mac_address}")
            return False
        
        # Convert to bytes
        mac_bytes = bytes.fromhex(mac_clean)
        
        # Create magic packet (6xFF + 16*MAC)
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Send to standard WoL ports
        sock.sendto(magic_packet, ('255.255.255.255', 9))
        sock.sendto(magic_packet, ('255.255.255.255', 7))
        sock.close()
        
        log(f"WoL sent (Python) to MAC: {mac_address}")
        return True
        
    except Exception as e:
        log(f"Python WoL error: {e}", True)
        return False

def wake_pc_wakeonlan(mac_address):
    """Send Wake-on-LAN using wakeonlan utility"""
    try:
        wakeonlan_path = "/data/data/com.termux/files/usr/bin/wakeonlan"
        
        if not os.path.exists(wakeonlan_path):
            log("wakeonlan not found")
            return False
        
        # Execute wakeonlan command
        result = subprocess.run(
            [wakeonlan_path, mac_address],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            log(f"wakeonlan success: {result.stdout.strip()}")
            return True
        else:
            log(f"wakeonlan error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        log("wakeonlan timeout (packet may have been sent)")
        return True
    except Exception as e:
        log(f"wakeonlan error: {e}", True)
        return False

def wake_pc():
    """Main function to wake up PC"""
    log(f"Waking up PC with MAC: {MAC}")
    
    # Try wakeonlan utility first
    if wake_pc_wakeonlan(MAC):
        return True
    
    # Fallback to Python implementation
    log("Trying Python WoL...")
    return wake_pc_python(MAC)

def get_current_update_id():
    """Get current update ID from Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('result'):
                updates = data['result']
                if updates:
                    return updates[-1]['update_id']
        return 0
    except Exception as e:
        log(f"Error getting update_id: {e}")
        return 0

def restart_bot():
    """Restart the bot with proper queue clearing"""
    log("Restart requested")
    
    # Get current update ID from Telegram
    current_id = get_current_update_id()
    if current_id > 0:
        # Save current ID + 1 for new bot
        save_last_update_id(current_id + 1)
        log(f"Set new update_id: {current_id + 1}")
    
    # Send restart notification
    send_message("🔄 Restarting bot...")
    time.sleep(1)
    
    log("Exiting for restart...")
    sys.exit(EXIT_RESTART)

def stop_bot():
    """Stop the bot"""
    log("Stop requested")
    
    send_message("🛑 Stopping bot...")
    time.sleep(1)
    
    log("Shutting down...")
    sys.exit(EXIT_NORMAL)

def get_status():
    """Get bot status information"""
    uptime = int(time.time() - START_TIME)
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60
    seconds = uptime % 60
    
    status = f"""📊 Bot Status:
• PID: {os.getpid()}
• Uptime: {hours}h {minutes}m {seconds}s
• MAC: {MAC}
• Version: 2.2
• Started: {time.ctime(START_TIME)}"""
    
    return status

def clear_telegram_queue():
    """Clear Telegram command queue on startup"""
    try:
        # Get all updates
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('result'):
                updates = data['result']
                if updates:
                    last_id = updates[-1]['update_id']
                    # Set offset to clear queue
                    params = {'offset': last_id + 1}
                    requests.get(url, params=params, timeout=5)
                    log(f"Telegram queue cleared, last ID: {last_id}")
                    
                    # Return last ID for new bot
                    return last_id
        return 0
    except Exception as e:
        log(f"Error clearing queue: {e}")
        return 0

def main():
    """Main bot function"""
    print("\n" + "="*60)
    print("🤖 PC Wake Bot v2.2")
    print(f"PID: {os.getpid()}")
    print("="*60)
    
    # Clear Telegram queue on startup
    last_telegram_id = clear_telegram_queue()
    
    # Decide which update_id to use
    saved_id = load_last_update_id()
    
    if saved_id > last_telegram_id and saved_id > 0:
        last_update_id = saved_id
        log(f"Using saved update_id: {last_update_id}")
    else:
        last_update_id = last_telegram_id
        save_last_update_id(last_update_id)
        log(f"Using Telegram update_id: {last_update_id}")
    
    # Save PID
    save_pid()
    
    log("Bot started!")
    
    # Send startup notification
    if not send_message(f"🤖 Bot started (PID: {os.getpid()})"):
        log("⚠️ Failed to send startup message")
    
    error_count = 0
    
    try:
        while True:
            try:
                # Get updates from Telegram
                url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
                params = {
                    'offset': last_update_id + 1,
                    'timeout': 30,
                    'allowed_updates': ['message']
                }
                
                response = requests.get(url, params=params, timeout=35)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('ok') and data.get('result'):
                        for update in data['result']:
                            update_id = update['update_id']
                            
                            if update_id > last_update_id:
                                last_update_id = update_id
                                save_last_update_id(update_id)
                                
                                if 'message' in update and 'text' in update['message']:
                                    text = update['message']['text'].strip()
                                    log(f"Command: {text}")
                                    
                                    if text.lower() == '/start':
                                        send_message("""Hello! I'm a PC Wake Bot.

Available commands:
/wake - Wake up PC
/status - Bot status
/restart - Restart bot
/stop - Stop bot""")
                                    
                                    elif text.lower() == '/wake':
                                        log("Executing /wake command")
                                        if wake_pc():
                                            send_message("✅ Magic Packet sent! PC should wake up.")
                                        else:
                                            send_message("❌ Failed to send Wake-on-LAN packet")
                                    
                                    elif text.lower() == '/status':
                                        send_message(get_status())
                                    
                                    elif text.lower() == '/restart':
                                        restart_bot()  # Won't return
                                    
                                    elif text.lower() == '/stop':
                                        stop_bot()  # Won't return
                
                # Reset error counter
                error_count = 0
                
                # Short pause
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                error_count += 1
                log(f"Network error (#{error_count}): {e}")
                
                if error_count > 10:
                    log("Too many network errors, restarting...")
                    send_message("⚠️ Many network errors, restarting...")
                    time.sleep(2)
                    sys.exit(EXIT_RESTART)
                else:
                    time.sleep(5)
                    
            except Exception as e:
                error_count += 1
                log(f"Unexpected error (#{error_count}): {e}", True)
                
                if error_count > 5:
                    log("Too many errors, restarting...")
                    sys.exit(EXIT_CRASH)
                else:
                    time.sleep(5)
    
    except KeyboardInterrupt:
        log("Stopped by user (Ctrl+C)")
        send_message("🛑 Bot stopped by user")
    
    except Exception as e:
        log(f"Critical error in main: {e}", True)
        sys.exit(EXIT_CRASH)

if __name__ == '__main__':
    try:
        main()
        
    except Exception as e:
        log(f"💥 Unhandled error: {e}", True)
        
        # Write to crash log
        try:
            with open(CRASH_LOG, "a") as f:
                f.write(f"[{time.ctime()}] CRASH: {e}\n")
                import traceback
                f.write(traceback.format_exc() + "\n" + "="*50 + "\n")
        except:
            pass
        
        sys.exit(EXIT_CRASH)
