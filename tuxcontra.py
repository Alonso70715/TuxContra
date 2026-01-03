import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import random
import string
import pyperclip
import hashlib
import json
import os
import sys
import math
from datetime import datetime
import threading
import time

# ============================================================================
# CONFIGURACIÓN DE RUTAS PARA EL ICONO
# ============================================================================

def encontrar_icono():
    """
    Busca el icono en todas las ubicaciones posibles
    Retorna la ruta del icono encontrado o None si no se encuentra
    """
    print("\n" + "="*60)
    print("BUSCANDO ICONO PARA TUXCONTRA")
    print("="*60)
    
    # Lista completa de posibles ubicaciones (en orden de prioridad)
    posibles_rutas = []
    
    # 1. Directorio donde está este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Directorio actual de trabajo
    current_dir = os.getcwd()
    
    # Rutas principales a verificar
    directorios_base = [
        script_dir,  # Donde está el script
        current_dir,  # Directorio actual
        r"C:\TuxContra",  # Tu carpeta principal
        os.path.join(os.path.expanduser("~"), "Desktop"),  # Escritorio
        os.path.join(os.path.expanduser("~"), "Documents"),  # Documentos
    ]
    
    # Nombres posibles del icono
    nombres_icono = [
        "tuxcontra.ico",
        "icono.ico", 
        "icon.ico",
        "tux.ico",
        "password.ico",
        "lock.ico",
    ]
    
    # Subdirectorios donde buscar
    subdirectorios = [
        "",           # En la raíz
        "Icons",      # Carpeta Icons
        "icons",      # Carpeta icons (minúscula)
        "Iconos",     # Carpeta Iconos
        "iconos",     # Carpeta iconos
        "Resources",  # Carpeta Resources
        "resources",  # Carpeta resources
        "Images",     # Carpeta Images
        "images",     # Carpeta images
    ]
    
    # Generar todas las combinaciones posibles
    for base in directorios_base:
        for subdir in subdirectorios:
            for nombre in nombres_icono:
                if subdir:
                    ruta = os.path.join(base, subdir, nombre)
                else:
                    ruta = os.path.join(base, nombre)
                if ruta not in posibles_rutas:
                    posibles_rutas.append(ruta)
    
    # Agregar algunas rutas específicas basadas en tu descripción
    rutas_especificas = [
        r"C:\TuxContra\Icons\tuxcontra.ico",  # Tu ruta exacta
        r"C:\TuxContra\tuxcontra.ico",
        r"C:\TuxContra\icono.ico",
        os.path.join(script_dir, "Icons", "tuxcontra.ico"),
        os.path.join(script_dir, "tuxcontra.ico"),
        os.path.join(current_dir, "Icons", "tuxcontra.ico"),
        os.path.join(current_dir, "tuxcontra.ico"),
    ]
    
    # Combinar todas las rutas
    todas_rutas = rutas_especificas + posibles_rutas
    
    print(f"Verificando {len(todas_rutas)} ubicaciones posibles...\n")
    
    # Verificar cada ruta
    encontrados = []
    for i, ruta in enumerate(todas_rutas, 1):
        if os.path.exists(ruta):
            tamano = os.path.getsize(ruta)
            print(f"✅ [{i}] ENCONTRADO: {ruta}")
            print(f"   Tamaño: {tamano:,} bytes")
            encontrados.append(ruta)
        else:
            print(f"   [{i}] No existe: {ruta}")
    
    if encontrados:
        print(f"\n✨ Se encontraron {len(encontrados)} iconos válidos.")
        print(f"📌 Usando el primero: {encontrados[0]}")
        return encontrados[0]
    else:
        print("\n❌ No se encontró ningún icono.")
        print("💡 Sugerencias:")
        print("   1. Asegúrate de que el archivo .ico existe")
        print("   2. Verifica que el nombre sea correcto")
        print("   3. Colócalo en la misma carpeta que este script")
        print("   4. O en una carpeta llamada 'Icons' dentro de esa carpeta")
        return None

