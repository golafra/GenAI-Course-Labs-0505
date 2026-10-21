<div dir="rtl" lang="fa">

# Spec تعریف شده؛ آیا باید برای Plan پرامپت بنویسیم؟

> یادداشت شخصی از سؤال کلاسی دوره — هم‌راستا با مسیر SDD و Promptهای زندهٔ Session-01.

---

## جواب یک‌خطی

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart RL
  A["Spec<br/>چه چیزی؟"] --> B["Plan<br/>چگونه؟"]
  B --> C{"Constitution + قالب Plan<br/>از قبل کامل است؟"}
  C -->|بله| D["پرامپت کوتاه کافی است<br/>Plan بساز؛ کد نزن"]
  C -->|خیر| E["قیود فنی را صریح<br/>در پرامپت Plan بنویس"]
```

**خلاصه:** Spec به‌تنهایی «چگونه پلن کن» را کامل نمی‌کند. نوشتن متا-پرامپت طولانی اجباری نیست؛ **دادن مرزهای فنی (یا داشتنشان در Constitution / قالب)** ضروری است — وگرنه مدل فرضیات معماری را مثل Vibe Coding داخل Plan می‌گذارد.

---

## ۱) نقش هر سند

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart TB
  subgraph WHAT["لایهٔ محصول — WHAT"]
    direction TB
    S["Spec<br/>رفتار · Acceptance · Scope · Edge"]
    CL["Clarify<br/>فقط ابهام پرهزینهٔ رفتاری"]
  end

  subgraph HOW["لایهٔ فنی — HOW"]
    direction TB
    P["Plan<br/>معماری · لایه‌ها · ذخیره · تست · ساختار"]
    T["Tasks<br/>تکه‌های کوچک + وابستگی"]
  end

  subgraph DO["اجرا"]
    direction TB
    A["Analyze<br/>شکاف قبل از کد"]
    I["Implement + Test"]
  end

  S --> CL --> P --> T --> A --> I
```

| سند | سؤال | در پرامپت چه بگویی؟ |
|-----|------|---------------------|
| Spec | سیستم *چه* کند؟ | User Story، Acceptance، Edge — **نه** کلاس و فریم‌ورک |
| Plan | *چگونه* بسازیم؟ | زبان، معماری، جهت وابستگی، تست — **هنوز کد نزن** |
| Tasks | *به چه ترتیب؟* | کارهای کوچک متصل به Requirement |

---

## ۲) تصمیم: پرامپت Plan بنویسم یا نه؟

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart TB
  START(["Spec تأیید + Clarify تمام"]) --> Q1{"Constitution پروژه<br/>قوانین فنی ثابت دارد؟"}
  Q1 -->|نه| WRITE["پرامپت Plan بنویس<br/>و قیود را قفل کن"]
  Q1 -->|بله| Q2{"چند معماری معقول هست<br/>و یکی را می‌خواهی؟"}
  Q2 -->|بله| WRITE
  Q2 -->|نه| Q3{"گزینه‌هایی باید<br/>صریح Reject شوند؟"}
  Q3 -->|بله| WRITE
  Q3 -->|نه| SHORT["پرامپت کوتاه + قالب Plan<br/>کافی است"]

  WRITE --> OUT["خروجی: plan.md<br/>و در صورت نیاز research / data-model / contracts"]
  SHORT --> OUT
  OUT --> NEXT["بعد: Tasks ← Analyze ← Implement"]
