import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._selected_state = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        getYears = self._model.getYears()
        for y in getYears:
            self._listYear.append(y)
            self._view.ddyear.options.append(ft.dropdown.Option(str(y)))
        self._view.update_page()

    def handle_avvistamenti(self, e):
        self._view.txt_result.controls.clear()
        anno = self._view.ddyear.value
        if anno is None:
            self._view.create_alert("Seleziona un anno!")
            self._view.update_page()
            return
        else:
            grafo = self._model.buildGraph(anno[0:4])
            if grafo:
                self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!", color='green'))
                self._view.txt_result.controls.append(ft.Text(self._model.printGraphDetails()))
                nodi = self._model.getNodes()
                for n in nodi:
                    self._view.ddState.options.append(
                        ft.dropdown.Option(text=n.id, data=n, on_click=self.readDDState))
                self._view.update_page()
            else:
                self._view.txt_result.controls.append(ft.Text("Errore nella creazione del grafo!", color='red'))
                self._view.update_page()
                return

    def handle_analizza(self, e):
        stato = self._view.ddState.value
        if stato is None:
            self._view.create_alert("Seleziona uno stato!")
            self._view.update_page()
            return
        else:
            predecessori = self._model.getPredecessori(stato)
            self._view.txt_result.controls.append(ft.Text(f"PREDECESSORI DI {stato}:"))
            for p in predecessori:
                self._view.txt_result.controls.append(ft.Text(f"{p.id}"))

            successori = self._model.getSuccessori(stato)
            self._view.txt_result.controls.append(ft.Text(f"SUCCESSORI DI {stato}:"))
            for p in successori:
                self._view.txt_result.controls.append(ft.Text(f"{p.id}"))

            raggiungibili, n = self._model.getRaggiungibili(stato)
            self._view.txt_result.controls.append(ft.Text(f"RAGGIUNGIBILI DA {stato} SONO {n}:"))
            for p in raggiungibili:
                self._view.txt_result.controls.append(ft.Text(f"{p.id}"))
            self._view.update_page()
            return

    def handle_seqAvvistamenti(self, e):
        self._view.txt_result.controls.clear()
        self._view.update_page()
        selected_node = self._view.ddState.value
        if selected_node is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un Nodo!", color='red'))
            self._view.update_page()
        else:
            node = self._model._idMap[selected_node]
            percorso = self._model.getPath(node)
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino più lungo di avvistamenti successivi, lunghezza {len(percorso)}"))
            self._view.update_page()
            for n in percorso:
                self._view.txt_result.controls.append(
                    ft.Text(f"C{n.id}"))
                self._view.update_page()

    def readDDState(self, e):
        if e.control.data is None:
            self._selected_state = None
        else:
            self._selected_state = e.control.data
