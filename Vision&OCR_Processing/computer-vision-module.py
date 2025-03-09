# vision/computer_vision_module.py
import cv2
import numpy as np
import os
import time
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime

class ComputerVisionModule:
    """Computer Vision Module für das Universal OCR Tool 2.0 mit OpenCV-Integration.
    
    Dieses Modul erweitert das OCR-Tool um fortgeschrittene Bildverarbeitungs- und
    Objekterkennungsfunktionen unter Verwendung von OpenCV.
    
    Features:
    - Objekterkennung und -annotation mit verschiedenen Modellen (YOLO, SSD, etc.)
    - Objektverfolgung (Tracking) in Videostreams und -dateien
    - Live-Kamera-Integration für Echtzeit-OCR und -Erkennung
    - Verbesserte Bildvorverarbeitung für OCR
    - Unterstützung für QR-Code- und Barcode-Erkennung
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert das Computer Vision Modul mit Konfiguration.
        
        Args:
            config: Konfigurationswörterbuch mit Einstellungen für Vision-Funktionen
        """
        self.config = config
        self.logger = logging.getLogger("ocrtool.vision")
        
        # Konfigurationsoptionen
        self.models_dir = config.get("models_dir", "models/vision")
        self.enable_gpu = config.get("enable_gpu", False)
        self.confidence_threshold = config.get("confidence_threshold", 0.5)
        self.use_cuda = config.get("use_cuda", False)
        
        # Initialisiere Tracking
        self.tracker_type = config.get("tracker_type", "CSRT")
        self.active_trackers = {}
        self.tracked_objects = {}
        
        # Initialisiere Objekterkennung
        self._initialize_object_detection()
        
        # Kamera-Setup
        self.camera_index = config.get("camera_index", 0)
        self.camera = None
        
        # Barcode-/QR-Code-Detektor
        self.barcode_detector = cv2.barcode_BarcodeDetector()
        
        self.logger.info("Computer Vision Module initialisiert")
    
    def _initialize_object_detection(self):
        """Initialisiert die Objekterkennungsmodelle basierend auf der Konfiguration."""
        detection_model = self.config.get("detection_model", "yolo")
        self.detection_model_type = detection_model
        
        try:
            if detection_model.lower() == "yolo":
                self._initialize_yolo()
            elif detection_model.lower() == "ssd":
                self._initialize_ssd()
            elif detection_model.lower() == "faster_rcnn":
                self._initialize_faster_rcnn()
            else:
                self.logger.warning(f"Unbekanntes Detektionsmodell: {detection_model}. Verwende YOLO als Fallback.")
                self._initialize_yolo()
                
        except Exception as e:
            self.logger.error(f"Fehler beim Initialisieren des Objekterkennungsmodells: {e}")
            self.object_detector = None
    
    def _initialize_yolo(self):
        """Initialisiert das YOLO-Objekterkennungsmodell."""
        yolo_version = self.config.get("yolo_version", "yolov4")
        
        # Pfade zu Modell-Dateien
        if yolo_version == "yolov4":
            config_path = os.path.join(self.models_dir, "yolov4.cfg")
            weights_path = os.path.join(self.models_dir, "yolov4.weights")
            classes_path = os.path.join(self.models_dir, "coco.names")
        elif yolo_version == "yolov3":
            config_path = os.path.join(self.models_dir, "yolov3.cfg")
            weights_path = os.path.join(self.models_dir, "yolov3.weights")
            classes_path = os.path.join(self.models_dir, "coco.names")
        else:
            raise ValueError(f"Nicht unterstützte YOLO-Version: {yolo_version}")
        
        # Lade Klassennamen
        with open(classes_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        # Lade YOLO-Netzwerk
        self.object_detector = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        
        # Verwende GPU, falls konfiguriert und verfügbar
        if self.enable_gpu:
            self.object_detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.object_detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
        # Bestimme Output-Layer-Namen
        self.layer_names = self.object_detector.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.object_detector.getUnconnectedOutLayers()]
        
        self.logger.info(f"YOLO ({yolo_version}) Modell initialisiert")
    
    def _initialize_ssd(self):
        """Initialisiert das SSD (Single Shot MultiBox Detector) Modell."""
        model_path = os.path.join(self.models_dir, "ssd_mobilenet_v2.pb")
        config_path = os.path.join(self.models_dir, "ssd_mobilenet_v2.pbtxt")
        classes_path = os.path.join(self.models_dir, "coco.names")
        
        # Lade Klassennamen
        with open(classes_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        # Lade SSD-Netzwerk
        self.object_detector = cv2.dnn.readNetFromTensorflow(model_path, config_path)
        
        # Verwende GPU, falls konfiguriert und verfügbar
        if self.enable_gpu:
            self.object_detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.object_detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
        self.logger.info("SSD MobileNet Modell initialisiert")
    
    def _initialize_faster_rcnn(self):
        """Initialisiert das Faster R-CNN Modell."""
        model_path = os.path.join(self.models_dir, "faster_rcnn_inception_v2.pb")
        config_path = os.path.join(self.models_dir, "faster_rcnn_inception_v2.pbtxt")
        classes_path = os.path.join(self.models_dir, "coco.names")
        
        # Lade Klassennamen
        with open(classes_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        # Lade Faster R-CNN Netzwerk
        self.object_detector = cv2.dnn.readNetFromTensorflow(model_path, config_path)
        
        # Verwende GPU, falls konfiguriert und verfügbar
        if self.enable_gpu:
            self.object_detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.object_detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
        self.logger.info("Faster R-CNN Modell initialisiert")
    
    def detect_objects(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Erkennt Objekte im Bild mit dem konfigurierten Objekterkennungsmodell.
        
        Args:
            image: Eingabebild als NumPy-Array
            
        Returns:
            Liste von erkannten Objekten mit Details (Klasse, Konfidenz, Position)
        """
        if self.object_detector is None:
            self.logger.error("Objektdetektor nicht initialisiert")
            return []
        
        height, width, _ = image.shape
        
        # Vorverarbeitung des Bildes je nach Modelltyp
        if self.detection_model_type.lower() == "yolo":
            blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
            self.object_detector.setInput(blob)
            detections = self.object_detector.forward(self.output_layers)
            return self._process_yolo_detections(detections, width, height)
        elif self.detection_model_type.lower() in ["ssd", "faster_rcnn"]:
            blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False)
            self.object_detector.setInput(blob)
            detections = self.object_detector.forward()
            return self._process_ssd_detections(detections, width, height)
        else:
            self.logger.error(f"Nicht unterstützter Modelltyp für Objekterkennung: {self.detection_model_type}")
            return []
    
    def _process_yolo_detections(self, detections, width, height) -> List[Dict[str, Any]]:
        """Verarbeitet die YOLO-Detektionsergebnisse.
        
        Args:
            detections: Rohausgabe des YOLO-Netzwerks
            width: Bildbreite
            height: Bildhöhe
            
        Returns:
            Liste der erkannten Objekte mit Details
        """
        boxes = []
        confidences = []
        class_ids = []
        
        # Verarbeite alle Detektionen
        for output in detections:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > self.confidence_threshold:
                    # Objektkoordinaten
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Rechteckkoordinaten
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Verwende Non-Maximum Suppression, um überlappende Boxen zu eliminieren
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, 0.4)
        
        results = []
        for i in indices:
            if isinstance(i, list):  # Kompatibilität mit älteren OpenCV-Versionen
                i = i[0]
            
            box = boxes[i]
            x, y, w, h = box
            
            # Stelle sicher, dass die Koordinaten innerhalb des Bildes liegen
            x = max(0, x)
            y = max(0, y)
            
            class_id = class_ids[i]
            class_name = self.classes[class_id] if class_id < len(self.classes) else f"unknown_{class_id}"
            
            results.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidences[i],
                "box": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                }
            })
        
        return results
    
    def _process_ssd_detections(self, detections, width, height) -> List[Dict[str, Any]]:
        """Verarbeitet SSD- oder Faster R-CNN-Detektionsergebnisse.
        
        Args:
            detections: Rohausgabe des SSD/Faster R-CNN-Netzwerks
            width: Bildbreite
            height: Bildhöhe
            
        Returns:
            Liste der erkannten Objekte mit Details
        """
        results = []
        
        # SSD liefert: [img_id, class_id, confidence, x_min, y_min, x_max, y_max]
        for detection in detections[0, 0]:
            confidence = float(detection[2])
            
            if confidence > self.confidence_threshold:
                class_id = int(detection[1])
                
                # Skaliere Begrenzungsrahmen auf Bildgröße
                x_min = int(detection[3] * width)
                y_min = int(detection[4] * height)
                x_max = int(detection[5] * width)
                y_max = int(detection[6] * height)
                
                # Berechne Breite und Höhe
                w = x_max - x_min
                h = y_max - y_min
                
                # Stelle sicher, dass die Koordinaten innerhalb des Bildes liegen
                x_min = max(0, x_min)
                y_min = max(0, y_min)
                
                class_name = self.classes[class_id - 1] if 0 < class_id <= len(self.classes) else f"unknown_{class_id}"
                
                results.append({
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "box": {
                        "x": x_min,
                        "y": y_min,
                        "width": w,
                        "height": h
                    }
                })
        
        return results
    
    def annotate_image(self, image: np.ndarray, detections: List[Dict[str, Any]], 
                       show_labels: bool = True, color_map: Dict[str, Tuple] = None) -> np.ndarray:
        """Zeichnet erkannte Objekte ins Bild ein.
        
        Args:
            image: Originalbild als NumPy-Array
            detections: Liste der erkannten Objekte von detect_objects()
            show_labels: Ob Klassenlabels angezeigt werden sollen
            color_map: Benutzerdefinierte Farben für Klassen als Dict (Klasse -> RGB-Tuple)
            
        Returns:
            Annotiertes Bild als NumPy-Array
        """
        output_image = image.copy()
        
        # Standardfarbe, wenn keine Map angegeben ist
        default_color = (0, 255, 0)  # Grün
        
        for detection in detections:
            # Extrahiere Informationen aus der Detektion
            class_name = detection["class_name"]
            confidence = detection["confidence"]
            box = detection["box"]
            x, y, w, h = box["x"], box["y"], box["width"], box["height"]
            
            # Bestimme Farbe für diese Klasse
            if color_map and class_name in color_map:
                color = color_map[class_name]
            else:
                # Generiere eine zufällige, aber konsistente Farbe basierend auf dem Klassennamen
                color_seed = sum(ord(c) for c in class_name)
                np.random.seed(color_seed)
                color = tuple(map(int, np.random.randint(0, 255, size=3)))
            
            # Zeichne Begrenzungsrahmen
            cv2.rectangle(output_image, (x, y), (x + w, y + h), color, 2)
            
            if show_labels:
                # Bereite Label mit Klasse und Konfidenz vor
                label = f"{class_name}: {confidence:.2f}"
                
                # Bestimme Textgröße für den Hintergrund
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                
                # Zeichne Hintergrund für Text
                cv2.rectangle(output_image, (x, y - text_size[1] - 5), (x + text_size[0], y), color, -1)
                
                # Zeichne Text
                cv2.putText(output_image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
        return output_image
    
    def initialize_tracking(self, image: np.ndarray, roi: Tuple[int, int, int, int], 
                           tracker_type: str = None, object_id: str = None) -> str:
        """Initialisiert ein Tracking für eine Region (ROI) im Bild.
        
        Args:
            image: Bild, in dem getrackt werden soll
            roi: Region of Interest (x, y, width, height)
            tracker_type: Art des Trackers, überschreibt Standardeinstellung
            object_id: Optionale Objekt-ID, sonst wird automatisch generiert
            
        Returns:
            Objekt-ID für das Tracking
        """
        if tracker_type is None:
            tracker_type = self.tracker_type
        
        # Generiere eine ID für das Objekt, falls nicht angegeben
        if object_id is None:
            object_id = f"track_{int(time.time())}_{len(self.active_trackers)}"
        
        # Erstelle einen geeigneten Tracker
        tracker = self._create_tracker(tracker_type)
        
        # Initialisiere den Tracker mit dem Bild und der ROI
        bbox = roi  # (x, y, width, height)
        success = tracker.init(image, bbox)
        
        if success:
            # Speichere den aktiven Tracker
            self.active_trackers[object_id] = {
                "tracker": tracker,
                "type": tracker_type,
                "last_position": bbox,
                "created_at": datetime.now(),
                "last_updated": datetime.now(),
                "frames_tracked": 1
            }
            
            # Initialisiere Tracking-Historie
            self.tracked_objects[object_id] = {
                "positions": [bbox],
                "timestamps": [datetime.now()]
            }
            
            self.logger.info(f"Tracking initialisiert für Objekt {object_id} mit Tracker {tracker_type}")
            return object_id
        else:
            self.logger.error(f"Tracking-Initialisierung fehlgeschlagen für ROI {roi}")
            return None
    
    def _create_tracker(self, tracker_type: str):
        """Erstellt einen Tracker des angegebenen Typs.
        
        Args:
            tracker_type: Art des Trackers (CSRT, KCF, BOOSTING, MIL, TLD, MEDIANFLOW, MOSSE)
            
        Returns:
            OpenCV-Tracker-Objekt
        """
        tracker_type = tracker_type.upper()
        
        if tracker_type == 'CSRT':
            return cv2.TrackerCSRT_create()
        elif tracker_type == 'KCF':
            return cv2.TrackerKCF_create()
        elif tracker_type == 'BOOSTING':
            return cv2.legacy.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            return cv2.TrackerMIL_create()
        elif tracker_type == 'TLD':
            return cv2.legacy.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            return cv2.legacy.TrackerMedianFlow_create()
        elif tracker_type == 'MOSSE':
            return cv2.legacy.TrackerMOSSE_create()
        else:
            self.logger.warning(f"Unbekannter Tracker-Typ {tracker_type}, verwende CSRT")
            return cv2.TrackerCSRT_create()
    
    def update_tracking(self, image: np.ndarray, object_id: str) -> Optional[Tuple[bool, Tuple]]:
        """Aktualisiert das Tracking für ein bestimmtes Objekt.
        
        Args:
            image: Neues Bild für das Tracking-Update
            object_id: ID des zu trackenden Objekts
            
        Returns:
            Tuple mit (Erfolg, Begrenzungsrahmen) oder None bei ungültiger ID
        """
        if object_id not in self.active_trackers:
            self.logger.warning(f"Ungültige Objekt-ID für Tracking: {object_id}")
            return None
        
        # Hole aktiven Tracker
        tracker_info = self.active_trackers[object_id]
        tracker = tracker_info["tracker"]
        
        # Update Tracker mit neuem Frame
        success, bbox = tracker.update(image)
        
        if success:
            # Update Tracking-Informationen
            tracker_info["last_position"] = bbox
            tracker_info["last_updated"] = datetime.now()
            tracker_info["frames_tracked"] += 1
            
            # Speichere Position in Historie
            self.tracked_objects[object_id]["positions"].append(bbox)
            self.tracked_objects[object_id]["timestamps"].append(datetime.now())
            
            return (success, bbox)
        else:
            return (False, None)
    
    def stop_tracking(self, object_id: str) -> bool:
        """Beendet das Tracking für ein Objekt.
        
        Args:
            object_id: ID des Tracking-Objekts
            
        Returns:
            True wenn erfolgreich, False wenn ID ungültig
        """
        if object_id in self.active_trackers:
            # Entferne aktiven Tracker, aber behalte die Historie
            del self.active_trackers[object_id]
            self.logger.info(f"Tracking gestoppt für Objekt {object_id}")
            return True
        else:
            self.logger.warning(f"Versuche, Tracking für ungültige ID zu stoppen: {object_id}")
            return False
    
    def detect_and_track(self, image: np.ndarray, track_classes: List[str] = None, 
                         min_confidence: float = None) -> Dict[str, Any]:
        """Erkennt Objekte und startet Tracking für sie automatisch.
        
        Args:
            image: Bild zur Erkennung und Tracking
            track_classes: Optionale Liste von Klassen, die getrackt werden sollen (None = alle)
            min_confidence: Minimale Konfidenz für Tracking, überschreibt die Standardeinstellung
            
        Returns:
            Dict mit erkannten Objekten und Tracking-IDs
        """
        if min_confidence is None:
            min_confidence = self.confidence_threshold
        
        # Erkenne Objekte im Bild
        detections = self.detect_objects(image)
        
        # Ergebnisse für das Tracking
        results = {
            "detections": detections,
            "tracking_started": [],
            "tracking_updated": []
        }
        
        # Für jede Detektion überprüfen, ob sie getrackt werden soll
        for detection in detections:
            class_name = detection["class_name"]
            confidence = detection["confidence"]
            bbox = detection["box"]
            bbox_tuple = (bbox["x"], bbox["y"], bbox["width"], bbox["height"])
            
            # Prüfe, ob diese Klasse getrackt werden soll
            if track_classes is not None and class_name not in track_classes:
                continue
            
            # Prüfe, ob die Konfidenz ausreichend ist
            if confidence < min_confidence:
                continue
            
            # Erstelle eine ID basierend auf Klasse und Zeitstempel
            object_id = f"{class_name}_{int(time.time())}_{len(self.active_trackers)}"
            
            # Starte Tracking für dieses Objekt
            tracking_id = self.initialize_tracking(image, bbox_tuple, object_id=object_id)
            
            if tracking_id:
                results["tracking_started"].append({
                    "object_id": tracking_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "initial_bbox": bbox
                })
        
        # Update bestehende Trackings
        for object_id in list(self.active_trackers.keys()):
            tracking_result = self.update_tracking(image, object_id)
            
            if tracking_result:
                success, bbox = tracking_result
                
                if success:
                    results["tracking_updated"].append({
                        "object_id": object_id,
                        "bbox": {
                            "x": int(bbox[0]),
                            "y": int(bbox[1]),
                            "width": int(bbox[2]),
                            "height": int(bbox[3])
                        }
                    })
                else:
                    # Tracking fehlgeschlagen, entferne es
                    self.stop_tracking(object_id)
        
        return results
    
    def annotate_tracked_objects(self, image: np.ndarray, 
                                tracking_results: Dict[str, Any],
                                show_ids: bool = True,
                                show_trajectories: bool = False) -> np.ndarray:
        """Zeichnet getrackte Objekte in ein Bild ein.
        
        Args:
            image: Originalbild
            tracking_results: Ergebnisse von detect_and_track()
            show_ids: Ob Objekt-IDs angezeigt werden sollen
            show_trajectories: Ob Bewegungstrajektorien angezeigt werden sollen
            
        Returns:
            Annotiertes Bild
        """
        output_image = image.copy()
        
        # Zeichne aktualisierte Trackings
        for obj in tracking_results["tracking_updated"]:
            object_id = obj["object_id"]
            bbox = obj["bbox"]
            
            # Extrahiere die Klasse aus der Objekt-ID (wenn im Format "class_timestamp_index")
            class_parts = object_id.split('_')
            if len(class_parts) >= 3:
                class_name = class_parts[0]
            else:
                class_name = "unknown"
            
            # Generiere Farbe basierend auf Objekt-ID
            color_seed = sum(ord(c) for c in object_id)
            np.random.seed(color_seed)
            color = tuple(map(int, np.random.randint(0, 255, size=3)))
            
            # Zeichne Begrenzungsrahmen
            x, y, w, h = bbox["x"], bbox["y"], bbox["width"], bbox["height"]
            cv2.rectangle(output_image, (x, y), (x + w, y + h), color, 2)
            
            # Zeige ID/Klasse
            if show_ids:
                label = f"{class_name}: {object_id}"
                cv2.putText(output_image, label, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Zeichne Trajektorie wenn gewünscht und verfügbar
            if show_trajectories and object_id in self.tracked_objects:
                positions = self.tracked_objects[object_id]["positions"]
                
                # Zeichne die letzten N Positionen (max. 20)
                n_positions = min(len(positions), 20)
                for i in range(1, n_positions):
                    prev_pos = positions[-i-1]
                    curr_pos = positions[-i]
                    
                    # Berechne Mittelpunkte für eine glattere Linie
                    prev_center = (int(prev_pos[0] + prev_pos[2]/2), int(prev_pos[1] + prev_pos[3]/2))
                    curr_center = (int(curr_pos[0] + curr_pos[2]/2), int(curr_pos[1] + curr_pos[3]/2))
                    
                    # Zeichne Linie mit abnehmender Dicke für ältere Positionen
                    thickness = max(1, 3 - i//5)
                    cv2.line(output_image, prev_center, curr_center, color, thickness)
        
        # Zeichne neu erkannte Objekte
        for obj in tracking_results["tracking_started"]:
            # Diese wurden bereits in active_trackers aufgenommen und werden oben gezeichnet
            pass
        
        return output_image
    
    def init_camera(self, camera_index: int = None, resolution: Tuple[int, int] = None) -> bool:
        """Initialisiert eine Kamera für Live-Videoerfassung.
        
        Args:
            camera_index: Index der zu verwendenden Kamera (0 = Standard)
            resolution: Optionale Auflösung (Breite, Höhe)
            
        Returns:
            True wenn erfolgreich, False bei Fehler
        """
        if camera_index is not None:
            self.camera_index = camera_index
        
        # Schließe vorherige Kamera, falls vorhanden
        if self.camera is not None:
            self.camera.release()
        
        try:
            # Öffne neue Kamera
            self.camera = cv2.VideoCapture(self.camera_index)
            
            if not self.camera.isOpened():
                self.logger.error(f"Konnte Kamera mit Index {self.camera_index} nicht öffnen")
                return False
            
            # Setze Auflösung, falls angegeben
            if resolution:
                width, height = resolution
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            self.logger.info(f"Kamera initialisiert: Index {self.camera_index}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler bei Kamera-Initialisierung: {e}")
            return False
    
    def release_camera(self):
        """Gibt die Kameraressourcen frei."""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            self.logger.info("Kamera freigegeben")
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """Erfasst einen Frame von der initialisierten Kamera.
        
        Returns:
            Bild als NumPy-Array oder None bei Fehler
        """
        if self.camera is None:
            self.logger.error("Kamera nicht initialisiert")
            return None
        
        success, frame = self.camera.read()
        
        if success:
            return frame
        else:
            self.logger.error("Fehler beim Erfassen eines Frames")
            return None
    
    def detect_qr_barcodes(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Erkennt QR-Codes und Barcodes im Bild.
        
        Args:
            image: Eingabebild
            
        Returns:
            Liste der erkannten Codes mit Typ, Inhalt und Position
        """
        results = []
        
        # OpenCV 4.5.1+ hat einen Barcode-Detektor
        try:
            # Versuche mit dem barcode_BarcodeDetector
            retval, decoded_info, decoded_type, points = self.barcode_detector.detectAndDecode(image)
            
            if retval:
                for info, type_code, pts in zip(decoded_info, decoded_type, points):
                    if info:  # Nur gültige Codes
                        # Berechne Begrenzungsrahmen
                        x_values = [pt[0] for pt in pts]
                        y_values = [pt[1] for pt in pts]
                        
                        x = min(x_values)
                        y = min(y_values)
                        w = max(x_values) - x
                        h = max(y_values) - y
                        
                        results.append({
                            "type": type_code,
                            "data": info,
                            "points": pts.tolist(),
                            "box": {
                                "x": int(x),
                                "y": int(y),
                                "width": int(w),
                                "height": int(h)
                            }
                        })
            
        except AttributeError:
            # Fallback für ältere OpenCV-Versionen mit QRCodeDetector
            try:
                qr_detector = cv2.QRCodeDetector()
                data, bbox, _ = qr_detector.detectAndDecode(image)
                
                if data and bbox is not None:
                    bbox = bbox[0]
                    x_values = [pt[0] for pt in bbox]
                    y_values = [pt[1] for pt in bbox]
                    
                    x = min(x_values)
                    y = min(y_values)
                    w = max(x_values) - x
                    h = max(y_values) - y
                    
                    results.append({
                        "type": "QR-Code",
                        "data": data,
                        "points": bbox.tolist(),
                        "box": {
                            "x": int(x),
                            "y": int(y),
                            "width": int(w),
                            "height": int(h)
                        }
                    })
            except Exception as e:
                self.logger.error(f"Fehler bei QR-Code-Erkennung: {e}")
        
        return results
    
    def enhance_image_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """Verbessert ein Bild speziell für OCR-Verarbeitung.
        
        Diese Methode wendet verschiedene OpenCV-Techniken an, um die Lesbarkeit
        von Text im Bild zu optimieren und die OCR-Genauigkeit zu verbessern.
        
        Args:
            image: Eingabebild
            
        Returns:
            Verbessertes Bild für OCR
        """
        # Konvertiere zu Graustufen, falls das Bild farbig ist
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Rauschunterdrückung
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Kontrastverstärkung mit CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Binärisierung mit adaptivem Threshold
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphologische Operationen zum Verbessern der Textqualität
        # Entfernt kleine Störungen und verbindet nahe Textteile
        kernel = np.ones((1, 1), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return binary
    
    def segment_text_regions(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Segmentiert Textregionen in einem Bild mit MSER.
        
        Args:
            image: Eingabebild
            
        Returns:
            Liste von Textregionen mit Positionsdaten
        """
        # Konvertiere zu Graustufen, falls erforderlich
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # MSER für Texterkennung
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)
        
        # Erstelle Hüllrechtecke für Textregionen
        text_regions = []
        
        for region in regions:
            # Berechne Begrenzungsrechteck
            x, y, w, h = cv2.boundingRect(region)
            
            # Filtere zu kleine oder zu große Regionen
            if w < 3 or h < 3 or w > image.shape[1]//2 or h > image.shape[0]//2:
                continue
            
            # Berechne Seitenverhältnis (kann helfen, Textregionen zu identifizieren)
            aspect_ratio = w / h
            
            # Typische Textbereiche haben ein Seitenverhältnis zwischen 0.1 und 10
            if 0.1 <= aspect_ratio <= 10:
                text_regions.append({
                    "type": "text_region",
                    "box": {
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h
                    },
                    "aspect_ratio": aspect_ratio
                })
        
        # Gruppiere nahe beieinander liegende Regionen (einfache Implementierung)
        return text_regions
    
    def extract_document_from_camera(self, adjust_perspective: bool = True) -> Optional[np.ndarray]:
        """Erfasst ein Dokument von der Kamera mit automatischer Dokumentenerkennung.
        
        Args:
            adjust_perspective: Ob die Perspektive korrigiert werden soll
            
        Returns:
            Extrahiertes Dokumentbild oder None bei Fehler
        """
        if self.camera is None:
            success = self.init_camera()
            if not success:
                return None
        
        # Erfasse Frame
        frame = self.capture_frame()
        if frame is None:
            return None
        
        # Suche nach Dokumentkonturen
        document_image = self._extract_document_from_image(frame, adjust_perspective)
        return document_image
    
    def _extract_document_from_image(self, image: np.ndarray, adjust_perspective: bool = True) -> Optional[np.ndarray]:
        """Extrahiert ein Dokument aus einem Bild.
        
        Args:
            image: Eingabebild
            adjust_perspective: Ob die Perspektive korrigiert werden soll
            
        Returns:
            Extrahiertes Dokumentbild oder originales Bild, wenn kein Dokument gefunden wurde
        """
        # Konvertiere zu Graustufen
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Blur zur Rauschunterdrückung
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Kantenerkennung
        edges = cv2.Canny(blurred, 75, 200)
        
        # Finden der Konturen
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sortiere Konturen nach Größe (absteigend)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        document_contour = None
        
        # Gehe durch die größten Konturen und finde die dokumentähnlichste
        for contour in contours[:5]:  # Überprüfe nur die 5 größten Konturen
            # Annäherung der Kontur, um kleinere Details zu reduzieren
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            # Wenn wir ein Viereck haben, ist es wahrscheinlich ein Dokument
            if len(approx) == 4:
                document_contour = approx
                break
        
        # Wenn kein Dokumentkontour gefunden wurde, gib das Original zurück
        if document_contour is None:
            return image
        
        # Wenn keine Perspektivkorrektur gewünscht ist, schneide einfach den Bereich aus
        if not adjust_perspective:
            x, y, w, h = cv2.boundingRect(document_contour)
            return image[y:y+h, x:x+w]
        
        # Perspektivkorrektur
        # Ordne die Punkte in der richtigen Reihenfolge an (oben-links, oben-rechts, unten-rechts, unten-links)
        rect = self._order_points(document_contour.reshape(4, 2))
        
        # Berechne die neue Breite und Höhe
        (tl, tr, br, bl) = rect
        
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b))
        
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b))
        
        # Zielkoordinaten
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype="float32")
        
        # Berechne Perspektivtransformationsmatrix
        transform_matrix = cv2.getPerspectiveTransform(rect, dst)
        
        # Wende die Transformation an
        warped = cv2.warpPerspective(image, transform_matrix, (max_width, max_height))
        
        return warped
    
    def _order_points(self, pts):
        """Ordnet vier Punkte im Uhrzeigersinn an, beginnend mit dem oberen linken Punkt."""
        # Initialisiere geordnete Punkte
        rect = np.zeros((4, 2), dtype="float32")
        
        # Der oben-links Punkt hat die kleinste Summe
        # Der unten-rechts Punkt hat die größte Summe
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Berechne die Differenz zwischen den Punkten
        # Der oben-rechts Punkt hat die kleinste Differenz
        # Der unten-links Punkt hat die größte Differenz
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect