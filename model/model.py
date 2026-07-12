import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getAllCategories()

    def creaGrafo(self, category_id, d1, d2):
        self._graph.clear()
        self._idMap.clear()

        vertici = DAO.getAllProducts(category_id)
        for v in vertici:
            self._idMap[v.product_id] = v
        self._graph.add_nodes_from(vertici)

        for n1, n2, weight in DAO.getProductsByItems(category_id, d1, d2, self._idMap):
            self._graph.add_edge(n1, n2, weight=weight)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()




