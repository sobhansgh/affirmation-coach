import flet as ft
from services.streak_service import get_user_progress
from database.database import SessionLocal

class DashboardView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        db = SessionLocal()
        try:
            progress = get_user_progress(db)
            level = progress.current_level
            xp = progress.current_xp
            streak = progress.current_streak
            best_streak = progress.best_streak
        finally:
            db.close()

        stats_row = ft.Row(
            controls=[
                self._create_stat_card("سطح فعلی", str(level), ft.icons.STAR, ft.colors.BLUE_400),
                self._create_stat_card("امتیاز (XP)", f"{xp:,}", ft.icons.BOLT, ft.colors.AMBER_400),
                self._create_stat_card("استریک", f"{streak} روز", ft.icons.LOCAL_FIRE_DEPARTMENT, ft.colors.GREEN_400),
                self._create_stat_card("بهترین استریک", f"{best_streak} روز", ft.icons.EMOJI_EVENTS, ft.colors.PURPLE_400),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return ft.Column(
            controls=[
                ft.Text("خوش برگشتی! 🌟", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("امروز یک روز عالی برای رشد و پیشرفت است.", size=16, color=ft.colors.OUTLINE),
                ft.Container(height=30),
                stats_row,
                ft.Container(height=40),
                # فضای آماده برای اضافه شدن Heatmap در مراحل بعدی
                ft.Container(
                    content=ft.Column([
                        ft.Text("وضعیت تمرین‌های امروز", size=20, weight=ft.FontWeight.W_600),
                        ft.ProgressBar(value=0.4, color=ft.colors.GREEN_400, bgcolor=ft.colors.SURFACE_VARIANT, height=10),
                        ft.Text("۲ از ۵ تمرین انجام شده", size=12, color=ft.colors.OUTLINE)
                    ]),
                    padding=20,
                    border_radius=15,
                    bgcolor=ft.colors.SURFACE_VARIANT
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def _create_stat_card(self, title, value, icon, color):
        return ft.Container(
            width=200,
            padding=20,
            border_radius=15,
            bgcolor=ft.colors.SURFACE_VARIANT,
            content=ft.Column(
                controls=[
                    ft.Row([ft.Icon(icon, color=color, size=30), ft.Text(title, size=16, color=ft.colors.OUTLINE)], alignment=ft.MainAxisAlignment.START),
                    ft.Text(value, size=32, weight=ft.FontWeight.BOLD, color=color),
                ],
            )
        )