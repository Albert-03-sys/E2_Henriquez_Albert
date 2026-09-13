import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VistaPrincipal(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("🛡️ Escáner de Puertos y Servicios - TECI")
        self.geometry("900x650")
        self.configure(bg="#f4f4f4")
        
        # Principio UCD: Fuentes legibles y consistentes
        self.fuente_titulos = ("Arial", 14, "bold")
        self.fuente_normal = ("Arial", 11)

        self._crear_menu_navegacion()
        
        # Contenedor de las 3 vistas
        self.contenedor = tk.Frame(self, bg="#f4f4f4")
        self.contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inicializar las 3 Vistas
        self.frames = {}
        for F in (VistaDashboard, VistaNuevoEscaneo, VistaHistorial, VistaReglas):
            nombre_vista = F.__name__
            frame = F(parent=self.contenedor, controlador=self.controlador, vista_principal=self)
            self.frames[nombre_vista] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        
        self.mostrar_vista("VistaDashboard")

    def _crear_menu_navegacion(self):
        menu_frame = tk.Frame(self, bg="#2c3e50")
        menu_frame.pack(fill=tk.X)

        # Accesibilidad: Botones grandes y contrastantes
        btn_dash = tk.Button(menu_frame, text="📊 Dashboard", bg="#34495e", fg="white", font=self.fuente_normal, command=lambda: self.mostrar_vista("VistaDashboard"))
        btn_dash.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_scan = tk.Button(menu_frame, text="🎯 Nuevo Escaneo", bg="#34495e", fg="white", font=self.fuente_normal, command=lambda: self.mostrar_vista("VistaNuevoEscaneo"))
        btn_scan.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_hist = tk.Button(menu_frame, text="🗂️ Historial", bg="#34495e", fg="white", font=self.fuente_normal, command=lambda: self.mostrar_vista("VistaHistorial"))
        btn_hist.pack(side=tk.LEFT, padx=5, pady=5)

        btn_reglas = tk.Button(menu_frame, text="⚙️ Reglas", bg="#34495e", fg="white", font=self.fuente_normal, command=lambda: self.mostrar_vista("VistaReglas"))
        btn_reglas.pack(side=tk.LEFT, padx=5, pady=5)
            
    def mostrar_vista(self, nombre_vista):
        frame = self.frames[nombre_vista]
        if hasattr(frame, 'actualizar_datos'):
            frame.actualizar_datos() # Refresca datos al entrar a la vista
        frame.tkraise()

class VistaDashboard(tk.Frame):
    def __init__(self, parent, controlador, vista_principal):
        super().__init__(parent, bg="#f4f4f4")
        self.controlador = controlador
        
        # Aviso de uso responsable (Requisito E3)
        aviso = tk.Label(self, text="⚠️ AVISO DE USO RESPONSABLE: Esta herramienta es exclusivamente para fines académicos y de auditoría\nen redes autorizadas. Todo uso no ético o sin consentimiento está estrictamente prohibido.", 
                         fg="#c0392b", bg="#f9ebea", font=("Arial", 10, "bold"), pady=10)
        aviso.pack(fill=tk.X, pady=(0, 15))
        
        lbl_titulo = tk.Label(self, text="Resumen de Seguridad Global", font=vista_principal.fuente_titulos, bg="#f4f4f4")
        lbl_titulo.pack(pady=5)
        
        # Contenedor para gráficas integradas Matplotlib
        self.frame_graficas = tk.Frame(self, bg="#f4f4f4")
        self.frame_graficas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = None

    def actualizar_datos(self):
        # Limpiar canvas anterior
        for widget in self.frame_graficas.winfo_children():
            widget.destroy()
            
        datos_graficas = self.controlador.obtener_datos_graficas()
        
        # Crear 2 gráficas integradas (Requisito E3)
        fig = Figure(figsize=(8, 4), dpi=100)
        
        # Gráfica 1: Riesgos (Barras)
        ax1 = fig.add_subplot(121)
        riesgos = list(datos_graficas['riesgos'].keys())
        cantidades_r = list(datos_graficas['riesgos'].values())
        colores_r = ['green', 'orange', 'red']
        ax1.bar(riesgos, cantidades_r, color=colores_r)
        ax1.set_title('Puertos por Nivel de Riesgo')
        
        # Gráfica 2: Estados (Pastel)
        ax2 = fig.add_subplot(122)
        estados = list(datos_graficas['estados'].keys())
        cantidades_e = list(datos_graficas['estados'].values())
        ax2.pie(cantidades_e, labels=estados, autopct='%1.1f%%', colors=['#3498db', '#e74c3c'])
        ax2.set_title('Estado de Puertos Histórico')
        
        fig.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class VistaNuevoEscaneo(tk.Frame):
    def __init__(self, parent, controlador, vista_principal):
        super().__init__(parent, bg="#f4f4f4")
        self.controlador = controlador
        self.vp = vista_principal
        
        tk.Label(self, text="Configurar Nuevo Escaneo", font=self.vp.fuente_titulos, bg="#f4f4f4").pack(pady=20)
        
        # Formulario
        form_frame = tk.Frame(self, bg="#ffffff", bd=2, relief=tk.GROOVE, padx=30, pady=30)
        form_frame.pack()
        
        tk.Label(form_frame, text="Host / IP Objetivo:", font=self.vp.fuente_normal, bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_host = tk.Entry(form_frame, font=self.vp.fuente_normal, width=30)
        self.entry_host.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Puertos (separados por coma):", font=self.vp.fuente_normal, bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_puertos = tk.Entry(form_frame, font=self.vp.fuente_normal, width=30)
        self.entry_puertos.grid(row=1, column=1, pady=5, padx=10)
        
        # Retroalimentación visual (Errores)
        self.lbl_error = tk.Label(form_frame, text="", font=("Arial", 10), fg="red", bg="#ffffff")
        self.lbl_error.grid(row=2, column=0, columnspan=2, pady=10)
        
        btn_iniciar = tk.Button(form_frame, text="🚀 Iniciar Escaneo", bg="#27ae60", fg="white", font=self.vp.fuente_titulos, command=self.validar_y_escanear)
        btn_iniciar.grid(row=3, column=0, columnspan=2, pady=15, ipadx=20)

    def validar_y_escanear(self):
        # Validación de formulario (Requisito E3)
        host = self.entry_host.get().strip()
        puertos_str = self.entry_puertos.get().strip()
        
        self.entry_host.config(bg="white")
        self.entry_puertos.config(bg="white")
        
        if not host:
            self.lbl_error.config(text="El campo Host es obligatorio.")
            self.entry_host.config(bg="#fadbd8") # Color rojo claro
            return
            
        if not puertos_str:
            self.lbl_error.config(text="Debe ingresar al menos un puerto.")
            self.entry_puertos.config(bg="#fadbd8")
            return
            
        try:
            puertos = [int(p.strip()) for p in puertos_str.split(",")]
        except ValueError:
            self.lbl_error.config(text="Los puertos deben ser números enteros separados por coma.")
            self.entry_puertos.config(bg="#fadbd8")
            return
            
        self.lbl_error.config(text="Ejecutando escaneo...", fg="blue")
        self.update() # Forzar actualización de la UI
        
        # Llamar al controlador (Eventos separados del modelo)
        self.controlador.ejecutar_escaneo_gui(host, puertos)
        
        self.lbl_error.config(text="")
        self.entry_host.delete(0, tk.END)
        self.entry_puertos.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Escaneo finalizado correctamente.")
        self.vp.mostrar_vista("VistaHistorial")

class VistaHistorial(tk.Frame):
    def __init__(self, parent, controlador, vista_principal):
        super().__init__(parent, bg="#f4f4f4")
        self.controlador = controlador
        self.vp = vista_principal
        
        tk.Label(self, text="Historial de Escaneos", font=self.vp.fuente_titulos, bg="#f4f4f4").pack(pady=10)
        
        # Filtro (Requisito E3)
        filtro_frame = tk.Frame(self, bg="#f4f4f4")
        filtro_frame.pack(fill=tk.X, pady=5)
        tk.Label(filtro_frame, text="Filtrar por Host:", bg="#f4f4f4").pack(side=tk.LEFT)
        self.entry_filtro = tk.Entry(filtro_frame)
        self.entry_filtro.pack(side=tk.LEFT, padx=10)
        self.entry_filtro.bind("<KeyRelease>", self.filtrar_tabla)
        
        # Tabla Treeview
        columnas = ("id", "host", "fecha", "total_puertos")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        self.tabla.heading("id", text="ID")
        self.tabla.heading("host", text="Host / IP")
        self.tabla.heading("fecha", text="Fecha de Inicio")
        self.tabla.heading("total_puertos", text="Puertos Escaneados")
        
        self.tabla.column("id", width=50, anchor=tk.CENTER)
        self.tabla.column("total_puertos", width=120, anchor=tk.CENTER)
        
        self.tabla.pack(fill=tk.BOTH, expand=True)

    def actualizar_datos(self, filtro=""):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        escaneos = self.controlador.obtener_historial()
        for esc in escaneos:
            if filtro.lower() in esc['host'].lower():
                self.tabla.insert("", tk.END, values=(
                    esc['id'], esc['host'], esc['inicio'], esc['total_puertos']
                ))

    def filtrar_tabla(self, event):
        filtro = self.entry_filtro.get()
        self.actualizar_datos(filtro)

class VistaReglas(tk.Frame):
    def __init__(self, parent, controlador, vista_principal):
        super().__init__(parent, bg="#f4f4f4")
        self.controlador = controlador
        self.vp = vista_principal
        
        tk.Label(self, text="Gestión de Reglas de Riesgo (CRUD)", font=self.vp.fuente_titulos, bg="#f4f4f4").pack(pady=10)
        
        # Formulario Crear
        f_frame = tk.Frame(self)
        f_frame.pack(pady=5)
        tk.Label(f_frame, text="Tipo (Puerto/Huella):").grid(row=0, column=0)
        self.e_tipo = ttk.Combobox(f_frame, values=["Puerto", "Huella"]); self.e_tipo.grid(row=0, column=1)
        tk.Label(f_frame, text="Criterio (ej. 3306 o Apache):").grid(row=0, column=2)
        self.e_crit = tk.Entry(f_frame); self.e_crit.grid(row=0, column=3)
        tk.Label(f_frame, text="Riesgo:").grid(row=0, column=4)
        self.e_riesgo = ttk.Combobox(f_frame, values=["Bajo", "Medio", "Alto"]); self.e_riesgo.grid(row=0, column=5)
        
        tk.Button(f_frame, text="Crear Regla", bg="green", fg="white", command=self.crear).grid(row=0, column=6, padx=10)
        
        # Tabla Leer/Eliminar
        columnas = ("id", "tipo", "criterio", "riesgo")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col in columnas: self.tabla.heading(col, text=col.upper())
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Button(self, text="Eliminar Seleccionada", bg="red", fg="white", command=self.eliminar).pack(pady=5)

    def actualizar_datos(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        try:
            for r in self.controlador.obtener_reglas():
                self.tabla.insert("", tk.END, values=(r['id'], r['tipo'], r['criterio'], r['nivel_riesgo']))
        except Exception as e:
            messagebox.showerror("Error DB", str(e))

    def crear(self):
        try:
            self.controlador.crear_regla(self.e_tipo.get(), self.e_crit.get(), self.e_riesgo.get())
            self.actualizar_datos()
        except Exception as e: messagebox.showerror("Error", str(e))

    def eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion: return
        id_regla = self.tabla.item(seleccion[0])['values'][0]
        self.controlador.eliminar_regla(id_regla)
        self.actualizar_datos()