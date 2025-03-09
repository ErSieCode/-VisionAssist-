```markdown
# Universal OCR Tool 2.0 - OpenCV Integration und Multi-Output-Funktionalität

## Übersicht

Diese Erweiterung des Universal OCR Tool 2.0 implementiert fortschrittliche Computer Vision-Funktionen und Multi-Output-Verarbeitung. Die Integration von OpenCV ermöglicht Objekterkennung, Tracking und Kamera-Support, während das Multi-Output-System vielseitige Ausgabeformate aus einem einzigen Eingabedokument generieren kann.

## Inhaltsverzeichnis

1. [OpenCV-Integration](#opencv-integration)
   - [Computer Vision Modul](#computer-vision-modul)
   - [Objekterkennung und Annotation](#objekterkennung-und-annotation)
   - [Objekt-Tracking](#objekt-tracking)
   - [Kamera-Integration](#kamera-integration)
   - [OCR-Verbesserungen](#ocr-verbesserungen)

2. [Multi-Output-Funktionalität](#multi-output-funktionalität)
   - [Ausgabeformate](#ausgabeformate)
   - [API-Integration](#api-integration)
   - [Kombinierte Dokumente](#kombinierte-dokumente)
   - [Bild-Annotation](#bild-annotation)

3. [Installation und Konfiguration](#installation-und-konfiguration)
   - [Abhängigkeiten](#abhängigkeiten)
   - [Konfigurationsoptionen](#konfigurationsoptionen)
   - [Modelldownload](#modelldownload)

4. [Anwendungsbeispiele](#anwendungsbeispiele)
   - [Dokumenten-OCR mit Objekterkennung](#dokumenten-ocr-mit-objekterkennung)
   - [Video-Verarbeitung](#video-verarbeitung)
   - [Multi-Format-Export](#multi-format-export)

5. [Entwicklerhinweise](#entwicklerhinweise)
   - [Klassenstruktur](#klassenstruktur)
   - [Erweiterungsmöglichkeiten](#erweiterungsmöglichkeiten)
   - [Performance-Optimierung](#performance-optimierung)

## OpenCV-Integration

### Computer Vision Modul

Das Computer Vision Modul (`ComputerVisionModule`) bildet das Herzstück der OpenCV-Integration. Es erweitert das Universal OCR Tool um fortschrittliche Bildverarbeitungs- und Analysefunktionen:

- **Objekterkennung**: Integration verschiedener Detektionsmodelle (YOLO, SSD, Faster R-CNN)
- **Objekt-Tracking**: Echtzeit-Verfolgung von Objekten über Bild- und Videosequenzen
- **Kamera-Support**: Direktes Erfassen und Verarbeiten von Kameraeingaben
- **Bild-Annotation**: Visualisierung von erkannten Objekten und Textbereichen
- **Barcode- und QR-Code-Erkennung**: Automatische Erkennung und Dekodierung

Die Klasse bietet eine einheitliche Schnittstelle für alle Vision-Funktionen und ist vollständig in die bestehende OCR-Pipeline integriert.

### Objekterkennung und Annotation

Die Objekterkennung basiert auf vortrainierten Deep-Learning-Modellen und unterstützt verschiedene Architekturen:

- **YOLO** (You Only Look Once): Schnelle Echtzeit-Objekterkennung mit hoher Genauigkeit
- **SSD** (Single Shot MultiBox Detector): Gute Balance zwischen Geschwindigkeit und Genauigkeit
- **Faster R-CNN**: Hochgenaue Objekterkennung für anspruchsvolle Szenarien

Die erkannten Objekte werden in einem standardisierten Format zurückgegeben:

```python
{
    "class_id": 0,
    "class_name": "person",
    "confidence": 0.92,
    "box": {
        "x": 120,
        "y": 50,
        "width": 80,
        "height": 200
    }
}
```

Die Annotation von Bildern erfolgt mit der `annotate_image`-Methode, die Begrenzungsrahmen, Klassenbezeichnungen und Konfidenzwerte visualisiert.

### Objekt-Tracking

Das Tracking-System ermöglicht die kontinuierliche Verfolgung von Objekten über mehrere Frames hinweg:

- **Multi-Tracker-Unterstützung**: CSRT, KCF, BOOSTING, MIL, TLD, MEDIANFLOW, MOSSE
- **Initialisierung**: Starten des Trackings für spezifische Regionen oder erkannte Objekte
- **Update**: Kontinuierliche Aktualisierung der Objektpositionen in neuen Frames
- **Trajektorien**: Speicherung von Bewegungspfaden für Analysen und Visualisierungen

Die Integration von Erkennung und Tracking erfolgt mit der `detect_and_track`-Methode, die neue Objekte erkennt und bestehende Trackings aktualisiert.

### Kamera-Integration

Die direkte Kameraunterstützung ermöglicht die Echtzeit-Verarbeitung von Video-Eingaben:

- **Kamera-Initialisierung**: Flexible Auswahl und Konfiguration von Kamerageräten
- **Frame-Erfassung**: Einfache API zum Erfassen von Einzelbildern
- **Dokumenten-Extraktion**: Automatische Erkennung und Extraktion von Dokumenten im Kamerabild
- **Perspektivkorrektur**: Verbesserte Lesbarkeit durch automatische Entzerrung

### OCR-Verbesserungen

Die OpenCV-Integration verbessert auch die OCR-Funktionalität des Tools:

- **Erweiterte Bildvorverarbeitung**: Spezialisierte Filter und Transformationen für bessere Texterkennung
- **Textsegmentierung**: Präzise Erkennung von Textbereichen für zielgerichtete OCR
- **Schatten- und Reflexionsentfernung**: Verbesserte Erkennung bei ungünstigen Lichtverhältnissen
- **Deskewing**: Automatische Korrektur von Text-Schräglagen
- **Tabellenextraktion**: Erkennung von Tabellenstrukturen für strukturierte Datenextraktion

## Multi-Output-Funktionalität

### Ausgabeformate

Der Multi-Output-Prozessor (`MultiOutputProcessor`) ermöglicht die gleichzeitige Generierung verschiedener Ausgabeformate aus einem einzigen Eingabedokument:

- **Text**: Einfache Textextraktion mit optionaler Strukturierung
- **JSON**: Strukturierte Daten mit zusätzlichen Metainformationen
- **PDF**: Formatierte Dokumente mit Text und optionalen Bildern
- **Annotierte Bilder**: Visualisierung von erkannten Textregionen und Objekten
- **Thumbnails**: Kompakte Vorschaubilder mit optionaler Textüberlagerung
- **CSV**: Tabellarische Daten für erkannte Textblöcke oder Objekte
- **Markdown**: Strukturierte Dokumentation mit Text und Bildreferenzen
- **HTML**: Interaktive Dokumente mit eingebetteten Bildern und Analyseergebnissen
- **DOCX**: Microsoft Word-kompatible Dokumente
- **Kombinierte Dokumente**: Umfassende Berichte mit allen Erkennungsergebnissen

### API-Integration

Der Multi-Output-Prozessor unterstützt die direkte Integration mit externen Systemen:

- **API-Weiterleitung**: Automatische Übermittlung von Erkennungsergebnissen an externe Dienste
- **Konfigurierbare Endpunkte**: Flexible Definition von API-Zielen
- **Anpassbare Payloads**: Selektive Übermittlung von Daten basierend auf Anforderungen
- **Fehlerbehandlung**: Robuste Verarbeitung von API-Fehlern und Wiederholungsstrategien

### Kombinierte Dokumente

Die `_generate_combined_output`-Methode erstellt umfassende Berichte, die alle Aspekte der Dokumentenanalyse zusammenfassen:

- **Inhaltsübersicht**: Zusammenfassung der enthaltenen Informationen
- **Originalbilder und Annotationen**: Visuelle Darstellung der Erkennungsergebnisse
- **Extrahierter Text**: Vollständiger erkannter Text mit Formatierung
- **Strukturierte Daten**: Tabellen mit erkannten Textblöcken und Objekten
- **Metadaten**: Zusätzliche Dokumenteninformationen
- **Verarbeitungsstatistiken**: Informationen zur Verarbeitungsqualität

### Bild-Annotation

Die Bild-Annotations-Funktionalität erzeugt aussagekräftige visuelle Darstellungen:

- **Textregionen**: Farbkodierte Hervorhebung von erkannten Textbereichen mit Konfidenzwerten
- **Objekte**: Markierung von erkannten Objekten mit Klassenbezeichnungen
- **Tracking-Informationen**: Visualisierung von Objektbewegungen
- **Barcode- und QR-Code-Informationen**: Markierung und Dekodierung von erkannten Codes

## Installation und Konfiguration

### Abhängigkeiten

Die Erweiterung benötigt folgende zusätzliche Bibliotheken:

```
opencv-python>=4.5.0
opencv-contrib-python>=4.5.0
numpy>=1.19.0
reportlab>=3.5.0
python-docx>=0.8.10
requests>=2.25.0
pillow>=8.0.0
```

### Konfigurationsoptionen

Die Hauptkonfigurationsoptionen für die OpenCV-Integration umfassen:

```python
{
    "models_dir": "models/vision",  # Verzeichnis für Vision-Modelle
    "enable_gpu": true,             # GPU-Beschleunigung aktivieren
    "confidence_threshold": 0.5,    # Schwellenwert für Objekterkennung
    "tracker_type": "CSRT",         # Standard-Tracker-Typ
    "detection_model": "yolo",      # Standardmodell für Objekterkennung
    "yolo_version": "yolov4",       # YOLO-Version
    "camera_index": 0,              # Standard-Kamera-Index
    "enable_morphological": true,   # Morphologische Operationen für OCR
    "enable_perspective_correction": true,  # Perspektivkorrektur aktivieren
    "denoising_strength": 10        # Stärke der Rauschunterdrückung
}
```

Für den Multi-Output-Prozessor sind folgende Optionen relevant:

```python
{
    "output_dir": "output",              # Ausgabeverzeichnis
    "enable_api_forwarding": false,      # API-Weiterleitung aktivieren
    "api_endpoints": ["https://api.example.com/ocr"],  # API-Ziele
    "default_formats": ["text", "json"], # Standardausgabeformate
    "enable_thumbnails": true,           # Thumbnails generieren
    "thumbnail_size": [200, 200]         # Thumbnail-Größe
}
```

### Modelldownload

Die vortrainierten Objekterkennungsmodelle müssen separat heruntergeladen werden:

```bash
# YOLO-Modelle
mkdir -p models/vision
cd models/vision
wget https://pjreddie.com/media/files/yolov4.weights
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names

