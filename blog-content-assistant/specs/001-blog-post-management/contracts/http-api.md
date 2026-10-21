# قرارداد HTTP — وضعیت پس از گام ۱۵

Base: `/api`  
Auth: `Authorization: Bearer <token>`  
Mutationهای پس از ایجاد: هدر `If-Match` با مقدار version (ETag بدون یا با کوتیشن)

## Ops (محلی)

| Method | Path | توضیح |
|--------|------|--------|
| POST | `/api/ops/provision` | ساخت کاربر + token یک‌بارمصرف در پاسخ |
| POST | `/api/ops/revoke-token/{userId}` | بی‌اعتبار کردن credential |
| POST | `/api/ops/revoke-permissions/{userId}` | صفر کردن Permissionها |

## Author

| Method | Path |
|--------|------|
| POST | `/api/author/posts` |
| GET | `/api/author/posts` |
| GET | `/api/author/posts/{id}` |
| PUT | `/api/author/posts/{id}` |
| DELETE | `/api/author/posts/{id}` |
| POST | `/api/author/posts/{id}/submit` |

## Editor

| Method | Path |
|--------|------|
| GET | `/api/editor/queue` |
| GET | `/api/editor/posts/{id}` |
| POST | `/api/editor/posts/{id}/request-changes` |
| POST | `/api/editor/posts/{id}/approve` |
| POST | `/api/editor/posts/{id}/publish` |

## Public

| Method | Path | توضیح |
|--------|------|--------|
| GET | `/api/posts` | فقط published |
| GET | `/api/posts/{id}` | فقط published؛ وگرنه 404 یکسان |

## کدهای خطای پایدار (نمونه)

`unauthorized` · `forbidden` · `not_found` · `validation_error` · `conflict` · `precondition_required` · `stale_version`
