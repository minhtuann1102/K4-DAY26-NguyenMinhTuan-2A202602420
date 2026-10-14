"""Liệt kê các model Gemini "flash" mà API key hiện tại truy cập được.

Key đọc từ biến môi trường / file .env — không hard-code vào mã nguồn.
    python check_models.py
"""

import json
import os
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "01-function-calling" / ".env")
key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not key:
    raise SystemExit("Thiếu GEMINI_API_KEY hoặc GOOGLE_API_KEY (biến môi trường hoặc .env)")

req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models",
    headers={"x-goog-api-key": key},  # header thay vì ?key= để key không lọt vào URL/log
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())

print("Flash models available:")
for m in data["models"]:
    if "flash" in m["name"].lower():
        print(" ", m["name"])
