"""
Interfaz gráfica principal del Extractor de Código.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import threading
from pathlib import Path

from core.file_extractor import FileExtractor
from gui.components import ModernButton, ModernFrame, ProgressDialog, ConfigDialog
from config import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_MIN_SIZE, COLORS,
    DEFAULT_OUTPUT_FILENAME, DEFAULT_LOG_FILENAME
)

class CodeExtractorGUI:
    """Interfaz gráfica principal de la aplicación."""
    
    def __init__(self):
        # Inicializar la ventana principal con soporte para drag & drop
        self.root = TkinterDnD.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*WINDOW_MIN_SIZE)
        self.root.configure(bg=COLORS["bg_primary"])
        
        self.extractor = FileExtractor()
        self.current_source_path = ""
        self.current_output_path = ""
        self.extraction_thread = None
        self.progress_dialog = None
        
        self.setup_window()
        self.create_widgets()
        self.setup_drag_drop()
    
    def setup_window(self):
        """Configura la ventana principal."""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*WINDOW_MIN_SIZE)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar color de fondo
        self.root.configure(bg=COLORS["bg_primary"])
        
        # Icono de la ventana (opcional)
        try:
            # Si tienes un archivo de icono, descomenta la siguiente línea
            # self.root.iconbitmap('assets/icon.ico')
            pass
        except:
            pass
    
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    # Eliminado: setup_styles. Todos los estilos ahora se aplican directamente con customtkinter y los componentes ModernButton/ModernFrame.
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal moderno
        main_frame = ModernFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Extractor de Código", font=ctk.CTkFont(size=22, weight="bold"), text_color=COLORS["text_primary"])
        title_label.pack(pady=(0, 5))

        subtitle_label = ctk.CTkLabel(main_frame, text="Consolida todo el código de tu proyecto en un archivo de texto", font=ctk.CTkFont(size=13), text_color=COLORS["text_secondary"])
        subtitle_label.pack(pady=(0, 20))

        # Zona de drag & drop
        self.create_drag_drop_zone(main_frame)
        # Sección de configuración
        self.create_config_section(main_frame)
        # Sección de salida
        self.create_output_section(main_frame)
        # Botones de acción
        self.create_action_buttons(main_frame)
        # Barra de estado
        self.create_status_bar(main_frame)

    # --- PARTE 2 ---
    def create_drag_drop_zone(self, parent):
        """Crea la zona de drag & drop."""
        # Frame contenedor
        drop_frame = ModernFrame(parent)
        drop_frame.pack(fill="x", pady=(0, 15))

        # Zona de drop
        self.drop_zone = ModernFrame(drop_frame, fg_color=COLORS["bg_accent"])
        self.drop_zone.pack(fill="x", pady=5)

        # Etiqueta de la zona de drop
        self.drop_label = ctk.CTkLabel(
            self.drop_zone,
            text="📁 Arrastra una carpeta aquí o haz clic para buscar",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_secondary"],
            anchor="center"
        )
        self.drop_label.pack(expand=True, fill="both")

        # Hacer la zona clickeable
        self.drop_zone.bind("<Button-1>", self.select_folder)
        self.drop_label.bind("<Button-1>", self.select_folder)

        # Efectos hover
        self.drop_zone.bind("<Enter>", self.on_drop_zone_enter)
        self.drop_zone.bind("<Leave>", self.on_drop_zone_leave)

        # Mostrar carpeta seleccionada
        self.source_path_label = ctk.CTkLabel(
            drop_frame,
            text="Ninguna carpeta seleccionada",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"]
        )
        self.source_path_label.pack(fill="x", pady=(10, 0))
    
    def create_config_section(self, parent):
        """Crea la sección de configuración."""
        config_frame = ModernFrame(parent)
        config_frame.pack(fill="x", pady=(0, 15))

        # Frame para botones de configuración
        buttons_frame = ModernFrame(config_frame, fg_color=COLORS["bg_primary"])
        buttons_frame.pack(fill="x")

        # Botón de configuración avanzada
        self.config_button = ModernButton(
            buttons_frame,
            text="⚙️ Configurar Extensiones y Exclusiones",
            command=self.open_config_dialog
        )
        self.config_button.pack(side="left", padx=(0, 10))

        # Botón de vista previa
        self.preview_button = ModernButton(
            buttons_frame,
            text="👁️ Vista Previa",
            command=self.show_preview,
            state="disabled"
        )
        self.preview_button.pack(side="left")
    
    def create_output_section(self, parent):
        """Crea la sección de archivo de salida."""
        output_frame = ModernFrame(parent)
        output_frame.pack(fill="x", pady=(0, 15))

        # Frame para ruta de salida
        path_frame = ModernFrame(output_frame, fg_color=COLORS["bg_primary"])
        path_frame.pack(fill="x", pady=(0, 10))

        # Entry para ruta de salida
        self.output_entry = ctk.CTkEntry(path_frame, font=ctk.CTkFont(size=11), width=350)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.output_entry.insert(0, DEFAULT_OUTPUT_FILENAME)

        # Botón para seleccionar ubicación
        self.browse_button = ModernButton(
            path_frame,
            text="📂 Buscar",
            command=self.select_output_file
        )
        self.browse_button.pack(side="right")
    
    def create_action_buttons(self, parent):
        """Crea los botones de acción principales."""
        action_frame = ModernFrame(parent, fg_color=COLORS["bg_primary"])
        action_frame.pack(fill="x", pady=15)

        # Botón de extracción
        self.extract_button = ModernButton(
            action_frame,
            text="🚀 Extraer Código",
            command=self.start_extraction,
            state="disabled",
            primary=True
        )
        self.extract_button.pack(side="right", padx=(10, 0))

        # Botón de limpiar
        self.clear_button = ModernButton(
            action_frame,
            text="🗑️ Limpiar",
            command=self.clear_selection
        )
        self.clear_button.pack(side="right")
    
    def create_status_bar(self, parent):
        """Crea la barra de estado."""
        status_frame = ModernFrame(parent, fg_color=COLORS["bg_secondary"])
        status_frame.pack(fill="x", side="bottom")

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Listo para extraer código",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_secondary"]
        )
        self.status_label.pack(side="left", pady=5)
    
    def setup_drag_drop(self):
        """Configura la funcionalidad de drag & drop."""
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.on_drop)
        
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """Maneja el evento de soltar archivos."""
        files = self.root.tk.splitlist(event.data)
        if files:
            path = files[0]
            if os.path.isdir(path):
                self.set_source_path(path)
            else:
                messagebox.showwarning("Advertencia", 
                                     "Por favor, selecciona una carpeta, no un archivo.")
    
    def on_drop_zone_enter(self, event):
        """Efecto hover al entrar en la zona de drop."""
        self.drop_zone.configure(style='DropZone.TFrame')
        self.drop_label.configure(foreground=COLORS["text_primary"])
    
    def on_drop_zone_leave(self, event):
        """Efecto hover al salir de la zona de drop."""
        self.drop_label.configure(foreground=COLORS["text_secondary"])
    
    def select_folder(self, event=None):
        """Abre el diálogo para seleccionar carpeta."""
        folder = filedialog.askdirectory(title="Seleccionar carpeta del proyecto")
        if folder:
            self.set_source_path(folder)
    
    def set_source_path(self, path):
        """Establece la carpeta de origen."""
        self.current_source_path = path
        
        # Mostrar ruta truncada si es muy larga
        display_path = path
        if len(display_path) > 80:
            display_path = "..." + display_path[-77:]
        
        self.source_path_label.configure(text=f"📁 {display_path}")
        self.drop_label.configure(text=f"✓ Carpeta seleccionada: {os.path.basename(path)}")
        
        # Habilitar botones
        self.extract_button.configure(state='normal')
        self.preview_button.configure(state='normal')
        
        # Actualizar estado
        self.update_status("Carpeta seleccionada. Listo para extraer.")
    
    def select_output_file(self):
        """Selecciona el archivo de salida."""
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo de código extraído",
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ],
            initialfile=DEFAULT_OUTPUT_FILENAME
        )
        
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
    
    def open_config_dialog(self):
        """Abre el diálogo de configuración."""
        dialog = ConfigDialog(self.root, self.extractor)
        self.root.wait_window(dialog.dialog)
    
    def show_preview(self):
        """Muestra una vista previa de los archivos a procesar."""
        if not self.current_source_path:
            return
        
        try:
            summary = self.extractor.get_summary(self.current_source_path)
            
            preview_text = f"""
