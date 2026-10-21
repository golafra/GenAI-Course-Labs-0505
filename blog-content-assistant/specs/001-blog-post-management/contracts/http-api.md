# قرارداد HTTP (پیش‌نویس — تکمیل در فازهای ۲–۶)

Base: `/api`

## عمومی (US3)

- `GET /api/posts` — فقط published  
- `GET /api/posts/{id}` — فقط published؛ ناموجود/خصوصی → 404 یکسان  

## نویسنده (US1) — نیازمند Auth

- `POST /api/author/posts`  
- `GET /api/author/posts`  
- `GET /api/author/posts/{id}`  
- `PUT /api/author/posts/{id}` + `If-Match`  
- `DELETE /api/author/posts/{id}` + `If-Match`  
- `POST /api/author/posts/{id}/submit` + `If-Match`  

## ویراستار (US2) — نیازمند Auth

- `GET /api/editor/queue`  
- `GET /api/editor/posts/{id}`  
- `POST /api/editor/posts/{id}/request-changes`  
- `POST /api/editor/posts/{id}/approve`  
- `POST /api/editor/posts/{id}/publish`  

## خطا

Problem Details با `code` پایدار؛ بدون افشای Secret.  
نبود If-Match در mutation → 428.

## وضعیت فاز ۱

هنوز فقط `GET /health` برای اثبات Host زنده است؛ مسیرهای بالا از گام ۱۱ به بعد اضافه می‌شوند.
