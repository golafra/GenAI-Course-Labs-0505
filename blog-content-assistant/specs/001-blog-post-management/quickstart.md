# QuickStart (وضعیت فاز ۱)

> این فایل در گام ۱۵ باید با دستورهای واقعاً اجراشده بازنویسی شود. فعلاً فقط اسکلت Host.

## پیش‌نیاز

- Python 3.11+

## راه‌اندازی

```powershell
cd blog-content-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

## اجرای API

```powershell
$env:BLOG_LAB_DATABASE_PATH = "./data/blog_lab.db"
uvicorn blog_lab.api.main:create_app --factory --app-dir src --reload
```

سپس `GET http://127.0.0.1:8000/health` باید `{"status":"ok"}` بدهد.

Auth، Post و Editor هنوز پیاده نشده‌اند (گام ۱۱ به بعد).
