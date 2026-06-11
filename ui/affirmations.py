import flet as ft
from database.database import SessionLocal
from services.affirmation_service import get_active_affirmations, add_affirmation


class AffirmationsView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        self.list_view = ft.ListView(expand=True, spacing=10)
        self.load_affirmations()

        # فرم پاپ‌آپ برای افزودن عبارت جدید
        self.new_text_field = ft.TextField(label="متن عبارت تأکیدی", multiline=True, rtl=True)
        self.category_dropdown = ft.Dropdown(
            label="دسته‌بندی",
            options=[
                ft.dropdown.Option("اعتماد به نفس"),
                ft.dropdown.Option("مالی"),
                ft.dropdown.Option("سلامتی"),
                ft.dropdown.Option("روابط"),
                ft.dropdown.Option("کسب و کار"),
            ],
            value="اعتماد به نفس"
        )

        self.add_dialog = ft.AlertDialog(
            title=ft.Text("افزودن عبارت جدید"),
            content=ft.Column([self.new_text_field, self.category_dropdown], tight=True),
            actions=[
                ft.TextButton("ذخیره", on_click=self.save_affirmation, style=ft.ButtonStyle(color=ft.colors.GREEN)),
                ft.TextButton("انصراف", on_click=lambda e: self.close_dialog()),
            ],
        )

        return ft.Stack(
            controls=[
                ft.Column([
                    ft.Text("مدیریت عبارات تأکیدی", size=28, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    self.list_view
                ], expand=True),

                # دکمه شناور در پایین صفحه
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    bgcolor=ft.colors.BLUE_400,
                    on_click=self.open_dialog,
                    bottom=20,
                    right=20,  # در حالت RTL در سمت چپ نمایش داده می‌شود
                )
            ],
            expand=True
        )

    def load_affirmations(self):
        self.list_view.controls.clear()
        db = SessionLocal()
        try:
            affirmations = get_active_affirmations(db)
            if not affirmations:
                self.list_view.controls.append(ft.Text("هنوز عبارتی ثبت نکرده‌اید.", color=ft.colors.OUTLINE))

            for aff in affirmations:
                self.list_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.FORMAT_QUOTE, color=ft.colors.BLUE_400),
                        title=ft.Text(aff.text, size=16),
                        subtitle=ft.Text(aff.category, size=12, color=ft.colors.OUTLINE),
                        trailing=ft.Switch(value=aff.is_active, active_color=ft.colors.GREEN_400),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
        finally:
            db.close()

    def open_dialog(self, e):
        self.page.dialog = self.add_dialog
        self.add_dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.add_dialog.open = False
        self.page.update()

    def save_affirmation(self, e):
        text = self.new_text_field.value
        category = self.category_dropdown.value
        if text and category:
            db = SessionLocal()
            try:
                add_affirmation(db, text, category)
            finally:
                db.close()
            self.new_text_field.value = ""
            self.close_dialog()
            self.load_affirmations()
            self.page.update()