# blog-content-assistant

آزمایشگاه شخصی Python برای مسیر **Workshop-1** با رویکرد SDD.

- **وضعیت:** معادل گام‌های **۱ تا ۱۵** انجام شده  
- **Upstream مفهومی:** [Workshop-1](https://github.com/oroumand/SoftwareEngineering-GenAI-0505/tree/main/Workshop-1)

## گزارش‌های تکلیف

| سند | محتوا |
|-----|--------|
| [docs/lab-steps-01-10.md](docs/lab-steps-01-10.md) | اسناد SDD + اسکلت فاز ۱ |
| [docs/lab-steps-11-15.md](docs/lab-steps-11-15.md) | Auth → Author → Editor → Hardening → QuickStart |

## اجرای سریع

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
$env:BLOG_LAB_DATABASE_PATH = "./data/blog_lab.db"
uvicorn blog_lab.api.main:create_app --factory --app-dir src --reload
```

جزئیات Demo: [`specs/001-blog-post-management/quickstart.md`](specs/001-blog-post-management/quickstart.md)

## معماری

```text
src/blog_lab/
  domain/          # Post aggregate
  application/     # Use cases + UserAccess + AppResult
  infrastructure/  # SQLite store
  api/             # FastAPI routes (thin)
```

## مسیر کارگاه

```text
۱–۹ اسناد → ۱۰ اسکلت → ۱۱ Auth → ۱۲ Author → ۱۳ Editor → ۱۴ Hardening → ۱۵ QuickStart ✅
```
