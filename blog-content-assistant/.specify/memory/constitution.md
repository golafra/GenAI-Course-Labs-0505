# قانون اساسی — blog-content-assistant

## اصل ۱ — توسعهٔ مبتنی بر مشخصات (SDD)

- هر قابلیت فقط پس از Spec تأییدشده پیاده‌سازی می‌شود.
- تغییر رفتاری مهم ابتدا در Spec ثبت می‌شود، بعد Plan / Tasks / کد / تست.
- خروجی Agent بدون انطباق با Spec و این Constitution پذیرفته نیست.

## اصل ۲ — معماری و جهت وابستگی (Python)

```text
blog-content-assistant/
├── src/blog_lab/
│   ├── domain/           # موجودیت‌ها و ناورداها — بدون FastAPI/DB
│   ├── application/      # Use Case، مجوز، Portها
│   ├── infrastructure/   # SQLite، Adapterها
│   └── api/              # FastAPI، HTTP، Composition
└── tests/
```

قواعد:

1. `domain` به هیچ لایهٔ بیرونی وابسته نیست.
2. `application` فقط به `domain` وابسته است؛ به FastAPI یا SQLAlchemy مستقیم وابسته نمی‌شود.
3. `infrastructure` Portهای `application` را پیاده می‌کند.
4. `api` فقط Composition و نگاشت HTTP است؛ Business Rule تکرار نمی‌شود.
5. پروژهٔ AI / MCP / Vector فقط با نیازمندی تأییدشده اضافه می‌شود.

## اصل ۳ — امنیت و مرز مسئولیت

- قواعد کسب‌وکار در Domain یا Application enforce می‌شوند؛ نه فقط در Prompt.
- Permission جاری از منبع معتبر سمت سرور خوانده می‌شود؛ Header/Body نقش جعلی نمی‌سازد.
- مدل زبانی یا Tool Call به‌تنهایی مجوز تغییر State نمی‌دهد.
- Secret و Credential خام در مخزن یا Log ممنوع است.

## اصل ۴ — کیفیت و آزمون

- قواعد مهم Domain و Application آزمون خودکار دارند.
- آزمون Domain/Application بدون سرویس بیرونی اجرا می‌شود.
- تکمیل قابلیت با Acceptance و شواهد (تست سبز / demo) اثبات می‌شود.

## اصل ۵ — سادگی تدریجی

- نسخهٔ اولیه بدون LLM، MCP، Agent و Vector DB اجرا می‌شود.
- فاز فعلی (معادل گام ۱۰ کارگاه): فقط اسکلت و Startup — نه Auth کامل، نه Post.
- فازهای بعدی (معادل گام ۱۱–۱۵): Auth → Author → Editor → Hardening → QuickStart.
