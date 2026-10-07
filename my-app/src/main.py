import flet as ft
from datetime import datetime


class Note:
    def __init__(self, text, category="общее"):
        self.text = text
        self.category = category
        self.important = False
        self.created = datetime.now().strftime("%d.%m %H:%M")
        self.views = 0

    def show(self):
        self.views += 1
        return f"[{self.category}] {self.text} — {self.created} (открыто {self.views})"


class NoteCheck(ft.Checkbox):
    def __init__(self, note, toggle):
        super().__init__()
        self.note = note
        self.label = note.show()
        self.on_change = lambda e: toggle(note, e.control.value)


def main(page: ft.Page):
    page.title = "Заметки"

    notes = []
    lv = ft.ListView(expand=True)
    field = ft.TextField(hint_text="новая заметка...", expand=True,
                         border_color=ft.Colors.PURPLE_200)

    def draw():
        lv.controls.clear()
        for n in notes:
            lv.controls.append(NoteCheck(n, toggle))
        page.update()

    def toggle(note, val):
        note.important = val

    def add(e):
        if field.value:
            notes.append(Note(field.value))
            field.value = ""
            draw()

    def clear(e):
        notes[:] = [n for n in notes if n.important]
        draw()

    field.on_submit = add

    page.add(field, ft.Row([
        ft.ElevatedButton("добавить", on_click=add),
        ft.TextButton("оставить важные", on_click=clear),
    ]), ft.Divider(), lv)

    draw()


ft.app(main)
