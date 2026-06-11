from sqlalchemy.orm import Session
from database.models import UserProgress

# سیستم محاسبه سطح
LEVEL_THRESHOLDS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5000,
    9: 7500,
    10: 10000
}


def get_user_progress(db: Session) -> UserProgress:
    """دریافت یا ایجاد پروفایل پیشرفت کاربر (Singleton در دیتابیس)"""
    progress = db.query(UserProgress).first()
    if not progress:
        progress = UserProgress()
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress


def calculate_level(current_xp: int) -> int:
    """محاسبه سطح فعلی کاربر بر اساس XP"""
    current_level = 1
    for level, required_xp in sorted(LEVEL_THRESHOLDS.items()):
        if current_xp >= required_xp:
            current_level = level
        else:
            break
    return current_level


def add_xp(db: Session, amount: int):
    """افزودن XP به کاربر و بروزرسانی سطح در صورت نیاز"""
    progress = get_user_progress(db)
    progress.current_xp += amount

    # بررسی و بروزرسانی لول
    new_level = calculate_level(progress.current_xp)
    if new_level > progress.current_level:
        progress.current_level = new_level
        # در فازهای بعدی می‌توان اینجا Achievement یا Notification صادر کرد

    db.commit()
    db.refresh(progress)
    return progress


def update_streak(db: Session, all_daily_reminders_completed: bool):
    """
    بروزرسانی وضعیت استمرار روزانه (Streak)
    اگر کاربر تمام یادآوری‌ها را انجام داده باشد یک روز اضافه می‌شود
    در غیر این صورت استریک ریست می‌شود.
    """
    progress = get_user_progress(db)

    if all_daily_reminders_completed:
        progress.current_streak += 1
        # ثبت بهترین رکورد کاربر
        if progress.current_streak > progress.best_streak:
            progress.best_streak = progress.current_streak
    else:
        progress.current_streak = 0

    db.commit()
    db.refresh(progress)
    return progress