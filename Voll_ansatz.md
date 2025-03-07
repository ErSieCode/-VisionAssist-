# Modulare Dateistruktur für ein KI-gestütztes Assistenzsystem für Sehbehinderte

Die folgende Dateistruktur bietet eine modulare Organisation des Assistenzsystems mit klaren Schnittstellen zwischen den Komponenten und der Möglichkeit zur späteren Integration von Mobilgeräten.

```
assisttech/
├── core/                       # Kernkomponenten des Systems
│   ├── __init__.py
│   ├── system.py               # Hauptsystemklasse
│   ├── config.py               # Konfigurationsmanager
│   ├── logging_manager.py      # Zentrales Logging
│   └── event_manager.py        # Eventbasierte Kommunikation (wichtig für Multi-Plattform)
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
├── api/                        # API-Schicht (wichtig für Mobile-Integration)
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
├── config/                     # Konfigurationsdateien
│   ├── config.yaml             # Hauptkonfiguration
│   ├── logging_config.yaml     # Logging-Konfiguration
│   └── models_config.yaml      # KI-Modell-Konfiguration
│
├── data/                       # Datenspeicher
│   ├── db/                     # Datenbanken
│   ├── models/                 # KI-Modelle
│   ├── cache/                  # Cache-Daten
│   └── user/                   # Benutzerdaten
│
├── logs/                       # Log-Dateien
│
├── assets/                     # Statische Assets
│   ├── icons/                  # Icons und Bilder
│   ├── sounds/                 # Audiorückmeldungen
│   └── translations/           # Übersetzungen
│
├── tests/                      # Tests
│   ├── unit/                   # Unit-Tests
│   ├── integration/            # Integrationstests
│   └── e2e/                    # End-to-End-Tests
│
├── docs/                       # Dokumentation
│   ├── api/                    # API-Dokumentation
│   ├── user/                   # Benutzerhandbuch
│   └── developer/              # Entwicklerhandbuch
│
├── scripts/                    # Hilfsskripte
│   ├── install.py              # Installationsskript
│   ├── build.py                # Build-Skript
│   └── deploy.py               # Deployment-Skript
│
├── main.py                     # Haupteinstiegspunkt
├── requirements.txt            # Python-Abhängigkeiten
├── setup.py                    # Installationskonfiguration
├── .env                        # Umgebungsvariablen
└── README.md                   # Projektbeschreibung
```

## Kern-Komponenten-Interaktion

Die modulare Architektur ermöglicht eine klare Trennung der Funktionalitäten mit definierten Schnittstellen zwischen den Komponenten.

### Event-basierte Kommunikation

Die `core/event_manager.py` implementiert ein Publish-Subscribe-Muster, das die Kommunikation zwischen Komponenten ermöglicht, ohne dass sie direkt voneinander abhängen. Dies ist entscheidend für die spätere Integration von Mobilgeräten.

```python
# Beispielimplementierung des Event Managers
class EventManager:
    def __init__(self):
        self.subscribers = {}
        
    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        
    def publish(self, event_type, data=None):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)
```

### API-Schicht für Mobile-Integration

Die API-Schicht (`api/`) bietet REST- und WebSocket-Endpoints, die von Mobilgeräten angesprochen werden können. Diese Schicht dient als Brücke zwischen dem Kernsystem und zukünftigen Mobilanwendungen.

```python
# Beispiel REST-API Endpunkt für die Sprachausgabesteuerung
@app.route('/api/speech/speak', methods=['POST'])
def speak_text():
    data = request.json
    text = data.get('text', '')
    speed = data.get('speed', 1.0)
    voice = data.get('voice', 'default')
    
    # Text an TTS-System weiterleiten
    tts_manager.speak(text, speed=speed, voice=voice)
    
    return jsonify({'status': 'success'})
```

## Mobile-Integration-Strategie

Die Architektur ermöglicht eine nahtlose Integration von Mobilgeräten durch:

1. **Zentrale API-Schicht**: Alle Kernfunktionen sind über die API zugänglich
2. **Zustandssynchronisation**: Der `integration/mobile/sync_service.py` sorgt für die Synchronisation zwischen PC und Mobilgeräten
3. **Platform-agnostische Kommunikation**: Das Eventsystem ermöglicht plattformübergreifende Kommunikation
4. **Geteiltes Kontextgedächtnis**: Die Datenbank speichert Kontextinformationen, die zwischen Geräten synchronisiert werden können

