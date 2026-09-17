import os
import sys
import socket
import webbrowser
import threading
import time

# Ensure current directory is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)

import database

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def open_browser(port):
    time.sleep(1.2)
    webbrowser.open(f"http://127.0.0.1:{port}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    local_ip = get_local_ip()

    print("=" * 65)
    print("      CARD SHOP — DIGITAL GIFT CARD & VOUCHER MARKETPLACE")
    print("=" * 65)
    print("[1] Initializing SQLite database...")
    database.init_db()
    print("[✓] Database ready with 16 vouchers, UPI ID, and admin settings.")
    print("\n[2] 🚀 Server starting on 0.0.0.0...")
    print("=" * 65)
    print(f"  💻 PC Localhost:   http://localhost:{port}")
    print(f"  📱 Mobile (Wi-Fi): http://{local_ip}:{port}")
    print("=" * 65)
    print("Tip: To open on your mobile phone, connect to the same Wi-Fi")
    print(f"     and open: http://{local_ip}:{port} in your mobile browser.")
    print("=" * 65)

    # Launch browser on PC automatically if running locally
    if os.environ.get("RENDER") is None and os.environ.get("RAILWAY_ENVIRONMENT") is None:
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