```

### مثال دوره (Prompt زندهٔ Session-01)

بعد از Spec، استاد **عمداً** قیود Plan را می‌نویسد: Onion، CQRS/MediatR، جهت وابستگی، روش تست — و «هنوز کد نزن».

منبع: `Session-01/Prompts/LIVE-PROMPTS-FA.md` (مرحلهٔ ۳ — معماری).

---

## ۳) اگر پرامپت Plan می‌نویسیم، چه چیزهایی داخلش باشد؟

```mermaid
%%{init: {"themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
mindmap
  root((پرامپت Plan))
    لنگر
      Spec تأییدشده
      Constitution
      هنوز کد نزن
    زمینه فنی
      زبان و نسخه
      فریم‌ورک
      Storage و Scope
    معماری
      لایه‌ها
      جهت وابستگی
      محل Business Rule
    قرارداد
      Data Model
      API یا Toolها
      شکل Errorها
    کیفیت
      استراتژی Test
      TDD در صورت نیاز
    ساختار
      درخت پوشه
    کنترل
      گزینه‌های Reject شده
      محدودیت غیرعملکردی
```

### چک‌لیست سریع (کپی در چت)

- [ ] ارجاع به Spec تأییدشده + Constitution  
- [ ] «هنوز کد نزن»  
- [ ] زبان / فریم‌ورک / نوع پروژه  
- [ ] Storage و آنچه خارج از Scope است  
- [ ] لایه‌ها و جهت وابستگی  
- [ ] کجا Rule enforce می‌شود (Application، نه فقط Prompt)  
- [ ] استراتژی Test  
- [ ] ساختار پوشه‌ها  
- [ ] گزینه‌های Reject شده + دلیل کوتاه  
- [ ] خروجی مورد انتظار: `plan.md` (و در صورت نیاز data-model / contracts)

### چه چیزهایی داخل پرامپت Plan نباشد

| نگذار | چرا |
|--------|-----|
| کد خط‌به‌خط | آن Implement است |
| تکرار تمام Acceptance | ارجاع به Spec کافی است |
| «هر طور قشنگ شد معماری کن» | دوباره Vibe در لباس Plan |
| ابهام محصول (مثلاً ایمیل یکتا؟) | آن Clarify است، نه Plan |

---

## ۴) مقایسه با Vibe Coding

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart TB
  subgraph VIBE["Vibe Coding"]
    direction RL
    VP["Prompt کوتاه"] --> VC["کد + فرضیات پنهان"]
    VC --> VFIX["Patch پشت Patch"]
  end

  subgraph SDD["Spec-Driven Development"]
    direction RL
    SP["Spec"] --> PL["Plan با مرز"]
    PL --> TK["Tasks"]
    TK --> IM["Implement با شواهد"]
  end
```

در Vibe، Agent هم‌زمان تحلیلگر محصول، معمار و برنامه‌نویس است.  
در SDD قبل از پیاده‌سازی، **مرجع حقیقت (Spec)**، **مرز تصمیم (Plan / Constitution)** و **تعریف پایان (Acceptance / Test)** بسته می‌شود.

---

## ۵) جملهٔ آماده برای پاسخ کلاسی

> Spec مرجع «چه چیزی» است؛ Plan مرجع «چگونه». نوشتن پرامپت طولانیِ «چگونه فکر کن» اجباری نیست اگر Constitution و قالب Plan موجود باشند؛ اما دادن قیود فنی، مرز لایه‌ها، تست و گزینه‌های Reject شده برای Plan ضروری است — وگرنه مدل فرضیات معماری را مثل Vibe Coding داخل Plan می‌گذارد. بعد Plan را به Tasks می‌شکنیم و قبل از کد Analyze می‌کنیم.

---

## ۶) مسیر کامل SDD (یادآوری)

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart RL
  C["Constitution"] --> S["Specify"]
  S --> CL["Clarify"]
  CL --> P["Plan"]
  P --> T["Tasks"]
  T --> A["Analyze"]
  A --> I["Implement"]
  I --> TE["Test"]
```

---

## ارجاعات

- Promptهای زنده: مخزن دوره ← `Session-01/Prompts/LIVE-PROMPTS-FA.md`
- راهنمای Spec Kit: مخزن دوره ← `Session-02/Documets/SpecKit-Workshop-Guide-fa.md`
- نمونهٔ Plan: مخزن دوره ← `Session-01/Samples/SDD/specs/001-user-profile/plan.md`

</div>
