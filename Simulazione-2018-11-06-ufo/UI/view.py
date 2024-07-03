import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.btn_seqAvv = None
        self.btn_analizza = None
        self.btn_avvistamenti = None
        self.ddState = None
        self.ddyear = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Lab13 - Ufo sighting", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW 1
        self.ddyear = ft.Dropdown(label="Anno", width=500)
        self.btn_avvistamenti = ft.ElevatedButton(text="Avvistamenti", on_click=self._controller.handle_avvistamenti)
        row1 = ft.Row([self.ddyear, self.btn_avvistamenti],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # ROW 2
        self.ddState = ft.Dropdown(label="Stato", width=500)
        self.btn_analizza = ft.ElevatedButton(text="Analizza", on_click=self._controller.handle_analizza)
        self.btn_seqAvv = ft.ElevatedButton(text="Sequenza di avvistamenti",
                                            on_click=self._controller.handle_seqAvvistamenti)
        row2 = ft.Row([self.ddState, self.btn_analizza, self.btn_seqAvv],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self._controller.fillDD()

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
