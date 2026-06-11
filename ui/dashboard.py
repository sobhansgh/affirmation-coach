import flet as ft
from services.streak_service import get_user_progress
from database.database import SessionLocal

class DashboardView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        # دریافت اطلاعات کاربر از دیتابیس
        db = SessionLocal()
        try:
            progress = get_user_progress(db)
            level = progress.current_level
            xp = progress.current_xp
            streak = progress.current_streak
            best_streak = progress.best_streak
        finally:
            db.close()

        # فرمت‌بندی اعداد برای خوانایی بهتر (جداسازی سه‌رقمی)
        formatted_xp = f"{xp:,}"

        # کارت‌های آماری
        stats_row = ft.Row(
            controls=[
                self._create_stat_card("سطح فعلی", str(level), ft.colors.BLUE_400),
                self._create_stat_card("امتیاز (XP)", formatted_xp, ft.colors.AMBER_400),
                self._create_stat_card("استریک (روز)", str(streak), ft.colors.GREEN_400),
                self._create_stat_card("بهترین استریک", str(best_streak), ft.colors.PURPLE_400),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        return ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Text("خلاصه وضعیت شما", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                stats_row,
                ft.Divider(height=40, color=ft.colors.ON_SURFACE_VARIANT),
                # در اینجا بعداً بخش لیست عبارات و هیت‌مپ اضافه می‌شود
                ft.Text("عبارات تأکیدی فعال", size=20, weight=ft.FontWeight.W_600),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _create_stat_card(self, title, value, color):
        """متد کمکی برای ساخت کارت‌های آماری زیبا"""
        return ft.Card(
            elevation=4,
            content=ft.Container(
                padding=20,
                width=150,
                content=ft.Column(
                    controls=[
                        ft.Text(title, size=14, color=ft.colors.OUTLINE),
                        ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        )