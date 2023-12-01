import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
from scipy.integrate import odeint

# Función para cerrar la ventana
def cerrar_ventana():
    ventana.destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Runge-Kutta")
ventana.geometry("1920x1080")  # Tamaño de la ventana
ventana.configure(bg="#424242")

# Función para manejar el evento de selección de la lista desplegable
def seleccionar_valor(event):
    valor_seleccionado = entrada_metodo.get()
    
    if valor_seleccionado == "RK1":
        etiqueta_7 = tk.Label(ventana, text="Trabajando con RK1...", bg="#B3B9B8", fg="black", font=('Computer Modern', 13), width=19, height=2)
        etiqueta_7.place(x=330, y=325)
        resolver_edo(1)
    elif valor_seleccionado == "RK2":
        etiqueta_7 = tk.Label(ventana, text="Trabajando con RK2...", bg="#B3B9B8", fg="black", font=('Computer Modern', 13), width=19, height=2)
        etiqueta_7.place(x=330, y=325)
        resolver_edo(2)
    elif valor_seleccionado == "RK4":
        etiqueta_7 = tk.Label(ventana, text="Trabajando con RK4...", bg="#B3B9B8", fg="black", font=('Computer Modern', 13), width=19, height=2)
        etiqueta_7.place(x=330, y=325)
        resolver_edo(4)
# Crear una variable de control StringVar para la lista desplegable
entrada_metodo = tk.StringVar()

# Crear una lista desplegable (combobox) con cambios en color y fuente
combo = ttk.Combobox(ventana, textvariable=entrada_metodo, foreground="#4B9C89", font=("Computer Modern", 13))
combo['values'] = ('RK1', 'RK2', 'RK4')
combo.place(x=580, y=251)
combo.place(width=85, height=45)
combo.configure(justify="center")
# Configurar un valor predeterminado en la lista desplegable (opcional)
combo.set('Método')

# Configurar la función de manejo de eventos para la lista desplegable
combo.bind("<<ComboboxSelected>>", seleccionar_valor)

# Función para resolver la EDO usando el método de RK1
def runge_kutta_1(f, x0, y0, h, num_steps):
    x = [x0]
    y = [y0]
    while x[-1] < num_steps:
        x_next = x[-1] + h
        y_next = y[-1] + h * f(x[-1], y[-1])
        x.append(x_next)
        y.append(y_next)
    return x, y

def runge_kutta_2(f, x0, y0, h, num_steps):
    x = [x0]
    y = [y0]
    while x[-1] < num_steps:
        x_next = x[-1] + h
        k1 = h * f(x[-1], y[-1])
        k2 = h * f(x[-1] + h, y[-1] + k1)
        y_next = y[-1] + 0.5 * (k1 + k2)
        x.append(x_next)
        y.append(y_next)
    return x, y

def runge_kutta_4(f, x0, y0, h, num_steps):
    x = [x0]
    y = [y0]
    while x[-1] < num_steps:
        k1 = h * f(x[-1], y[-1])
        k2 = h * f(x[-1] + h/2, y[-1] + k1/2)
        k3 = h * f(x[-1] + h/2, y[-1] + k2/2)
        k4 = h * f(x[-1] + h, y[-1] + k3)
        
        x_next = x[-1] + h
        y_next = y[-1] + (k1 + 2*k2 + 2*k3 + k4)/6
        
        x.append(x_next)
        y.append(y_next)
    
    return x, y

# Función que crea una función simbólica a partir de la entrada del usuario
def crear_funcion(equation):
    x, y = sp.symbols('x y')
    # Evaluar la entrada del usuario y crear una función simbólica
    try:
        funcion = sp.sympify(equation)
        return sp.lambdify((x, y), funcion, 'numpy')
    except sp.SympifyError:
        return None
    
