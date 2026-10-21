# مبنای فنی — blog-content-assistant

| تصمیم | انتخاب | دلیل کوتاه |
|--------|--------|------------|
| زبان | Python 3.11+ | پشتهٔ شخصی دوره |
| API | FastAPI | OpenAPI خودکار، تست آسان |
| اعتبارسنجی | Pydantic v2 | Schema صریح |
| ذخیره | SQLite فایل محلی | بدون سرویس بیرونی در MVP |
| ORM | SQLAlchemy 2.x (از فاز ۲/۳) | Adapter زیر `infrastructure` |
| تست | pytest + httpx | Unit و Integration سبک |
| Auth (از گام ۱۱) | Bearer opaque token + hash در DB | نقش از Client پذیرفته نمی‌شود |
| AI / MCP | بعد از Feature اول | مطابق Constitution |

## محدودیت‌های Startup (فاز ۱)

- مسیر دیتابیس از تنظیمات خوانده می‌شود؛ خالی/نامعتبر → Fail-fast.
- پیام خطا مقدار مسیر حساس یا Secret را چاپ نمی‌کند.
- Startup عادی Migration یا Provision ضمنی انجام نمی‌دهد.
