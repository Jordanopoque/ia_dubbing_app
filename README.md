# 🎙️ IA Dubbing Project

Proyecto desarrollado en **Python** para la creación de un sistema de **doblaje automático de videos mediante Inteligencia Artificial**.

El sistema permite descargar un video, transcribir su contenido, traducir el diálogo, generar una nueva voz mediante IA y posteriormente integrar el audio doblado al video original, procurando conservar el audio ambiental.

## 🚀 Características

* 📥 Descarga de videos desde YouTube.
* 🎧 Extracción y procesamiento de audio.
* 🧠 Transcripción automática con Whisper.
* 🌎 Traducción del contenido.
* 🗣️ Generación de voz mediante XTTS-v2.
* 🎚️ Separación de voz y ambiente con Demucs.
* 🔄 Sincronización del audio generado.
* 🎬 Renderizado del video final con FFmpeg.
* ⚡ Soporte para aceleración mediante GPU NVIDIA/CUDA.

## 🛠️ Tecnologías

* **Python 3.10**
* **Whisper**
* **XTTS-v2**
* **Demucs**
* **PyTorch**
* **FFmpeg**
* **yt-dlp**
* **CUDA**

## 📁 Estructura

```text
IA_Dubbing_Project/
│
├── assets/
│   ├── audio/
│   └── video/
│
├── output/
│
├── src/
│   ├── dubbing/
│   ├── sync/
│   ├── translator/
│   ├── tts/
│   └── utils/
│
├── main.py
├── render_final.py
├── requirements.txt
└── README.md
```

## ⚙️ Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/IA_Dubbing_Project.git
cd IA_Dubbing_Project
```

Crear el entorno virtual:

```bash
python -m venv venv
```

Activar el entorno virtual en Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

En sistemas con GPU NVIDIA compatible con CUDA:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## ▶️ Uso

Ejecutar:

```bash
python main.py
```

El sistema solicitará la URL del video:

```text
🔗 Pega URL de YouTube:
```

A partir de ahí se inicia el procesamiento del video y se generan los archivos correspondientes.

Para ejecutar algunas etapas individualmente:

```bash
python -m src.dubbing.srt_xtts
```

```bash
python -m src.dubbing.sync_audio
```

Para generar el video final:

```bash
python render_final.py
```

## 🔄 Flujo

```text
YouTube
   ↓
Descarga
   ↓
Transcripción
   ↓
Traducción
   ↓
Generación de voz IA
   ↓
Sincronización
   ↓
Mezcla con audio ambiental
   ↓
Renderizado
   ↓
🎬 Video doblado
```

## 🚧 Estado

**En desarrollo.**

El proyecto cuenta actualmente con un pipeline funcional de procesamiento y doblaje automático. Se continúa trabajando en mejorar la sincronización, naturalidad de la voz, calidad de la traducción y preservación del audio original.

## ⚠️ Consideraciones

El uso de videos y voces de terceros debe realizarse respetando los derechos de autor, licencias y condiciones de uso correspondientes.

## 👨‍💻 Autor

**Jordan**

Proyecto personal orientado a la exploración y desarrollo de soluciones de **Inteligencia Artificial aplicada al procesamiento audiovisual**.
