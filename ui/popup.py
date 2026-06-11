import flet as ft
from services.sound_service import play_sound


# بعداً سرویس‌های ثبت XP و لاگ در دیتابیس را به اینجا متصل می‌کنیم

def show_affirmation_popup(page: ft.Page, affirmation_text: str):
    """نمایش پاپ‌آپ عبارت تأکیدی"""

    # پخش صدای آرامش‌بخش
    play_sound("zen.wav")

    def handle_done(e):
        # منطق ثبت موفقیت و دریافت XP
        print("انجام شد!")
        dialog.open = False
        page.update()

    def handle_snooze(e):
        # منطق تعویق (مثلاً 15 دقیقه بعد)
        print("بعداً یادآوری کن!")
        dialog.open = False
        page.update()

    def handle_failed(e):
        # منطق ثبت شکست و ریست استریک
        print("انجام ندادم!")
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("زمان تمرین ذهنی", text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            padding=20,
            content=ft.Text(
                affirmation_text,
                size=22,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            )
        ),
        actions=[
            ft.TextButton("انجام دادم ✓", on_click=handle_done, style=ft.ButtonStyle(color=ft.colors.GREEN)),
            ft.TextButton("بعداً", on_click=handle_snooze),
            ft.TextButton("انجام ندادم ✗", on_click=handle_failed, style=ft.ButtonStyle(color=ft.colors.RED)),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=15)
    )

    page.dialog = dialog
    dialog.open = True
    page.update()