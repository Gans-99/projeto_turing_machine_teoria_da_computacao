from State import State
from Machine import Machine

def teste_anbn(): # Livre de contexto
    print("{ a^nb^n | n>=0 }")
    q0 = State('q0')
    q1 = State('q1')
    q2 = State('q2')
    q3 = State('q3')
    q4 = State('q4')
    qf = State('qf')
    qf.setFinal()

    q0.addTransition(q1, 'a', 'A', 'D')
    q0.addTransition(q3, None, None, 'E')
    q0.addTransition(q4, 'B', 'B', 'D')

    q1.addTransition(q1, 'a', 'a', 'D')
    q1.addTransition(q1, 'B', 'B', 'D')
    q1.addTransition(q2, 'b', 'B', 'E')

    q2.addTransition(q2, 'a', 'a', 'E')
    q2.addTransition(q2, 'B', 'B', 'E')
    q2.addTransition(q0, 'A', 'A', 'D')

    q4.addTransition(q4, 'B', 'B', 'D')
    q4.addTransition(q3, None, None, 'E')

    q3.addTransition(q3, 'A', 'A', 'E')
    q3.addTransition(q3, 'B', 'B', 'E')
    q3.addTransition(qf, None, None, 'D')

    w = 'aaabbbb'   # REJEITA
    #w = 'aaaabbbb'    # ACEITA

    mt = Machine(q0, w, 20)
    mt.run()

def teste_y_x(): # Regular
    print("{ w in Σ^* | w é um número binario multiplo de 3}")
    q0 = State('q0')
    q1 = State('q1')
    q2 = State('q2')
    q0.setFinal()

    q0.addTransition(q0, '0', '0', 'D')
    q0.addTransition(q1, '1', '1', 'D')

    q1.addTransition(q0, '1', '1', 'D')
    q1.addTransition(q2, '0', '0', 'D')

    q2.addTransition(q2, '1', '1', 'D')
    q2.addTransition(q1, '0', '0', 'D')

    w = '00001101'  # REJEITA
    w = '0000110'   # ACEITA

    mt = Machine(q0, w, 20)
    mt.run()

def teste_numero_par_de_uns():
    print("\nTeste: número par de 1s")

    q0 = State('q0')
    q1 = State('q1')
    q0.setFinal()

    q0.addTransition(q0, '0', '0', 'D')
    q0.addTransition(q1, '1', '1', 'D')

    q1.addTransition(q1, '0', '0', 'D')
    q1.addTransition(q0, '1', '1', 'D')

    w = '1101'  # REJEITA
    w = '110'   # ACEITA

    mt = Machine(q0, w, 20)
    mt.run()

def teste_anbncn(): # Sensível ao contexto
    print("\nTeste: { a^n b^n c^n | n > 0 }")

    q_start = State('q_start')  # estado inicial (nega branco -> rejeita se vazio)
    q0 = State('q0')            # estado de iteração (quando vindo de volta)
    q1 = State('q1')            # buscar e marcar 'b'
    q2 = State('q2')            # buscar e marcar 'c'
    q3 = State('q3')            # voltar ao início (esquerda)
    qf = State('qf')            # final
    qf.setFinal()

    # ---------------------------
    # q_start: inicial (não aceita fita vazia)
    # ---------------------------
    q_start.addTransition(q1, 'a', 'A', 'D')   # primeiro 'a' -> marca e vai procurar 'b'
    q_start.addTransition(q_start, 'A', 'A', 'D')  # pula A
    q_start.addTransition(q_start, 'B', 'B', 'D')  # pula B
    q_start.addTransition(q_start, 'C', 'C', 'D')  # pula C
    # IMPORTANT: NÃO colocar transição para None aqui (vazio deve rejeitar)

    # ---------------------------
    # q0: estado de iteração normal (após retornar do q3)
    # Se encontrar branco aqui -> aceita (pois já houve ao menos 1 marcação)
    # ---------------------------
    q0.addTransition(q1, 'a', 'A', 'D')
    q0.addTransition(q0, 'A', 'A', 'D')
    q0.addTransition(q0, 'B', 'B', 'D')
    q0.addTransition(q0, 'C', 'C', 'D')
    q0.addTransition(qf, None, None, 'D')  # quando tudo marcado e chegarmos ao branco → aceita

    # ---------------------------
    # q1: avançar até achar 'b' não marcado e marcá-lo
    # ---------------------------
    q1.addTransition(q1, 'a', 'a', 'D')
    q1.addTransition(q1, 'A', 'A', 'D')
    q1.addTransition(q1, 'B', 'B', 'D')
    q1.addTransition(q1, 'C', 'C', 'D')
    q1.addTransition(q2, 'b', 'B', 'D')  # marca b e segue para buscar c

    # ---------------------------
    # q2: avançar até achar 'c' não marcado e marcá-lo (depois volta)
    # ---------------------------
    q2.addTransition(q2, 'a', 'a', 'D')
    q2.addTransition(q2, 'A', 'A', 'D')
    q2.addTransition(q2, 'b', 'b', 'D')
    q2.addTransition(q2, 'B', 'B', 'D')
    q2.addTransition(q2, 'C', 'C', 'D')
    q2.addTransition(q3, 'c', 'C', 'E')  # marca c e começa a voltar (E = esquerda)

    # ---------------------------
    # q3: volta ao início (anda para a esquerda até encontrar branco)
    #       ao encontrar branco, move para a direita e vai para q0 (iteração)
    # ---------------------------
    q3.addTransition(q3, 'A', 'A', 'E')
    q3.addTransition(q3, 'B', 'B', 'E')
    q3.addTransition(q3, 'C', 'C', 'E')
    q3.addTransition(q3, 'a', 'a', 'E')
    q3.addTransition(q3, 'b', 'b', 'E')
    q3.addTransition(q3, 'c', 'c', 'E')
    q3.addTransition(q0, None, None, 'D')  # ao encontrar branco à esquerda, vai para q0 (move D para cair no 1º símbolo)

    # ---------------------------
    # Palavra de teste
    # ---------------------------
    #w = "aaabbbccc"   # deve ACEITAR
    #w = "abc"       # também aceita
    #w = ""          # deve REJEITAR (n>0)
    w = "abbccc"    # rejeita
    #w = "aaabbbcc"  # rejeita

    mt = Machine(q_start, w, 100)
    mt.run()

if __name__ == "__main__":
    #teste_anbn()
    #teste_y_x()
    #teste_numero_par_de_uns()
    teste_anbncn()
