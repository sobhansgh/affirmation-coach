import pygame
import os

# راه‌اندازی اولیه ماژول صدای پای‌گیم
pygame.mixer.init()


def play_sound(sound_filename: str):
    """
    پخش یک فایل صوتی از پوشه assets/sounds/
    مثال ورودی: "bell.wav"
    """
    sound_path = os.path.join("assets", "sounds", sound_filename)

    # بررسی وجود فایل برای جلوگیری از کرش کردن برنامه
    if os.path.exists(sound_path):
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
        except Exception as e:
            print(f"خطا در پخش صدا: {e}")
    else:
        print(f"اخطار: فایل صوتی یافت نشد -> {sound_path}")