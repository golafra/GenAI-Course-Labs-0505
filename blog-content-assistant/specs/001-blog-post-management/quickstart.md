# QuickStart — اجرا و Demo واقعی (گام ۱۵)

دستورهای زیر روی همین Repository اجرا و با تست‌ها هم‌راستا شده‌اند.

## پیش‌نیاز

- Python 3.11+ (`py -3`)

## نصب و تست

```powershell
cd blog-content-assistant
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

انتظار: همهٔ تست‌ها سبز (حدود ۲۲).

## اجرای Host

```powershell
$env:BLOG_LAB_DATABASE_PATH = "./data/blog_lab.db"
uvicorn blog_lab.api.main:create_app --factory --app-dir src --reload
```

- Health: `GET http://127.0.0.1:8000/health`
- OpenAPI: `GET http://127.0.0.1:8000/openapi.json`
- Docs UI: `http://127.0.0.1:8000/docs`

## Demo دستی (حداقلی)

```powershell
# 1) Author
$author = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/ops/provision -ContentType application/json -Body '{"display_name":"A","can_write":true}'

# 2) Editor
$editor = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/ops/provision -ContentType application/json -Body '{"display_name":"E","can_review":true,"can_publish":true}'

$ah = @{ Authorization = "Bearer $($author.token)" }
$eh = @{ Authorization = "Bearer $($editor.token)" }

# 3) Create + Submit
$post = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/author/posts -Headers $ah -ContentType application/json -Body '{"title":"سلام","body":"متن"}'
$ah2 = $ah + @{ "If-Match" = $post.version }
$pending = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/author/posts/$($post.id)/submit" -Headers $ah2

# 4) Approve + Publish
$eh2 = $eh + @{ "If-Match" = $pending.version }
$approved = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/editor/posts/$($post.id)/approve" -Headers $eh2
$eh3 = $eh + @{ "If-Match" = $approved.version }
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/editor/posts/$($post.id)/publish" -Headers $eh3

# 5) Public
Invoke-RestMethod http://127.0.0.1:8000/api/posts
```

Token فقط یک‌بار در پاسخ provision برمی‌گردد؛ در مخزن ذخیره نکنید.

## نکتهٔ Startup

راه‌اندازی عادی Host، Schema یا کاربر نمی‌سازد. اولین `POST /api/ops/provision` (یا `init_schema` در تست) Schema را ایجاد می‌کند.
