# blog-content-assistant

آزمایشگاه شخصی Python برای مسیر **Workshop-1** دوره (BlogSpecLab) با رویکرد SDD.

- **Upstream مفهومی:** [Workshop-1](https://github.com/oroumand/SoftwareEngineering-GenAI-0505/tree/main/Workshop-1)  
- **وضعیت:** معادل گام‌های **۱ تا ۱۰** انجام شده؛ آمادهٔ شروع گام **۱۱ (Auth)**

## این پروژه چیست / چیست نیست

| است | نیست |
|-----|------|
| مسیر SDD کارگاه با Python | کپی خط‌به‌خط نمونهٔ .NET استاد |
| Spec / Plan / Tasks فارسی | محصول Production کامل |
| اسکلت + `/health` + تست Startup | Auth و Post (از گام ۱۱) |

جزئیات تکلیف‌محور و فلوچارت: [`docs/lab-steps-01-10.md`](docs/lab-steps-01-10.md)

## ساختار

```text
.specify/memory/constitution.md
AGENTS.md
docs/architecture/technical-baseline.md
docs/lab-steps-01-10.md
specs/001-blog-post-management/
src/blog_lab/{domain,application,infrastructure,api}/
tests/
```

## اجرا

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
$env:BLOG_LAB_DATABASE_PATH = "./data/blog_lab.db"
uvicorn blog_lab.api.main:create_app --factory --app-dir src --reload
```

## مسیر کارگاه

```text
۱–۹ اسناد  →  ۱۰ اسکلت (اینجا)  →  ۱۱ Auth  →  ۱۲ Post  →  ۱۳ Editor  →  ۱۴ Hardening  →  ۱۵ QuickStart
```
