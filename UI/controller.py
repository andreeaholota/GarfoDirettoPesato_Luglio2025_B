import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._sceltaCategory = None
        self._dataInizio = None
        self._dataFine = None

    def fillDDCategory(self):
        for c in self._model.getCategories():
            self._view._ddcategory.options.append(
                ft.dropdown.Option(data=c, text=c.category_name, on_click= self._pickCategory)
            )
        self._view.update_page()

    def fillDDDataInizio(self):
        for c in self._model.getDateRange():
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(data=c, text=c, on_click= self.pickStartDate)
            )
        self._view.update_page()

    def fillDDDataFine(self):
        for c in self._model.getDateRange():
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(data=c, text=c, on_click=self.pickEndDate)
            )
        self._view.update_page()

    def pickStartDate(self, e):
        self._dataInizio = e.control.value  # o self._view._dp1.value, equivalente

    def pickEndDate(self, e):
        self._dataFine = e.control.value

    def _pickCategory(self, e):
        self._sceltaCategory = e.control.data

    def handleCreaGrafo(self, e):
        if self._sceltaCategory is None:
            self._view.create_alert("Seleziona una categoria!");
            return
        try:
            self._model.creaGrafo(self._sceltaCategory.category_id, self._dataInizio, self._dataFine )
        except Exception as ex:
            self._view.create_alert(f"Errore: {ex}")
            return
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {a}"))
        self._view.update_page()

    def handleBestProdotti(self, e):
        pass

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

        self._view._dp1.on_change = self.pickStartDate
        self._view._dp2.on_change = self.pickEndDate
