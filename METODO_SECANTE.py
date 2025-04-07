import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
from matplotlib.backend_bases import MouseButton

def secante(f, x0, x1, tol=1e-6, max_iter=100):
    iteraciones = []
    decimales = abs(int(np.log10(tol))) if tol > 0 else 6

    for i in range(max_iter):
        f_x0 = f(x0)
        f_x1 = f(x1)
        
        # Evitar división por cero
        if abs(f_x1 - f_x0) < 1e-12:
            return None, i, iteraciones

        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        error = abs(x2 - x1)

        iteraciones.append((
            i,
            round(x0, decimales),
            round(x1, decimales),
            round(f_x0, decimales),
            round(f_x1, decimales),
            round(x2, decimales),
            round(error, decimales)
        ))

        # Criterio de parada
        if error < tol:
            return x2, i + 1, iteraciones

        x0, x1 = x1, x2  # Actualizar valores para la siguiente iteración

    return x1, max_iter, iteraciones

def graficar_funcion(f_sympy, x0, x1, raiz, iteraciones, frame_grafica):
    x = sp.symbols('x')
    f_lambda = sp.lambdify(x, f_sympy, 'numpy')
    
    # Limpiar el frame de la gráfica anterior
    for widget in frame_grafica.winfo_children():
        widget.destroy()
    
    # Crear figura con fondo blanco
    fig = plt.Figure(figsize=(6, 4), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    
    # Calcular rango para la gráfica
    x_min = min(x0, x1, raiz if raiz is not None else x1) - 2
    x_max = max(x0, x1, raiz if raiz is not None else x1) + 2
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = f_lambda(x_vals)
    
    # Graficar función
    line, = ax.plot(x_vals, y_vals, label=f"f(x) = {sp.pretty(f_sympy)}", linewidth=2)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    
    # Almacenar puntos para interactividad
    puntos_grafica = []
    
    # Marcar puntos importantes (ahora tenemos dos puntos iniciales)
    punto_inicial1 = ax.scatter([x0], [f_lambda(x0)], color='red', s=80, 
                              label='Punto Inicial X0', zorder=5)
    punto_inicial2 = ax.scatter([x1], [f_lambda(x1)], color='blue', s=80,
                              label='Punto Inicial X1', zorder=5)
    puntos_grafica.append((x0, f_lambda(x0), "Punto inicial X0"))
    puntos_grafica.append((x1, f_lambda(x1), "Punto inicial X1"))
    
    if raiz is not None:
        punto_raiz = ax.scatter([raiz], [0], color='green', s=100, 
                               label='Raíz encontrada', zorder=5)
        puntos_grafica.append((raiz, 0, "Raíz encontrada"))
    
    # Marcar todas las iteraciones
    for iteracion in iteraciones:
        iter_idx, xi0, xi1, _, _, xi2, _ = iteracion
        punto = ax.scatter([xi2], [f_lambda(xi2)], color='orange', s=60, 
                         alpha=0.7, zorder=4)
        puntos_grafica.append((xi2, f_lambda(xi2), f"Iteración {iter_idx}"))
    
    # Configuración del gráfico
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("f(x)", fontsize=10)
    ax.legend(fontsize=9)
    ax.set_title("Gráfica de la función - Método de la Secante", pad=15)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Función para mostrar coordenadas al hacer clic
    def on_click(event):
        if event.inaxes != ax:
            return
        
        x_click = event.xdata
        y_click = event.ydata
        
        # Buscar el punto más cercano
        min_dist = float('inf')
        punto_cercano = None
        
        for x, y, label in puntos_grafica:
            dist = (x - x_click)**2 + (y - y_click)**2
            if dist < min_dist:
                min_dist = dist
                punto_cercano = (x, y, label)
        
        # Umbral de distancia para considerar un clic válido
        if min_dist < 0.5:
            x, y, label = punto_cercano
            if "Raíz" in label:
                ax.set_title(f"{label}: ({x:.6f}, {y:.6f})", pad=15)
            else:
                ax.set_title(f"{label}: ({x:.6f}, {y:.6f})", pad=15)
        else:
            ax.set_title(f"Coordenadas: ({x_click:.4f}, {y_click:.4f})", pad=15)
        
        fig.canvas.draw()
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    # Mostrar figura en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def actualizar_tabla(tabla, iteraciones):
    for row in tabla.get_children():
        tabla.delete(row)

    for iteracion in iteraciones:
        tabla.insert("", "end", values=iteracion)

def parse_tolerancia(tol_str):
    """Convierte una cadena como 'x10^-4' o '10^-4' a un valor numérico."""
    try:
        match = re.match(r'x?10\^(-?\d+)', tol_str)
        if match:
            exponente = int(match.group(1))
            return 10 ** exponente
        return float(tol_str)
    except:
        return 1e-6  # Valor por defecto

def calcular_secante():
    try:
        expr = entrada_funcion.get()
        x0 = float(entrada_x0.get().replace(',', '.'))  # Permitir comas
        x1 = float(entrada_x1.get().replace(',', '.'))  # Segundo punto inicial
        tol_str = entrada_tolerancia.get()
        tol = parse_tolerancia(tol_str)
        
        x = sp.symbols('x')
        f_sympy = sp.sympify(expr)
        f_lambda = sp.lambdify(x, f_sympy, 'numpy')
        
        raiz, num_iteraciones, datos_iteraciones = secante(f_lambda, x0, x1, tol)
        
        # Mostrar resultados
        if raiz is not None:
            decimales = abs(int(np.log10(tol))) if tol > 0 else 6
            resultado_raiz.set(f"Raíz encontrada: {round(raiz, decimales)}")
            resultado_iteraciones.set(f"Iteraciones realizadas: {num_iteraciones}")
        else:
            resultado_raiz.set("No se encontró raíz (posible división por cero o no convergió)")
        
        # Actualizar tabla y gráfica
        actualizar_tabla(tabla_iteraciones, datos_iteraciones)
        graficar_funcion(f_sympy, x0, x1, raiz, datos_iteraciones, frame_grafica)
        
    except Exception as e:
        messagebox.showerror("Error", f"Entrada inválida: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("MÉTODO DE LA SECANTE")

# Marco para datos de usuario
frame_datos = tk.LabelFrame(ventana, text="Ingresa los Datos Usuario", padx=5, pady=5)
frame_datos.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Entradas de usuario (ahora con X0 y X1)
tk.Label(frame_datos, text="Función f(x):").grid(row=0, column=0, sticky="e")
entrada_funcion = tk.Entry(frame_datos, width=30)
entrada_funcion.grid(row=0, column=1, padx=5, pady=5)
entrada_funcion.insert(0, "x**2 - 2")  # Ejemplo por defecto

tk.Label(frame_datos, text="X0:").grid(row=1, column=0, sticky="e")
entrada_x0 = tk.Entry(frame_datos)
entrada_x0.grid(row=1, column=1, padx=5, pady=5)
entrada_x0.insert(0, "1.0")

tk.Label(frame_datos, text="X1:").grid(row=2, column=0, sticky="e")
entrada_x1 = tk.Entry(frame_datos)
entrada_x1.grid(row=2, column=1, padx=5, pady=5)
entrada_x1.insert(0, "2.0")

tk.Label(frame_datos, text="Tolerancia (ej: x10^-6):").grid(row=3, column=0, sticky="e")
entrada_tolerancia = tk.Entry(frame_datos)
entrada_tolerancia.grid(row=3, column=1, padx=5, pady=5)
entrada_tolerancia.insert(0, "x10^-6")

# Botón para calcular
boton_calcular = tk.Button(frame_datos, text="CALCULAR", command=calcular_secante)
boton_calcular.grid(row=4, column=0, columnspan=2, pady=5)

# Marco para resultados
frame_resultados = tk.LabelFrame(ventana, text="Datos Generados por el Método", padx=5, pady=5)
frame_resultados.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Resultados
resultado_raiz = tk.StringVar()
resultado_iteraciones = tk.StringVar()

tk.Label(frame_resultados, textvariable=resultado_raiz).grid(row=0, column=0, sticky="w")
tk.Label(frame_resultados, textvariable=resultado_iteraciones).grid(row=1, column=0, sticky="w")

# Marco para tabla de iteraciones
frame_tabla = tk.LabelFrame(ventana, text="Tabla con los Datos Generados", padx=5, pady=5)
frame_tabla.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

tabla_iteraciones = ttk.Treeview(
    frame_tabla,
    columns=("Iteración", "Xn", "Xn+1", "f(Xn)", "f(Xn+1)", "Xn+2", "Error absoluto"),
    show="headings"
)
tabla_iteraciones.heading("Iteración", text="Iteración")
tabla_iteraciones.heading("Xn", text="Xn")
tabla_iteraciones.heading("Xn+1", text="Xn+1")
tabla_iteraciones.heading("f(Xn)", text="f(Xn)")
tabla_iteraciones.heading("f(Xn+1)", text="f(Xn+1)")
tabla_iteraciones.heading("Xn+2", text="Xn+2")
tabla_iteraciones.heading("Error absoluto", text="Error absoluto")

tabla_iteraciones.column("Iteración", width=80)
tabla_iteraciones.column("Xn", width=80)
tabla_iteraciones.column("Xn+1", width=80)
tabla_iteraciones.column("f(Xn)", width=80)
tabla_iteraciones.column("f(Xn+1)", width=80)
tabla_iteraciones.column("Xn+2", width=80)
tabla_iteraciones.column("Error absoluto", width=100)

tabla_iteraciones.pack(fill=tk.BOTH, expand=True)

# Marco para gráfica
frame_grafica_container = tk.LabelFrame(ventana, text="Gráfica de la función", padx=5, pady=5)
frame_grafica_container.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

frame_grafica = tk.Frame(frame_grafica_container)
frame_grafica.pack(fill=tk.BOTH, expand=True)

# Configurar redimensionamiento
ventana.grid_rowconfigure(2, weight=1)
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)

ventana.mainloop()