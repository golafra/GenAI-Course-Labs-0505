# راهنمای عامل — blog-content-assistant

پروژهٔ آموزشی Python برای کارگاه BlogSpecLab با رویکرد SDD. ابتدا مدیریت و انتشار پست؛ AI فقط بعد از نیازمندی تأییدشده.

## منابع مرجع

- اصول پایدار: [`.specify/memory/constitution.md`](.specify/memory/constitution.md)
- مبنای فنی: [`docs/architecture/technical-baseline.md`](docs/architecture/technical-baseline.md)
- اسناد هر قابلیت: `specs/<feature>/`
- مسیر کارگاه شخصی: [`docs/lab-steps-01-10.md`](docs/lab-steps-01-10.md)

## روش کار

1. محدودهٔ درخواست را مشخص کن.
2. Spec / Plan / Tasks همان قابلیت را بخوان.
3. فقط همان فاز یا Taskهای مجاز را اجرا کن؛ فاز بعدی را خودکار شروع نکن.
4. ابهام کسب‌وکار را حدس نزن؛ گزارش بده.
5. پس از تغییر: `pytest` و خلاصهٔ Diff.

## ممنوعیت‌ها

- کپی خط‌به‌خط مخزن `.NET` استاد
- افزودن AI/MCP قبل از تکمیل Feature اول
- Secret در کد یا تست
- Business Logic در لایهٔ `api`

## زبان

- مستندات و پیام‌های انسانی: فارسی
- شناسه‌های کد: انگلیسی

## ساخت و آزمون (وضعیت فعلی — پایان گام ۱۵)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
$env:BLOG_LAB_DATABASE_PATH = "./data/blog_lab.db"
uvicorn blog_lab.api.main:create_app --factory --app-dir src
```

گزارش گام ۱۱–۱۵: [`docs/lab-steps-11-15.md`](docs/lab-steps-11-15.md)
