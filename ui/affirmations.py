import flet as ft
from database.database import SessionLocal
from services.affirmation_service import add_affirmation, get_active_affirmations


class AffirmationsView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        # فیلدهای ورودی
        self.text_input = ft.TextField(label="عبارت تأکیدی جدید خود را بنویسید...", expand=True)

        self.category_dropdown = ft.Dropdown(
            label="دسته‌بندی",
            options=[
                ft.dropdown.Option("اعتماد به نفس"),
                ft.dropdown.Option("مالی"),
                ft.dropdown.Option("سلامتی"),
                ft.dropdown.Option("روابط"),
                ft.dropdown.Option("کسب و کار"),
                ft.dropdown.Option("شخصی"),
            ],
            width=180
        )

        add_button = ft.ElevatedButton(
            "افزودن",
            on_click=self.add_new_affirmation,
            icon=ft.icons.ADD,
            style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE)
        )

        # فضایی برای نمایش لیست عبارات
        self.affirmations_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

        # بارگذاری اولیه لیست
        self.load_affirmations()

        return ft.Container(
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("مدیریت عبارات تأکیدی", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("عباراتی که در اینجا اضافه می‌کنید در زمان‌بندی‌های مشخص به شما یادآوری می‌شوند.", color=ft.colors.OUTLINE),
                    ft.Container(height=10),

                    # فرم افزودن عبارت
                    ft.Row(
                        controls=[self.text_input, self.category_dropdown, add_button],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=30, color=ft.colors.SURFACE_VARIANT),

                    # لیست عبارات
                    self.affirmations_list
                ],
                expand=True
            )
        )

    def load_affirmations(self):
        """خواندن عبارات از دیتابیس و رندر کردن آن‌ها در لیست"""
        self.affirmations_list.controls.clear()
        db = SessionLocal()
        try:
            affirmations = get_active_affirmations(db)
            for aff in affirmations:
                # طراحی هر ردیف از عبارات به صورت یک کارت کوچک (ListTile)
                item = ft.Card(
                    elevation=1,
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.AUTO_AWESOME, color=ft.colors.AMBER_400),
                        title=ft.Text(aff.text, size=16),
                        subtitle=ft.Text(aff.category, color=ft.colors.BLUE_200, size=12),
                        trailing=ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            icon_color=ft.colors.RED_400,
                            tooltip="حذف موقت"
                        )
                    )
                )
                self.affirmations_list.controls.append(item)
        finally:
            db.close()

        # بروزرسانی صفحه برای نمایش تغییرات
        if self.page:
            self.page.update()

    def add_new_affirmation(self, e):
        """منطق دکمه افزودن"""
        if not self.text_input.value or not self.category_dropdown.value:
            # اگر فیلدها خالی بود کاری نکن
            return

        db = SessionLocal()
        try:
            add_affirmation(db, self.text_input.value, self.category_dropdown.value)

            # پاک کردن فیلدها بعد از ثبت موفق
            self.text_input.value = ""
            self.category_dropdown.value = None

            # رفرش کردن لیست
            self.load_affirmations()
        finally:
            db.close()