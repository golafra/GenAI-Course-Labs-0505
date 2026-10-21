# Plan: 001-blog-post-management

**Spec:** [spec.md](./spec.md)  
**پشته:** Python 3.11+ · FastAPI · SQLite · pytest

## Summary

سامانهٔ API برای گردش کار Draft → PendingReview → ChangesRequested / Approved → Published با نقش‌های Author/Editor، بدون AI در این Feature.

## Technical Context

| مورد | مقدار |
|------|--------|
| Language | Python 3.11+ |
| API | FastAPI + Pydantic v2 |
| Storage | SQLite (فایل) |
| Testing | pytest، httpx ASGI |
| Auth | Opaque Bearer + hash (از فاز ۲ / گام ۱۱) |

## Constitution Check

- [x] بدون AI در Feature اول  
- [x] جهت وابستگی domain ← application ← infrastructure / api  
- [x] Rule در Application/Domain نه در Prompt  

## Project Structure

```text
src/blog_lab/
  domain/
  application/
  infrastructure/
  api/
tests/
specs/001-blog-post-management/
```

## فازهای اجرا (هم‌تراز کارگاه)

| فاز | معادل گام کارگاه | محتوا |
|-----|------------------|--------|
| ۱ | ۱۰ | اسکلت پکیج، تنظیمات، تست Startup |
| ۲ | ۱۱ | Auth، Permission، WriteSession، ProblemDetails |
| ۳ | ۱۲ | US1 Author + Post Aggregate |
| ۴ | ۱۳ | US2 Editor |
| ۵ | ۱۴ | US3 Public + Hardening |
| ۶ | ۱۵ | OpenAPI تطبیق، QuickStart واقعی، Validation |

## Rejected

- کپی ساختار csproj / MediatR از نمونهٔ استاد  
- EF Core / .NET — خارج از پشتهٔ این آزمایشگاه  
- شروع با LLM قبل از Feature اول  
