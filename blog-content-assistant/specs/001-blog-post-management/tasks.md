# Tasks: 001-blog-post-management

**ورودی:** Spec، Plan، Research، Data Model، Contracts، Constitution، Technical Baseline.

## فاز ۱ — آماده‌سازی (معادل گام ۱۰) ✅

- [x] T001 ایجاد پکیج‌های `domain` / `application` / `infrastructure` / `api` و `tests` با جهت وابستگی مطابق Constitution  
- [x] T002 ثبت وابستگی‌ها در `pyproject.toml` (FastAPI، Pydantic، pytest، httpx، …)  
- [x] T003 مسیر DB از تنظیمات + `.env.example` + `.gitignore` برای `data/*.db`  
- [x] T004 تست Startup: مسیر معتبر → Host بالا می‌آید؛ مسیر خالی/نامعتبر → Fail-fast بدون افشای جزئیات حساس؛ بدون Migration/Provision ضمنی  

## فاز ۲ — Auth و زیرساخت (معادل گام ۱۱) — بعدی

- [ ] T005–T011 قرارداد UserAccess، Credential، WriteSession، Provision، Bearer handler، ProblemDetails  

## فاز ۳ — US1 نویسنده (گام ۱۲)

- [ ] T012–T020 Domain Post، تست‌ها، Store، Author API  

## فاز ۴ — US2 ویراستار (گام ۱۳)

- [ ] T021–T027 Review / Publish  

## فاز ۵ — US3 Hardening (گام ۱۴)

- [ ] T028–T035 Public API، امنیت، رقابت  

## فاز ۶ — تکمیل (گام ۱۵)

- [ ] T036–T040 OpenAPI، QuickStart واقعی، Validation  

> شناسه‌های T005+ عمداً خلاصه‌اند؛ هنگام اجرای هر گام، از پرامپت همان گام کارگاه الهام بگیر و Taskها را ریز کن — بدون کپی کد .NET.
