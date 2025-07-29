import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as patches
from matplotlib.widgets import Button
import time

class InteractiveEightQueens:
    def __init__(self):
        self.size = 8
        self.board = [-1] * self.size
        self.solutions = []
        self.current_solution_index = 0
        self.is_solving = False
        self.is_paused = False
        self.should_stop = False
        self.step_delay = 0.5
        self.show_animation = True
        
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 10))
        plt.subplots_adjust(bottom=0.25)
        
        self.setup_buttons()
        self.draw_empty_board()
        
    def setup_buttons(self):
        # Fila superior de botones principales
        ax_solve = plt.axes([0.05, 0.12, 0.12, 0.04])
        ax_fast = plt.axes([0.19, 0.12, 0.12, 0.04])
        ax_instant = plt.axes([0.33, 0.12, 0.12, 0.04])
        ax_next = plt.axes([0.47, 0.12, 0.12, 0.04])
        ax_reset = plt.axes([0.61, 0.12, 0.12, 0.04])
        ax_all = plt.axes([0.75, 0.12, 0.12, 0.04])
        
        # Fila de controles
        ax_pause = plt.axes([0.05, 0.07, 0.12, 0.04])
        ax_stop = plt.axes([0.19, 0.07, 0.12, 0.04])
        ax_exit = plt.axes([0.75, 0.07, 0.12, 0.04])
        
        # Controles de velocidad
        ax_speed_label = plt.axes([0.35, 0.03, 0.1, 0.02])
        ax_slow = plt.axes([0.35, 0.07, 0.08, 0.03])
        ax_medium = plt.axes([0.45, 0.07, 0.08, 0.03])
        ax_fast_speed = plt.axes([0.55, 0.07, 0.08, 0.03])
        
        # Botones principales
        self.btn_solve = Button(ax_solve, 'Paso a Paso')
        self.btn_fast = Button(ax_fast, 'Rápido')
        self.btn_instant = Button(ax_instant, 'Instantáneo')
        self.btn_next = Button(ax_next, 'Siguiente')
        self.btn_reset = Button(ax_reset, 'Reiniciar')
        self.btn_all = Button(ax_all, 'Ver Todas')
        
        # Controles de ejecución
        self.btn_pause = Button(ax_pause, 'Pausar')
        self.btn_stop = Button(ax_stop, 'Detener')
        self.btn_exit = Button(ax_exit, 'Salir')
        
        # Controles de velocidad
        self.btn_speed_slow = Button(ax_slow, 'Lento')
        self.btn_speed_medium = Button(ax_medium, 'Medio')
        self.btn_speed_fast = Button(ax_fast_speed, 'Rápido')
        
        ax_speed_label.text(0.5, 0.5, 'Velocidad:', ha='center', va='center', fontsize=10)
        ax_speed_label.set_xticks([])
        ax_speed_label.set_yticks([])
        
        # Eventos de botones principales
        self.btn_solve.on_clicked(self.start_solving_animated)
        self.btn_fast.on_clicked(self.start_solving_fast)
        self.btn_instant.on_clicked(self.start_solving_instant)
        self.btn_next.on_clicked(self.next_solution)
        self.btn_reset.on_clicked(self.reset_board)
        self.btn_all.on_clicked(self.find_all_solutions)
        
        # Eventos de controles
        self.btn_pause.on_clicked(self.toggle_pause)
        self.btn_stop.on_clicked(self.stop_solving)
        self.btn_exit.on_clicked(self.exit_program)
        
        # Eventos de velocidad
        self.btn_speed_slow.on_clicked(lambda x: self.set_speed(0.8))
        self.btn_speed_medium.on_clicked(lambda x: self.set_speed(0.3))
        self.btn_speed_fast.on_clicked(lambda x: self.set_speed(0.1))
        
    def draw_empty_board(self):
        self.ax.clear()
        
        for i in range(self.size):
            for j in range(self.size):
                color = 'lightgray' if (i + j) % 2 == 0 else 'darkgray'
                square = patches.Rectangle((j, i), 1, 1, facecolor=color, edgecolor='black')
                self.ax.add_patch(square)
        
        self.ax.set_xlim(0, self.size)
        self.ax.set_ylim(0, self.size)
        self.ax.set_aspect('equal')
        self.ax.set_xticks(range(self.size + 1))
        self.ax.set_yticks(range(self.size + 1))
        self.ax.grid(True, alpha=0.3)
        
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.ax.set_xticklabels([''] + cols)
        self.ax.set_yticklabels(list(range(8, 0, -1)) + [''])
        
        self.ax.set_xlabel('Columnas', fontsize=12)
        self.ax.set_ylabel('Filas', fontsize=12)
        self.ax.set_title('Problema de las 8 Reinas - Tablero Vacío', fontsize=14, fontweight='bold')
        
        plt.draw()
    
    def draw_current_state(self, title="", highlight_row=None):
        if self.should_stop:
            return
        
        self.ax.clear()
        
        for i in range(self.size):
            for j in range(self.size):
                if highlight_row is not None and i == (self.size - 1 - highlight_row):
                    color = 'yellow' if (i + j) % 2 == 0 else 'orange'
                else:
                    color = 'lightgray' if (i + j) % 2 == 0 else 'darkgray'
                square = patches.Rectangle((j, i), 1, 1, facecolor=color, edgecolor='black')
                self.ax.add_patch(square)
        
        for row in range(self.size):
            if self.board[row] != -1:
                col = self.board[row]
                queen_x = col + 0.5
                queen_y = self.size - row - 0.5
                
                circle = Circle((queen_x, queen_y), 0.3, color='gold', ec='black', linewidth=2)
                self.ax.add_patch(circle)
                
                crown_points = []
                for i in range(5):
                    angle = i * 72 - 90
                    x = queen_x + 0.15 * np.cos(np.radians(angle))
                    y = queen_y + 0.15 * np.sin(np.radians(angle))
                    crown_points.append([x, y])
                
                crown = patches.Polygon(crown_points, closed=True, color='orange', ec='black')
                self.ax.add_patch(crown)
                
                self.ax.text(queen_x, queen_y, str(row + 1), ha='center', va='center', 
                           fontsize=10, fontweight='bold', color='black')
        
        # Agregar indicador de estado
        status_text = ""
        if self.is_paused:
            status_text = " [PAUSADO]"
        elif self.should_stop:
            status_text = " [DETENIENDO...]"
        
        self.ax.set_xlim(0, self.size)
        self.ax.set_ylim(0, self.size)
        self.ax.set_aspect('equal')
        self.ax.set_xticks(range(self.size + 1))
        self.ax.set_yticks(range(self.size + 1))
        self.ax.grid(True, alpha=0.3)
        
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.ax.set_xticklabels([''] + cols)
        self.ax.set_yticklabels(list(range(8, 0, -1)) + [''])
        
        self.ax.set_xlabel('Columnas', fontsize=12)
        self.ax.set_ylabel('Filas', fontsize=12)
        self.ax.set_title(title + status_text, fontsize=14, fontweight='bold')
        
        plt.draw()
        if self.show_animation and not self.should_stop:
            plt.pause(self.step_delay)
    
    def is_safe(self, row, col):
        for i in range(row):
            if self.board[i] == col:
                return False
            if abs(self.board[i] - col) == abs(i - row):
                return False
        return True
    
    def backtrack_visual(self, row):
        if self.should_stop:
            return False
        
        if self.wait_if_paused():
            return False
        
        if row == self.size:
            self.draw_current_state("¡Solución Encontrada!")
            return True
        
        self.draw_current_state(f"Buscando posición para Reina {row + 1}", highlight_row=row)
        
        for col in range(self.size):
            if self.should_stop:
                return False
            
            if self.wait_if_paused():
                return False
            
            if self.is_safe(row, col):
                self.board[row] = col
                self.draw_current_state(f"Reina {row + 1} colocada en columna {col + 1}")
                
                if self.backtrack_visual(row + 1):
                    return True
                
                if self.should_stop:
                    return False
                
                self.board[row] = -1
                self.draw_current_state(f"Retrocediendo desde fila {row + 1}")
        
        return False
    
    def toggle_pause(self, event):
        if not self.is_solving:
            print("No hay proceso en ejecución para pausar")
            return
        
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.btn_pause.label.set_text('Reanudar')
            print("⏸️ Proceso pausado - Presiona 'Reanudar' para continuar")
        else:
            self.btn_pause.label.set_text('Pausar')
            print("▶️ Proceso reanudado")
        
        plt.draw()
    
    def stop_solving(self, event):
        if not self.is_solving:
            print("No hay proceso en ejecución para detener")
            return
        
        self.should_stop = True
        self.is_paused = False
        print("🛑 Deteniendo proceso de búsqueda...")
        
        # Resetear texto del botón pausar
        self.btn_pause.label.set_text('Pausar')
        plt.draw()
    
    def exit_program(self, event):
        print("👋 Cerrando programa...")
        plt.close('all')
        exit()
    
    def wait_if_paused(self):
        while self.is_paused and not self.should_stop:
            plt.pause(0.1)
        
        if self.should_stop:
            return True
        return False
    
    def set_speed(self, delay):
        self.step_delay = delay
        speed_name = "Lento" if delay > 0.5 else "Medio" if delay > 0.2 else "Rápido"
        print(f"Velocidad cambiada a: {speed_name} ({delay}s por paso)")
    
    def solve_optimized(self):
        def backtrack(row):
            if self.should_stop:
                return False
            
            if row == self.size:
                return True
            
            for col in range(self.size):
                if self.should_stop:
                    return False
                
                if self.is_safe(row, col):
                    self.board[row] = col
                    if backtrack(row + 1):
                        return True
                    self.board[row] = -1
            return False
        
        return backtrack(0)
    
    def start_solving_animated(self, event):
        if self.is_solving:
            return
        
        self.is_solving = True
        self.should_stop = False
        self.is_paused = False
        self.show_animation = True
        self.board = [-1] * self.size
        
        # Resetear botón pausar
        self.btn_pause.label.set_text('Pausar')
        
        self.draw_current_state("Iniciando búsqueda animada...")
        
        success = self.backtrack_visual(0)
        
        if success and not self.should_stop:
            self.solutions = [self.board.copy()]
            self.current_solution_index = 0
            self.show_solution_info()
        elif self.should_stop:
            self.draw_current_state("Búsqueda detenida por el usuario")
            self.board = [-1] * self.size
        else:
            self.draw_current_state("No se encontró solución")
        
        self.is_solving = False
        self.should_stop = False
    
    def start_solving_fast(self, event):
        if self.is_solving:
            return
        
        self.is_solving = True
        self.should_stop = False
        self.board = [-1] * self.size
        
        self.draw_current_state("Resolviendo rápidamente...")
        
        old_delay = self.step_delay
        self.step_delay = 0.1
        
        success = self.backtrack_visual(0)
        
        self.step_delay = old_delay
        
        if success and not self.should_stop:
            self.solutions = [self.board.copy()]
            self.current_solution_index = 0
            self.show_solution_info()
        elif self.should_stop:
            self.draw_current_state("Búsqueda detenida por el usuario")
            self.board = [-1] * self.size
        else:
            self.draw_current_state("No se encontró solución")
        
        self.is_solving = False
        self.should_stop = False
    
    def start_solving_instant(self, event):
        if self.is_solving:
            return
        
        self.is_solving = True
        self.should_stop = False
        self.board = [-1] * self.size
        
        self.draw_current_state("Resolviendo instantáneamente...")
        
        start_time = time.time()
        success = self.solve_optimized()
        end_time = time.time()
        
        if success and not self.should_stop:
            self.solutions = [self.board.copy()]
            self.current_solution_index = 0
            solve_time = (end_time - start_time) * 1000
            title = f"¡Resuelto en {solve_time:.2f} ms!"
            self.draw_current_state(title)
            self.show_solution_info()
            print(f"Tiempo de resolución: {solve_time:.2f} milisegundos")
        elif self.should_stop:
            self.draw_current_state("Búsqueda detenida por el usuario")
            self.board = [-1] * self.size
        else:
            self.draw_current_state("No se encontró solución")
        
        self.is_solving = False
        self.should_stop = False
    
    def show_solution_info(self):
        if self.solutions:
            solution = self.solutions[self.current_solution_index]
            cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            chess_notation = [f"{cols[col]}{8-row}" for row, col in enumerate(solution)]
            
            title = f"Solución {self.current_solution_index + 1}/{len(self.solutions)}"
            self.draw_current_state(title)
            
            print(f"\nSolución encontrada:")
            print(f"Posiciones: {', '.join(chess_notation)}")
    
    def next_solution(self, event):
        if self.is_solving:
            return
        
        self.board = [-1] * self.size
        self.draw_current_state("Buscando siguiente solución...")
        
        found_new = False
        attempt = 0
        max_attempts = 100
        
        while not found_new and attempt < max_attempts:
            self.board = [-1] * self.size
            if self.solve_different_solution():
                solution_tuple = tuple(self.board)
                existing_solutions = [tuple(sol) for sol in self.solutions]
                
                if solution_tuple not in existing_solutions:
                    self.solutions.append(self.board.copy())
                    self.current_solution_index = len(self.solutions) - 1
                    found_new = True
            
            attempt += 1
        
        if found_new:
            self.show_solution_info()
        else:
            self.draw_current_state("No se encontraron más soluciones únicas")
    
    def solve_different_solution(self):
        import random
        
        def backtrack_random(row):
            if row == self.size:
                return True
            
            cols = list(range(self.size))
            random.shuffle(cols)
            
            for col in cols:
                if self.is_safe(row, col):
                    self.board[row] = col
                    if backtrack_random(row + 1):
                        return True
                    self.board[row] = -1
            
            return False
        
        return backtrack_random(0)
    
    def find_all_solutions(self, event):
        if self.is_solving:
            return
        
        self.draw_current_state("Encontrando todas las soluciones...")
        
        all_solutions = []
        board = [-1] * self.size
        
        def find_all_recursive(row):
            if row == self.size:
                all_solutions.append(board.copy())
                return
            
            for col in range(self.size):
                safe = True
                for i in range(row):
                    if board[i] == col or abs(board[i] - col) == abs(i - row):
                        safe = False
                        break
                
                if safe:
                    board[row] = col
                    find_all_recursive(row + 1)
                    board[row] = -1
        
        find_all_recursive(0)
        
        self.solutions = all_solutions
        self.current_solution_index = 0
        
        if self.solutions:
            self.board = self.solutions[0].copy()
            title = f"Encontradas {len(self.solutions)} soluciones - Mostrando solución 1"
            self.draw_current_state(title)
            
            print(f"\n¡Se encontraron {len(self.solutions)} soluciones!")
            print("Usa 'Siguiente Solución' para ver las demás.")
            
            for i, solution in enumerate(self.solutions[:5]):
                cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                chess_notation = [f"{cols[col]}{8-row}" for row, col in enumerate(solution)]
                print(f"Solución {i+1}: {', '.join(chess_notation)}")
        else:
            self.draw_current_state("No se encontraron soluciones")
    
    def reset_board(self, event):
        if self.is_solving:
            return
        
        self.board = [-1] * self.size
        self.solutions = []
        self.current_solution_index = 0
        self.draw_empty_board()
        print("\nTablero reiniciado")
    
    def show(self):
        plt.show()

