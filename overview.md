## 10. Systemintegration für Windows und Browser

### 10.1 Windows-Systemintegration
# KI-gestütztes Assistenzsystem für Sehbehinderte: Komplette Implementierung

In diesem Dokument wird der vollständige technische Aufbau eines KI-gestützten Assistenzsystems für blinde und sehbehinderte Nutzer beschrieben. Die Architektur ist modular gestaltet und ermöglicht eine nahtlose Integration sowohl auf PC-Systemen als auch später auf Mobilgeräten.

## Inhaltsverzeichnis

1. [Systemarchitektur und Überblick](#1-systemarchitektur-und-überblick)
2. [Hardware- und Softwarevoraussetzungen](#2-hardware--und-softwarevoraussetzungen)
3. [Entwicklungsumgebung einrichten](#3-entwicklungsumgebung-einrichten)
4. [Ordnerstruktur und Komponentenorganisation](#4-ordnerstruktur-und-komponentenorganisation)
5. [Kernsystem installieren und konfigurieren](#5-kernsystem-installieren-und-konfigurieren)
6. [Event-Manager implementieren](#6-event-manager-implementieren)
7. [Sprachverarbeitung implementieren](#7-sprachverarbeitung-implementieren)
8. [Bildverarbeitung und Kamerazugriff](#8-bildverarbeitung-und-kamerazugriff)
9. [KI-Modelle einrichten](#9-ki-modelle-einrichten)
10. [Systemintegration für Windows und Browser](#10-systemintegration-für-windows-und-browser)
11. [Datenbank-Setup und Synchronisierung](#11-datenbank-setup-und-synchronisierung)
12. [KI-Agenten integrieren](#12-ki-agenten-integrieren)
13. [API-Schicht für Geräteintegration](#13-api-schicht-für-geräteintegration)
14. [UI-Komponenten](#14-ui-komponenten)
15. [Mediensteuerung](#15-mediensteuerung)
16. [Installation und Deployment](#16-installation-und-deployment)
17. [Mobile Integration](#17-mobile-integration)
18. [Erweiterungsmöglichkeiten](#18-erweiterungsmöglichkeiten)

## 1. Systemarchitektur und Überblick

Das System basiert auf einer modularen Architektur mit klaren Schnittstellen zwischen den Komponenten. Die Hauptkomponenten sind:

1. **Kern (Core)**: Zentrales System mit Konfigurationsmanagement und Event-System
2. **Nutzerinteraktionsschicht**: Verarbeitet Spracheingaben, Tastatur, Maus und gibt Feedback
3. **KI-Assistenzkern**: Zentrale Steuerungseinheit mit mehreren spezialisierten KI-Agenten
4. **Systemintegrationsschicht**: Verbindet das System mit Windows, Webbrowsern und anderen Plattformen
5. **Datenmanagement**: Lokale Datenbanken mit Synchronisierungsfunktionen für Geräteübergreifende Nutzung
6. **API-Schicht**: REST- und WebSocket-Schnittstellen für externe Zugriffe und Geräteintegration
7. **Mediensteuerung**: Kontrolle von Audio- und Videowiedergabe über verschiedene Plattformen

### Architekturdiagramm (konzeptionell)

```
+-----------------------------------------------------+
|                      KERN                           |
|   Konfiguration | Event-Manager | Logging | System  |
+-----------------------------------------------------+
                         |
+------------------------------------------+ +----------------------+
|            NUTZERINTERAKTION             | |                      |
| Speech-to-Text | Text-to-Speech | Kamera | |    API-SCHICHT      |
+------------------------------------------+ | REST | WebSocket    |
                     |                       |                      |
+------------------------------------------+ +----------------------+
|             KI-ASSISTENZKERN             |           |
| Sprachagent | Systemagent | Lernmodul    |           |
| Kontextgedächtnis | Inhaltsanalyse       |  +-------------------+
+------------------------------------------+  | MOBILE INTEGRATION |
                     |                        | Sync | Push        |
+------------------+-------------------+      +-------------------+
| SYSTEMINTEGRATION | DATENMANAGEMENT  |
| Windows-API      | Nutzerprofile-DB  |
| Browser-Extension| System-DB         |
| UI-Automation    | Kontext-Cache     |
+------------------+-------------------+
                     |
+------------------------------------------+
|         MEDIENSTEUERUNG                  |
| Audio-Manager | Video-Manager | Kontrolle|
+------------------------------------------+
```

## 2. Hardware- und Softwarevoraussetzungen

### Hardware-Anforderungen

- **CPU**: Intel Core i7/AMD Ryzen 7 oder besser
- **RAM**: Mindestens 16 GB, empfohlen 32 GB
- **Speicher**: 100 GB SSD-Speicher
- **Grafikkarte**: NVIDIA RTX 2080 oder vergleichbar (für KI-Beschleunigung)
- **Audio**: Hochwertiges Mikrofon oder Headset
- **Kamera**: Webcam mit mindestens 1080p-Auflösung
- **Netzwerk**: Ethernet oder WLAN mit stabiler Internetverbindung

### Software-Voraussetzungen

- **Betriebssystem**: Windows 10 (Version 2004 oder höher) oder Windows 11
- **Python**: Version 3.10 oder höher
- **CUDA**: Version 11.8 (für NVIDIA GPU-Beschleunigung)
- **Webbrowser**: Chrome oder Edge (aktuelle Version)
- **Datenbank**: PostgreSQL 14 oder höher (für vollständige Funktionalität) oder SQLite (für einfache Installation)
- **Docker**: Für isolierte Komponenten (optional)
- **Node.js**: Version 16 oder höher (für WebSocket-Server und React-basierte Mobile-Unterstützung)

## 3. Entwicklungsumgebung einrichten

Bevor wir mit der eigentlichen Implementierung beginnen, müssen wir eine vollständige Entwicklungsumgebung einrichten.

### 3.1 Basis-System einrichten

```bash
# Erstelle Projektverzeichnis
mkdir -p AssistTech
cd AssistTech

# Git-Repository initialisieren
git init

# Python-Umgebung mit Conda einrichten (empfohlen für einfache Paketverwaltung)
# Herunterladen und installieren: https://www.anaconda.com/products/individual
conda create -n assist-tech python=3.10
conda activate assist-tech

# Basis-Entwicklungspakete installieren
pip install black isort flake8 pytest pytest-cov mypy fastapi uvicorn
```

### 3.2 Ordnerstruktur erstellen

```bash
# Erstelle Projektstruktur (entsprechend der modularen Architektur)
mkdir -p assisttech/{core,speech,vision,nlp,integration,db,ui,api,media,utils,config,data,logs,assets,tests,docs,scripts}
mkdir -p assisttech/integration/mobile
mkdir -p assisttech/db/repositories
mkdir -p assisttech/db/migrations
mkdir -p assisttech/ui/accessibility
mkdir -p assisttech/api/endpoints
mkdir -p assisttech/assets/{icons,sounds,translations}
mkdir -p assisttech/tests/{unit,integration,e2e}
mkdir -p assisttech/docs/{api,user,developer}
mkdir -p assisttech/data/{db,models,cache,user}

# Erstelle leere __init__.py Dateien für alle Python-Pakete
find assisttech -type d -exec touch {}/__init__.py \;
```

### 3.3 CUDA und GPU-Unterstützung einrichten

```bash
# CUDA-Toolkit für NVIDIA RTX 2080 installieren
conda install -c conda-forge cudatoolkit=11.8 cudnn=8.6.0

# PyTorch mit CUDA-Unterstützung installieren
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3.4 Versionskontrolle einrichten

```bash
# .gitignore erstellen
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtuelle Umgebungen
venv/
ENV/
.env

# Daten und Modelle
data/models/*
data/db/*
data/cache/*
!data/models/.gitkeep
!data/db/.gitkeep
!data/cache/.gitkeep

# Logs
logs/*
!logs/.gitkeep

# IDE
.idea/
.vscode/
*.swp
*.swo

# Betriebssystem
.DS_Store
Thumbs.db
EOL

# Leere .gitkeep-Dateien erstellen
find assisttech/data -type d -exec touch {}/.gitkeep \;
touch logs/.gitkeep

# Initialer Commit
git add .
git commit -m "Initiale Projektstruktur"
```

## 4. Ordnerstruktur und Komponentenorganisation

Die modulare Struktur des Systems folgt dem folgenden Aufbau:

```
assisttech/
├── core/                       # Kernkomponenten des Systems
│   ├── __init__.py
│   ├── system.py               # Hauptsystemklasse
│   ├── config.py               # Konfigurationsmanager
│   ├── logging_manager.py      # Zentrales Logging
│   └── event_manager.py        # Eventbasierte Kommunikation
│
├── speech/                     # Sprachverarbeitung
│   ├── __init__.py
│   ├── speech_manager.py       # Zentraler Manager für Sprache
│   ├── speech_recognition.py   # Speech-to-Text
│   ├── text_to_speech.py       # Text-to-Speech
│   ├── voice_activity.py       # Sprachaktivitätserkennung
│   └── wake_word.py            # Wake-Word-Erkennung
│
├── vision/                     # Bildverarbeitung
│   ├── __init__.py
│   ├── camera_manager.py       # Kamerazugriff und -steuerung
│   ├── object_detector.py      # Objekterkennung
│   ├── scene_analyzer.py       # Szenenanalyse
│   └── ocr_processor.py        # Texterkennung in Bildern
│
├── nlp/                        # Natural Language Processing
│   ├── __init__.py
│   ├── llm_manager.py          # Large Language Model Manager
│   ├── context_memory.py       # Kontextgedächtnis
│   ├── content_analyzer.py     # Inhaltsanalyse und Zusammenfassung
│   ├── intent_processor.py     # Intentionserkennung
│   └── assistant_agent.py      # Hauptagent für Assistenzfunktionen
│
├── integration/                # Systemintegration
│   ├── __init__.py
│   ├── windows_integration.py  # Windows-spezifische Integration
│   ├── browser_integration.py  # Browser-Integration
│   ├── integration_manager.py  # Zentrale Verwaltung der Integrationen
│   └── mobile/                 # Zukünftige Mobile-Integration
│       ├── __init__.py
│       ├── mobile_api.py       # API für Mobilgeräteanbindung
│       └── sync_service.py     # Synchronisationsdienst
│
├── db/                         # Datenbankverwaltung
│   ├── __init__.py
│   ├── database_manager.py     # Zentrale Datenbankschnittstelle
│   ├── models.py               # Datenbankmodelle (SQLAlchemy)
│   ├── migrations/             # Datenbankmigrationen
│   └── repositories/           # Repository-Pattern für Datenzugriff
│       ├── __init__.py
│       ├── user_repository.py
│       ├── settings_repository.py
│       └── context_repository.py
│
├── ui/                         # Benutzeroberfläche
│   ├── __init__.py
│   ├── tray_application.py     # Systray-Anwendung
│   ├── settings_dialog.py      # Einstellungsdialog
│   ├── feedback_manager.py     # Feedback (audio, visuell)
│   └── accessibility/          # Barrierefreiheitskomponenten
│       ├── __init__.py
│       ├── screen_reader.py    # Bildschirmlesefunktionen
│       └── magnifier.py        # Vergrößerungsfunktionen
│
├── api/                        # API-Schicht (für Mobile-Integration)
│   ├── __init__.py
│   ├── rest_api.py             # REST-API
│   ├── websocket_server.py     # WebSocket-Server für Echtzeit-Kommunikation
│   ├── auth.py                 # Authentifizierung und Autorisierung
│   └── endpoints/              # API-Endpunkte
│       ├── __init__.py
│       ├── assistant_api.py    # Assistenten-Endpunkte
│       ├── speech_api.py       # Sprach-Endpunkte
│       └── vision_api.py       # Bildverarbeitungs-Endpunkte
│
├── media/                      # Medienwiedergabe und -steuerung
│   ├── __init__.py
│   ├── media_controller.py     # Mediensteuerung
│   ├── audio_manager.py        # Audiowiedergabe (inkl. Geschwindigkeit)
│   └── video_manager.py        # Videowiedergabesteuerung
│
├── utils/                      # Hilfsfunktionen
│   ├── __init__.py
│   ├── audio_utils.py          # Audio-Hilfsfunktionen
│   ├── image_utils.py          # Bild-Hilfsfunktionen
│   ├── text_utils.py           # Text-Hilfsfunktionen
│   └── platform_utils.py       # Plattformspezifische Hilfsfunktionen
│
├── main.py                     # Haupteinstiegspunkt
```

## 5. Kernsystem installieren und konfigurieren

### 5.1 Abhängigkeiten installieren

```bash
# Aktualisiere requirements.txt mit allen benötigten Paketen
cat > requirements.txt << EOL
# Basis
pyyaml==6.0.1
python-dotenv==1.0.0
loguru==0.7.0
colorama==0.4.6
tqdm==4.66.1

# Sprachverarbeitung
SpeechRecognition==3.10.0
pyaudio==0.2.13
whisper==1.0.0
piper-tts==1.2.0
pydub==0.25.1
webrtcvad==2.0.10

# KI und NLP
transformers==4.30.2
accelerate==0.21.0
bitsandbytes==0.41.0
sentence-transformers==2.2.2
huggingface-hub==0.16.4
protobuf==4.24.2
tokenizers==0.13.3

# Bildverarbeitung
opencv-python==4.8.0.76
pillow==10.0.0
timm==0.9.2
detectron2==0.7.0

# Webintegration
selenium==4.11.2
webdriver-manager==4.0.0
beautifulsoup4==4.12.2
lxml==4.9.3

# GUI und Systemintegration
pywin32==306
wxPython==4.2.1
pyside6==6.5.2
pyautogui==0.9.54
pynput==1.7.6
python-uinput==0.11.2
win32gui==221.6
pygetwindow==0.0.9

# Datenbanken
sqlalchemy==2.0.20
alembic==1.12.0
psycopg2-binary==2.9.7
python-jose==3.3.0
passlib==1.7.4

# APIs und Server
fastapi==0.103.1
uvicorn==0.23.2
websockets==11.0.3
grpcio==1.57.0
grpcio-tools==1.57.0
pyjwt==2.8.0
httpx==0.25.0

# Medienverwaltung
python-vlc==3.0.18122
pyaudio==0.2.13
moviepy==1.0.3

# Hilfspakete
numpy==1.25.2
pandas==2.1.0
matplotlib==3.7.2
EOL

# Installiere Abhängigkeiten
pip install -r requirements.txt

# Spezielle Pakete
pip install git+https://github.com/openai/whisper.git
```

### 5.2 Konfigurationsdateien erstellen

```bash
# Hauptkonfigurationsdatei
cat > config/config.yaml << EOL
system:
  name: "AssistTech"
  version: "1.0.0"
  log_level: "INFO"
  data_dir: "./data"
  models_dir: "./data/models"
  enable_api: true
  
speech:
  tts_engine: "piper"  # Alternativen: "system", "espeak"
  tts_voice: "de_DE-thorsten-medium"
  tts_rate: 1.0
  stt_engine: "whisper"  # Alternativen: "google", "vosk"
  whisper_model: "small"  # Alternativen: "tiny", "base", "small", "medium"
  wake_word: "Assistent"
  
vision:
  camera_index: 0
  detection_model: "yolov5s"
  ocr_engine: "easyocr"
  
nlp:
  llm_model: "mistral-7b-instruct-v0.1"
  llm_quantization: "q4_0"  # Alternativen: "q4_1", "q5_0", "q8_0"
  embedding_model: "all-MiniLM-L6-v2"
  intent_model: "distilbert-intent"
  
database:
  type: "sqlite"  # Alternativen: "postgresql"
  host: "localhost"
  port: 5432
  name: "assisttech"
  user: "assisttech_user"
  password_env: "DB_PASSWORD"  # Wird aus Umgebungsvariable gelesen
  sync_enabled: true
  
ui:
  theme: "dark"  # Alternativen: "light", "system"
  font_size: "medium"  # Alternativen: "small", "large"
  
integration:
  browser_extension_path: "./extensions/chrome"
  windows_automation: true
  
api:
  host: "0.0.0.0"
  port: 8000
  ws_port: 8001
  enable_auth: true
  jwt_secret_env: "JWT_SECRET"  # Wird aus Umgebungsvariable gelesen
  
media:
  default_player: "system"  # Alternativen: "vlc", "browser"
  default_speed: 1.0
  
security:
  encrypt_data: true
  encryption_key_env: "ENCRYPTION_KEY"  # Wird aus Umgebungsvariable gelesen
  
learning:
  enable_personalization: true
  context_memory_items: 100
  feedback_collection: true
  
mobile:
  enable_sync: true
  sync_interval: 60  # Sekunden
  push_notifications: true
EOL

# Logging-Konfiguration
cat > config/logging_config.yaml << EOL
version: 1
formatters:
  standard:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: standard
    filename: logs/assisttech.log
loggers:
  '':  # Root logger
    level: DEBUG
    handlers: [console, file]
    propagate: no
EOL

# Umgebungsvariablen in .env-Datei (nicht in Git speichern!)
cat > .env << EOL
DB_PASSWORD=supersecurepassword
ENCRYPTION_KEY=4175b9d8e724c2fde62b329cc4776e55
JWT_SECRET=9c8b7a6d5e4f3g2h1i0j9k8l7m6n5o4p
EOL
```

## 6. Event-Manager implementieren

Der Event-Manager ist eine zentrale Komponente, die die Kommunikation zwischen den verschiedenen Modulen ermöglicht. Durch das Publish-Subscribe-Muster können Module unabhängig voneinander arbeiten und trotzdem miteinander kommunizieren.

```python
# core/event_manager.py
import logging
import threading
import queue
import time
from typing import Dict, List, Callable, Any, Optional

class EventManager:
    """
    Zentrale Komponente für die event-basierte Kommunikation zwischen Modulen.
    Implementiert ein Publish-Subscribe-Muster.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("EventManager")
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue = queue.Queue()
        self.is_running = False
        self.processing_thread = None
        
        # Für verzögerte Events
        self.scheduled_events = {}
        self.scheduler_thread = None
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Registriert einen Callback für einen bestimmten Event-Typ.
        
        Args:
            event_type: Der Typ des Events (z.B. "speech.command_received")
            callback: Die Funktion, die bei diesem Event aufgerufen wird
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        
        if callback not in self.subscribers[event_type]:
            self.subscribers[event_type].append(callback)
            self.logger.debug(f"Neuer Subscriber für Event-Typ '{event_type}'")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Entfernt einen Callback für einen bestimmten Event-Typ.
        
        Args:
            event_type: Der Typ des Events
            callback: Die zu entfernende Callback-Funktion
        """
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            self.logger.debug(f"Subscriber für Event-Typ '{event_type}' entfernt")
            
            # Entferne leere Listen
            if not self.subscribers[event_type]:
                del self.subscribers[event_type]
    
    def publish(self, event_type: str, data: Any = None) -> None:
        """
        Veröffentlicht ein Event.
        
        Args:
            event_type: Der Typ des Events
            data: Die mit dem Event verbundenen Daten
        """
        self.logger.debug(f"Event veröffentlicht: {event_type}")
        
        # Füge das Event zur Warteschlange hinzu
        self.event_queue.put((event_type, data))
        
        # Starte die Verarbeitung, falls sie noch nicht läuft
        if not self.is_running:
            self.start()
    
    def publish_delayed(self, event_type: str, data: Any = None, delay: float = 1.0) -> str:
        """
        Veröffentlicht ein Event nach einer Verzögerung.
        
        Args:
            event_type: Der Typ des Events
            data: Die mit dem Event verbundenen Daten
            delay: Verzögerung in Sekunden
            
        Returns:
            event_id: ID des geplanten Events (für mögliche Stornierung)
        """
        import uuid
        event_id = str(uuid.uuid4())
        scheduled_time = time.time() + delay
        
        self.scheduled_events[event_id] = {
            "event_type": event_type,
            "data": data,
            "scheduled_time": scheduled_time
        }
        
        self.logger.debug(f"Event {event_type} geplant für {delay} Sekunden Verzögerung (ID: {event_id})")
        
        # Starte den Scheduler, falls er noch nicht läuft
        if self.scheduler_thread is None or not self.scheduler_thread.is_alive():
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
        
        return event_id
    
    def cancel_delayed_event(self, event_id: str) -> bool:
        """
        Bricht ein geplantes Event ab.
        
        Args:
            event_id: Die ID des geplanten Events
            
        Returns:
            bool: True, wenn das Event gefunden und abgebrochen wurde
        """
        if event_id in self.scheduled_events:
            del self.scheduled_events[event_id]
            self.logger.debug(f"Geplantes Event mit ID {event_id} abgebrochen")
            return True
        return False
    
    def start(self) -> None:
        """Startet die Event-Verarbeitung."""
        if self.is_running:
            return
        
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._processing_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        self.logger.info("Event-Verarbeitung gestartet")
    
    def stop(self) -> None:
        """Stoppt die Event-Verarbeitung."""
        self.is_running = False
        
        if self.processing_thread:
            self.processing_thread.join(timeout=2.0)
            
        self.logger.info("Event-Verarbeitung gestoppt")
    
    def _processing_loop(self) -> None:
        """Thread-Funktion für die Event-Verarbeitung."""
        try:
            while self.is_running:
                try:
                    # Warte auf Events in der Warteschlange
                    event_type, data = self.event_queue.get(timeout=1.0)
                    
                    # Verarbeite das Event
                    self._process_event(event_type, data)
                    
                    # Markiere das Event als erledigt
                    self.event_queue.task_done()
                
                except queue.Empty:
                    # Keine Events in der Warteschlange
                    continue
                
                except Exception as e:
                    self.logger.error(f"Fehler bei der Event-Verarbeitung: {e}")
        
        except Exception as e:
            self.logger.error(f"Fehler im Event-Processing-Thread: {e}")
            self.is_running = False
    
    def _scheduler_loop(self) -> None:
        """Thread-Funktion für den Event-Scheduler."""
        try:
            while self.is_running or self.scheduled_events:
                current_time = time.time()
                to_remove = []
                
                # Prüfe alle geplanten Events
                for event_id, event_info in self.scheduled_events.items():
                    if current_time >= event_info["scheduled_time"]:
                        # Zeit ist abgelaufen, veröffentliche das Event
                        self.publish(event_info["event_type"], event_info["data"])
                        to_remove.append(event_id)
                
                # Entferne verarbeitete Events
                for event_id in to_remove:
                    del self.scheduled_events[event_id]
                
                # Kurze Pause
                time.sleep(0.1)
        
        except Exception as e:
            self.logger.error(f"Fehler im Event-Scheduler-Thread: {e}")
    
    def _process_event(self, event_type: str, data: Any) -> None:
        """
        Verarbeitet ein einzelnes Event und ruft alle registrierten Callbacks auf.
        
        Args:
            event_type: Der Typ des Events
            data: Die mit dem Event verbundenen Daten
        """
        if event_type in self.subscribers:
            callbacks = self.subscribers[event_type].copy()  # Kopie erstellen, falls sich während der Verarbeitung etwas ändert
            
            for callback in callbacks:
                try:
                    callback(data)
                except Exception as e:
                    self.logger.error(f"Fehler im Callback für Event '{event_type}': {e}")
```

## 7. Sprachverarbeitung implementieren

### 7.1 Spracherkennungsmanager

```python
# speech/speech_manager.py
import os
import logging
import threading
import queue
import time
from pathlib import Path

class SpeechManager:
    """Verwaltet Spracheingabe und -ausgabe."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("SpeechManager")
        self.config = config
        self.event_manager = event_manager
        
        # Lade Komponenten
        from speech.speech_recognition import SpeechRecognizer
        from speech.text_to_speech import TextToSpeech
        from speech.wake_word import WakeWordDetector
        from speech.voice_activity import VoiceActivityDetector
        
        # Komponenten initialisieren
        self.recognizer = SpeechRecognizer(config, event_manager)
        self.synthesizer = TextToSpeech(config, event_manager)
        self.wake_word_detector = WakeWordDetector(config, event_manager)
        self.voice_activity_detector = VoiceActivityDetector(config)
        
        # Spracherkennung konfigurieren
        self.wake_word = config["speech"]["wake_word"].lower()
        self.listening = False
        self.continuous_mode = False
        self.audio_queue = queue.Queue()
        self.listen_thread = None
        self.process_thread = None
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("speech.wake_word_detected", self._on_wake_word_detected)
        self.event_manager.subscribe("speech.text_recognized", self._on_text_recognized)
        self.event_manager.subscribe("assistant.response_ready", self._on_response_ready)
        
    def _on_system_ready(self, data):
        """Handler für system.ready Event"""
        # Starte Hintergrundaktivitäten
        self.start_listening()
        
    def _on_wake_word_detected(self, data):
        """Handler für wake_word_detected Event"""
        # Wechsle in aktiven Zuhörmodus
        self.synthesizer.play_notification('wake_word')
        self.continuous_mode = True
        
    def _on_text_recognized(self, text):
        """Handler für text_recognized Event"""
        # Wenn nicht im kontinuierlichen Modus und das Wake Word enthalten ist
        if not self.continuous_mode and self.wake_word in text.lower():
            # Extrahiere Befehl nach dem Wake Word
            command = text.lower().split(self.wake_word, 1)[1].strip()
            if command:
                self.event_manager.publish("speech.command_received", command)
        # Im kontinuierlichen Modus jede Erkennung weitergeben
        elif self.continuous_mode:
            self.event_manager.publish("speech.command_received", text)
            # Zurück in den Wake-Word-Modus nach einem Befehl
            self.continuous_mode = False
            
    def _on_response_ready(self, response):
        """Handler für response_ready Event"""
        # Text ausgeben
        self.synthesizer.speak(response)
    
    def start_listening(self):
        """Startet die kontinuierliche Spracherkennung."""
        if self.listening:
            return
        
        self.listening = True
        
        # Starte Wake-Word-Detektor
        self.wake_word_detector.start()
        
        # Starte Threads
        self.listen_thread = threading.Thread(target=self._listen_loop)
        self.process_thread = threading.Thread(target=self._process_loop)
        
        self.listen_thread.daemon = True
        self.process_thread.daemon = True
        
        self.listen_thread.start()
        self.process_thread.start()
        
        self.logger.info("Spracherkennung gestartet")
        
        # Zeige Bereitschaft
        self.synthesizer.play_notification('startup')
        
    def stop_listening(self):
        """Stoppt die kontinuierliche Spracherkennung."""
        self.listening = False
        self.wake_word_detector.stop()
        
        if self.listen_thread:
            self.listen_thread.join(timeout=2.0)
        if self.process_thread:
            self.process_thread.join(timeout=2.0)
        
        self.logger.info("Spracherkennung gestoppt")
    
    def _listen_loop(self):
        """Thread-Funktion für das kontinuierliche Abhören des Mikrofons."""
        import pyaudio
        import numpy as np
        import wave
        import tempfile
        
        # Audio-Parameter
        sample_rate = 16000
        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        
        # PyAudio initialisieren
        audio = pyaudio.PyAudio()
        
        stream = audio.open(
            format=audio_format,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size
        )
        
        frames = []
        is_speaking = False
        silence_frames = 0
        
        try:
            while self.listening:
                data = stream.read(chunk_size, exception_on_overflow=False)
                
                # Prüfe auf Sprachaktivität
                if self.voice_activity_detector.is_speech(data):
                    if not is_speaking:
                        is_speaking = True
                        # Event: Sprachstart
                        self.event_manager.publish("speech.speech_started", None)
                    
                    frames.append(data)
                    silence_frames = 0
                else:
                    frames.append(data)
                    
                    if is_speaking:
                        silence_frames += 1
                        
                        # Wenn genug Stille erkannt wurde und wir vorher gesprochen haben
                        if silence_frames > 30:  # ca. 1 Sekunde Stille
                            is_speaking = False
                            
                            # Event: Sprachende
                            self.event_manager.publish("speech.speech_ended", None)
                            
                            # Audio in eine temporäre Datei schreiben
                            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
                                temp_path = temp.name
                            
                            wf = wave.open(temp_path, 'wb')
                            wf.setnchannels(channels)
                            wf.setsampwidth(audio.get_sample_size(audio_format))
                            wf.setframerate(sample_rate)
                            wf.writeframes(b''.join(frames))
                            wf.close()
                            
                            # Audiodatei in die Warteschlange stellen
                            self.audio_queue.put(temp_path)
                            
                            # Frames zurücksetzen
                            frames = []
                
                # Begrenze die Aufnahmelänge
                if len(frames) > 160 * sample_rate // chunk_size:  # Max. 10 Sekunden
                    if is_speaking:
                        # Event: Sprachende (wegen Zeitüberschreitung)
                        self.event_manager.publish("speech.speech_ended", None)
                        is_speaking = False
                        
                        # Audio in eine temporäre Datei schreiben
                        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
                            temp_path = temp.name
                        
                        wf = wave.open(temp_path, 'wb')
                        wf.setnchannels(channels)
                        wf.setsampwidth(audio.get_sample_size(audio_format))
                        wf.setframerate(sample_rate)
                        wf.writeframes(b''.join(frames))
                        wf.close()
                        
                        # Audiodatei in die Warteschlange stellen
                        self.audio_queue.put(temp_path)
                    
                    # Frames zurücksetzen
                    frames = []
        
        except Exception as e:
            self.logger.error(f"Fehler im Listening-Thread: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
    
    def _process_loop(self):
        """Thread-Funktion für die Verarbeitung aufgenommener Audio."""
        try:
            while self.listening:
                try:
                    # Warte auf Audio aus der Warteschlange
                    audio_path = self.audio_queue.get(timeout=1.0)
                    
                    # Transkribiere Audio
                    text = self.recognizer.transcribe_audio(audio_path)
                    
                    # Lösche temporäre Datei
                    try:
                        os.unlink(audio_path)
                    except:
                        pass
                    
                    if text:
                        self.logger.debug(f"Erkannter Text: {text}")
                        
                        # Veröffentliche erkannten Text als Event
                        self.event_manager.publish("speech.text_recognized", text)
                
                except queue.Empty:
                    continue
                except Exception as e:
                    self.logger.error(f"Fehler bei der Audioverarbeitung: {e}")
        
        except Exception as e:
            self.logger.error(f"Fehler im Processing-Thread: {e}")
    
    def speak(self, text, block=True, speed=None):
        """Gibt Text als Sprache aus."""
        return self.synthesizer.speak(text, block, speed)
    
    def listen_once(self, timeout=5.0, language="de"):
        """Hört einmalig auf eine Spracheingabe und gibt den erkannten Text zurück."""
        self.logger.info("Höre auf einmalige Spracheingabe...")
        
        # Spiele Hinweiston
        self.synthesizer.play_notification('listening')
        
        return self.recognizer.listen_once(timeout, language)
```

### 7.2 Wake-Word-Erkennung

```python
# speech/wake_word.py
import os
import logging
import threading
import queue
import time
import numpy as np
import pyaudio
from pathlib import Path

class WakeWordDetector:
    """Klasse zur Erkennung des Wake-Words."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("WakeWordDetector")
        self.config = config
        self.event_manager = event_manager
        
        # Konfiguration
        self.wake_word = config["speech"]["wake_word"].lower()
        self.sample_rate = 16000
        self.chunk_size = 1024
        
        # Status
        self.is_running = False
        self.detection_thread = None
        
        # Einfacher Ansatz: Verwende Spracherkennung für Wake-Word
        # In einer vollständigen Implementierung würde hier ein spezialisiertes
        # Wake-Word-Modell verwendet werden (z.B. Porcupine, Snowboy)
        
        # Modellpfad
        models_dir = Path(config["system"]["models_dir"])
        self.model_dir = models_dir / "wake_word"
        os.makedirs(self.model_dir, exist_ok=True)
    
    def start(self):
        """Startet die Wake-Word-Erkennung."""
        if self.is_running:
            return
        
        self.is_running = True
        self.detection_thread = threading.Thread(target=self._detection_loop)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        
        self.logger.info("Wake-Word-Erkennung gestartet")
    
    def stop(self):
        """Stoppt die Wake-Word-Erkennung."""
        self.is_running = False
        
        if self.detection_thread:
            self.detection_thread.join(timeout=2.0)
        
        self.logger.info("Wake-Word-Erkennung gestoppt")
    
    def _detection_loop(self):
        """Thread-Funktion für die kontinuierliche Wake-Word-Erkennung."""
        try:
            # In einer vollständigen Implementierung würde hier ein
            # spezialisiertes Wake-Word-Modell verwendet werden
            # 
            # Für diesen Prototyp verwenden wir ein vereinfachtes Modell,
            # das auf der regulären Spracherkennung basiert
            
            # Diese Implementierung ist nur ein Platzhalter
            # und sollte in der Produktion nicht verwendet werden
            
            # Hinweis: Eine echte Wake-Word-Erkennung würde ein spezialisiertes
            # Modell wie Porcupine, Snowboy oder ein eigenes trainiertes
            # Modell verwenden, das kontinuierlich und effizient läuft
            
            # Für den Zweck dieser Implementierung:
            # Wir hören alle 0.5 Sekunden kurz zu und prüfen auf das Wake Word
            
            from speech.speech_recognition import SpeechRecognizer
            recognizer = SpeechRecognizer(self.config, self.event_manager)
            
            audio = pyaudio.PyAudio()
            
            while self.is_running:
                # Kurzes Audio aufnehmen (1 Sekunde)
                stream = audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=self.chunk_size
                )
                
                frames = []
                for _ in range(int(self.sample_rate / self.chunk_size)):
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    frames.append(data)
                
                stream.stop_stream()
                stream.close()
                
                # Prüfe auf Wake Word (vereinfachte Implementierung)
                import tempfile
                import wave
                
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
                    temp_path = temp.name
                
                wf = wave.open(temp_path, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                # Schnelle, ungenaue Transkription für Wake-Word
                text = recognizer.transcribe_audio(temp_path, fast_mode=True)
                
                # Lösche temporäre Datei
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                # Prüfe auf Wake Word
                if text and self.wake_word.lower() in text.lower():
                    self.logger.info(f"Wake Word erkannt: {text}")
                    
                    # Veröffentliche Wake-Word-Event
                    self.event_manager.publish("speech.wake_word_detected", {
                        "wake_word": self.wake_word,
                        "full_text": text
                    })
                
                # Pause zwischen den Erkennungsversuchen
                time.sleep(0.5)
            
            audio.terminate()
        
        except Exception as e:
            self.logger.error(f"Fehler im Wake-Word-Erkennungs-Thread: {e}")
            self.is_running = False
```

### 7.3 Text-to-Speech mit Geschwindigkeitskontrolle

```python
# speech/text_to_speech.py
import os
import logging
import tempfile
from pathlib import Path
import subprocess
import numpy as np
import torch
import sounddevice as sd
import soundfile as sf
import threading
import queue
import time

class TextToSpeech:
    """Klasse für Text-to-Speech mit flexibler Geschwindigkeitskontrolle."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("TextToSpeech")
        self.config = config
        self.event_manager = event_manager
        
        # Konfiguration
        self.voice = config["speech"]["tts_voice"]
        self.rate = float(config["speech"]["tts_rate"])
        self.engine_type = config["speech"]["tts_engine"]
        
        # Audio-Queue für nicht-blockierende Sprachausgabe
        self.audio_queue = queue.Queue()
        self.is_playing = False
        self.play_thread = None
        
        # Notification-Sounds
        self.notification_sounds = {}
        self._load_notification_sounds()
        
        # Prüfe, ob Piper installiert ist
        try:
            subprocess.run(["piper", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.piper_installed = True
        except FileNotFoundError:
            self.logger.warning("Piper TTS nicht gefunden. Installation mit 'pip install piper-tts'")
            self.piper_installed = False
        
        # Modellpfad
        models_dir = Path(config["system"]["models_dir"])
        self.model_dir = models_dir / "tts"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Stelle sicher, dass die Modelle vorhanden sind
        self._ensure_models()
        
        # Starte Wiedergabe-Thread
        self.start_playback_thread()
    
    def _load_notification_sounds(self):
        """Lädt Benachrichtigungstöne."""
        try:
            # Pfade zu Benachrichtigungstönen
            sound_dir = Path("assets/sounds")
            
            # Überprüfe, ob das Verzeichnis existiert
            if sound_dir.exists():
                # Lade Standard-Benachrichtigungstöne
                for sound_name in ["startup", "wake_word", "listening", "success", "error"]:
                    sound_path = sound_dir / f"{sound_name}.wav"
                    
                    if sound_path.exists():
                        try:
                            data, samplerate = sf.read(str(sound_path))
                            self.notification_sounds[sound_name] = (data, samplerate)
                            self.logger.debug(f"Benachrichtigungston '{sound_name}' geladen")
                        except Exception as e:
                            self.logger.error(f"Fehler beim Laden des Benachrichtigungstons '{sound_name}': {e}")
            else:
                self.logger.warning(f"Verzeichnis für Benachrichtigungstöne nicht gefunden: {sound_dir}")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Benachrichtigungstöne: {e}")
    
    def start_playback_thread(self):
        """Startet den Thread für die Audiowiedergabe."""
        if self.play_thread is None or not self.play_thread.is_alive():
            self.is_playing = True
            self.play_thread = threading.Thread(target=self._playback_loop)
            self.play_thread.daemon = True
            self.play_thread.start()
            self.logger.debug("Audiowiedergabe-Thread gestartet")
    
    def stop_playback_thread(self):
        """Stoppt den Thread für die Audiowiedergabe."""
        self.is_playing = False
        
        if self.play_thread:
            self.play_thread.join(timeout=2.0)
            self.play_thread = None
            
        self.logger.debug("Audiowiedergabe-Thread gestoppt")
    
    def _playback_loop(self):
        """Thread-Funktion für die Audiowiedergabe-Warteschlange."""
        try:
            while self.is_playing:
                try:
                    # Warte auf Audio in der Warteschlange
                    audio_info = self.audio_queue.get(timeout=1.0)
                    
                    # Spiele Audio ab
                    if isinstance(audio_info, tuple) and len(audio_info) == 3:
                        data, samplerate, speed = audio_info
                        
                        # Passe Geschwindigkeit an (falls erforderlich)
                        if speed != 1.0:
                            import librosa
                            import numpy as np
                            
                            # Time stretching mit librosa
                            data_stretched = librosa.effects.time_stretch(
                                np.asarray(data, dtype=np.float32), 
                                rate=speed
                            )
                            
                            # Abspielen
                            sd.play(data_stretched, samplerate)
                            sd.wait()
                        else:
                            # Normal abspielen
                            sd.play(data, samplerate)
                            sd.wait()
                    
                    # Markiere als erledigt
                    self.audio_queue.task_done()
                    
                    # Veröffentliche Event: Sprachausgabe beendet
                    self.event_manager.publish("speech.tts_finished", None)
                
                except queue.Empty:
                    continue
                except Exception as e:
                    self.logger.error(f"Fehler bei der Audiowiedergabe: {e}")
        
        except Exception as e:
            self.logger.error(f"Fehler im Audiowiedergabe-Thread: {e}")
            self.is_playing = False
    
    def _ensure_models(self):
        """Stellt sicher, dass die benötigten TTS-Modelle vorhanden sind."""
        voice_parts = self.voice.split("-")
        lang_voice = voice_parts[0]
        quality = voice_parts[-1] if len(voice_parts) > 1 else "medium"
        
        model_file = self.model_dir / f"{lang_voice}_{quality}.onnx"
        config_file = self.model_dir / f"{lang_voice}_{quality}.json"
        
        if not model_file.exists() or not config_file.exists():
            self.logger.info(f"Lade TTS-Modell für {self.voice}...")
            self._download_model(lang_voice, quality)
    
    def _download_model(self, lang_voice, quality):
        """Lädt ein TTS-Modell herunter."""
        try:
            from huggingface_hub import hf_hub_download
            
            language, voice = lang_voice.split("_")
            model_path = f"{language}/{voice}/{quality}/{lang_voice}-{quality}.onnx"
            config_path = f"{language}/{voice}/{quality}/{lang_voice}-{quality}.json"
            
            hf_hub_download(repo_id='rhasspy/piper-voices', 
                           filename=model_path, 
                           local_dir=self.model_dir.parent)
            
            hf_hub_download(repo_id='rhasspy/piper-voices', 
                           filename=config_path, 
                           local_dir=self.model_dir.parent)
            
            self.logger.info(f"TTS-Modell für {lang_voice} erfolgreich heruntergeladen.")
        except Exception as e:
            self.logger.error(f"Fehler beim Herunterladen des TTS-Modells: {e}")
            raise
    
    def speak(self, text, block=True, speed=None):
        """
        Gibt Text als Sprache aus mit anpassbarer Geschwindigkeit.
        
        Args:
            text: Der auszugebende Text
            block: Ob die Funktion blockieren soll, bis die Sprachausgabe abgeschlossen ist
            speed: Geschwindigkeitsfaktor (1.0 = normal, 2.0 = doppelt so schnell)
        """
        if not text:
            return
        
        # Standardgeschwindigkeit verwenden, falls nicht angegeben
        if speed is None:
            speed = self.rate
        
        # Veröffentliche Event: Sprachausgabe startet
        self.event_manager.publish("speech.tts_started", {"text": text, "speed": speed})
        
        if self.engine_type == "piper" and self.piper_installed:
            return self._speak_with_piper(text, block, speed)
        else:
            self.logger.warning(f"Verwende Systemstimme (Engine {self.engine_type} nicht verfügbar)")
            return self._speak_with_system(text, block, speed)
    
    def speak_text_portion(self, text, start_position=0, end_position=None, speed=None, block=True):
        """
        Liest einen bestimmten Teil eines Textes vor.
        
        Args:
            text: Der gesamte Text
            start_position: Startposition (Index)
            end_position: Endposition (Index), None für Ende des Textes
            speed: Geschwindigkeitsfaktor
            block: Ob die Funktion blockieren soll
        """
        if end_position is None:
            end_position = len(text)
            
        text_portion = text[start_position:end_position]
        return self.speak(text_portion, block, speed)
    
    def _speak_with_piper(self, text, block, speed=1.0):
        """Verwendet Piper TTS zur Sprachausgabe."""
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
                temp_path = temp.name
            
            voice_model = str(self.model_dir / f"{self.voice}.onnx")
            voice_config = str(self.model_dir / f"{self.voice}.json")
            
            cmd = [
                "piper",
                "--model", voice_model,
                "--config", voice_config,
                "--output_file", temp_path
            ]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                self.logger.error(f"Fehler bei Piper TTS: {stderr}")
                return
            
            # Audio laden
            data, samplerate = sf.read(temp_path)
            
            # Audio in die Warteschlange stellen
            self.audio_queue.put((data, samplerate, speed))
            
            # Blockieren, falls gewünscht
            if block:
                self.audio_queue.join()
            
            # Temporäre Datei löschen
            try:
                os.unlink(temp_path)
            except:
                pass
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Sprachausgabe mit Piper: {e}")
            self._speak_with_system(text, block, speed)  # Fallback zur Systemstimme
            return False
    
    def _speak_with_system(self, text, block, speed=1.0):
        """Verwendet die Systemstimme zur Sprachausgabe."""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Geschwindigkeit einstellen (pyttsx3 verwendet Wörter pro Minute)
            base_rate = 150  # Standard-WPM
            engine.setProperty('rate', int(base_rate * speed))
            
            # Sprich
            engine.say(text)
            
            if block:
                engine.runAndWait()
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Sprachausgabe mit der Systemstimme: {e}")
            return False
    
    def play_notification(self, sound_name):
        """Spielt einen Benachrichtigungston ab."""
        try:
            if sound_name in self.notification_sounds:
                data, samplerate = self.notification_sounds[sound_name]
                
                # Audio in die Warteschlange stellen
                self.audio_queue.put((data, samplerate, 1.0))
                
                return True
            else:
                self.logger.warning(f"Benachrichtigungston '{sound_name}' nicht gefunden")
                return False
        
        except Exception as e:
            self.logger.error(f"Fehler beim Abspielen des Benachrichtigungstons: {e}")
            return False
```

## 8. Bildverarbeitung und Kamerazugriff

### 8.1 Kamera-Manager und Bildanalyse

```python
# vision/camera_manager.py
import os
import logging
import threading
import time
from pathlib import Path
import cv2
import numpy as np
import torch
from PIL import Image

class CameraManager:
    """Verwaltet den Kamerazugriff und die Bildverarbeitung."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("CameraManager")
        self.config = config
        self.event_manager = event_manager
        
        # Kamera-Konfiguration
        self.camera_index = config["vision"]["camera_index"]
        self.frame_width = 640
        self.frame_height = 480
        self.fps = 30
        
        # Status
        self.is_running = False
        self.camera = None
        self.current_frame = None
        self.lock = threading.Lock()
        
        # Thread für Kamera-Verarbeitung
        self.camera_thread = None
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("vision.capture_image", self._on_capture_image)
        self.event_manager.subscribe("vision.stop_camera", self._on_stop_camera)
    
    def _on_system_ready(self, data):
        """Handler für System-Ready-Event"""
        # Optional: Kamera automatisch starten
        # self.start_camera()
        pass
    
    def _on_capture_image(self, data):
        """Handler für Capture-Image-Event"""
        # Stelle sicher, dass die Kamera läuft
        if not self.is_running:
            self.start_camera()
            # Kurze Wartezeit für Kamera-Initialisierung
            time.sleep(0.5)
        
        # Erfasse Bild
        image = self.capture_image()
        
        # Veröffentliche erfasstes Bild
        if image is not None:
            self.event_manager.publish("vision.image_captured", {
                "image": image,
                "timestamp": time.time(),
                "format": "numpy_rgb"
            })
    
    def _on_stop_camera(self, data):
        """Handler für Stop-Camera-Event"""
        self.stop_camera()
    
    def start_camera(self):
        """Startet die Kamera."""
        if self.is_running:
            return True
        
        try:
            # Kamera öffnen
            self.camera = cv2.VideoCapture(self.camera_index)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
            
            if not self.camera.isOpened():
                self.logger.error(f"Konnte Kamera mit Index {self.camera_index} nicht öffnen")
                return False
            
            self.is_running = True
            self.camera_thread = threading.Thread(target=self._camera_loop)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            
            self.logger.info(f"Kamera mit Index {self.camera_index} erfolgreich gestartet")
            
            # Veröffentliche Event: Kamera gestartet
            self.event_manager.publish("vision.camera_started", {
                "camera_index": self.camera_index,
                "resolution": (self.frame_width, self.frame_height),
                "fps": self.fps
            })
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Starten der Kamera: {e}")
            return False
    
    def stop_camera(self):
        """Stoppt die Kamera."""
        self.is_running = False
        
        if self.camera_thread:
            self.camera_thread.join(timeout=2.0)
            self.camera_thread = None
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        self.logger.info("Kamera gestoppt")
        
        # Veröffentliche Event: Kamera gestoppt
        self.event_manager.publish("vision.camera_stopped", None)
    
    def _camera_loop(self):
        """Thread-Funktion für die kontinuierliche Kamera-Erfassung."""
        try:
            while self.is_running:
                success, frame = self.camera.read()
                
                if not success:
                    self.logger.warning("Fehler beim Lesen des Kamera-Frames")
                    time.sleep(0.1)
                    continue
                
                # Frame im BGR-Format speichern (OpenCV-Standard)
                with self.lock:
                    self.current_frame = frame
                
                # Veröffentliche Frame-Update-Event (nur bei Bedarf)
                # self.event_manager.publish("vision.frame_updated", None)
                
                # Kurze Pause, um CPU-Auslastung zu reduzieren
                time.sleep(1.0 / self.fps)
        
        except Exception as e:
            self.logger.error(f"Fehler im Kamera-Thread: {e}")
        finally:
            if self.camera:
                self.camera.release()
    
    def get_current_frame(self):
        """Gibt den aktuellen Kamera-Frame zurück."""
        with self.lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
            return None
    
    def capture_image(self):
        """Erfasst ein einzelnes Bild von der Kamera."""
        if not self.is_running:
            self.start_camera()
            # Kurze Wartezeit für Kamera-Initialisierung
            time.sleep(0.5)
        
        frame = self.get_current_frame()
        
        if frame is not None:
            # Konvertiere von BGR zu RGB (Standard für die meisten Bildverarbeitungsmodelle)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return rgb_frame
        
        return None
    
    def capture_image_pil(self):
        """Erfasst ein einzelnes Bild und gibt es als PIL-Image zurück."""
        frame = self.capture_image()
        
        if frame is not None:
            pil_image = Image.fromarray(frame)
            return pil_image
        
        return None
    
    def save_image(self, filename=None, format="jpg"):
        """
        Erfasst ein Bild und speichert es als Datei.
        
        Args:
            filename: Dateiname, falls nicht angegeben wird ein Zeitstempel verwendet
            format: Bildformat ("jpg", "png", etc.)
            
        Returns:
            str: Pfad zur gespeicherten Datei oder None bei Fehler
        """
        frame = self.capture_image()
        
        if frame is None:
            self.logger.error("Konnte kein Bild erfassen")
            return None
        
        try:
            # Erstelle Dateinamen mit Zeitstempel, falls nicht angegeben
            if filename is None:
                timestamp = int(time.time())
                filename = f"data/images/capture_{timestamp}.{format}"
            
            # Stelle sicher, dass das Verzeichnis existiert
            directory = os.path.dirname(filename)
            os.makedirs(directory, exist_ok=True)
            
            # Speichere das Bild
            if format.lower() in ["jpg", "jpeg"]:
                # Konvertiere zurück zu BGR für OpenCV
                bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite(filename, bgr_frame)
            else:
                # Für andere Formate verwende PIL
                pil_image = Image.fromarray(frame)
                pil_image.save(filename, format=format.upper())
            
            self.logger.info(f"Bild erfolgreich gespeichert: {filename}")
            
            # Veröffentliche Event: Bild gespeichert
            self.event_manager.publish("vision.image_saved", {
                "filename": filename,
                "format": format
            })
            
            return filename
        
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern des Bildes: {e}")
            return None
```

### 8.2 Szenenanalysator

```python
# vision/scene_analyzer.py
import os
import logging
import time
import numpy as np
import cv2
from PIL import Image
import torch
from pathlib import Path

class SceneAnalyzer:
    """Analysiert Szenen und erstellt Beschreibungen von Bildern."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("SceneAnalyzer")
        self.config = config
        self.event_manager = event_manager
        
        # Modellpfad
        models_dir = Path(config["system"]["models_dir"])
        self.model_dir = models_dir / "vision"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Lade ObjectDetector und OCRProcessor
        from vision.object_detector import ObjectDetector
        from vision.ocr_processor import OCRProcessor
        
        self.object_detector = ObjectDetector(config, event_manager)
        self.ocr_processor = OCRProcessor(config, event_manager)
        
        # Registriere Event-Handler
        self.event_manager.subscribe("vision.image_captured", self._on_image_captured)
        self.event_manager.subscribe("vision.analyze_scene", self._on_analyze_scene)
    
    def _on_image_captured(self, data):
        """Handler für image_captured Event."""
        # Automatische Analyse deaktiviert, um Ressourcen zu sparen
        # Stattdessen nur auf explizites analyze_scene-Event reagieren
        pass
    
    def _on_analyze_scene(self, data):
        """Handler für analyze_scene Event."""
        image = None
        
        # Extrahiere Bild aus den Eventdaten
        if isinstance(data, dict) and "image" in data:
            image = data["image"]
        elif isinstance(data, np.ndarray):
            image = data
        
        # Erfasse ein Bild, falls keines übergeben wurde
        if image is None:
            # Erfasse Bild von der Kamera
            self.event_manager.publish("vision.capture_image", None)
            
            # Warte auf die Bilderfassung (mit Timeout)
            captured_image = None
            start_time = time.time()
            
            def on_image_captured(event_data):
                nonlocal captured_image
                captured_image = event_data["image"]
            
            # Temporärer Event-Handler für Bilderfassung
            self.event_manager.subscribe("vision.image_captured", on_image_captured)
            
            # Warte auf das Bild
            while captured_image is None and time.time() - start_time < 5.0:
                time.sleep(0.1)
            
            # Entferne temporären Handler
            self.event_manager.unsubscribe("vision.image_captured", on_image_captured)
            
            if captured_image is None:
                self.logger.error("Timeout bei der Bilderfassung")
                self.event_manager.publish("vision.analysis_failed", {
                    "error": "Timeout bei der Bilderfassung"
                })
                return
            
            image = captured_image
        
        # Führe die Analyse durch
        self.analyze_image(image)
    
    def analyze_image(self, image):
        """
        Führt eine vollständige Bildanalyse durch.
        
        Args:
            image: Das zu analysierende Bild (numpy-Array oder PIL-Image)
        """
        try:
            self.logger.info("Starte Bildanalyse")
            
            # Konvertiere zu numpy-Array, falls es ein PIL-Image ist
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            # Starte Timer für Performance-Messung
            start_time = time.time()
            
            # Objekterkennung durchführen
            detections = self.object_detector.detect_objects(image)
            
            # Text erkennen (OCR)
            text = None
            if self.ocr_processor.is_ready():
                text = self.ocr_processor.get_text(image)
            
            # Bild beschreiben
            caption = self.object_detector.generate_caption(image, detections)
            
            # Szenenanalyse
            scene_type = self._analyze_scene_type(detections)
            
            # Zusammenfassung der erkannten Objekte
            object_summary = {}
            for det in detections:
                cls = det['class']
                if cls in object_summary:
                    object_summary[cls] += 1
                else:
                    object_summary[cls] = 1
            
            # Ergebniszusammenfassung
            result = {
                'caption': caption,
                'scene_type': scene_type,
                'objects': object_summary,
                'detections': detections,
                'text': text,
                'analysis_time': time.time() - start_time
            }
            
            # Veröffentliche Event: Analyse abgeschlossen
            self.event_manager.publish("vision.analysis_completed", result)
            
            self.logger.info(f"Bildanalyse abgeschlossen in {result['analysis_time']:.2f} Sekunden")
            
            return result
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Bildanalyse: {e}")
            
            # Veröffentliche Event: Analyse fehlgeschlagen
            self.event_manager.publish("vision.analysis_failed", {
                "error": str(e)
            })
            
            return {
                'caption': "Fehler bei der Bildanalyse.",
                'scene_type': "unknown",
                'objects': {},
                'detections': [],
                'text': None,
                'error': str(e)
            }
    
    def _analyze_scene_type(self, detections):
        """
        Bestimmt den Typ der Szene basierend auf erkannten Objekten.
        
        Args:
            detections: Liste der erkannten Objekte
            
        Returns:
            str: Szenentyp (z.B. "indoor", "outdoor", "urban", etc.)
        """
        # Extrahiere erkannte Klassen
        classes = [det['class'] for det in detections]
        
        # Zähle Häufigkeiten
        class_counts = {}
        for cls in classes:
            if cls in class_counts:
                class_counts[cls] += 1
            else:
                class_counts[cls] = 1
        
        # Definiere Kategorien von Objekten für verschiedene Szenentypen
        outdoor_objects = {"tree", "sky", "mountain", "grass", "forest", "road", "car", "bicycle"}
        indoor_objects = {"chair", "sofa", "table", "bed", "book", "tv", "laptop", "bottle"}
        urban_objects = {"building", "person", "car", "traffic light", "bus", "truck"}
        nature_objects = {"tree", "mountain", "river", "lake", "flower", "animal", "bird"}
        
        # Zähle Übereinstimmungen
        outdoor_count = sum(class_counts.get(obj, 0) for obj in outdoor_objects)
        indoor_count = sum(class_counts.get(obj, 0) for obj in indoor_objects)
        urban_count = sum(class_counts.get(obj, 0) for obj in urban_objects)
        nature_count = sum(class_counts.get(obj, 0) for obj in nature_objects)
        
        # Bestimme den dominanten Szenentyp
        scene_scores = {
            "indoor": indoor_count,
            "outdoor": outdoor_count,
            "urban": urban_count,
            "nature": nature_count
        }
        
        # Wähle den Typ mit der höchsten Punktzahl
        if max(scene_scores.values()) > 0:
            dominant_scene = max(scene_scores.items(), key=lambda x: x[1])[0]
            return dominant_scene
        else:
            return "unknown"
```

## 9. KI-Modelle einrichten

### 9.1 Intent-Prozessor

```python
# nlp/intent_processor.py
import os
import logging
import torch
import numpy as np
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class IntentProcessor:
    """Erkennt und verarbeitet Intentionen aus Nutzereingaben."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("IntentProcessor")
        self.config = config
        self.event_manager = event_manager
        
        # Modellpfad
        models_dir = Path(config["system"]["models_dir"])
        self.model_dir = models_dir / "nlp"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Modellkonfiguration
        self.model_name = config["nlp"]["intent_model"]
        
        # Gerät (CPU/GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"Verwende Device für Intent-Klassifikation: {self.device}")
        
        # Intents und Vertrauensschwelle
        self.intent_classes = [
            "browser_open", "browser_search", "browser_summary", "browser_navigate",
            "system_open", "system_close", "system_control",
            "media_play", "media_pause", "media_volume", "media_speed",
            "vision_capture", "vision_describe", "vision_read",
            "help", "info", "general_query"
        ]
        self.confidence_threshold = 0.6
        
        # Intent-Klassifikationsmodell
        self.tokenizer = None
        self.model = None
        
        # Lade Intent-Modell
        self.load_model()
        
        # Registriere Event-Handler
        self.event_manager.subscribe("speech.command_received", self._on_command_received)
    
    def load_model(self):
        """Lädt das Intent-Klassifikationsmodell."""
        try:
            self.logger.info(f"Lade Intent-Klassifikationsmodell: {self.model_name}")
            
            # Für eine vereinfachte Implementierung verwenden wir ein Standard-Hugging-Face-Modell
            # In einer vollständigen Implementierung würde ein speziell trainiertes Modell 
            # für die anwendungsspezifischen Intents verwendet werden
            
            model_path = self.model_dir / "intent-model"
            
            if model_path.exists():
                # Lokales Modell verwenden
                self.tokenizer = AutoTokenizer.from_pretrained(str(model_path))
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    str(model_path),
                    num_labels=len(self.intent_classes)
                ).to(self.device)
            else:
                # Hugging-Face-Modell verwenden
                # Hinweis: Dies ist nur ein Platzhalter - in der Produktion sollte ein
                # speziell für diese Anwendung trainiertes Modell verwendet werden
                self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    "distilbert-base-uncased",
                    num_labels=len(self.intent_classes)
                ).to(self.device)
                
                # Speichere Modell lokal für späteren Gebrauch
                self.tokenizer.save_pretrained(str(model_path))
                self.model.save_pretrained(str(model_path))
            
            self.logger.info("Intent-Klassifikationsmodell erfolgreich geladen")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Laden des Intent-Klassifikationsmodells: {e}")
            # Setze das Modell auf None, um später eine regelbasierte Fallback-Lösung zu verwenden
            self.model = None
    
    def _on_command_received(self, command):
        """Handler für command_received Event."""
        if not command:
            return
        
        # Erkenne die Intention des Befehls
        intent, confidence, params = self.recognize_intent(command)
        
        # Veröffentliche Intent erkannt Event
        self.event_manager.publish("nlp.intent_recognized", {
            "intent": intent,
            "confidence": confidence,
            "params": params,
            "original_command": command
        })
        
        # Verarbeite die Intention entsprechend
        self.process_intent(intent, params, command)
    
    def recognize_intent(self, text):
        """
        Erkennt die Intention aus einem Text.
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            tuple: (intent, confidence, params)
        """
        # Wenn das Modell nicht geladen werden konnte, verwende regelbasierte Erkennung
        if self.model is None:
            return self._rule_based_intent_recognition(text)
        
        try:
            # Tokenisiere den Text
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
            
            # Führe Modell-Inferenz durch
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Extrahiere Prädiktionen
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=1)[0]
            
            # Finde die wahrscheinlichste Intention
            max_prob, max_idx = torch.max(probabilities, dim=0)
            confidence = max_prob.item()
            intent = self.intent_classes[max_idx.item()]
            
            # Extrahiere Parameter aus dem Text
            params = self._extract_params(text, intent)
            
            # Überprüfe Konfidenzschwelle
            if confidence < self.confidence_threshold:
                # Fallback bei geringer Konfidenz
                fallback_intent, fallback_confidence, fallback_params = self._rule_based_intent_recognition(text)
                
                # Wenn die regelbasierte Erkennung besser ist, verwende diese
                if fallback_confidence > confidence:
                    return fallback_intent, fallback_confidence, fallback_params
            
            return intent, confidence, params
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Intent-Erkennung: {e}")
            # Fallback zur regelbasierten Erkennung
            return self._rule_based_intent_recognition(text)
    
    def _rule_based_intent_recognition(self, text):
        """
        Regelbasierte Intent-Erkennung als Fallback.
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            tuple: (intent, confidence, params)
        """
        text_lower = text.lower()
        
        # Browser-Intents
        if any(keyword in text_lower for keyword in ["öffne website", "gehe zu", "besuche", "navigiere zu"]):
            url = self._extract_url(text_lower)
            return "browser_open", 0.9, {"url": url}
        
        elif any(keyword in text_lower for keyword in ["suche nach", "google", "finde"]):
            query = text_lower.split("suche nach", 1)[1].strip() if "suche nach" in text_lower else text_lower.split("google", 1)[1].strip()
            return "browser_search", 0.9, {"query": query}
        
        elif any(keyword in text_lower for keyword in ["fasse zusammen", "zusammenfassung", "zusammenfassen"]):
            return "browser_summary", 0.9, {}
        
        # System-Intents
        elif any(keyword in text_lower for keyword in ["öffne programm", "starte programm", "öffne anwendung"]):
            program = text_lower.split("programm", 1)[1].strip() if "programm" in text_lower else text_lower.split("anwendung", 1)[1].strip()
            return "system_open", 0.9, {"program": program}
        
        elif any(keyword in text_lower for keyword in ["schließe", "beende", "stoppe"]):
            program = None
            for part in ["schließe", "beende", "stoppe"]:
                if part in text_lower:
                    parts = text_lower.split(part, 1)
                    if len(parts) > 1:
                        program = parts[1].strip()
                        break
            
            return "system_close", 0.8, {"program": program}
        
        # Medien-Intents
        elif any(keyword in text_lower for keyword in ["spiele", "abspielen", "play"]):
            return "media_play", 0.9, {}
        
        elif any(keyword in text_lower for keyword in ["pause", "pausieren", "stopp"]):
            return "media_pause", 0.9, {}
        
        elif any(keyword in text_lower for keyword in ["lauter", "leiser", "lautstärke"]):
            direction = "up" if "lauter" in text_lower else "down" if "leiser" in text_lower else None
            return "media_volume", 0.9, {"direction": direction}
        
        elif any(keyword in text_lower for keyword in ["schneller", "langsamer", "geschwindigkeit"]):
            direction = "up" if "schneller" in text_lower else "down" if "langsamer" in text_lower else None
            return "media_speed", 0.9, {"direction": direction}
        
        # Vision-Intents
        elif any(keyword in text_lower for keyword in ["mach ein foto", "mach ein bild", "nimm ein foto"]):
            return "vision_capture", 0.9, {}
        
        elif any(keyword in text_lower for keyword in ["beschreibe", "was siehst du", "erkenne"]):
            return "vision_describe", 0.9, {}
        
        elif any(keyword in text_lower for keyword in ["lies den text", "text erkennen", "ocr"]):
            return "vision_read", 0.9, {}
        
        # Hilfe- und Info-Intents
        elif any(keyword in text_lower for keyword in ["hilfe", "help", "unterstützung"]):
            return "help", 0.9, {}
        
        elif any(keyword in text_lower for keyword in ["info", "information", "version"]):
            return "info", 0.9, {}
        
        # Fallback: Allgemeine Anfrage
        else:
            return "general_query", 0.6, {"query": text}
    
    def _extract_params(self, text, intent):
        """
        Extrahiert Parameter basierend auf der erkannten Intention.
        
        Args:
            text: Der Originaltext
            intent: Die erkannte Intention
            
        Returns:
            dict: Extrahierte Parameter
        """
        text_lower = text.lower()
        params = {}
        
        if intent == "browser_open":
            params["url"] = self._extract_url(text_lower)
        
        elif intent == "browser_search":
            for keyword in ["suche nach", "google", "finde"]:
                if keyword in text_lower:
                    params["query"] = text_lower.split(keyword, 1)[1].strip()
                    break
        
        elif intent == "system_open":
            for keyword in ["öffne", "starte"]:
                if keyword in text_lower:
                    parts = text_lower.split(keyword, 1)
                    if len(parts) > 1:
                        program_part = parts[1].strip()
                        
                        # Entferne "programm" oder "anwendung" aus dem Text
                        for suffix in ["programm", "anwendung"]:
                            if suffix in program_part:
                                program_part = program_part.replace(suffix, "").strip()
                        
                        params["program"] = program_part
                        break
        
        elif intent == "media_volume" or intent == "media_speed":
            params["direction"] = "up" if any(kw in text_lower for kw in ["lauter", "hoch", "schneller"]) else "down"
        
        return params
    
    def _extract_url(self, text):
        """
        Extrahiert eine URL aus dem Text.
        
        Args:
            text: Der Text, der eine URL enthalten könnte
            
        Returns:
            str: Die extrahierte URL oder eine leere Zeichenfolge
        """
        import re
        
        # Einfache URL-Extraktion (für vollständige URLs)
        url_match = re.search(r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[a-zA-Z0-9./-_%?&=]*', text)
        if url_match:
            return url_match.group(0)
        
        # Einfache Domain-Extraktion (z.B. "google.com")
        domain_match = re.search(r'[a-zA-Z0-9.-]+\.(com|org|net|de|info|io|app|gov|edu)', text)
        if domain_match:
            domain = domain_match.group(0)
            return f"https://{domain}"
        
        # Extrahiere nach Keywords
        keywords = ["öffne", "besuche", "gehe zu", "website", "seite"]
        for keyword in keywords:
            if keyword in text:
                parts = text.split(keyword, 1)
                if len(parts) > 1:
                    potential_url = parts[1].strip()
                    
                    # Entferne Füllwörter
                    for word in ["die", "der", "das", "eine", "einen", "website", "seite"]:
                        potential_url = potential_url.replace(f" {word} ", " ").strip()
                    
                    # Verwende das erste Wort als potenzielle Domain
                    domain = potential_url.split()[0]
                    
                    # Füge .com hinzu, falls keine TLD
                    if "." not in domain:
                        domain = f"{domain}.com"
                    
                    return f"https://{domain}"
        
        return ""
    
    def process_intent(self, intent, params, original_command):
        """
        Verarbeitet eine erkannte Intention.
        
        Args:
            intent: Die erkannte Intention
            params: Extrahierte Parameter
            original_command: Das ursprüngliche Kommando
        """
        self.logger.info(f"Verarbeite Intent: {intent}, Params: {params}")
        
        # Verarbeite basierend auf Intent-Typ
        if intent.startswith("browser_"):
            self._process_browser_intent(intent, params, original_command)
        
        elif intent.startswith("system_"):
            self._process_system_intent(intent, params, original_command)
        
        elif intent.startswith("media_"):
            self._process_media_intent(intent, params, original_command)
        
        elif intent.startswith("vision_"):
            self._process_vision_intent(intent, params, original_command)
        
        elif intent in ["help", "info"]:
            self._process_info_intent(intent, params, original_command)
        
        else:  # general_query
            # Leite allgemeine Anfragen an den KI-Assistenten weiter
            self.event_manager.publish("assistant.process_query", {
                "query": original_command,
                "intent": intent,
                "params": params
            })
    
    def _process_browser_intent(self, intent, params, original_command):
        """
        Verarbeitet Browser-bezogene Intents und veröffentlicht entsprechende Events.
        
        Args:
            intent: Die erkannte Intention (browser_open, browser_search, etc.)
            params: Extrahierte Parameter (URL, Suchbegriff, etc.)
            original_command: Das ursprüngliche Sprachkommando
        """
        if intent == "browser_open":
        url = params.get("url", "")
        
        if not url:
            self.logger.warning("Keine URL für browser_open-Intent gefunden")
            self.event_manager.publish("assistant.response_ready", 
                                      "Ich konnte keine Website in deinem Befehl erkennen. Bitte gib die Website an, die ich öffnen soll.")
            return
        
        # Stelle sicher, dass die URL ein Protokoll hat
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        # Veröffentliche Event zum Öffnen der URL
        self.event_manager.publish("browser.navigate_to", {
            "url": url,
            "source": "voice_command"
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", f"Ich öffne {url} für dich.")
    
    elif intent == "browser_search":
        query = params.get("query", "")
        
        if not query:
            self.logger.warning("Kein Suchbegriff für browser_search-Intent gefunden")
            self.event_manager.publish("assistant.response_ready", 
                                      "Ich konnte keinen Suchbegriff erkennen. Wonach soll ich suchen?")
            return
        
        # Erstelle Such-URL für Google
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        # Veröffentliche Event zum Öffnen der Such-URL
        self.event_manager.publish("browser.navigate_to", {
            "url": search_url,
            "source": "voice_command",
            "is_search": True,
            "search_query": query
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", f"Ich suche nach '{query}' für dich.")
    
    elif intent == "browser_summary":
        # Veröffentliche Event zum Zusammenfassen der aktuellen Seite
        self.event_manager.publish("browser.summarize_page", {
            "source": "voice_command"
        })
        
        # Informiere den Nutzer, dass die Zusammenfassung in Bearbeitung ist
        self.event_manager.publish("assistant.response_ready", 
                                  "Ich erstelle eine Zusammenfassung der aktuellen Webseite. Einen Moment bitte...")
    
    elif intent == "browser_navigate":
        # Behandle Navigation innerhalb der Seite (z.B. "klicke auf den Link")
        action = None
        target = None
        
        # Extrahiere Navigationsdetails aus dem Originalbefehl
        if "zurück" in original_command.lower():
            action = "back"
        elif "vorwärts" in original_command.lower() or "weiter" in original_command.lower():
            action = "forward"
        elif "aktualisieren" in original_command.lower() or "neu laden" in original_command.lower():
            action = "refresh"
        elif "klicke" in original_command.lower() or "klick" in original_command.lower():
            action = "click"
            # Versuche, das Ziel zu extrahieren
            for keyword in ["auf", "den", "die", "das"]:
                if f"klicke {keyword}" in original_command.lower() or f"klick {keyword}" in original_command.lower():
                    parts = original_command.lower().split(f"klick{'e' if 'klicke' in original_command.lower() else ''} {keyword}", 1)
                    if len(parts) > 1:
                        target = parts[1].strip()
                        break
        
        # Veröffentliche entsprechendes Event für Browser-Navigation
        if action:
            self.event_manager.publish("browser.navigate", {
                "action": action,
                "target": target,
                "source": "voice_command"
            })
            
            # Bestätige dem Nutzer
            if action == "back":
                self.event_manager.publish("assistant.response_ready", "Ich gehe zurück zur vorherigen Seite.")
            elif action == "forward":
                self.event_manager.publish("assistant.response_ready", "Ich gehe zur nächsten Seite.")
            elif action == "refresh":
                self.event_manager.publish("assistant.response_ready", "Ich aktualisiere die Seite.")
            elif action == "click" and target:
                self.event_manager.publish("assistant.response_ready", f"Ich klicke auf '{target}'.")
            else:
                self.event_manager.publish("assistant.response_ready", "Ich führe die Navigation aus.")
        else:
            self.logger.warning(f"Unbekannte Browser-Navigation: {original_command}")
            self.event_manager.publish("assistant.response_ready", 
                                      "Ich konnte nicht verstehen, wie ich navigieren soll. Bitte präzisiere deinen Befehl.")

def _process_system_intent(self, intent, params, original_command):
    """
    Verarbeitet System-bezogene Intents (Anwendungen öffnen/schließen, Systemsteuerung).
    
    Args:
        intent: Die erkannte Intention (system_open, system_close, system_control)
        params: Extrahierte Parameter
        original_command: Das ursprüngliche Sprachkommando
    """
    if intent == "system_open":
        program = params.get("program", "")
        
        if not program:
            self.event_manager.publish("assistant.response_ready", 
                                      "Ich konnte nicht erkennen, welches Programm ich öffnen soll.")
            return
        
        # Veröffentliche Event zum Öffnen der Anwendung
        self.event_manager.publish("system.launch_application", {
            "app_name": program,
            "source": "voice_command"
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", f"Ich öffne {program} für dich.")
    
    elif intent == "system_close":
        program = params.get("program", "")
        
        if program:
            # Veröffentliche Event zum Schließen einer bestimmten Anwendung
            self.event_manager.publish("system.close_application", {
                "app_name": program,
                "source": "voice_command"
            })
            
            # Bestätige dem Nutzer
            self.event_manager.publish("assistant.response_ready", f"Ich schließe {program}.")
        else:
            # Schließe das aktuelle Fenster
            self.event_manager.publish("system.close_active_window", {
                "source": "voice_command"
            })
            
            # Bestätige dem Nutzer
            self.event_manager.publish("assistant.response_ready", "Ich schließe das aktuelle Fenster.")
    
    elif intent == "system_control":
        # Extrahiere Steuerungsdetails aus dem Originalbefehl
        action = None
        if "maximiere" in original_command.lower():
            action = "maximize"
        elif "minimiere" in original_command.lower():
            action = "minimize"
        elif "hinaus" in original_command.lower() or "vollbild" in original_command.lower():
            action = "fullscreen"
        
        if action:
            # Veröffentliche entsprechendes Event für Systemsteuerung
            self.event_manager.publish("system.window_control", {
                "action": action,
                "source": "voice_command"
            })
            
            # Bestätige dem Nutzer
            action_text = {"maximize": "maximiere", "minimize": "minimiere", "fullscreen": "zeige im Vollbild"}
            self.event_manager.publish("assistant.response_ready", f"Ich {action_text.get(action, '')} das Fenster.")
        else:
            self.logger.warning(f"Unbekannte Systemsteuerung: {original_command}")
            self.event_manager.publish("assistant.response_ready", 
                                      "Ich konnte nicht verstehen, wie ich das System steuern soll.")

def _process_media_intent(self, intent, params, original_command):
    """
    Verarbeitet Medien-bezogene Intents (Abspielen, Pause, Lautstärke, Geschwindigkeit).
    
    Args:
        intent: Die erkannte Intention (media_play, media_pause, media_volume, media_speed)
        params: Extrahierte Parameter
        original_command: Das ursprüngliche Sprachkommando
    """
    if intent == "media_play":
        # Veröffentliche Event zum Abspielen von Medien
        self.event_manager.publish("media.control", {
            "action": "play",
            "source": "voice_command"
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", "Ich starte die Wiedergabe.")
    
    elif intent == "media_pause":
        # Veröffentliche Event zum Pausieren von Medien
        self.event_manager.publish("media.control", {
            "action": "pause",
            "source": "voice_command"
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", "Ich pausiere die Wiedergabe.")
    
    elif intent == "media_volume":
        direction = params.get("direction", "")
        
        if direction:
            # Veröffentliche Event zur Lautstärkeanpassung
            self.event_manager.publish("media.volume", {
                "direction": direction,
                "source": "voice_command"
            })
            
            # Bestätige dem Nutzer
            direction_text = "erhöhe" if direction == "up" else "verringere"
            self.event_manager.publish("assistant.response_ready", f"Ich {direction_text} die Lautstärke.")
    
    elif intent == "media_speed":
        direction = params.get("direction", "")
        
        if direction:
            # Veröffentliche Event zur Geschwindigkeitsanpassung
            self.event_manager.publish("media.speed", {
                "direction": direction,
                "source": "voice_command"
            })
            
            # Bestätige dem Nutzer
            direction_text = "erhöhe" if direction == "up" else "verringere"
            self.event_manager.publish("assistant.response_ready", f"Ich {direction_text} die Wiedergabegeschwindigkeit.")

def _process_vision_intent(self, intent, params, original_command):
    """
    Verarbeitet Bild-bezogene Intents (Foto aufnehmen, Szene beschreiben, Text lesen).
    
    Args:
        intent: Die erkannte Intention (vision_capture, vision_describe, vision_read)
        params: Extrahierte Parameter
        original_command: Das ursprüngliche Sprachkommando
    """
    if intent == "vision_capture":
        # Optional: Dateiname oder Format extrahieren
        filename = None
        format = "jpg"
        
        # Veröffentliche Event zum Aufnehmen eines Bildes
        self.event_manager.publish("vision.capture_and_save", {
            "filename": filename,
            "format": format,
            "source": "voice_command"
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", "Ich nehme ein Foto auf.")
    
    elif intent == "vision_describe":
        # Veröffentliche Event zur Bildanalyse
        self.event_manager.publish("vision.analyze_scene", {
            "source": "voice_command"
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", "Ich beschreibe, was ich sehe. Einen Moment bitte...")
    
    elif intent == "vision_read":
        # Veröffentliche Event zur Texterkennung
        self.event_manager.publish("vision.read_text", {
            "source": "voice_command"
        })
        
        # Bestätige dem Nutzer
        self.event_manager.publish("assistant.response_ready", "Ich lese den Text, den ich sehe. Einen Moment bitte...")

def _process_info_intent(self, intent, params, original_command):
    """
    Verarbeitet Hilfe- und Info-Intents.
    
    Args:
        intent: Die erkannte Intention (help, info)
        params: Extrahierte Parameter
        original_command: Das ursprüngliche Sprachkommando
    """
    if intent == "help":
        # Erstelle Hilfenachricht
        help_message = (
            "Hier sind einige Befehle, die du verwenden kannst:\n"
            "- 'Öffne [Website]' zum Öffnen einer Website\n"
            "- 'Suche nach [Begriff]' für eine Websuche\n"
            "- 'Fasse die Seite zusammen' für eine Zusammenfassung\n"
            "- 'Öffne [Programm]' zum Starten einer Anwendung\n"
            "- 'Schließe [Programm]' zum Beenden einer Anwendung\n"
            "- 'Mach ein Foto' zum Aufnehmen eines Bildes\n"
            "- 'Beschreibe, was du siehst' für eine Bildanalyse\n"
            "- 'Lies den Text' für Texterkennung\n"
            "- Mediensteuerung: 'Abspielen', 'Pause', 'Lauter', 'Leiser', 'Schneller', 'Langsamer'\n"
        )
        
        # Sende Hilfenachricht
        self.event_manager.publish("assistant.response_ready", help_message)
    
    elif intent == "info":
        # Hole Systeminfo
        import platform
        import sys
        from datetime import datetime
        
        system_info = {
            "system_name": self.config["system"]["name"],
            "version": self.config["system"]["version"],
            "python_version": sys.version.split()[0],
            "platform": platform.system(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Erstelle Info-Nachricht
        info_message = (
            f"System: {system_info['system_name']} Version {system_info['version']}\n"
            f"Laufend auf {system_info['platform']} mit Python {system_info['python_version']}\n"
            f"Aktuelles Datum und Uhrzeit: {system_info['date']}"
        )
        
        # Sende Info-Nachricht
        ### 9.2 KI-Manager für Sprachmodell (LLM)

```python
# nlp/llm_manager.py
import os
import logging
import torch
import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class LLMManager:
    """Verwaltet das große Sprachmodell (LLM) für Konversationen und Textgenerierung."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("LLMManager")
        self.config = config
        self.event_manager = event_manager
        
        # Modellpfad
        models_dir = Path(config["system"]["models_dir"])
        self.model_dir = models_dir / "llm"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Modellkonfiguration
        self.model_name = config["nlp"]["llm_model"]
        self.quantization = config["nlp"]["llm_quantization"]
        
        # Gerät (CPU/GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"Verwende Device für LLM: {self.device}")
        
        # Initialisierung des Modells
        self.tokenizer = None
        self.model = None
        self.generator = None
        
        # Geschichte der Konversation
        self.conversation_history = []
        self.max_history_length = 10  # Anzahl der zu speichernden Nachrichten
        
        # Lade das Modell
        self.load_model()
        
        # Registriere Event-Handler
        self.event_manager.subscribe("assistant.process_query", self._on_process_query)
        self.event_manager.subscribe("assistant.clear_history", self._on_clear_history)
    
    def _on_process_query(self, data):
        """Handler für process_query Event."""
        if isinstance(data, dict) and "query" in data:
            query = data["query"]
            context = data.get("context", "")
            
            # Generiere Antwort
            response = self.generate_response(query, context=context)
            
            # Veröffentliche Event: Antwort bereit
            self.event_manager.publish("assistant.response_ready", response)
    
    def _on_clear_history(self, data):
        """Handler für clear_history Event."""
        self.clear_conversation_history()
    
    def load_model(self):
        """Lädt das Sprachmodell und den Tokenizer."""
        try:
            self.logger.info(f"Lade LLM-Modell: {self.model_name}")
            
            # Prüfe, ob es ein lokales Modell oder ein Hugging Face-Modell ist
            model_path = self.model_dir / self.model_name
            if model_path.exists():
                use_path = str(model_path)
                self.logger.info(f"Verwende lokales Modell: {use_path}")
            else:
                use_path = self.model_name
                self.logger.info(f"Lade Modell von Hugging Face: {use_path}")
            
            # Tokenizer laden
            self.tokenizer = AutoTokenizer.from_pretrained(use_path)
            
            # Modell laden mit Quantisierung
            if self.device == "cuda":
                self.logger.info(f"Lade quantisiertes Modell mit {self.quantization}")
                
                # Modell mit 8-Bit-Quantisierung laden (für geringeren GPU-Speicherverbrauch)
                self.model = AutoModelForCausalLM.from_pretrained(
                    use_path,
                    device_map="auto",
                    load_in_8bit=True,
                    trust_remote_code=True
                )
            else:
                self.logger.info("Lade Modell für CPU")
                self.model = AutoModelForCausalLM.from_pretrained(
                    use_path,
                    device_map="auto",
                    trust_remote_code=True
                )
            
            # Text-Generator-Pipeline einrichten
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto"
            )
            
            self.logger.info("LLM-Modell erfolgreich geladen.")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Laden des LLM-Modells: {e}")
            raise
    
    def add_to_conversation_history(self, role, content):
        """
        Fügt eine Nachricht zur Konversationsgeschichte hinzu.
        
        Args:
            role: Die Rolle (user, assistant, system)
            content: Der Inhalt der Nachricht
        """
        self.conversation_history.append({"role": role, "content": content})
        
        # Beschränke die Länge der Geschichte
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def clear_conversation_history(self):
        """Löscht die Konversationsgeschichte."""
        self.conversation_history = []
        self.logger.info("Konversationsgeschichte gelöscht")
    
    def generate_response(self, prompt, max_length=1024, temperature=0.7, context=""):
        """
        Generiert eine Antwort basierend auf dem gegebenen Prompt und Kontext.
        
        Args:
            prompt: Der Eingabetext
            max_length: Maximale Länge der generierten Antwort
            temperature: Temperatur für die Textgenerierung (höher = kreativer)
            context: Zusätzlicher Kontext für die Generierung
            
        Returns:
            str: Die generierte Antwort
        """
        try:
            # Füge den Prompt zur Konversationsgeschichte hinzu
            self.add_to_conversation_history("user", prompt)
            
            # Erstelle einen formatierten Prompt mit Konversationsgeschichte
            formatted_prompt = self._format_conversation_history(context)
            
            self.logger.debug(f"Generiere Antwort für Prompt: {prompt}")
            
            # Führe die Textgenerierung durch
            response = self.generator(
                formatted_prompt,
                max_length=max_length,
                do_sample=True,
                temperature=temperature,
                top_p=0.95,
                top_k=50,
                num_return_sequences=1
            )[0]["generated_text"]
            
            # Extrahiere die Antwort (ohne den ursprünglichen Prompt)
            answer = self._extract_assistant_response(response, formatted_prompt)
            
            # Füge die Antwort zur Konversationsgeschichte hinzu
            self.add_to_conversation_history("assistant", answer)
            
            return answer
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Textgenerierung: {e}")
            return "Es tut mir leid, ich konnte keine Antwort generieren. Bitte versuche es erneut."
    
    def _format_conversation_history(self, context=""):
        """
        Formatiert die Konversationsgeschichte für das Modell.
        
        Args:
            context: Zusätzlicher Kontext
            
        Returns:
            str: Formatierter Prompt
        """
        # Format basierend auf dem Modelltyp anpassen
        # Für Mistral-Modelle verwenden wir das Chatml-Format
        system_prompt = (
            "Du bist ein hilfreicher Assistent für eine blinde Person. "
            "Deine Antworten sollten klar, präzise und verständlich sein. "
            "Beschreibe visuelle Informationen detailliert und bedenke, dass der Nutzer "
            "nicht sehen kann, was auf dem Bildschirm passiert."
        )
        
        if context:
            system_prompt += f"\n\nKontext: {context}"
        
        # Für Mistral-Modelle
        if "mistral" in self.model_name.lower():
            formatted_prompt = f"<s>[INST] {system_prompt} [/INST]</s>\n"
            
            for message in self.conversation_history:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    formatted_prompt += f"<s>[INST] {content} [/INST]"
                elif role == "assistant":
                    formatted_prompt += f" {content}</s>\n"
            
            # Hinzufügen des abschließenden Tokens für die Antwort des Assistenten
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                formatted_prompt += " "
            
            return formatted_prompt
        
        # Für andere Modelle (z.B. Llama)
        else:
            formatted_prompt = f"### System:\n{system_prompt}\n\n"
            
            for message in self.conversation_history:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    formatted_prompt += f"### User:\n{content}\n\n"
                elif role == "assistant":
                    formatted_prompt += f"### Assistant:\n{content}\n\n"
            
            # Hinzufügen des abschließenden Tokens für die Antwort des Assistenten
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                formatted_prompt += "### Assistant:\n"
            
            return formatted_prompt
    
    def _extract_assistant_response(self, full_response, prompt):
        """
        Extrahiert die Antwort des Assistenten aus der vollständigen Modellantwort.
        
        Args:
            full_response: Die vollständige Antwort des Modells
            prompt: Der ursprüngliche Prompt
            
        Returns:
            str: Die extrahierte Antwort des Assistenten
        """
        # Entferne den ursprünglichen Prompt
        answer = full_response[len(prompt):].strip()
        
        # Entferne Formatierungsmarker basierend auf dem Modelltyp
        if "mistral" in self.model_name.lower():
            # Für Mistral-Modelle, entferne alle Tokens nach </s>
            if "</s>" in answer:
                answer = answer.split("</s>")[0].strip()
        else:
            # Für andere Modelle, entferne alle Tokens nach "### User:"
            if "### User:" in answer:
                answer = answer.split("### User:")[0].strip()
            # Oder nach "### System:"
            elif "### System:" in answer:
                answer = answer.split("### System:")[0].strip()
        
        return answer
    
    def generate_structured_response(self, system_prompt, user_query, max_length=1024):
        """
        Generiert eine strukturierte Antwort mit System- und Nutzerprompt.
        
        Args:
            system_prompt: Der Systemprompt
            user_query: Die Nutzeranfrage
            max_length: Maximale Länge der generierten Antwort
            
        Returns:
            str: Die generierte Antwort
        """
        try:
            # Formatiere den Prompt für Instruction-abgestimmte Modelle
            if "mistral" in self.model_name.lower():
                prompt = f"<s>[INST] {system_prompt}\n\n{user_query} [/INST]"
            else:
                prompt = f"""
### System:
{system_prompt}

### User:
{user_query}

### Assistant:
"""
            
            # Generiere die Antwort
            response = self.generate_response(prompt, max_length=max_length)
            
            return response
        
        except Exception as e:
            self.logger.error(f"Fehler bei der strukturierten Textgenerierung: {e}")
            return ""
```

### 9.3 Kontextgedächtnis und Personalisierung

```python
# nlp/context_memory.py
import logging
import time
import json
from pathlib import Path
import sqlite3
import threading
import os

class ContextMemory:
    """Verwaltet das Kontextgedächtnis für personalisierte Interaktionen."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("ContextMemory")
        self.config = config
        self.event_manager = event_manager
        
        # Maximale Anzahl an Kontextelementen
        self.max_items = config["learning"]["context_memory_items"]
        
        # Daten-Verzeichnis
        data_dir = Path(config["system"]["data_dir"])
        os.makedirs(data_dir, exist_ok=True)
        self.memory_file = data_dir / "context_memory.db"
        
        # Lock für Thread-Sicherheit
        self.db_lock = threading.Lock()
        
        # Initialisiere die Datenbank
        self._init_database()
        
        # Registriere Event-Handler
        self.event_manager.subscribe("assistant.response_ready", self._on_response_ready)
        self.event_manager.subscribe("nlp.intent_recognized", self._on_intent_recognized)
        self.event_manager.subscribe("user.preference_updated", self._on_preference_updated)
    
    def _on_response_ready(self, response):
        """Handler für response_ready Event."""
        # Speichere die letzte Antwort im Kontext
        self.store_fact("last_assistant_response", response)
    
    def _on_intent_recognized(self, data):
        """Handler für intent_recognized Event."""
        if isinstance(data, dict):
            intent = data.get("intent", "")
            confidence = data.get("confidence", 0.0)
            
            # Speichere die letzte Intention im Kontext
            self.store_fact("last_recognized_intent", intent, confidence)
    
    def _on_preference_updated(self, data):
        """Handler für preference_updated Event."""
        if isinstance(data, dict):
            category = data.get("category", "")
            key = data.get("key", "")
            value = data.get("value", "")
            
            if category and key and value:
                # Speichere die aktualisierte Präferenz
                self.store_preference(category, key, value)
    
    def _init_database(self):
        """Initialisiert die SQLite-Datenbank für das Kontextgedächtnis."""
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                # Tabelle für allgemeine Fakten
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY,
                    key TEXT UNIQUE,
                    value TEXT,
                    confidence REAL,
                    last_updated INTEGER
                )
                ''')
                
                # Tabelle für Konversationshistorie
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY,
                    timestamp INTEGER,
                    user_input TEXT,
                    system_response TEXT
                )
                ''')
                
                # Tabelle für Nutzervorlieben
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    key TEXT,
                    value TEXT,
                    confidence REAL,
                    last_updated INTEGER,
                    UNIQUE(category, key)
                )
                ''')
                
                conn.commit()
                conn.close()
                
                self.logger.info("Kontextgedächtnis-Datenbank initialisiert.")
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Initialisierung der Kontextgedächtnis-Datenbank: {e}")
    
    def store_fact(self, key, value, confidence=1.0):
        """
        Speichert einen Fakt im Kontextgedächtnis.
        
        Args:
            key: Der Schlüssel des Fakts
            value: Der Wert des Fakts
            confidence: Die Konfidenz des Fakts (0.0 - 1.0)
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                current_time = int(time.time())
                
                cursor.execute('''
                INSERT OR REPLACE INTO facts (key, value, confidence, last_updated)
                VALUES (?, ?, ?, ?)
                ''', (key, str(value), confidence, current_time))
                
                conn.commit()
                conn.close()
                
                self.logger.debug(f"Fakt gespeichert: {key} = {value}")
                
                # Veröffentliche Event: Fakt aktualisiert
                self.event_manager.publish("context.fact_updated", {
                    "key": key,
                    "value": value,
                    "confidence": confidence
                })
                
                return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern eines Fakts: {e}")
            return False
    
    def get_fact(self, key, default=None):
        """
        Ruft einen Fakt aus dem Kontextgedächtnis ab.
        
        Args:
            key: Der Schlüssel des Fakts
            default: Der Standardwert, falls der Fakt nicht existiert
            
        Returns:
            Der Wert des Fakts oder der Standardwert
        """
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                cursor.execute('SELECT value FROM facts WHERE key = ?', (key,))
                result = cursor.fetchone()
                
                conn.close()
                
                if result:
                    return result[0]
                else:
                    return default
        
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen eines Fakts: {e}")
            return default
    
    def store_conversation(self, user_input, system_response):
        """
        Speichert einen Konversationseintrag.
        
        Args:
            user_input: Die Nutzereingabe
            system_response: Die Systemantwort
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                current_time = int(time.time())
                
                cursor.execute('''
                INSERT INTO conversation_history (timestamp, user_input, system_response)
                VALUES (?, ?, ?)
                ''', (current_time, user_input, system_response))
                
                # Lösche alte Einträge, wenn die maximale Anzahl überschritten wird
                cursor.execute('''
                DELETE FROM conversation_history
                WHERE id NOT IN (
                    SELECT id FROM conversation_history
                    ORDER BY timestamp DESC
                    LIMIT ?
                )
                ''', (self.max_items,))
                
                conn.commit()
                conn.close()
                
                self.logger.debug("Konversationseintrag gespeichert")
                
                # Veröffentliche Event: Konversation gespeichert
                self.event_manager.publish("context.conversation_stored", {
                    "timestamp": current_time,
                    "user_input": user_input,
                    "system_response": system_response
                })
                
                return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern eines Konversationseintrags: {e}")
            return False
    
    def get_recent_conversations(self, limit=5):
        """
        Ruft die neuesten Konversationseinträge ab.
        
        Args:
            limit: Maximale Anzahl der abzurufenden Einträge
            
        Returns:
            list: Liste der Konversationseinträge
        """
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                cursor.execute('''
                SELECT timestamp, user_input, system_response 
                FROM conversation_history
                ORDER BY timestamp DESC
                LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                conn.close()
                
                conversations = []
                for timestamp, user_input, system_response in results:
                    conversations.append({
                        "timestamp": timestamp,
                        "user_input": user_input,
                        "system_response": system_response
                    })
                
                return conversations
        
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen der Konversationshistorie: {e}")
            return []
    
    def store_preference(self, category, key, value, confidence=1.0):
        """
        Speichert eine Nutzervorliebe.
        
        Args:
            category: Die Kategorie der Vorliebe (z.B. "ui", "speech")
            key: Der Schlüssel der Vorliebe
            value: Der Wert der Vorliebe
            confidence: Die Konfidenz der Vorliebe (0.0 - 1.0)
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                current_time = int(time.time())
                
                cursor.execute('''
                INSERT OR REPLACE INTO preferences (category, key, value, confidence, last_updated)
                VALUES (?, ?, ?, ?, ?)
                ''', (category, key, str(value), confidence, current_time))
                
                conn.commit()
                conn.close()
                
                self.logger.debug(f"Präferenz gespeichert: {category}.{key} = {value}")
                
                # Veröffentliche Event: Präferenz aktualisiert
                self.event_manager.publish("context.preference_updated", {
                    "category": category,
                    "key": key,
                    "value": value,
                    "confidence": confidence
                })
                
                return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern einer Präferenz: {e}")
            return False
    
    def get_preference(self, category, key, default=None):
        """
        Ruft eine Nutzervorliebe ab.
        
        Args:
            category: Die Kategorie der Vorliebe
            key: Der Schlüssel der Vorliebe
            default: Der Standardwert, falls die Vorliebe nicht existiert
            
        Returns:
            Der Wert der Vorliebe oder der Standardwert
        """
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                cursor.execute('SELECT value FROM preferences WHERE category = ? AND key = ?', 
                              (category, key))
                result = cursor.fetchone()
                
                conn.close()
                
                if result:
                    return result[0]
                else:
                    return default
        
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen einer Präferenz: {e}")
            return default
    
    def get_all_preferences(self, category=None):
        """
        Ruft alle Nutzervorlieben ab, optional gefiltert nach Kategorie.
        
        Args:
            category: Optional, die Kategorie der Vorlieben
            
        Returns:
            dict: Dictionary mit den Vorlieben
        """
        try:
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                if category:
                    cursor.execute('''
                    SELECT category, key, value FROM preferences
                    WHERE category = ?
                    ORDER BY category, key
                    ''', (category,))
                else:
                    cursor.execute('''
                    SELECT category, key, value FROM preferences
                    ORDER BY category, key
                    ''')
                
                results = cursor.fetchall()
                conn.close()
                
                preferences = {}
                for cat, key, value in results:
                    if cat not in preferences:
                        preferences[cat] = {}
                    preferences[cat][key] = value
                
                return preferences
        
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen aller Präferenzen: {e}")
            return {}
    
    def build_context_for_llm(self, max_tokens=1000):
        """
        Erstellt einen Kontext für das LLM basierend auf gespeicherten Informationen.
        
        Args:
            max_tokens: Maximale Anzahl der Tokens für den Kontext
            
        Returns:
            str: Der erstellte Kontext
        """
        try:
            # Hole die neuesten Konversationen
            conversations = self.get_recent_conversations(3)
            
            # Hole die wichtigsten Fakten
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                cursor.execute('''
                SELECT key, value FROM facts
                ORDER BY confidence DESC, last_updated DESC
                LIMIT 10
                ''')
                
                facts = cursor.fetchall()
                
                # Hole die wichtigsten Präferenzen
                cursor.execute('''
                SELECT category, key, value FROM preferences
                ORDER BY confidence DESC, last_updated DESC
                LIMIT 10
                ''')
                
                preferences = cursor.fetchall()
                
                conn.close()
            
            # Baue den Kontext
            context = "### Nutzerkontext ###\n"
            
            # Fakten hinzufügen
            if facts:
                context += "\nBekannte Fakten über den Nutzer:\n"
                for key, value in facts:
                    context += f"- {key}: {value}\n"
            
            # Präferenzen hinzufügen
            if preferences:
                context += "\nNutzervorlieben:\n"
                for category, key, value in preferences:
                    context += f"- {category} - {key}: {value}\n"
            
            # Konversationshistorie hinzufügen
            if conversations:
                context += "\nLetzte Konversationen:\n"
                for conv in reversed(conversations):
                    context += f"Nutzer: {conv['user_input']}\n"
                    context += f"System: {conv['system_response']}\n\n"
            
            # Veröffentliche Event: Kontext erstellt
            self.event_manager.publish("context.context_built", {
                "context": context,
                "max_tokens": max_tokens
            })
            
            return context
        
        except Exception as e:
            self.logger.error(f"Fehler beim Erstellen des LLM-Kontexts: {e}")
            return ""
    
    def learn_from_conversation(self, user_input, system_response):
        """
        Lernt aus einer Konversation, extrahiert Fakten und Präferenzen.
        
        Args:
            user_input: Die Nutzereingabe
            system_response: Die Systemantwort
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            # Speichere die Konversation
            self.store_conversation(user_input, system_response)
            
            # Hier könnte eine fortgeschrittene Analyse der Konversation erfolgen,
            # um automatisch Fakten und Präferenzen zu extrahieren
            # Dies würde normalerweise mit einer speziellen NLP-Komponente umgesetzt
            
            # Veröffentliche Event: Aus Konversation gelernt
            self.event_manager.publish("context.learned_from_conversation", {
                "user_input": user_input,
                "system_response": system_response
            })
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Lernen aus der Konversation: {e}")
            return False
    
    def sync_with_mobile(self, mobile_data):
        """
        Synchronisiert das Kontextgedächtnis mit einem Mobilgerät.
        
        Args:
            mobile_data: Die zu synchronisierenden Daten vom Mobilgerät
            
        Returns:
            dict: Die synchronisierten Daten
        """
        try:
            # Verarbeite die eingehenden Daten vom Mobilgerät
            if "facts" in mobile_data:
                for key, value, confidence in mobile_data["facts"]:
                    self.store_fact(key, value, confidence)
            
            if "preferences" in mobile_data:
                for category, key, value, confidence in mobile_data["preferences"]:
                    self.store_preference(category, key, value, confidence)
            
            if "conversations" in mobile_data:
                for user_input, system_response in mobile_data["conversations"]:
                    self.store_conversation(user_input, system_response)
            
            # Erstelle Daten für die Rücksynchronisierung
            with self.db_lock:
                conn = sqlite3.connect(str(self.memory_file))
                cursor = conn.cursor()
                
                # Hole alle Fakten
                cursor.execute('''
                SELECT key, value, confidence, last_updated FROM facts
                ORDER BY last_updated DESC
                ''')
                facts = cursor.fetchall()
                
                # Hole alle Präferenzen
                cursor.execute('''
                SELECT category, key, value, confidence, last_updated FROM preferences
                ORDER BY last_updated DESC
                ''')
                preferences = cursor.fetchall()
                
                # Hole die neuesten Konversationen
                cursor.execute('''
                SELECT timestamp, user_input, system_response FROM conversation_history
                ORDER BY timestamp DESC
                LIMIT ?
                ''', (self.max_items,))
                conversations = cursor.fetchall()
                
                conn.close()
            
            # Erstelle Synchronisierungsdaten
            sync_data = {
                "facts": facts,
                "preferences": preferences,
                "conversations": conversations,
                "timestamp": int(time.time())
            }
            
            # Veröffentliche Event: Synchronisierung abgeschlossen
            self.event_manager.publish("context.sync_completed", {
                "direction": "to_mobile",
                "data_size": len(json.dumps(sync_data))
            })
            
            return sync_data
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Synchronisierung mit dem Mobilgerät: {e}")
            return None
```

### 9.4 Inhaltsanalyse und Zusammenfassung

```python
# nlp/content_analyzer.py
import os
import logging
import re
import torch
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from bs4 import BeautifulSoup

class ContentAnalyzer:
    """Analysiert und verarbeitet Inhalte von Webseiten, Dokumenten etc."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("ContentAnalyzer")
        self.config = config
        self.event_manager = event_manager
        
        # Modellpfad
        models_dir = Path(config["system"]["models_dir"])
        self.model_dir = models_dir / "nlp"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Gerät (CPU/GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"Verwende Device für Content Analysis: {self.device}")
        
        # Summarizer für Textzusammenfassungen
        self.summarizer = None
        
        # Lade Modelle
        self.load_models()
        
        # Registriere Event-Handler
        self.event_manager.subscribe("browser.summarize_page", self._on_summarize_page)
        self.event_manager.subscribe("content.analyze_text", self._on_analyze_text)
    
    def _on_summarize_page(self, data):
        """Handler für summarize_page Event."""
        if not isinstance(data, dict):
            data = {}
        
        # Hole HTML-Inhalt
        if "html_content" in data:
            html_content = data["html_content"]
            
            # Erstelle Zusammenfassung
            summary = self.summarize_webpage(html_content)
            
            # Veröffentliche Zusammenfassung
            self.event_manager.publish("browser.summary_ready", {
                "summary": summary,
                "source": data.get("source", "unknown")
            })
        else:
            self.logger.error("Kein HTML-Inhalt für die Zusammenfassung bereitgestellt")
            self.event_manager.publish("browser.summary_failed", {
                "error": "Kein HTML-Inhalt verfügbar",
                "source": data.get("source", "unknown")
            })
    
    def _on_analyze_text(self, data):
        """Handler für analyze_text Event."""
        if isinstance(data, dict) and "text" in data:
            text = data["text"]
            
            # Analysiere den Text
            result = self.analyze_text(text)
            
            # Veröffentliche Analyseergebnis
            self.event_manager.publish("content.analysis_ready", {
                "analysis": result,
                "source": data.get("source", "unknown")
            })
    
    def load_models(self):
        """Lädt die benötigten NLP-Modelle."""
        try:
            self.logger.info("Lade Zusammenfassungsmodell...")
            
            # Prüfe, ob ein lokales Modell vorhanden ist
            model_path = self.model_dir / "summarizer"
            if model_path.exists():
                summarizer_model = str(model_path)
                self.logger.info(f"Verwende lokales Summarizer-Modell: {summarizer_model}")
            else:
                # Verwende ein vortrainiertes Modell von Hugging Face
                summarizer_model = "sshleifer/distilbart-cnn-12-6"
                self.logger.info(f"Lade Summarizer-Modell von Hugging Face: {summarizer_model}")
            
            # Initialisiere den Summarizer
            self.summarizer = pipeline(
                "summarization",
                model=summarizer_model,
                tokenizer=summarizer_model,
                device=0 if self.device == "cuda" else -1
            )
            
            self.logger.info("Zusammenfassungsmodell erfolgreich geladen.")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der NLP-Modelle: {e}")
            raise
    
    def clean_html(self, html_content):
        """Bereinigt HTML-Inhalt für die Textverarbeitung."""
        try:
            # Parse HTML mit BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Entferne Skripte, Stylesheets und andere irrelevante Elemente
            for tag in soup(["script", "style", "meta", "link", "noscript", "iframe", "svg"]):
                tag.decompose()
            
            # Extrahiere den Text
            text = soup.get_text(separator='\n')
            
            # Bereinige Whitespace
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            clean_text = '\n'.join(lines)
            
            return clean_text
        
        except Exception as e:
            self.logger.error(f"Fehler bei der HTML-Bereinigung: {e}")
            return ""
    
    def extract_main_content(self, html_content):
        """Extrahiert den Hauptinhalt einer Webseite."""
        try:
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Entferne offensichtliche Navigations- und Footerbereiche
            for tag in soup.find_all(["nav", "footer", "header", "aside"]):
                tag.decompose()
            
            # Entferne Elemente mit typischen Klassen für Navigation, Werbung etc.
            nav_patterns = ["nav", "menu", "sidebar", "advertisement", "ad-", "banner", "footer", "header"]
            for pattern in nav_patterns:
                for tag in soup.find_all(class_=re.compile(pattern, re.IGNORECASE)):
                    tag.decompose()
            
            # Suche nach dem Hauptinhaltsbereich
            main_content = None
            
            # Versuche es mit typischen Content-Container-IDs/Klassen
            content_patterns = ["content", "main", "article", "post", "story"]
            for pattern in content_patterns:
                # Suche nach ID
                content = soup.find(id=re.compile(pattern, re.IGNORECASE))
                if content:
                    main_content = content
                    break
                
                # Suche nach Klasse
                content = soup.find(class_=re.compile(pattern, re.IGNORECASE))
                if content:
                    main_content = content
                    break
            
            # Wenn kein spezifischer Content-Bereich gefunden wurde, verwende <main>, <article> oder <body>
            if not main_content:
                main_content = soup.find("main") or soup.find("article") or soup.body
            
            # Extrahiere Text aus dem Hauptinhalt
            if main_content:
                for tag in main_content(["script", "style"]):
                    tag.decompose()
                
                text = main_content.get_text(separator='\n')
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                return '\n'.join(lines)
            else:
                # Fallback: verwende den gesamten bereinigten Text
                return self.clean_html(html_content)
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Extraktion des Hauptinhalts: {e}")
            return self.clean_html(html_content)
    
    def extract_article_sections(self, html_content):
        """Extrahiert Abschnitte aus einem Artikel oder einer Webseite."""
        try:
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extrahiere den Titel
            title = ""
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text().strip()
            
            h1_tag = soup.find("h1")
            if h1_tag:
                title = h1_tag.get_text().strip()
            
            # Extrahiere Abschnitte basierend auf Überschriften
            sections = []
            
            # Finde den Hauptinhaltsbereich
            main_content = None
            content_tags = ["main", "article", "div"]
            content_patterns = ["content", "main", "article", "post", "story"]
            
            for tag in content_tags:
                for pattern in content_patterns:
                    elements = soup.find_all(tag, class_=re.compile(pattern, re.IGNORECASE))
                    elements.extend(soup.find_all(tag, id=re.compile(pattern, re.IGNORECASE)))
                    if elements:
                        main_content = elements[0]  # Verwende den ersten gefundenen
                        break
                if main_content:
                    break
            
            # Wenn kein Hauptinhalt gefunden wurde, verwende den gesamten Body
            if not main_content:
                main_content = soup.body
            
            if main_content:
                # Finde alle Überschriften im Hauptinhalt
                headings = main_content.find_all(["h1", "h2", "h3", "h4"])
                
                # Extrahiere Abschnitte basierend auf Überschriften
                for i, heading in enumerate(headings):
                    section_title = heading.get_text().strip()
                    
                    # Sammle den Inhalt bis zur nächsten Überschrift
                    content = []
                    elem = heading.next_sibling
                    
                    while elem and (i == len(headings) - 1 or elem != headings[i + 1]):
                        if elem.name and elem.name.startswith('h') and len(elem.name) == 2 and int(elem.name[1]) <= int(heading.name[1]):
                            break
                        
                        if isinstance(elem, str):
                            if elem.strip():
                                content.append(elem.strip())
                        elif elem.name in ["p", "li", "div", "span"]:
                            text = elem.get_text().strip()
                            if text:
                                content.append(text)
                        
                        try:
                            elem = elem.next_sibling
                        except AttributeError:
                            break
                    
                    if section_title and content:
                        sections.append({
                            "title": section_title,
                            "content": "\n".join(content)
                        })
                
                # Wenn keine Abschnitte gefunden wurden, erstelle Abschnitte aus Absätzen
                if not sections:
                    paragraphs = main_content.find_all("p")
                    
                    current_section = {"title": "Inhalt", "content": ""}
                    section_content = []
                    
                    for p in paragraphs:
                        text = p.get_text().strip()
                        if text:
                            section_content.append(text)
                    
                    if section_content:
                        current_section["content"] = "\n".join(section_content)
                        sections.append(current_section)
            
            # Füge den Titel als ersten Abschnitt hinzu, wenn noch keine Abschnitte vorhanden sind
            if not sections and title:
                sections.append({
                    "title": "Titel",
                    "content": title
                })
            
            return sections
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Extraktion von Artikelabschnitten: {e}")
            return []
    
    def summarize_text(self, text, max_length=150, min_length=50):
        """Erstellt eine Zusammenfassung des Textes."""
        try:
            if not text or len(text.split()) < min_length:
                return text
            
            if not self.summarizer:
                self.logger.warning("Summarizer nicht initialisiert.")
                return text[:max_length * 2] + "..."
            
            # Teile langen Text in Abschnitte auf, um das Token-Limit nicht zu überschreiten
            max_chunk_length = 1024  # ca. 1024 Tokens
            text_chunks = []
            
            words = text.split()
            chunk = []
            word_count = 0
            
            for word in words:
                chunk.append(word)
                word_count += 1
                
                if word_count >= max_chunk_length:
                    text_chunks.append(" ".join(chunk))
                    chunk = []
                    word_count = 0
            
            if chunk:
                text_chunks.append(" ".join(chunk))
            
            # Fasse jeden Abschnitt zusammen
            summaries = []
            
            for chunk in text_chunks:
                if len(chunk.split()) < min_length:
                    summaries.append(chunk)
                    continue
                
                summary = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )[0]["summary_text"]
                
                summaries.append(summary)
            
            # Kombiniere die Zusammenfassungen
            final_summary = " ".join(summaries)
            
            return final_summary
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Textzusammenfassung: {e}")
            return text[:max_length * 2] + "..."
    
    def summarize_webpage(self, html_content):
        """Erstellt eine Zusammenfassung einer Webseite."""
        try:
            # Extrahiere den Hauptinhalt
            main_content = self.extract_main_content(html_content)
            
            # Erstelle die Zusammenfassung
            if main_content:
                summary = self.summarize_text(main_content)
                return summary
            else:
                return "Konnte keinen relevanten Inhalt auf der Webseite finden."
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Webseiten-Zusammenfassung: {e}")
            return "Fehler bei der Analyse der Webseite."
    
    def summarize_sections(self, html_content):
        """Erstellt Zusammenfassungen für einzelne Abschnitte einer Webseite."""
        try:
            # Extrahiere Abschnitte
            sections = self.extract_article_sections(html_content)
            
            # Erstelle Zusammenfassungen für jeden Abschnitt
            summarized_sections = []
            
            for section in sections:
                title = section["title"]
                content = section["content"]
                
                if len(content.split()) > 50:  # Nur längere Abschnitte zusammenfassen
                    summary = self.summarize_text(content)
                else:
                    summary = content
                
                summarized_sections.append({
                    "title": title,
                    "original_content": content,
                    "summary": summary
                })
            
            return summarized_sections
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Abschnittszusammenfassung: {e}")
            return []
    
    def analyze_text(self, text):
        """
        Führt eine vollständige Analyse eines Textes durch.
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            dict: Das Analyseergebnis
        """
        try:
            # Textstatistiken
            words = text.split()
            word_count = len(words)
            char_count = len(text)
            sentences = text.split(".")
            sentence_count = len([s for s in sentences if s.strip()])
            
            # Durchschnittliche Wort- und Satzlänge
            avg_word_length = char_count / word_count if word_count > 0 else 0
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            # Häufige Wörter (ohne Stoppwörter)
            stopwords = set(["der", "die", "das", "und", "in", "zu", "den", "dem", "mit", "auf", "ein", "eine", "ist", "von", "für"])
            word_frequencies = {}
            
            for word in words:
                word_lower = word.lower().strip(",.!?;:'\"()[]{}")
                if word_lower and word_lower not in stopwords and len(word_lower) > 2:
                    if word_lower in word_frequencies:
                        word_frequencies[word_lower] += 1
                    else:
                        word_frequencies[word_lower] = 1
            
            # Top 10 häufigste Wörter
            top_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Zusammenfassung
            summary = self.summarize_text(text)
            
            # Ergebniszusammenfassung
            result = {
                'summary': summary,
                'statistics': {
                    'word_count': word_count,
                    'character_count': char_count,
                    'sentence_count': sentence_count,
                    'avg_word_length': round(avg_word_length, 1),
                    'avg_sentence_length': round(avg_sentence_length, 1)
                },
                'frequent_words': dict(top_words)
            }
            
            return result
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Textanalyse: {e}")
            return {
                'summary': "Fehler bei der Textanalyse.",
                'error': str(e)
            }
```

## 10. Systemintegration für Windows und Browser

### 10.1 Windows-Systemintegration

```python
# integration/windows_integration.py
import os
import logging
import threading
import time
import subprocess
import pyautogui
import pygetwindow as gw
from pathlib import Path
import win32gui
import win32con
import win32api
import win32process
import ctypes
from ctypes import wintypes
import psutil

class WindowsIntegration:
    """Bietet Funktionen zur Integration mit dem Windows-Betriebssystem."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("WindowsIntegration")
        self.config = config
        self.event_manager = event_manager
        
        # Aktiviere/Deaktiviere Windows-Automation
        self.automation_enabled = config["integration"]["windows_automation"]
        
        # Windows-UI-Automation-Bibliothek
        try:
            import uiautomation as auto
            self.ui_automation = auto
            self.ui_auto_available = True
        except ImportError:
            self.logger.warning("Windows UI Automation nicht verfügbar, installiere...")
            os.system("pip install uiautomation")
            try:
                import uiautomation as auto
                self.ui_automation = auto
                self.ui_auto_available = True
            except ImportError:
                self.logger.error("Konnte Windows UI Automation nicht installieren")
                self.ui_automation = None
                self.ui_auto_available = False
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.launch_application", self._on_launch_application)
        self.event_manager.subscribe("system.close_application", self._on_close_application)
        self.event_manager.subscribe("system.close_active_window", self._on_close_active_window)
        self.event_manager.subscribe("system.window_control", self._on_window_control)
        self.event_manager.subscribe("system.simulate_keypress", self._on_simulate_keypress)
        self.event_manager.subscribe("system.simulate_mouse_click", self._on_simulate_mouse_click)
    
    def _on_launch_application(self, data):
        """Handler für launch_application Event."""
        if isinstance(data, dict) and "app_name" in data:
            app_name = data["app_name"]
            app_path = data.get("app_path")
            
            result = self.launch_application(app_name, app_path)
            
            # Veröffentliche Ergebnis
            self.event_manager.publish("system.application_launched", {
                "app_name": app_name,
                "success": result
            })
    
    def _on_close_application(self, data):
        """Handler für close_application Event."""
        if isinstance(data, dict) and "app_name" in data:
            app_name = data["app_name"]
            
            # Suche nach dem passenden Fenster
            matching_windows = [win for win in gw.getAllWindows() if app_name.lower() in win.title.lower()]
            
            if matching_windows:
                window = matching_windows[0]
                window.close()
                
                # Veröffentliche Ergebnis
                self.event_manager.publish("system.application_closed", {
                    "app_name": app_name,
                    "window_title": window.title,
                    "success": True
                })
            else:
                self.logger.warning(f"Kein Fenster für Anwendung '{app_name}' gefunden")
                
                # Veröffentliche Ergebnis
                self.event_manager.publish("system.application_closed", {
                    "app_name": app_name,
                    "success": False,
                    "error": "Anwendung nicht gefunden"
                })
    
    def _on_close_active_window(self, data):
        """Handler für close_active_window Event."""
        window = self.get_active_window()
        
        if window:
            window_title = window.title
            window.close()
            
            # Veröffentliche Ergebnis
            self.event_manager.publish("system.active_window_closed", {
                "window_title": window_title,
                "success": True
            })
        else:
            self.logger.warning("Kein aktives Fenster gefunden")
            
            # Veröffentliche Ergebnis
            self.event_manager.publish("system.active_window_closed", {
                "success": False,
                "error": "Kein aktives Fenster gefunden"
            })
    
    def _on_window_control(self, data):
        """Handler für window_control Event."""
        if isinstance(data, dict) and "action" in data:
            action = data["action"]
            window = self.get_active_window()
            
            if not window:
                self.logger.warning("Kein aktives Fenster für Fensteraktion gefunden")
                
                # Veröffentliche Ergebnis
                self.event_manager.publish("system.window_control_applied", {
                    "action": action,
                    "success": False,
                    "error": "Kein aktives Fenster gefunden"
                })
                return
            
            window_title = window.title
            success = False
            
            if action == "maximize":
                window.maximize()
                success = True
            elif action == "minimize":
                window.minimize()
                success = True
            elif action == "restore":
                window.restore()
                success = True
            elif action == "fullscreen":
                # Sende Alt+Enter für Vollbild
                pyautogui.hotkey('alt', 'enter')
                success = True
            
            # Veröffentliche Ergebnis
            self.event_manager.publish("system.window_control_applied", {
                "action": action,
                "window_title": window_title,
                "success": success
            })
    
    def _on_simulate_keypress(self, data):
        """Handler für simulate_keypress Event."""
        if isinstance(data, dict) and "key_combination" in data:
            key_combination = data["key_combination"]
            interval = data.get("interval", 0.1)
            
            result = self.simulate_keypress(key_combination, interval)
            
            # Veröffentliche Ergebnis
            self.event_manager.publish("system.keypress_simulated", {
                "key_combination": key_combination,
                "success": result
            })
    
    def _on_simulate_mouse_click(self, data):
        """Handler für simulate_mouse_click Event."""
        if isinstance(data, dict) and "x" in data and "y" in data:
            x = data["x"]
            y = data["y"]
            button = data.get("button", "left")
            
            result = self.simulate_mouse_click(x, y, button)
            
            # Veröffentliche Ergebnis
            self.event_manager.publish("system.mouse_click_simulated", {
                "x": x,
                "y": y,
                "button": button,
                "success": result
            })
    
    def get_active_window(self):
        """Gibt das aktuell aktive Fenster zurück."""
        try:
            return gw.getActiveWindow()
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen des aktiven Fensters: {e}")
            return None
    
    def get_all_windows(self):
        """Gibt eine Liste aller sichtbaren Fenster zurück."""
        try:
            windows = gw.getAllWindows()
            return [win for win in windows if win.visible and win.title]
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen aller Fenster: {e}")
            return []
    
    def focus_window(self, window):
        """Fokussiert ein Fenster."""
        try:
            if isinstance(window, str):
                # Suche nach Fenstern mit dem angegebenen Titel
                matching_windows = [win for win in gw.getAllWindows() if window.lower() in win.title.lower()]
                if matching_windows:
                    window = matching_windows[0]
                else:
                    self.logger.warning(f"Kein Fenster mit Titel '{window}' gefunden")
                    return False
            
            window.activate()
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Fokussieren des Fensters: {e}")
            return False
    
    def launch_application(self, app_name, app_path=None):
        """Startet eine Anwendung."""
        try:
            # Versuche zunächst, die Anwendung über den Namen zu starten
            if app_path is None:
                # Prüfe, ob die Anwendung bereits geöffnet ist
                matching_windows = [win for win in gw.getAllWindows() if app_name.lower() in win.title.lower()]
                if matching_windows:
                    self.logger.info(f"Anwendung '{app_name}' ist bereits geöffnet")
                    return self.focus_window(matching_windows[0])
                
                # Häufige Anwendungen
                common_apps = {
                    "notepad": "notepad.exe",
                    "notizblock": "notepad.exe",
                    "word": "winword.exe",
                    "excel": "excel.exe",
                    "powerpoint": "powerpnt.exe",
                    "browser": "chrome.exe",
                    "chrome": "chrome.exe",
                    "edge": "msedge.exe",
                    "firefox": "firefox.exe",
                    "explorer": "explorer.exe",
                    "datei-explorer": "explorer.exe",
                    "rechner": "calc.exe",
                    "calculator": "calc.exe"
                }
                
                # Prüfe, ob es sich um eine bekannte Anwendung handelt
                for key, exe in common_apps.items():
                    if key in app_name.lower():
                        app_path = exe
                        break
                
                # Wenn kein spezifischer Pfad gefunden wurde, starte über den Namen
                if app_path is None:
                    # Starte die Anwendung über Windows Run
                    subprocess.Popen(f"start {app_name}", shell=True)
                else:
                    # Starte die gefundene Anwendung
                    subprocess.Popen(app_path)
                
                # Warte, bis die Anwendung gestartet ist
                success = False
                for _ in range(10):  # Maximal 10 Sekunden warten
                    time.sleep(1)
                    matching_windows = [win for win in gw.getAllWindows() if app_name.lower() in win.title.lower()]
                    if matching_windows:
                        success = self.focus_window(matching_windows[0])
                        break
                
                if not success:
                    self.logger.warning(f"Konnte Anwendung '{app_name}' nicht starten oder finden")
                
                return success
            else:
                # Starte die Anwendung über den angegebenen Pfad
                subprocess.Popen(app_path)
                return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Starten der Anwendung '{app_name}': {e}")
            return False
    
    def simulate_keypress(self, key_combination, interval=0.1):
        """Simuliert Tastatureingaben."""
        try:
            pyautogui.hotkey(*key_combination.split('+'), interval=interval)
            return True
        except Exception as e:
            self.logger.error(f"Fehler bei der Tastensimulation: {e}")
            return False
    
    def simulate_mouse_click(self, x, y, button='left'):
        """Simuliert einen Mausklick an den angegebenen Koordinaten."""
        try:
            pyautogui.click(x=x, y=y, button=button)
            return True
        except Exception as e:
            self.logger.error(f"Fehler bei der Mausklick-Simulation: {e}")
            return False
    
    def get_element_by_automation_id(self, automation_id, timeout=5):
        """Findet ein Element über seine Automation ID."""
        if not self.ui_auto_available:
            self.logger.error("Windows UI Automation nicht verfügbar")
            return None
        
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                element = self.ui_automation.FindControl(ControlType=self.ui_automation.ControlType.Button, AutomationId=automation_id)
                if element:
                    return element
                time.sleep(0.5)
            
            self.logger.warning(f"Element mit AutomationId '{automation_id}' nicht gefunden")
            return None
        
        except Exception as e:
            self.logger.error(f"Fehler beim Suchen des Elements: {e}")
            return None
    
    def get_element_by_name(self, name, element_type=None, timeout=5):
        """Findet ein Element über seinen Namen."""
        if not self.ui_auto_available:
            self.logger.error("Windows UI Automation nicht verfügbar")
            return None
        
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                if element_type:
                    element = self.ui_automation.FindControl(ControlType=element_type, Name=name)
                else:
                    element = self.ui_automation.FindControl(Name=name)
                
                if element:
                    return element
                time.sleep(0.5)
            
            self.logger.warning(f"Element mit Name '{name}' nicht gefunden")
            return None
        
        except Exception as e:
            self.logger.error(f"Fehler beim Suchen des Elements nach Namen: {e}")
            return None
    
    def click_element(self, element):
        """Klickt auf ein UI-Element."""
        if not self.ui_auto_available:
            self.logger.error("Windows UI Automation nicht verfügbar")
            return False
        
        try:
            if isinstance(element, str):
                # Versuche, das Element über Namen zu finden
                element = self.get_element_by_name(element)
                if not element:
                    return False
            
            element.Click()
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Klicken auf das Element: {e}")
            return False
    
    def get_window_info(self, window_title=None):
        """Gibt Informationen über ein Fenster zurück."""
        try:
            if window_title:
                # Suche nach Fenstern mit dem angegebenen Titel
                matching_windows = [win for win in gw.getAllWindows() if window_title.lower() in win.title.lower()]
                if matching_windows:
                    window = matching_windows[0]
                else:
                    self.logger.warning(f"Kein Fenster mit Titel '{window_title}' gefunden")
                    return None
            else:
                # Verwende das aktive Fenster
                window = gw.getActiveWindow()
                if not window:
                    self.logger.warning("Kein aktives Fenster gefunden")
                    return None
            
            # Sammle Informationen über das Fenster
            info = {
                'title': window.title,
                'position': (window.left, window.top),
                'size': (window.width, window.height),
                'visible': window.visible,
                'minimized': window.isMinimized,
                'maximized': window.isMaximized,
                'process_id': None
            }
            
            # Versuche, die Prozess-ID zu finden
            try:
                hwnd = win32gui.FindWindow(None, window.title)
                if hwnd:
                    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                    info['process_id'] = process_id
                    
                    # Hole zusätzliche Prozessinformationen
                    try:
                        process = psutil.Process(process_id)
                        info['process_name'] = process.name()
                        info['process_path'] = process.exe()
                        info['process_cpu'] = process.cpu_percent()
                        info['process_memory'] = process.memory_info().rss
                    except:
                        pass
            except:
                pass
            
            return info
        
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen der Fensterinformationen: {e}")
            return None
    
    def get_screen_text_at_position(self, x, y, width=300, height=200):
        """
        Erfasst Text vom Bildschirm an einer bestimmten Position.
        Hilfreich für blinde Benutzer, um Text unter dem Mauszeiger zu lesen.
        
        Args:
            x, y: Koordinaten des Ausgangspunkts
            width, height: Größe des zu erfassenden Bereichs
            
        Returns:
            str: Erkannter Text oder None bei Fehler
        """
        try:
            # Screenshot des Bereichs machen
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Veröffentliche Event, um OCR auf diesem Screenshot durchzuführen
            self.event_manager.publish("vision.read_text_from_image", {
                "image": screenshot,
                "source": "screen_reader"
            })
            
            # Hinweis: Das Ergebnis wird asynchron über das Event-System zurückgegeben
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Erfassen von Text vom Bildschirm: {e}")
            return False
```

### 10.2 Browser-Integration

```python
# integration/browser_integration.py
import os
import logging
import time
import json
import threading
import queue
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class BrowserIntegration:
    """Bietet Funktionen zur Integration mit Webbrowsern."""
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("BrowserIntegration")
        self.config = config
        self.event_manager = event_manager
        
        # Browser-Konfiguration
        self.browser_type = "chrome"  # Standardmäßig Chrome verwenden
        self.headless = False  # Standardmäßig nicht im Headless-Modus
        
        # WebDriver
        self.driver = None
        self.driver_lock = threading.Lock()
        
        # Warteschlange für Browser-Befehle
        self.command_queue = queue.Queue()
        self.command_thread = None
        self.is_processing = False
        
        # Registriere Event-Handler
        self.event_manager.subscribe("browser.navigate_to", self._on_navigate_to)
        self.event_manager.subscribe("browser.navigate", self._on_navigate)
        self.event_manager.subscribe("browser.summarize_page", self._on_summarize_page)
        self.event_manager.subscribe("browser.find_element", self._on_find_element)
        self.event_manager.subscribe("browser.click_element", self._on_click_element)
        self.event_manager.subscribe("browser.fill_form", self._on_fill_form)
    
    def start_command_processing(self):
        """Startet die Verarbeitung von Browser-Befehlen."""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.command_thread = threading.Thread(target=self._process_commands)
        self.command_thread.daemon = True
        self.command_thread.start()
        
        self.logger.info("Browser-Befehlsverarbeitung gestartet")
    
    def stop_command_processing(self):
        """Stoppt die Verarbeitung von Browser-Befehlen."""
        self.is_processing = False
        
        if self.command_thread:
            self.command_thread.join(timeout=2.0)
            self.command_thread = None
        
        self.logger.info("Browser-Befehlsverarbeitung gestoppt")
    
    def _process_commands(self):
        """Thread-Funktion für die Verarbeitung von Browser-Befehlen."""
        try:
            while self.is_processing:
                try:
                    # Warte auf Befehle aus der Warteschlange
                    command, args = self.command_queue.get(timeout=1.0)
                    
                    # Führe den Befehl aus
                    try:
                        command(*args)
                    except Exception as e:
                        self.logger.error(f"Fehler bei der Ausführung eines Browser-Befehls: {e}")
                    
                    # Markiere den Befehl als erledigt
                    self.command_queue.task_done()
                
                except queue.Empty:
                    # Keine Befehle in der Warteschlange
                    continue
        
        except Exception as e:
            self.logger.error(f"Fehler im Browser-Befehlsverarbeitungs-Thread: {e}")
    
    def _on_navigate_to(self, data):
        """Handler für navigate_to Event."""
        if isinstance(data, dict) and "url" in data:
            url = data["url"]
            
            # Füge den Befehl zur Warteschlange hinzu
            self.command_queue.put((self.navigate_to, [url]))
            
            # Starte die Befehlsverarbeitung, falls noch nicht gestartet
            if not self.is_processing:
                self.start_command_processing()
    
    def _on_navigate(self, data):
        """Handler für navigate Event."""
        if isinstance(data, dict) and "action" in data:
            action = data["action"]
            target = data.get("target")
            
            if action == "back":
                self.command_queue.put((self.go_back, []))
            elif action == "forward":
                self.command_queue.put((self.go_forward, []))
            elif action == "refresh":
                self.command_queue.put((self.refresh, []))
            elif action == "click" and target:
                self.command_queue.put((self.click_most_relevant_link, [target]))
            
            # Starte die Befehlsverarbeitung, falls noch nicht gestartet
            if not self.is_processing:
                self.start_command_processing()
    
    def _on_summarize_page(self, data):
        """Handler für summarize_page Event."""
        # Hole den aktuellen Seiteninhalt
        def summarize():
            html_content = self.get_page_content()
            title = self.get_page_title()
            
            if html_content:
                # Veröffentliche Event für die Inhaltsanalyse
                self.event_manager.publish("content.analyze_text", {
                    "text": html_content,
                    "source": "browser",
                    "title": title
                })
            else:
                self.event_manager.publish("browser.summary_failed", {
                    "error": "Konnte den Seiteninhalt nicht abrufen"
                })
        
        # Füge den Befehl zur Warteschlange hinzu
        self.command_queue.put((summarize, []))
        
        # Starte die Befehlsverarbeitung, falls noch nicht gestartet
        if not self.is_processing:
            self.start_command_processing()
    
    def _on_find_element(self, data):
        """Handler für find_element Event."""
        if isinstance(data, dict) and "selector" in data:
            selector = data["selector"]
            by = data.get("by", By.CSS_SELECTOR)
            timeout = data.get("timeout", 10)
            
            # Füge den Befehl zur Warteschlange hinzu
            self.command_queue.put((self.find_element, [selector, by, timeout]))
            
            # Starte die Befehlsverarbeitung, falls noch nicht gestartet
            if not self.is_processing:
                self.start_command_processing()
    
    def _on_click_element(self, data):
        """Handler für click_element Event."""
        if isinstance(data, dict) and "selector" in data:
            selector = data["selector"]
            by = data.get("by", By.CSS_SELECTOR)
            timeout = data.get("timeout", 10)
            
            # Füge den Befehl zur Warteschlange hinzu
            self.command_queue.put((self.click_element, [selector, by, timeout]))
            
            # Starte die Befehlsverarbeitung, falls noch nicht gestartet
            if not self.is_processing:
                self.start_command_processing()
    
    def _on_fill_form(self, data):
        """Handler für fill_form Event."""
        if isinstance(data, dict) and "selector" in data and "text" in data:
            selector = data["selector"]
            text = data["text"]
            by = data.get("by", By.CSS_SELECTOR)
            timeout = data.get("timeout", 10)
            
            # Füge den Befehl zur Warteschlange hinzu
            self.command_queue.put((self.fill_form_field, [selector, text, by, timeout]))
            
            # Starte die Befehlsverarbeitung, falls noch nicht gestartet
            if not self.is_processing:
                self.start_command_processing()
    
    def initialize_browser(self, browser_type=None, headless=None):
        """Initialisiert den Browser."""
        if browser_type:
            self.browser_type = browser_type.lower()
        
        if headless is not None:
            self.headless = headless
        
        with self.driver_lock:
            # Schließe vorherigen Browser, falls vorhanden
            self._close_browser()
            
            try:
                if self.browser_type == "chrome":
                    self.logger.info("Initialisiere Chrome-Browser")
                    options = Options()
                    
                    ```python
            # Stelle sicher, dass das Verzeichnis existiert
            os.makedirs(devices_path.parent, exist_ok=True)
            
            # Speichere Geräte
            with open(devices_path, "w") as f:
                json.dump(self.registered_devices, f, indent=4)
            
            self.logger.info(f"{len(self.registered_devices)} registrierte Geräte gespeichert.")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern registrierter Geräte: {e}")
    
    def _start_sync_thread(self):
        """Startet einen Thread für die regelmäßige Synchronisierung."""
        if not self.sync_enabled:
            self.logger.warning("Synchronisierung ist deaktiviert.")
            return
        
        # Starte Thread
        sync_thread = threading.Thread(target=self._sync_loop)
        sync_thread.daemon = True
        sync_thread.start()
        
        self.logger.info(f"Synchronisierungs-Thread gestartet (Intervall: {self.sync_interval} Sekunden).")
    
    def _sync_loop(self):
        """Thread-Funktion für die regelmäßige Synchronisierung."""
        try:
            while self.sync_enabled:
                # Führe Synchronisierung durch
                if not self.sync_in_progress:
                    self.perform_sync()
                
                # Warte bis zum nächsten Intervall
                time.sleep(self.sync_interval)
        
        except Exception as e:
            self.logger.error(f"Fehler im Synchronisierungs-Thread: {e}")
    
    def perform_sync(self):
        """Führt eine Synchronisierung mit Mobilgeräten durch."""
        if self.sync_in_progress:
            self.logger.warning("Eine Synchronisierung ist bereits im Gange.")
            return False
        
        try:
            self.sync_in_progress = True
            
            # Veröffentliche Event: Synchronisierung gestartet
            self.event_manager.publish("mobile.sync_started", {
                "timestamp": time.time()
            })
            
            # Veröffentliche Sync-Request an Datenbank
            self.event_manager.publish("db.sync_request", {
                "source": "mobile_integration"
            })
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Synchronisierung: {e}")
            self.sync_in_progress = False
            return False
    
    def register_device(self, device_info):
        """
        Registriert ein Mobilgerät für Benachrichtigungen und Synchronisierung.
        
        Args:
            device_info: Informationen zum Gerät
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            device_id = device_info.get("device_id")
            
            if not device_id:
                self.logger.error("Fehlende Geräte-ID bei der Registrierung.")
                return False
            
            # Prüfe, ob das Gerät bereits registriert ist
            for i, device in enumerate(self.registered_devices):
                if device.get("device_id") == device_id:
                    # Aktualisiere Geräteinformationen
                    self.registered_devices[i] = device_info
                    self._save_registered_devices()
                    
                    self.logger.info(f"Gerät aktualisiert: {device_id}")
                    
                    # Veröffentliche Event: Gerät aktualisiert
                    self.event_manager.publish("mobile.device_updated", device_info)
                    
                    return True
            
            # Neues Gerät registrieren
            self.registered_devices.append(device_info)
            self._save_registered_devices()
            
            self.logger.info(f"Neues Gerät registriert: {device_id}")
            
            # Veröffentliche Event: Gerät registriert
            self.event_manager.publish("mobile.device_registered", device_info)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Geräteregistrierung: {e}")
            return False
    
    def unregister_device(self, device_id):
        """
        Entfernt ein Mobilgerät aus der Registrierung.
        
        Args:
            device_id: ID des zu entfernenden Geräts
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            if not device_id:
                self.logger.error("Fehlende Geräte-ID bei der Entfernung.")
                return False
            
            # Suche das Gerät
            for i, device in enumerate(self.registered_devices):
                if device.get("device_id") == device_id:
                    # Entferne das Gerät
                    removed_device = self.registered_devices.pop(i)
                    self._save_registered_devices()
                    
                    self.logger.info(f"Gerät entfernt: {device_id}")
                    
                    # Veröffentliche Event: Gerät entfernt
                    self.event_manager.publish("mobile.device_unregistered", removed_device)
                    
                    return True
            
            self.logger.warning(f"Gerät nicht gefunden: {device_id}")
            return False
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Geräteentfernung: {e}")
            return False
    
    def send_push_notification(self, title, message, data=None):
        """
        Sendet eine Push-Benachrichtigung an alle registrierten Geräte.
        
        Args:
            title: Titel der Benachrichtigung
            message: Nachrichtentext
            data: Zusätzliche Daten (optional)
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if not self.push_notifications:
            self.logger.warning("Push-Benachrichtigungen sind deaktiviert.")
            return False
        
        try:
            if not self.registered_devices:
                self.logger.info("Keine registrierten Geräte für Push-Benachrichtigungen.")
                return False
            
            # Erstelle Benachrichtigung
            notification = {
                "title": title,
                "message": message,
                "data": data or {},
                "timestamp": time.time()
            }
            
            # Veröffentliche Event: Push-Benachrichtigung
            self.event_manager.publish("mobile.push_notification", notification)
            
            # In einer vollständigen Implementierung würde hier die Benachrichtigung
            # über einen Push-Benachrichtigungsdienst (z.B. Firebase Cloud Messaging)
            # an die registrierten Geräte gesendet werden.
            
            self.logger.info(f"Push-Benachrichtigung an {len(self.registered_devices)} Geräte gesendet: {title}")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Senden der Push-Benachrichtigung: {e}")
            return False
```

**10.3 Integration Manager für zentrale Koordination

```python

    # integration/integration_manager.py
import os
import logging
import threading
import time
from pathlib import Path

class IntegrationManager:
    """
    Verwaltet und koordiniert die verschiedenen Systemintegrationen.
    Dient als zentrale Anlaufstelle für alle Integrationsfunktionen.
    """
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("IntegrationManager")
        self.config = config
        self.event_manager = event_manager
        
        # Flags für aktivierte Integrationen
        self.windows_integration_enabled = config["integration"]["windows_automation"]
        self.browser_integration_enabled = True  # Standardmäßig aktiviert
        
        # Status der Integrationen
        self.windows_integration_active = False
        self.browser_integration_active = False
        self.mobile_integration_active = False
        
        # Laden der Komponenten
        self._load_components()
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("system.shutdown", self._on_system_shutdown)
        self.event_manager.subscribe("browser.initialized", self._on_browser_initialized)
        self.event_manager.subscribe("browser.closed", self._on_browser_closed)
    
    def _load_components(self):
        """Lädt die Integrationskomponenten basierend auf der Konfiguration."""
        # Windows-Integration laden
        if self.windows_integration_enabled:
            try:
                from integration.windows_integration import WindowsIntegration
                self.windows_integration = WindowsIntegration(self.config, self.event_manager)
                self.logger.info("Windows-Integration geladen")
            except Exception as e:
                self.logger.error(f"Fehler beim Laden der Windows-Integration: {e}")
                self.windows_integration = None
                self.windows_integration_enabled = False
        else:
            self.windows_integration = None
        
        # Browser-Integration laden
        if self.browser_integration_enabled:
            try:
                from integration.browser_integration import BrowserIntegration
                self.browser_integration = BrowserIntegration(self.config, self.event_manager)
                self.logger.info("Browser-Integration geladen")
            except Exception as e:
                self.logger.error(f"Fehler beim Laden der Browser-Integration: {e}")
                self.browser_integration = None
                self.browser_integration_enabled = False
        else:
            self.browser_integration = None
        
        # Mobile-Integration laden
        try:
            from integration.mobile.mobile_api import MobileAPIManager
            self.mobile_api = MobileAPIManager(self.config, self.event_manager)
            self.logger.info("Mobile-API-Integration geladen")
            
            # Lade Synchronisationsdienst, wenn eine Datenbank verfügbar ist
            try:
                from db.database_manager import DatabaseManager
                db_manager = DatabaseManager(self.config, self.event_manager)
                
                from integration.mobile.sync_service import SyncService
                self.sync_service = SyncService(self.config, self.event_manager, db_manager)
                self.logger.info("Mobile-Synchronisationsdienst geladen")
            except Exception as e:
                self.logger.error(f"Fehler beim Laden des Synchronisationsdienstes: {e}")
                self.sync_service = None
            
            self.mobile_integration_active = True
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Mobile-Integration: {e}")
            self.mobile_api = None
            self.sync_service = None
            self.mobile_integration_active = False
    
    def _on_system_ready(self, data):
        """Handler für system.ready Event."""
        # Starte Windows-Integration, falls aktiviert
        if self.windows_integration_enabled and self.windows_integration:
            self.windows_integration_active = True
            self.logger.info("Windows-Integration aktiv")
        
        # Starte Browser-Integration, falls aktiviert
        if self.browser_integration_enabled and self.browser_integration:
            # Browser-Integration wird bei Bedarf initialisiert
            self.logger.info("Browser-Integration bereit")
        
        # Veröffentliche Event: Integrationen bereit
        self.event_manager.publish("integration.ready", {
            "windows_integration": self.windows_integration_active,
            "browser_integration": self.browser_integration_enabled,
            "mobile_integration": self.mobile_integration_active
        })
    
    def _on_system_shutdown(self, data):
        """Handler für system.shutdown Event."""
        # Schließe Browser-Integration
        if self.browser_integration:
            try:
                # Schließe Browser, falls geöffnet
                self.browser_integration._close_browser()
            except Exception as e:
                self.logger.error(f"Fehler beim Schließen der Browser-Integration: {e}")
        
        # Veröffentliche Event: Integrationen heruntergefahren
        self.event_manager.publish("integration.shutdown", None)
    
    def _on_browser_initialized(self, data):
        """Handler für browser.initialized Event."""
        self.browser_integration_active = True
    
    def _on_browser_closed(self, data):
        """Handler für browser.closed Event."""
        self.browser_integration_active = False
    
    def navigate_to_url(self, url):
        """
        Navigiert zu einer URL im Browser.
        
        Args:
            url: Die URL, zu der navigiert werden soll
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.browser_integration and self.browser_integration_enabled:
            return self.browser_integration.navigate_to(url)
        else:
            self.logger.warning("Browser-Integration nicht verfügbar")
            return False
    
    def get_page_content(self):
        """
        Holt den Inhalt der aktuellen Seite im Browser.
        
        Returns:
            str: Der HTML-Inhalt der Seite oder None bei Fehler
        """
        if self.browser_integration and self.browser_integration_active:
            return self.browser_integration.get_page_content()
        else:
            self.logger.warning("Browser-Integration nicht verfügbar oder aktiv")
            return None
    
    def launch_application(self, app_name, app_path=None):
        """
        Startet eine Anwendung.
        
        Args:
            app_name: Der Name der Anwendung
            app_path: Optional, der Pfad zur Anwendung
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.windows_integration and self.windows_integration_active:
            return self.windows_integration.launch_application(app_name, app_path)
        else:
            self.logger.warning("Windows-Integration nicht verfügbar oder aktiv")
            return False
    
    def close_application(self, app_name):
        """
        Schließt eine Anwendung.
        
        Args:
            app_name: Der Name der Anwendung
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.windows_integration and self.windows_integration_active:
            # Suche nach dem passenden Fenster
            matching_windows = [win for win in self.windows_integration.get_all_windows() if app_name.lower() in win.title.lower()]
            
            if matching_windows:
                result = self.windows_integration.close_application(matching_windows[0])
                return result
            else:
                self.logger.warning(f"Keine Anwendung mit dem Namen '{app_name}' gefunden")
                return False
        else:
            self.logger.warning("Windows-Integration nicht verfügbar oder aktiv")
            return False
    
    def get_active_window_info(self):
        """
        Gibt Informationen über das aktive Fenster zurück.
        
        Returns:
            dict: Informationen über das Fenster oder None bei Fehler
        """
        if self.windows_integration and self.windows_integration_active:
            return self.windows_integration.get_window_info()
        else:
            self.logger.warning("Windows-Integration nicht verfügbar oder aktiv")
            return None
    
    def get_screen_text(self, x=None, y=None, width=300, height=200):
        """
        Erfasst Text vom Bildschirm an einer bestimmten Position.
        
        Args:
            x, y: Koordinaten des Ausgangspunkts (None für Bildschirmmitte)
            width, height: Größe des zu erfassenden Bereichs
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.windows_integration and self.windows_integration_active:
            # Bestimme Koordinaten, falls nicht angegeben
            if x is None or y is None:
                import pyautogui
                screen_width, screen_height = pyautogui.size()
                
                if x is None:
                    x = screen_width // 2 - width // 2
                if y is None:
                    y = screen_height // 2 - height // 2
            
            return self.windows_integration.get_screen_text_at_position(x, y, width, height)
        else:
            self.logger.warning("Windows-Integration nicht verfügbar oder aktiv")
            return False
    
    def register_mobile_device(self, device_info):
        """
        Registriert ein Mobilgerät für die Synchronisation.
        
        Args:
            device_info: Informationen zum Gerät
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.mobile_api and self.mobile_integration_active:
            return self.mobile_api.register_device(device_info)
        else:
            self.logger.warning("Mobile-Integration nicht verfügbar oder aktiv")
            return False
    
    def send_push_notification(self, title, message, data=None):
        """
        Sendet eine Push-Benachrichtigung an registrierte Mobilgeräte.
        
        Args:
            title: Der Titel der Benachrichtigung
            message: Der Nachrichtentext
            data: Zusätzliche Daten (optional)
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.mobile_api and self.mobile_integration_active:
            return self.mobile_api.send_push_notification(title, message, data)
        else:
            self.logger.warning("Mobile-Integration nicht verfügbar oder aktiv")
            return False

 ```


**10.4 API und Schnittstellen für Web und Mobile

```
# api/rest_api.py
import os
import logging
import time
import json
import threading
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, status, Request, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
import uvicorn

class RestAPI:
    """
    REST-API für den Zugriff auf das Assistenzsystem von externen Clients.
    """
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("RestAPI")
        self.config = config
        self.event_manager = event_manager
        
        # API-Konfiguration
        self.host = config["api"]["host"]
        self.port = config["api"]["port"]
        self.auth_enabled = config["api"]["enable_auth"]
        
        # Erstelle FastAPI-Anwendung
        self.app = FastAPI(
            title="AssistTech API",
            description="API für den Zugriff auf das AssistTech-Assistenzsystem",
            version=config["system"]["version"]
        )
        
        # Aktiviere CORS für Frontend-Zugriff
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In Produktion beschränken
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # OAuth2-Authentifizierung
        if self.auth_enabled:
            # Lade JWT-Secret aus Umgebungsvariablen
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            jwt_secret_env = config["api"]["jwt_secret_env"]
            self.jwt_secret = os.getenv(jwt_secret_env)
            
            if not self.jwt_secret:
                self.logger.error(f"JWT-Secret nicht gefunden in Umgebungsvariable {jwt_secret_env}")
                self.jwt_secret = "defaultsecret"  # Nicht für Produktion verwenden!
            
            # OAuth2-Schema
            self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
            
            # Authentifizierungsfunktionen
            from jose import jwt
            from datetime import datetime, timedelta
            
            self.jwt = jwt
            
            # Füge Authentifizierung hinzu
            @self.app.post("/token")
            async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
                # Hier würde man normalerweise einen Benutzer authentifizieren
                # Für diese Implementierung erlauben wir jeden Benutzer mit passendem Passwort
                if form_data.username == "admin" and form_data.password == "password":
                    access_token = self._create_access_token(
                        data={"sub": form_data.username}
                    )
                    return {"access_token": access_token, "token_type": "bearer"}
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Falsche Anmeldeinformationen",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
        
        # API-Endpunkte registrieren
        self._setup_endpoints()
        
        # Server-Thread
        self.server_thread = None
        self.is_running = False
        
        # Event-Warteschlangen für asynchrone Antworten
        self.event_queues = {}
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("system.shutdown", self._on_system_shutdown)
    
    def _create_access_token(self, data: dict):
        """Erstellt ein JWT-Token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = self.jwt.encode(to_encode, self.jwt_secret, algorithm="HS256")
        return encoded_jwt
    
    async def _get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        """Überprüft das JWT-Token und gibt den Benutzer zurück."""
        try:
            payload = self.jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Ungültiges Token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return {"username": username}
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ungültiges Token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def _setup_endpoints(self):
        """Richtet die API-Endpunkte ein."""
        
        # Root-Endpunkt für Statusprüfung
        @self.app.get("/")
        async def root():
            return {"status": "ok", "version": self.config["system"]["version"]}
        
        # Sprachendpunkte
        @self.app.post("/speech/speak")
        async def speak(request: Request):
            data = await request.json()
            text = data.get("text", "")
            speed = data.get("speed", 1.0)
            
            if not text:
                return JSONResponse(status_code=400, content={"error": "Text erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("speech.speak_text", {
                "text": text,
                "speed": speed,
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Sprachausgabe"})
        
        @self.app.post("/speech/listen")
        async def listen(request: Request):
            data = await request.json()
            timeout = data.get("timeout", 5.0)
            language = data.get("language", "de")
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("speech.listen_once", {
                "timeout": timeout,
                "language": language,
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=timeout + 2.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Spracherkennung"})
        
        # Browser-Endpunkte
        @self.app.post("/browser/navigate")
        async def navigate_to(request: Request):
            data = await request.json()
            url = data.get("url", "")
            
            if not url:
                return JSONResponse(status_code=400, content={"error": "URL erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("browser.navigate_to", {
                "url": url,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=30.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Navigation"})
        
        @self.app.post("/browser/summarize")
        async def summarize_page(request: Request):
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("browser.summarize_page", {
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=60.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Zusammenfassung"})
        
        # Vision-Endpunkte
        @self.app.post("/vision/capture")
        async def capture_image(request: Request):
            data = await request.json()
            save = data.get("save", False)
            format = data.get("format", "jpg")
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            if save:
                self.event_manager.publish("vision.capture_and_save", {
                    "format": format,
                    "source": "api",
                    "event_id": event_id
                })
            else:
                self.event_manager.publish("vision.capture_image", {
                    "source": "api",
                    "event_id": event_id
                })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Bilderfassung"})
        
        @self.app.post("/vision/analyze")
        async def analyze_image(request: Request):
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("vision.analyze_scene", {
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=30.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Bildanalyse"})
        
        # System-Endpunkte
        @self.app.post("/system/launch")
        async def launch_application(request: Request):
            data = await request.json()
            app_name = data.get("app_name", "")
            
            if not app_name:
                return JSONResponse(status_code=400, content={"error": "Anwendungsname erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("system.launch_application", {
                "app_name": app_name,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout beim Starten der Anwendung"})
        
        # Assistenten-Endpunkte
        @self.app.post("/assistant/query")
        async def process_query(request: Request):
            data = await request.json()
            query = data.get("query", "")
            
            if not query:
                return JSONResponse(status_code=400, content={"error": "Anfrage erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("assistant.process_query", {
                "query": query,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=60.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Verarbeitung der Anfrage"})
        
        # Medien-Endpunkte
        @self.app.post("/media/control")
        async def media_control(request: Request):
            data = await request.json()
            action = data.get("action", "")
            
            if not action:
                return JSONResponse(status_code=400, content={"error": "Aktion erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("media.control", {
                "action": action,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Mediensteuerung"})
        
        # Synchronisierungsendpunkt für Mobile-Geräte
        @self.app.post("/sync")
        async def sync_data(request: Request):
            data = await request.json()
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("mobile.sync_data_received", {
                "data": data,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=30.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Synchronisierung"})
        
        # Geräteregistrierung für Mobile-Geräte
        @self.app.post("/register_device")
        async def register_device(request: Request):
            data = await request.json()
            device_info = data.get("device_info", {})
            
            if not device_info or "device_id" not in device_info:
                return JSONResponse(status_code=400, content={"error": "Geräteinformationen erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("mobile.register_device", {
                "device_info": device_info,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Geräteregistrierung"})
    
    def _on_system_ready(self, data):
        """Handler für system.ready Event."""
        # Starte den API-Server
        self.start_server()
    
    def _on_system_shutdown(self, data):
        """Handler für system.shutdown Event."""
        # Stoppe den API-Server
        self.stop_server()
    
    def start_server(self):
        """Startet den API-Server."""
        if self.is_running:
            return
        
        # Starte den Server in einem separaten Thread
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.is_running = True
        self.logger.info(f"API-Server gestartet auf {self.host}:{self.port}")
        
        # Veröffentliche Event: API-Server gestartet
        self.event_manager.publish("api.server_started", {
            "host": self.host,
            "port": self.port
        })
    
    def stop_server(self):
        """Stoppt den API-Server."""
        self.is_running = False
        
        # Server wird automatisch beendet, wenn das Programm schließt
        
        self.logger.info("API-Server gestoppt")
        
        # Veröffentliche Event: API-Server gestoppt
        self.event_manager.publish("api.server_stopped", None)
    
    def _run_server(self):
        """Thread-Funktion für den API-Server."""
        try:
            import uvicorn
           uvicorn.run(self.app, host=self.host, port=self.port)
       
       except Exception as e:
           self.logger.error(f"Fehler beim Starten des API-Servers: {e}")
         
           
**10.5 WebSocket-Server für Echtzeit-Kommunikation
 
 # api/websocket_server.py
import os
import logging
import time
import json
import threading
import asyncio
from pathlib import Path
from datetime import datetime

import websockets
from typing import Dict, List, Set, Any

class WebSocketServer:
    """
    WebSocket-Server für Echtzeit-Kommunikation mit Clients.
    Ermöglicht Push-Benachrichtigungen und Echtzeit-Updates für mobile Clients.
    """
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("WebSocketServer")
        self.config = config
        self.event_manager = event_manager
        
        # Server-Konfiguration
        self.host = config["api"]["host"]
        self.port = config["api"]["ws_port"]
        
        # Status
        self.is_running = False
        self.server = None
        self.server_task = None
        self.event_loop = None
        self.server_thread = None
        
        # Verbundene Clients
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.authenticated_clients: Dict[websockets.WebSocketServerProtocol, Dict] = {}
        
        # Event-Dict für Client-Benachrichtigungen
        self.event_types_to_forward = {
            "speech.tts_started", "speech.tts_finished",
            "vision.image_captured", "vision.analysis_completed",
            "browser.navigation_completed", "browser.summary_ready",
            "assistant.response_ready", "media.status",
            "system.launched_application", "system.window_control_applied"
        }
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("system.shutdown", self._on_system_shutdown)
        
        # Registriere Handler für alle weiterzuleitenden Event-Typen
        for event_type in self.event_types_to_forward:
            self.event_manager.subscribe(event_type, self._on_forwardable_event)
    
    def _on_system_ready(self, data):
        """Handler für system.ready Event."""
        # Starte den WebSocket-Server
        self.start_server()
    
    def _on_system_shutdown(self, data):
        """Handler für system.shutdown Event."""
        # Stoppe den WebSocket-Server
        self.stop_server()
    
    def _on_forwardable_event(self, data):
        """Handler für Events, die an Clients weitergeleitet werden sollen."""
        # Sende das Event an alle verbundenen Clients
        event_type = None
        
        # Bestimme den Event-Typ
        for et in self.event_types_to_forward:
            if self.event_manager._current_event_type == et:
                event_type = et
                break
        
        if event_type:
            event_data = {
                "type": "event",
                "event_type": event_type,
                "timestamp": time.time(),
                "data": data
            }
            
            # Leite Event an alle Clients weiter (asynchron)
            asyncio.run_coroutine_threadsafe(
                self._broadcast_to_clients(event_data),
                self.event_loop
            )
    
    async def _broadcast_to_clients(self, message):
        """Sendet eine Nachricht an alle verbundenen Clients."""
        if not self.clients:
            return
        
        # Konvertiere Nachricht zu JSON
        message_json = json.dumps(message)
        
        # Sende an alle Clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                self.logger.error(f"Fehler beim Senden an Client: {e}")
                disconnected_clients.add(client)
        
        # Entferne getrennte Clients
        for client in disconnected_clients:
            if client in self.clients:
                self.clients.remove(client)
            if client in self.authenticated_clients:
                del self.authenticated_clients[client]
    
    async def _handler(self, websocket, path):
        """Handler für eingehende WebSocket-Verbindungen."""
        client_info = {
            "ip": websocket.remote_address[0],
            "connected_at": datetime.now().isoformat(),
            "authenticated": False,
            "user_id": None
        }
        
        self.logger.info(f"Neue Client-Verbindung: {client_info['ip']}")
        
        try:
            # Füge Client zur Clients-Liste hinzu
            self.clients.add(websocket)
            
            # Sende Willkommensnachricht
            await websocket.send(json.dumps({
                "type": "welcome",
                "message": f"Willkommen beim AssistTech WebSocket-Server v{self.config['system']['version']}",
                "require_auth": False  # In Produktion auf True setzen
            }))
            
            # Verarbeite eingehende Nachrichten
            async for message in websocket:
                try:
                    # Parse JSON
                    data = json.loads(message)
                    
                    # Verarbeite Nachrichtentyp
                    msg_type = data.get("type", "")
                    
                    if msg_type == "auth":
                        # Authentifiziere den Client
                        token = data.get("token", "")
                        
                        # Hier sollte die Token-Validierung erfolgen
                        # Für diesen Prototyp akzeptieren wir jedes Token
                        client_info["authenticated"] = True
                        client_info["user_id"] = "user123"  # Dummy-ID
                        
                        self.authenticated_clients[websocket] = client_info
                        
                        await websocket.send(json.dumps({
                            "type": "auth_response",
                            "success": True,
                            "message": "Authentifizierung erfolgreich"
                        }))
                    
                    elif msg_type == "command":
                        # Verarbeite einen Befehl vom Client
                        command = data.get("command", "")
                        command_data = data.get("data", {})
                        
                        # Prüfe, ob der Client authentifiziert ist (in Produktion aktivieren)
                        #if websocket not in self.authenticated_clients:
                        #    await websocket.send(json.dumps({
                        #        "type": "error",
                        #        "message": "Nicht authentifiziert"
                        #    }))
                        #    continue
                        
                        # Leite Befehl an Event-Manager weiter
                        if command == "speak":
                            text = command_data.get("text", "")
                            if text:
                                self.event_manager.publish("speech.speak_text", {
                                    "text": text,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "speak",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "Text erforderlich"
                                }))
                        
                        elif command == "query":
                            query = command_data.get("query", "")
                            if query:
                                self.event_manager.publish("assistant.process_query", {
                                    "query": query,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "query",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "Anfrage erforderlich"
                                }))
                        
                        elif command == "browser_navigate":
                            url = command_data.get("url", "")
                            if url:
                                self.event_manager.publish("browser.navigate_to", {
                                    "url": url,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "browser_navigate",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "URL erforderlich"
                                }))
                        
                        elif command == "media_control":
                            action = command_data.get("action", "")
                            if action:
                                self.event_manager.publish("media.control", {
                                    "action": action,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "media_control",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "Aktion erforderlich"
                                }))
                        
                        else:
                            await websocket.send(json.dumps({
                                "type": "error",
                                "message": f"Unbekannter Befehl: {command}"
                            }))
                    
                    elif msg_type == "ping":
                        # Einfacher Ping/Pong-Mechanismus zur Verbindungsprüfung
                        await websocket.send(json.dumps({
                            "type": "pong",
                            "timestamp": time.time()
                        }))
                    
                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": f"Unbekannter Nachrichtentyp: {msg_type}"
                        }))
                
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Ungültiges JSON-Format"
                    }))
                except Exception as e:
                    self.logger.error(f"Fehler bei der Verarbeitung der Nachricht: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Interner Serverfehler"
                    }))
        
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Client-Verbindung geschlossen: {client_info['ip']}")
        except Exception as e:
            self.logger.error(f"Fehler in der WebSocket-Verbindung: {e}")
        finally:
            # Entferne Client aus Listen
            if websocket in self.clients:
                self.clients.remove(websocket)
            if websocket in self.authenticated_clients:
                del self.authenticated_clients[websocket]
    
    def start_server(self):
        """Startet den WebSocket-Server."""
        if self.is_running:
            return
        
        # Starte den Server in einem separaten Thread
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.is_running = True
        self.logger.info(f"WebSocket-Server gestartet auf {self.host}:{self.port}")
        
        # Veröffentliche Event: WebSocket-Server gestartet
        self.event_manager.publish("api.websocket_server_started", {
            "host": self.host,
            "port": self.port
        })
    
    def stop_server(self):
        """Stoppt den WebSocket-Server."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Stoppe den Server
        if self.server_task and not self.server_task.done():
            asyncio.run_coroutine_threadsafe(self._stop_server(), self.event_loop)
        
        # Warte auf das Ende des Server-Threads
        if self.server_thread:
            self.server_thread.join(timeout=5.0)
        
        self.logger.info("WebSocket-Server gestoppt")
        
        # Veröffentliche Event: WebSocket-Server gestoppt
        self.event_manager.publish("api.websocket_server_stopped", None)
    
    async def _stop_server(self):
        """Beendet den WebSocket-Server asynchron."""
        # Schließe alle Client-Verbindungen
        for client in self.clients:
            try:
                await client.close()
            except:
                pass
        
        # Schließe den Server
        if self.server:
            self.server.close()
            await self.server.wait_closed()
    
    def _run_server(self):
        """Thread-Funktion für den WebSocket-Server."""
        try:
            # Erstelle Event-Loop
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            
            # Starte WebSocket-Server
            start_server = websockets.serve(self._handler, self.host, self.port)
            self.server = self.event_loop.run_until_complete(start_server)
            
            # Halte die Event-Loop am Laufen
            self.event_loop.run_forever()
        
        except Exception as e:
            self.logger.error(f"Fehler beim Starten des WebSocket-Servers: {e}")
        finally:
            # Aufräumarbeiten
            if self.event_loop and not self.event_loop.is_closed():
                # Schließe ausstehende Aufgaben
                tasks = asyncio.all_tasks(self.event_loop)
                for task in tasks:
                    task.cancel()
                
                # Schließe die Event-Loop
                self.event_loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                self.event_loop.close()
                
            11. Datenbank-Setup und Synchronisierung
11.1 Datenbankmanager
           
            
            








# api/rest_api.py
import os
import logging
import time
import json
import threading
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, status, Request, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
import uvicorn

class RestAPI:
    """
    REST-API für den Zugriff auf das Assistenzsystem von externen Clients.
    """
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("RestAPI")
        self.config = config
        self.event_manager = event_manager
        
        # API-Konfiguration
        self.host = config["api"]["host"]
        self.port = config["api"]["port"]
        self.auth_enabled = config["api"]["enable_auth"]
        
        # Erstelle FastAPI-Anwendung
        self.app = FastAPI(
            title="AssistTech API",
            description="API für den Zugriff auf das AssistTech-Assistenzsystem",
            version=config["system"]["version"]
        )
        
        # Aktiviere CORS für Frontend-Zugriff
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In Produktion beschränken
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # OAuth2-Authentifizierung
        if self.auth_enabled:
            # Lade JWT-Secret aus Umgebungsvariablen
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            jwt_secret_env = config["api"]["jwt_secret_env"]
            self.jwt_secret = os.getenv(jwt_secret_env)
            
            if not self.jwt_secret:
                self.logger.error(f"JWT-Secret nicht gefunden in Umgebungsvariable {jwt_secret_env}")
                self.jwt_secret = "defaultsecret"  # Nicht für Produktion verwenden!
            
            # OAuth2-Schema
            self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
            
            # Authentifizierungsfunktionen
            from jose import jwt
            from datetime import datetime, timedelta
            
            self.jwt = jwt
            
            # Füge Authentifizierung hinzu
            @self.app.post("/token")
            async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
                # Hier würde man normalerweise einen Benutzer authentifizieren
                # Für diese Implementierung erlauben wir jeden Benutzer mit passendem Passwort
                if form_data.username == "admin" and form_data.password == "password":
                    access_token = self._create_access_token(
                        data={"sub": form_data.username}
                    )
                    return {"access_token": access_token, "token_type": "bearer"}
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Falsche Anmeldeinformationen",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
        
        # API-Endpunkte registrieren
        self._setup_endpoints()
        
        # Server-Thread
        self.server_thread = None
        self.is_running = False
        
        # Event-Warteschlangen für asynchrone Antworten
        self.event_queues = {}
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("system.shutdown", self._on_system_shutdown)
    
    def _create_access_token(self, data: dict):
        """Erstellt ein JWT-Token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = self.jwt.encode(to_encode, self.jwt_secret, algorithm="HS256")
        return encoded_jwt
    
    async def _get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        """Überprüft das JWT-Token und gibt den Benutzer zurück."""
        try:
            payload = self.jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Ungültiges Token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return {"username": username}
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ungültiges Token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def _setup_endpoints(self):
        """Richtet die API-Endpunkte ein."""
        
        # Root-Endpunkt für Statusprüfung
        @self.app.get("/")
        async def root():
            return {"status": "ok", "version": self.config["system"]["version"]}
        
        # Sprachendpunkte
        @self.app.post("/speech/speak")
        async def speak(request: Request):
            data = await request.json()
            text = data.get("text", "")
            speed = data.get("speed", 1.0)
            
            if not text:
                return JSONResponse(status_code=400, content={"error": "Text erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("speech.speak_text", {
                "text": text,
                "speed": speed,
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Sprachausgabe"})
        
        @self.app.post("/speech/listen")
        async def listen(request: Request):
            data = await request.json()
            timeout = data.get("timeout", 5.0)
            language = data.get("language", "de")
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("speech.listen_once", {
                "timeout": timeout,
                "language": language,
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=timeout + 2.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Spracherkennung"})
        
        # Browser-Endpunkte
        @self.app.post("/browser/navigate")
        async def navigate_to(request: Request):
            data = await request.json()
            url = data.get("url", "")
            
            if not url:
                return JSONResponse(status_code=400, content={"error": "URL erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("browser.navigate_to", {
                "url": url,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=30.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Navigation"})
        
        @self.app.post("/browser/summarize")
        async def summarize_page(request: Request):
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("browser.summarize_page", {
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=60.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Zusammenfassung"})
        
        # Vision-Endpunkte
        @self.app.post("/vision/capture")
        async def capture_image(request: Request):
            data = await request.json()
            save = data.get("save", False)
            format = data.get("format", "jpg")
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            if save:
                self.event_manager.publish("vision.capture_and_save", {
                    "format": format,
                    "source": "api",
                    "event_id": event_id
                })
            else:
                self.event_manager.publish("vision.capture_image", {
                    "source": "api",
                    "event_id": event_id
                })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Bilderfassung"})
        
        @self.app.post("/vision/analyze")
        async def analyze_image(request: Request):
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("vision.analyze_scene", {
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=30.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Bildanalyse"})
        
        # System-Endpunkte
        @self.app.post("/system/launch")
        async def launch_application(request: Request):
            data = await request.json()
            app_name = data.get("app_name", "")
            
            if not app_name:
                return JSONResponse(status_code=400, content={"error": "Anwendungsname erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("system.launch_application", {
                "app_name": app_name,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout beim Starten der Anwendung"})
        
        # Assistenten-Endpunkte
        @self.app.post("/assistant/query")
        async def process_query(request: Request):
            data = await request.json()
            query = data.get("query", "")
            
            if not query:
                return JSONResponse(status_code=400, content={"error": "Anfrage erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("assistant.process_query", {
                "query": query,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=60.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Verarbeitung der Anfrage"})
        
        # Medien-Endpunkte
        @self.app.post("/media/control")
        async def media_control(request: Request):
            data = await request.json()
            action = data.get("action", "")
            
            if not action:
                return JSONResponse(status_code=400, content={"error": "Aktion erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("media.control", {
                "action": action,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Mediensteuerung"})
        
        # Synchronisierungsendpunkt für Mobile-Geräte
        @self.app.post("/sync")
        async def sync_data(request: Request):
            data = await request.json()
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("mobile.sync_data_received", {
                "data": data,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=30.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Synchronisierung"})
        
        # Geräteregistrierung für Mobile-Geräte
        @self.app.post("/register_device")
        async def register_device(request: Request):
            data = await request.json()
            device_info = data.get("device_info", {})
            
            if not device_info or "device_id" not in device_info:
                return JSONResponse(status_code=400, content={"error": "Geräteinformationen erforderlich"})
            
            # Generiere eindeutige Event-ID
            import uuid
            event_id = str(uuid.uuid4())
            
            # Erstelle Warteschlange für die Antwort
            self.event_queues[event_id] = queue.Queue()
            
            # Veröffentliche Event
            self.event_manager.publish("mobile.register_device", {
                "device_info": device_info,
                "source": "api",
                "event_id": event_id
            })
            
            # Warte auf die Antwort (mit Timeout)
            try:
                result = self.event_queues[event_id].get(timeout=10.0)
                del self.event_queues[event_id]
                return result
            except queue.Empty:
                del self.event_queues[event_id]
                return JSONResponse(status_code=408, content={"error": "Timeout bei der Geräteregistrierung"})
    
    def _on_system_ready(self, data):
        """Handler für system.ready Event."""
        # Starte den API-Server
        self.start_server()
    
    def _on_system_shutdown(self, data):
        """Handler für system.shutdown Event."""
        # Stoppe den API-Server
        self.stop_server()
    
    def start_server(self):
        """Startet den API-Server."""
        if self.is_running:
            return
        
        # Starte den Server in einem separaten Thread
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.is_running = True
        self.logger.info(f"API-Server gestartet auf {self.host}:{self.port}")
        
        # Veröffentliche Event: API-Server gestartet
        self.event_manager.publish("api.server_started", {
            "host": self.host,
            "port": self.port
        })
    
    def stop_server(self):
        """Stoppt den API-Server."""
        self.is_running = False
        
        # Server wird automatisch beendet, wenn das Programm schließt
        
        self.logger.info("API-Server gestoppt")
        
        # Veröffentliche Event: API-Server gestoppt
        self.event_manager.publish("api.server_stopped", None)
    
    def _run_server(self):
        """Thread-Funktion für den API-Server."""
        try:
            import uvicorn
            uvicorn.run(self.

**10.5 WebSocket-Server für Echtzeit-Kommunikation

# api/websocket_server.py
import os
import logging
import time
import json
import threading
import asyncio
from pathlib import Path
from datetime import datetime

import websockets
from typing import Dict, List, Set, Any

class WebSocketServer:
    """
    WebSocket-Server für Echtzeit-Kommunikation mit Clients.
    Ermöglicht Push-Benachrichtigungen und Echtzeit-Updates für mobile Clients.
    """
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("WebSocketServer")
        self.config = config
        self.event_manager = event_manager
        
        # Server-Konfiguration
        self.host = config["api"]["host"]
        self.port = config["api"]["ws_port"]
        
        # Status
        self.is_running = False
        self.server = None
        self.server_task = None
        self.event_loop = None
        self.server_thread = None
        
        # Verbundene Clients
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.authenticated_clients: Dict[websockets.WebSocketServerProtocol, Dict] = {}
        
        # Event-Dict für Client-Benachrichtigungen
        self.event_types_to_forward = {
            "speech.tts_started", "speech.tts_finished",
            "vision.image_captured", "vision.analysis_completed",
            "browser.navigation_completed", "browser.summary_ready",
            "assistant.response_ready", "media.status",
            "system.launched_application", "system.window_control_applied"
        }
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("system.shutdown", self._on_system_shutdown)
        
        # Registriere Handler für alle weiterzuleitenden Event-Typen
        for event_type in self.event_types_to_forward:
            self.event_manager.subscribe(event_type, self._on_forwardable_event)
    
    def _on_system_ready(self, data):
        """Handler für system.ready Event."""
        # Starte den WebSocket-Server
        self.start_server()
    
    def _on_system_shutdown(self, data):
        """Handler für system.shutdown Event."""
        # Stoppe den WebSocket-Server
        self.stop_server()
    
    def _on_forwardable_event(self, data):
        """Handler für Events, die an Clients weitergeleitet werden sollen."""
        # Sende das Event an alle verbundenen Clients
        event_type = None
        
        # Bestimme den Event-Typ
        for et in self.event_types_to_forward:
            if self.event_manager._current_event_type == et:
                event_type = et
                break
        
        if event_type:
            event_data = {
                "type": "event",
                "event_type": event_type,
                "timestamp": time.time(),
                "data": data
            }
            
            # Leite Event an alle Clients weiter (asynchron)
            asyncio.run_coroutine_threadsafe(
                self._broadcast_to_clients(event_data),
                self.event_loop
            )
    
    async def _broadcast_to_clients(self, message):
        """Sendet eine Nachricht an alle verbundenen Clients."""
        if not self.clients:
            return
        
        # Konvertiere Nachricht zu JSON
        message_json = json.dumps(message)
        
        # Sende an alle Clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                self.logger.error(f"Fehler beim Senden an Client: {e}")
                disconnected_clients.add(client)
        
        # Entferne getrennte Clients
        for client in disconnected_clients:
            if client in self.clients:
                self.clients.remove(client)
            if client in self.authenticated_clients:
                del self.authenticated_clients[client]
    
    async def _handler(self, websocket, path):
        """Handler für eingehende WebSocket-Verbindungen."""
        client_info = {
            "ip": websocket.remote_address[0],
            "connected_at": datetime.now().isoformat(),
            "authenticated": False,
            "user_id": None
        }
        
        self.logger.info(f"Neue Client-Verbindung: {client_info['ip']}")
        
        try:
            # Füge Client zur Clients-Liste hinzu
            self.clients.add(websocket)
            
            # Sende Willkommensnachricht
            await websocket.send(json.dumps({
                "type": "welcome",
                "message": f"Willkommen beim AssistTech WebSocket-Server v{self.config['system']['version']}",
                "require_auth": False  # In Produktion auf True setzen
            }))
            
            # Verarbeite eingehende Nachrichten
            async for message in websocket:
                try:
                    # Parse JSON
                    data = json.loads(message)
                    
                    # Verarbeite Nachrichtentyp
                    msg_type = data.get("type", "")
                    
                    if msg_type == "auth":
                        # Authentifiziere den Client
                        token = data.get("token", "")
                        
                        # Hier sollte die Token-Validierung erfolgen
                        # Für diesen Prototyp akzeptieren wir jedes Token
                        client_info["authenticated"] = True
                        client_info["user_id"] = "user123"  # Dummy-ID
                        
                        self.authenticated_clients[websocket] = client_info
                        
                        await websocket.send(json.dumps({
                            "type": "auth_response",
                            "success": True,
                            "message": "Authentifizierung erfolgreich"
                        }))
                    
                    elif msg_type == "command":
                        # Verarbeite einen Befehl vom Client
                        command = data.get("command", "")
                        command_data = data.get("data", {})
                        
                        # Prüfe, ob der Client authentifiziert ist (in Produktion aktivieren)
                        #if websocket not in self.authenticated_clients:
                        #    await websocket.send(json.dumps({
                        #        "type": "error",
                        #        "message": "Nicht authentifiziert"
                        #    }))
                        #    continue
                        
                        # Leite Befehl an Event-Manager weiter
                        if command == "speak":
                            text = command_data.get("text", "")
                            if text:
                                self.event_manager.publish("speech.speak_text", {
                                    "text": text,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "speak",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "Text erforderlich"
                                }))
                        
                        elif command == "query":
                            query = command_data.get("query", "")
                            if query:
                                self.event_manager.publish("assistant.process_query", {
                                    "query": query,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "query",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "Anfrage erforderlich"
                                }))
                        
                        elif command == "browser_navigate":
                            url = command_data.get("url", "")
                            if url:
                                self.event_manager.publish("browser.navigate_to", {
                                    "url": url,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "browser_navigate",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "URL erforderlich"
                                }))
                        
                        elif command == "media_control":
                            action = command_data.get("action", "")
                            if action:
                                self.event_manager.publish("media.control", {
                                    "action": action,
                                    "source": "websocket"
                                })
                                
                                await websocket.send(json.dumps({
                                    "type": "command_response",
                                    "command": "media_control",
                                    "success": True
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "error",
                                    "message": "Aktion erforderlich"
                                }))
                        
                        else:
                            await websocket.send(json.dumps({
                                "type": "error",
                                "message": f"Unbekannter Befehl: {command}"
                            }))
                    
                    elif msg_type == "ping":
                        # Einfacher Ping/Pong-Mechanismus zur Verbindungsprüfung
                        await websocket.send(json.dumps({
                            "type": "pong",
                            "timestamp": time.time()
                        }))
                    
                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": f"Unbekannter Nachrichtentyp: {msg_type}"
                        }))
                
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Ungültiges JSON-Format"
                    }))
                except Exception as e:
                    self.logger.error(f"Fehler bei der Verarbeitung der Nachricht: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Interner Serverfehler"
                    }))
        
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Client-Verbindung geschlossen: {client_info['ip']}")
        except Exception as e:
            self.logger.error(f"Fehler in der WebSocket-Verbindung: {e}")
        finally:
            # Entferne Client aus Listen
            if websocket in self.clients:
                self.clients.remove(websocket)
            if websocket in self.authenticated_clients:
                del self.authenticated_clients[websocket]
    
    def start_server(self):
        """Startet den WebSocket-Server."""
        if self.is_running:
            return
        
        # Starte den Server in einem separaten Thread
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.is_running = True
        self.logger.info(f"WebSocket-Server gestartet auf {self.host}:{self.port}")
        
        # Veröffentliche Event: WebSocket-Server gestartet
        self.event_manager.publish("api.websocket_server_started", {
            "host": self.host,
            "port": self.port
        })
    
    def stop_server(self):
        """Stoppt den WebSocket-Server."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Stoppe den Server
        if self.server_task and not self.server_task.done():
            asyncio.run_coroutine_threadsafe(self._stop_server(), self.event_loop)
        
        # Warte auf das Ende des Server-Threads
        if self.server_thread:
            self.server_thread.join(timeout=5.0)
        
        self.logger.info("WebSocket-Server gestoppt")
        
        # Veröffentliche Event: WebSocket-Server gestoppt
        self.event_manager.publish("api.websocket_server_stopped", None)
    
    async def _stop_server(self):
        """Beendet den WebSocket-Server asynchron."""
        # Schließe alle Client-Verbindungen
        for client in self.clients:
            try:
                await client.close()
            except:
                pass
        
        # Schließe den Server
        if self.server:
            self.server.close()
            await self.server.wait_closed()
    
    def _run_server(self):
        """Thread-Funktion für den WebSocket-Server."""
        try:
            # Erstelle Event-Loop
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            
            # Starte WebSocket-Server
            start_server = websockets.serve(self._handler, self.host, self.port)
            self.server = self.event_loop.run_until_complete(start_server)
            
            # Halte die Event-Loop am Laufen
            self.event_loop.run_forever()
        
        except Exception as e:
            self.logger.error(f"Fehler beim Starten des WebSocket-Servers: {e}")
        finally:
            # Aufräumarbeiten
            if self.event_loop and not self.event_loop.is_closed():
                # Schließe ausstehende Aufgaben
                tasks = asyncio.all_tasks(self.event_loop)
                for task in tasks:
                    task.cancel()
                
                # Schließe die Event-Loop
                self.event_loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                self.event_loop.close()

**11. Datenbank-Setup und Synchronisierung

**11.1 Datenbankmanager

# db/database_manager.py
import os
import logging
import time
import json
import threading
import sqlite3
from pathlib import Path
from datetime import datetime

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# SQLAlchemy Base
Base = declarative_base()

# Datenbankmodelle definieren
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    settings = relationship("UserSetting", back_populates="user")
    contexts = relationship("ContextItem", back_populates="user")

class UserSetting(Base):
    __tablename__ = 'user_settings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String(50))
    key = Column(String(50))
    value = Column(Text)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="settings")

class ContextItem(Base):
    __tablename__ = 'context_items'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    key = Column(String(100))
    value = Column(Text)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="contexts")

class ConversationHistory(Base):
    __tablename__ = 'conversation_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_text = Column(Text)
    response_text = Column(Text)
    intent = Column(String(50))
    confidence = Column(Float)
    
    user = relationship("User")

class SyncLog(Base):
    __tablename__ = 'sync_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    device_id = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)
    details = Column(Text)
    
    user = relationship("User")

class DatabaseManager:
    """
    Verwaltet den Zugriff auf die Datenbank und stellt Repositories zur Verfügung.
    """
    
    def __init__(self, config, event_manager):
        self.logger = logging.getLogger("DatabaseManager")
        self.config = config
        self.event_manager = event_manager
        
        # Datenbank-Konfiguration
        self.db_type = config["database"]["type"]
        self.db_host = config["database"]["host"]
        self.db_port = config["database"]["port"]
        self.db_name = config["database"]["name"]
        self.db_user = config["database"]["user"]
        
        # DB-Passwort aus Umgebungsvariable laden
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        db_password_env = config["database"]["password_env"]
        self.db_password = os.getenv(db_password_env)
        
        # Sync-Konfiguration
        self.sync_enabled = config["database"]["sync_enabled"]
        
        # Engine und Session
        self.engine = None
        self.Session = None
        self.session = None
        
        # Sessions-Dict für Thread-Sicherheit
        self.sessions = {}
        self.sessions_lock = threading.Lock()
        
        # Initialisiere Datenbank
        self._initialize_database()
        
        # Repositories laden
        self._load_repositories()
        
        # Registriere Event-Handler
        self.event_manager.subscribe("system.ready", self._on_system_ready)
        self.event_manager.subscribe("db.sync_request", self._on_sync_request)
    
    def _initialize_database(self):
        """Initialisiert die Datenbankverbindung basierend auf der Konfiguration."""
        try:
            # Bestimme Connection-String
            if self.db_type == "sqlite":
                # SQLite verwenden (einfache Einrichtung für Entwicklung)
                db_path = os.path.join(self.config["system"]["data_dir"], "db", f"{self.db_name}.db")
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                
                connection_string = f"sqlite:///{db_path}"
                self.engine = create_engine(connection_string)
            
            elif self.db_type == "postgresql":
                # PostgreSQL verwenden (für Produktion empfohlen)
                connection_string = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
                self.engine = create_engine(connection_string)
            
            else:
                self.logger.error(f"Nicht unterstützter Datenbanktyp: {self.db_type}")
                raise ValueError(f"Nicht unterstützter Datenbanktyp: {self.db_type}")
            
            # Tabellen erstellen
            Base.metadata.create_all(self.engine)
            
            # Session-Factory erstellen
            self.Session = sessionmaker(bind=self.engine)
            
            # Erstelle Standard-Session
            self.session = self.Session()
            
            # Standardbenutzer erstellen, falls nicht vorhanden
            self._create_default_user()
            
            self.logger.info(f"Datenbank initialisiert: {self.db_type}")
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Datenbankinitialisierung: {e}")
            raise
    
    def _create_default_user(self):
        """Erstellt einen Standard-Benutzer, falls noch keiner existiert."""
        try:
            # Prüfe, ob bereits ein Benutzer existiert
            user = self.session.query(User).filter_by(username="default").first()
            
            if not user:
                # Erstelle Standardbenutzer
                user = User(username="default")
                self.session.add(user)
                self.session.commit()
                
                self.logger.info("Standard-Benutzer erstellt")
                
                # Erstelle einige Standard-Einstellungen
                settings = [
                    UserSetting(user_id=user.id, category="ui", key="theme", value="dark"),
                    UserSetting(user_id=user.id, category="ui", key="font_size", value="medium"),
                    UserSetting(user_id=user.id, category="speech", key="tts_rate", value="1.0"),
                    UserSetting(user_id=user.id, category="speech", key="tts_voice", value="de_DE-thorsten-medium")
                ]
                
                for setting in settings:
                    self.session.add(setting)
                
                self.session.commit()
                self.logger.info("Standard-Einstellungen erstellt")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Erstellen des Standard-Benutzers: {e}")
            self.session.rollback()
    
    def _load_repositories(self):
        """Lädt die Repository-Komponenten."""
        try:
            from db.repositories.user_repository import UserRepository
            from db.repositories.settings_repository import SettingsRepository
            from db.repositories.context_repository import ContextRepository
            
            self.user_repository = UserRepository(self)
            self.settings_repository = SettingsRepository(self)
            self.context_repository = ContextRepository(self)
            
            self.logger.info("Repositories geladen")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Repositories: {e}")
    
    def _on_system_ready(self, data):
        """Handler für system.ready Event."""
        self.logger.info("Datenbank-Manager bereit")
    
    def _on_sync_request(self, data):
        """Handler für db.sync_request Event."""
        if not self.sync_enabled:
            self.logger.warning("Synchronisierung ist deaktiviert")
            return
        
        source = data.get("source", "unknown")
        timestamp = data.get("last_sync_timestamp", 0)
        
        self.logger.info(f"Synchronisierungsanfrage von {source} (Zeitstempel: {timestamp})")
        
        # Hole Synchronisierungsdaten
        sync_data = self.get_sync_data_since(timestamp)
        
        # Veröffentliche Event: Synchronisierungsdaten bereit
        self.event_manager.publish("db.sync_data_ready", {
            "data": sync_data,
            "source": source
        })
    
    def get_session(self):
        """
        Gibt eine Thread-sichere Session zurück.
        
        Returns:
            SQLAlchemy-Session
        """
        thread_id = threading.get_ident()
        
        with self.sessions_lock:
            if thread_id not in self.sessions:
                self.sessions[thread_id] = self.Session()
            
            return self.sessions[thread_id]
    
    def release_session(self):
        """Gibt die aktuelle Thread-Session frei."""
        thread_id = threading.get_ident()
        
        with self.sessions_lock:
            if thread_id in self.sessions:
                self.sessions[thread_id].close()
                del self.sessions[thread_id]
    
    def store_user_setting(self, category, key, value):
        """
        Speichert eine Benutzereinstellung.
        
        Args:
            category: Die Kategorie der Einstellung
            key: Der Schlüssel der Einstellung
            value: Der Wert der Einstellung
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        return self.settings_repository.store_setting(1, category, key, value)  # User-ID 1 = Standardbenutzer
    
    def get_user_setting(self, category, key, default=None):
        """
        Holt eine Benutzereinstellung.
        
        Args:
            category: Die Kategorie der Einstellung
            key: Der Schlüssel der Einstellung
            default: Der Standardwert, falls die Einstellung nicht existiert
            
        Returns:
            Der Wert der Einstellung oder der Standardwert
        """
        return self.settings_repository.get_setting(1, category, key, default)  # User-ID 1 = Standardbenutzer
    
    def store_context_item(self, key, value, confidence=1.0):
        """
        Speichert ein Kontextelement.
        
        Args:
            key: Der Schlüssel des Elements
            value: Der Wert des Elements
            confidence: Die Konfidenz des Elements
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        return self.context_repository.store_item(1, key, value, confidence)  # User-ID 1 = Standardbenutzer
    
    def get_context_item(self, key, default=None):
        """
        Holt ein Kontextelement.
        
        Args:
            key: Der Schlüssel des Elements
            default: Der Standardwert, falls das Element nicht existiert
            
        Returns:
            Der Wert des Elements oder der Standardwert
        """
        return self.context_repository.get_item(1, key, default)  # User-ID 1 = Standardbenutzer
    
    def store_conversation(self, input_text, response_text, intent=None, confidence=None):
        """
        Speichert einen Konversationseintrag.
        
        Args:
            input_text: Die Nutzereingabe
            response_text: Die Systemantwort
            intent: Optional, die erkannte Intention
            confidence: Optional, die Konfidenz der Intentionserkennung
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            session = self.get_session()
            
            conversation = ConversationHistory(
                user_id=1,  # Standardbenutzer
                input_text=input_text,
                response_text=response_text,
                intent=intent,
                confidence=confidence
            )
            
            session.add(conversation)
            session.commit()
            
            self.logger.debug("Konversation gespeichert")
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern der Konversation: {e}")
            session.rollback()
            return False
        finally:
            self.release_session()
    
    def get_recent_conversations(self, limit=5):
        """
        Holt die neuesten Konversationseinträge.
        
        Args:
            limit: Maximale Anzahl der Einträge
            
        Returns:
            list: Liste der Konversationseinträge
        """
        try:
            session = self.get_session()
            
            conversations = session.query(ConversationHistory)\
                .filter_by(user_id=1)\
                .order_by(ConversationHistory.timestamp.desc())\
                .limit(limit)\
                .all()
            
            result = []
            for conv in conversations:
                result.append({
                    "timestamp": conv.timestamp.isoformat() if conv.timestamp else None,
                    "input_text": conv.input_text,
                    "response_text": conv.response_text,
                    "intent": conv.intent
                })
            
            return result
        
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen der Konversationen: {e}")
            return []
        finally:
            self.release_session()
    
    def log_sync(self, device_id, success, details=None):
        """
        Protokolliert einen Synchronisierungsvorgang.
        
        Args:
            device_id: Die ID des Geräts
            success: Ob die Synchronisierung erfolgreich war
            details: Optional, Details zur Synchronisierung
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            session = self.get_session()
            
            sync_log = SyncLog(
                user_id=1,  # Standardbenutzer
                device_id=device_id,
                success=success,
                details=details
            )
            
            session.add(sync_log)
            session.commit()
            
            self.logger.debug(f"Synchronisierung protokolliert: {device_id}")
            return True
        
        except Exception as e:
            self.logger.error(f"Fehler beim Protokollieren der Synchronisierung: {e}")
            session.rollback()
            return False
        finally:
            self.release_session()
    
    def get_sync_data_since(self, timestamp=0):
        """
        Holt alle Daten, die seit dem angegebenen Zeitstempel geändert wurden.
        
        Args:
            timestamp: Zeitstempel der letzten Synchronisierung
            
        Returns:
            dict: Die zu synchronisierenden Daten
        """
        try:
            session = self.get_session()
            
            # Konvertiere Zeitstempel zu Datetime
            from_date = datetime.fromtimestamp(timestamp) if timestamp > 0 else datetime.fromtimestamp(0)
            
            # Hole geänderte Einstellungen
            settings = session.query(UserSetting)\
                .filter(UserSetting.last_updated >= from_date)\
                .all()
            
            settings_data = []
            for setting in settings:
                settings_data.append({
                    "





