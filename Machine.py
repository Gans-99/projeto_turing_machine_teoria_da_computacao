from State import State

class Machine:
    def __init__(self, q: State, w: str, _range: int, blank=' '):
        self.q = q
        self.w = w if w is not None else ''
        self.blank = blank
        self.set_fita_space(_range)
        self.init_fita(self.w)
        print(f'Fita inicial: {self.get_tape_as_string()}')

    def run(self, max_steps=1000):
        steps = 0

        while steps < max_steps:
            cur_sym = self.tape[self.head]
            transition = self.q.transition(cur_sym)

            if transition is None:
                if self.q.isFinal:
                    print(f'\nAceitou em {steps} passos !!!')
                    print('Fita final:', self.get_tape_as_string())
                    return True
                else:
                    print(f'\nRejeitou em {steps} passos !!!')
                    print('Fita final:', self.get_tape_as_string())
                    return False

            edge = transition.getEdge()
            next_state = transition.getState()

            write = edge.getWrite()
            move = edge.getMove()

            print(f'{self.q.getName()} lendo [{cur_sym}] -> escreve [{write}] move [{move}] vai para {next_state.getName()}')

            if write is not None:
                self.tape[self.head] = write

            if move in ('R', 'D', '>'):
                self.head += 1
            elif move in ('L', 'E', '<'):
                self.head -= 1

            self.q = next_state
            steps += 1

        print('Parou por limite de passos !!!')
        return False

    def init_fita(self, w):
        i = 0
        for a in list(w):
            self.tape[self.head + i] = a
            i += 1

    def set_fita_space(self, _range):
        self.range = _range
        self.max = self.range * 2 + 3
        self.tape = [self.blank] * self.max
        self.head = self.range + 1

    def get_tape_as_string(self):
        return ''.join([c if c is not None else self.blank for c in self.tape]).strip()
