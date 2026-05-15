from flask import Flask, request, render_template_string, jsonify, Response
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from run_pipeline import run_pipeline
import uuid
import threading
import json
from numpy import info
import yt_dlp
import time

import run_pipeline

app = Flask(__name__)
app.secret_key = "ia-dubbing-key-2024"

BASE_DIR = Path(__file__).parent
VIDEOS_DIR = BASE_DIR / "assets" / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# Variables globales para rastrear descarga
download_state = {}

ALLOWED_DOMAINS = ["youtube.com", "youtu.be", "vimeo.com"]

# ========================
# TEMPLATE HTML
# ========================




app = Flask(__name__)
app.secret_key = "ia-dubbing-key-2024"

BASE_DIR = Path(__file__).parent
VIDEOS_DIR = BASE_DIR / "assets" / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

download_state = {}

# ========================
# DOMINIOS PERMITIDOS
# ========================
ALLOWED_DOMAINS = ["youtube.com", "youtu.be", "vimeo.com"]

def is_valid_url(url):
    try:
        domain = urlparse(url).netloc.lower().replace("www.", "")
        return any(domain == d or domain.endswith("." + d) for d in ALLOWED_DOMAINS)
    except:
        return False


# ========================
# TEMPLATE (SIN CAMBIOS GRANDES)
# ========================
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Dubbing AI - Plataforma Profesional</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            color: #e2e8f0;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 48px;
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #94a3b8;
            max-width: 500px;
            margin: 0 auto;
        }
        
        .view { display: none; }
        .view.active { display: block; animation: fadeIn 0.3s ease; }
        
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .card {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 16px;
            padding: 32px;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(15, 23, 42, 0.3);
        }
        
        .input-group {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 14px 18px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 12px;
            background: rgba(15, 23, 42, 0.5);
            color: #f8fafc;
            font-size: 1rem;
            transition: all 0.2s ease;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #60a5fa;
            background: rgba(15, 23, 42, 0.8);
            box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
        }
        
        .btn {
            padding: 14px 28px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
            color: white;
            width: 100%;
            justify-content: center;
            font-size: 1.05rem;
            padding: 16px 32px;
        }
        
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(96, 165, 250, 0.3); }
        .btn-primary:active { transform: translateY(0); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .btn-secondary {
            background: rgba(148, 163, 184, 0.1);
            color: #cbd5e1;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        
        .btn-secondary:hover { background: rgba(148, 163, 184, 0.15); }
        
        .quality-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin: 24px 0;
        }
        
        .quality-btn {
            padding: 12px 16px;
            border: 2px solid rgba(148, 163, 184, 0.2);
            border-radius: 10px;
            background: rgba(15, 23, 42, 0.5);
            color: #cbd5e1;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .quality-btn:hover {
            border-color: #60a5fa;
            background: rgba(96, 165, 250, 0.1);
        }
        
        .quality-btn.selected {
            border-color: #60a5fa;
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
            color: #60a5fa;
        }
        
        .progress-container {
            margin: 32px 0;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(148, 163, 184, 0.1);
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 12px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%);
            width: 0%;
            transition: width 0.2s ease;
        }
        
        .progress-text {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            color: #94a3b8;
        }
        
        .status-message {
            padding: 14px 16px;
            border-radius: 10px;
            margin-bottom: 16px;
            font-size: 0.95rem;
        }
        
        .status-info { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }
        .status-success { background: rgba(34, 197, 94, 0.1); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.2); }
        .status-error { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }
        
        .video-list {
            margin-top: 24px;
        }
        
        .video-item {
            background: rgba(15, 23, 42, 0.5);
            padding: 16px;
            border-radius: 10px;
            border: 1px solid rgba(148, 163, 184, 0.1);
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .video-info h3 { margin-bottom: 4px; font-size: 1rem; }
        .video-info p { font-size: 0.85rem; color: #94a3b8; }
        
        .btn-small {
            padding: 8px 16px;
            font-size: 0.9rem;
        }
        
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid rgba(96, 165, 250, 0.3);
            border-top-color: #60a5fa;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading { opacity: 0.6; pointer-events: none; }
        
        .steps {
            display: flex;
            gap: 20px;
            margin: 24px 0;
            position: relative;
        }
        
        .step {
            flex: 1;
            text-align: center;
        }
        
        .step-number {
            width: 40px;
            height: 40px;
            margin: 0 auto 12px;
            border-radius: 50%;
            background: rgba(148, 163, 184, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            border: 2px solid rgba(148, 163, 184, 0.2);
        }
        
        .step.active .step-number {
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
            border-color: #60a5fa;
            color: white;
        }
        
        .step-name { font-size: 0.9rem; color: #94a3b8; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Video Dubbing AI</h1>
            <p class="subtitle">Transforma y doblaja tus videos con inteligencia artificial</p>
        </header>
        
        <!-- Vista 1: Cargar Video -->
        <div id="view-upload" class="view active">
            <div class="card">
                <div class="steps">
                    <div class="step active">
                        <div class="step-number">1</div>
                        <div class="step-name">Cargar Video</div>
                    </div>
                    <div class="step">
                        <div class="step-number">2</div>
                        <div class="step-name">Seleccionar Calidad</div>
                    </div>
                    <div class="step">
                        <div class="step-number">3</div>
                        <div class="step-name">Procesar</div>
                    </div>
                </div>
                
                <div class="input-group">
                    <input type="text" id="videoUrl" placeholder="Ingresa la URL del video (YouTube, Vimeo, etc.)" />
                    <button class="btn btn-secondary" onclick="analyzeVideo()">Analizar</button>
                </div>
                
                <p style="font-size: 0.85rem; color: #94a3b8; text-align: center;">
                    Soportamos YouTube, Vimeo, TikTok y muchas otras plataformas
                </p>
            </div>
        </div>
        
        <!-- Vista 2: Seleccionar Calidad -->
        <div id="view-quality" class="view">
            <div class="card">
                <div class="steps">
                    <div class="step">
                        <div class="step-number">1</div>
                        <div class="step-name">Cargar Video</div>
                    </div>
                    <div class="step active">
                        <div class="step-number">2</div>
                        <div class="step-name">Seleccionar Calidad</div>
                    </div>
                    <div class="step">
                        <div class="step-number">3</div>
                        <div class="step-name">Procesar</div>
                    </div>
                </div>
                
                <h2 style="margin-bottom: 12px; font-size: 1.3rem;">Selecciona la Calidad</h2>
                <p id="videoTitle" style="color: #94a3b8; margin-bottom: 24px;"></p>
                
                <div id="qualityContainer"></div>
                
                <div style="display: flex; gap: 12px; margin-top: 32px;">
                    <button class="btn btn-secondary" style="flex: 1;" onclick="goBack()">Atrás</button>
                    <button class="btn btn-primary" style="flex: 1;" id="downloadBtn" onclick="downloadVideo()">
                        Descargar Video
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Vista 3: Descargando -->
        <div id="view-downloading" class="view">
            <div class="card">
                <div class="steps">
                    <div class="step">
                        <div class="step-number">1</div>
                        <div class="step-name">Cargar Video</div>
                    </div>
                    <div class="step">
                        <div class="step-number">2</div>
                        <div class="step-name">Seleccionar Calidad</div>
                    </div>
                    <div class="step active">
                        <div class="step-number">3</div>
                        <div class="step-name">Procesar</div>
                    </div>
                </div>
                
                <h2 style="margin-bottom: 32px; font-size: 1.3rem;">
                    <span class="spinner"></span> Descargando Video
                </h2>
                
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="progress-text">
                        <span id="progressPercent">0%</span>
                        <span id="progressStatus">Iniciando...</span>
                    </div>
                </div>
                
                <div id="statusMessage"></div>
            </div>
        </div>
        
        <!-- Vista 4: Completado -->
        <div id="view-complete" class="view">
            <div class="card">
                <h2 style="color: #22c55e; margin-bottom: 24px; font-size: 1.3rem;">
                    Descarga Completada
                </h2>
                
                <div class="status-message status-success">
                    <strong>Éxito:</strong> Tu video está listo para procesar
                </div>
                
                <div class="video-list" id="readyVideosList"></div>
                
                <div style="display: flex; gap: 12px; margin-top: 32px;">
                    <button class="btn btn-secondary" style="flex: 1;" onclick="startNewDownload()">
                        Descargar Otro
                    </button>
                    <button class="btn btn-primary" style="flex: 1;" onclick="startProcessing()">
                        Iniciar Doblaje
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let selectedQuality = null;
        let currentVideoData = null;
        let currentSessionId = null;
        
        function switchView(viewId) {
            document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
            document.getElementById(viewId).classList.add("active");
        }
        
        function analyzeVideo() {
            const url = document.getElementById("videoUrl").value.trim();
            if (!url) {
                alert("Por favor ingresa una URL");
                return;
            }
            
            fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: url })
            })
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                    return;
                }
                currentVideoData = data;
                displayQualities(data.formats);
                switchView("view-quality");
            })
            .catch(e => alert("Error al analizar: " + e));
        }
        
        function displayQualities(formats) {
            const container = document.getElementById("qualityContainer");
            container.innerHTML = "";
            
            formats.forEach(fmt => {
                const btn = document.createElement("button");
                btn.className = "quality-btn";
                btn.innerHTML = fmt.quality;
                btn.onclick = () => selectQuality(fmt.format_id, btn);
                container.appendChild(btn);
            });
            
            document.getElementById("videoTitle").textContent = currentVideoData.title;
        }
        
        function selectQuality(formatId, btn) {
            document.querySelectorAll(".quality-btn").forEach(b => b.classList.remove("selected"));
            btn.classList.add("selected");
            selectedQuality = formatId;
        }
        
        function downloadVideo() {
            if (!selectedQuality) {
                alert("Selecciona una calidad");
                return;
            }
            
            switchView("view-downloading");
            const url = document.getElementById("videoUrl").value;
            
            fetch("/api/download", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url: url,
                    format_id: selectedQuality
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.session_id) {
                    currentSessionId = data.session_id;
                    monitorDownload(data.session_id);
                } else if (data.error) {
                    alert("Error: " + data.error);
                    switchView("view-upload");
                }
            });
        }
        
        function monitorDownload(sessionId) {
            const eventSource = new EventSource("/api/progress/" + sessionId);
            
            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                document.getElementById("progressFill").style.width = data.progress + "%";
                document.getElementById("progressPercent").textContent = data.progress + "%";
                document.getElementById("progressStatus").textContent = data.status || "Descargando...";
                
                if (data.completed) {
                    eventSource.close();
                    loadReadyVideos();
                    switchView("view-complete");
                }
            };
            
            eventSource.onerror = () => {
                eventSource.close();
                alert("Error en la descarga");
                switchView("view-upload");
            };
        }
        
        function loadReadyVideos() {
            fetch("/api/videos")
            .then(r => r.json())
            .then(videos => {
                const list = document.getElementById("readyVideosList");
                list.innerHTML = "";
                videos.forEach(v => {
                    const item = document.createElement("div");
                    item.className = "video-item";
                    item.innerHTML = `
                        <div class="video-info">
                            <h3>${v.name}</h3>
                            <p>${v.date} • ${v.size}</p>
                        </div>
                        <button class="btn btn-small btn-secondary">Detalles</button>
                    `;
                    list.appendChild(item);
                });
            });
        }
        
        function goBack() {
            switchView("view-upload");
            selectedQuality = null;
        }
        
        function startNewDownload() {
            document.getElementById("videoUrl").value = "";
            switchView("view-upload");
        }
        
        function startProcessing() {
    if (!currentSessionId) {
        alert("No hay sesión activa");
        return;
    }

    fetch("/api/dub", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            session_id: currentSessionId
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            alert("Doblaje iniciado: " + data.status);
        }
    });
}
    </script>