def crear_icono_simple():
    """
    Crea un icono simple si no existe uno
    """
    icono_path = os.path.join(os.path.dirname(__file__), "tuxcontra_simple.ico")
    
    if os.path.exists(icono_path):
        return icono_path
    
    try:
        # Intentar usar Pillow si está disponible
        from PIL import Image, ImageDraw
        
        print("\n🛠️ Creando icono simple...")
        
        # Crear imágenes en diferentes tamaños
        sizes = [16, 32, 48, 64, 128]
        images = []
        
        for size in sizes:
            img = Image.new('RGBA', (size, size), (44, 62, 80, 255))
            draw = ImageDraw.Draw(img)
            
            # Dibujar un candado simple
            margin = size // 4
            lock_width = size - 2 * margin
            
            # Arco del candado
            arc_top = margin
            arc_bottom = margin + lock_width // 2
            draw.arc([margin, arc_top, margin + lock_width, arc_bottom],
                    start=0, end=180, fill=(52, 152, 219, 255), width=max(1, size//16))
            
            # Cuerpo del candado
            body_top = arc_bottom
            body_bottom = size - margin
            draw.rectangle([margin, body_top, margin + lock_width, body_bottom],
                         fill=(52, 152, 219, 255))
            
            images.append(img)
        
        # Guardar como ICO
        images[0].save(icono_path, format='ICO', sizes=[(img.size[0], img.size[1]) for img in images],
                      append_images=images[1:])
        
        print(f"✅ Icono simple creado: {icono_path}")
        return icono_path
        
    except ImportError:
        print("⚠ Pillow no está instalado. Instálalo con: pip install pillow")
        return None
    except Exception as e:
        print(f"⚠ Error creando icono: {e}")
        return None

def establecer_icono_ventana(root):
    """
    Establece el icono de la ventana principal
    """
    # Primero buscar icono existente
    icono_path = encontrar_icono()
    
    if not icono_path:
        # Si no se encuentra, crear uno simple
        icono_path = crear_icono_simple()
    
    if icono_path:
        try:
            root.iconbitmap(icono_path)
            print(f"\n🎯 Icono establecido exitosamente: {icono_path}")
            return True
        except Exception as e:
            print(f"\n⚠ Error al establecer icono: {e}")
            return False
    
    print("\n⚠ No se pudo establecer ningún icono. Usando icono por defecto.")
    return False

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_app_data_dir():
    """
    Obtiene el directorio para guardar datos de la aplicación
    """
    if sys.platform.startswith('win'):
        # En Windows: AppData\Local\TuxContra
        appdata = os.getenv('LOCALAPPDATA')
        if appdata:
            app_dir = os.path.join(appdata, 'TuxContra')
            os.makedirs(app_dir, exist_ok=True)
            return app_dir
    
    # Para otros sistemas o fallback
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'TuxContra_Data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def instalar_dependencias():
    """
    Instala dependencias necesarias si no están disponibles
    """
    dependencias = ['pyperclip']
    
    for dep in dependencias:
        try:
            if dep == 'pyperclip':
                import pyperclip
            print(f"✅ {dep} ya está instalado")
        except ImportError:
            print(f"⚠ {dep} no está instalado. Instalando...")
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ {dep} instalado correctamente")
            except Exception as e:
                print(f"❌ Error instalando {dep}: {e}")
                return False
    return True

# ============================================================================
# CLASE PRINCIPAL TUXCONTRA
# ============================================================================

class TuxContra:
    def __init__(self, root):
        self.root = root
        self.root.title("TuxContra - Generador de Contraseñas Seguras")
        
        # Configuración inicial
        self.setup_window()
        
        # Variables y configuración
        self.setup_variables()
        
        # Crear interfaz
        self.create_widgets()
        
        # Generar primera contraseña
        self.generate_password()
    
    def setup_window(self):
        """Configura la ventana principal"""
        # Tamaño y posición
        self.root.geometry("900x750")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        
        # Establecer icono
        establecer_icono_ventana(self.root)
        
        # Centrar ventana
        self.center_window()
        
        # Directorio de datos
        self.data_dir = get_app_data_dir()
        print(f"📁 Directorio de datos: {self.data_dir}")
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_variables(self):
        """Configura las variables de control"""
        # Colores (gris azulado)
        self.bg_color = '#2c3e50'
        self.fg_color = '#ecf0f1'
        self.accent_color = '#3498db'
        self.secondary_color = '#34495e'
        self.button_color = '#2980b9'
        self.success_color = '#27ae60'
        self.warning_color = '#e74c3c'
        
        # Control de generación
        self.generating = False
        self.stop_generation = False
        
        # Conjunto de contraseñas generadas
        self.generated_passwords = set()
        
        # Historial
        self.password_history = []
        self.history_file = os.path.join(self.data_dir, "tuxcontra_history.json")
        self.load_history()
        
        # Fuentes
        self.font_title = ('Arial', 24, 'bold')
        self.font_subtitle = ('Arial', 14, 'italic')
        self.font_medium = ('Arial', 12)
        self.font_small = ('Arial', 10)
        self.font_mono = ('Courier New', 11)
        
        # Variables de control tkinter
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=16)
        self.entropy_var = tk.StringVar(value="Bits: --")
        self.status_var = tk.StringVar(value="Listo para generar contraseñas")
        self.progress_var = tk.IntVar(value=0)
        self.stats_var = tk.StringVar(value="Caracteres: 0 | Palabras: 0 | Líneas: 1")
        
        # Variables de caracteres
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        # Límites
        self.MIN_LENGTH = 1
        self.MAX_LENGTH = 1000
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        self.create_title_section(main_frame)
        
        # Configuración
        self.create_config_section(main_frame)
        
        # Contraseña generada
        self.create_password_section(main_frame)
        
        # Botones
        self.create_buttons_section(main_frame)
        
        # Estadísticas
        self.create_stats_section(main_frame)
        
        # Historial
        self.create_history_section(main_frame)
        
        # Barra de estado
        self.create_status_bar(main_frame)
    
    def create_title_section(self, parent):
        """Crea la sección del título"""
        title_frame = tk.Frame(parent, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título principal
        title_label = tk.Label(title_frame, text="🔐 TuxContra", 
                              font=self.font_title, bg=self.bg_color, 
                              fg=self.accent_color)
        title_label.pack(side=tk.LEFT)
        
        # Indicador de entropía
        entropy_label = tk.Label(title_frame, textvariable=self.entropy_var,
                                font=('Arial', 12, 'bold'), bg=self.bg_color,
                                fg=self.success_color)
        entropy_label.pack(side=tk.RIGHT, padx=10)
        
        # Subtítulo
        subtitle_label = tk.Label(parent, text="Generador de Contraseñas de Hasta 1000 Caracteres",
                                 font=self.font_subtitle, bg=self.bg_color, fg=self.fg_color)
        subtitle_label.pack(pady=(0, 20))
    
    def create_config_section(self, parent):
        """Crea la sección de configuración"""
        config_frame = tk.LabelFrame(parent, text=" Configuración ", 
                                    font=self.font_medium, bg=self.bg_color,
                                    fg=self.fg_color, padx=15, pady=15,
                                    relief=tk.GROOVE, bd=2)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Control de longitud
        self.create_length_control(config_frame)
        
        # Control de caracteres
        self.create_chars_control(config_frame)
    
    def create_length_control(self, parent):
        """Crea el control de longitud"""
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # Etiqueta
        tk.Label(frame, text="Longitud:", font=self.font_medium, 
                bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT, padx=(0, 10))
        
        # Slider
        self.length_slider = tk.Scale(frame, from_=self.MIN_LENGTH, to=self.MAX_LENGTH, 
                                     orient=tk.HORIZONTAL, variable=self.length_var,
                                     length=350, bg=self.secondary_color, fg=self.fg_color,
                                     highlightbackground=self.bg_color,
                                     troughcolor=self.accent_color,
                                     command=self.on_length_change,
                                     sliderlength=25)
        self.length_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Entrada numérica
        value_frame = tk.Frame(frame, bg=self.bg_color)
        value_frame.pack(side=tk.RIGHT)
        
        tk.Label(value_frame, text="Caracteres:", font=self.font_medium,
                bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT, padx=(0, 5))
        
        length_entry = tk.Entry(value_frame, textvariable=self.length_var,
                               width=5, font=self.font_medium, justify=tk.CENTER,
                               bg=self.secondary_color, fg=self.fg_color,
                               relief=tk.SUNKEN, bd=2)
        length_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón MAX
        tk.Button(value_frame, text="MAX", font=('Arial', 9, 'bold'),
                 bg=self.accent_color, fg=self.fg_color,
                 command=lambda: self.length_var.set(self.MAX_LENGTH),
                 padx=5, pady=1).pack(side=tk.LEFT)
    
    def create_chars_control(self, parent):
        """Crea el control de tipos de caracteres"""
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X)
        
        # Primera fila de checkboxes
        frame1 = tk.Frame(frame, bg=self.bg_color)
        frame1.pack(fill=tk.X, pady=(0, 5))
        
        tk.Checkbutton(frame1, text="Minúsculas (a-z)", variable=self.lower_var,
                      font=self.font_medium, bg=self.bg_color, fg=self.fg_color,
                      selectcolor=self.secondary_color,
                      command=self.generate_password).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Checkbutton(frame1, text="Mayúsculas (A-Z)", variable=self.upper_var,
                      font=self.font_medium, bg=self.bg_color, fg=self.fg_color,
                      selectcolor=self.secondary_color,
                      command=self.generate_password).pack(side=tk.LEFT, padx=(0, 20))
        
        # Segunda fila de checkboxes
        frame2 = tk.Frame(frame, bg=self.bg_color)
        frame2.pack(fill=tk.X)
        
        tk.Checkbutton(frame2, text="Números (0-9)", variable=self.digits_var,
                      font=self.font_medium, bg=self.bg_color, fg=self.fg_color,
                      selectcolor=self.secondary_color,
                      command=self.generate_password).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Checkbutton(frame2, text="Símbolos (!@#$%...)", variable=self.symbols_var,
                      font=self.font_medium, bg=self.bg_color, fg=self.fg_color,
                      selectcolor=self.secondary_color,
                      command=self.generate_password).pack(side=tk.LEFT)
        
        # Botón seleccionar todo
        tk.Button(frame, text="✓ Seleccionar Todo", font=('Arial', 10),
                 bg=self.secondary_color, fg=self.fg_color,
                 command=self.select_all_chars,
                 padx=10, pady=2).pack(side=tk.RIGHT, pady=(5, 0))
    
    def create_password_section(self, parent):
        """Crea la sección para mostrar la contraseña"""
        password_frame = tk.LabelFrame(parent, text=" Contraseña Generada ",
                                      font=self.font_medium, bg=self.bg_color,
                                      fg=self.fg_color, padx=15, pady=15,
                                      relief=tk.GROOVE, bd=2)
        password_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Área de texto con scrollbars
        text_frame = tk.Frame(password_frame, bg=self.secondary_color)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        scrollbar_y = tk.Scrollbar(text_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Widget de texto
        self.password_text = tk.Text(text_frame, wrap=tk.NONE,
                                    font=self.font_mono, bg=self.secondary_color,
                                    fg='#e74c3c', height=6,
                                    yscrollcommand=scrollbar_y.set,
                                    xscrollcommand=scrollbar_x.set,
                                    padx=10, pady=10,
                                    insertbackground=self.fg_color,
                                    selectbackground=self.accent_color)
        self.password_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.password_text.yview)
        scrollbar_x.config(command=self.password_text.xview)
        
        # Barra de progreso (oculta inicialmente)
        self.progress_bar = ttk.Progressbar(password_frame, variable=self.progress_var,
                                           maximum=100, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        self.progress_bar.pack_forget()
    
    def create_buttons_section(self, parent):
        """Crea la sección de botones"""
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botón Generar
        self.generate_btn = tk.Button(frame, text="🔄 Generar Nueva", 
                                     font=self.font_medium, bg=self.button_color,
                                     fg=self.fg_color, activebackground=self.accent_color,
                                     command=self.generate_password,
                                     padx=20, pady=10, relief=tk.RAISED, bd=3)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Copiar
        self.copy_btn = tk.Button(frame, text="📋 Copiar", 
                                 font=self.font_medium, bg=self.success_color,
                                 fg=self.fg_color, activebackground='#2ecc71',
                                 command=self.copy_to_clipboard,
                                 padx=20, pady=10, relief=tk.RAISED, bd=3)
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Cancelar (oculto inicialmente)
        self.cancel_btn = tk.Button(frame, text="⏹️ Cancelar", 
                                   font=self.font_medium, bg=self.warning_color,
                                   fg=self.fg_color, activebackground='#c0392b',
                                   command=self.cancel_generation,
                                   padx=20, pady=10, relief=tk.RAISED, bd=3)
        
        # Botón Guardar en Archivo
        tk.Button(frame, text="💾 Guardar", 
                 font=self.font_medium, bg='#9b59b6',
                 fg=self.fg_color, activebackground='#8e44ad',
                 command=self.save_to_file,
                 padx=20, pady=10, relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Limpiar Historial
        tk.Button(frame, text="🗑️ Limpiar", 
                 font=self.font_medium, bg=self.warning_color,
                 fg=self.fg_color, activebackground='#c0392b',
                 command=self.clear_history,
                 padx=20, pady=10, relief=tk.RAISED, bd=3).pack(side=tk.LEFT)
    
    def create_stats_section(self, parent):
        """Crea la sección de estadísticas"""
        frame = tk.Frame(parent, bg=self.secondary_color, padx=10, pady=5)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(frame, textvariable=self.stats_var,
                font=self.font_small, bg=self.secondary_color,
                fg=self.fg_color).pack()
    
    def create_history_section(self, parent):
        """Crea la sección de historial"""
        history_frame = tk.LabelFrame(parent, text=" Historial (Últimas 5) ",
                                     font=self.font_medium, bg=self.bg_color,
                                     fg=self.fg_color, padx=15, pady=15,
                                     relief=tk.GROOVE, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar
        history_canvas = tk.Canvas(history_frame, bg=self.secondary_color,
                                  highlightthickness=0)
        scrollbar = tk.Scrollbar(history_frame, orient=tk.VERTICAL, 
                                command=history_canvas.yview)
        self.history_inner_frame = tk.Frame(history_canvas, bg=self.secondary_color)
        
        history_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_canvas.create_window((0, 0), window=self.history_inner_frame, anchor=tk.NW)
        
        # Configurar scroll
        self.history_inner_frame.bind("<Configure>", 
            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all")))
        
        # Actualizar historial
        self.update_history_display()
    
    def create_status_bar(self, parent):
        """Crea la barra de estado"""
        frame = tk.Frame(parent, bg=self.bg_color, height=25)
        frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        frame.pack_propagate(False)
        
        tk.Label(frame, textvariable=self.status_var,
                font=self.font_small, bg=self.bg_color,
                fg='#95a5a6', anchor=tk.W).pack(fill=tk.X, padx=5, pady=5)
    
    # ========================================================================
    # MÉTODOS DE CONTROL
    # ========================================================================
    
    def select_all_chars(self):
        """Selecciona todos los tipos de caracteres"""
        self.lower_var.set(True)
        self.upper_var.set(True)
        self.digits_var.set(True)
        self.symbols_var.set(True)
        self.generate_password()
    
    def on_length_change(self, value):
        """Cuando cambia la longitud"""
        if not self.generating:
            self.generate_password()
    
    def update_stats(self, password):
        """Actualiza las estadísticas"""
        length = len(password)
        words = len([w for w in password.replace('\n', ' ').split() if len(w) > 0])
        lines = password.count('\n') + 1
        
        self.stats_var.set(f"Caracteres: {length:,} | Palabras: {words:,} | Líneas: {lines}")
    
    def calculate_entropy(self):
        """Calcula la entropía en bits"""
        charset_size = 0
        if self.lower_var.get():
            charset_size += 26
        if self.upper_var.get():
            charset_size += 26
        if self.digits_var.get():
            charset_size += 10
        if self.symbols_var.get():
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        length = self.length_var.get()
        entropy = math.log2(charset_size ** length)
        return entropy
    
    # ========================================================================
    # GENERACIÓN DE CONTRASEÑAS
    # ========================================================================
    
    def generate_password_thread(self):
        """Hilo para generar contraseñas largas"""
        length = self.length_var.get()
        
        # Caracteres disponibles
        chars = ""
        if self.lower_var.get():
            chars += string.ascii_lowercase
        if self.upper_var.get():
            chars += string.ascii_uppercase
        if self.digits_var.get():
            chars += string.digits
        if self.symbols_var.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        
        if not chars:
            self.root.after(0, lambda: self.status_var.set("⚠ Selecciona al menos un tipo de carácter"))
            return
        
        # Generar en bloques
        password_parts = []
        chunk_size = min(100, length)
        num_chunks = max(1, length // chunk_size)
        
        for chunk in range(num_chunks):
            if self.stop_generation:
                break
            
            current_chunk_size = chunk_size if chunk < num_chunks - 1 else length % chunk_size
            if current_chunk_size == 0:
                current_chunk_size = chunk_size
            
            chunk_password = ''.join(random.choice(chars) for _ in range(current_chunk_size))
            password_parts.append(chunk_password)
            
            # Actualizar progreso
            progress = ((chunk + 1) / num_chunks) * 100
            self.root.after(0, lambda p=progress: self.progress_var.set(p))
            
            time.sleep(0.01)
        
        password = ''.join(password_parts)[:length]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        self.root.after(0, self.finish_password_generation, password, password_hash)
    
    def finish_password_generation(self, password, password_hash):
        """Finaliza la generación"""
        if password_hash not in self.generated_passwords:
            self.generated_passwords.add(password_hash)
        
        # Mostrar contraseña
        self.password_text.config(state='normal')
        self.password_text.delete(1.0, tk.END)
        self.password_text.insert(1.0, password)
        self.password_text.config(state='disabled')
        
        # Actualizar estadísticas
        self.update_stats(password)
        
        # Calcular entropía
        entropy = self.calculate_entropy()
        if entropy >= 256:
            color, strength = "#27ae60", "Extremadamente Fuerte"
        elif entropy >= 128:
            color, strength = "#27ae60", "Muy Fuerte"
        elif entropy >= 64:
            color, strength = "#f39c12", "Fuerte"
        elif entropy >= 32:
            color, strength = "#e67e22", "Moderada"
        else:
            color, strength = "#e74c3c", "Débil"
        
        self.entropy_var.set(f"Bits: {entropy:.0f} ({strength})")
        
        # Actualizar estado
        length = self.length_var.get()
        if length > 500:
            self.status_var.set(f"✓ Contraseña MONSTRUOSA ({length:,} chars)")
        elif length > 100:
            self.status_var.set(f"✓ Contraseña EXTRA LARGA ({length:,} chars)")
        else:
            self.status_var.set(f"✓ Contraseña generada ({length} chars)")
        
        # Agregar al historial
        self.add_to_history(password)
        
        # Restaurar controles
        self.generating = False
        self.stop_generation = False
        self.progress_bar.pack_forget()
        self.generate_btn.config(state='normal', text="🔄 Generar Nueva")
        if self.cancel_btn.winfo_ismapped():
            self.cancel_btn.pack_forget()
        self.progress_var.set(0)
    
    def generate_password(self):
        """Inicia la generación"""
        if not (self.lower_var.get() or self.upper_var.get() or 
                self.digits_var.get() or self.symbols_var.get()):
            self.status_var.set("⚠ Selecciona al menos un tipo de carácter")
            return
        
        length = self.length_var.get()
        
        if length > 500:
            self.status_var.set("⏳ Generando contraseña MONSTRUOSA...")
        elif length > 100:
            self.status_var.set("⏳ Generando contraseña larga...")
        else:
            self.status_var.set("⏳ Generando...")
        
        # Mostrar barra de progreso
        if length > 50:
            self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Deshabilitar controles
        self.generating = True
        self.generate_btn.config(state='disabled', text="⏳ Generando...")
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Iniciar hilo
        thread = threading.Thread(target=self.generate_password_thread, daemon=True)
        thread.start()
    
    def cancel_generation(self):
        """Cancela la generación"""
        self.stop_generation = True
        self.status_var.set("⏹️ Generación cancelada")
        self.generate_btn.config(state='normal', text="🔄 Generar Nueva")
        self.cancel_btn.pack_forget()
        self.progress_bar.pack_forget()
    
    # ========================================================================
    # MANEJO DE CONTRASEÑAS
    # ========================================================================
    
    def copy_to_clipboard(self):
        """Copia la contraseña al portapapeles"""
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            try:
                pyperclip.copy(password)
                self.status_var.set("✓ Contraseña copiada")
                
                length = len(password)
                if length > 1000:
                    msg = f"¡Contraseña MONSTRUOSA copiada!\n\n{length:,} caracteres"
                elif length > 100:
                    msg = f"¡Contraseña EXTRA LARGA copiada!\n\n{length:,} caracteres"
                else:
                    msg = "Contraseña copiada al portapapeles"
                
                messagebox.showinfo("Copiado", f"{msg}\n\nPuedes pegarla con Ctrl+V")
                
            except Exception as e:
                self.status_var.set("✗ Error al copiar")
                messagebox.showerror("Error", f"No se pudo copiar:\n{e}")
        else:
            messagebox.showwarning("Advertencia", "No hay contraseña para copiar.")
    
    def save_to_file(self):
        """Guarda la contraseña en un archivo"""
        password = self.password_text.get(1.0, tk.END).strip()
        if not password:
            messagebox.showwarning("Advertencia", "No hay contraseña para guardar.")
            return
        
        default_name = f"tuxcontra_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=default_name,
            initialdir=self.data_dir
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Contraseña generada por TuxContra\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Longitud: {len(password):,} caracteres\n")
                    f.write(f"Entropía: {self.calculate_entropy():.0f} bits\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(password)
                    f.write("\n\n" + "=" * 50 + "\n")
                
                self.status_var.set(f"✓ Guardado: {os.path.basename(file_path)}")
                messagebox.showinfo("Guardado", f"Contraseña guardada en:\n{file_path}")
                
            except Exception as e:
                self.status_var.set("✗ Error al guardar")
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")
    
    # ========================================================================
    # HISTORIAL
    # ========================================================================
    
    def add_to_history(self, password):
        """Agrega al historial"""
        display_password = password
        if len(password) > 100:
            display_password = f"{password[:50]}...{password[-50:]}"
        
        entry = {
            "password": password,
            "display": display_password,
            "length": len(password),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "entropy": self.calculate_entropy()
        }
        
        self.password_history.insert(0, entry)
        
        # Limitar a 20 entradas
        if len(self.password_history) > 20:
            self.password_history = self.password_history[:20]
        
        self.update_history_display()
        self.save_history()
    
    def update_history_display(self):
        """Actualiza el historial en pantalla"""
        # Limpiar
        for widget in self.history_inner_frame.winfo_children():
            widget.destroy()
        
        if not self.password_history:
            tk.Label(self.history_inner_frame, 
                    text="No hay historial aún.\nGenera algunas contraseñas primero.",
                    font=self.font_medium, bg=self.secondary_color,
                    fg='#95a5a6', pady=20).pack()
            return
        
        # Mostrar últimas 5
        for i, entry in enumerate(self.password_history[:5]):
            frame = tk.Frame(self.history_inner_frame, bg=self.secondary_color)
            frame.pack(fill=tk.X, pady=3, padx=5)
            
            # Fecha/hora
            time_frame = tk.Frame(frame, bg=self.secondary_color)
            time_frame.pack(side=tk.LEFT, fill=tk.Y)
            
            tk.Label(time_frame, text=f"{entry['date']}",
                    font=('Arial', 8), bg=self.secondary_color,
                    fg='#95a5a6').pack()
            
            tk.Label(time_frame, text=f"{entry['timestamp']}",
                    font=('Arial', 10, 'bold'), bg=self.secondary_color,
                    fg=self.fg_color).pack()
            
            # Contraseña
            pwd_frame = tk.Frame(frame, bg=self.secondary_color)
            pwd_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            pwd_text = tk.Text(pwd_frame, height=2, wrap=tk.WORD,
                              font=('Courier New', 9), bg=self.secondary_color,
                              fg=self.fg_color, relief=tk.FLAT, bd=0)
            pwd_text.insert(1.0, entry['display'])
            pwd_text.config(state='disabled')
            pwd_text.pack(fill=tk.X)
            
            # Información y botón
            info_frame = tk.Frame(frame, bg=self.secondary_color)
            info_frame.pack(side=tk.RIGHT, fill=tk.Y)
            
            tk.Label(info_frame, text=f"{entry['length']:,} chars\n{entry['entropy']:.0f} bits",
                    font=('Arial', 9), bg=self.secondary_color,
                    fg=self.accent_color, justify=tk.RIGHT).pack(pady=2)
            
            tk.Button(info_frame, text="📋 Copiar", font=('Arial', 8),
                     bg=self.button_color, fg=self.fg_color,
                     command=lambda p=entry['password']: self.copy_from_history(p),
                     relief=tk.RAISED, bd=1, padx=5, pady=1).pack()
    
    def copy_from_history(self, password):
        """Copia una contraseña del historial"""
        try:
            pyperclip.copy(password)
            self.status_var.set(f"✓ Copiada del historial ({len(password):,} chars)")
            
            # Mostrar en área principal
            self.password_text.config(state='normal')
            self.password_text.delete(1.0, tk.END)
            self.password_text.insert(1.0, password)
            self.password_text.config(state='disabled')
            self.update_stats(password)
            
        except Exception as e:
            self.status_var.set("✗ Error al copiar del historial")
    
    def save_history(self):
        """Guarda el historial en archivo"""
        try:
            filtered_history = []
            for entry in self.password_history:
                filtered_entry = entry.copy()
                if len(entry['password']) > 500:
                    filtered_entry['password'] = "[CONTRASEÑA DEMASIADO LARGA]"
                filtered_history.append(filtered_entry)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_history, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def load_history(self):
        """Carga el historial desde archivo"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.password_history = json.load(f)
                
                for entry in self.password_history:
                    if 'entropy' not in entry:
                        entry['entropy'] = 0
                
                print(f"✓ Historial cargado: {len(self.password_history)} entradas")
        except Exception as e:
            print(f"Error cargando historial: {e}")
            self.password_history = []
    
    def clear_history(self):
        """Limpia el historial"""
        if not self.password_history:
            messagebox.showinfo("Historial", "El historial ya está vacío.")
            return
        
        if messagebox.askyesno("Confirmar", 
            f"¿Eliminar {len(self.password_history)} contraseñas del historial?"):
            
            self.password_history = []
            self.generated_passwords.clear()
            self.update_history_display()
            self.save_history()
            self.status_var.set("✓ Historial limpiado")
            
            messagebox.showinfo("Historial", "Historial limpiado correctamente.")

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    print("\n" + "="*60)
    print("INICIANDO TUXCONTRA")
    print("="*60)
    
    # Instalar dependencias
    if not instalar_dependencias():
        print("⚠ Algunas dependencias no se pudieron instalar")
        print("⚠ Algunas funciones pueden no estar disponibles")
    
    # Crear ventana
    root = tk.Tk()
    
    # Configurar aplicación
    app = TuxContra(root)
    
    # Configurar cierre
    def on_closing():
        if app.generating:
            if messagebox.askyesno("Generación en curso", 
                                  "Hay una generación en curso. ¿Cancelar y salir?"):
                app.stop_generation = True
                time.sleep(0.5)
        app.save_history()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Atajos de teclado
    root.bind('<Control-g>', lambda e: app.generate_password())
    root.bind('<Control-c>', lambda e: app.copy_to_clipboard())
    root.bind('<Control-s>', lambda e: app.save_to_file())
    root.bind('<Escape>', lambda e: app.cancel_generation() if app.generating else None)
    
    # Iniciar
    print("\n✅ Aplicación lista")
    print("="*60)
    root.mainloop()

if __name__ == "__main__":
    main()