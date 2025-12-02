from Edge import Edge
from Transition import Transition

class State:
    def __init__(self, name: str):
        self.name = name
        self.isFinal = False
        self.transitions = []

    def getName(self):
        return self.name

    def setFinal(self):
        self.isFinal = True

    # Aceita: (estado_destino, leitura, escrita, direcao)
    def addTransition(self, state, read=None, write=None, move=None):
        edge = Edge.instance(read, write, move)
        t = Transition(state, edge)
        self.transitions.append(t)
        return self

    def transition(self, symbol):
        for t in self.transitions:
            e = t.getEdge()
            expected = e.getC()
            if expected == symbol:
                return t
            # trata branco
            if expected is None and (symbol is None or symbol == ' '):
                return t
        return None


    def equals(self, s):
        if isinstance(s, State):
            return s.getName() == self.getName()
        return False
