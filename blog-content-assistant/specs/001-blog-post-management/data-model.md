# Data Model (هدف — پیاده‌سازی تدریجی)

## Post

| فیلد | توضیح |
|------|--------|
| id | تولید سرور |
| owner_id | ثابت از هویت ایجادکننده |
| title / body | غیرخالی، غیر whitespace |
| status | draft · pending_review · changes_requested · approved · published |
| content_revision | از ۱؛ فقط با تغییر واقعی title/body |
| version | توکن رقابت |
| is_deleted | حذف منطقی |
| current_review_id | آخرین تصمیم مرتبط (nullable) |
| publication | فقط در published |

## ReviewDecision

Immutable؛ Approve یا RequestChanges؛ Snapshot عنوان/متن؛ reviewer ≠ owner برای Approve؛ reason برای RequestChanges الزامی.

## UserAccess (سروری)

`user_id`, `can_write`, `can_review`, `can_publish`, `is_active`

## Credential

Token خام فقط یک‌بار تحویل؛ در DB فقط hash + expiry + revoked.