def resolver_edo(id):
    id_i = id
    equation = entrada_edo.get()
    x0 = float(entrada_x0.get())
    y0 = float(entraday0.get())
    num_steps = float(entrada_x.get())
    h = float(entrada_h.get())

    funcion = crear_funcion(equation)
    if funcion is not None:
        x_rk, y_rk = runge_kutta_1(funcion, x0, y0, h, num_steps)
        x_rk2, y_rk2 = runge_kutta_2(funcion, x0, y0, h, num_steps)
        x_rk4, y_rk4 = runge_kutta_4(funcion, x0, y0, h, num_steps)
        if(id_i == 1):
            def dF(y, x):
                dy = funcion(x, y)  # Evaluar la función en el punto (x, y)
                return dy
            sol = odeint(dF, y0, x_rk)  #usar los mismos valores de x que se usaron en el método de Runge-Kutta
        
            # Calcular el error entre la solución real y la de Runge-Kutta
            error = [abs((sol[i][0] - y_rk[i])) for i in range(len(sol))]
            real = [(sol[i][0]) for i in range(len(sol))]
            # Actualizar la tabla con los resultados, incluyendo la columna de error
            tabla.delete(*tabla.get_children())
            for i in range(len(x_rk)):
                tabla.insert("", "end", values=("{:.4f}".format(x_rk[i]), "{:.4f}".format(y_rk[i]), "{:.4f}".format(y_rk2[i]), "{:.4f}".format(y_rk4[i]),"{:.4f}".format(real[i]),  "{:.4f}".format(error[i])))

            # Actualizar el gráfico en la misma interfaz
            ax.clear()
            ax.plot(x_rk, y_rk, marker='o', label='RK1')
            ax.plot(x_rk, [sol[i][0] for i in range(len(sol))], color='red', label='Real')  # Trazar ambas soluciones en la misma gráfica
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Solución de la EDO')
            ax.grid()
            ax.legend()  # Mostrar leyenda
            canvas.draw()

        elif(id_i == 2):
            def dF(y, x):
                dy = funcion(x, y)  # Evaluar la función en el punto (x, y)
                return dy
            sol = odeint(dF, y0, x_rk2)  # e usar los mismos valores de x que se usaron en el método de Runge-Kutta
        
            # Calcular el error entre la solución real y la de Runge-Kutta
            error = [abs((sol[i][0] - y_rk2[i])) for i in range(len(sol))]
            real = [(sol[i][0]) for i in range(len(sol))]
            # Actualizar la tabla con los resultados, incluyendo la columna de error
            tabla.delete(*tabla.get_children())
            for i in range(len(x_rk2)):
                tabla.insert("", "end", values=("{:.4f}".format(x_rk[i]), "{:.4f}".format(y_rk[i]), "{:.4f}".format(y_rk2[i]), "{:.4f}".format(y_rk4[i]), "{:.4f}".format(real[i]),"{:.4f}".format(error[i])))

            # Actualizar el gráfico en la misma interfaz
            ax.clear()
            ax.plot(x_rk2, y_rk2, marker='o', label='RK2')
            ax.plot(x_rk2, [sol[i][0] for i in range(len(sol))], color='red', label='Real')  # Trazar ambas soluciones en la misma gráfica
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Solución de la EDO')
            ax.grid()
            ax.legend()  # Mostrar leyenda
            canvas.draw()

        elif(id_i == 4):
            def dF(y, x):
                dy = funcion(x, y)  # Evaluar la función en el punto (x, y)
                return dy
            sol = odeint(dF, y0, x_rk4)  # usar los mismos valores de x que se usaron en el método de Runge-Kutta
        
            # Calcular el error entre la solución real y la de Runge-Kutta
            error = [abs((sol[i][0] - y_rk4[i])) for i in range(len(sol))]
            real = [(sol[i][0]) for i in range(len(sol))]
            # Actualizar la tabla con los resultados, incluyendo la columna de error
            tabla.delete(*tabla.get_children())
            for i in range(len(x_rk4)):
                tabla.insert("", "end", values=("{:.4f}".format(x_rk[i]), "{:.4f}".format(y_rk[i]), "{:.4f}".format(y_rk2[i]), "{:.4f}".format(y_rk4[i]), "{:.4f}".format(y_rk4[i]),"{:.4f}".format(error[i])))

            # Actualizar el gráfico en la misma interfaz
            ax.clear()
            ax.plot(x_rk4, y_rk4, marker='o', label='RK4')
            ax.plot(x_rk4, [sol[i][0] for i in range(len(sol))], color='red', label='Real')  # Trazar ambas soluciones en la misma gráfica
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Solución de la EDO')
            ax.grid()
            ax.legend()  # Mostrar leyenda
            canvas.draw()
