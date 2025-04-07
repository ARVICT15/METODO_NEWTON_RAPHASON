import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import numpy as np
import sympy as sp

class MetodosNumericosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroMath XR-9000")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a1a')
        
        # Estilo futurista
        self.style = ttk.Style()
        self.style.theme_create('cyber', settings={
            "TLabel": {
                "configure": {"background": "#0a0a1a", "foreground": "#00ffcc", "font": ('Courier', 12)}
            },
            "TButton": {
                "configure": {"background": "#003333", "foreground": "#00ffcc", 
                              "font": ('Courier', 12, 'bold'), "borderwidth": 1},
                "map": {"background": [("active", "#006666")]}
            },
            "TFrame": {
                "configure": {"background": "#0a0a1a"}
            },
            "TNotebook": {
                "configure": {"background": "#0a0a1a", "borderwidth": 0}
            },
            "TNotebook.Tab": {
                "configure": {"background": "#003333", "foreground": "#00ffcc", 
                             "font": ('Courier', 11, 'bold'), "padding": [10, 5]},
                "map": {"background": [("selected", "#006666")]}
            }
        })
        self.style.theme_use('cyber')
        
        # Crear efecto de neón
        self.neon_blue = "#00f3ff"
        self.neon_pink = "#ff00ff"
        
        # Banner superior
        self.header = tk.Frame(root, bg='#0a0a1a', height=100)
        self.header.pack(fill=tk.X, pady=(0, 20))
        
        try:
            logo_img = Image.open("logo.png").resize((80, 80))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(self.header, image=self.logo, bg='#0a0a1a').pack(side=tk.LEFT, padx=20)
        except:
            # Logo por defecto si no se encuentra la imagen
            tk.Label(self.header, text="[X]", font=('Courier', 24), 
                    bg='#0a0a1a', fg=self.neon_blue).pack(side=tk.LEFT, padx=20)
        
        tk.Label(self.header, text="NEURO-MATH XR-9000", font=('Courier', 28, 'bold'), 
                bg='#0a0a1a', fg=self.neon_blue).pack(side=tk.LEFT, pady=20)
        
        # Panel de pestañas
        self.tab_control = ttk.Notebook(root)
        
        # Pestaña de menú principal
        self.tab_menu = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_menu, text='≡ MENÚ PRINCIPAL')
        
        # Pestaña Newton-Raphson
        self.tab_newton = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_newton, text='∇ NEWTON-RAPHSON')
        
        # Pestaña Secante
        self.tab_secante = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_secante, text='⇄ MÉTODO SECANTE')
        
        self.tab_control.pack(expand=1, fill='both')
        
        # Configurar menú principal
        self.setup_menu_tab()
        
        # Configurar pestañas de métodos
        self.setup_newton_tab()
        self.setup_secante_tab()
        
        # Efecto de borde neón
        self.create_neon_border()
    
    def create_neon_border(self):
        border = tk.Frame(self.root, bg=self.neon_blue, height=2)
        border.pack(fill=tk.X, side=tk.BOTTOM)
        border = tk.Frame(self.root, bg=self.neon_blue, height=2)
        border.pack(fill=tk.X, side=tk.TOP)
        border = tk.Frame(self.root, bg=self.neon_blue, width=2)
        border.pack(fill=tk.Y, side=tk.LEFT)
        border = tk.Frame(self.root, bg=self.neon_blue, width=2)
        border.pack(fill=tk.Y, side=tk.RIGHT)
    
    def setup_menu_tab(self):
        # Marco central del menú
        menu_frame = tk.Frame(self.tab_menu, bg='#0a0a1a')
        menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título del menú
        tk.Label(menu_frame, text="SELECCIONE ALGORITMO", 
                font=('Courier', 20, 'bold'), bg='#0a0a1a', fg=self.neon_pink).grid(row=0, column=0, pady=(0, 40))
        
        # Botones de métodos
        btn_style = {'font': ('Courier', 14), 'width': 25, 'height': 2, 
                    'bg': '#003333', 'fg': self.neon_blue, 'activebackground': '#006666',
                    'activeforeground': self.neon_blue, 'relief': tk.RAISED, 'borderwidth': 3}
        
        newton_btn = tk.Button(menu_frame, text="NEWTON-RAPHSON", 
                             command=lambda: self.tab_control.select(self.tab_newton), **btn_style)
        newton_btn.grid(row=1, column=0, pady=15)
        
        secante_btn = tk.Button(menu_frame, text="MÉTODO SECANTE", 
                              command=lambda: self.tab_control.select(self.tab_secante), **btn_style)
        secante_btn.grid(row=2, column=0, pady=15)
        
        # Efecto de terminal inferior
        terminal_frame = tk.Frame(self.tab_menu, bg='black', height=100)
        terminal_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        terminal_text = tk.Label(terminal_frame, text=">>> Sistema listo. Esperando selección de algoritmo...", 
                                font=('Courier', 10), bg='black', fg='#00ff00', anchor='w')
        terminal_text.pack(fill=tk.X, padx=10)
    
    def setup_newton_tab(self):
        # Configuración similar a la interfaz de Newton-Raphson anterior
        # ... (código de la interfaz Newton-Raphson que proporcionaste)
        
        # Ejemplo simplificado:
        frame = ttk.Frame(self.tab_newton)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="NEWTON-RAPHSON ACTIVADO", font=('Courier', 16, 'bold')).pack(pady=20)
        # Aquí iría el resto de tu interfaz Newton-Raphson
    
    def setup_secante_tab(self):
        # Configuración similar a la interfaz de Secante anterior
        # ... (código de la interfaz Secante que proporcionaste)
        
        # Ejemplo simplificado:
        frame = ttk.Frame(self.tab_secante)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="ALGORITMO SECANTE ACTIVADO", font=('Courier', 16, 'bold')).pack(pady=20)
        # Aquí iría el resto de tu interfaz Secante

if __name__ == "__main__":
    root = tk.Tk()
    app = MetodosNumericosApp(root)
    root.mainloop()