```python
# Beispiel für einen Synchronisationsdienst
class SyncService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def get_sync_data(self, user_id, last_sync_timestamp):
        """Holt alle Daten, die seit dem letzten Sync geändert wurden"""
        return {
            'user_preferences': self.db_manager.get_preferences_since(user_id, last_sync_timestamp),
            'context_memory': self.db_manager.get_context_since(user_id, last_sync_timestamp),
            'conversation_history': self.db_manager.get_conversations_since(user_id, last_sync_timestamp)
        }
        
    def apply_sync_data(self, user_id, sync_data):
        """Wendet vom Mobilgerät empfangene Synchronisierungsdaten an"""
        # Implementierung der Datensynchronisation
```

## Spezifische Funktionsimplementierungen

Die Architektur unterstützt folgende spezifische Use-Cases:

### 1. Sprachtrigger und Browserfunktionen

Im `nlp/intent_processor.py` werden Sprachkommandos analysiert und die entsprechenden Aktionen ausgelöst:

```python
def process_browser_command(self, command):
    """Verarbeitet browserrelevante Sprachbefehle"""
    if "öffne" in command.lower() and any(domain in command.lower() for domain in [".de", ".com", ".org"]):
        # Extrahiere URL und öffne sie
        url = self._extract_url(command)
        return self.browser_integration.navigate_to(url)
    
    elif "zusammenfassen" in command.lower():
        # Hole Seiteninhalt und erstelle Zusammenfassung
        html_content = self.browser_integration.get_page_content()
        return self.content_analyzer.summarize_webpage(html_content)
    
    elif "klicke" in command.lower() and "link" in command.lower():
        # Identifiziere und klicke auf den relevantesten Link
        return self.browser_integration.click_most_relevant_link(command)
```

### 2. Text vorlesen mit Geschwindigkeitskontrolle

In `speech/text_to_speech.py` werden Funktionen zur flexiblen Textausgabe implementiert:

```python
def speak_text(self, text, speed=1.0, start_position=0, end_position=None):
    """Liest Text vor mit anpassbarer Geschwindigkeit und Position"""
    if end_position is None:
        end_position = len(text)
        
    text_portion = text[start_position:end_position]
    
    # Setze Vorlesegeschwindigkeit
    self.engine.setProperty('rate', int(self.base_rate * speed))
    
    # Text vorlesen
    self.engine.say(text_portion)
    self.engine.runAndWait()
```

### 3. Mediensteuerung

Die Komponente `media/media_controller.py` implementiert die Mediensteuerung für Browser-basierte Inhalte:

```python
def control_video(self, command):
    """Steuert Videowiedergabe im Browser"""
    if "abspielen" in command or "play" in command:
        return self.browser_integration.execute_script("document.querySelector('video').play()")
    
    elif "pause" in command:
        return self.browser_integration.execute_script("document.querySelector('video').pause()")
    
    elif "schneller" in command or "x2" in command:
        return self.browser_integration.execute_script("document.querySelector('video').playbackRate = 2.0")
```

## Beispiel-Workflow: Webseite öffnen, zusammenfassen und vorlesen

Diese Architektur ermöglicht den gewünschten Workflow über folgende Komponenten:

1. `speech/wake_word.py` erkennt das Aktivierungswort
2. `speech/speech_recognition.py` erfasst und transkribiert den Sprachbefehl
3. `nlp/intent_processor.py` analysiert die Intention (z.B. "öffne Website")
4. `integration/browser_integration.py` öffnet die Website
5. `nlp/content_analyzer.py` erstellt eine Zusammenfassung
6. `speech/text_to_speech.py` liest die Zusammenfassung vor
7. `integration/browser_integration.py` navigiert zu Links oder steuert Medien

Durch die modulare Struktur können diese Komponenten sowohl auf dem PC als auch später auf Mobilgeräten genutzt werden, wobei die API-Schicht als vereinheitlichende Schnittstelle dient.

## Vorteile dieser Architektur

1. **Klare Trennung der Zuständigkeiten**: Jedes Modul hat eine klar definierte Aufgabe
2. **Erweiterbarkeit**: Neue Funktionen können einfach hinzugefügt werden
3. **Plattformunabhängigkeit**: Die Kernfunktionalität ist von der Plattform (PC/Mobile) entkoppelt
4. **Testbarkeit**: Komponenten können isoliert getestet werden
5. **Mobile-First-Readiness**: Die API-Schicht ermöglicht eine nahtlose Integration von Mobilgeräten

Diese Architektur behält alle Funktionen des ursprünglichen Systems bei, organisiert sie jedoch in einer Weise, die eine einfache Erweiterung auf Mobilgeräte ermöglicht, ohne umfangreiche Umstrukturierungen zu erfordern.