# Crear un gráfico dentro de la GUI
fig = Figure(figsize=(7, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack()
canvas.get_tk_widget().grid(padx=1000, pady = 200)

# Crear una tabla para mostrar los resultados
tabla = ttk.Treeview(ventana, columns=("x_n", "RK1", "RK2", "RK4", "Real", "Error"), height= 12)
tabla.heading("x_n", text="x_n")
tabla.heading("RK1", text="RK1")
tabla.heading("RK2", text="RK2")
tabla.heading("RK4", text="RK4")
tabla.heading("Real", text="Real")
tabla.heading("Error", text="Error")

# Configurar el ancho de las columnas
tabla.column("#0", width=0, stretch=tk.NO)  # Columna oculta
tabla.column("x_n", width=80, anchor="center")
tabla.column("RK1", width=120, anchor="center")
tabla.column("RK2", width=120, anchor="center")
tabla.column("RK4", width=120, anchor="center")
tabla.column("Real", width=120, anchor="center")
tabla.column("Error", width=120, anchor="center")
tabla.place(x=80, y=446)  # Ajusta las coordenadas (x, y) 
style = ttk.Style()
style.configure("Treeview", rowheight=20)  # Ajusta la altura de fila aq
style.configure("Treeview.Heading", font=('Computer Modern', 12, 'bold'), background='#76D8C0')  # Cambiar el tipo y tamaño de letra de los encabezados
style.configure("Treeview", font=('Computer Modern', 14))  # Cambiar el tipo y tamaño de letra del contenido

# Crear un botón rojo de "Cerrar"
boton_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar_ventana, bg="#FF5733", fg="white", width=11, height=2, font=('Computer Modern', 14))
boton_cerrar.place(x=1760, y=920)

# Crear una etiqueta para el texto "Ecuación diferencial ordinaria de primer orden"
etiqueta_1 = tk.Label(ventana, text="Ecuación diferencial ordinaria de primer orden", bg="#424242", fg="white", font=('Computer Modern', 20))
etiqueta_1.place(x=125, y=70)

# Etiqueta para la parte de mensaje de ingreso
etiqueta_2 = tk.Label(ventana, text="Ingresa la ecuación y' = ", bg="#76D8C0", fg="black", font=('Computer Modern', 14), width=25, height=2)
etiqueta_2.place(x=135, y=120)

# Entrada de EDO
entrada_edo = tk.StringVar()
entrada_1 = tk.Entry(ventana, textvariable=entrada_edo, font=('Computer Modern', 14), width=30)
entrada_1.place(x=417, y=120)
entrada_1.place(width=250, height=49.5)

# Etiqueta de parámetros
etiqueta_3 = tk.Label(ventana, text="Parámetros", bg="#488A7A", fg="black", font=('Computer Modern', 15, 'bold'), width=10, height=2)
etiqueta_3.place(x=345, y=196)

# Etiqueta de x_0
etiqueta_4 = tk.Label(ventana, text="x_0", bg="#76D8C0", fg="black", font=('Computer Modern', 13), width=5, height=2)
etiqueta_4.place(x=135, y=251)
# Entrada de x_0
entrada_x0 = tk.StringVar()
entrada_2 = tk.Entry(ventana, textvariable=entrada_x0, font=('Computer Modern', 13), width=30)
entrada_2.place(x=186, y=251)
entrada_2.place(width=60, height=44)

# Etiqueta de y_0
etiqueta_5 = tk.Label(ventana, text="y_0", bg="#76D8C0", fg="black", font=('Computer Modern', 13), width=5, height=2)
etiqueta_5.place(x=247, y=251)
# Entrada de y_0
entraday0 = tk.StringVar()
entrada_3 = tk.Entry(ventana, textvariable=entraday0, font=('Computer Modern', 13), width=30)
entrada_3.place(x=298, y=251)
entrada_3.place(width=60, height=44)

# Etiqueta de x
etiqueta_6 = tk.Label(ventana, text="x", bg="#76D8C0", fg="black", font=('Computer Modern', 13), width=5, height=2)
etiqueta_6.place(x=358, y=251)
# Entrada de x
entrada_x = tk.StringVar()
entrada_4 = tk.Entry(ventana, textvariable=entrada_x, font=('Computer Modern', 13), width=30)
entrada_4.place(x=408, y=251)
entrada_4.place(width=60, height=44)

# Etiqueta de h
etiqueta_7 = tk.Label(ventana, text="h", bg="#76D8C0", fg="black", font=('Computer Modern', 13), width=5, height=2)
etiqueta_7.place(x=468, y=251)
# Entrada de h
entrada_h = tk.StringVar()
entrada_5 = tk.Entry(ventana, textvariable=entrada_h, font=('Computer Modern', 13), width=30)
entrada_5.place(x=519, y=251)
entrada_5.place(width=60, height=44)

# Etiqueta de resultados
etiqueta_8 = tk.Label(ventana, text="Resultados", bg="#488A7A", fg="black", font=('Computer Modern', 15, 'bold'), width=10, height=2)
etiqueta_8.place(x=345, y=390)

# Crear una etiqueta para el texto "Ecuación diferencial ordinaria de primer orden"
etiqueta_9 = tk.Label(ventana, text="Gráfico de las soluciones", bg="#424242", fg="white", font=('Computer Modern', 20))
etiqueta_9.place(x=1200, y=140)
ventana.mainloop()
