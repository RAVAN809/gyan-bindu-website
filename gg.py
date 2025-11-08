import subprocess
import time
import re
import json
import os
import threading
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class UltimateDeviceManager:
    def __init__(self):
        self.output_dir = "/storage/emulated/0/RAVAN_ALL/Ter/"
        self.captured_data = []
        self.connected_devices = []
        self.transfer_history = []
        self.capture_running = False
        os.makedirs(self.output_dir, exist_ok=True)
        
    def run_command(self, command, wait=True):
        """Run command and return result"""
        try:
            if wait:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result
            else:
                subprocess.Popen(command, shell=True)
                return None
        except Exception as e:
            print(f"❌ Command error: {e}")
            return None

    def show_banner(self):
        """Show awesome banner"""
        print("""
    ╔══════════════════════════════════════════════╗
    ║           🚀 ULTIMATE DEVICE MANAGER         ║
    ║              🤖 ALL-IN-ONE TOOL              ║
    ║                                              ║
    ║ 📱 Wireless Debugging • 📡 Traffic Capture   ║
    ║ 🔑 Headers/Passwords • 📁 File Transfer      ║
    ║ 🎯 Auto Pairing • 📊 Data Analysis           ║
    ╚══════════════════════════════════════════════╝
        """)

    # ==================== WIRELESS DEBUGGING ====================
    def wireless_debugging_setup(self):
        """Complete wireless debugging setup"""
        print("\n" + "="*60)
        print("📱 WIRELESS DEBUGGING SETUP")
        print("="*60)
        
        steps = [
            ("Check USB Connection", self.check_usb_connection),
            ("Enable Developer Options", self.enable_developer_options),
            ("Enable Wireless Debugging", self.enable_wireless_debugging),
            ("Get Pairing Code", self.get_pairing_code),
            ("Auto Pair Device", self.auto_pair_device),
            ("Connect Wirelessly", self.connect_wirelessly),
            ("Verify Connection", self.verify_connection)
        ]
        
        for i, (name, action) in enumerate(steps, 1):
            print(f"\n📝 Step {i}/{len(steps)}: {name}")
            if not action():
                print(f"❌ Failed at: {name}")
                return False
            time.sleep(1)
        
        print("\n✅ WIRELESS DEBUGGING READY!")
        return True

    def check_usb_connection(self):
        result = self.run_command("adb devices")
        if result and "device" in result.stdout:
            print("   ✅ USB Device connected!")
            return True
        print("   ❌ Connect device via USB first!")
        return False

    def enable_developer_options(self):
        print("   👉 Settings > About Phone > Tap Build Number 7 times")
        input("   ⏎ Press Enter after enabling...")
        return True

    def enable_wireless_debugging(self):
        print("   👉 Developer Options > Wireless Debugging > ON")
        print("   👉 Tap 'Pair device with pairing code'")
        input("   ⏎ Press Enter when ready...")
        return True

    def get_pairing_code(self):
        print("   💡 Enter pairing details:")
        ip = input("   IP (e.g., 192.168.1.100): ").strip()
        port = input("   Port (e.g., 34567): ").strip()
        code = input("   Code (6 digits): ").strip()
        
        if ip and port and code:
            self.pairing_info = {'ip': ip, 'port': port, 'code': code}
            return True
        return False

    def auto_pair_device(self):
        pairing = self.pairing_info
        print(f"   🔗 Pairing {pairing['ip']}:{pairing['port']}...")
        
        cmd = f"adb pair {pairing['ip']}:{pairing['port']} {pairing['code']}"
        result = self.run_command(cmd)
        
        if result and "Successfully paired" in result.stdout:
            print("   ✅ Paired successfully!")
            match = re.search(r'(\d+\.\d+\.\d+\.\d+:\d+)', result.stdout)
            if match:
                self.connect_address = match.group(1)
                return True
        print("   ❌ Pairing failed!")
        return False

    def connect_wirelessly(self):
        cmd = f"adb connect {self.connect_address}"
        result = self.run_command(cmd)
        if result and "connected" in result.stdout:
            print("   ✅ Connected wirelessly!")
            return True
        return False

    def verify_connection(self):
        result = self.run_command("adb devices")
        if result and self.connect_address in result.stdout:
            print("   ✅ Wireless connection verified!")
            return True
        return False

    # ==================== TRAFFIC CAPTURE ====================
    def start_traffic_capture(self):
        """Start capturing all traffic data"""
        print("\n" + "="*60)
        print("📡 STARTING TRAFFIC CAPTURE")
        print("="*60)
        
        self.capture_running = True
        self.captured_data = []
        
        # Start capture in thread
        capture_thread = threading.Thread(target=self._capture_traffic)
        capture_thread.daemon = True
        capture_thread.start()
        
        print("🎯 Traffic capture started...")
        print("💡 Press Enter to stop capture")
        input()
        
        self.capture_running = False
        print("🛑 Stopping capture...")
        time.sleep(2)
        
        # Save captured data
        self._save_captured_data()
        
        return len(self.captured_data)

    def _capture_traffic(self):
        """Background traffic capture"""
        self.run_command("adb logcat -c")
        
        while self.capture_running:
            result = self.run_command("adb logcat -d -t 1000")
            if result and result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    self._analyze_traffic_line(line)
            time.sleep(5)

    def _analyze_traffic_line(self, line):
        """Analyze log line for all types of data"""
        # URLs and APIs
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', line, re.IGNORECASE)
        for url in urls:
            if len(url) > 10:
                self._add_captured_data('url', url, line)

        # Headers and Auth
        patterns = {
            'user_agent': r'User-Agent[=:][\'"]?([^\'"]+)',
            'authorization': r'Authorization[=:][\'"]?([^\'"]+)',
            'cookie': r'Cookie[=:][\'"]?([^\'"]+)',
            'x_api_key': r'X-API-Key[=:][\'"]?([^\'"]+)',
            'x_auth_token': r'X-Auth-Token[=:][\'"]?([^\'"]+)',
            'session_id': r'Session[=:][\'"]?([^\'"]+)',
            'password': r'password[=:][\'"]?([^\'"]+)',
            'email': r'email[=:][\'"]?([^\'"]+)',
            'username': r'username[=:][\'"]?([^\'"]+)'
        }
        
        for data_type, pattern in patterns.items():
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 3:
                    self._add_captured_data(data_type, match, line)

        # JSON Data
        json_matches = re.findall(r'\{[^{}]*"[^"]*"[^{}]*\}', line)
        for json_str in json_matches:
            try:
                json_data = json.loads(json_str)
                self._add_captured_data('json_data', json_data, line)
            except:
                pass

        # API Endpoints
        api_patterns = [r'/api/v\d+/[^\s]+', r'/v\d+/[^\s]+', r'/graphql', r'/rest/[^\s]+']
        for pattern in api_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                self._add_captured_data('api_endpoint', match, line)

        # Tokens
        token_patterns = [r'eyJ[^\s]+', r'[A-Fa-f0-9]{32}', r'[A-Fa-f0-9]{64}']
        for pattern in token_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                self._add_captured_data('potential_token', match, line)

    def _add_captured_data(self, data_type, data, raw_line):
        """Add captured data to collection"""
        item = {
            'type': data_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'raw_line': raw_line[:200]  # First 200 chars
        }
        self.captured_data.append(item)
        print(f"   🔍 Captured {data_type}: {str(data)[:50]}...")

    def _save_captured_data(self):
        """Save all captured data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        capture_dir = f"{self.output_dir}/Traffic_Capture_{timestamp}"
        os.makedirs(capture_dir, exist_ok=True)
        
        # Categorize data
        categories = {
            'urls': [x for x in self.captured_data if x['type'] == 'url'],
            'headers': [x for x in self.captured_data if x['type'] in ['user_agent', 'cookie', 'content_type']],
            'auth_data': [x for x in self.captured_data if x['type'] in ['authorization', 'x_api_key', 'x_auth_token']],
            'json_data': [x for x in self.captured_data if x['type'] == 'json_data'],
            'api_endpoints': [x for x in self.captured_data if x['type'] == 'api_endpoint'],
            'tokens': [x for x in self.captured_data if x['type'] == 'potential_token'],
            'passwords': [x for x in self.captured_data if x['type'] == 'password'],
            'sessions': [x for x in self.captured_data if x['type'] in ['session_id', 'token']],
            'user_info': [x for x in self.captured_data if x['type'] in ['email', 'username']]
        }
        
        # Save each category
        for category_name, data in categories.items():
            if data:
                # JSON file
                with open(f"{capture_dir}/{category_name}.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Text file
                with open(f"{capture_dir}/{category_name}.txt", 'w', encoding='utf-8') as f:
                    f.write(f"=== {category_name.upper()} ===\n\n")
                    for item in data:
                        f.write(f"Time: {item['timestamp']}\n")
                        f.write(f"Data: {item['data']}\n")
                        f.write("-" * 50 + "\n\n")
        
        # Save complete data
        with open(f"{capture_dir}/COMPLETE_DATA.json", 'w', encoding='utf-8') as f:
            json.dump(self.captured_data, f, indent=2, ensure_ascii=False)
        
        # Generate summary
        summary = {
            'total_captured': len(self.captured_data),
            'categories': {k: len(v) for k, v in categories.items()},
            'capture_dir': capture_dir,
            'timestamp': timestamp
        }
        
        with open(f"{capture_dir}/SUMMARY.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ All data saved to: {capture_dir}")
        print(f"📊 Capture Summary: {summary}")

    # ==================== FILE MANAGEMENT ====================
    def file_manager(self):
        """Complete file management system"""
        print("\n" + "="*60)
        print("📁 FILE MANAGER")
        print("="*60)
        
        while True:
            print("\n📋 Options:")
            print("1. 📤 Push file to device")
            print("2. 📥 Pull file from device")
            print("3. 📂 List device files")
            print("4. 💾 Backup device data")
            print("5. 🗑️ Clean device cache")
            print("6. 🔙 Back to main menu")
            
            choice = input("\n👉 Enter choice (1-6): ").strip()
            
            if choice == "1":
                self.push_file()
            elif choice == "2":
                self.pull_file()
            elif choice == "3":
                self.list_files()
            elif choice == "4":
                self.backup_device()
            elif choice == "5":
                self.clean_cache()
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice!")

    def push_file(self):
        local_file = input("Local file path: ").strip()
        device_path = input("Device path: ").strip()
        
        if os.path.exists(local_file):
            cmd = f"adb push {local_file} {device_path}"
            result = self.run_command(cmd)
            if result and result.returncode == 0:
                print("✅ File pushed successfully!")
            else:
                print("❌ Push failed!")
        else:
            print("❌ Local file not found!")

    def pull_file(self):
        device_file = input("Device file path: ").strip()
        local_path = input("Local path: ").strip()
        
        cmd = f"adb pull {device_file} {local_path}"
        result = self.run_command(cmd)
        if result and result.returncode == 0:
            print("✅ File pulled successfully!")
        else:
            print("❌ Pull failed!")

    def list_files(self):
        path = input("Device path (default: /sdcard/): ").strip() or "/sdcard/"
        result = self.run_command(f"adb shell ls -la {path}")
        if result:
            print(f"\n📂 Files in {path}:\n{result.stdout}")

    def backup_device(self):
        backup_dir = f"{self.output_dir}/Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        print("📦 Starting backup...")
        self.run_command(f"adb backup -apk -shared -all -f {backup_dir}/backup.ab")
        print(f"✅ Backup saved: {backup_dir}")

    def clean_cache(self):
        print("🧹 Cleaning device cache...")
        self.run_command("adb shell pm clear")
        print("✅ Cache cleaned!")

    # ==================== ADVANCED TOOLS ====================
    def advanced_tools(self):
        """Advanced device tools"""
        print("\n" + "="*60)
        print("🛠️ ADVANCED TOOLS")
        print("="*60)
        
        while True:
            print("\n🔧 Options:")
            print("1. 📱 Device Information")
            print("2. 📶 Network Information")
            print("3. 📷 Take Screenshot")
            print("4. 🎥 Screen Record")
            print("5. 🔍 App Analysis")
            print("6. 📊 System Monitor")
            print("7. 🔙 Back to main menu")
            
            choice = input("\n👉 Enter choice (1-7): ").strip()
            
            if choice == "1":
                self.device_info()
            elif choice == "2":
                self.network_info()
            elif choice == "3":
                self.take_screenshot()
            elif choice == "4":
                self.screen_record()
            elif choice == "5":
                self.app_analysis()
            elif choice == "6":
                self.system_monitor()
            elif choice == "7":
                break
            else:
                print("❌ Invalid choice!")

    def device_info(self):
        print("\n📱 DEVICE INFORMATION:")
        commands = {
            'Model': 'adb shell getprop ro.product.model',
            'Android': 'adb shell getprop ro.build.version.release',
            'API Level': 'adb shell getprop ro.build.version.sdk',
            'Device ID': 'adb shell settings get secure android_id',
            'Battery': 'adb shell dumpsys battery | grep level',
            'Storage': 'adb shell df -h /sdcard'
        }
        
        for name, cmd in commands.items():
            result = self.run_command(cmd)
            if result:
                print(f"   {name}: {result.stdout.strip()}")

    def take_screenshot(self):
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = f"{self.output_dir}/{filename}"
        self.run_command(f"adb exec-out screencap -p > {filepath}")
        print(f"✅ Screenshot: {filepath}")

    def app_analysis(self):
        print("\n🔍 ANALYZING INSTALLED APPS...")
        result = self.run_command("adb shell pm list packages -3")
        if result:
            apps = [line.replace('package:', '').strip() for line in result.stdout.split('\n') if line.strip()]
            print(f"📱 Found {len(apps)} third-party apps")
            
            # Save app list
            with open(f"{self.output_dir}/installed_apps.txt", 'w') as f:
                for app in apps:
                    f.write(f"{app}\n")

    def system_monitor(self):
        print("\n📊 SYSTEM MONITORING...")
        commands = {
            'CPU Usage': 'adb shell top -n 1 | head -10',
            'Memory Info': 'adb shell cat /proc/meminfo | head -5',
            'Battery Status': 'adb shell dumpsys battery',
            'Running Processes': 'adb shell ps | head -15'
        }
        
        for name, cmd in commands.items():
            print(f"\n{name}:")
            result = self.run_command(cmd)
            if result:
                print(result.stdout)

    # ==================== MAIN MENU ====================
    def main_menu(self):
        """Main menu system"""
        while True:
            self.show_banner()
            
            print("\n🏠 MAIN MENU:")
            print("1. 📱 Wireless Debugging Setup")
            print("2. 📡 Traffic Capture (Headers/Passwords/JSON)")
            print("3. 📁 File Manager")
            print("4. 🛠️ Advanced Tools")
            print("5. 📊 View Capture History")
            print("6. 🚪 Exit")
            
            choice = input("\n👉 Enter your choice (1-6): ").strip()
            
            if choice == "1":
                self.wireless_debugging_setup()
            elif choice == "2":
                count = self.start_traffic_capture()
                print(f"🎉 Captured {count} data items!")
            elif choice == "3":
                self.file_manager()
            elif choice == "4":
                self.advanced_tools()
            elif choice == "5":
                self.view_history()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice!")
            
            input("\n⏎ Press Enter to continue...")

    def view_history(self):
        """View capture history"""
        print("\n📊 CAPTURE HISTORY")
        print("="*40)
        
        # Find all capture directories
        captures = []
        if os.path.exists(self.output_dir):
            for item in os.listdir(self.output_dir):
                if item.startswith("Traffic_Capture_"):
                    captures.append(item)
        
        if captures:
            print(f"📁 Found {len(captures)} capture sessions:")
            for capture in sorted(captures)[-10:]:  # Show last 10
                print(f"   • {capture}")
        else:
            print("   No capture history found!")

# 🚀 AUTO-INSTALL AND RUN
def auto_install():
    """Auto-install required packages"""
    print("🔧 AUTO-INSTALLING PACKAGES...")
    
    commands = [
        "pkg update -y && pkg upgrade -y",
        "pkg install python python-pip android-tools -y",
        "pip install requests",
    ]
    
    for cmd in commands:
        print(f"   Running: {cmd.split()[0]}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Success")
        else:
            print(f"   ⚠️ Issue: {result.stderr}")

if __name__ == "__main__":
    # Auto-install on first run
    auto_install()
    
    # Start the ultimate manager
    manager = UltimateDeviceManager()
    manager.main_menu()
