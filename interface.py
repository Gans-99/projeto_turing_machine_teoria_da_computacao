import tkinter as tk
from tkinter import ttk, messagebox
from State import State
from Machine import Machine

class TuringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina de Turing")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2e")

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#1e1e2e", foreground="white", font=("Segoe UI", 12))
        self.style.configure("TButton", font=("Segoe UI", 11), padding=6)
        self.style.map("TButton", background=[("active", "#3b82f6")])

        # --- Título ---
        title = ttk.Label(root, text="Simulador de Máquina de Turing", font=("Segoe UI", 18, "bold"), foreground="#38bdf8")
        title.pack(pady=15)

        # --- Entrada da fita ---
        entry_frame = ttk.Frame(root)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame, text="Entrada (fita):").grid(row=0, column=0, padx=5)
        self.entry_input = ttk.Entry(entry_frame, width=40)
        self.entry_input.grid(row=0, column=1, padx=5)

        ttk.Button(entry_frame, text="Executar", command=self.run_machine).grid(row=0, column=2, padx=5)

        # --- Seletor de teste ---
        ttk.Label(entry_frame, text="Teste:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_test = ttk.Combobox(entry_frame, values=["a^n b^n", "Binário múltiplo de 3", "Número par de 1s"])
        self.combo_test.current(0)
        self.combo_test.grid(row=1, column=1, padx=5, pady=5)

        # --- Área de fita ---
        self.canvas = tk.Canvas(root, width=700, height=150, bg="#2e2e3e", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.cells = []
        self.tape_data = []
        self.head_pos = 0

        # --- Área de saída ---
        self.text_output = tk.Text(root, width=90, height=12, bg="#181825", fg="white", insertbackground="white", font=("Consolas", 10))
        self.text_output.pack(pady=10)

    def build_tape(self, tape_str):
        self.canvas.delete("all")
        self.cells.clear()
        x = 20
        for i, c in enumerate(tape_str):
            rect = self.canvas.create_rectangle(x, 40, x+40, 90, fill="#4c566a", outline="#81a1c1", width=2)
            text = self.canvas.create_text(x+20, 65, text=c if c.strip() != "" else "□", font=("Consolas", 16), fill="white")
            self.cells.append((rect, text))
            x += 45
        self.head_indicator = self.canvas.create_polygon(45, 25, 35, 10, 55, 10, fill="#88c0d0")

    def move_head(self, pos):
        x = 45 + (pos * 45)
        self.canvas.coords(self.head_indicator, x, 25, x-10, 10, x+10, 10)
        self.canvas.update()

    def log(self, msg):
        self.text_output.insert(tk.END, msg + "\n")
        self.text_output.see(tk.END)

    def run_machine(self):
        self.text_output.delete(1.0, tk.END)
        w = self.entry_input.get().strip()
        if not w:
            messagebox.showerror("Erro", "Digite uma entrada para a fita.")
            return

        choice = self.combo_test.get()
        self.text_output.insert(tk.END, f"Executando teste: {choice}\nEntrada: {w}\n\n")

        # Seleciona teste
        if choice == "a^n b^n":
            q0 = State('q0'); q1 = State('q1'); q2 = State('q2'); q3 = State('q3'); q4 = State('q4'); qf = State('qf')
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
        elif choice == "Binário múltiplo de 3":
            q0 = State('q0'); q1 = State('q1'); q2 = State('q2')
            q0.setFinal()
            q0.addTransition(q0, '0', '0', 'D')
            q0.addTransition(q1, '1', '1', 'D')
            q1.addTransition(q0, '1', '1', 'D')
            q1.addTransition(q2, '0', '0', 'D')
            q2.addTransition(q2, '1', '1', 'D')
            q2.addTransition(q1, '0', '0', 'D')
        else:  # Número par de 1s
            q0 = State('q0'); q1 = State('q1')
            q0.setFinal()
            q0.addTransition(q0, '0', '0', 'D')
            q0.addTransition(q1, '1', '1', 'D')
            q1.addTransition(q1, '0', '0', 'D')
            q1.addTransition(q0, '1', '1', 'D')

        mt = Machine(q0, w, 20)
        self.build_tape(mt.get_tape_as_string())

        def step():
            cur_sym = mt.tape[mt.head]
            transition = mt.q.transition(cur_sym)
            if transition is None:
                if mt.q.isFinal:
                    self.log("\n✅ ACEITOU!")
                    self.canvas.config(bg="#14532d")
                else:
                    self.log("\n❌ REJEITOU!")
                    self.canvas.config(bg="#7f1d1d")
                return

            e = transition.getEdge()
            s = transition.getState()
            write, move = e.getWrite(), e.getMove()
            self.log(f"{mt.q.getName()} lendo [{cur_sym}] -> escreve [{write}] move [{move}] vai para {s.getName()}")
            if write is not None:
                mt.tape[mt.head] = write
                self.canvas.itemconfig(self.cells[mt.head - mt.range - 1][1], text=write)
            if move in ('R', 'D', '>'):
                mt.head += 1
            elif move in ('L', 'E', '<'):
                mt.head -= 1
            mt.q = s
            self.move_head(mt.head - mt.range - 1)
            self.root.after(500, step)

        step()

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringApp(root)
    root.mainloop()
