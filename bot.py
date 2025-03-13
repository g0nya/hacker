import requests
import hashlib
import hmac
import json
from datetime import datetime

# Ваши данные
MID = "ваш_merchant_id"
SECRET_KEY = "ваш_secret_key"

def generate_signature(mid, timestamp, secret_key):
    # Генерация подписи (HMAC-SHA256)
    message = f"{mid}{timestamp}"
    signature = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature

def create_payment(amount, goods_name, buyer_email):
    # Текущее время для подписи
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Генерация подписи
    signature = generate_signature(MID, timestamp, SECRET_KEY)

    # Данные для запроса
    payload = {
        "mid": MID,
        "timestamp": timestamp,
        "signature": signature,
        "amt": amount,  # Сумма платежа
        "goodsName": goods_name,  # Название товара
        "buyerEmail": buyer_email,  # Email пользователя
        "returnUrl": "https://вашсайт.ру/успешная-оплата",  # URL для перенаправления
    }

    # Отправка запроса к API NicePay
    response = requests.post(
        "https://api.nicepay.co.kr/v1/payments",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
    )

    if response.status_code == 200:
        return response.json().get("paymentUrl")  # URL для оплаты
    else:
        return None  # Ошибка при создании платежа

# Пример использования
payment_url = create_payment(270, "Подписка на бота", "user@example.com")
if payment_url:
    print(f"Оплатите подписку: {payment_url}")
else:
    print("Ошибка при создании платежа.")
