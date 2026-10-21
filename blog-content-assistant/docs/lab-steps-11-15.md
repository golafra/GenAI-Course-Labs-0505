<div dir="rtl" lang="fa">

# گزارش تکلیف: گام‌های ۱۱ تا ۱۵ کارگاه (پیاده‌سازی ساده‌شدهٔ Python)

> مسیر مفهومی Workshop-1 بدون کپی کد .NET استاد. پشته: FastAPI + SQLite + pytest.

## جواب کوتاه

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart RL
  S10["۱۰ اسکلت"] --> S11["۱۱ Auth"]
  S11 --> S12["۱۲ Author"]
  S12 --> S13["۱۳ Editor"]
  S13 --> S14["۱۴ Hardening"]
  S14 --> S15["۱۵ QuickStart / OpenAPI"]
```

**وضعیت:** گام‌های ۱۱–۱۵ در `blog-content-assistant` پیاده و با `pytest` (۲۲ تست) اثبات شده‌اند.

---

## نقشهٔ فاز ↔ کد

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart TB
  subgraph S11["گام ۱۱ — Auth"]
    A1["UserAccess سروری"]
    A2["Bearer → فقط هویت"]
    A3["Provision / Revoke"]
    A4["ProblemDetails"]
  end
  subgraph S12["گام ۱۲ — Author"]
    B1["Post Aggregate"]
    B2["CRUD + Submit"]
    B3["If-Match / ETag"]
  end
  subgraph S13["گام ۱۳ — Editor"]
    C1["RequestChanges"]
    C2["Approve غیرمالک"]
    C3["Publish"]
  end
  subgraph S14["گام ۱۴ — Hardening"]
    D1["Public فقط Published"]
    D2["ضد جعل نقش"]
    D3["stale version / revoke"]
  end
  subgraph S15["گام ۱۵ — تکمیل"]
    E1["OpenAPI"]
    E2["QuickStart واقعی"]
    E3["این گزارش"]
  end
  S11 --> S12 --> S13 --> S14 --> S15
```

| گام | چه ساخته شد؟ | مسیرهای اصلی |
|-----|--------------|--------------|
| ۱۱ | هویت opaque، Permission سروری، ops provision/revoke، خطای 401 | `application/security.py`, `api/deps.py`, `api/ops` |
| ۱۲ | Domain پست + Author API | `domain/posts.py`, `AuthorPostService`, `/api/author/*` |
| ۱۳ | صف ویراستار، برگشت، تأیید، انتشار | `EditorPostService`, `/api/editor/*` |
| ۱۴ | Public API، ماتریس امنیت ساده، Version | `/api/posts`, تست‌های hardening |
| ۱۵ | OpenAPI خودکار FastAPI، QuickStart، گزارش | `/openapi.json`, `quickstart.md` |

---

## جریان کسب‌وکار (بعد از پیاده‌سازی)

```mermaid
%%{init: {"flowchart": {"htmlLabels": true}, "themeVariables": {"fontFamily": "Tahoma, Vazirmatn, sans-serif"}}}%%
flowchart TB
  D["draft"] -->|submit| P["pending_review"]
  P -->|request_changes| C["changes_requested"]
  C -->|edit + submit| P
  P -->|approve غیرمالک| A["approved"]
  A -->|publish| Pub["published"]
  A -->|edit محتوا| D
  P -->|edit محتوا| D
```

قواعد کلیدی که در کد enforce شده‌اند (نه فقط Prompt):

- Header نقش/مالکیت نمی‌سازد  
- خودتأییدی ممنوع  
- Public فقط `published` و بدون فیلدهای مدیریتی  
- نبود `If-Match` → 428 ؛ نسخهٔ کهنه → 412  
- Publish تکراری اطلاعات انتشار نخست را عوض نمی‌کند  

---

## شواهد تست

```text
pytest  →  22 passed
```

پوشش تقریبی:

- Startup Fail-fast (گام ۱۰ ماندگار)
- Domain transitions
- Auth 401 / revoke / جعل نقش
- Author isolation + submit
- Editor مسیر کامل تا publish
- Public 404 برای غیرعمومی
- OpenAPI شامل مسیرهای اصلی

---

## ساده‌سازی نسبت به نمونهٔ استاد (عمدی)

| استاد (.NET) | این آزمایشگاه |
|--------------|----------------|
| چند پروژه csproj / EF / MediatR | یک پکیج Python لایه‌بندی‌شده |
| Migrationهای غنی | `init_schema` صریح در provision/تست |
| ماتریس امنیتی بسیار گسترده | سناریوهای اصلی اثبات‌شده |
| ETag UUID با قواعد کامل ASP.NET | Version UUID + If-Match |

هدف تکلیف: **تکمیل مسیر ۱۱–۱۵ و اثبات رفتار**، نه parity خط‌به‌خط.

---

## قدم بعد (خارج از این تکلیف)

- Feature دوم AI / Content Review (گام ۱۶+)
- یا Homework Session-05 (Tool Calling / MCP) روی همین Blog Service

</div>