if __name__ == "__main__":
    print("=== PROBLEMA DE LAS 8 REINAS INTERACTIVO ===")
    print("\n🎮 CONTROLES PRINCIPALES:")
    print("- 'Paso a Paso': Animación completa del proceso")
    print("- 'Rápido': Animación acelerada")
    print("- 'Instantáneo': Resolución ultra-rápida")
    print("- 'Siguiente': Busca nueva solución")
    print("- 'Ver Todas': Encuentra las 92 soluciones")
    print("- 'Reiniciar': Limpia el tablero")
    print("\n⏯️ CONTROLES DE EJECUCIÓN:")
    print("- 'Pausar/Reanudar': Pausa la animación en curso")
    print("- 'Detener': Cancela la búsqueda actual")
    print("- 'Salir': Cierra el programa")
    print("\n⚡ VELOCIDADES:")
    print("- 'Lento': 0.8s por paso (educativo)")
    print("- 'Medio': 0.3s por paso (balanceado)")
    print("- 'Rápido': 0.1s por paso (dinámico)")
    print("\n🚀 TIP: ¡Prueba el modo 'Instantáneo' para máxima velocidad!")
    print("💡 Durante la animación puedes pausar o detener en cualquier momento\n")
    
    game = InteractiveEightQueens()
    game.show()