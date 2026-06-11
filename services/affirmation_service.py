from sqlalchemy.orm import Session
from database.models import Affirmation

# مخزن تولید عبارات تأکیدی پیشنهادی بر اساس دسته‌بندی
PREDEFINED_AFFIRMATIONS = {
    "اعتماد به نفس": [
        "من هر روز اعتماد به نفس بیشتری دارم.",
        "من به توانایی‌های خود اعتماد کامل دارم.",
        "با آرامش و اطمینان تصمیم می‌گیرم."
    ],
    "مالی": [
        "من هر روز فرصت‌های مالی بیشتری ایجاد می‌کنم.",
        "مشتریان مناسب به سمت من جذب می‌شوند.",
        "من ارزش خلق می‌کنم و ثروت به سوی من جریان دارد."
    ],
    "سلامتی": [
        "بدن من هر روز سالم‌تر و قوی‌تر می‌شود.",
        "من به سلامتی جسم و روحم اهمیت می‌دهم.",
        "انرژی مثبت در تمام سلول‌های بدن من جریان دارد."
    ],
    "روابط": [
        "من روابط سالم و سازنده‌ای با اطرافیانم دارم.",
        "من عشق و احترام را در روابطم جذب می‌کنم."
    ],
    "کسب و کار": [
        "کسب و کار من هر روز رشد می‌کند و گسترش می‌یابد.",
        "من توانایی حل مشکلات مشتریان را به بهترین شکل دارم."
    ],
    "شخصی": [
        "من هر روز نسخه بهتری از خودم می‌شوم.",
        "من به اهداف شخصی‌ام متعهد هستم."
    ]
}

def add_affirmation(db: Session, text: str, category: str) -> Affirmation:
    """افزودن یک عبارت تأکیدی جدید به دیتابیس"""
    new_affirmation = Affirmation(text=text, category=category, is_active=True)
    db.add(new_affirmation)
    db.commit()
    db.refresh(new_affirmation)
    return new_affirmation

def get_active_affirmations(db: Session):
    """دریافت تمام عبارات تأکیدی فعال کاربر"""
    return db.query(Affirmation).filter(Affirmation.is_active == True).all()

def toggle_affirmation_status(db: Session, affirmation_id: int):
    """فعال یا غیرفعال کردن یک عبارت تأکیدی"""
    affirmation = db.query(Affirmation).filter(Affirmation.id == affirmation_id).first()
    if affirmation:
        affirmation.is_active = not affirmation.is_active
        db.commit()
    return affirmation

def generate_suggestions(category: str) -> list:
    """تولید عبارات پیشنهادی بر اساس موضوع انتخابی"""
    return PREDEFINED_AFFIRMATIONS.get(category, [])