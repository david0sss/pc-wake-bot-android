# pc-wake-bot-android
A Telegram bot that allows you to wake up your PC remotely using Wake-on-LAN from your Android phone (via Termux).
# README.md - Complete Version

# PC Wake Bot for Android 📱➡️💻

A Telegram bot that allows you to wake up your PC remotely using Wake-on-LAN from your Android phone (via Termux).

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Termux](https://img.shields.io/badge/Android-Termux-green?logo=android)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🔔 **Wake up your PC** from anywhere using Telegram
- 📱 **Android phone** as a remote control (via Termux)
- 🔄 **Auto-restart** on crashes
- 📊 **Status monitoring** and logging
- 🛡️ **Secure** - Only responds to your User ID
- 🚀 **Easy setup** with bash scripts
- 🧠 **Smart queue management** - No duplicate commands
- 📝 **Comprehensive logging** - Debug easily

## 📋 Prerequisites

### Hardware Requirements:
- Android phone (with Termux installed)
- PC with Wake-on-LAN support (most modern PCs have this)
- Both devices on same network (or port forwarding configured)

### Software Requirements:
- **Termux** app (from F-Droid or GitHub)
- **Python 3.10+** (installed via Termux)
- **Telegram account** (free)
- **Internet connection** on both devices

## 🚀 Quick Installation (5 Minutes)

### Step 1: Install Termux
**Recommended**: Download from [F-Droid](https://f-droid.org/en/packages/com.termux/) (more stable)

**Alternative**: Download from [GitHub Releases](https://github.com/termux/termux-app/releases)

### Step 2: Install Dependencies
Open Termux and run:

#### Update package lists
```pkg update && pkg upgrade -y```

#### Install Python
```pkg install python```

#### Install required packages
```pkg install python wakeonlan git nano curl wget -y```
or
```pip install wakeonlan```

#### Install Python library
```pip install requests```

### Step 3: Clone This Repository
```bash
cd ~
git clone https://github.com/yourusername/pc-wake-bot-android.git
cd pc-wake-bot-android
```

### Step 4: Configure the Bot
Edit the configuration file:
```bash
nano pc_wake_bot.py
```

Find these lines (around line 15-18) and replace with your values:
```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"      # Get from @BotFather
USER_ID = YOUR_TELEGRAM_USER_ID_HERE         # Get from @userinfobot
MAC = "YOUR_PC_MAC_ADDRESS_HERE"            # Format: "AA:BB:CC:DD:EE:FF"
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### Step 5: Make Scripts Executable
```bash
chmod +x start_bot.sh stop_bot.sh restart_bot.sh clear_queue.sh
chmod +x pc_wake_bot.py
```

### Step 6: Run the Bot
#### Run only after [connecting your telegram bot](#-Telegram-Bot-Creation) to your termux script, otherwise it wouldn't work
```bash
./start_bot.sh
```

Done! Your bot is now running. Send `/start` to your Telegram bot to begin.

## 📖 Detailed Setup Guide

### Part 1: Telegram Bot Creation

#### 1.1 Create Bot with BotFather
1. Open Telegram app
2. Search for `@BotFather` (official bot creator)
3. Send `/newbot`
4. Follow prompts:
   - Choose bot name: `My PC Wake Bot`
   - Choose username: `my_pc_wake_bot` (must end with "bot")
5. **IMPORTANT**: Save the token shown (looks like `1234567890:ABCdefGHIjklMnoPQRstuVWXYZ`)
6. Optional: Set bot profile picture with `/setuserpic`

#### 1.2 Get Your User ID
1. Open Telegram
2. Search for `@userinfobot`
3. Send `/start`
4. Save the numeric ID shown (like `1420529753`)

#### 1.3 Start Chat with Your Bot
1. Search for your bot by username (e.g., `@my_pc_wake_bot`)
2. Click "Start" or send `/start`

### Part 2: PC Configuration

#### 2.1 Find Your PC's MAC Address
**Windows:**
*Open Command Prompt as Administrator*
```cmd
ipconfig /all
```
*Look for your active network adapter (Wi-Fi or Ethernet)
Find "Physical Address" - that's your MAC
Example: 50-EB-F2-21-E3-FF*
**Linux:**
```bash
ip link show
```
*Look for "link/ether" followed by MAC address*

**Mac OS:**
```bash
ifconfig en0 | grep ether
```

#### 2.2 Enable Wake-on-LAN in BIOS/UEFI
1. Restart your PC
2. Enter BIOS/UEFI (usually press: F2, DEL, F10, or F12 during boot)
3. Navigate to:
   - Power Management → Wake-on-LAN → **Enabled**
   - Or: Advanced → PCI-E Configuration → Power On By PCI-E → **Enabled**
   - Or: APM Configuration → Power On By PCI-E → **Enabled**
4. Save and exit

#### 2.3 Enable Wake-on-LAN in Windows
1. Open Device Manager (`Win + X → Device Manager`)
2. Expand "Network adapters"
3. Right-click your network adapter → Properties
4. Go to "Power Management" tab:
   - ✅ Check "Allow this device to wake the computer"
   - ✅ Check "Only allow a magic packet to wake the computer"
5. Go to "Advanced" tab:
   - Find "Wake on Magic Packet" → Set to **Enabled**
   - Find "Wake on Pattern Match" → Set to **Enabled**
6. Click OK and restart

#### 2.4 Configure Router (Optional - for remote access)
If you want to wake PC from outside your home network (Its neded ONLY if this phone with termux will be outside your home network,
so if you place your old phone with termux always at home on charger, you could wake your pc from outside via telegram also, without port forwording):
1. Log into router admin panel (usually 192.168.1.1 or 192.168.0.1)
2. Find "Port Forwarding" or "Virtual Servers"
3. Add rule:
   - Service: Wake-on-LAN
   - External Port: 7, 9
   - Internal Port: 7, 9
   - Protocol: UDP
   - IP: Your PC's local IP address

### Part 3: Android/Termux Setup

#### 3.1 Termux Initial Setup
##### After installing Termux, run:
```bash
termux-setup-storage
```
##### Grant permission when prompted
Install essential tools
```bash pkg install python wakeonlan git nano curl wget```

##### Verify installations
```bash python --version```  *Should show Python 3.10+*
```bash which wakeonlan```   *Should show /data/data/com.termux/files/usr/bin/wakeonlan*

#### 3.2 Clone and Configure
Clone repository
```bash
cd ~
git clone https://github.com/yourusername/pc-wake-bot-android.git
cd pc-wake-bot-android
```
Edit configuration
```bash 
nano pc_wake_bot.py
```
***Edit the 3 variables mentioned earlie
Save with Ctrl+X, Y, Enter***

## 🤖 Telegram Commands Reference

| Command | Description | Example Response |
|---------|-------------|------------------|
| `/start` | Show welcome message and commands | Lists all available commands |
| `/wake` | Send Wake-on-LAN packet to PC | "✅ Magic Packet sent! PC should wake up." |
| `/status` | Show bot status information | Bot uptime, PID, MAC address, etc. |
| `/restart` | Restart the bot | "🔄 Restarting bot..." |
| `/stop` | Stop the bot | "🛑 Stopping bot..." |

## 📁 Project Structure

```
pc-wake-bot-android/
├── pc_wake_bot.py          # Main bot script (Python)
├── start_bot.sh            # Start script with auto-restart
├── stop_bot.sh             # Stop bot and all processes
├── restart_bot.sh          # Restart bot (stop + start)
├── clear_queue.sh          # Clear Telegram command queue
├── README.md              # This documentation
├── LICENSE                # MIT License file
├── .gitignore            # Git ignore file
├── bot.log               # Bot activity logs (auto-generated)
├── crash.log             # Crash reports (auto-generated)
├── supervisor.log        # Supervisor output (auto-generated)
├── bot.pid              # Process ID file (auto-generated)
└── last_update_id.txt   # Last processed command ID (auto-generated)
```

## 🔧 Management Scripts

### Start Bot
```bash
./start_bot.sh
```
Starts bot with supervisor that automatically restarts on crashes.

### Stop Bot
```bash
./stop_bot.sh
```
Stops bot and all related processes.

### Restart Bot
```bash
./restart_bot.sh
```
Restarts bot (convenient for updates).

### Clear Command Queue
```bash
./clear_queue.sh
```
Clears stuck Telegram commands if bot stops responding.

## 🐛 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Bot Doesn't Start
**Symptoms:** Script exits immediately or shows errors

**Solutions:**
Check Python installation
```bash
python --version
```
Check dependencies
```bash
pip list | grep requests
```
Check file permissions
```bash
ls -la *.sh *.py
```
Check logs
```bash
tail -f bot.log
```

#### 2. Wake-on-LAN Doesn't Work
**Symptoms:** PC doesn't wake up

**Checklist:**
- ✅ PC is connected to power (not sleeping/hibernating)
- ✅ MAC address is correct (case-sensitive)
- ✅ Wake-on-LAN enabled in BIOS
- ✅ Wake-on-LAN enabled in Windows/Linux
- ✅ Phone and PC on same network
- ✅ Router supports Wake-on-LAN broadcasts
- ✅ **You can also try to wake your pc via another app,
you can find a lot of in google play or in appstore**

**Test from same network first:**
In Termux, test WoL locally
```bash
wakeonlan YOUR_MAC_ADDRESS
```

#### 3. Bot Stops Responding to Commands
**Symptoms:** Commands sent but no response

**Solution:**
```bash
./clear_queue.sh
./restart_bot.sh
```

#### 4. Termux Closes on App Switch
**Solution:** Use Termux:Widget or Termux:Boot for background operation

#### 5. "Permission Denied" Error
**Solution:**
```bash
chmod +x *.sh *.py
```

### Viewing Logs
Real-time bot activity
```bash
tail -f bot.log
```
Supervisor output
```bash
tail -f supervisor.log
```
Error reports
```bash
tail -f crash.log
```
All logs combined
```
tail -f *.log
```

## 🔒 Security Best Practices

### 1. Protect Your Bot Token
- Never share your bot token
- Don't commit token to public repositories
- Use environment variables for production

### 2. Network Security
- Use on trusted networks only
- Configure router firewall if using remotely
- Consider VPN for remote access

### 3. Regular Maintenance
Update packages monthly
```bash
pkg update && pkg upgrade
```
Update Python packages
```bash
pip install --upgrade requests
```
Clear old logs
```bash
find . -name "*.log" -mtime +30 -delete
```

## 🏗️ Technical Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Android       │     │   Telegram      │     │      PC         │
│   Phone         │────▶│      Bot        │────▶│   (Target)      │
│                 │     │                 │     │                 │
│  • Termux       │     │  • @BotFather   │     │  • WoL Enabled  │
│  • Python       │     │  • Your Bot     │     │  • Network Card │
│  • Scripts      │     │  • Commands     │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        └────────────────────────┴────────────────────────┘
                               LAN/WAN
```

### How It Works:
1. **Termux** runs Python script continuously
2. **Telegram API** delivers your commands to the script
3. **Bot** validates commands and your User ID
4. **Wake-on-LAN** packet sent to PC's MAC address
5. **PC network card** detects magic packet and triggers wake-up

## 🌐 Advanced Configuration

### Run Bot on Boot (Termux:Boot)
1. Install Termux:Boot from F-Droid
2. Create boot script:
```bash
mkdir -p ~/.termux/boot
nano ~/.termux/boot/start_pc_bot.sh
```
3. Add content:
```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/pc-wake-bot-android
./start_bot.sh
```
4. Make executable:
```bash
chmod +x ~/.termux/boot/start_pc_bot.sh
```

### Multiple PCs Configuration
Edit `pc_wake_bot.py` to support multiple MACs:
```python
PCs = {
    "livingroom": "AA:BB:CC:DD:EE:FF",
    "bedroom": "11:22:33:44:55:66",
    "office": "FF:EE:DD:CC:BB:AA"
}

# Then modify command handling to accept /wake livingroom
```

### Custom Wake Methods
Add custom wake methods in `wake_pc()` function:
```python
def wake_pc():
    # Method 1: wakeonlan utility
    # Method 2: Python socket
    # Method 3: HTTP request to router API
    # Method 4: SSH to Raspberry Pi
```

## 📊 Monitoring and Maintenance

### Daily Checks
Check if bot is running
```bash
ps aux | grep python | grep -v grep
```
Check logs for errors
```bash
grep -i error bot.log | tail -5
```
Check last activity
```bash
tail -5 bot.log
```

### Weekly Maintenance
Rotate logs (keep 7 days)
```bash
find . -name "*.log" -mtime +7 -delete
```
Update packages
```bash
pkg update && pkg upgrade
pip install --upgrade requests
```

### Monthly Tasks
Backup configuration
```bash
cp pc_wake_bot.py pc_wake_bot.py.backup_$(date +%Y%m%d)
```
Review crash logs
```bash
cat crash.log | wc -l  # Count crashes
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Setup
Clone for development
```bash
git clone https://github.com/yourusername/pc-wake-bot-android.git
cd pc-wake-bot-android
```
Create virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # On Termux: source venv/bin/activate.fish
```
Install dev dependencies
```bash
pip install -r requirements.txt
```

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Update documentation when changing features

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Why MIT License?**
- Permissive - allows commercial use
- Simple and understood by everyone
- Compatible with GPL
- No liability or warranty

## ⭐ Support the Project

If this project helped you:
1. **Star** the repository on GitHub
2. **Share** with friends who might find it useful
3. **Contribute** improvements or bug fixes
4. **Follow** for updates

## 📞 Need Help?

### Before Asking for Help:
1. Check the [Troubleshooting](#-troubleshooting-guide) section
2. Look at existing [Issues](https://github.com/david0sss/pc-wake-bot-android/issues)
3. Search closed issues for similar problems
4. **ALWAYS use AI firstly to analyse the code and errors, it helps VERY often.**

### When Creating an Issue:
Please include:
1. **Problem description**: What happens vs what you expect
2. **Steps to reproduce**: Exactly how to trigger the issue
3. **Logs**: Relevant sections from `bot.log` and `crash.log`
4. **Environment**: 
   - Phone model and Android version
   - Termux version (`pkg show termux`)
   - Python version (`python --version`)

## 🔗 Useful Links

- [Termux Official Wiki](https://wiki.termux.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Wake-on-LAN Wikipedia](https://en.wikipedia.org/wiki/Wake-on-LAN)
- [MIT License Explained](https://choosealicense.com/licenses/mit/)

## 🙏 Acknowledgments

- **Termux Team** for amazing Android terminal emulator
- **Telegram** for free bot platform
- **Python Community** for excellent libraries
- **All Contributors** who helped improve this project

---

**Note**: For Wake-on-LAN to work across different networks (outside your home), you need to configure port forwarding on your router for UDP ports 7 and 9 to your PC's local IP address. (Its neded ONLY if this phone with termux will be outside your home network,
so if you place your old phone with termux always at home on charger, you could wake your pc from outside via telegram also, without port forwording)

**Disclaimer**: Use this tool responsibly. Only wake PCs you own or have permission to access.
```