</body>
</html>
"""


# ========================
# FRONTEND
# ========================
@app.route("/")
def index():
    return render_template_string(MAIN_TEMPLATE)


# ========================
# ANALIZAR VIDEO
# ========================
@app.route("/api/analyze", methods=["POST"])
def analyze_video():
    try:
        data = request.json
        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "URL requerida"}), 400

        if not is_valid_url(url):
            return jsonify({"error": "Dominio no permitido"}), 400

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        seen = set()

        for fmt in info.get("formats", []):
            if fmt.get("vcodec") == "none":
                continue

            height = fmt.get("height") or 0

            if height >= 480:
                quality = f"{height}p"
                if quality not in seen:
                    formats.append({
                        "format_id": fmt["format_id"],
                        "quality": quality,
                        "height": height
                    })
                    seen.add(quality)

        if not formats:
            for fmt in info.get("formats", []):
                if fmt.get("vcodec") != "none":
                    label = fmt.get("format_note", "standard")
                    if label not in seen:
                        formats.append({
                            "format_id": fmt["format_id"],
                            "quality": label,
                            "height": fmt.get("height") or 0
                        })
                        seen.add(label)

        formats.sort(key=lambda x: x["height"], reverse=True)

        return jsonify({
            "title": info.get("title", "Video"),
            "formats": formats[:5]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ========================
# DESCARGA
# ========================
@app.route("/api/download", methods=["POST"])
def download_video():
    try:
        data = request.json
        url = data.get("url", "").strip()
        format_id = data.get("format_id", "")

        if not url:
            return jsonify({"error": "URL requerida"}), 400

        if not is_valid_url(url):
            return jsonify({"error": "Dominio no permitido"}), 400

        session_id = str(uuid.uuid4())

        download_state[session_id] = {
            "progress": 0,
            "status": "Iniciando...",
            "completed": False
        }

        thread = threading.Thread(
            target=_download_worker,
            args=(url, format_id, session_id)
        )
        thread.daemon = True
        thread.start()

        return jsonify({"session_id": session_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/api/dub", methods=["POST"])
def dub_video():
    try:
        data = request.json
        session_id = data.get("session_id")

        if not session_id:
            return jsonify({"error": "session_id requerido"}), 400

        if session_id not in download_state:
            return jsonify({"error": "session_id inválido"}), 400

        file_path = download_state[session_id].get("file_path")

        if not file_path:
            return jsonify({"error": "archivo no encontrado"}), 400

        print("🎬 Video a doblar:", file_path)

        # 🔥 AQUÍ LLAMAS TU PIPELINE REAL
        run_pipeline.run_pipeline(file_path)

        return jsonify({
            "status": "Doblaje iniciado",
            "file": file_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================
# WORKER YT-DLP
# ========================
def _download_worker(url, format_id, session_id):
    try:
        output_path = VIDEOS_DIR / "%(title)s.%(ext)s"

        def progress_hook(d):
            if d["status"] == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1

                progress = (downloaded / total) * 100

                download_state[session_id]["progress"] = round(progress, 2)
                download_state[session_id]["status"] = f"Descargando {round(progress,1)}%"

            elif d["status"] == "finished":
                download_state[session_id]["progress"] = 95
                download_state[session_id]["status"] = "Finalizando..."

        format_string = f"{format_id}+bestaudio/best" if format_id else "bestvideo+bestaudio/best"

        ydl_opts = {
            "format": format_string,
            "outtmpl": str(output_path),
            "merge_output_format": "mp4",
            "progress_hooks": [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            file_path = ydl.prepare_filename(info)

        download_state[session_id]["file_path"] = file_path

        download_state[session_id]["progress"] = 100
        download_state[session_id]["status"] = "Completado"
        download_state[session_id]["completed"] = True

    except Exception as e:
        download_state[session_id]["error"] = str(e)
        download_state[session_id]["status"] = f"Error: {str(e)}"
        download_state[session_id]["completed"] = True


# ========================
# PROGRESO (SSE)
# ========================
@app.route("/api/progress/<session_id>")
def progress(session_id):
    def generate():
        while True:
            state = download_state.get(session_id, {})
            yield f"data: {json.dumps(state)}\n\n"

            if state.get("completed"):
                break

            time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")


# ========================
# VIDEOS
# ========================
@app.route("/api/videos")
def videos():
    result = []

    for f in VIDEOS_DIR.glob("*"):
        if f.suffix in [".mp4", ".mkv", ".webm"]:
            size = f.stat().st_size / (1024 * 1024)
            date = datetime.fromtimestamp(f.stat().st_mtime)

            result.append({
                "name": f.stem,
                "size": f"{size:.1f} MB",
                "date": date.strftime("%d/%m/%Y %H:%M")
            })

    return jsonify(result)


# ========================
# RUN
# ========================
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
