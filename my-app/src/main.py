import flet as ft
from abc import ABC, abstractmethod
from datetime import datetime


class Base(ABC):
    @abstractmethod
    def build(self):
        ...


class Note(Base):
    def __init__(self, text, category="общее"):
        self.text = text
        self.category = category
        self.important = False
        self.created = datetime.now().strftime("%d.%m %H:%M")
        self.views = 0

    def build(self):
        self.views += 1
        return f"[{self.category}] {self.text} — {self.created} (открыто {self.views})"


class NoteField(Base, ft.TextField):
    def __init__(self):
        ft.TextField.__init__(self)
        self.hint_text = "новая заметка..."
        self.expand = True
        self.border_color = ft.Colors.PURPLE_200
        self.focused_border_color = ft.Colors.PURPLE_400

    def build(self):
        return self


class NoteCheck(Base, ft.Checkbox):
    def __init__(self, note, toggle):
        ft.Checkbox.__init__(self)
        self.note = note
        self.label = note.build()
        self.on_change = lambda e: toggle(note, e.control.value)

    def build(self):
        return self


class AddButton(Base, ft.ElevatedButton):
    def __init__(self, on_click):
        ft.ElevatedButton.__init__(self)
        self.text = "добавить"
        self.icon = ft.Icons.EDIT_NOTE
        self.on_click = on_click
        self.style = ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_400,
        )

    def build(self):
        return self


def main(page: ft.Page):
    page.title = "Заметки"

    notes = []
    lv = ft.ListView(expand=True)
    field = NoteField()

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
        AddButton(add),
        ft.TextButton("оставить важные", on_click=clear),
    ]), ft.Divider(), lv)

    draw()


ft.app(main)
