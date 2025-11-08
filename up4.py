import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import time

# Configuration - No changes needed
API_ID = 22951855
API_HASH = "92b8b324f4b4baf7017847a4a26d73fa"
FOLDER = "/storage/emulated/0/RAVAN_ALL/all/"
SESSION = open("session.txt").read().strip()

async def max_speed_upload():
    print("🚀 MAX SPEED UPLOAD STARTING...")
    print("⚡ No Questions - Direct Upload")
    print("=" * 40)
    
    start_time = time.time()
    
    # Connect
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.start()
    
    # Find all_Zip channel automatically
    target_channel = None
    async for dialog in client.iter_dialogs():
        if "all_zip" in dialog.name.lower():
            target_channel = dialog.entity
            print(f"🎯 Target: {dialog.name}")
            break
    
    if not target_channel:
        print("❌ all_Zip channel not found! Using first available channel.")
        async for dialog in client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                target_channel = dialog.entity
                print(f"🎯 Using: {dialog.name}")
                break
    
    if not target_channel:
        print("❌ No channels found!")
        return
    
    # Get all files quickly
    all_files = []
    for root, dirs, files in os.walk(FOLDER):
        for file in files:
            if not file.startswith('.'):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size > 100:  # Skip empty files
                    all_files.append(file_path)
    
    total_files = len(all_files)
    print(f"📦 Files found: {total_files}")
    
    if total_files == 0:
        print("❌ No files to upload!")
        return
    
    print("🔥 UPLOADING AT MAX SPEED...\n")
    
    # Upload ALL files as fast as possible
    uploaded = 0
    failed = 0
    
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        
        try:
            # UPLOAD (no caption for max speed)
            await client.send_file(target_channel, file_path)
            
            # DELETE immediately
            os.remove(file_path)
            
            uploaded += 1
            print(f"✅ {uploaded}/{total_files} - {file_name}")
            
        except Exception as e:
            failed += 1
            # Quick error message
            print(f"❌ {file_name}")
    
    # Results
    total_time = time.time() - start_time
    speed = uploaded / total_time if total_time > 0 else 0
    
    print("\n" + "=" * 40)
    print(f"🎉 UPLOAD COMPLETED!")
    print(f"✅ Uploaded: {uploaded}")
    print(f"❌ Failed: {failed}") 
    print(f"⏰ Time: {total_time:.1f}s")
    print(f"⚡ Speed: {speed:.1f} files/sec")
    print(f"💾 Storage Freed: {uploaded} files")
    
    await client.disconnect()

# Run immediately without any questions
asyncio.run(max_speed_upload())