# Optional: SSD und Faster R-CNN Modelle
wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
tar -xzf ssd_mobilenet_v2_coco_2018_03_29.tar.gz
```

## Anwendungsbeispiele

### Dokumenten-OCR mit Objekterkennung

```python
from ocr_processor import OCRProcessor
from vision.computer_vision_module import ComputerVisionModule
from output.multi_output_processor import MultiOutputProcessor

# Module initialisieren
cv_module = ComputerVisionModule({"detection_model": "yolo"})
output_processor = MultiOutputProcessor({"default_formats": ["json", "pdf", "image_annotated"]})

# Bild laden und Objekte erkennen
image = cv2.imread("document.jpg")
detections = cv_module.detect_objects(image)

# Bild für OCR optimieren
enhanced_image = cv_module.enhance_for_ocr(image)

# OCR durchführen
ocr_processor = OCRProcessor()
ocr_result = ocr_processor.process_image(enhanced_image)

# Ergebnisse kombinieren
combined_result = {
    "doc_id": "doc_001",
    "text": ocr_result["text"],
    "text_blocks": ocr_result["text_blocks"],
    "detections": detections,
    "images": {
        "original": image,
        "enhanced": enhanced_image
    },
    "metadata": {
        "source": "document.jpg",
        "date_processed": "2023-09-15T12:34:56Z"
    }
}

