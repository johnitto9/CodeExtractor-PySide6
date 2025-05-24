"""
Componentes personalizados para la interfaz gráfica.
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import time
from config import COLORS

class ProgressDialog:
    """Diálogo de progreso para la extracción de archivos (CTk)."""
    def __init__(self, parent, cancel_callback=None):
        self.parent = parent
        self.cancel_callback = cancel_callback
        self.dialog = None
        self.progress_var = 0
        self.status_var = ""
        self.is_cancelled = False

    def show(self):
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Extrayendo Código...")
        self.dialog.geometry("500x200")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        x = (self.dialog.winfo_screenwidth() // 2) - (250)
        y = (self.dialog.winfo_screenheight() // 2) - (100)
        self.dialog.geometry(f'+{x}+{y}')

        # Barra de progreso
        self.progressbar = ctk.CTkProgressBar(self.dialog, width=400)
        self.progressbar.pack(pady=(40, 10))
        self.progressbar.set(0)

        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(self.dialog, text="Iniciando extracción...", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=(10, 20))

        # Botón cancelar
        cancel_button = ctk.CTkButton(self.dialog, text="Cancelar", command=self.cancel)
        cancel_button.pack(pady=(0, 10))

        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        self.dialog.wait_window()

    def update_progress(self, percent, status):
        self.progressbar.set(percent / 100)
        self.status_label.configure(text=status)
        self.dialog.update_idletasks()

    def cancel(self):
        self.is_cancelled = True
        if self.cancel_callback:
            self.cancel_callback()
        self.close()

    def close(self):
        if self.dialog:
            self.dialog.destroy()

class ConfigDialog:
    """Diálogo para configurar extensiones y exclusiones (CTk)."""
    def __init__(self, parent, extractor):
        self.parent = parent
        self.extractor = extractor
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Configuración avanzada")
        self.dialog.geometry("600x450")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        x = (self.dialog.winfo_screenwidth() // 2) - (300)
        y = (self.dialog.winfo_screenheight() // 2) - (225)
        self.dialog.geometry(f'+{x}+{y}')

        info_label = ctk.CTkLabel(self.dialog, text="(Configuración avanzada próximamente)", font=ctk.CTkFont(size=14), text_color="#888")
        info_label.pack(expand=True)

        close_button = ctk.CTkButton(self.dialog, text="Cerrar", command=self.dialog.destroy)
        close_button.pack(pady=20)

class ModernButton(ctk.CTkButton):
    """Botón con estilo moderno personalizado (CTk)."""
    def __init__(self, parent, primary=False, **kwargs):
        if primary:
            kwargs['fg_color'] = COLORS["success"]
            kwargs['hover_color'] = "#45a049"
            kwargs['text_color'] = COLORS["text_primary"]
            kwargs['font'] = ctk.CTkFont(size=12, weight="bold")
        else:
            kwargs['fg_color'] = COLORS["accent"]
            kwargs['hover_color'] = COLORS["accent_hover"]
            kwargs['text_color'] = COLORS["text_primary"]
            kwargs['font'] = ctk.CTkFont(size=11)
        super().__init__(parent, **kwargs)

class ModernFrame(ctk.CTkFrame):
    """Frame con estilo moderno (CTk)."""
    def __init__(self, parent, **kwargs):
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = COLORS["bg_secondary"]
        super().__init__(parent, **kwargs)
