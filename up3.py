import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import time
import aiofiles

# Configuration
API_ID = 22951855
API_HASH = "92b8b324f4b4baf7017847a4a26d73fa"
DEFAULT_BASE_FOLDER = "/storage/emulated/0/RAVAN_ALL/"
SESSION_STRING = open("session.txt").read().strip()

class InstantUploader:
    def __init__(self):
        self.client = None
        self.channels = []
    
    async def connect(self):
        """Instant connection"""
        self.client = TelegramClient(
            StringSession(SESSION_STRING), 
            API_ID, 
            API_HASH,
            connection_retries=3,
            timeout=30
        )
        await self.client.start()
        print("⚡ CONNECTED")
    
    async def get_channels_fast(self):
        """Get channels instantly"""
        self.channels = []
        async for dialog in self.client.iter_dialogs(limit=50):
            if dialog.is_channel or dialog.is_group:
                self.channels.append({
                    'name': dialog.name,
                    'entity': dialog.entity,
                    'id': dialog.id
                })
        return self.channels

    def show_channels_quick(self):
        """Quick channel display"""
        print("\n📋 CHANNELS:")
        for i, channel in enumerate(self.channels[:15]):
            print(f"{i+1}. {channel['name']}")
        print("0. Exit")

    def select_channel_fast(self):
        """Instant channel selection"""
        self.show_channels_quick()
        try:
            choice = int(input("\n👉 Enter number: "))
            if choice == 0:
                return None
            return self.channels[choice-1]
        except:
            return None

    def get_files_instant(self, folder_path):
        """Get files instantly without deep scan"""
        files = []
        try:
            # Only immediate files, no subfolder scanning for speed
            with os.scandir(folder_path) as entries:
                for entry in entries:
                    if entry.is_file() and not entry.name.startswith('.') and entry.stat().st_size > 100:
                        files.append(entry.path)
        except:
            pass
        return files

    async def upload_instant(self, channel, folder_path):
        """INSTANT UPLOAD - No delays"""
        print(f"\n🚀 UPLOADING TO: {channel['name']}")
        print("⚡ TURBO MODE: INSTANT START")
        
        files = self.get_files_instant(folder_path)
        
        if not files:
            print("❌ No files found!")
            return
        
        print(f"📦 Files: {len(files)}")
        start_time = time.time()
        uploaded = 0
        
        # UPLOAD IMMEDIATELY - No batch processing delays
        for file_path in files:
            try:
                file_name = os.path.basename(file_path)
                
                # INSTANT UPLOAD - No progress, no callbacks
                await self.client.send_file(
                    channel['entity'],
                    file_path,
                    caption=file_name,
                    part_size_kb=2048,  # Larger chunks = faster
                    file_size=os.path.getsize(file_path)
                )
                
                # INSTANT DELETE
                os.remove(file_path)
                uploaded += 1
                print(f"✅ {file_name}")
                
            except Exception as e:
                print(f"❌ {os.path.basename(file_path)}")
        
        total_time = time.time() - start_time
        print(f"\n🎉 DONE! {uploaded} files in {total_time:.1f}s")

    async def run_instant(self):
        """Main function - instant start"""
        await self.connect()
        await self.get_channels_fast()
        
        channel = self.select_channel_fast()
        if not channel:
            return
        
        folder = input(f"📁 Folder [{DEFAULT_BASE_FOLDER}]: ").strip() or DEFAULT_BASE_FOLDER
        
        if not os.path.exists(folder):
            print("❌ Folder missing!")
            return
        
        # START UPLOAD IMMEDIATELY
        await self.upload_instant(channel, folder)
        await self.client.disconnect()

# ULTRA FAST - Direct upload without questions
async def instant_upload_to_channel(channel_name, folder_path=DEFAULT_BASE_FOLDER):
    """DIRECT UPLOAD - No questions asked"""
    uploader = InstantUploader()
    await uploader.connect()
    await uploader.get_channels_fast()
    
    # Find channel instantly
    for channel in uploader.channels:
        if channel_name.lower() in channel['name'].lower():
            print(f"🚀 DIRECT UPLOAD: {channel['name']}")
            await uploader.upload_instant(channel, folder_path)
            break
    
    await uploader.client.disconnect()

# SUPER TURBO - Upload everything immediately
async def super_turbo_upload():
    """SUPER TURBO - Upload to first available channel instantly"""
    uploader = InstantUploader()
    await uploader.connect()
    await uploader.get_channels_fast()
    
    if uploader.channels:
        channel = uploader.channels[0]  # First channel
        print(f"🚀 SUPER TURBO: {channel['name']}")
        await uploader.upload_instant(channel, DEFAULT_BASE_FOLDER)
    
    await uploader.client.disconnect()

async def main():
    import sys
    
    if len(sys.argv) > 1:
        # COMMAND: python up3.py "channelname"
        await instant_upload_to_channel(sys.argv[1])
    elif len(sys.argv) > 2:
        # COMMAND: python up3.py "channelname" "/custom/folder"
        await instant_upload_to_channel(sys.argv[1], sys.argv[2])
    else:
        # QUICK INTERACTIVE MODE
        uploader = InstantUploader()
        await uploader.run_instant()

if __name__ == "__main__":
    # NO DELAYS - START IMMEDIATELY
    asyncio.run(main())
