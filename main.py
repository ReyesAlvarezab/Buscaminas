import tkinter as tk
from tkinter import messagebox
import random

class Buscaminas:
    #Setea los atributos de la ventana principal del juego
    def __init__(self, ventana_principal, filas, cols, mines):
        self.ventana_principal = ventana_principal
        self.filas = filas
        self.cols = cols
        self.mines = mines

        self.tablero = [[0] * cols for _ in range(filas)]
        self.mine_positions = set()
        self.celda_bandera = set()

        self.create_widgets()

    def create_widgets(self):
        self.ventana_principal.title("Buscaminas")

        # Configurar menú
        menu_bar = tk.Menu(self.ventana_principal)
        self.ventana_principal.config(menu=menu_bar)

        # Configura la barra con las acciones de la ventana principal del juego
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Juego", menu=game_menu)
        game_menu.add_command(label="Nuevo Juego", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="Salir", command=self.ventana_principal.destroy)

        self.buttons = [[None] * self.cols for _ in range(self.filas)]

        # Crea los botones del tablero
        for i in range(self.filas):
            for j in range(self.cols):
                button = tk.Button(self.ventana_principal, text=" ", width=2, height=1,
                                   command=lambda i=i, j=j: self.click_izq(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

                # Asociar eventos al clic derecho
                button.bind("<Button-3>", lambda event, i=i, j=j: self.click_der(event, i, j))

        self.plantar_minas()

    def plantar_minas(self):
        # Ubica las minas en el tablero de forma aleatoria
        cont = 0
        while cont < self.mines:
            row = random.randint(0, self.filas - 1)
            col = random.randint(0, self.cols - 1)

            if self.tablero[row][col] != -1:
                self.tablero[row][col] = -1
                self.mine_positions.add((row, col))
                cont += 1

        self.calcular_minas_alrededor()

    def calcular_minas_alrededor(self):
        # Al presionar una casilla y no es bomba, cuenta cuantas bombas hay aledañas a esta casilla presionada.  
        for row, col in self.mine_positions:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.filas and 0 <= j < self.cols and self.tablero[i][j] != -1:
                        self.tablero[i][j] += 1

    def click_izq(self, row, col):
        # Acciones del click izquierdo
        button = self.buttons[row][col]

        # Si la celda está marcada con bandera, no permitir clic izquierdo
        if (row, col) in self.celda_bandera:
            return

        # Caso si la casilla es bomba
        if self.tablero[row][col] == -1:
            self.game_over()

        # Caso si la casilla NO es bomba
        else:
            self.revelar_celda(row, col)


    def click_der(self, event, row, col):
        # Acciones del click derecho
        button = self.buttons[row][col]

        # Marcar con una bandera
        if button["state"] == tk.NORMAL and (row, col) not in self.celda_bandera:
            button["text"] = "🚩"  
            self.celda_bandera.add((row, col))

        # Desmarcar una bandera    
        elif button["text"] == "🚩":
            button["text"] = " "  
            self.celda_bandera.remove((row, col))

    def revelar_celda(self, row, col):
        button = self.buttons[row][col]

        # Ocurre si la casilla no está marcada con una bandera
        if button["state"] == tk.NORMAL and (row, col) not in self.celda_bandera:
            value = self.tablero[row][col]

            # Caso en que la casilla no contiene una bomba y no hay bombas alrededor
            if value == 0:
                button["text"] = " "
                button["state"] = tk.DISABLED
                button["bg"] = "light blue"
                self.mostrar_aledaños(row, col)
        
            # Caso en que la casilla no contiene una bomba y si hay bombas al rededor
            else:
                button["text"] = str(value)
                button["state"] = tk.DISABLED
                button["bg"] = "light blue"

            # Cada vez que se presiona una casilla se verifica que se hayan clickeado todas las casillas
            # que no tienen bomba
            if self.check_win():
                self.game_win()

    def mostrar_aledaños(self, row, col):
        # Si se clickea una casilla que no tiene bombas al rededor, se "desbloquearan" todas las casillas que
        # no tengan bomba y sean aledañas a las que se vayan "desbloqueando", provovando la reacción en cadena
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self.filas and 0 <= j < self.cols:
                    self.revelar_celda(i, j)

    def game_over(self):
        # Mensaje que se muestra al perder el juego, además de reiniciarlo
        messagebox.showinfo("Game Over", "¡Has perdido!")
        self.reset_game()

    def game_win(self):
        # Mensaje de victoria
        messagebox.showinfo("¡Felicidades!", "¡Has ganado!")
        self.reset_game()

    def reset_game(self):
        # Acciones cuando se termina el juego, se crea uno nuevo
        self.ventana_principal.destroy()
        self.create_widgets
        root = tk.Tk()
        window_width = 400
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        iniciar_juego(root)

    def check_win(self):
        #Accion de checkear en cada momento si se ganó el juego
        for i in range(self.filas):
            for j in range(self.cols):
                if self.tablero[i][j] != -1 and self.buttons[i][j]["state"] == tk.NORMAL:
                    return False
        return True

def iniciar_juego(root):
    # Ventana para ingresar filas, columnas y minas
    param_window = tk.Toplevel(root)
    param_window.title("Configuración del juego")

    tk.Label(param_window, text="Número de filas:").grid(row=0, column=0)
    filas_entry = tk.Entry(param_window)
    filas_entry.grid(row=0, column=1)

    tk.Label(param_window, text="Número de columnas:").grid(row=1, column=0)
    cols_entry = tk.Entry(param_window)
    cols_entry.grid(row=1, column=1)

    tk.Label(param_window, text="Número de minas:").grid(row=2, column=0)
    mines_entry = tk.Entry(param_window)
    mines_entry.grid(row=2, column=1)

    start_button = tk.Button(param_window, text="Comenzar Juego", command=lambda: iniciar_juego_from_entry(root, filas_entry.get(), cols_entry.get(), mines_entry.get()))
    start_button.grid(row=3, columnspan=2)

def iniciar_juego_from_entry(root, filas, cols, mines):
    try:
        # Verifica que los valores sean positivos y un mínimo de minas
        filas = int(filas)
        cols = int(cols)
        mines = int(mines)
        if filas <= 0 or cols <= 0 or mines <= 0 or mines >= filas * cols:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")
        else:
            root.destroy()
            root = tk.Tk()
            game = Buscaminas(root, filas=filas, cols=cols, mines=mines)
            root.mainloop()
    except ValueError:
        # Verifica que los valores sean números
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos.")

def main():
    root = tk.Tk()

    # Configurar el tamaño de la ventana y centrarla
    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Iniciar la configuración del juego
    iniciar_juego(root)

    root.mainloop()

if __name__ == "__main__":
    main()

