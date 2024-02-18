import ply.lex as lex
import tkinter as tk
from tkinter import ttk

# Palabras reservadas
palabras_reservadas = ["for", "do", "while", "if", "else", "static", "void", "public", "lenght", "printf", "main"]
# Palabras para tipos de datos
tipos_de_datos = ["int", "string", "double", "float"]

# Tokens
tokens = [
    'RESERVADA',
    'TIPO_DATO',
    'IDENTIFICADOR',
    'SIMBOLO',
    'INCREMENTO',
    'CADENA',
    'NUMERO',
    'PUNTO',
]

# Variables de conteo globales
contador_palabras_reservadas = 0
contador_tipos_datos = 0
contador_identificadores = 0
contador_cadenas = 0
contador_simbolos = 0
contador_numeros = 0
contador_puntos = 0
contador_incrementos = 0

# Regla para palabras reservadas
@lex.TOKEN(r'\b(?:' + '|'.join(palabras_reservadas) + r')\b')
def t_RESERVADA(t):
    return t

# Regla para los tipos de datos
@lex.TOKEN(r'\b(?:' + '|'.join(tipos_de_datos) + r')\b')
def t_TIPO_DATO(t):
    return t

# Regla para símbolos
def t_SIMBOLO(t):
    r'[\(\)\{\}\[\]\"\'\,\:\;\=<>-]'
    return t

# Regla para cadenas de texto
def t_CADENA(t):
    r'\"(.*?)\"'
    t.value = t.value[1:-1]  # Elimina las comillas alrededor de la cadena
    return t

# Regla de incremento
def t_INCREMENTO(t):
    r'\+\+'
    return t

# Regla para el punto como símbolo independiente
def t_PUNTO(t):
    r'\.'
    return t

# Regla para identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'IDENTIFICADOR'
    return t

# Regla para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para manejar errores
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


# Regla para manejar espacios y tabuladores
t_ignore = ' \t'

# Regla para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 

def analizar_codigo(event=None):
    global contador_palabras_reservadas, contador_tipos_datos, contador_identificadores, contador_cadenas, contador_simbolos, contador_numeros, contador_puntos, contador_incrementos
    
    # Limpia los resultados anteriores en el Treeview
    for item in frame_resultado.get_children():
        frame_resultado.delete(item)
    codigo = entrada_texto.get("1.0", tk.END)
    entrada = codigo.split("\n")
    lexemas = []
    
    # Declaración de variables de conteo
    contador_palabras_reservadas = 0
    contador_tipos_datos = 0
    contador_identificadores = 0
    contador_cadenas = 0
    contador_simbolos = 0
    contador_numeros = 0
    contador_puntos = 0
    contador_incrementos = 0
    
    # Analiza cada línea del código y recopila los lexemas identificados.
    for i, entrada_linea in enumerate(entrada):
        analizador_lexico.input(entrada_linea)
        while True:
            token = analizador_lexico.token()
            if not token:
                break
            tipo = ""
            if token.type.startswith("RESERVADA"):
                tipo = "Palabra Reservada"
                contador_palabras_reservadas += 1
            elif token.type == "TIPO_DATO":
                tipo="Tipo de dato"
                contador_tipos_datos += 1
            elif token.type == "IDENTIFICADOR":
                tipo="Identificador"
                contador_identificadores += 1
            elif token.type == "SIMBOLO":
                tipo= "Simbolo"
                contador_simbolos += 1
            elif token.type == "NUMERO":
                tipo="Numero"
                contador_numeros += 1
            elif token.type == "PUNTO":
                tipo="Punto"
                contador_puntos += 1                                           
            elif token.type =="INCREMENTO":
                tipo="Incremento"
                contador_incrementos += 1
            elif token.type == "CADENA":
                tipo="Cadena"
                contador_cadenas += 1
            lexemas.append((i+1, token.value, tipo))  # Agregar lexema, número de línea y tipo a la lista lexemas        

    # Muestra los lexemas identificados y sus números de línea en la ventana de resultados.
    for linea, lexema, tipo in lexemas:
        # Insertar "x" en la columna correspondiente y dejar las demás vacías
        values = [""] * 15
        if tipo == "Palabra Reservada":
            values[1] = "x"
        if tipo == "Tipo de dato":
            values[2] = "x"
        if tipo == "Identificador":
            values[3] = "x"
        if tipo == "Cadena":
            values[4]= "x"
        if tipo == "Simbolo":
            values[5] = "x"
        if tipo == "Numero":
            values[6] = "x"
        if tipo == "Punto":
            values[7] = "x"                      
        if tipo == "Incremento":
            values[8] = "x"

        values[0] = lexema  # Insertar el lexema en la columna "Token"
        values[9] = linea  # Insertar el número de línea
        frame_resultado.insert("", "end", values=values)

analizador_lexico = lex.lex()

