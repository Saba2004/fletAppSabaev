import flet as ft

class Task:
    def __init__(self, text, done=False):
        self.text = text
        self.done = done

def main(page: ft.Page):
    page.title = "Todo"

    tasks = []
    list_view = ft.ListView(expand=True)
    field = ft.TextField(hint_text="задача...", expand=True)

    def draw():
        list_view.controls.clear()
        for t in tasks:
            cb = ft.Checkbox(label=t.text, value=t.done)
            cb.on_change = lambda e, task=t: setattr(task, "done", e.control.value)
            list_view.controls.append(cb)
        page.update()

    def add(e):
        if field.value:
            tasks.append(Task(field.value))
            field.value = ""
            draw()

    def clear(e):
        tasks[:] = [t for t in tasks if not t.done]
        draw()

    page.add(field, ft.Row([
        ft.ElevatedButton("добавить", on_click=add),
        ft.TextButton("убрать готовые", on_click=clear),
    ]), list_view)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=add)

    field.on_submit = add
    draw()

ft.app(main)