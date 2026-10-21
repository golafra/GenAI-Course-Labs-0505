# GenAI-Course-Labs-0505

مخزن شخصی **تمرین‌ها و تکالیف عملی** دورهٔ [از Prompt تا Production؛ مهندسی نرم‌افزار در عصر هوش مصنوعی](https://nikamooz.com/classes/prompt-to-production-software-engineering-in-the-age-of-artificial-intelligence/).

این ریپو **محتوای رسمی دوره نیست**؛ پیاده‌سازی‌ها، یادداشت‌ها و آزمایش‌های من روی تکالیف است. اسلایدها و نمونه‌کدهای استاد در مخزن upstream دوره منتشر می‌شوند.

## منبع دوره (Upstream)

- مخزن عمومی دوره: [oroumand/SoftwareEngineering-GenAI-0505](https://github.com/oroumand/SoftwareEngineering-GenAI-0505)
- مدرس: **علیرضا ارومند**

## هدف این مخزن

در طول دوره، تکالیف را **خودم** با رویکرد **توسعهٔ مبتنی بر مشخصات (SDD)** پیاده‌سازی، تست و در صورت نیاز گسترش می‌دهم. شمارهٔ جلسه در ساختار پوشه‌ها مبنا نیست؛ هر پوشه نام **موضوع تکلیف** دارد.

اصول کار با هوش مصنوعی در توسعه (Spec، Context، اعتبارسنجی خروجی، مرز Application و مدل، Tool Calling و …) بین تکالیف مشترک است؛ **پشتهٔ اصلی پیاده‌سازی: Python**.

## تکالیف

| پوشه | توضیح | وضعیت |
|------|--------|--------|
| `blog-content-assistant` | آزمایشگاه Python مسیر Workshop-1 (معادل گام ۱–۱۵) | گام ۱–۱۵ انجام شد |

تکالیف بعدی با نام معنادار به همین جدول و ساختار اضافه می‌شوند.

## سوالات و تحقیقات کلاسی

پاسخ‌ها و پژوهش‌های مربوط به پرسش‌های استاد (نه کد تکلیف عملی).

| فایل | موضوع |
|------|--------|
| [class-research/spec-vs-plan-prompt.md](class-research/spec-vs-plan-prompt.md) | بعد از Spec آیا پرامپت Plan لازم است؟ (فلوچارت + چک‌لیست) |
| [class-research/human-in-agentic-sdlc.md](class-research/human-in-agentic-sdlc.md) | چرخهٔ استاندارد حضور انسان در تولید نرم‌افزار با Agentها |

## رویکرد کلی

```text
Constitution → Specify → Clarify → Plan → Tasks → Implement → Test
```

قبل از کدنویسی، تصمیم‌های مهم در Spec/مستندات همان تکلیف ثبت می‌شود. خروجی مدل بدون بررسی و تست در این مخزن «تحویلی» محسوب نمی‌شود.

## پیش‌نیازهای محلی (خلاصه)

- Python 3.11+
- Git

جزئیات هر تکلیف در README همان پوشه آمده است.

## مجوز و استفاده

کد این مخزن کار شخصی من روی تکالیف دوره است. استفادهٔ دیگران آزاد است؛ لطفاً منبع دوره و مخزن upstream را ذکر کنید. محتوای رسمی دوره تحت مالکیت ارائه‌دهندهٔ دوره است.

---

**Software Engineering in the Age of AI — personal lab work (0505 cohort)**
