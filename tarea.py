import numpy as np
import matplotlib.pyplot as plt

# Datos
x_puntos = [1, 2, 4, 6]
y_puntos = [2, 5, 17, 21]

# Polinomio interpolante
P = lambda x: -0.4*x**3 + 3.8*x**2 - 5.6*x + 4.2

# Crear la gráfica
x = np.linspace(0, 7, 400)
plt.plot(x, P(x), 'b-', label='$P(x) = -0.4x^3 + 3.8x^2 - 5.6x + 4.2$')
plt.scatter(x_puntos, y_puntos, color='red', label='Puntos dados')

# Ajustes visuales
plt.title('Interpolación polinómica de Newton')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.show()