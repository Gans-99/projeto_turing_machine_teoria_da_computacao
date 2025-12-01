# .\.venv\Scripts\python.exe -m pip install readchar
#import threading
#import readchar
from State import State
from Transition import Transition
from Edge import Edge
from Machine import Machine

def teste_y_x():
    print("{ w in Σ^* | w é um número binario multiplo de 3}")
    q0 = State('q0')
    q1 = State('q1')
    q2 = State('q2')
    q0.setFinal()

    q0.addTransition(q0, '0')
    q0.addTransition(q1, '1')

    q1.addTransition(q0, '1')
    q1.addTransition(q2, '0')

    q2.addTransition(q2, '1')
    q2.addTransition(q1, '0')

    w = '000111'

    mt = Machine(q0, w, 20)
    mt.run()

if __name__ == "__main__":
    teste_y_x()

    #teste push
