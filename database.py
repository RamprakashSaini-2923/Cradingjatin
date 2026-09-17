import sqlite3
import os
import random
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marketplace.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        denomination TEXT NOT NULL,
        price INTEGER NOT NULL,
        original_price INTEGER NOT NULL,
        badge TEXT DEFAULT '',
        icon TEXT DEFAULT 'ticket',
        image_url TEXT DEFAULT '',
        description TEXT DEFAULT '',
        in_stock INTEGER DEFAULT 1,
        popularity_order INTEGER DEFAULT 0
    );
    """)

    # Create Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        amount INTEGER NOT NULL,
        customer_email TEXT NOT NULL,
        referral_code TEXT DEFAULT '',
        utr_number TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        voucher_code TEXT DEFAULT '',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create Settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    # Seed default settings if empty
    default_settings = [
        ("upi_id", "9412339808@fam"),
        ("store_name", "Card Shop Digital Marketplace"),
        ("hero_title", "Instant Digital Gift Cards & Gaming Vouchers"),
        ("hero_subtitle", "Instant fast delivery. 100% verified codes. Trusted by thousands of gamers and digital creators."),
        ("support_telegram", "https://t.me/cardshop_support"),
        ("support_whatsapp", "+91 94123 39808"),
        ("admin_pin", "1234")
    ]
    for k, v in default_settings:
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?);", (k, v))

    # Seed default products if empty
    cursor.execute("SELECT COUNT(*) FROM products;")
    if cursor.fetchone()[0] == 0:
        seed_products = [
            # Gaming Credits
            ("Steam Wallet Code ₹500", "gaming", "Steam", "₹500 Balance", 489, 500, "BESTSELLER", "gamepad-2", "/static/assets/cards/steam_500.svg", "Redeemable on Steam store for any PC game, DLC, or in-game item.", 1, 1),
            ("Steam Wallet Code ₹1,000", "gaming", "Steam", "₹1,000 Balance", 969, 1000, "POPULAR", "gamepad-2", "/static/assets/cards/steam_1000.svg", "Full ₹1000 balance added instantly to your Steam account.", 1, 2),
            ("Valorant 1,000 VP Code", "gaming", "Riot Games", "1000 VP", 799, 850, "HOT", "crosshair", "/static/assets/cards/valorant_vp.svg", "Riot Points for weapon skins, battle pass, and radiant points.", 1, 3),
            ("BGMI 600+60 UC Voucher", "gaming", "BGMI", "660 UC", 749, 799, "INSTANT", "zap", "/static/assets/cards/bgmi_uc.svg", "Instant Royale Pass upgrade and crate openings for BGMI.", 1, 4),
            ("Xbox Game Pass Ultimate", "gaming", "Xbox", "1 Month Pass", 549, 599, "BEST VALUE", "shield", "/static/assets/cards/xbox_pass.svg", "Access 100+ high-quality games on PC, Console, and Cloud.", 1, 5),
            ("PlayStation Store Card ₹1,000", "gaming", "Sony PlayStation", "₹1,000 Balance", 979, 1000, "POPULAR", "disc", "/static/assets/cards/playstation_1000.svg", "Add funds to your PlayStation Network wallet.", 1, 6),
            
            # Subscriptions
            ("Netflix Premium UHD", "subscriptions", "Netflix", "1 Month Voucher", 629, 649, "POPULAR", "tv", "/static/assets/cards/netflix_uhd.svg", "Ultra HD 4K streaming voucher for 1 month.", 1, 7),
            ("Spotify Premium Individual", "subscriptions", "Spotify", "3 Months Voucher", 349, 399, "HOT", "music", "/static/assets/cards/spotify_prem.svg", "Ad-free music streaming, offline downloads, unlimited skips.", 1, 8),
            ("Amazon Prime Video / Delivery", "subscriptions", "Amazon", "3 Months Voucher", 429, 459, "VALUE", "play-circle", "/static/assets/cards/amazon_prime.svg", "Prime video, fast deliveries, and prime gaming benefits.", 1, 9),
            ("YouTube Premium Code", "subscriptions", "Google", "3 Months Voucher", 369, 399, "INSTANT", "video", "/static/assets/cards/youtube_prem.svg", "Ad-free YouTube, background play, and YouTube Music included.", 1, 10),
            
            # Gift Cards
            ("Google Play Gift Card ₹500", "giftcards", "Google Play", "₹500 Code", 489, 500, "BESTSELLER", "play", "/static/assets/cards/play_500.svg", "Purchase apps, games, movies, and in-app purchases on Play Store.", 1, 11),
            ("Google Play Gift Card ₹1,000", "giftcards", "Google Play", "₹1,000 Code", 975, 1000, "POPULAR", "play", "/static/assets/cards/play_1000.svg", "Instant code delivery directly into your tracking portal.", 1, 12),
            ("Amazon Shopping Voucher ₹500", "giftcards", "Amazon", "₹500 Voucher", 495, 500, "POPULAR", "shopping-bag", "/static/assets/cards/amazon_500.svg", "Eligible on millions of physical & digital items across Amazon.", 1, 13),
            ("Apple App Store Card ₹1,000", "giftcards", "Apple", "₹1,000 Code", 985, 1000, "VERIFIED", "smartphone", "/static/assets/cards/apple_1000.svg", "Redeemable for App Store, Apple Arcade, iCloud, and Apple Music.", 1, 14),
            
            # Software Keys
            ("Windows 11 Pro Retail Key", "software", "Microsoft", "Lifetime License", 599, 1999, "HOT DEAL", "laptop", "/static/assets/cards/windows_11.svg", "100% Genuine digital retail license key with instant activation.", 1, 15),
            ("Microsoft Office 365 Pro Plus", "software", "Microsoft", "1 Year License", 799, 2499, "VALUE", "file-text", "/static/assets/cards/office_365.svg", "Includes Word, Excel, PowerPoint, Outlook, and 1TB OneDrive cloud.", 1, 16)
        ]
        cursor.executemany("""
        INSERT INTO products (title, category, brand, denomination, price, original_price, badge, icon, image_url, description, in_stock, popularity_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, seed_products)

    conn.commit()
    conn.close()

