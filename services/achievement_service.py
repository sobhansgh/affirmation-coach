from sqlalchemy.orm import Session
from datetime import datetime
from database.models import Achievement, UserProgress, DailyLog

# لیست دستاوردهای پیش‌فرض بر اساس مستندات پروژه
DEFAULT_ACHIEVEMENTS = [
    {"title": "اولین قدم", "description": "اولین فعالیت خود را ثبت کنید."},
    {"title": "شروع استمرار", "description": "سه روز متوالی استریک داشته باشید."},
    {"title": "هفته طلایی", "description": "هفت روز متوالی استریک داشته باشید."},
    {"title": "قهرمان ماه", "description": "سی روز متوالی استریک داشته باشید."},
    {"title": "متمرکز", "description": "صد فعالیت موفق ثبت کنید."},
    {"title": "سطح ۵", "description": "به سطح ۵ برسید."},
    {"title": "استاد ذهن (سطح ۱۰)", "description": "به سطح ۱۰ برسید."}
]


def initialize_achievements(db: Session):
    """ایجاد دستاوردهای اولیه در دیتابیس در صورت عدم وجود"""
    existing_count = db.query(Achievement).count()
    if existing_count == 0:
        for ach in DEFAULT_ACHIEVEMENTS:
            new_ach = Achievement(title=ach["title"], description=ach["description"])
            db.add(new_ach)
        db.commit()


def unlock_achievement(db: Session, title: str):
    """باز کردن یک دستاورد خاص"""
    achievement = db.query(Achievement).filter(Achievement.title == title).first()
    if achievement and not achievement.is_unlocked:
        achievement.is_unlocked = True
        achievement.unlocked_at = datetime.utcnow()
        db.commit()
        return True  # نشان‌دهنده این است که دستاورد به تازگی باز شده است
    return False


def check_all_achievements(db: Session):
    """
    بررسی جامع برای باز کردن دستاوردها بر اساس وضعیت فعلی کاربر
    این تابع باید بعد از هر تغییر مهم در استریک یا لول فراخوانی شود
    """
    progress = db.query(UserProgress).first()
    if not progress:
        return

    # بررسی سطح‌ها
    if progress.current_level >= 5:
        unlock_achievement(db, "سطح ۵")
    if progress.current_level >= 10:
        unlock_achievement(db, "استاد ذهن (سطح ۱۰)")

    # بررسی استریک‌ها
    if progress.current_streak >= 3:
        unlock_achievement(db, "شروع استمرار")
    if progress.current_streak >= 7:
        unlock_achievement(db, "هفته طلایی")
    if progress.current_streak >= 30:
        unlock_achievement(db, "قهرمان ماه")