# Verschiedene Ausgabeformate generieren
output_result = output_processor.process(
    combined_result,
    formats=["text", "json", "pdf", "image_annotated", "combined"]
)

# Ausgabepfade anzeigen
for format_name, format_result in output_result["outputs"].items():
    print(f"{format_name}: {format_result['path']}")
```

### Video-Verarbeitung

```python
import cv2
import time

# CV-Modul initialisieren
cv_module = ComputerVisionModule({"detection_model": "yolo"})

# Video öffnen
video = cv2.VideoCapture("video.mp4")

# Output-Video vorbereiten
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Tracking alle 30 Frames neu initialisieren
detection_interval = 30
frame_count = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    
    # Bei bestimmten Frames neu erkennen und Tracking starten
    if frame_count % detection_interval == 0:
        tracking_results = cv_module.detect_and_track(frame, track_classes=["person", "car"])
        print(f"Frame {frame_count}: {len(tracking_results['tracking_started'])} neue Objekte erkannt")
    else:
        # In anderen Frames nur Tracking aktualisieren
        tracking_results = {"tracking_updated": []}
        for object_id in list(cv_module.active_trackers.keys()):
            tracking_result = cv_module.update_tracking(frame, object_id)
            if tracking_result and tracking_result[0]:
                success, bbox = tracking_result
                tracking_results["tracking_updated"].append({
                    "object_id": object_id,
                    "bbox": {
                        "x": int(bbox[0]),
                        "y": int(bbox[1]),
                        "width": int(bbox[2]),
                        "height": int(bbox[3])
                    }
                })
    
    # Visualisierung
    annotated_frame = cv_module.annotate_tracked_objects(
        frame, tracking_results, show_trajectories=True
    )
    
    # In Output-Video schreiben
    output_video.write(annotated_frame)
    
    # Anzeigen (optional)
    cv2.imshow('Tracking', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    frame_count += 1

# Ressourcen freigeben
video.release()
output_video.release()
cv2.destroyAllWindows()
```

### Multi-Format-Export

```python
# OCR-Ergebnis mit verschiedenen Ausgabeformaten verarbeiten
ocr_result = ocr_processor.process_image("invoice.pdf")

# Zusätzliche Metadaten
metadata = {
    "document_type": "invoice",
    "document_id": "INV-2023-001",
    "date": "2023-09-15",
    "priority": "high"
}

# Ergebnisse kombinieren
combined_data = {
    "doc_id": metadata["document_id"],
    "text": ocr_result["text"],
    "text_blocks": ocr_result["text_blocks"],
    "metadata": metadata,
    "images": {
        "original": ocr_result["image"]
    },
    "processing_info": {
        "ocr_engine": "neural_ocr",
        "processing_time": ocr_result["processing_time"],
        "confidence": ocr_result["confidence"]
    }
}

# API-Konfiguration
api_options = {
    "api_endpoint": "https://erp-system.example.com/api/documents",
    "api_headers": {
        "Authorization": "Bearer token123",
        "Content-Type": "application/json"
    },
    "include_detections": True,
    "save_response": True
}

# Verschiedene Ausgabeformate generieren
output_result = output_processor.process(
    combined_data,
    formats=["text", "json", "pdf", "docx", "api", "combined"],
    options={
        "api": api_options,
        "pdf": {"include_images": True},
        "docx": {"include_metadata": True},
        "combined": {"include_text_blocks": True}
    }
)

# Verarbeitungsergebnisse anzeigen
print(f"Text: {output_result['outputs']['text']['char_count']} Zeichen")
print(f"JSON: {output_result['outputs']['json']['size']} Bytes")
print(f"PDF: {output_result['outputs']['pdf']['pages']} Seite(n)")

if "api" in output_result["outputs"]:
    api_result = output_result["outputs"]["api"]
    print(f"API-Status: {api_result.get('status_code')}")
```

## Entwicklerhinweise

### Klassenstruktur

Die Hauptklassen der Erweiterung sind:

- `ComputerVisionModule`: Zentrale Komponente für OpenCV-Funktionen
- `OpenCVOCRHelper`: Unterstützungsklasse für OCR-Vorverarbeitung
- `MultiOutputProcessor`: Verarbeitung verschiedener Ausgabeformate

Die Integration mit dem bestehenden Universal OCR Tool erfolgt über:

```python
# Bestehende OCR-Prozessor-Klasse erweitern
class OCRProcessor:
    def __init__(self, config=None):
        # Standard-Konfiguration
        self.config = config or {}
        
        # Module initialisieren
        self.cv_module = ComputerVisionModule(self.config.get("vision", {}))
        self.ocr_helper = OpenCVOCRHelper(self.config.get("ocr", {}))
        self.output_processor = MultiOutputProcessor(self.config.get("output", {}))
    
    def process_image(self, image_path):
        # Bild laden
        image = cv2.imread(image_path)
        
        # Objekte erkennen (optional)
        detections = []
        if self.config.get("detect_objects", False):
            detections = self.cv_module.detect_objects(image)
        
        # Textregionen erkennen
        text_regions = self.ocr_helper.detect_text_regions(image)
        
        # Bild für OCR optimieren
        enhanced_image = self.ocr_helper.enhance_for_ocr(image)
        
        # OCR durchführen mit bestehendem Neural OCR Engine
        ocr_result = self.neural_ocr_engine.recognize_text(enhanced_image)
        
        # Ergebnisse kombinieren
        result = {
            "text": ocr_result["text"],
            "text_blocks": ocr_result["text_blocks"],
            "detections": detections,
            "image": image,
            "enhanced_image": enhanced_image,
            "confidence": ocr_result["overall_confidence"],
            "processing_time": ocr_result["processing_time"]
        }
        
        return result
```

### Erweiterungsmöglichkeiten

Die Architektur ist modular gestaltet und bietet verschiedene Erweiterungsmöglichkeiten:

1. **Zusätzliche Detektionsmodelle**: Integration weiterer Objekterkennungsmodelle wie EfficientDet oder MobileNet
2. **Spezialisierte Dokumentenerkennung**: Hinzufügen dedizierter Modelle für Ausweise, Rechnungen oder andere Dokumententypen
3. **Erweiterte OCR-Nachbearbeitung**: NLP-basierte Textkorrekturen und semantische Analyse
4. **Weitere Ausgabeformate**: Erweiterung um zusätzliche Export-Formate wie XML, XLSX oder datenbankspezifische Formate
5. **Cloud-Integration**: Anbindung an Cloud-Speicher und -Dienste für nahtlose Dokumentenverarbeitung

### Performance-Optimierung

Für optimale Leistung sollten folgende Aspekte beachtet werden:

1. **GPU-Beschleunigung**: Aktivierung der GPU-Unterstützung für Detektionsmodelle und Bildverarbeitung
2. **Modellquantisierung**: Verwendung quantisierter Modelle für schnellere Inferenz bei geringfügig reduzierter Genauigkeit
3. **Parallele Verarbeitung**: Implementierung von Multi-Threading für gleichzeitige Verarbeitung mehrerer Dokumente
4. **Caching-Strategien**: Zwischenspeicherung von Zwischenergebnissen für häufig verwendete Operationen
5. **Bilddownsampling**: Reduzierung der Bildauflösung für schnellere Vorverarbeitung mit anschließender hochauflösender OCR

Die Balance zwischen Genauigkeit und Geschwindigkeit kann über die Konfiguration für verschiedene Anwendungsfälle optimiert werden.
```Strukturierte Daten**: Tabellen mit erkannten Textblöcken und Objekten
- **Metadaten**: Zusätzliche Dokumenteninformationen
- **Verarbeitungsstatistiken**: Informationen zur Verarbeitungsqualität

### Bild-Annotation

Die Bild-Annotations-Funktionalität erzeugt aussagekräftige visuelle Darstellungen:

- **Textregionen**: Farbkodierte Hervorhebung von erkannten Textbereichen mit Konfidenzwerten
- **Objekte**: Markierung von erkannten Objekten mit Klassenbezeichnungen
- **Tracking-Informationen**: Visualisierung von Objektbewegungen
- **Barcode- und QR-Code-Informationen**: Markierung und Dekodierung von erkannten Codes

## Installation und Konfiguration

### Abhängigkeiten

Die Erweiterung benötigt folgende zusätzliche Bibliotheken:

```
opencv-python>=4.5.0
opencv-contrib-python>=4.5.0
numpy>=1.19.0
reportlab>=3.5.0
python-docx>=0.8.10
requests>=2.25.0
pillow>=8.0.0
```

### Konfigurationsoptionen

Die Hauptkonfigurationsoptionen für die OpenCV-Integration umfassen:

```python
{
    "models_dir": "models/vision",  # Verzeichnis für Vision-Modelle
    "enable_gpu": true,             # GPU-Beschleunigung aktivieren
    "confidence_threshold": 0.5,    # Schwellenwert für Objekterkennung
    "tracker_type": "CSRT",         # Standard-Tracker-Typ
    "detection_model": "yolo",      # Standardmodell für Objekterkennung
    "yolo_version": "yolov4",       # YOLO-Version
    "camera_index": 0,              # Standard-Kamera-Index
    "enable_morphological": true,   # Morphologische Operationen für OCR
    "enable_perspective_correction": true,  # Perspektivkorrektur aktivieren
    "denoising_strength": 10        # Stärke der Rauschunterdrückung
}
```

Für den Multi-Output-Prozessor sind folgende Optionen relevant:

```python
{
    "output_dir": "output",              # Ausgabeverzeichnis
    "enable_api_forwarding": false,      # API-Weiterleitung aktivieren
    "api_endpoints": ["https://api.example.com/ocr"],  # API-Ziele
    "default_formats": ["text", "json"], # Standardausgabeformate
    "enable_thumbnails": true,           # Thumbnails generieren
    "thumbnail_size": [200, 200]         # Thumbnail-Größe
}
```

### Modelldownload

Die vortrainierten Objekterkennungsmodelle müssen separat heruntergeladen werden:

```bash
# YOLO-Modelle
mkdir -p models/vision
cd models/vision
wget https://pjreddie.com/media/files/yolov4.weights
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names

# Optional: SSD und Faster R-CNN Modelle
wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
tar -xzf ssd_mobilenet_v2_coco_2018_03_29.tar.gz
```

## Anwendungsbeispiele

### Dokumenten-OCR mit Objekterkennung

```python
from ocr_processor import OCRProcessor
from vision.computer_vision_module import ComputerVisionModule
from output.multi_output_processor import MultiOutputProcessor

# Module initialisieren
cv_module = ComputerVisionModule({"detection_model": "yolo"})
output_processor = MultiOutputProcessor({"default_formats": ["json", "pdf", "image_annotated"]})

# Bild laden und Objekte erkennen
image = cv2.imread("document.jpg")
detections = cv_module.detect_objects(image)

# Bild für OCR optimieren
enhanced_image = cv_module.enhance_for_ocr(image)

# OCR durchführen
ocr_processor = OCRProcessor()
ocr_result = ocr_processor.process_image(enhanced_image)

# Ergebnisse kombinieren
combined_result = {
    "doc_id": "doc_001",
    "text": ocr_result["text"],
    "text_blocks": ocr_result["text_blocks"],
    "detections": detections,
    "images": {
        "original": image,
        "enhanced": enhanced_image
    },
    "metadata": {
        "source": "document.jpg",
        "date_processed": "2023-09-15T12:34:56Z"
    }
}

# Verschiedene Ausgabeformate generieren
output_result = output_processor.process(
    combined_result,
    formats=["text", "json", "pdf", "image_annotated", "combined"]
)

# Ausgabepfade anzeigen
for format_name, format_result in output_result["outputs"].items():
    print(f"{format_name}: {format_result['path']}")
```

### Video-Verarbeitung

```python
import cv2
import time

# CV-Modul initialisieren
cv_module = ComputerVisionModule({"detection_model": "yolo"})

# Video öffnen
video = cv2.VideoCapture("video.mp4")

# Output-Video vorbereiten
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Tracking alle 30 Frames neu initialisieren
detection_interval = 30
frame_count = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    
    # Bei bestimmten Frames neu erkennen und Tracking starten
    if frame_count % detection_interval == 0:
        tracking_results = cv_module.detect_and_track(frame, track_classes=["person", "car"])
        print(f"Frame {frame_count}: {len(tracking_results['tracking_started'])} neue Objekte erkannt")
    else:
        # In anderen Frames nur Tracking aktualisieren
        tracking_results = {"tracking_updated": []}
        for object_id in list(cv_module.active_trackers.keys()):
            tracking_result = cv_module.update_tracking(frame, object_id)
            if tracking_result and tracking_result[0]:
                success, bbox = tracking_result
                tracking_results["tracking_updated"].append({
                    "object_id": object_id,
                    "bbox": {
                        "x": int(bbox[0]),
                        "y": int(bbox[1]),
                        "width": int(bbox[2]),
                        "height": int(bbox[3])
                    }
                })
    
    # Visualisierung
    annotated_frame = cv_module.annotate_tracked_objects(
        frame, tracking_results, show_trajectories=True
    )
    
    # In Output-Video schreiben
    output_video.write(annotated_frame)
    
    # Anzeigen (optional)
    cv2.imshow('Tracking', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    frame_count += 1

# Ressourcen freigeben
video.release()
output_video.release()
cv2.destroyAllWindows()
```

### Multi-Format-Export

```python
# OCR-Ergebnis mit verschiedenen Ausgabeformaten verarbeiten
ocr_result = ocr_processor.process_image("invoice.pdf")

# Zusätzliche Metadaten
metadata = {
    "document_type": "invoice",
    "document_id": "INV-2023-001",
    "date": "2023-09-15",
    "priority": "high"
}

# Ergebnisse kombinieren
combined_data = {
    "doc_id": metadata["document_id"],
    "text": ocr_result["text"],
    "text_blocks": ocr_result["text_blocks"],
    "metadata": metadata,
    "images": {
        "original": ocr_result["image"]
    },
    "processing_info": {
        "ocr_engine": "neural_ocr",
        "processing_time": ocr_result["processing_time"],
        "confidence": ocr_result["confidence"]
    }
}

# API-Konfiguration
api_options = {
    "api_endpoint": "https://erp-system.example.com/api/documents",
    "api_headers": {
        "Authorization": "Bearer token123",
        "Content-Type": "application/json"
    },
    "include_detections": True,
    "save_response": True
}

# Verschiedene Ausgabeformate generieren
output_result = output_processor.process(
    combined_data,
    formats=["text", "json", "pdf", "docx", "api", "combined"],
    options={
        "api": api_options,
        "pdf": {"include_images": True},
        "docx": {"include_metadata": True},
        "combined": {"include_text_blocks": True}
    }
)

# Verarbeitungsergebnisse anzeigen
print(f"Text: {output_result['outputs']['text']['char_count']} Zeichen")
print(f"JSON: {output_result['outputs']['json']['size']} Bytes")
print(f"PDF: {output_result['outputs']['pdf']['pages']} Seite(n)")

if "api" in output_result["outputs"]:
    api_result = output_result["outputs"]["api"]
    print(f"API-Status: {api_result.get('status_code')}")
```

## Entwicklerhinweise

### Klassenstruktur

Die Hauptklassen der Erweiterung sind:

- `ComputerVisionModule`: Zentrale Komponente für OpenCV-Funktionen
- `OpenCVOCRHelper`: Unterstützungsklasse für OCR-Vorverarbeitung
- `MultiOutputProcessor`: Verarbeitung verschiedener Ausgabeformate

Die Integration mit dem bestehenden Universal OCR Tool erfolgt über:

```python
# Bestehende OCR-Prozessor-Klasse erweitern
class OCRProcessor:
    def __init__(self, config=None):
        # Standard-Konfiguration
        self.config = config or {}
        
        # Module initialisieren
        self.cv_module = ComputerVisionModule(self.config.get("vision", {}))
        self.ocr_helper = OpenCVOCRHelper(self.config.get("ocr", {}))
        self.output_processor = MultiOutputProcessor(self.config.get("output", {}))
    
    def process_image(self, image_path):
        # Bild laden
        image = cv2.imread(image_path)
        
        # Objekte erkennen (optional)
        detections = []
        if self.config.get("detect_objects", False):
            detections = self.cv_module.detect_objects(image)
        
        # Textregionen erkennen
        text_regions = self.ocr_helper.detect_text_regions(image)
        
        # Bild für OCR optimieren
        enhanced_image = self.ocr_helper.enhance_for_ocr(image)
        
        # OCR durchführen mit bestehendem Neural OCR Engine
        