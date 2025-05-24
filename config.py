"""
Configuraciones de la aplicación Extractor de Código.
"""

import os

# Configuraciones de archivos
DEFAULT_EXCLUDED_FILES = [
    "package-lock.json",
    "yarn.lock", 
    "composer.lock",
    "Pipfile.lock",
    "poetry.lock",
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini"
]

DEFAULT_EXCLUDED_FOLDERS = [
    "node_modules",
    "__pycache__",
    ".git",
    ".svn",
    ".hg",
    "build",
    "dist",
    "target",
    "bin",
    "obj",
    ".vscode",
    ".idea",
    "vendor",
    ".env",
    "venv",
    "env",
    "virtualenv"
]

DEFAULT_ALLOWED_EXTENSIONS = [
    ".py",
    ".js", 
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".java",
    ".c",
    ".cpp",
    ".cc",
    ".h",
    ".hpp",
    ".cs",
    ".php",
    ".rb",
    ".go",
    ".rs",
    ".swift",
    ".kt",
    ".scala",
    ".sh",
    ".bat",
    ".ps1",
    ".sql",
    ".xml",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".md",
    ".txt",
    ".dockerfile",
    ".makefile",
    ".vue",
    ".svelte"
]

# Configuraciones de la GUI
WINDOW_TITLE = "Extractor de Código v2.0"
WINDOW_SIZE = "900x700"
WINDOW_MIN_SIZE = (800, 600)

# Colores del tema
COLORS = {
    "bg_primary": "#2b2b2b",
    "bg_secondary": "#3c3c3c", 
    "bg_accent": "#404040",
    "text_primary": "#ffffff",
    "text_secondary": "#b0b0b0",
    "accent": "#007acc",
    "accent_hover": "#005a9e",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336",
    "border": "#555555"
}

# Configuraciones de archivo de salida
DEFAULT_OUTPUT_FILENAME = "codigo_extraido.txt"
DEFAULT_LOG_FILENAME = "errores_extraccion.log"

# Configuraciones de procesamiento
MAX_FILE_SIZE_MB = 10  # Tamaño máximo de archivo individual en MB
ENCODING_DETECTION_BYTES = 8192  # Bytes a leer para detectar codificación

# Configuraciones de la aplicación
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Extractor de código para consolidar proyectos de programación"
APP_AUTHOR = "CodeExtractor"

# Rutas
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
CONFIG_DIR = os.path.join(PROJECT_DIR, "config")
LOGS_DIR = os.path.join(PROJECT_DIR, "logs")

# Crear directorios si no existen
for directory in [ASSETS_DIR, CONFIG_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)
