import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Configuration
API_ID = 22951855
API_HASH = "92b8b324f4b4baf7017847a4a26d73fa"

async def create_new_session():
    print("📱 Creating new Telegram session...")
    print("="*50)
    
    # Get phone number from user
    phone = input("Enter your phone number (with country code): ").strip()
    
    # Create new client with StringSession
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    try:
        # Connect and authorize
        await client.start(phone)
        
        # Get the session string
        session_string = client.session.save()
        
        print("\n" + "="*50)
        print("✅ NEW SESSION CREATED SUCCESSFULLY!")
        print("="*50)
        print(f"Phone: {phone}")
        print(f"Session String: {session_string}")
        print("="*50)
        
        # Save to file
        with open("session.txt", "w") as f:
            f.write(session_string)
        
        print("\n✅ Session saved to 'session.txt' file")
        print("📝 Copy this session string and replace in your main script")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(create_new_session())
