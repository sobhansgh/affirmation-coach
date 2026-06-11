import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# اطمینان از وجود پوشه data برای ذخیره فایل دیتابیس
os.makedirs("data", exist_ok=True)

# آدرس دیتابیس SQLite
DATABASE_URL = "sqlite:///data/app.db"

# ایجاد Engine دیتابیس
# آرگومان check_same_thread=False برای برنامه‌های چندنخی مانند Flet ضروری است
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# ایجاد کلاس ساخت Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# کلاس پایه برای مدل‌ها
Base = declarative_base()

def get_db():
    """یک تابع کمکی برای مدیریت باز و بسته شدن Session دیتابیس"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()