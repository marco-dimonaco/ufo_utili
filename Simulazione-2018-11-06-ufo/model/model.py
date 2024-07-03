import networkx as nx
import copy
import geopy
from geopy import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self._bestdTot = None
        self._bestComp = None
        self._grafo = nx.DiGraph()
        self._idMap = {}
        for i in DAO.getAllStates():
            self._idMap[i.id] = i

    def buildGraph(self, anno):
        self._grafo.clear()
        allNodes = DAO.getStates(anno)
        self._grafo.add_nodes_from(allNodes)
        self.addEdges(anno)
        return True

    def addEdges(self, anno):
        allConnessioni = DAO.getConnections(self._idMap, anno)
        for c in allConnessioni:
            self._grafo.add_edge(c.st1, c.st2)

    def getSuccessori(self, origine):
        successori = list(self._grafo.successors(self._idMap[origine]))
        return successori

    def getPredecessori(self, origine):
        predecessori = list(self._grafo.predecessors(self._idMap[origine]))
        return predecessori

    def getRaggiungibili(self, origine):
        raggiungibili = list(nx.dfs_tree(self._grafo, self._idMap[origine]))
        return raggiungibili, len(raggiungibili)

    def getPath(self, n):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [n]
        successori = self._grafo.successors(n)
        for a in successori:
            if a not in parziale:
                parziale.append(a)
                self._ricorsione(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self._bestComp

    def _ricorsione(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache

        if len(parziale) > self._bestdTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestdTot = len(parziale)
            return
        # verifico se posso aggiungere un altro elemento
        successori = self._grafo.successors(parziale[-1])
        for a in successori:
            if a not in parziale:
                parziale.append(a)
                self._ricorsione(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

    @staticmethod
    def getYears():
        return DAO.getAllYears()

    def getNodes(self):
        return self._grafo.nodes

    def printGraphDetails(self):
        return (f"#Vertici: {len(self._grafo.nodes)}\n"
                f"#Archi: {len(self._grafo.edges)}")
