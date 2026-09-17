import os
from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

import database

# Initialize database
database.init_db()

app = FastAPI(
    title="Card Shop Marketplace API",
    description="Digital Gift Card & Voucher Marketplace Backend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class OrderCreateRequest(BaseModel):
    product_id: int
    customer_email: str
    utr_number: str = Field(..., min_length=6, max_length=30)
    referral_code: Optional[str] = ""

class AdminLoginRequest(BaseModel):
    pin: str

class OrderActionRequest(BaseModel):
    action: str  # "approve" or "reject"
    voucher_code: Optional[str] = ""

class SettingUpdateRequest(BaseModel):
    key: str
    value: str

# Helper auth check
def verify_admin(x_admin_pin: Optional[str]):
    settings = database.get_all_settings()
    configured_pin = settings.get("admin_pin", "1234")
    if not x_admin_pin or x_admin_pin != configured_pin:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin PIN")

# --- PUBLIC API ROUTES ---

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Card Shop Marketplace"}

@app.get("/api/settings")
def get_public_settings():
    settings = database.get_all_settings()
    # Don't expose admin_pin publicly
    return {
        "upi_id": settings.get("upi_id", "9412339808@fam"),
        "store_name": settings.get("store_name", "Card Shop Digital Marketplace"),
        "hero_title": settings.get("hero_title", "Instant Digital Gift Cards & Gaming Vouchers"),
        "hero_subtitle": settings.get("hero_subtitle", "Fast delivery. 100% verified codes. Trusted by gamers & creators."),
        "support_telegram": settings.get("support_telegram", "https://t.me/cardshop_support"),
        "support_whatsapp": settings.get("support_whatsapp", "+91 94123 39808"),
    }

@app.get("/api/products")
def list_products(category: Optional[str] = None):
    return database.get_all_products(category)

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    prod = database.get_product_by_id(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@app.post("/api/orders")
def place_order(payload: OrderCreateRequest):
    if "@" not in payload.customer_email or "." not in payload.customer_email:
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")
    if len(payload.utr_number.strip()) < 6:
        raise HTTPException(status_code=400, detail="Please enter a valid 12-digit UPI Reference / UTR Number.")

    try:
        order = database.create_order(
            product_id=payload.product_id,
            customer_email=payload.customer_email,
            utr_number=payload.utr_number,
            referral_code=payload.referral_code or ""
        )
        return {"success": True, "order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/orders/{order_id}")
def get_order_status(order_id: str):
    order = database.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order ID not found.")
    return order

@app.get("/api/orders/track/search")
def search_order_tracking(q: str = Query(..., min_length=2)):
    orders = database.track_orders_by_query(q)
    return {"query": q, "results": orders}

# --- ADMIN API ROUTES ---

@app.post("/api/admin/login")
def admin_login(payload: AdminLoginRequest):
    settings = database.get_all_settings()
    configured_pin = settings.get("admin_pin", "1234")
    if payload.pin == configured_pin:
        return {"success": True, "token": configured_pin}
    raise HTTPException(status_code=401, detail="Invalid Admin PIN")

@app.get("/api/admin/stats")
def admin_stats(x_admin_pin: Optional[str] = Header(None)):
    verify_admin(x_admin_pin)
    return database.get_admin_stats()

@app.get("/api/admin/orders")
def admin_orders(status: Optional[str] = None, x_admin_pin: Optional[str] = Header(None)):
    verify_admin(x_admin_pin)
    return database.get_all_orders_admin(status)

@app.post("/api/admin/orders/{order_id}/action")
def admin_order_action(order_id: str, payload: OrderActionRequest, x_admin_pin: Optional[str] = Header(None)):
    verify_admin(x_admin_pin)
    order = database.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if payload.action == "approve":
        code = payload.voucher_code or f"VOUCHER-{os.urandom(4).hex().upper()}"
        database.update_order_status(order_id, "completed", code)
        return {"success": True, "status": "completed", "voucher_code": code}
    elif payload.action == "reject":
        database.update_order_status(order_id, "rejected", "")
        return {"success": True, "status": "rejected"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

@app.post("/api/admin/settings")
def update_settings(payload: SettingUpdateRequest, x_admin_pin: Optional[str] = Header(None)):
    verify_admin(x_admin_pin)
    database.update_setting(payload.key, payload.value)
    return {"success": True, "key": payload.key, "value": payload.value}

# --- STATIC FILES & SPA SERVING ---
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.api_route("/", methods=["GET", "HEAD"])
def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.api_route("/orders", methods=["GET", "HEAD"])
def serve_orders_page():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.api_route("/admin", methods=["GET", "HEAD"])
def serve_admin_page():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.api_route("/{full_path:path}", methods=["GET", "HEAD"])
def catch_all(full_path: str):
    # If the file exists in static, return it, else index.html for SPA routes
    file_candidate = os.path.join(static_dir, full_path)
    if os.path.isfile(file_candidate):
        return FileResponse(file_candidate)
    return FileResponse(os.path.join(static_dir, "index.html"))
