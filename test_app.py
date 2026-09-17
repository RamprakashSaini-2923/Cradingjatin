import os
import sys
import unittest
from fastapi.testclient import TestClient

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from server import app
import database

class TestMarketplaceApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()
        cls.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get("status"), "ok")

    def test_settings_public(self):
        res = self.client.get("/api/settings")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("upi_id"), "9412339808@fam")
        # Ensure admin_pin is NOT exposed
        self.assertNotIn("admin_pin", data)

    def test_products_list(self):
        res = self.client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        products = res.json()
        self.assertGreater(len(products), 0)

        # Test filtering by category
        res_gaming = self.client.get("/api/products?category=gaming")
        self.assertEqual(res_gaming.status_code, 200)
        for p in res_gaming.json():
            self.assertEqual(p["category"], "gaming")

    def test_order_lifecycle(self):
        # 1. Place order
        order_payload = {
            "product_id": 1,
            "customer_email": "tester@example.com",
            "utr_number": "428192847192",
            "referral_code": "DISCOUNT10"
        }
        res_order = self.client.post("/api/orders", json=order_payload)
        self.assertEqual(res_order.status_code, 200)
        order_data = res_order.json().get("order")
        order_id = order_data["order_id"]
        self.assertTrue(order_id.startswith("VM-"))
        self.assertEqual(order_data["status"], "pending")

        # 2. Track order (status pending, voucher code empty)
        res_track = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(res_track.status_code, 200)
        tracked = res_track.json()
        self.assertEqual(tracked["status"], "pending")
        self.assertEqual(tracked["voucher_code"], "")

        # 3. Admin login check
        res_login = self.client.post("/api/admin/login", json={"pin": "1234"})
        self.assertEqual(res_login.status_code, 200)
        admin_pin = res_login.json().get("token")

        # 4. Admin stats check
        res_stats = self.client.get("/api/admin/stats", headers={"X-Admin-Pin": admin_pin})
        self.assertEqual(res_stats.status_code, 200)
        self.assertGreaterEqual(res_stats.json().get("total_orders"), 1)

        # 5. Admin approves order with voucher code
        test_voucher_code = "STEAM-ABC12-XYZ89"
        res_approve = self.client.post(
            f"/api/admin/orders/{order_id}/action",
            headers={"X-Admin-Pin": admin_pin},
            json={"action": "approve", "voucher_code": test_voucher_code}
        )
        self.assertEqual(res_approve.status_code, 200)
        self.assertEqual(res_approve.json().get("status"), "completed")

        # 6. Customer tracking reveals the code!
        res_track_after = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(res_track_after.status_code, 200)
        tracked_after = res_track_after.json()
        self.assertEqual(tracked_after["status"], "completed")
        self.assertEqual(tracked_after["voucher_code"], test_voucher_code)

    def test_static_assets(self):
        # Verify index.html is served
        res_index = self.client.get("/")
        self.assertEqual(res_index.status_code, 200)
        self.assertIn("Card Shop", res_index.text)

        # Verify QR image is accessible
        res_qr = self.client.get("/static/assets/upi_qr.png")
        self.assertEqual(res_qr.status_code, 200)

if __name__ == "__main__":
    unittest.main()
