# Tasks: 001-blog-post-management

**ورودی:** Spec، Plan، Research، Data Model، Contracts، Constitution، Technical Baseline.

## فاز ۱ — آماده‌سازی (گام ۱۰) ✅

- [x] T001 لایه‌های domain / application / infrastructure / api  
- [x] T002 وابستگی‌ها در `pyproject.toml`  
- [x] T003 مسیر DB + gitignore  
- [x] T004 تست Startup Fail-fast  

## فاز ۲ — Auth (گام ۱۱) ✅

- [x] T005 `UserAccess` سروری  
- [x] T006 نتیجهٔ Application مستقل از HTTP (`AppResult`)  
- [x] T007 Credential hash در SQLite  
- [x] T008 Store با قفل ساده برای نوشتن  
- [x] T009 Provision / revoke محلی (`/api/ops/*`)  
- [x] T010 Bearer فقط هویت؛ Permission از Store  
- [x] T011 ProblemDetails + If-Match / ETag  

## فاز ۳ — Author US1 (گام ۱۲) ✅

- [x] T012–T014 آزمون Domain / Author API  
- [x] T015–T016 Aggregate Post + Review/Publication  
- [x] T017 SqliteBlogStore برای پست  
- [x] T018–T020 AuthorPostService + مسیرهای Author  

## فاز ۴ — Editor US2 (گام ۱۳) ✅

- [x] T021–T023 آزمون Editor / self-approval  
- [x] T024–T027 EditorPostService + مسیرهای Editor  

## فاز ۵ — Hardening US3 (گام ۱۴) ✅

- [x] T028–T031 Public API + تست عدم افشا  
- [x] T032–T035 revoke permission، stale version، publish idempotent  

## فاز ۶ — تکمیل (گام ۱۵) ✅

- [x] T036 OpenAPI (`/openapi.json`)  
- [x] T037 QuickStart واقعی  
- [x] T038–T040 گزارش تکلیف `docs/lab-steps-11-15.md` + به‌روزرسانی README  

> این Taskها نسخهٔ ساده‌شدهٔ آموزشی‌اند؛ معادل مفهومی پرامپت‌های `Workshop-1/Prompts/step11`…`step15`.
