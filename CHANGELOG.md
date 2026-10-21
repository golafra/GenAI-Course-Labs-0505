# Changelog

## 0.2.0 — ۱۴۰۴/۰۷/۲۹ (2026-10-21)

### افزوده شد

- تکمیل مسیر Workshop گام‌های ۱۱ تا ۱۵ در `blog-content-assistant` (نسخهٔ ساده‌شدهٔ Python)
  - Auth با Bearer و Permission سروری، Provision/Revoke
  - Author API (CRUD + Submit) و Domain پست
  - Editor (RequestChanges / Approve / Publish) با منع خودتأییدی
  - Public API فقط Published و سناریوهای Hardening (stale version، revoke)
  - QuickStart واقعی، قرارداد HTTP به‌روز، گزارش مصور `docs/lab-steps-11-15.md`
- مجموعهٔ آزمون‌های pytest برای Auth، Domain، Editor و Public (۲۲ تست سبز)

### تغییر کرد

- وضعیت تکلیف در README ریشه: گام ۱–۱۵ انجام شد
- نسخهٔ پکیج آزمایشگاه به 0.2.0

## 0.1.0 — ۱۴۰۴/۰۷/۲۹ (2026-10-21)

### افزوده شد

- پوشهٔ `class-research` برای سوالات و تحقیقات کلاسی (جایگزین نام عمومی notes)
- پاسخ مصور «بعد از Spec آیا پرامپت Plan لازم است؟»
- پاسخ مصور «چرخهٔ استاندارد حضور انسان در Agentic SDLC»
- آزمایشگاه `blog-content-assistant` (Python): معادل مفهومی گام‌های ۱–۱۰ کارگاه Workshop-1
  - Constitution، AGENTS، Spec/Plan/Tasks و اسناد SDD
  - اسکلت لایه‌ای FastAPI و تست‌های Startup (فاز ۱)
- به‌روزرسانی README ریشه برای فهرست تکالیف و تحقیقات
