# Research: تصمیم‌های فنی کوتاه

## R1 — Persistence

**تصمیم:** SQLite فایل محلی.  
**چرا:** بدون Docker برای MVP آموزشی؛ قابل پاک‌سازی در تست.  
**جایگزین ردشده:** PostgreSQL زودهنگام.

## R2 — Auth مدل

**تصمیم:** Bearer opaque؛ ذخیرهٔ hash؛ نقش فقط سروری.  
**چرا:** مطابق اصل «Header نقش نمی‌سازد».  
**زمان پیاده‌سازی:** فاز ۲ (گام ۱۱).

## R3 — Concurrency

**تصمیم:** فیلد `version` (UUID یا عدد یکنواخت) + هدر If-Match در API.  
**زمان:** همراه US1/US3.

## R4 — Startup Configuration

**تصمیم:** مسیر DB الزامی و غیرخالی؛ Fail-fast بدون افشای جزئیات حساس؛ بدون Migration ضمنی در Startup.  
**زمان:** فاز ۱ (همین گام).