def get_all_products(category=None):
    conn = get_connection()
    cursor = conn.cursor()
    if category and category.lower() != 'all':
        cursor.execute("SELECT * FROM products WHERE in_stock = 1 AND category = ? ORDER BY popularity_order ASC;", (category.lower(),))
    else:
        cursor.execute("SELECT * FROM products WHERE in_stock = 1 ORDER BY popularity_order ASC;")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_product_by_id(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?;", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def generate_order_id():
    return f"VM-{random.randint(10000, 99999)}"

def create_order(product_id: int, customer_email: str, utr_number: str, referral_code: str = ""):
    product = get_product_by_id(product_id)
    if not product:
        raise ValueError("Product not found")

    order_id = generate_order_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO orders (id, product_id, product_name, amount, customer_email, referral_code, utr_number, status, voucher_code, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', '', ?, ?);
    """, (
        order_id,
        product["id"],
        f"{product['brand']} - {product['title']} ({product['denomination']})",
        product["price"],
        customer_email.strip().lower(),
        referral_code.strip().upper(),
        utr_number.strip(),
        now,
        now
    ))
    conn.commit()
    conn.close()

    return {
        "order_id": order_id,
        "product_name": product["title"],
        "denomination": product["denomination"],
        "amount": product["price"],
        "customer_email": customer_email,
        "utr_number": utr_number,
        "status": "pending",
        "created_at": now
    }

def get_order_by_id(order_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE UPPER(id) = UPPER(?);", (order_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def track_orders_by_query(query: str):
    conn = get_connection()
    cursor = conn.cursor()
    q = query.strip()
    cursor.execute("""
    SELECT * FROM orders 
    WHERE UPPER(id) = UPPER(?) OR LOWER(customer_email) = LOWER(?)
    ORDER BY created_at DESC;
    """, (q, q))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_all_orders_admin(status_filter: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    if status_filter and status_filter.lower() != 'all':
        cursor.execute("SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC;", (status_filter.lower(),))
    else:
        cursor.execute("SELECT * FROM orders ORDER BY created_at DESC;")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def update_order_status(order_id: str, new_status: str, voucher_code: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE orders 
    SET status = ?, voucher_code = ?, updated_at = ? 
    WHERE UPPER(id) = UPPER(?);
    """, (new_status.lower(), voucher_code.strip(), now, order_id.strip()))
    conn.commit()
    conn.close()

def get_admin_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM orders;")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending';")
    pending_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed';")
    completed_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM orders WHERE status = 'completed';")
    total_revenue = cursor.fetchone()[0]

    conn.close()
    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_revenue": total_revenue
    }

def get_all_settings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM settings;")
    rows = dict(cursor.fetchall())
    conn.close()
    return rows

def update_setting(key: str, value: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?);", (key, value))
    conn.commit()
    conn.close()
