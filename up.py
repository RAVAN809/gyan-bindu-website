import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import time
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import hashlib

# Configuration
API_ID = 22951855
API_HASH = "92b8b324f4b4baf7017847a4a26d73fa"
DEFAULT_BASE_FOLDER = "/storage/emulated/0/RAVAN_ALL/"
SESSION_STRING = open("session.txt").read().strip()

# Performance optimization settings
MAX_CONCURRENT_UPLOADS = 5  # Telegram API limits
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for faster processing
BATCH_SIZE = 10  # Process files in batches

class TurboChannelUploader:
    def __init__(self):
        self.client = None
        self.channels = []
        self.upload_semaphore = asyncio.Semaphore(MAX_CONCURRENT_UPLOADS)
        self.executor = ThreadPoolExecutor(max_workers=10)
    
    async def connect(self):
        """Connect to Telegram with optimized settings"""
        self.client = TelegramClient(
            StringSession(SESSION_STRING), 
            API_ID, 
            API_HASH,
            connection_retries=10,
            retry_delay=1,
            timeout=60,
            flood_sleep_threshold=60
        )
        await self.client.start()
        print("⚡ Turbo Mode: Connected to Telegram")
    
    async def get_all_channels(self):
        """Get all channels with caching"""
        print("🚀 Loading channels in turbo mode...")
        self.channels = []
        
        # Use faster iteration with limits
        async for dialog in self.client.iter_dialogs(limit=100):
            if dialog.is_channel or dialog.is_group:
                self.channels.append({
                    'name': dialog.name,
                    'entity': dialog.entity,
                    'id': dialog.id
                })
        
        print(f"✅ Found {len(self.channels)} channels/groups")
        return self.channels
    
    def show_channel_menu(self):
        """Optimized channel selection"""
        print("\n" + "="*50)
        print("🚀 TURBO UPLOAD - SELECT CHANNEL")
        print("="*50)
        
        for i, channel in enumerate(self.channels[:20]):
            print(f"{i+1:2d}. {channel['name']}")
        
        print("\n0. Exit")
    
    def select_channel(self):
        """Fast channel selection"""
        self.show_channel_menu()
        choice = input("\n🎯 Enter channel number: ").strip()
        
        if choice == "0":
            return None
        
        if choice.isdigit() and 1 <= int(choice) <= len(self.channels):
            return self.channels[int(choice) - 1]
        else:
            print("❌ Invalid choice!")
            return self.select_channel()

    async def preprocess_files(self, folder_path):
        """Pre-process files for maximum speed"""
        print("🔍 Scanning files in turbo mode...")
        
        all_files = []
        total_size = 0
        
        # Fast directory walking with os.scandir
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and not entry.name.startswith('.'):
                    file_size = entry.stat().st_size
                    if file_size > 100:  # Skip empty files
                        all_files.append(entry.path)
                        total_size += file_size
                elif entry.is_dir():
                    # Recursively scan subdirectories
                    sub_files = await asyncio.get_event_loop().run_in_executor(
                        self.executor, 
                        self._scan_subdirectory, 
                        entry.path
                    )
                    all_files.extend(sub_files)
        
        print(f"📦 Found {len(all_files)} files ({total_size/1024/1024:.1f} MB)")
        return all_files

    def _scan_subdirectory(self, folder_path):
        """Scan subdirectory using thread pool"""
        files = []
        for root, dirs, filenames in os.walk(folder_path):
            for file in filenames:
                if not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) > 100:
                        files.append(file_path)
        return files

    async def upload_single_file(self, channel_entity, file_path):
        """Upload single file with optimized settings"""
        async with self.upload_semaphore:  # Rate limiting
            try:
                file_name = os.path.basename(file_path)
                
                # Ultra-fast upload with optimized parameters
                await self.client.send_file(
                    channel_entity,
                    file_path,
                    caption=f"📁 {file_name}",
                    part_size_kb=1024,  # Larger chunks for faster upload
                    file_size=os.path.getsize(file_path),
                    progress_callback=None,  # Disable progress for speed
                    allow_cache=False,
                    fast_upload=True
                )
                
                # Fast file deletion
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, 
                    os.remove, 
                    file_path
                )
                
                return file_name, True
                
            except Exception as e:
                return file_name, False

    async def upload_files_turbo(self, channel, folder_path):
        """Ultra-fast parallel upload with batch processing"""
        start_time = time.time()
        
        print(f"\n🚀 TURBO UPLOAD STARTED")
        print(f"📁 Target: {channel['name']}")
        print(f"📂 Source: {folder_path}")
        print("⚡ Mode: ULTRA FAST + PARALLEL + AUTO-DELETE")
        print("=" * 50)
        
        # Pre-process all files
        files = await self.preprocess_files(folder_path)
        
        if not files:
            print("❌ No valid files found!")
            return
        
        print(f"🎯 Uploading {len(files)} files in parallel...")
        
        # Batch processing for maximum speed
        uploaded = 0
        failed = 0
        batch_count = 0
        
        for i in range(0, len(files), BATCH_SIZE):
            batch_count += 1
            batch = files[i:i + BATCH_SIZE]
            
            print(f"📦 Processing batch {batch_count} ({len(batch)} files)...")
            
            # Create upload tasks for current batch
            upload_tasks = [
                self.upload_single_file(channel['entity'], file_path) 
                for file_path in batch
            ]
            
            # Execute batch in parallel
            batch_results = await asyncio.gather(*upload_tasks, return_exceptions=True)
            
            # Process results
            for file_name, success in batch_results:
                if isinstance(success, bool):
                    if success:
                        uploaded += 1
                        print(f"✅ [{uploaded}] {file_name}")
                    else:
                        failed += 1
                        print(f"❌ Failed: {file_name}")
        
        # Performance summary
        total_time = time.time() - start_time
        files_per_second = uploaded / total_time if total_time > 0 else 0
        
        print("=" * 50)
        print(f"🎉 TURBO UPLOAD COMPLETED!")
        print(f"✅ Successful: {uploaded}")
        print(f"❌ Failed: {failed}")
        print(f"⏰ Total time: {total_time:.1f} seconds")
        print(f"🚀 Speed: {files_per_second:.1f} files/second")
        print(f"💾 Storage freed: {uploaded} files")

    async def run_turbo(self):
        """Main turbo function"""
        await self.connect()
        await self.get_all_channels()
        
        channel = self.select_channel()
        if not channel:
            print("👋 Goodbye!")
            return
        
        folder = input(f"📁 Enter folder path [{DEFAULT_BASE_FOLDER}]: ").strip()
        if not folder:
            folder = DEFAULT_BASE_FOLDER
        
        if not os.path.exists(folder):
            print(f"❌ Folder not found: {folder}")
            return
        
        await self.upload_files_turbo(channel, folder)
        await self.client.disconnect()

# Ultra-fast quick upload
async def turbo_quick_upload(channel_name, folder_path=DEFAULT_BASE_FOLDER):
    """Ultra-fast upload to specific channel"""
    uploader = TurboChannelUploader()
    await uploader.connect()
    await uploader.get_all_channels()
    
    # Fast channel search
    target_channel = None
    for channel in uploader.channels:
        if channel_name.lower() in channel['name'].lower():
            target_channel = channel
            break
    
    if target_channel:
        print(f"🚀 TURBO QUICK UPLOAD: {target_channel['name']}")
        await uploader.upload_files_turbo(target_channel, folder_path)
    else:
        print(f"❌ Channel '{channel_name}' not found!")
    
    await uploader.client.disconnect()

async def main():
    import sys
    
    if len(sys.argv) > 1:
        # Turbo quick mode
        channel_name = sys.argv[1]
        folder = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BASE_FOLDER
        await turbo_quick_upload(channel_name, folder)
    else:
        # Interactive turbo mode
        uploader = TurboChannelUploader()
        await uploader.run_turbo()

if __name__ == "__main__":
    # Set high performance event loop
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())
