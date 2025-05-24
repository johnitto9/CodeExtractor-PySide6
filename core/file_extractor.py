"""
Módulo principal para la extracción de contenido de archivos.
"""

import os
import chardet
from pathlib import Path
from typing import List, Tuple, Callable, Optional
import logging
from config import (
    DEFAULT_EXCLUDED_FILES, 
    DEFAULT_EXCLUDED_FOLDERS,
    DEFAULT_ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    ENCODING_DETECTION_BYTES
)

class FileExtractor:
    """Clase principal para extraer contenido de archivos de una carpeta."""
    
    def __init__(self):
        self.excluded_files = DEFAULT_EXCLUDED_FILES.copy()
        self.excluded_folders = DEFAULT_EXCLUDED_FOLDERS.copy()
        self.allowed_extensions = DEFAULT_ALLOWED_EXTENSIONS.copy()
        self.max_file_size = MAX_FILE_SIZE_MB * 1024 * 1024  # Convertir a bytes
        self.progress_callback: Optional[Callable] = None
        self.cancel_flag = False
        
    def set_progress_callback(self, callback: Callable):
        """Establece la función de callback para reportar progreso."""
        self.progress_callback = callback
        
    def cancel_extraction(self):
        """Cancela la extracción en curso."""
        self.cancel_flag = True
        
    def detect_encoding(self, file_path: str) -> str:
        """
        Detecta la codificación de un archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Codificación detectada o 'utf-8' como fallback
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(ENCODING_DETECTION_BYTES)
                result = chardet.detect(raw_data)
                return result['encoding'] if result['encoding'] else 'utf-8'
        except Exception:
            return 'utf-8'
    
    def is_file_allowed(self, file_path: str) -> bool:
        """
        Verifica si un archivo debe ser procesado.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            True si el archivo debe ser procesado, False en caso contrario
        """
        file_name = os.path.basename(file_path)
        
        # Verificar archivos excluidos
        if file_name in self.excluded_files:
            return False
            
        # Verificar extensión
        _, ext = os.path.splitext(file_name)
        if ext.lower() not in self.allowed_extensions:
            return False
            
        # Verificar tamaño del archivo
        try:
            if os.path.getsize(file_path) > self.max_file_size:
                return False
        except OSError:
            return False
            
        return True
    
    def is_folder_allowed(self, folder_path: str) -> bool:
        """
        Verifica si una carpeta debe ser procesada.
        
        Args:
            folder_path: Ruta de la carpeta
            
        Returns:
            True si la carpeta debe ser procesada, False en caso contrario
        """
        folder_name = os.path.basename(folder_path)
        return folder_name not in self.excluded_folders
    
    def count_files(self, source_path: str) -> int:
        """
        Cuenta el total de archivos a procesar para el progreso.
        
        Args:
            source_path: Ruta de origen
            
        Returns:
            Número total de archivos a procesar
        """
        total_files = 0
        
        for root, dirs, files in os.walk(source_path):
            # Filtrar carpetas excluidas
            dirs[:] = [d for d in dirs if self.is_folder_allowed(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_file_allowed(file_path):
                    total_files += 1
                    
        return total_files
    
    def extract_content(self, source_path: str, output_path: str, log_path: Optional[str] = None) -> Tuple[int, List[str]]:
        """
        Extrae el contenido de todos los archivos permitidos en una carpeta.
        
        Args:
            source_path: Carpeta de origen
            output_path: Archivo de salida
            log_path: Archivo de log de errores (opcional)
            
        Returns:
            Tupla con (número de archivos procesados, lista de errores)
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"La carpeta de origen no existe: {source_path}")
        
        processed_files = 0
        errors = []
        self.cancel_flag = False
        
        # Contar archivos totales para progreso
        total_files = self.count_files(source_path)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as output_file:
                # Escribir encabezado
                output_file.write(f"=== EXTRACCIÓN DE CÓDIGO ===\n")
                output_file.write(f"Carpeta origen: {source_path}\n")
                output_file.write(f"Total de archivos a procesar: {total_files}\n")
                output_file.write(f"{'='*50}\n\n")
                
                current_file = 0
                
                for root, dirs, files in os.walk(source_path):
                    if self.cancel_flag:
                        break
                        
                    # Filtrar carpetas excluidas
                    dirs[:] = [d for d in dirs if self.is_folder_allowed(os.path.join(root, d))]
                    
                    # Escribir información de la carpeta
                    relative_path = os.path.relpath(root, source_path)
                    output_file.write(f"--- Carpeta: {relative_path} ---\n")
                    
                    # Verificar si la carpeta está vacía
                    allowed_files = [f for f in files if self.is_file_allowed(os.path.join(root, f))]
                    if not allowed_files and not dirs:
                        output_file.write("(Carpeta vacía)\n\n")
                        continue
                    
                    # Procesar archivos
                    for file in files:
                        if self.cancel_flag:
                            break
                            
                        file_path = os.path.join(root, file)
                        
                        if not self.is_file_allowed(file_path):
                            continue
                            
                        current_file += 1
                        
                        # Reportar progreso
                        if self.progress_callback:
                            progress = (current_file / total_files) * 100
                            self.progress_callback(progress, f"Procesando: {file}")
                        
                        try:
                            # Detectar codificación y leer archivo
                            encoding = self.detect_encoding(file_path)
                            
                            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                                content = f.read()
                            
                            # Escribir contenido al archivo de salida
                            relative_file_path = os.path.relpath(file_path, source_path)
                            output_file.write(f"--- Inicio del archivo: {relative_file_path} ---\n")
                            output_file.write(content)
                            if not content.endswith('\n'):
                                output_file.write('\n')
                            output_file.write(f"--- Fin del archivo: {relative_file_path} ---\n\n")
                            
                            processed_files += 1
                            
                        except Exception as e:
                            error_msg = f"Error al procesar {file_path}: {str(e)}"
                            errors.append(error_msg)
                            
                            # Log del error
                            if log_path:
                                try:
                                    with open(log_path, 'a', encoding='utf-8') as log_file:
                                        log_file.write(f"[ERROR] {error_msg}\n")
                                except Exception:
                                    pass  # Si no se puede escribir el log, continuar
                
                # Escribir resumen final
                output_file.write(f"\n{'='*50}\n")
                output_file.write(f"=== RESUMEN DE EXTRACCIÓN ===\n")
                output_file.write(f"Archivos procesados exitosamente: {processed_files}\n")
                output_file.write(f"Errores encontrados: {len(errors)}\n")
                if self.cancel_flag:
                    output_file.write("NOTA: Extracción cancelada por el usuario\n")
                output_file.write(f"{'='*50}\n")
        
        except Exception as e:
            error_msg = f"Error crítico durante la extracción: {str(e)}"
            errors.append(error_msg)
            raise Exception(error_msg)
        
        return processed_files, errors
    
    def get_summary(self, source_path: str) -> dict:
        """
        Obtiene un resumen de la carpeta a procesar.
        
        Args:
            source_path: Carpeta de origen
            
        Returns:
            Diccionario con estadísticas del contenido
        """
        if not os.path.exists(source_path):
            return {}
        
        summary = {
            'total_folders': 0,
            'total_files': 0,
            'allowed_files': 0,
            'excluded_files': 0,
            'total_size': 0,
            'extensions': {},
            'largest_file': None,
            'largest_size': 0
        }
        
        for root, dirs, files in os.walk(source_path):
            summary['total_folders'] += len(dirs)
            summary['total_files'] += len(files)
            
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    file_size = os.path.getsize(file_path)
                    summary['total_size'] += file_size
                    
                    if file_size > summary['largest_size']:
                        summary['largest_size'] = file_size
                        summary['largest_file'] = os.path.relpath(file_path, source_path)
                    
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()
                    summary['extensions'][ext] = summary['extensions'].get(ext, 0) + 1
                    
                    if self.is_file_allowed(file_path):
                        summary['allowed_files'] += 1
                    else:
                        summary['excluded_files'] += 1
                        
                except OSError:
                    continue
        
        return summary
