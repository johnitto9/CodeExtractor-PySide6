<!-- README.md -->

<p align="center">
  <img src="assets/app_icon.png" alt="Code Extractor Logo" width="120" />
</p>

<h1 align="center">Code Extractor</h1>

<p align="center">
  <a href="https://github.com/johnitto9/CodeExtractor-PySide6/releases/latest">
    <img src="https://img.shields.io/github/v/release/johnitto9/CodeExtractor-PySide6?style=for-the-badge" alt="Latest Release">
  </a>
  <a href="https://github.com/johnitto9/CodeExtractor-PySide6/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/johnitto9/CodeExtractor-PySide6?style=for-the-badge" alt="License">
  </a>
  <a href="https://pypi.org/project/chardet/">
    <img src="https://img.shields.io/pypi/pyversions/chardet?style=for-the-badge" alt="Python Versions">
  </a>
  <a href="https://github.com/johnitto9/CodeExtractor-PySide6/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/johnitto9/CodeExtractor-PySide6/ci.yml?branch=main&style=for-the-badge" alt="Build Status">
  </a>
</p>

<p align="center">
  <img src="assets/banner_codext.png" alt="Code Extractor Banner" width="800" />
</p>

---

## 📋 Table of Contents

- [Features](#✨-features)  
- [Tech Stack](#🛠-tech-stack)  
- [Installation](#🚀-installation)  
- [Usage](#🎬-usage)  
- [Configuration](#⚙-configuration)  
- [Screenshots](#📸-screenshots)  
- [Contributing](#🤝-contributing)  
- [License](#📄-license)  

---

## ✨ Features

- **Drag & Drop** folders straight into the GUI  
- **Recursive scan** of your project, with customizable excludes  
- **Encoding detection** via [chardet]  
- **Real-time progress bar** and cancel button  
- **Preview summary**: total files, sizes, extensions  
- **Single consolidated `.txt`** with all your source code  
- **Cross-platform GUI**: PySide6 **and** CustomTkinter versions  

---

## 🛠 Tech Stack

| Component           | Technology                |
|---------------------|---------------------------|
| GUI                 | PySide6 / CustomTkinter   |
| File & Encoding     | Python 3.x, chardet       |
| Packaging & Testing | pytest, black, flake8     |
| OS Support          | Windows, macOS, Linux     |

---

## 🚀 Installation

```bash
git clone https://github.com/johnitto9/CodeExtractor-PySide6.git
cd CodeExtractor-PySide6
```

1. **Create a virtual environment** (optional but recommended)  
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎬 Usage

### Run the PySide6 version
```bash
python main.py
```

### Or run the CustomTkinter version
```bash
python -m gui.main_window
```

1. **Drag & drop** your project folder, or click to browse.  
2. Choose an **output file** (default: `codigo_extraido.txt`).  
3. Click **“Extract Code”** and watch the progress.

---

## ⚙ Configuration

All defaults are in [`config.py`](config.py). You can tweak:

- **Excluded files/folders**  
- **Allowed extensions**  
- **Theme colors**  
- **Max file size**  
- **Output/log filenames**  

```python
# Example: increase max file size
MAX_FILE_SIZE_MB = 20
```

---

## 📸 Screenshots

<p align="center">
  <img src="assets/sc1.png" alt="Screenshot 1" width="45%" />
  &nbsp;&nbsp;
  <img src="assets/sc2.png" alt="Screenshot 2" width="45%" />
</p>

---

## 🤝 Contributing

1. Fork the repo  
2. Create your feature branch  
   ```bash
   git checkout -b feature/YourFeature
   ```  
3. Commit your changes  
   ```bash
   git commit -m "Add awesome feature"
   ```  
4. Push to your branch  
   ```bash
   git push origin feature/YourFeature
   ```  
5. Open a Pull Request  

Please follow PEP 8 + Black style and include tests where applicable.

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ by [johnitto9](https://github.com/johnitto9)
</p>
