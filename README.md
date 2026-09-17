# Card Shop — Digital Gift Card & Voucher Marketplace

A full-stack, responsive web application with a modern dark neon/cyberpunk aesthetic for selling digital vouchers, gaming cards, and gift passes. Features integrated UPI QR payments, 2-step checkout (Email + Consent first, then Payment), live order tracking, and an admin management dashboard.

---

## 📱 How to Run & Access on Mobile Phone (Local Wi-Fi)

1. Open PowerShell in the project directory:
   ```powershell
   cd C:\Users\Rohan\.gemini\antigravity\scratch\voucher-marketplace
   python run.py
   ```

2. When the server starts, it binds to `0.0.0.0` and displays your network URLs:
   - **PC Access:** `http://localhost:8000`
   - **Mobile Phone Access (Same Wi-Fi):** `http://[YOUR-LOCAL-IP]:8000` (e.g. `http://172.16.65.219:8000`)
   - **Admin Panel:** `http://localhost:8000/#admin` (Default PIN: `1234`)

> **Mobile Tip:** Connect your phone to the same Wi-Fi router/hotspot as your computer, and open the `http://[YOUR-LOCAL-IP]:8000` link in Chrome/Safari on your phone!

---

## 🌐 How to Push to GitHub & Deploy for Free (Accessible by Anyone Worldwide)

To make your website accessible to anyone in the world on any phone or PC without keeping your computer on:

### Step 1: Push Code to GitHub

Open PowerShell in the folder:
```powershell
cd C:\Users\Rohan\.gemini\antigravity\scratch\voucher-marketplace

# Initialize git repository
git init
git add .
git commit -m "Initial commit of Card Shop Marketplace"

# Add your GitHub repository link and push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/card-shop.git
git push -u origin main
```

### Step 2: Free 1-Click Cloud Deployment (Render.com)

1. Go to [Render.com](https://render.com) and sign up (free).
2. Click **"New +"** ➔ **"Web Service"**.
3. Connect your GitHub repository (`card-shop`).
4. Settings (Render will auto-detect from `render.yaml`):
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Click **"Deploy Web Service"**.

🎉 Within 2 minutes, Render gives you a free live public URL (e.g., `https://card-shop-xyz.onrender.com`) that works on **every PC, iPhone, Android phone, and tablet worldwide**!
