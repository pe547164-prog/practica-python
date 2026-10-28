"""
    admin     / admin123  -> Administrador (clientes, artículos, ventas, historial)
    vendedor  / venta123  -> Vendedor      (clientes y ventas)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

IVA = 0.16
ANCHO_TICKET = 52

# ----------------------------------------------------------------------------
# DATOS EN MEMORIA (generados desde el programa)
# ----------------------------------------------------------------------------
USUARIOS = {
    "admin": ("admin123", "Administrador"),
    "vendedor": ("venta123", "Vendedor"),
}

CLIENTES = {
    1: {"nombre": "Ana López", "telefono": "7711234567",
        "correo": "ana@mail.com", "direccion": "Centro, Tlahuelilpan"},
    2: {"nombre": "Carlos Pérez", "telefono": "7719876543",
        "correo": "carlos@mail.com", "direccion": "Col. Morelos, Tula"},
    3: {"nombre": "María Torres", "telefono": "7715558899",
        "correo": "maria@mail.com", "direccion": "Av. Hidalgo 45, Tezontepec"},
}

PRODUCTOS = {
    101: {"nombre": "Cuaderno profesional", "categoria": "Papelería", "precio": 45.50, "existencia": 40},
    102: {"nombre": "Pluma azul", "categoria": "Papelería", "precio": 8.00, "existencia": 120},
    103: {"nombre": "Mochila escolar", "categoria": "Accesorios", "precio": 350.00, "existencia": 15},
    104: {"nombre": "Memoria USB 32GB", "categoria": "Electrónica", "precio": 120.00, "existencia": 25},
    105: {"nombre": "Calculadora científica", "categoria": "Electrónica", "precio": 210.00, "existencia": 12},
}

VENTAS = []  # lista de diccionarios; cada venta guarda su ticket completo


# ----------------------------------------------------------------------------
# LÓGICA (independiente de la interfaz)
# ----------------------------------------------------------------------------
def siguiente_id(datos, inicio=1):
    return max(datos.keys(), default=inicio - 1) + 1


def calcular_totales(detalle):
    """Subtotal = suma de importes; IVA = subtotal * .16; Total = subtotal + IVA."""
    subtotal = round(sum(d["importe"] for d in detalle), 2)
    iva = round(subtotal * IVA, 2)
    total = round(subtotal + iva, 2)
    return subtotal, iva, total


def generar_ticket(venta):
    w = ANCHO_TICKET
    lineas = [
        "=" * w,
        "TIENDA".center(w),
        "Nota de venta".center(w),
        "=" * w,
        f"Folio   : {venta['folio']:05d}",
        f"Fecha   : {venta['fecha']}",
        f"Cliente : {venta['cliente']}",
        f"Atendió : {venta['vendedor']}",
        "-" * w,
        f"{'Producto':<22}{'Cant':>5}{'P.Unit':>11}{'Importe':>12}",
        "-" * w,
    ]
    for d in venta["detalle"]:
        lineas.append(f"{d['nombre'][:21]:<22}{d['cantidad']:>5}"
                      f"{d['precio']:>11.2f}{d['importe']:>12.2f}")
    lineas += [
        "-" * w,
        f"{'Subtotal:':>40}{venta['subtotal']:>12.2f}",
        f"{'IVA (16%):':>40}{venta['iva']:>12.2f}",
        f"{'TOTAL:':>40}{venta['total']:>12.2f}",
        "=" * w,
        "¡Gracias por su compra!".center(w),
    ]
    return "\n".join(lineas)


def mostrar_ticket(master, venta):
    win = tk.Toplevel(master)
    win.title(f"Ticket #{venta['folio']:05d}")
    win.configure(bg=FONDO)
    texto = tk.Text(win, font=("Courier New", 10), width=ANCHO_TICKET + 2,
                    height=venta["detalle"].__len__() + 18, bg="#fffef2")
    texto.insert("1.0", generar_ticket(venta))
    texto.config(state="disabled")
    texto.pack(padx=10, pady=10)
    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=(0, 10))



# ----------------------------------------------------------------------------
# COLORES (paleta roja)
# ----------------------------------------------------------------------------
ROJO, ROJO_OSC, ROJO_CLARO, FONDO = "#C0343F", "#9E2630", "#F6D5D8", "#FDF3F3"


def aplicar_colores(root):
    root.configure(bg=FONDO)
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", background=FONDO, foreground="#2A2123")
    s.configure("TButton", background=ROJO, foreground="white", borderwidth=0, padding=3)
    s.map("TButton", background=[("active", ROJO_OSC)])
    s.configure("TNotebook", background=FONDO, borderwidth=0)
    s.configure("TNotebook.Tab", background=ROJO_CLARO, foreground=ROJO_OSC, padding=(12, 5))
    s.map("TNotebook.Tab", background=[("selected", ROJO)], foreground=[("selected", "white")])
    s.configure("TLabelframe", background=FONDO, bordercolor=ROJO_CLARO)
    s.configure("TLabelframe.Label", background=FONDO, foreground=ROJO_OSC)
    s.configure("Treeview", background="white", fieldbackground="white", rowheight=24)
    s.configure("Treeview.Heading", background=ROJO, foreground="white", relief="flat")
    s.map("Treeview.Heading", background=[("active", ROJO_OSC)])
    s.map("Treeview", background=[("selected", ROJO_CLARO)], foreground=[("selected", ROJO_OSC)])
    s.configure("TCombobox", fieldbackground="white", bordercolor=ROJO_CLARO, arrowcolor=ROJO)
    s.map("TCombobox", fieldbackground=[("readonly", "white")], selectbackground=[("readonly", "white")],
          selectforeground=[("readonly", "#2A2123")])
    s.configure("TEntry", fieldbackground="white", bordercolor=ROJO_CLARO)

# ----------------------------------------------------------------------------
# INTERFAZ: INICIO DE SESIÓN
# ----------------------------------------------------------------------------
class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        aplicar_colores(self)
        self.title("Iniciar sesión - Tienda V1.0")
        self.resizable(False, False)
        self.configure(bg="#FBE3E5")
        self.resultado = None

        marco = tk.Frame(self, bg="#FBE3E5", padx=30, pady=20)
        marco.pack()
        tk.Label(marco, text="Iniciar sesión Tienda V1.0", font=("Arial", 14, "bold"),
                 bg="#ececec", width=28, pady=10).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        tk.Label(marco, text="Usuario:", bg="#FBE3E5", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", pady=5)
        tk.Label(marco, text="Contraseña:", bg="#FBE3E5", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="e", pady=5)
        self.usuario = tk.StringVar()
        self.clave = tk.StringVar()
        e1 = ttk.Entry(marco, textvariable=self.usuario, width=25)
        e2 = ttk.Entry(marco, textvariable=self.clave, show="*", width=25)
        e1.grid(row=1, column=1, padx=8)
        e2.grid(row=2, column=1, padx=8)
        ttk.Button(marco, text="Iniciar sesión", command=self.entrar).grid(row=3, column=0, columnspan=2, pady=15)
        e1.focus()
        self.bind("<Return>", lambda e: self.entrar())

    def entrar(self):
        u, c = self.usuario.get().strip(), self.clave.get()
        if u in USUARIOS and USUARIOS[u][0] == c:
            self.resultado = (u, USUARIOS[u][1])
            self.destroy()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
            self.clave.set("")


# ----------------------------------------------------------------------------
# INTERFAZ: CRUD GENÉRICO (clientes y artículos)
# ----------------------------------------------------------------------------
class CrudFrame(ttk.Frame):
    def __init__(self, master, datos, campos, puede_borrar=True, id_inicial=1):
        super().__init__(master, padding=10)
        self.datos, self.campos, self.id_inicial = datos, campos, id_inicial
        self.vars = {}

        cols = ("id",) + tuple(c[0] for c in campos)
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tabla.heading("id", text="ID")
        self.tabla.column("id", width=60, anchor="center")
        for clave, etiqueta, _ in campos:
            self.tabla.heading(clave, text=etiqueta)
            self.tabla.column(clave, width=130)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

        form = ttk.LabelFrame(self, text="Datos", padding=8)
        form.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        for i, (clave, etiqueta, _) in enumerate(campos):
            ttk.Label(form, text=etiqueta + ":").grid(row=i, column=0, sticky="w", pady=4)
            self.vars[clave] = tk.StringVar()
            ttk.Entry(form, textvariable=self.vars[clave], width=24).grid(row=i, column=1, padx=5, pady=4)

        botones = ttk.Frame(form)
        botones.grid(row=len(campos), column=0, columnspan=2, pady=10)
        ttk.Button(botones, text="Agregar", command=self.agregar).grid(row=0, column=0, padx=3)
        ttk.Button(botones, text="Editar", command=self.editar).grid(row=0, column=1, padx=3)
        if puede_borrar:
            ttk.Button(botones, text="Eliminar", command=self.eliminar).grid(row=0, column=2, padx=3)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).grid(row=0, column=3, padx=3)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.refrescar()

    # --- utilidades
    def refrescar(self):
        self.tabla.delete(*self.tabla.get_children())
        for id_, reg in sorted(self.datos.items()):
            fila = [id_]
            for clave, _, tipo in self.campos:
                fila.append(f"{reg[clave]:.2f}" if tipo is float else reg[clave])
            self.tabla.insert("", "end", iid=str(id_), values=fila)

    def limpiar(self):
        for v in self.vars.values():
            v.set("")
        self.tabla.selection_remove(self.tabla.selection())

    def seleccionar(self, _evt=None):
        sel = self.tabla.selection()
        if not sel:
            return
        reg = self.datos[int(sel[0])]
        for clave, _, tipo in self.campos:
            self.vars[clave].set(f"{reg[clave]:.2f}" if tipo is float else reg[clave])

    def leer_formulario(self):
        reg = {}
        for clave, etiqueta, tipo in self.campos:
            texto = self.vars[clave].get().strip()
            if not texto:
                raise ValueError(f"El campo '{etiqueta}' es obligatorio.")
            try:
                valor = tipo(texto)
            except ValueError:
                raise ValueError(f"'{etiqueta}' debe ser un valor numérico válido.")
            if tipo in (int, float) and valor < 0:
                raise ValueError(f"'{etiqueta}' no puede ser negativo.")
            reg[clave] = valor
        return reg

    # --- operaciones
    def agregar(self):
        try:
            reg = self.leer_formulario()
        except ValueError as e:
            return messagebox.showwarning("Datos inválidos", str(e))
        self.datos[siguiente_id(self.datos, self.id_inicial)] = reg
        self.refrescar()
        self.limpiar()

    def editar(self):
        sel = self.tabla.selection()
        if not sel:
            return messagebox.showinfo("Editar", "Seleccione un registro de la tabla.")
        try:
            reg = self.leer_formulario()
        except ValueError as e:
            return messagebox.showwarning("Datos inválidos", str(e))
        self.datos[int(sel[0])] = reg
        self.refrescar()
        self.limpiar()

    def eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            return messagebox.showinfo("Eliminar", "Seleccione un registro de la tabla.")
        if messagebox.askyesno("Confirmar", "¿Eliminar el registro seleccionado?"):
            del self.datos[int(sel[0])]
            self.refrescar()
            self.limpiar()


# ----------------------------------------------------------------------------
# INTERFAZ: VENTAS
# ----------------------------------------------------------------------------
class VentaFrame(ttk.Frame):
    def __init__(self, master, usuario):
        super().__init__(master, padding=10)
        self.usuario = usuario
        self.carrito = []

        sup = ttk.LabelFrame(self, text="Nueva venta", padding=8)
        sup.pack(fill="x")
        ttk.Label(sup, text="Cliente:").grid(row=0, column=0, sticky="w", pady=4)
        self.cb_cliente = ttk.Combobox(sup, state="readonly", width=34)
        self.cb_cliente.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)
        ttk.Label(sup, text="Código de producto:").grid(row=1, column=0, sticky="w", pady=4)
        self.cb_producto = ttk.Combobox(sup, state="readonly", width=40)
        self.cb_producto.grid(row=1, column=1, sticky="w", padx=5)
        ttk.Label(sup, text="Cantidad:").grid(row=1, column=2, padx=(15, 3))
        self.cantidad = tk.StringVar(value="1")
        ttk.Entry(sup, textvariable=self.cantidad, width=6).grid(row=1, column=3)
        ttk.Button(sup, text="Agregar al ticket", command=self.agregar).grid(row=1, column=4, padx=10)

        cols = ("codigo", "nombre", "cantidad", "precio", "importe")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c, t, a in (("codigo", "Código", 80), ("nombre", "Producto", 240),
                        ("cantidad", "Cantidad", 80), ("precio", "Precio unit.", 100),
                        ("importe", "Importe", 100)):
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=a, anchor="center" if c != "nombre" else "w")
        self.tabla.pack(fill="both", expand=True, pady=8)

        inf = ttk.Frame(self)
        inf.pack(fill="x")
        ttk.Button(inf, text="Quitar seleccionado", command=self.quitar).pack(side="left")
        ttk.Button(inf, text="Cancelar venta", command=self.cancelar).pack(side="left", padx=6)
        self.lbl_total = ttk.Label(inf, font=("Arial", 11, "bold"))
        self.lbl_total.pack(side="right")
        ttk.Button(inf, text="Finalizar venta y generar ticket", command=self.finalizar).pack(side="right", padx=15)
        self.actualizar()

    def actualizar(self):
        """Recarga los combos con los datos vigentes de clientes y productos."""
        self.cb_cliente["values"] = [f"{i} - {c['nombre']}" for i, c in sorted(CLIENTES.items())]
        self.cb_producto["values"] = [f"{i} - {p['nombre']} (${p['precio']:.2f}, existencia {p['existencia']})"
                                      for i, p in sorted(PRODUCTOS.items())]
        self._mostrar_carrito()

    def _mostrar_carrito(self):
        self.tabla.delete(*self.tabla.get_children())
        for d in self.carrito:
            self.tabla.insert("", "end", iid=str(d["codigo"]),
                              values=(d["codigo"], d["nombre"], d["cantidad"],
                                      f"{d['precio']:.2f}", f"{d['importe']:.2f}"))
        s, i, t = calcular_totales(self.carrito)
        self.lbl_total.config(text=f"Subtotal: ${s:.2f}   IVA: ${i:.2f}   TOTAL: ${t:.2f}")

    def agregar(self):
        if not self.cb_producto.get():
            return messagebox.showinfo("Venta", "Elija un producto.")
        codigo = int(self.cb_producto.get().split(" - ")[0])
        try:
            cant = int(self.cantidad.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            return messagebox.showwarning("Cantidad", "La cantidad debe ser un entero mayor que cero.")
        prod = PRODUCTOS[codigo]
        ya = next((d for d in self.carrito if d["codigo"] == codigo), None)
        if cant + (ya["cantidad"] if ya else 0) > prod["existencia"]:
            return messagebox.showwarning("Sin existencia",
                                          f"Solo hay {prod['existencia']} piezas de '{prod['nombre']}'.")
        if ya:
            ya["cantidad"] += cant
            ya["importe"] = round(ya["cantidad"] * ya["precio"], 2)
        else:
            self.carrito.append({"codigo": codigo, "nombre": prod["nombre"], "cantidad": cant,
                                 "precio": prod["precio"], "importe": round(cant * prod["precio"], 2)})
        self.cantidad.set("1")
        self._mostrar_carrito()

    def quitar(self):
        sel = self.tabla.selection()
        if sel:
            self.carrito = [d for d in self.carrito if str(d["codigo"]) != sel[0]]
            self._mostrar_carrito()

    def cancelar(self):
        self.carrito.clear()
        self._mostrar_carrito()

    def finalizar(self):
        if not self.cb_cliente.get():
            return messagebox.showinfo("Venta", "Seleccione un cliente.")
        if not self.carrito:
            return messagebox.showinfo("Venta", "El ticket no tiene productos.")
        cid = int(self.cb_cliente.get().split(" - ")[0])
        subtotal, iva, total = calcular_totales(self.carrito)
        venta = {
            "folio": siguiente_id({v["folio"]: v for v in VENTAS}),
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cliente_id": cid, "cliente": CLIENTES[cid]["nombre"],
            "vendedor": self.usuario, "detalle": [dict(d) for d in self.carrito],
            "subtotal": subtotal, "iva": iva, "total": total,
        }
        for d in self.carrito:                      # descuenta existencias
            PRODUCTOS[d["codigo"]]["existencia"] -= d["cantidad"]
        VENTAS.append(venta)
        self.carrito.clear()
        self.cb_cliente.set("")
        self.actualizar()
        mostrar_ticket(self, venta)


class HistorialFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        cols = ("folio", "fecha", "cliente", "vendedor", "total")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=14)
        for c, t, a in (("folio", "Folio", 70), ("fecha", "Fecha", 160), ("cliente", "Cliente", 200),
                        ("vendedor", "Vendedor", 110), ("total", "Total", 100)):
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=a, anchor="center")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<Double-1>", lambda e: self.ver())
        pie = ttk.Frame(self)
        pie.pack(fill="x", pady=8)
        ttk.Button(pie, text="Ver ticket", command=self.ver).pack(side="left")
        self.lbl = ttk.Label(pie, font=("Arial", 11, "bold"))
        self.lbl.pack(side="right")

    def actualizar(self):
        self.tabla.delete(*self.tabla.get_children())
        for v in VENTAS:
            self.tabla.insert("", "end", iid=str(v["folio"]),
                              values=(f"{v['folio']:05d}", v["fecha"], v["cliente"],
                                      v["vendedor"], f"{v['total']:.2f}"))
        self.lbl.config(text=f"Ventas: {len(VENTAS)}   Ingresos: ${sum(v['total'] for v in VENTAS):.2f}")

    def ver(self):
        sel = self.tabla.selection()
        if sel:
            mostrar_ticket(self, next(v for v in VENTAS if str(v["folio"]) == sel[0]))


# ----------------------------------------------------------------------------
# VENTANA PRINCIPAL
# ----------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self, usuario, rol):
        super().__init__()
        aplicar_colores(self)
        self.title(f"Tienda V1.0 - {usuario} ({rol})")
        self.geometry("960x520")
        self.cerrar_sesion = False

        barra = ttk.Frame(self, padding=(10, 6))
        barra.pack(fill="x")
        ttk.Label(barra, text=f"Usuario: {usuario}   |   Rol: {rol}", font=("Arial", 10, "bold")).pack(side="left")
        ttk.Button(barra, text="Cerrar sesión", command=self.salir).pack(side="right")

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.paginas = []

        # El Vendedor solo registra clientes y ventas; el Administrador gestiona todo.
        admin = rol == "Administrador"
        self.agregar_pagina(CrudFrame(self.nb, CLIENTES, [
            ("nombre", "Nombre", str), ("telefono", "Teléfono", str),
            ("correo", "Correo", str), ("direccion", "Dirección", str)],
            puede_borrar=admin), "Clientes")
        if admin:
            self.agregar_pagina(CrudFrame(self.nb, PRODUCTOS, [
                ("nombre", "Nombre", str), ("categoria", "Categoría", str),
                ("precio", "Precio", float), ("existencia", "Existencia", int)],
                id_inicial=101), "Artículos")
        self.agregar_pagina(VentaFrame(self.nb, usuario), "Ventas")
        if admin:
            self.agregar_pagina(HistorialFrame(self.nb), "Historial de ventas")
        self.nb.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

    def agregar_pagina(self, frame, texto):
        self.nb.add(frame, text=texto)
        self.paginas.append(frame)

    def al_cambiar_pestana(self, _evt):
        pagina = self.paginas[self.nb.index("current")]
        if hasattr(pagina, "actualizar"):
            pagina.actualizar()
        elif hasattr(pagina, "refrescar"):
            pagina.refrescar()

    def salir(self):
        self.cerrar_sesion = True
        self.destroy()


def main():
    while True:
        login = Login()
        login.mainloop()
        if not login.resultado:
            break
        app = App(*login.resultado)
        app.mainloop()
        if not app.cerrar_sesion:
            break


if __name__ == "__main__":
    main()