=== VISTA PREVIA ===

📁 Carpeta: {self.current_source_path}

📊 Estadísticas:
• Total de carpetas: {summary.get('total_folders', 0)}
• Total de archivos: {summary.get('total_files', 0)}
• Archivos a procesar: {summary.get('allowed_files', 0)}
• Archivos excluidos: {summary.get('excluded_files', 0)}
• Tamaño total: {self.format_size(summary.get('total_size', 0))}

📋 Extensiones encontradas:
"""
            
            for ext, count in sorted(summary.get('extensions', {}).items()):
                if ext in self.extractor.allowed_extensions:
                    preview_text += f"• {ext or '(sin extensión)'}: {count} archivos ✓\n"
                else:
                    preview_text += f"• {ext or '(sin extensión)'}: {count} archivos (excluido)\n"
            
            if summary.get('largest_file'):
                preview_text += f"\n📄 Archivo más grande: {summary['largest_file']} ({self.format_size(summary['largest_size'])})"
            
            # Mostrar en ventana de diálogo
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Vista Previa - Extractor de Código")
            preview_window.geometry("600x500")
            preview_window.configure(bg=COLORS["bg_primary"])
            
            # Hacer la ventana modal
            preview_window.transient(self.root)
            preview_window.grab_set()
            
            # Centrar ventana
            preview_window.update_idletasks()
            x = (preview_window.winfo_screenwidth() // 2) - (300)
            y = (preview_window.winfo_screenheight() // 2) - (250)
            preview_window.geometry(f'+{x}+{y}')
            
            # Texto de vista previa
            text_frame = ttk.Frame(preview_window, padding=20)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            text_widget = tk.Text(text_frame, 
                                wrap=tk.WORD,
                                bg=COLORS["bg_secondary"],
                                fg=COLORS["text_primary"],
                                font=('Consolas', 10),
                                state='normal')
            
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget.insert(tk.END, preview_text)
            text_widget.configure(state='disabled')
            
            # Botón cerrar
            close_button = ModernButton(preview_window, 
                                      text="Cerrar",
                                      command=preview_window.destroy)
            close_button.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar vista previa: {str(e)}")
    
    def format_size(self, size_bytes):
        """Formatea el tamaño en bytes a una representación legible."""
        if size_bytes == 0:
            return "0 B"
        
        sizes = ['B', 'KB', 'MB', 'GB']
        i = 0
        
        while size_bytes >= 1024 and i < len(sizes) - 1:
            size_bytes /= 1024
            i += 1
        
        return f"{size_bytes:.1f} {sizes[i]}"
    
    def start_extraction(self):
        """Inicia el proceso de extracción en un hilo separado."""
        if not self.current_source_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta primero.")
            return
        
        output_path = self.output_entry.get().strip()
        if not output_path:
            messagebox.showwarning("Advertencia", "Por favor, especifica un archivo de salida.")
            return
        
        # Crear directorio de salida si no existe
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el directorio: {str(e)}")
                return
        
        # Crear diálogo de progreso
        self.progress_dialog = ProgressDialog(self.root, self.cancel_extraction)
        
        # Configurar callback de progreso
        self.extractor.set_progress_callback(self.progress_dialog.update_progress)
        
        # Iniciar extracción en hilo separado
        self.extraction_thread = threading.Thread(
            target=self.run_extraction,
            args=(self.current_source_path, output_path),
            daemon=True
        )
        self.extraction_thread.start()
        
        # Mostrar diálogo de progreso
        self.progress_dialog.show()
    
    def run_extraction(self, source_path, output_path):
        """Ejecuta la extracción en un hilo separado."""
        try:
            log_path = os.path.join(os.path.dirname(output_path), DEFAULT_LOG_FILENAME)
            
            processed_files, errors = self.extractor.extract_content(
                source_path, output_path, log_path
            )
            
            # Programar la actualización de la UI en el hilo principal
            self.root.after(0, self.extraction_completed, processed_files, errors, output_path)
            
        except Exception as e:
            self.root.after(0, self.extraction_error, str(e))
    
    def extraction_completed(self, processed_files, errors, output_path):
        """Maneja la finalización exitosa de la extracción."""
        self.progress_dialog.close()
        
        message = f"Extracción completada exitosamente!\n\n"
        message += f"📁 Archivos procesados: {processed_files}\n"
        message += f"⚠️ Errores: {len(errors)}\n"
        message += f"💾 Archivo guardado en: {output_path}"
        
        if errors:
            message += f"\n\nAlgunos archivos no pudieron procesarse. "
            message += f"Revisa el archivo de log para más detalles."
        
        messagebox.showinfo("Extracción Completada", message)
        self.update_status(f"Extracción completada. {processed_files} archivos procesados.")
    
    def extraction_error(self, error_message):
        """Maneja errores durante la extracción."""
        self.progress_dialog.close()
        messagebox.showerror("Error", f"Error durante la extracción:\n{error_message}")
        self.update_status("Error durante la extracción.")
    
    def cancel_extraction(self):
        """Cancela la extracción en curso."""
        if self.extractor:
            self.extractor.cancel_extraction()
        self.update_status("Extracción cancelada.")
    
    def clear_selection(self):
        """Limpia la selección actual."""
        self.current_source_path = ""
        self.source_path_label.configure(text="Ninguna carpeta seleccionada")
        self.drop_label.configure(text="📁 Arrastra una carpeta aquí o haz clic para buscar")
        self.extract_button.configure(state='disabled')
        self.preview_button.configure(state='disabled')
        self.update_status("Listo para extraer código")
    
    def update_status(self, message):
        """Actualiza el mensaje de estado."""
        self.status_label.configure(text=message)
        self.root.update_idletasks()
    
    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()
