# Termux packages installation
pkg update && pkg upgrade -y
pkg install python python-pip android-tools tcpdump netcat-openbsd jq -y

# Python packages
pip install requests flask mitmproxy beautifulsoup4 urllib3

# Create directory
mkdir -p /storage/emulated/0/RAVAN_ALL/Ter/
