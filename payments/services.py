# services.py - نسخه اصلاح شده

import requests
from shop.settings import base as settings

class ZarinpalPaymentService:
    def __init__(self, amount, description, callback_url):
        self.amount = amount
        self.description = description
        self.callback_url = callback_url
        self.merchant_id = settings.MERCHANT_ID
        self.request_url = settings.ZARINPAL_REQUEST_URL
        self.verify_url = settings.ZARINPAL_VERIFY_URL
        self.startpay_url = settings.ZARINPAL_STARTPAY_URL
    
    def request_payment(self):
        data = {
            "merchant_id": self.merchant_id,
            "amount": self.amount,
            "description": self.description,
            "callback_url": self.callback_url,
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            self.request_url, 
            json=data,
            headers=headers
        )
        result = response.json()
        
        if result.get("data", {}).get("code") == 100:
            return {
                "authority": result["data"]["authority"],
                "url": self.startpay_url + result["data"]["authority"]
            }
        return result  # برای دیباگ خطا
    
    def verify_payment(self, authority):
        data = {
            "merchant_id": self.merchant_id,
            "amount": self.amount,
            "authority": authority
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            self.verify_url, 
            json=data,
            headers=headers
        )
        result = response.json()
        
        if result.get("data", {}).get("code") == 100:
            return {
                "success": True,
                "ref_id": result["data"]["ref_id"]
            }
        return {
            "success": False,
            "message": result.get("data", {}).get("message", "خطای ناشناخته")
        }