# Funcion de limpieza de ventanas
def limpiar_ventanas():
    entrada_texto.delete("1.0", tk.END)
    for widget in frame_resultado.get_children():
        frame_resultado.delete(widget)

# Ventana principal
ventana = tk.Tk()
#ventana.geometry("800x600")
ventana.title("Analizador lexico")
ventana.config(bg="#f1f1f1")

# Etiqueta y entrada para el codigo fuente
etiqueta_entrada = tk.Label(ventana, text="Ingrese el codigo:", font=("Arial", 12), bg="#f1f1f1", fg="#333333")
etiqueta_entrada.pack(pady=5)

# Ventana de entrada del codigo
entrada_texto = tk.Text(ventana, font=("Arial", 12), bg="white", fg="#333333", height=10, width=100)
entrada_texto.pack(pady=5)
entrada_texto.configure(insertbackground="#333333")

# Ventana de resultados
frame_resultado = ttk.Treeview(ventana, columns= ("Token", "Palabra Reservada", "Tipo de dato", "Identificador", "Cadena", "Simbolo", "Numero", "Punto", "Incremento", "Linea"), show="headings")
frame_resultado.heading("Token", text="Token")
frame_resultado.heading("Palabra Reservada", text="Palabra Reservada")
frame_resultado.heading("Tipo de dato", text="Tipo de dato")
frame_resultado.heading("Identificador", text="Identificador")
frame_resultado.heading("Cadena", text="Cadena")
frame_resultado.heading("Simbolo", text="Simbolo")
frame_resultado.heading("Numero", text="Numero")
frame_resultado.heading("Punto", text="Punto")
frame_resultado.heading("Incremento", text="Incremento")
frame_resultado.heading("Linea", text="Linea")
frame_resultado.pack(pady=5, fill="both", expand=True)

# Configurar redimensionamiento de columnas
for column in frame_resultado["columns"]:
    frame_resultado.column(column, anchor="center", width=1)
    frame_resultado.heading(column, text=column, anchor="center")
    
def resize_columns(event):
    width = event.width
    for column in frame_resultado["columns"]:
        frame_resultado.column(column, width=width//len(frame_resultado["columns"]))
# Asociar el evento de redimensionamiento a la ventana principal
ventana.bind("<Configure>", resize_columns)

# Etiqueta para mostrar los resultados
etiqueta_resultados = tk.Label(ventana, text="", font=("Arial", 12), bg="#f1f1f1", fg="#333333")
etiqueta_resultados.pack(pady=5)


def mostrar_totales():
    
    # Crear una nueva ventana para mostrar los totales
    ventana_totales = tk.Toplevel(ventana)
    ventana_totales.title("Totales")
    
    # Calcular las dimensiones de la ventana y la pantalla
    window_width = 400
    window_height = 300
    screen_width = ventana_totales.winfo_screenwidth()
    screen_height = ventana_totales.winfo_screenheight()

    # Calcular la posición x y y para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establecer la geometría de la ventana
    ventana_totales.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    # Treeview para mostrar los totales
    tree_totales = ttk.Treeview(ventana_totales, columns=("Tokens", "Totales"), show="headings")
    tree_totales.heading("Tokens", text="Tokens")
    tree_totales.heading("Totales", text="Totales")
    tree_totales.pack(pady=10, fill="both", expand=True)
    
    # Diccionario con los totales
    totales = {
        "Palabras reservadas": contador_palabras_reservadas,
        "Tipos de datos": contador_tipos_datos,
        "Identificadores": contador_identificadores,
        "Cadenas": contador_cadenas,
        "Símbolos": contador_simbolos,
        "Números": contador_numeros,
        "Puntos": contador_puntos,
        "Incrementos": contador_incrementos,
    }
    
    # Insertar los totales en el Treeview
    for token, total in totales.items():
        tree_totales.insert("", "end", values=(token, total))

# Contenedor para los botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

# Boton de analisis
boton_analizar = tk.Button(frame_botones, text="Analizar", font=("Arial", 12), bg="#3498db", fg="white", height=2, width=20, command=analizar_codigo)
boton_analizar.grid(row=0, column=0, padx=10)

# Boton de limpieza
boton_limpiar = tk.Button(frame_botones, text="Limpiar", font=("Arial", 12), bg="#e74c3c", fg="white", height=2, width=20, command=limpiar_ventanas)
boton_limpiar.grid(row=0, column=1, padx=10)

# Boton de totales
boton_totales = tk.Button(frame_botones, text="Totales", font=("Arial", 12), bg="#2ecc71", fg="white", height=2, width=20, command=mostrar_totales)
boton_totales.grid(row=0, column=2, padx=10)

# Calcula las dimensiones de la ventana y la pantalla
window_width = 800
window_height = 600
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Calcula la posición x y y para centrar la ventana
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Establece la geometría de la ventana
ventana.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))


ventana.mainloop()