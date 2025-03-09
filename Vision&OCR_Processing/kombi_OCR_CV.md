# Integrationshandbuch: Universal Vision & OCR Processing Platform

## Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Architekturüberblick](#architekturüberblick)
3. [Komponentenbeschreibung](#komponentenbeschreibung)
4. [Infrastruktur-Setup](#infrastruktur-setup)
   - [Rancher-Installation](#rancher-installation)
   - [Kubernetes-Cluster-Konfiguration](#kubernetes-cluster-konfiguration)
   - [Docker-Registry und Image-Management](#docker-registry-und-image-management)
5. [Automatisierung mit Ansible](#automatisierung-mit-ansible)
   - [Dynamische YAML-Generierung](#dynamische-yaml-generierung)
   - [Container-interne Umgebungsanpassung](#container-interne-umgebungsanpassung)
6. [Integration der Kernkomponenten](#integration-der-kernkomponenten)
   - [Computer Vision Modul](#computer-vision-modul)
   - [OCR-Verarbeitungssystem](#ocr-verarbeitungssystem)
   - [Multi-Output-Prozessor](#multi-output-prozessor)
7. [Implementierung der Datenflüsse](#implementierung-der-datenflüsse)
   - [Eingabeerfassung und -verarbeitung](#eingabeerfassung-und-verarbeitung)
   - [Verarbeitungspipeline](#verarbeitungspipeline)
   - [Ausgabegenerierung und -verteilung](#ausgabegenerierung-und-verteilung)
8. [KI-Integration für erweiterte Funktionen](#ki-integration-für-erweiterte-funktionen)
   - [Sprachausgabe und Objektbeschreibung](#sprachausgabe-und-objektbeschreibung)
   - [Räumliches Bewusstsein und Distanzmessung](#räumliches-bewusstsein-und-distanzmessung)
9. [Sicherheitsimplementierung](#sicherheitsimplementierung)
   - [Authentifizierung und Autorisierung](#authentifizierung-und-autorisierung)
   - [Verschlüsselung und Datenschutz](#verschlüsselung-und-datenschutz)
   - [Secure Configuration Management](#secure-configuration-management)
10. [Performanceoptimierung](#performanceoptimierung)
    - [Ressourcenmanagement](#ressourcenmanagement)
    - [Caching-Strategien](#caching-strategien)
    - [Skalierungsrichtlinien](#skalierungsrichtlinien)
11. [Deployment-Anleitung](#deployment-anleitung)
    - [Entwicklungsumgebung](#entwicklungsumgebung)
    - [Testumgebung](#testumgebung)
    - [Produktionsumgebung](#produktionsumgebung)
12. [Monitoring und Wartung](#monitoring-und-wartung)
    - [Metriken und Warnmeldungen](#metriken-und-warnmeldungen)
    - [Protokollmanagement](#protokollmanagement)
    - [Systemwartung](#systemwartung)
13. [Fehlerbehebung](#fehlerbehebung)
    - [Häufige Probleme und Lösungen](#häufige-probleme-und-lösungen)
    - [Diagnosetools](#diagnosetools)
14. [Fallbeispiele](#fallbeispiele)
    - [Echtzeit-Videoanalyse mit Sprachfeedback](#echtzeit-videoanalyse-mit-sprachfeedback)
    - [Batchverarbeitung von Dokumenten](#batchverarbeitung-von-dokumenten)
    - [Interaktives Objekterkennung-Szenario](#interaktives-objekterkennung-szenario)

## Einführung

Dieses Integrationshandbuch dokumentiert die umfassende Zusammenführung des Computer Vision Moduls und des Universal OCR Tools 2.0 zu einer leistungsstarken und flexiblen Plattform für Bild-, Video- und Dokumentenverarbeitung. Die resultierende Lösung vereint fortschrittliche Objekterkennung, präzise OCR-Fähigkeiten und innovative KI-Funktionen in einem skalierbaren, containerisierten System, das durch Rancher orchestriert und mit Ansible automatisiert wird.

Die integrierte Plattform kann Eingaben aus verschiedenen Quellen verarbeiten, darunter:
- Bilder in verschiedenen Formaten 
- PDF-Dokumente (auch beschädigte)
- Live-Videostreams von Kameras
- Bereits vorhandene Dokumente aus Datenbanken oder APIs

Nach der Verarbeitung können die Ergebnisse in vielfältigen Formaten ausgegeben werden:
- Extrahierter Text (strukturiert oder unstrukturiert)
- Annotierte Bilder mit erkannten Objekten und Text
- Aufbereitete PDF-Dokumente
- Kombinierte Berichte aus Text und Bildern
- Echtzeit-Sprachausgabe für erkannte Elemente
- Strukturierte Daten für Weiterverarbeitung durch andere Systeme

Dieses Dokument richtet sich an Systemarchitekten, DevOps-Ingenieure und Entwickler, die eine fortschrittliche Vision- und OCR-Lösung implementieren möchten, die modernsten Anforderungen an Skalierbarkeit, Sicherheit und Automatisierung entspricht.

## Architekturüberblick

Die integrierte Plattform ist nach modernen Microservice-Prinzipien aufgebaut und folgt einer mehrschichtigen Architektur, die durch Kubernetes orchestriert und von Rancher verwaltet wird.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Client-Zugriffsschicht                         │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────────────┐    │
│  │  REST API     │    │  Web Interface│    │  Command Line Client   │    │
│  └───────────────┘    └───────────────┘    └───────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Orchestrierungsschicht                           │
│  ┌───────────────────────────────┐    ┌───────────────────────────────┐ │
│  │        Rancher Dashboard      │    │       Kubernetes Cluster      │ │
│  └───────────────────────────────┘    └───────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Anwendungsschicht                                │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────────────┐    │
│  │ Vision Module │    │  OCR Engine   │    │   Multi-Output        │    │
│  │  Microservice │    │  Microservice │    │   Processor           │    │
│  └───────────────┘    └───────────────┘    └───────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Verarbeitungsschicht                             │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────────────┐    │
│  │ Worker Pods   │    │ Async Task    │    │   Resource Governor    │    │
│  │ (Skalierbar)  │    │ Processor     │    │                        │    │
│  └───────────────┘    └───────────────┘    └───────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Integrationsschicht                              │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────────────┐    │
│  │ KI-Modul für  │    │ Räumliche     │    │   Sprachausgabe-      │    │
│  │ Verarbeitung  │    │ Analyse       │    │   System              │    │
│  └───────────────┘    └───────────────┘    └───────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Datenhaltungsschicht                             │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────────────┐    │
│  │ Redis Cache   │    │ PostgreSQL    │    │   Object Storage      │    │
│  │               │    │ Datenbank     │    │   (MinIO)             │    │
│  └───────────────┘    └───────────────┘    └───────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

Die Architektur ist darauf ausgelegt, skalierbar, widerstandsfähig und sicher zu sein, während sie gleichzeitig eine hohe Flexibilität bei der Verarbeitung und Ausgabe gewährleistet. Jede Komponente kann unabhängig skaliert werden, um den spezifischen Anforderungen an Durchsatz und Ressourcenverfügbarkeit gerecht zu werden.

## Komponentenbeschreibung

### Kernkomponenten

1. **Computer Vision Modul**
   - Objekterkennung mit verschiedenen Detektionsmodellen (YOLO, SSD, Faster R-CNN)
   - Objektverfolgung in Videos und Echtzeit-Streams
   - Kamera-Integration für direkte Bilderfassung
   - QR-Code- und Barcode-Erkennung
   - Räumliche Analyse zur Distanzmessung

2. **Neural OCR Engine**
   - Fortschrittliche Texterkennung mit Deep-Learning-Modellen
   - Sprachspezifische OCR-Modelle für verbesserte Mehrsprachigkeit
   - Layoutanalyse für strukturierte Dokumentenverarbeitung
   - Handschrifterkennung
   - Bildvorverarbeitung mit adaptiven Techniken

3. **Multi-Output-Prozessor**
   - Flexible Ausgabegenerierung in verschiedenen Formaten
   - API-Integration für Datenweitergabe
   - Annotierte Bildgenerierung
   - Kombinierte Dokumentenerstellung (Text + Bilder)
   - Formatierte Berichte und Datenextrakte

4. **KI-Integrationsmodul**
   - Sprachgenerierung für erkannte Objekte und Texte
   - Semantische Analyse des Inhalts
   - Personalisierte Interaktionslogik
   - Echtzeit-Feedback-Generierung

### Infrastrukturkomponenten

1. **Rancher**
   - Zentrale Verwaltungsoberfläche für Kubernetes
   - Multi-Cluster-Management
   - Benutzerfreundliches Ressourcenmanagement
   - Integrierte CI/CD-Pipeline-Unterstützung

2. **Kubernetes**
   - Container-Orchestrierung
   - Automatische Skalierung
   - Self-Healing-Funktionalität
   - Ressourcenoptimierung

3. **Ansible**
   - Automatisierte Konfigurationsverwaltung
   - Dynamische YAML-Generierung für Kubernetes
   - Infrastructure-as-Code-Prinzipien
   - Container-interne Konfigurationsanpassung

4. **Docker**
   - Containerisierung aller Komponenten
   - Standardisierte Umgebungen
   - Isolierte Ausführung
   - Effizientes Ressourcenmanagement

### Datenspeicher und Cache

1. **Redis**
   - In-Memory-Caching für hohe Performance
   - Task-Queue für asynchrone Verarbeitung
   - Pub/Sub-Mechanismus für Ereigniskommunikation

2. **PostgreSQL**
   - Persistente Datenspeicherung
   - Verwaltung strukturierter Daten und Metadaten
   - Abfrage-Optimierung für komplexe Datenstrukturen

3. **MinIO**
   - Objektspeicher für Bilder, Videos und Dokumente
   - S3-kompatible API
   - Hoher Durchsatz und Skalierbarkeit

## Infrastruktur-Setup

### Rancher-Installation

Rancher dient als zentrale Verwaltungsschnittstelle für alle Kubernetes-Cluster und erleichtert die Bereitstellung, Überwachung und Wartung der Plattform erheblich.

#### Installationsschritte:

1. **Docker-Installation auf dem Rancher-Server**:

```bash
# Aktualisieren der Paketlisten
sudo apt-get update

# Installation von Docker-Abhängigkeiten
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Hinzufügen des Docker-Repositorys
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Docker installieren
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Docker-Dienst aktivieren
sudo systemctl enable docker
sudo systemctl start docker
```

2. **Rancher-Bereitstellung**:

```bash
# Rancher mit persistentem Volume bereitstellen
sudo docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  -v /opt/rancher:/var/lib/rancher \
  --privileged \
  rancher/rancher:latest
```

3. **Initialisierung und Zugriffsabsicherung**:
   - Rufen Sie die Rancher-Weboberfläche unter https://[SERVER_IP] auf
   - Setzen Sie ein sicheres Admin-Passwort
   - Konfigurieren Sie die Authentifizierungsmethode (LDAP/Active Directory empfohlen für Unternehmensumgebungen)

### Kubernetes-Cluster-Konfiguration

Rancher vereinfacht die Erstellung und Verwaltung von Kubernetes-Clustern erheblich. Für die integrierte Plattform empfehlen wir einen dedizierten Produktionscluster und separate Test- und Entwicklungscluster.

#### Produktionscluster-Einrichtung:

1. **Cluster-Erstellung über Rancher-UI**:
   - Navigieren Sie zu "Cluster Management" > "Create Cluster"
   - Wählen Sie den Anbieter (RKE für On-Premise, oder Cloud-Provider wie AWS/GCP/Azure)
   - Konfigurieren Sie die Node-Pools (mindestens 3 Control Plane, 2 etcd und 3+ Worker Nodes für Produktionsumgebungen)

2. **Netzwerkkonfiguration**:
   - Wählen Sie Calico als CNI-Plugin für erweiterte Netzwerkrichtlinien
   - Aktivieren Sie den Ingress-Controller
   - Konfigurieren Sie den Load Balancer Service entsprechend Ihrer Infrastruktur

3. **Persistenter Speicher**:
   - Konfigurieren Sie StorageClasses für verschiedene Leistungsanforderungen
   - Für Produktionsumgebungen empfehlen wir:
     - `fast-storage`: SSD-basiert für Datenbanken und Caches
     - `standard-storage`: für allgemeine Anwendungsdaten
     - `bulk-storage`: für große Datensätze und Archivdaten

4. **Ressourcenbeschränkungen**:
   - Definieren Sie ResourceQuotas für Namespaces
   - Konfigurieren Sie LimitRanges für Standardressourcenbeschränkungen

Beispiel für namespace-spezifische ResourceQuota:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ocr-vision-quota
  namespace: ocr-vision-system
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    persistentvolumeclaims: "20"
```

### Docker-Registry und Image-Management

Eine private Docker-Registry ist entscheidend für die Verwaltung der benutzerdefinierten Images und die Beschleunigung des Deployments.

#### Einrichtung der privaten Registry:

1. **Harbor-Registry-Deployment**:

```bash
# Harbor Helm Repository hinzufügen
helm repo add harbor https://helm.goharbor.io

# Harbor installieren
helm install harbor harbor/harbor \
  --namespace harbor \
  --create-namespace \
  --set expose.type=ingress \
  --set expose.tls.enabled=true \
  --set externalURL=https://harbor.[DOMAIN] \
  --set persistence.enabled=true \
  --set persistence.persistentVolumeClaim.registry.size=100Gi
```

2. **Image-Build und Push-Workflow mit GitLab CI/CD**:

```yaml
# .gitlab-ci.yml für automatisierte Image-Builds
stages:
  - build
  - test
  - push

variables:
  DOCKER_REGISTRY: harbor.[DOMAIN]/ocr-vision

build-vision-module:
  stage: build
  script:
    - docker build -t $DOCKER_REGISTRY/vision-module:$CI_COMMIT_SHORT_SHA -f docker/vision/Dockerfile .
    - docker tag $DOCKER_REGISTRY/vision-module:$CI_COMMIT_SHORT_SHA $DOCKER_REGISTRY/vision-module:latest

test-vision-module:
  stage: test
  script:
    - docker run --rm $DOCKER_REGISTRY/vision-module:$CI_COMMIT_SHORT_SHA pytest -xvs tests/vision/

push-vision-module:
  stage: push
  script:
    - docker login $DOCKER_REGISTRY -u $REGISTRY_USER -p $REGISTRY_PASSWORD
    - docker push $DOCKER_REGISTRY/vision-module:$CI_COMMIT_SHORT_SHA
    - docker push $DOCKER_REGISTRY/vision-module:latest
  only:
    - master
```

3. **Image-Pull-Secrets in Kubernetes konfigurieren**:

```bash
# Registry-Zugangsdaten als Secret speichern
kubectl create secret docker-registry harbor-registry-secret \
  --docker-server=harbor.[DOMAIN] \
  --docker-username=[USERNAME] \
  --docker-password=[PASSWORD] \
  --docker-email=[EMAIL] \
  --namespace=ocr-vision-system
```

## Automatisierung mit Ansible

### Dynamische YAML-Generierung

Ansible ermöglicht die dynamische Generierung von Kubernetes-Konfigurationen basierend auf der Umgebung und den Anforderungen.

#### Ansible-Playbook für Kubernetes-Konfigurationen:

```yaml
# kubernetes-config.yml
---
- name: Generate Kubernetes Configurations
  hosts: localhost
  connection: local
  vars_files:
    - vars/environment_config.yml
    - vars/component_versions.yml
  vars:
    namespace: "{{ env }}-ocr-vision-system"
  tasks:
    - name: Create namespace directory
      file:
        path: "generated_configs/{{ namespace }}"
        state: directory
        mode: '0755'

    - name: Generate Vision Module Deployment
      template:
        src: templates/vision-module-deployment.yml.j2
        dest: "generated_configs/{{ namespace }}/vision-module-deployment.yml"
      vars:
        component_name: vision-module
        replicas: "{{ env_configs[env].vision_module.replicas }}"
        cpu_request: "{{ env_configs[env].vision_module.resources.cpu_request }}"
        memory_request: "{{ env_configs[env].vision_module.resources.memory_request }}"
        cpu_limit: "{{ env_configs[env].vision_module.resources.cpu_limit }}"
        memory_limit: "{{ env_configs[env].vision_module.resources.memory_limit }}"
        image_tag: "{{ component_versions.vision_module }}"

    - name: Generate OCR Engine Deployment
      template:
        src: templates/ocr-engine-deployment.yml.j2
        dest: "generated_configs/{{ namespace }}/ocr-engine-deployment.yml"
      vars:
        component_name: ocr-engine
        replicas: "{{ env_configs[env].ocr_engine.replicas }}"
        cpu_request: "{{ env_configs[env].ocr_engine.resources.cpu_request }}"
        memory_request: "{{ env_configs[env].ocr_engine.resources.memory_request }}"
        cpu_limit: "{{ env_configs[env].ocr_engine.resources.cpu_limit }}"
        memory_limit: "{{ env_configs[env].ocr_engine.resources.memory_limit }}"
        image_tag: "{{ component_versions.ocr_engine }}"

    - name: Apply Kubernetes Configurations
      k8s:
        state: present
        src: "generated_configs/{{ namespace }}/{{ item }}"
        kubeconfig: "{{ kubeconfig_path }}"
      loop:
        - vision-module-deployment.yml
        - ocr-engine-deployment.yml
      when: apply_configs | default(false) | bool
```

Template-Beispiel für die Vision-Modul-Bereitstellung:

```yaml
# templates/vision-module-deployment.yml.j2
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ component_name }}
  namespace: {{ namespace }}
  labels:
    app: ocr-vision
    component: {{ component_name }}
spec:
  replicas: {{ replicas }}
  selector:
    matchLabels:
      app: ocr-vision
      component: {{ component_name }}
  template:
    metadata:
      labels:
        app: ocr-vision
        component: {{ component_name }}
    spec:
      containers:
      - name: {{ component_name }}
        image: {{ registry_url }}/ocr-vision/{{ component_name }}:{{ image_tag }}
        resources:
          requests:
            cpu: {{ cpu_request }}
            memory: {{ memory_request }}
          limits:
            cpu: {{ cpu_limit }}
            memory: {{ memory_limit }}
        env:
        - name: ENVIRONMENT
          value: {{ env }}
        - name: LOG_LEVEL
          value: {{ log_level | default('INFO') }}
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: models-volume
          mountPath: /app/models
      volumes:
      - name: config-volume
        configMap:
          name: {{ component_name }}-config
      - name: models-volume
        persistentVolumeClaim:
          claimName: models-pvc
      imagePullSecrets:
      - name: harbor-registry-secret
```

### Container-interne Umgebungsanpassung

Für Situationen, in denen Anpassungen innerhalb der Container notwendig sind, nutzen wir Ansible innerhalb der Container zur Laufzeit.

#### Ansible-Container-Setup:

1. **Basis-Image mit Ansible**:

```dockerfile
# Dockerfile.ansible-base
FROM python:3.9-slim

# Ansible und benötigte Pakete installieren
RUN apt-get update && apt-get install -y \
    ansible \
    openssh-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Standardkonfiguration für Ansible
COPY ansible.cfg /etc/ansible/ansible.cfg

# Arbeitsverzeichnis
WORKDIR /ansible

# Entrypoint-Skript
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

2. **Init-Container für Container-Konfiguration**:

```yaml
# In den Kubernetes-Deployment-Vorlagen hinzufügen
initContainers:
- name: config-init
  image: {{ registry_url }}/ocr-vision/ansible-base:latest
  command: ['ansible-playbook', 'container-setup.yml']
  env:
  - name: COMPONENT_TYPE
    value: {{ component_name }}
  - name: CONFIG_VERSION
    value: {{ config_version }}
  volumeMounts:
  - name: app-volume
    mountPath: /app
  - name: config-volume
    mountPath: /ansible/configs
  - name: playbooks-volume
    mountPath: /ansible/playbooks
```

3. **Beispiel-Playbook für Container-Konfiguration**:

```yaml
# container-setup.yml
---
- name: Container Setup
  hosts: localhost
  connection: local
  vars:
    component_type: "{{ lookup('env', 'COMPONENT_TYPE') }}"
    config_version: "{{ lookup('env', 'CONFIG_VERSION') }}"
  tasks:
    - name: Include component-specific variables
      include_vars:
        file: "configs/{{ component_type }}-vars.yml"

    - name: Configure application files
      template:
        src: "templates/{{ component_type }}/{{ item.src }}"
        dest: "/app/{{ item.dest }}"
        mode: "{{ item.mode | default('0644') }}"
      loop: "{{ config_files }}"

    - name: Configure models directory
      file:
        path: "/app/models/{{ item.path }}"
        state: directory
        mode: '0755'
      loop: "{{ model_directories }}"
      when: model_directories is defined

    - name: Download model files if needed
      get_url:
        url: "{{ item.url }}"
        dest: "/app/models/{{ item.path }}"
        mode: '0644'
        checksum: "{{ item.checksum | default(omit) }}"
      loop: "{{ model_files }}"
      when: model_files is defined and download_models | default(false) | bool
```

## Integration der Kernkomponenten

### Computer Vision Modul

Das Computer Vision Modul bietet fortschrittliche Bildverarbeitungs- und Objekterkennungsfunktionen, die für vielfältige Aufgaben genutzt werden können.

#### Vision-Modul-API-Integration:

```python
# api/vision_service.py
from fastapi import FastAPI, File, UploadFile, Form, Depends, Query
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from typing import List, Optional
import asyncio

from vision.computer_vision_module import ComputerVisionModule
from common.auth import get_current_user
from common.models import DetectionResult

app = FastAPI(title="Vision Module API")

# Globale Instanz des Computer Vision Moduls
vision_module = None

@app.on_event("startup")
async def startup_event():
    """Initialisiert das Vision-Modul beim Start der API."""
    global vision_module
    
    # Konfiguration laden
    config = {
        "detection_model": "yolo",
        "yolo_version": "yolov4",
        "enable_gpu": True,
        "confidence_threshold": 0.5,
        "models_dir": "/app/models/vision"
    }
    
    # Computer Vision Modul initialisieren
    vision_module = ComputerVisionModule(config)

@app.post("/detect", response_model=List[DetectionResult])
async def detect_objects(
    file: UploadFile = File(...),
    confidence: float = Query(0.5, ge=0.0, le=1.0),
    current_user: str = Depends(get_current_user)
):
    """Erkennt Objekte in einem hochgeladenen Bild."""
    try:
        # Bild einlesen
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return JSONResponse(
                status_code=400,
                content={"message": "Ungültiges Bildformat oder beschädigte Datei."}
            )
        
        # Objekte erkennen
        vision_module.confidence_threshold = confidence
        detections = vision_module.detect_objects(image)
        
        return detections
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler bei der Objekterkennung: {str(e)}"}
        )

@app.post("/track")
async def track_objects(
    file: UploadFile = File(...),
    track_classes: str = Form(None),
    min_confidence: float = Query(0.5, ge=0.0, le=1.0),
    current_user: str = Depends(get_current_user)
):
    """Erkennt und trackt Objekte in einem Video."""
    try:
        # Video temporär speichern
        temp_file = f"/tmp/{file.filename}"
        with open(temp_file, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Tracking-Klassen verarbeiten
        track_class_list = None
        if track_classes:
            track_class_list = [cls.strip() for cls in track_classes.split(",")]
        
        # Video-Tracking als Hintergrundaufgabe starten
        task_id = await start_tracking_task(temp_file, track_class_list, min_confidence)
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": "Video-Tracking gestartet."
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler beim Starten des Tracking-Prozesses: {str(e)}"}
        )

async def start_tracking_task(video_path, track_classes, min_confidence):
    """Startet eine Hintergrundaufgabe für Video-Tracking."""
    # Task-ID generieren
    task_id = f"track_{int(time.time())}"
    
    # Hintergrundaufgabe starten
    asyncio.create_task(
        process_video_tracking(task_id, video_path, track_classes, min_confidence)
    )
    
    return task_id

async def process_video_tracking(task_id, video_path, track_classes, min_confidence):
    """Verarbeitet das Video-Tracking als Hintergrundaufgabe."""
    # Implementierung der Video-Tracking-Logik
    # Diese Funktion würde Tracking-Ergebnisse in einer Datenbank oder einem Cache speichern
    pass
```

#### Integration der Kamera-Funktionalität:

```python
# services/camera_service.py

import cv2
import time
import threading
import queue
from typing import Dict, Any, Optional

class CameraService:
    """Service für die Verwaltung von Kamerastreams und deren Verarbeitung."""
    
    def __init__(self, vision_module):
        """Initialisiert den Kamera-Service.
        
        Args:
            vision_module: Eine Instanz des Computer Vision Moduls
        """
        self.vision_module = vision_module
        self.active_cameras = {}  # camera_id -> {camera, thread, running}
        self.frame_queues = {}    # camera_id -> queue
        self.processing_settings = {}  # camera_id -> settings
    
    def start_camera(self, camera_id: str, source: str, 
                    processing_settings: Optional[Dict[str, Any]] = None) -> bool:
        """Startet einen Kamerastream.
        
        Args:
            camera_id: Eindeutige ID für die Kamera
            source: Kameraquelle (Pfad, URL, Geräte-ID)
            processing_settings: Einstellungen für die Bildverarbeitung
            
        Returns:
            bool: True, wenn der Start erfolgreich war, sonst False
        """
        if camera_id in self.active_cameras:
            return False  # Kamera bereits aktiv
        
        # Standardeinstellungen falls nicht angegeben
        if processing_settings is None:
            processing_settings = {
                "detect_objects": True,
                "track_objects": False,
                "detect_text": False,
                "track_classes": None,
                "min_confidence": 0.5,
                "frame_interval": 1  # Jeder Frame wird verarbeitet
            }
        
        # Kamera öffnen
        camera = cv2.VideoCapture(source)
        if not camera.isOpened():
            return False
        
        # Frame-Queue erstellen
        frame_queue = queue.Queue(maxsize=30)  # Max. 30 Frames im Puffer
        self.frame_queues[camera_id] = frame_queue
        
        # Verarbeitungseinstellungen speichern
        self.processing_settings[camera_id] = processing_settings
        
        # Thread für Kameraverarbeitung starten
        running = threading.Event()
        running.set()
        thread = threading.Thread(
            target=self._process_camera_frames,
            args=(camera_id, camera, frame_queue, running)
        )
        thread.daemon = True
        thread.start()
        
        # Kamera als aktiv speichern
        self.active_cameras[camera_id] = {
            "camera": camera,
            "thread": thread,
            "running": running,
            "start_time": time.time()
        }
        
        return True
    
    def stop_camera(self, camera_id: str) -> bool:
        """Stoppt einen Kamerastream.
        
        Args:
            camera_id: ID des zu stoppenden Kamerastreams
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if camera_id not in self.active_cameras:
            return False
        
        # Thread stoppen
        self.active_cameras[camera_id]["running"].clear()
        
        # Auf Thread-Ende warten (max. 5 Sekunden)
        self.active_cameras[camera_id]["thread"].join(timeout=5)
        
        # Kamera freigeben
        self.active_cameras[camera_id]["camera"].release()
        
        # Kamera aus aktiven Kameras entfernen
        del self.active_cameras[camera_id]
        del self.frame_queues[camera_id]
        del self.processing_settings[camera_id]
        
        return True
    
    def get_latest_frame(self, camera_id: str) -> Optional[Dict[str, Any]]:
        """Gibt den neuesten verarbeiteten Frame einer Kamera zurück.
        
        Args:
            camera_id: ID des Kamerastreams
            
        Returns:
            Optional[Dict]: Frame-Informationen oder None, wenn nicht verfügbar
        """
        if camera_id not in self.frame_queues:
            return None
        
        # Neuesten Frame aus der Queue holen (ohne Blockieren)
        try:
            frame_data = self.frame_queues[camera_id].get_nowait()
            self.frame_queues[camera_id].task_done()
            return frame_data
        except queue.Empty:
            return None
    
    def _process_camera_frames(self, camera_id: str, camera, frame_queue, running):
        """Verarbeitet kontinuierlich Frames von der Kamera.
        
        Diese Methode läuft in einem separaten Thread für jede Kamera.
        
        Args:
            camera_id: ID des Kamerastreams
            camera: OpenCV-Kameraobjekt
            frame_queue: Queue für verarbeitete Frames
            running: Threading-Event zum Signalisieren, wann der Thread stoppen soll
        """
        frame_count = 0
        
        while running.is_set():
            # Frame von der Kamera lesen
            ret, frame = camera.read()
            if not ret:
                # Fehler beim Lesen des Frames
                time.sleep(0.1)
                continue
            
            # Prüfen, ob dieser Frame verarbeitet werden soll
            frame_interval = self.processing_settings[camera_id]["frame_interval"]
            if frame_count % frame_interval != 0:
                frame_count += 1
                continue
            
            # Frame verarbeiten basierend auf den Einstellungen
            settings = self.processing_settings[camera_id]
            processed_data = {
                "timestamp": time.time(),
                "frame_number": frame_count,
                "original_frame": frame
            }
            
            try:
                # Objekterkennung
                if settings["detect_objects"]:
                    detections = self.vision_module.detect_objects(frame)
                    processed_data["detections"] = detections
                    
                    # Frame mit Annotationen
                    annotated_frame = self.vision_module.annotate_image(
                        frame, detections, show_labels=True
                    )
                    processed_data["annotated_frame"] = annotated_frame
                
                # Objekt-Tracking
                if settings["track_objects"]:
                    track_results = self.vision_module.detect_and_track(
                        frame, 
                        track_classes=settings["track_classes"],
                        min_confidence=settings["min_confidence"]
                    )
                    processed_data["tracking"] = track_results
                    
                    # Frame mit Tracking-Visualisierung
                    tracking_frame = self.vision_module.annotate_tracked_objects(
                        frame, track_results, show_trajectories=True
                    )
                    processed_data["tracking_frame"] = tracking_frame
                
                # OCR-Integration (falls Text erkannt werden soll)
                if settings["detect_text"]:
                    # Dies würde eine Integration mit dem OCR-Engine erfordern
                    # Hier nur als Platzhalter
                    # processed_data["text"] = ocr_engine.recognize_text(frame)
                    pass
                
                # Frame in die Queue stellen (nicht blockierend)
                if not frame_queue.full():
                    frame_queue.put_nowait(processed_data)
                else:
                    # Bei voller Queue ältesten Frame entfernen und neuen einfügen
                    try:
                        frame_queue.get_nowait()
                        frame_queue.put_nowait(processed_data)
                    except Exception:
                        pass
            
            except Exception as e:
                # Fehler bei der Verarbeitung protokollieren
                print(f"Fehler bei der Verarbeitung von Kamera {camera_id}: {e}")
            
            # Frame-Zähler erhöhen
            frame_count += 1
            
            # Kurze Pause, um CPU-Überlastung zu vermeiden
            time.sleep(0.01)
```

### OCR-Verarbeitungssystem

Das OCR-Verarbeitungssystem basiert auf dem Neural OCR Engine und bietet fortschrittliche Texterkennung mit verschiedenen sprachspezifischen Modellen.

#### OCR-Service-Integration:

```python
# api/ocr_service.py
from fastapi import FastAPI, File, UploadFile, Form, Depends, Query
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from typing import Dict, Any, List, Optional
import time
import asyncio
import os

from ocr.neural_ocr_engine import NeuralOCREngine
from common.auth import get_current_user
from common.models import OCRResult

app = FastAPI(title="OCR Engine API")

# Globale Instanz der OCR-Engine
ocr_engine = None

@app.on_event("startup")
async def startup_event():
    """Initialisiert die OCR-Engine beim Start der API."""
    global ocr_engine
    
    # Konfiguration laden
    config = {
        "model_path": "/app/models/ocr",
        "languages": ["eng", "deu", "fra", "spa", "ita"],
        "enable_gpu": True,
        "preprocessing": {
            "enable_adaptive": True,
            "default_dpi": 300
        }
    }
    
    # OCR-Engine initialisieren
    ocr_engine = NeuralOCREngine(config)

@app.post("/recognize", response_model=OCRResult)
async def recognize_text(
    file: UploadFile = File(...),
    languages: str = Form(None),
    enhance_image: bool = Form(True),
    current_user: str = Depends(get_current_user)
):
    """Erkennt Text in einem hochgeladenen Bild oder Dokument."""
    try:
        # Datei temporär speichern
        temp_file = f"/tmp/{file.filename}"
        with open(temp_file, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Sprachen verarbeiten
        languages_list = None
        if languages:
            languages_list = [lang.strip() for lang in languages.split(",")]
        
        # OCR-Optionen
        options = {
            "languages": languages_list,
            "enhance_image": enhance_image
        }
        
        # Dateiendung bestimmen
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        # PDF oder Bild
        if file_extension == ".pdf":
            task_id = await start_pdf_ocr_task(temp_file, options)
            return {
                "task_id": task_id,
                "status": "processing",
                "message": "PDF-Verarbeitung gestartet."
            }
        else:
            # Bild direkt verarbeiten
            image = cv2.imread(temp_file)
            if image is None:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Ungültiges Bildformat oder beschädigte Datei."}
                )
            
            # OCR durchführen
            result = ocr_engine.recognize_text(image, options)
            
            # Temporäre Datei löschen
            try:
                os.remove(temp_file)
            except:
                pass
            
            return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler bei der Texterkennung: {str(e)}"}
        )

async def start_pdf_ocr_task(pdf_path, options):
    """Startet eine Hintergrundaufgabe für PDF-OCR."""
    # Task-ID generieren
    task_id = f"ocr_{int(time.time())}"
    
    # Hintergrundaufgabe starten
    asyncio.create_task(
        process_pdf_ocr(task_id, pdf_path, options)
    )
    
    return task_id

async def process_pdf_ocr(task_id, pdf_path, options):
    """Verarbeitet PDF-OCR als Hintergrundaufgabe."""
    # Implementierung der PDF-OCR-Logik
    # Diese Funktion würde OCR-Ergebnisse in einer Datenbank oder einem Cache speichern
    pass

@app.get("/task/{task_id}")
async def get_task_status(
    task_id: str,
    current_user: str = Depends(get_current_user)
):
    """Gibt den Status einer OCR-Aufgabe zurück."""
    # Implementierung der Task-Status-Abfrage
    # Dies würde den Fortschritt und die Ergebnisse aus einer Datenbank oder einem Cache abrufen
    pass
```

#### Integration der Dokumentenvorverarbeitung:

```python
# ocr/document_preprocessor.py
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional

class DocumentPreprocessor:
    """Erweiterte Dokumentenvorverarbeitung für OCR-Optimierung."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert den Dokumentenprozessor mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen für die Vorverarbeitung
        """
        self.config = config
        self.default_dpi = config.get("default_dpi", 300)
        self.enable_adaptive = config.get("enable_adaptive", True)
    
    def preprocess(self, image: np.ndarray, document_type: str = "general") -> np.ndarray:
        """Wendet optimale Vorverarbeitungsschritte auf ein Dokument an.
        
        Args:
            image: Eingabebild als NumPy-Array
            document_type: Art des Dokuments für spezialisierte Verarbeitung
            
        Returns:
            Vorverarbeitetes Bild
        """
        # Bild in Graustufen konvertieren, falls farbig
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Rauschunterdrückung
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Dokumenttyp-spezifische Verarbeitung
        if document_type == "text":
            return self._process_text_document(denoised)
        elif document_type == "form":
            return self._process_form_document(denoised)
        elif document_type == "handwritten":
            return self._process_handwritten_document(denoised)
        else:
            # Allgemeine Dokumentverarbeitung
            return self._process_general_document(denoised)
    
    def _process_text_document(self, image: np.ndarray) -> np.ndarray:
        """Verarbeitet ein Textdokument für optimale OCR-Ergebnisse.
        
        Args:
            image: Graustufenbild
            
        Returns:
            Vorverarbeitetes Bild
        """
        # Kontrastverstärkung mit CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Binärisierung mit adaptivem Threshold
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphologische Operationen zum Verbessern der Textqualität
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return processed
    
    def _process_form_document(self, image: np.ndarray) -> np.ndarray:
        """Verarbeitet ein Formular für optimale OCR-Ergebnisse.
        
        Erhält Linien und Kästchen in Formularen.
        
        Args:
            image: Graustufenbild
            
        Returns:
            Vorverarbeitetes Bild
        """
        # Adaptiver Threshold für Textbeibehaltung
        binary = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY, 15, 2
        )
        
        # Linien und Kästchen verstärken
        kernel_horizontal = np.ones((1, 40), np.uint8)
        kernel_vertical = np.ones((40, 1), np.uint8)
        
        # Horizontale Linien erkennen
        horizontal = cv2.morphologyEx(255 - binary, cv2.MORPH_OPEN, kernel_horizontal)
        
        # Vertikale Linien erkennen
        vertical = cv2.morphologyEx(255 - binary, cv2.MORPH_OPEN, kernel_vertical)
        
        # Linien kombinieren und dem Originalbild hinzufügen
        lines = cv2.add(horizontal, vertical)
        result = cv2.subtract(binary, lines)
        
        return result
    
    def _process_handwritten_document(self, image: np.ndarray) -> np.ndarray:
        """Verarbeitet ein handschriftliches Dokument für optimale OCR-Ergebnisse.
        
        Verwendet sanftere Methoden, um Handschriftdetails zu erhalten.
        
        Args:
            image: Graustufenbild
            
        Returns:
            Vorverarbeitetes Bild
        """
        # Weichere Kontrastverstärkung
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Binarisierung mit Otsu-Methode
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def _process_general_document(self, image: np.ndarray) -> np.ndarray:
        """Verarbeitet ein allgemeines Dokument für optimale OCR-Ergebnisse.
        
        Ausgeglichene Verarbeitung für unbekannte Dokumenttypen.
        
        Args:
            image: Graustufenbild
            
        Returns:
            Vorverarbeitetes Bild
        """
        # Kontrastverstärkung
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Binärisierung mit adaptivem Threshold
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return binary
    
    def deskew(self, image: np.ndarray) -> np.ndarray:
        """Korrigiert die Schräglage in einem Dokumentbild.
        
        Args:
            image: Eingabebild
            
        Returns:
            Korrigiertes Bild
        """
        # Bild in Graustufen konvertieren, falls farbig
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Nicht invertieren, wenn das Bild überwiegend weiß ist (Dokument auf weißem Hintergrund)
        if np.mean(gray) > 127:
            gray = 255 - gray
        
        # Kanten erkennen
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Linien mit Hough-Transformation finden
        lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
        
        if lines is None:
            return image  # Keine Linien gefunden, Original zurückgeben
        
        # Winkel der Linien sammeln und Median berechnen
        angles = []
        for line in lines:
            rho, theta = line[0]
            if theta < np.pi/4 or theta > 3*np.pi/4:  # Nur vertikale Linien berücksichtigen
                angles.append(theta)
        
        if not angles:
            return image  # Keine relevanten Linien, Original zurückgeben
        
        # Median-Winkel berechnen
        median_angle = np.median(angles)
        
        # Winkel korrigieren
        if median_angle < np.pi/4:
            angle = median_angle
        else:
            angle = median_angle - np.pi/2
        
        # Bild rotieren
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle * 180 / np.pi, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    def extract_document(self, image: np.ndarray) -> np.ndarray:
        """Extrahiert das Dokument aus einem Bild mit Hintergrund.
        
        Args:
            image: Eingabebild
            
        Returns:
            Extrahiertes Dokument
        """
        # Bild in Graustufen konvertieren
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Bilaterale Filterung zur Rauschunterdrückung unter Kantenerhalts
        blur = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Kanten erkennen
        edges = cv2.Canny(blur, 50, 150)
        
        # Kanten verstärken
        kernel = np.ones((5, 5), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Konturen finden
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Größte Kontur finden (vermutlich das Dokument)
        if not contours:
            return image  # Keine Konturen gefunden, Original zurückgeben
        
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Approximation der Kontur
        perimeter = cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)
        
        # Viereck prüfen (typisch für Dokumente)
        if len(approx) != 4:
            return image  # Kein Viereck gefunden, Original zurückgeben
        
        # Perspektivische Transformation
        src_pts = approx.reshape(4, 2).astype(np.float32)
        
        # Sortieren der Punkte
        rect = self._order_points(src_pts)
        
        # Zieldimensionen bestimmen
        width = int(max(
            np.linalg.norm(rect[1] - rect[0]),  # Obere Kante
            np.linalg.norm(rect[3] - rect[2])   # Untere Kante
        ))
        height = int(max(
            np.linalg.norm(rect[3] - rect[0]),  # Linke Kante
            np.linalg.norm(rect[2] - rect[1])   # Rechte Kante
        ))
        
        # Zielpunkte
        dst_pts = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype=np.float32)
        
        # Transformationsmatrix berechnen
        matrix = cv2.getPerspectiveTransform(rect, dst_pts)
        
        # Perspektivische Transformation anwenden
        warped = cv2.warpPerspective(image, matrix, (width, height))
        
        return warped
    
    def _order_points(self, pts):
        """Ordnet Punkte eines Vierecks im Uhrzeigersinn, beginnend links oben."""
        # Initialisierung des Ergebnisarrays
        rect = np.zeros((4, 2), dtype=np.float32)
        
        # Summe der Koordinaten
        s = pts.sum(axis=1)
        # Punkt mit kleinster Summe ist oben links
        rect[0] = pts[np.argmin(s)]
        # Punkt mit größter Summe ist unten rechts
        rect[2] = pts[np.argmax(s)]
        
        # Differenz der Koordinaten
        diff = np.diff(pts, axis=1)
        # Punkt mit kleinster Differenz ist oben rechts
        rect[1] = pts[np.argmin(diff)]
        # Punkt mit größter Differenz ist unten links
        rect[3] = pts[np.argmax(diff)]
        
        return rect
```

### Multi-Output-Prozessor

Der Multi-Output-Prozessor ist verantwortlich für die Transformation der Verarbeitungsergebnisse in verschiedene Ausgabeformate und deren Verteilung.

#### API für den Multi-Output-Prozessor:

```python
# api/output_service.py
from fastapi import FastAPI, Body, Depends, Query, Path
from fastapi.responses import JSONResponse, FileResponse, Response
import os
import json
from typing import Dict, Any, List, Optional

from output.multi_output_processor import MultiOutputProcessor
from common.auth import get_current_user
from common.models import OutputRequest, OutputResult

app = FastAPI(title="Output Processing API")

# Globale Instanz des Multi-Output-Prozessors
output_processor = None

@app.on_event("startup")
async def startup_event():
    """Initialisiert den Output-Prozessor beim Start der API."""
    global output_processor
    
    # Konfiguration laden
    config = {
        "output_dir": "/app/output",
        "enable_api_forwarding": True,
        "api_endpoints": [],
        "default_formats": ["text", "json"],
        "enable_thumbnails": True,
        "thumbnail_size": [200, 200]
    }
    
    # Output-Prozessor initialisieren
    output_processor = MultiOutputProcessor(config)

@app.post("/process", response_model=OutputResult)
async def process_output(
    request: OutputRequest,
    current_user: str = Depends(get_current_user)
):
    """Verarbeitet Inhalte in verschiedene Ausgabeformate."""
    try:
        content = request.content
        formats = request.formats
        options = request.options if request.options else {}
        
        # Ausgabeformate verarbeiten
        result = output_processor.process(content, formats, options)
        
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler bei der Ausgabeverarbeitung: {str(e)}"}
        )

@app.get("/download/{format_type}/{file_id}")
async def download_file(
    format_type: str = Path(..., description="Ausgabeformat"),
    file_id: str = Path(..., description="Datei-ID"),
    current_user: str = Depends(get_current_user)
):
    """Lädt eine generierte Ausgabedatei herunter."""
    try:
        # Pfad zur Datei bestimmen
        output_dir = output_processor.output_dir
        file_path = os.path.join(output_dir, f"{file_id}.{format_type}")
        
        # Prüfen, ob Datei existiert
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={"message": "Datei nicht gefunden."}
            )
        
        # MIME-Typ basierend auf Format bestimmen
        mime_types = {
            "txt": "text/plain",
            "json": "application/json",
            "pdf": "application/pdf",
            "png": "image/png",
            "jpg": "image/jpeg",
            "csv": "text/csv",
            "md": "text/markdown",
            "html": "text/html",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        
        extension = os.path.splitext(file_path)[1][1:]
        mime_type = mime_types.get(extension, "application/octet-stream")
        
        # Datei zum Download bereitstellen
        return FileResponse(
            path=file_path,
            media_type=mime_type,
            filename=os.path.basename(file_path)
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler beim Dateidownload: {str(e)}"}
        )

@app.get("/formats")
async def get_available_formats(
    current_user: str = Depends(get_current_user)
):
    """Listet alle verfügbaren Ausgabeformate auf."""
    try:
        # Verfügbare Formate aus dem Output-Prozessor abrufen
        formats = {
            "text": "Einfacher Text",
            "json": "Strukturierte JSON-Daten",
            "pdf": "PDF-Dokument",
            "image_annotated": "Annotiertes Bild",
            "thumbnail": "Vorschaubild",
            "csv": "CSV-Tabelle",
            "markdown": "Markdown-Dokument",
            "html": "HTML-Dokument",
            "docx": "Word-Dokument",
            "combined": "Kombiniertes Dokument mit allen Informationen"
        }
        
        return {
            "available_formats": formats,
            "default_formats": output_processor.default_formats
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler beim Abrufen der Formate: {str(e)}"}
        )
```

## Implementierung der Datenflüsse

### Eingabeerfassung und -verarbeitung

Die Verarbeitungspipeline beginnt mit der Erfassung der Eingabedaten aus verschiedenen Quellen und deren Vorbereitung für die weitere Verarbeitung.

#### Eingabe-Service:

```python
# services/input_service.py
import os
import mimetypes
import tempfile
import aiofiles
from fastapi import FastAPI, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional, BinaryIO
import asyncio
import httpx
import magic

from common.auth import get_current_user
from common.models import InputSource, ProcessingTask

app = FastAPI(title="Input Processing API")

# Unterstützte MIME-Typen
SUPPORTED_IMAGE_TYPES = [
    "image/jpeg", "image/png", "image/tiff", "image/gif", "image/bmp"
]
SUPPORTED_DOCUMENT_TYPES = [
    "application/pdf", "application/msword", 
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]
SUPPORTED_VIDEO_TYPES = [
    "video/mp4", "video/mpeg", "video/quicktime", "video/x-msvideo"
]

async def process_upload(file: UploadFile) -> Dict[str, Any]:
    """Verarbeitet eine hochgeladene Datei und bestimmt ihren Typ und Eigenschaften.
    
    Args:
        file: Die hochgeladene Datei
        
    Returns:
        Dictionary mit Dateiinformationen
    """
    # Temporäre Datei erstellen
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    # Datei auf Disk speichern
    async with aiofiles.open(temp_file_path, 'wb') as out_file:
        while content := await file.read(1024 * 1024):  # 1MB Chunks
            await out_file.write(content)
    
    # MIME-Typ mit magic bestimmen
    mime_type = magic.from_file(temp_file_path, mime=True)
    
    # Dateiart bestimmen
    file_type = "unknown"
    if mime_type in SUPPORTED_IMAGE_TYPES:
        file_type = "image"
    elif mime_type in SUPPORTED_DOCUMENT_TYPES:
        file_type = "document"
    elif mime_type in SUPPORTED_VIDEO_TYPES:
        file_type = "video"
    
    # Dateigröße ermitteln
    file_size = os.path.getsize(temp_file_path)
    
    # Informationen zurückgeben
    return {
        "filename": file.filename,
        "mime_type": mime_type,
        "file_type": file_type,
        "file_size": file_size,
        "temp_path": temp_file_path
    }

async def fetch_remote_file(url: str) -> Dict[str, Any]:
    """Lädt eine Datei von einer URL herunter.
    
    Args:
        url: URL der herunterzuladenden Datei
        
    Returns:
        Dictionary mit Dateiinformationen
    """
    # Temporäre Datei erstellen
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, "remote_file")
    
    # Datei herunterladen
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', url) as response:
            response.raise_for_status()
            
            # Content-Disposition-Header für Dateiname prüfen
            filename = url.split('/')[-1]
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[-1].strip('"\'')
            
            # Zieldatei mit korrektem Namen
            temp_file_path = os.path.join(temp_dir, filename)
            
            # In Datei speichern
            async with aiofiles.open(temp_file_path, 'wb') as out_file:
                async for chunk in response.aiter_bytes(chunk_size=1024 * 1024):  # 1MB Chunks
                    await out_file.write(chunk)
    
    # MIME-Typ mit magic bestimmen
    mime_type = magic.from_file(temp_file_path, mime=True)
    
    # Dateiart bestimmen
    file_type = "unknown"
    if mime_type in SUPPORTED_IMAGE_TYPES:
        file_type = "image"
    elif mime_type in SUPPORTED_DOCUMENT_TYPES:
        file_type = "document"
    elif mime_type in SUPPORTED_VIDEO_TYPES:
        file_type = "video"
    
    # Dateigröße ermitteln
    file_size = os.path.getsize(temp_file_path)
    
    # Informationen zurückgeben
    return {
        "filename": filename,
        "mime_type": mime_type,
        "file_type": file_type,
        "file_size": file_size,
        "temp_path": temp_file_path
    }

@app.post("/upload")
async def upload_file(
    file: UploadFile,
    processing_type: str = Form(None),
    options: str = Form("{}"),
    current_user: str = Depends(get_current_user)
):
    """Nimmt eine hochgeladene Datei entgegen und startet die Verarbeitung."""
    try:
        # Datei verarbeiten
        file_info = await process_upload(file)
        
        # Optionen parsen
        try:
            options_dict = json.loads(options)
        except json.JSONDecodeError:
            options_dict = {}
        
        # Verarbeitungstyp bestimmen, falls nicht angegeben
        if not processing_type:
            if file_info["file_type"] == "image":
                processing_type = "ocr_and_vision"
            elif file_info["file_type"] == "document":
                processing_type = "ocr"
            elif file_info["file_type"] == "video":
                processing_type = "video_analysis"
            else:
                processing_type = "unknown"
        
        # Verarbeitungsaufgabe erstellen
        task = await create_processing_task(
            source_type="upload",
            source_info=file_info,
            processing_type=processing_type,
            options=options_dict,
            user_id=current_user
        )
        
        return task
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler bei der Dateiverarbeitung: {str(e)}"}
        )

@app.post("/remote")
async def process_remote_file(
    source: InputSource,
    current_user: str = Depends(get_current_user)
):
    """Verarbeitet eine Datei von einer Remote-Quelle."""
    try:
        # Remote-Quelle verarbeiten
        if source.type == "url":
            file_info = await fetch_remote_file(source.url)
        else:
            return JSONResponse(
                status_code=400,
                content={"message": f"Nicht unterstützter Quelltyp: {source.type}"}
            )
        
        # Verarbeitungstyp bestimmen
        processing_type = source.processing_type or "auto"
        if processing_type == "auto":
            if file_info["file_type"] == "image":
                processing_type = "ocr_and_vision"
            elif file_info["file_type"] == "document":
                processing_type = "ocr"
            elif file_info["file_type"] == "video":
                processing_type = "video_analysis"
            else:
                processing_type = "unknown"
        
        # Verarbeitungsaufgabe erstellen
        task = await create_processing_task(
            source_type="remote",
            source_info=file_info,
            processing_type=processing_type,
            options=source.options or {},
            user_id=current_user
        )
        
        return task
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler bei der Remote-Dateiverarbeitung: {str(e)}"}
        )

@app.post("/camera")
async def process_camera_stream(
    source: InputSource,
    current_user: str = Depends(get_current_user)
):
    """Verarbeitet einen Live-Kamerastream."""
    try:
        # Stream-Quelle validieren
        if not source.url and not source.device_id:
            return JSONResponse(
                status_code=400,
                content={"message": "URL oder Geräte-ID für Kamerastream erforderlich."}
            )
        
        # Stream-Quelle formatieren
        stream_source = source.url or source.device_id
        
        # Verarbeitungsaufgabe erstellen
        task = await create_processing_task(
            source_type="camera",
            source_info={
                "stream_source": stream_source,
                "is_url": bool(source.url)
            },
            processing_type=source.processing_type or "video_analysis",
            options=source.options or {},
            user_id=current_user
        )
        
        return task
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Fehler bei der Kamerastream-Verarbeitung: {str(e)}"}
        )

async def create_processing_task(
    source_type: str,
    source_info: Dict[str, Any],
    processing_type: str,
    options: Dict[str, Any],
    user_id: str
) -> ProcessingTask:
    """Erstellt eine Verarbeitungsaufgabe und sendet sie an die Task-Queue.
    
    Args:
        source_type: Art der Quelle (upload, remote, camera)
        source_info: Informationen zur Quelle
        processing_type: Art der Verarbeitung
        options: Verarbeitungsoptionen
        user_id: ID des Benutzers
        
    Returns:
        Erstellte Verarbeitungsaufgabe
    """
    # Task-ID generieren
    task_id = f"{processing_type}_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    
    # Task erstellen
    task = {
        "task_id": task_id,
        "user_id": user_id,
        "source_type": source_type,
        "source_info": source_info,
        "processing_type": processing_type,
        "options": options,
        "status": "queued",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Task an die Queue senden (Implementierung abhängig vom Messaging-System)
    # Beispiel mit Redis als Queue:
    # await redis.rpush("processing_tasks", json.dumps(task))
    
    # Task in der Datenbank speichern (für Statusverfolgung)
    # Beispiel mit einer Datenbank-Integration:
    # await db.tasks.insert_one(task)
    
    # Verarbeitungsaufgabe zurückgeben
    return task
```

### Verarbeitungspipeline

Die Verarbeitungspipeline koordiniert die verschiedenen Schritte der Datenverarbeitung und stellt sicher, dass die Ergebnisse korrekt generiert und weitergeleitet werden.

#### Verarbeitungskoordinator:

```python
# services/processing_coordinator.py
import asyncio
import json
import time
import logging
from typing import Dict, Any, List, Optional, Callable
import aioredis
import os

from vision.computer_vision_module import ComputerVisionModule
from ocr.neural_ocr_engine import NeuralOCREngine
from output.multi_output_processor import MultiOutputProcessor

class ProcessingCoordinator:
    """Koordiniert die Verarbeitungspipeline für verschiedene Eingabetypen."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert den Verarbeitungskoordinator mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        self.logger = logging.getLogger("processing_coordinator")
        
        # Komponenten initialisieren
        self.vision_module = ComputerVisionModule(config.get("vision", {}))
        self.ocr_engine = NeuralOCREngine(config.get("ocr", {}))
        self.output_processor = MultiOutputProcessor(config.get("output", {}))
        
        # Redis-Verbindung für Task-Queue
        self.redis = None
        
        # Mapping von Verarbeitungstypen zu Funktionen
        self.processors = {
            "ocr": self.process_ocr,
            "vision": self.process_vision,
            "ocr_and_vision": self.process_ocr_and_vision,
            "video_analysis": self.process_video,
            "camera_stream": self.process_camera
        }
    
    async def start(self):
        """Startet den Verarbeitungskoordinator und verbindet zur Task-Queue."""
        # Redis-Verbindung herstellen
        redis_url = self.config.get("redis_url", "redis://localhost:6379/0")
        self.redis = await aioredis.create_redis_pool(redis_url)
        
        # Worker-Prozesse starten
        worker_count = self.config.get("worker_count", 4)
        self.logger.info(f"Starte {worker_count} Worker-Prozesse.")
        
        # Worker-Tasks erstellen
        self.workers = [
            asyncio.create_task(self.worker_loop(i))
            for i in range(worker_count)
        ]
    
    async def stop(self):
        """Stoppt den Verarbeitungskoordinator und gibt Ressourcen frei."""
        # Worker-Tasks abbrechen
        for worker in self.workers:
            worker.cancel()
        
        # Auf Beendigung warten
        await asyncio.gather(*self.workers, return_exceptions=True)
        
        # Redis-Verbindung schließen
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()
        
        self.logger.info("Verarbeitungskoordinator gestoppt.")
    
    async def worker_loop(self, worker_id: int):
        """Hauptschleife für Worker-Prozesse.
        
        Args:
            worker_id: ID des Worker-Prozesses
        """
        self.logger.info(f"Worker {worker_id} gestartet.")
        
        while True:
            try:
                # Task aus der Queue holen
                task_json = await self.redis.blpop("processing_tasks", timeout=0)
                task = json.loads(task_json[1])
                
                # Task-Status aktualisieren
                task["status"] = "processing"
                task["updated_at"] = time.time()
                await self.update_task_status(task)
                
                # Passenden Prozessor für den Task finden
                processing_type = task.get("processing_type")
                if processing_type in self.processors:
                    processor = self.processors[processing_type]
                    
                    # Task verarbeiten
                    try:
                        self.logger.info(f"Worker {worker_id} verarbeitet Task {task['task_id']} vom Typ {processing_type}.")
                        result = await processor(task)
                        
                        # Erfolgreiche Verarbeitung
                        task["status"] = "completed"
                        task["result"] = result
                        task["progress"] = 100
                    except Exception as e:
                        # Fehler bei der Verarbeitung
                        self.logger.error(f"Fehler bei der Verarbeitung von Task {task['task_id']}: {str(e)}")
                        task["status"] = "failed"
                        task["error"] = str(e)
                else:
                    # Unbekannter Verarbeitungstyp
                    self.logger.warning(f"Unbekannter Verarbeitungstyp: {processing_type}")
                    task["status"] = "failed"
                    task["error"] = f"Unbekannter Verarbeitungstyp: {processing_type}"
                
                # Task-Status aktualisieren
                task["updated_at"] = time.time()
                await self.update_task_status(task)
            
            except asyncio.CancelledError:
                # Worker wird beendet
                break
            except Exception as e:
                # Allgemeiner Fehler im Worker
                self.logger.error(f"Fehler im Worker {worker_id}: {str(e)}")
                await asyncio.sleep(1)  # Kurze Pause bei Fehlern
    
    async def update_task_status(self, task: Dict[str, Any]):
        """Aktualisiert den Status eines Tasks in der Datenbank und informiert Clients.
        
        Args:
            task: Task-Informationen
        """
        # Task in Redis speichern (für schnellen Zugriff)
        await self.redis.set(f"task:{task['task_id']}", json.dumps(task))
        
        # Bei Bedarf auch in einer persistenten Datenbank speichern
        # Beispielimplementierung würde hier eine Datenbankoperation durchführen
        
        # Event-Benachrichtigung für Echtzeit-Updates
        await self.redis.publish("task_updates", json.dumps({
            "task_id": task["task_id"],
            "status": task["status"],
            "progress": task["progress"]
        }))
    
    async def process_ocr(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet einen OCR-Task.
        
        Args:
            task: Task-Informationen
            
        Returns:
            Verarbeitungsergebnisse
        """
        # Quell-Informationen extrahieren
        source_info = task["source_info"]
        file_path = source_info["temp_path"]
        options = task["options"]
        
        # Prüfen, ob die Datei existiert
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        # Status aktualisieren
        task["progress"] = 10
        await self.update_task_status(task)
        
        # Dateiformat bestimmen und passend verarbeiten
        file_type = source_info["file_type"]
        
        if file_type == "document" and source_info["mime_type"] == "application/pdf":
            # PDF-Dokument verarbeiten
            # OCR auf PDF-Seiten durchführen
            results = await self.process_pdf_ocr(file_path, options)
        else:
            # Einfaches Bild verarbeiten
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Bild konnte nicht gelesen werden: {file_path}")
            
            # OCR durchführen
            result = self.ocr_engine.recognize_text(image, options)
            results = {"pages": [result]}
        
        # Status aktualisieren
        task["progress"] = 50
        await self.update_task_status(task)
        
        # Ausgabeformate bestimmen
        formats = options.get("output_formats", ["text", "json"])
        
        # Für jede Seite Ausgaben generieren
        output_results = []
        for i, page_result in enumerate(results["pages"]):
            # Multi-Output-Prozessor verwenden
            content = {
                "doc_id": f"{task['task_id']}_page{i+1}",
                "text": page_result["text"],
                "text_blocks": page_result.get("text_blocks", []),
                "metadata": {
                    "page": i+1,
                    "total_pages": len(results["pages"]),
                    "confidence": page_result.get("overall_confidence", 0.0)
                },
                "images": {
                    "original": source_info["temp_path"] if i == 0 else None
                }
            }
            
            # Ausgaben generieren
            output_result = self.output_processor.process(content, formats, options.get("output_options", {}))
            output_results.append(output_result)
        
        # Status aktualisieren
        task["progress"] = 90
        await self.update_task_status(task)
        
        # Gesamtergebnis zusammenstellen
        result = {
            "task_id": task["task_id"],
            "ocr_results": results,
            "output_results": output_results
        }
        
        # Temporäre Datei aufräumen, wenn gewünscht
        if options.get("cleanup_temp_files", True):
            try:
                os.remove(file_path)
            except:
                pass
        
        return result
    
    async def process_pdf_ocr(self, pdf_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Führt OCR auf einem PDF-Dokument durch.
        
        Args:
            pdf_path: Pfad zur PDF-Datei
            options: Verarbeitungsoptionen
            
        Returns:
            OCR-Ergebnisse für alle Seiten
        """
        # PDF-Seiten extrahieren
        # Hier würde eine ausführliche Implementierung PDF-Seiten in Bilder konvertieren
        # und OCR auf jeder Seite durchführen
        
        # Vereinfachte Implementierung als Platzhalter
        return {"pages": []}
    
    async def process_vision(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet einen Vision-Task (Objekterkennung).
        
        Args:
            task: Task-Informationen
            
        Returns:
            Verarbeitungsergebnisse
        """
        # Quell-Informationen extrahieren
        source_info = task["source_info"]
        file_path = source_info["temp_path"]
        options = task["options"]
        
        # Prüfen, ob die Datei existiert
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        # Status aktualisieren
        task["progress"] = 10
        await self.update_task_status(task)
        
        # Bild laden
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Bild konnte nicht gelesen werden: {file_path}")
        
        # Objekterkennung durchführen
        detections = self.vision_module.detect_objects(image)
        
        # Status aktualisieren
        task["progress"] = 50
        await self.update_task_status(task)
        
        # Annotiertes Bild erstellen
        annotated_image = self.vision_module.annotate_image(
            image, detections, 
            show_labels=options.get("show_labels", True)
        )
        
        # Ausgabeformate bestimmen
        formats = options.get("output_formats", ["json", "image_annotated"])
        
        # Multi-Output-Prozessor verwenden
        content = {
            "doc_id": task["task_id"],
            "detections": detections,
            "metadata": {
                "filename": source_info["filename"],
                "mime_type": source_info["mime_type"],
                "file_size": source_info["file_size"]
            },
            "images": {
                "original": image,
                "annotated": annotated_image
            }
        }
        
        # Ausgaben generieren
        output_result = self.output_processor.process(content, formats, options.get("output_options", {}))
        
        # Status aktualisieren
        task["progress"] = 90
        await self.update_task_status(task)
        
        # Gesamtergebnis zusammenstellen
        result = {
            "task_id": task["task_id"],
            "vision_results": {
                "detections": detections
            },
            "output_result": output_result
        }
        
        # Temporäre Datei aufräumen, wenn gewünscht
        if options.get("cleanup_temp_files", True):
            try:
                os.remove(file_path)
            except:
                pass
        
        return result
    
    async def process_ocr_and_vision(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet einen kombinierten OCR- und Vision-Task.
        
        Args:
            task: Task-Informationen
            
        Returns:
            Verarbeitungsergebnisse
        """
        # Quell-Informationen extrahieren
        source_info = task["source_info"]
        file_path = source_info["temp_path"]
        options = task["options"]
        
        # Prüfen, ob die Datei existiert
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        # Status aktualisieren
        task["progress"] = 10
        await self.update_task_status(task)
        
        # Bild laden
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Bild konnte nicht gelesen werden: {file_path}")
        
        # Objekterkennung durchführen
        detections = self.vision_module.detect_objects(image)
        
        # Status aktualisieren
        task["progress"] = 30
        await self.update_task_status(task)
        
        # OCR durchführen
        ocr_result = self.ocr_engine.recognize_text(image, options)
        
        # Status aktualisieren
        task["progress"] = 50
        await self.update_task_status(task)
        
        # Annotiertes Bild mit Objekten und Text erstellen
        annotated_image = self.vision_module.annotate_image(
            image, detections, 
            show_labels=options.get("show_labels", True)
        )
        
        # Text-Regionen hinzufügen, falls vorhanden
        if "text_blocks" in ocr_result:
            # Hier würde eine Implementierung Text-Regionen zum annotierten Bild hinzufügen
            pass
        
        # Ausgabeformate bestimmen
        formats = options.get("output_formats", ["json", "text", "image_annotated", "combined"])
        
        # Multi-Output-Prozessor verwenden
        content = {
            "doc_id": task["task_id"],
            "text": ocr_result["text"],
            "text_blocks": ocr_result.get("text_blocks", []),
            "detections": detections,
            "metadata": {
                "filename": source_info["filename"],
                "mime_type": source_info["mime_type"],
                "file_size": source_info["file_size"],
                "ocr_confidence": ocr_result.get("overall_confidence", 0.0)
            },
            "images": {
                "original": image,
                "annotated": annotated_image
            }
        }
        
        # Ausgaben generieren
        output_result = self.output_processor.process(content, formats, options.get("output_options", {}))
        
        # Status aktualisieren
        task["progress"] = 90
        await self.update_task_status(task)
        
        # Gesamtergebnis zusammenstellen
        result = {
            "task_id": task["task_id"],
            "vision_results": {
                "detections": detections
            },
            "ocr_results": ocr_result,
            "output_result": output_result
        }
        
        ```python
            # Temporäre Datei aufräumen, wenn gewünscht
            if options.get("cleanup_temp_files", True):
                try:
                    os.remove(file_path)
                except:
                    pass
            
            return result
    
    async def process_video(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet ein Video mit Objekterkennung und -tracking.
        
        Args:
            task: Task-Informationen
            
        Returns:
            Verarbeitungsergebnisse
        """
        # Quell-Informationen extrahieren
        source_info = task["source_info"]
        file_path = source_info["temp_path"]
        options = task["options"]
        
        # Prüfen, ob die Datei existiert
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        # Status aktualisieren
        task["progress"] = 10
        await self.update_task_status(task)
        
        # Video öffnen
        video = cv2.VideoCapture(file_path)
        if not video.isOpened():
            raise ValueError(f"Video konnte nicht geöffnet werden: {file_path}")
        
        # Video-Eigenschaften auslesen
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Tracking-Parameter
        detection_interval = options.get("detection_interval", 30)  # Frames zwischen Detektionen
        track_classes = options.get("track_classes", None)
        min_confidence = options.get("min_confidence", 0.5)
        
        # Output-Video konfigurieren, falls gewünscht
        output_video = None
        output_path = None
        if options.get("create_output_video", True):
            output_path = os.path.join(
                self.output_processor.output_dir,
                f"{task['task_id']}_output.mp4"
            )
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Ergebnisse sammeln
        tracking_results = []
        frame_results = []
        current_frame = 0
        
        # Video frame für frame verarbeiten
        while True:
            ret, frame = video.read()
            if not ret:
                break
            
            # Fortschritt berechnen und aktualisieren
            progress = min(90, 10 + int(80 * current_frame / max(1, frame_count)))
            if current_frame % 10 == 0:  # Nur alle 10 Frames aktualisieren
                task["progress"] = progress
                await self.update_task_status(task)
            
            # Objekterkennung und Tracking
            if current_frame % detection_interval == 0:
                # Neue Erkennung und Tracking durchführen
                frame_tracking = self.vision_module.detect_and_track(
                    frame, track_classes=track_classes, min_confidence=min_confidence
                )
            else:
                # Bestehendes Tracking aktualisieren
                frame_tracking = {"tracking_updated": []}
                for object_id in list(self.vision_module.active_trackers.keys()):
                    tracking_result = self.vision_module.update_tracking(frame, object_id)
                    if tracking_result and tracking_result[0]:
                        success, bbox = tracking_result
                        frame_tracking["tracking_updated"].append({
                            "object_id": object_id,
                            "bbox": {
                                "x": int(bbox[0]),
                                "y": int(bbox[1]),
                                "width": int(bbox[2]),
                                "height": int(bbox[3])
                            }
                        })
            
            # Frame mit Tracking visualisieren
            annotated_frame = self.vision_module.annotate_tracked_objects(
                frame, frame_tracking, show_trajectories=True
            )
            
            # Frame-Ergebnisse speichern
            frame_result = {
                "frame_number": current_frame,
                "timestamp": current_frame / fps,
                "tracking": frame_tracking
            }
            frame_results.append(frame_result)
            
            # In Output-Video schreiben, falls konfiguriert
            if output_video:
                output_video.write(annotated_frame)
            
            # Tracking-Ergebnisse für diesen Frame zur Gesamtliste hinzufügen
            if "tracking_started" in frame_tracking and frame_tracking["tracking_started"]:
                for tracked_obj in frame_tracking["tracking_started"]:
                    tracking_results.append({
                        "frame_start": current_frame,
                        "timestamp_start": current_frame / fps,
                        "object_id": tracked_obj["object_id"],
                        "class_name": tracked_obj.get("class_name", "unknown"),
                        "confidence": tracked_obj.get("confidence", 0.0),
                        "initial_position": tracked_obj.get("initial_bbox", {})
                    })
            
            # Frame-Zähler erhöhen
            current_frame += 1
        
        # Ressourcen freigeben
        video.release()
        if output_video:
            output_video.release()
        
        # Status aktualisieren
        task["progress"] = 95
        await self.update_task_status(task)
        
        # Ausgabeformate bestimmen
        formats = options.get("output_formats", ["json"])
        
        # Multi-Output-Prozessor verwenden
        content = {
            "doc_id": task["task_id"],
            "metadata": {
                "filename": source_info["filename"],
                "mime_type": source_info["mime_type"],
                "file_size": source_info["file_size"],
                "frame_count": frame_count,
                "fps": fps,
                "width": width,
                "height": height,
                "duration": frame_count / fps
            },
            "tracking_results": tracking_results,
            "video_info": {
                "output_video": output_path
            }
        }
        
        # Ausgaben generieren
        output_result = self.output_processor.process(content, formats, options.get("output_options", {}))
        
        # Gesamtergebnis zusammenstellen
        result = {
            "task_id": task["task_id"],
            "video_analysis": {
                "frame_count": frame_count,
                "tracked_objects": len(tracking_results),
                "output_video": output_path
            },
            "output_result": output_result
        }
        
        # Temporäre Datei aufräumen, wenn gewünscht
        if options.get("cleanup_temp_files", True):
            try:
                os.remove(file_path)
            except:
                pass
        
        return result
    
    async def process_camera(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet einen Kamerastream in Echtzeit.
        
        Args:
            task: Task-Informationen
            
        Returns:
            Verarbeitungsergebnisse
        """
        # Quell-Informationen extrahieren
        source_info = task["source_info"]
        stream_source = source_info["stream_source"]
        options = task["options"]
        
        # Parameter für Kameraverarbeitung
        processing_duration = options.get("duration", 60)  # Standardmäßig 60 Sekunden
        enable_object_detection = options.get("object_detection", True)
        enable_tracking = options.get("tracking", True)
        enable_ocr = options.get("ocr", False)
        audio_feedback = options.get("audio_feedback", False)
        
        # Status aktualisieren
        task["progress"] = 10
        await self.update_task_status(task)
        
        # Kamera öffnen
        camera = cv2.VideoCapture(stream_source)
        if not camera.isOpened():
            raise ValueError(f"Kamera konnte nicht geöffnet werden: {stream_source}")
        
        # Video-Eigenschaften auslesen
        fps = camera.get(cv2.CAP_PROP_FPS) or 30
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Ausgabeverzeichnis erstellen
        output_dir = os.path.join(
            self.output_processor.output_dir,
            f"camera_{task['task_id']}"
        )
        os.makedirs(output_dir, exist_ok=True)
        
        # Output-Video konfigurieren, falls gewünscht
        output_video = None
        output_path = None
        if options.get("record_video", True):
            output_path = os.path.join(output_dir, f"recording.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Sprachrückmeldung initialisieren, falls aktiviert
        voice_processor = None
        if audio_feedback:
            # Hier würde eine Implementierung die KI-Integration für Sprachausgabe initialisieren
            pass
        
        # Verarbeitungsergebnisse
        detections_history = []
        ocr_results = []
        frames_processed = 0
        start_time = time.time()
        end_time = start_time + processing_duration
        
        # Hauptschleife für Kameraverarbeitung
        while time.time() < end_time:
            ret, frame = camera.read()
            if not ret:
                # Fehler beim Lesen des Frames
                await asyncio.sleep(0.1)
                continue
            
            # Fortschritt berechnen und aktualisieren
            elapsed = time.time() - start_time
            progress = min(90, 10 + int(80 * elapsed / processing_duration))
            if frames_processed % 10 == 0:  # Nur alle 10 Frames aktualisieren
                task["progress"] = progress
                await self.update_task_status(task)
            
            frame_result = {
                "frame_number": frames_processed,
                "timestamp": elapsed
            }
            
            # Objekterkennung und Tracking
            if enable_object_detection:
                if enable_tracking:
                    # Objekte erkennen und tracken
                    tracking_result = self.vision_module.detect_and_track(
                        frame, track_classes=options.get("track_classes"),
                        min_confidence=options.get("min_confidence", 0.5)
                    )
                    frame_result["tracking"] = tracking_result
                    
                    # Frame mit Tracking visualisieren
                    annotated_frame = self.vision_module.annotate_tracked_objects(
                        frame, tracking_result, show_trajectories=True
                    )
                else:
                    # Nur Objekte erkennen
                    detections = self.vision_module.detect_objects(frame)
                    frame_result["detections"] = detections
                    
                    # Frame mit Detektionen visualisieren
                    annotated_frame = self.vision_module.annotate_image(
                        frame, detections, show_labels=True
                    )
                
                # Detektionen zur Historie hinzufügen
                if "detections" in frame_result:
                    detections_history.append(frame_result["detections"])
                elif "tracking" in frame_result and "tracking_started" in frame_result["tracking"]:
                    for obj in frame_result["tracking"]["tracking_started"]:
                        detections_history.append(obj)
            else:
                # Keine Objekterkennung, unverändertes Frame verwenden
                annotated_frame = frame
            
            # OCR durchführen, falls aktiviert
            if enable_ocr and frames_processed % 30 == 0:  # Nur jedes 30. Frame
                try:
                    ocr_result = self.ocr_engine.recognize_text(frame)
                    if ocr_result and ocr_result.get("text"):
                        frame_result["ocr"] = ocr_result
                        ocr_results.append({
                            "frame": frames_processed,
                            "timestamp": elapsed,
                            "text": ocr_result["text"]
                        })
                except Exception as e:
                    self.logger.error(f"Fehler bei OCR für Frame {frames_processed}: {str(e)}")
            
            # Sprachrückmeldung generieren, falls aktiviert
            if audio_feedback and voice_processor and "detections" in frame_result:
                # Hier würde eine Implementierung Sprachrückmeldungen zu erkannten Objekten generieren
                pass
            
            # In Output-Video schreiben, falls konfiguriert
            if output_video:
                output_video.write(annotated_frame)
            
            # Frame-Zähler erhöhen
            frames_processed += 1
            
            # Kurze Pause, um CPU-Überlastung zu vermeiden
            await asyncio.sleep(0.01)
        
        # Ressourcen freigeben
        camera.release()
        if output_video:
            output_video.release()
        
        # Status aktualisieren
        task["progress"] = 95
        await self.update_task_status(task)
        
        # Ausgabeformate bestimmen
        formats = options.get("output_formats", ["json"])
        
        # Multi-Output-Prozessor verwenden
        content = {
            "doc_id": task["task_id"],
            "metadata": {
                "stream_source": stream_source,
                "processing_duration": processing_duration,
                "frames_processed": frames_processed,
                "width": width,
                "height": height
            },
            "detections_summary": {
                "total_detections": len(detections_history),
                "detections": detections_history[:100]  # Begrenzen auf max. 100 Einträge
            },
            "ocr_summary": {
                "total_ocr_results": len(ocr_results),
                "ocr_results": ocr_results
            },
            "video_info": {
                "output_video": output_path
            }
        }
        
        # Ausgaben generieren
        output_result = self.output_processor.process(content, formats, options.get("output_options", {}))
        
        # Gesamtergebnis zusammenstellen
        result = {
            "task_id": task["task_id"],
            "camera_analysis": {
                "duration": processing_duration,
                "frames_processed": frames_processed,
                "detections_count": len(detections_history),
                "ocr_results_count": len(ocr_results),
                "output_video": output_path
            },
            "output_result": output_result
        }
        
        return result
```

### Ausgabegenerierung und -verteilung

Die Ausgabegenerierung und -verteilung ist verantwortlich für die Transformation der Verarbeitungsergebnisse in verschiedene Formate und die Bereitstellung dieser Formate für unterschiedliche Anwendungsfälle.

#### Erweiterter Output-Manager:

```python
# services/output_manager.py
import os
import json
import base64
import requests
import logging
from typing import Dict, Any, List, Optional
import asyncio
import aiofiles
import aiohttp

from output.multi_output_processor import MultiOutputProcessor

class OutputManager:
    """Verwaltet die Generierung und Verteilung von Ausgaben aus Verarbeitungsergebnissen."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert den Output-Manager mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        self.logger = logging.getLogger("output_manager")
        
        # Multi-Output-Prozessor initialisieren
        self.output_processor = MultiOutputProcessor(config.get("output", {}))
        
        # Zielkonfigurationen für Verteilung
        self.distribution_targets = config.get("distribution_targets", [])
    
    async def process_and_distribute(self, content: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Inhalte, erstellt Ausgaben und verteilt sie an konfigurierte Ziele.
        
        Args:
            content: Zu verarbeitender Inhalt
            options: Verarbeitungsoptionen
            
        Returns:
            Verarbeitungs- und Verteilungsergebnisse
        """
        # Ausgabeformate bestimmen
        formats = options.get("formats", self.output_processor.default_formats)
        
        # Output-Prozessor verwenden, um Ausgaben zu generieren
        processing_result = self.output_processor.process(content, formats, options)
        
        # Ausgaben verteilen, falls gewünscht
        distribution_results = {}
        if options.get("distribute", False):
            distribution_results = await self.distribute_outputs(
                processing_result, options.get("distribution_options", {})
            )
        
        # Gesamtergebnis zusammenstellen
        result = {
            "processing_result": processing_result,
            "distribution_results": distribution_results
        }
        
        return result
    
    async def distribute_outputs(self, processing_result: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Verteilt generierte Ausgaben an konfigurierte Ziele.
        
        Args:
            processing_result: Ergebnis der Ausgabeverarbeitung
            options: Verteilungsoptionen
            
        Returns:
            Ergebnisse der Verteilung
        """
        # Zu verteilende Ausgaben
        outputs = processing_result.get("outputs", {})
        
        # Ziele bestimmen
        targets = options.get("targets", self.distribution_targets)
        
        # Verteilungsaufgaben erstellen und ausführen
        distribution_tasks = []
        for target in targets:
            # Zielspezifische Formate
            target_formats = target.get("formats", list(outputs.keys()))
            
            # Nur vorhandene Formate berücksichtigen
            available_formats = [fmt for fmt in target_formats if fmt in outputs]
            
            if not available_formats:
                continue
            
            # Verteilungsaufgabe erstellen basierend auf Zieltyp
            target_type = target.get("type", "file")
            if target_type == "api":
                task = self._distribute_to_api(target, outputs, available_formats)
            elif target_type == "email":
                task = self._distribute_to_email(target, outputs, available_formats)
            elif target_type == "sftp":
                task = self._distribute_to_sftp(target, outputs, available_formats)
            elif target_type == "s3":
                task = self._distribute_to_s3(target, outputs, available_formats)
            elif target_type == "webhook":
                task = self._distribute_to_webhook(target, outputs, available_formats)
            else:  # Standardmäßig Dateiexport
                task = self._distribute_to_file(target, outputs, available_formats)
            
            distribution_tasks.append(task)
        
        # Alle Verteilungsaufgaben ausführen
        if distribution_tasks:
            results = await asyncio.gather(*distribution_tasks, return_exceptions=True)
            
            # Ergebnisse verarbeiten
            distribution_results = {}
            for i, result in enumerate(results):
                target_name = targets[i].get("name", f"target_{i}")
                
                if isinstance(result, Exception):
                    distribution_results[target_name] = {
                        "success": False,
                        "error": str(result)
                    }
                else:
                    distribution_results[target_name] = {
                        "success": True,
                        "result": result
                    }
            
            return distribution_results
        else:
            return {}
    
    async def _distribute_to_api(self, target: Dict[str, Any], outputs: Dict[str, Any], formats: List[str]) -> Dict[str, Any]:
        """Verteilt Ausgaben an einen API-Endpunkt.
        
        Args:
            target: Zielkonfiguration
            outputs: Generierte Ausgaben
            formats: Zu verteilende Formate
            
        Returns:
            API-Antwort
        """
        # API-Konfiguration extrahieren
        api_url = target.get("url")
        if not api_url:
            raise ValueError("API-URL ist erforderlich für API-Verteilung")
        
        headers = target.get("headers", {})
        if not "Content-Type" in headers:
            headers["Content-Type"] = "application/json"
        
        # Auth-Informationen
        auth = None
        if "auth" in target:
            auth_config = target["auth"]
            auth_type = auth_config.get("type", "basic")
            
            if auth_type == "basic":
                auth = aiohttp.BasicAuth(
                    login=auth_config.get("username", ""),
                    password=auth_config.get("password", "")
                )
            elif auth_type == "bearer":
                headers["Authorization"] = f"Bearer {auth_config.get('token', '')}"
        
        # Daten vorbereiten
        payload = {
            "outputs": {}
        }
        
        # Ausgaben hinzufügen
        for fmt in formats:
            output_info = outputs[fmt]
            
            # Dateien als Base64 kodieren oder Pfade senden
            if "path" in output_info and os.path.exists(output_info["path"]):
                if target.get("include_files", False):
                    # Datei einbetten
                    async with aiofiles.open(output_info["path"], "rb") as f:
                        file_content = await f.read()
                        payload["outputs"][fmt] = {
                            "content": base64.b64encode(file_content).decode("utf-8"),
                            "filename": os.path.basename(output_info["path"]),
                            "content_type": self._get_content_type(output_info["path"])
                        }
                else:
                    # Nur Pfad senden
                    payload["outputs"][fmt] = {
                        "path": output_info["path"]
                    }
            else:
                # Andere Informationen direkt senden
                payload["outputs"][fmt] = output_info
        
        # Metadaten hinzufügen
        payload["metadata"] = target.get("metadata", {})
        
        # API-Aufruf durchführen
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers, auth=auth) as response:
                response.raise_for_status()
                return await response.json()
    
    async def _distribute_to_email(self, target: Dict[str, Any], outputs: Dict[str, Any], formats: List[str]) -> Dict[str, Any]:
        """Verteilt Ausgaben per E-Mail.
        
        Args:
            target: Zielkonfiguration
            outputs: Generierte Ausgaben
            formats: Zu verteilende Formate
            
        Returns:
            Ergebnis des E-Mail-Versands
        """
        # E-Mail-Konfiguration
        recipient = target.get("recipient")
        if not recipient:
            raise ValueError("Empfänger ist erforderlich für E-Mail-Verteilung")
        
        subject = target.get("subject", "Verarbeitungsergebnisse")
        body = target.get("body", "Anbei die Verarbeitungsergebnisse.")
        
        # SMTP-Konfiguration aus Umgebung oder Konfiguration
        smtp_config = target.get("smtp_config", {})
        smtp_server = smtp_config.get("server", os.environ.get("SMTP_SERVER"))
        smtp_port = smtp_config.get("port", int(os.environ.get("SMTP_PORT", 587)))
        smtp_user = smtp_config.get("username", os.environ.get("SMTP_USER"))
        smtp_password = smtp_config.get("password", os.environ.get("SMTP_PASSWORD"))
        sender = smtp_config.get("sender", os.environ.get("SMTP_SENDER"))
        
        if not all([smtp_server, smtp_port, smtp_user, smtp_password, sender]):
            raise ValueError("Unvollständige SMTP-Konfiguration")
        
        # E-Mail-Paket importieren
        import aiosmtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        
        # E-Mail erstellen
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        
        # Text-Body hinzufügen
        message.attach(MIMEText(body, "plain"))
        
        # Anhänge hinzufügen
        for fmt in formats:
            output_info = outputs[fmt]
            if "path" in output_info and os.path.exists(output_info["path"]):
                filename = os.path.basename(output_info["path"])
                async with aiofiles.open(output_info["path"], "rb") as f:
                    attachment_data = await f.read()
                
                attachment = MIMEApplication(attachment_data)
                attachment.add_header("Content-Disposition", f"attachment; filename={filename}")
                message.attach(attachment)
        
        # E-Mail senden
        try:
            smtp = aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port, use_tls=True)
            await smtp.connect()
            await smtp.login(smtp_user, smtp_password)
            await smtp.send_message(message)
            await smtp.quit()
            
            return {
                "status": "sent",
                "recipient": recipient,
                "attachments": len(formats)
            }
        except Exception as e:
            raise ValueError(f"Fehler beim Senden der E-Mail: {str(e)}")
    
    async def _distribute_to_sftp(self, target: Dict[str, Any], outputs: Dict[str, Any], formats: List[str]) -> Dict[str, Any]:
        """Verteilt Ausgaben per SFTP.
        
        Args:
            target: Zielkonfiguration
            outputs: Generierte Ausgaben
            formats: Zu verteilende Formate
            
        Returns:
            Ergebnis des SFTP-Uploads
        """
        # SFTP-Konfiguration
        host = target.get("host")
        if not host:
            raise ValueError("Host ist erforderlich für SFTP-Verteilung")
        
        port = target.get("port", 22)
        username = target.get("username")
        password = target.get("password")
        key_path = target.get("key_path")
        remote_dir = target.get("remote_dir", ".")
        
        if not username:
            raise ValueError("Benutzername ist erforderlich für SFTP-Verteilung")
        if not password and not key_path:
            raise ValueError("Passwort oder Schlüsseldatei ist erforderlich für SFTP-Verteilung")
        
        # Asyncio SFTP-Client importieren
        import asyncssh
        
        # Verbindungsoptionen
        connect_options = {
            "username": username
        }
        
        if password:
            connect_options["password"] = password
        elif key_path:
            connect_options["client_keys"] = [key_path]
        
        # Mit SFTP-Server verbinden und Dateien hochladen
        uploaded_files = []
        async with asyncssh.connect(host, port=port, **connect_options) as conn:
            async with conn.start_sftp_client() as sftp:
                # Remote-Verzeichnis erstellen, falls nicht vorhanden
                try:
                    await sftp.stat(remote_dir)
                except asyncssh.SFTPError:
                    await sftp.mkdir(remote_dir)
                
                # Dateien hochladen
                for fmt in formats:
                    output_info = outputs[fmt]
                    if "path" in output_info and os.path.exists(output_info["path"]):
                        local_path = output_info["path"]
                        filename = os.path.basename(local_path)
                        remote_path = os.path.join(remote_dir, filename)
                        
                        await sftp.put(local_path, remote_path)
                        uploaded_files.append(remote_path)
        
        return {
            "status": "uploaded",
            "host": host,
            "remote_dir": remote_dir,
            "files": uploaded_files
        }
    
    async def _distribute_to_s3(self, target: Dict[str, Any], outputs: Dict[str, Any], formats: List[str]) -> Dict[str, Any]:
        """Verteilt Ausgaben zu einem S3-kompatiblen Objektspeicher.
        
        Args:
            target: Zielkonfiguration
            outputs: Generierte Ausgaben
            formats: Zu verteilende Formate
            
        Returns:
            Ergebnis des S3-Uploads
        """
        # S3-Konfiguration
        bucket = target.get("bucket")
        if not bucket:
            raise ValueError("Bucket ist erforderlich für S3-Verteilung")
        
        prefix = target.get("prefix", "")
        endpoint_url = target.get("endpoint_url")
        access_key = target.get("access_key", os.environ.get("AWS_ACCESS_KEY_ID"))
        secret_key = target.get("secret_key", os.environ.get("AWS_SECRET_ACCESS_KEY"))
        region = target.get("region", os.environ.get("AWS_REGION", "us-east-1"))
        
        if not all([access_key, secret_key]):
            raise ValueError("Zugriffsschlüssel und geheimer Schlüssel sind erforderlich für S3-Verteilung")
        
        # S3-Client importieren
        import aiobotocore.session
        
        # Mit S3 verbinden und Dateien hochladen
        uploaded_files = []
        session = aiobotocore.session.get_session()
        s3_config = {}
        
        if endpoint_url:
            s3_config["endpoint_url"] = endpoint_url
        
        async with session.create_client("s3", region_name=region,
                                          aws_access_key_id=access_key,
                                          aws_secret_access_key=secret_key,
                                          **s3_config) as s3:
            for fmt in formats:
                output_info = outputs[fmt]
                if "path" in output_info and os.path.exists(output_info["path"]):
                    local_path = output_info["path"]
                    filename = os.path.basename(local_path)
                    key = f"{prefix}{filename}" if prefix else filename
                    
                    # Datei hochladen
                    async with aiofiles.open(local_path, "rb") as f:
                        file_data = await f.read()
                        await s3.put_object(
                            Bucket=bucket,
                            Key=key,
                            Body=file_data,
                            ContentType=self._get_content_type(local_path)
                        )
                    
                    # URL zum Objekt generieren
                    url = f"s3://{bucket}/{key}"
                    # Bei öffentlichen Objekten auch HTTP-URL hinzufügen
                    if target.get("public", False):
                        if endpoint_url:
                            http_url = f"{endpoint_url}/{bucket}/{key}"
                        else:
                            http_url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
                        
                        uploaded_files.append({"key": key, "s3_url": url, "http_url": http_url})
                    else:
                        uploaded_files.append({"key": key, "s3_url": url})
        
        return {
            "status": "uploaded",
            "bucket": bucket,
            "prefix": prefix,
            "files": uploaded_files
        }
    
    async def _distribute_to_webhook(self, target: Dict[str, Any], outputs: Dict[str, Any], formats: List[str]) -> Dict[str, Any]:
        """Verteilt Ausgaben an einen Webhook.
        
        Args:
            target: Zielkonfiguration
            outputs: Generierte Ausgaben
            formats: Zu verteilende Formate
            
        Returns:
            Webhook-Antwort
        """
        # Webhook-Konfiguration
        webhook_url = target.get("url")
        if not webhook_url:
            raise ValueError("URL ist erforderlich für Webhook-Verteilung")
        
        method = target.get("method", "POST").upper()
        headers = target.get("headers", {})
        if not "Content-Type" in headers:
            headers["Content-Type"] = "application/json"
        
        # Payload vorbereiten
        payload = {
            "event_type": target.get("event_type", "processing_complete"),
            "outputs": {}
        }
        
        # Metadaten hinzufügen
        payload["metadata"] = target.get("metadata", {})
        
        # Ausgaben hinzufügen (nur Metadaten, keine Dateiinhalte)
        for fmt in formats:
            output_info = outputs[fmt].copy()
            
            # Pfad zu URL umwandeln, falls konfiguriert
            if "path" in output_info and target.get("generate_urls", False):
                base_url = target.get("base_download_url", "")
                if base_url:
                    filename = os.path.basename(output_info["path"])
                    output_info["download_url"] = f"{base_url}/{filename}"
            
            payload["outputs"][fmt] = output_info
        
        # Webhook aufrufen
        async with aiohttp.ClientSession() as session:
            if method == "POST":
                async with session.post(webhook_url, json=payload, headers=headers) as response:
                    response.raise_for_status()
                    try:
                        return await response.json()
                    except:
                        return {"status": response.status, "text": await response.text()}
            elif method == "PUT":
                async with session.put(webhook_url, json=payload, headers=headers) as response:
                    response.raise_for_status()
                    try:
                        return await response.json()
                    except:
                        return {"status": response.status, "text": await response.text()}
            else:
                raise ValueError(f"Nicht unterstützte HTTP-Methode für Webhook: {method}")
    
    async def _distribute_to_file(self, target: Dict[str, Any], outputs: Dict[str, Any], formats: List[str]) -> Dict[str, Any]:
        """Verteilt Ausgaben in ein Dateisystem.
        
        Args:
            target: Zielkonfiguration
            outputs: Generierte Ausgaben
            formats: Zu verteilende Formate
            
        Returns:
            Ergebnis der Dateiverteilung
        """
        # Zielverzeichnis
        output_dir = target.get("directory", self.output_processor.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        # Dateien kopieren oder verschieben
        copied_files = []
        for fmt in formats:
            output_info = outputs[fmt]
            if "path" in output_info and os.path.exists(output_info["path"]):
                source_path = output_info["path"]
                filename = target.get("filename_template", "{original}").format(
                    original=os.path.basename(source_path),
                    format=fmt,
                    timestamp=int(time.time())
                )
                
                dest_path = os.path.join(output_dir, filename)
                
                # Datei kopieren oder verschieben
                if target.get("move_files", False):
                    # Datei verschieben
                    os.rename(source_path, dest_path)
                else:
                    # Datei kopieren
                    async with aiofiles.open(source_path, "rb") as src:
                        async with aiofiles.open(dest_path, "wb") as dst:
                            while chunk := await src.read(65536):  # 64KB Chunks
                                await dst.write(chunk)
                
                copied_files.append({
                    "format": fmt,
                    "source": source_path,
                    "destination": dest_path
                })
        
        return {
            "status": "copied" if not target.get("move_files", False) else "moved",
            "directory": output_dir,
            "files": copied_files
        }
    
    def _get_content_type(self, file_path: str) -> str:
        """Bestimmt den MIME-Typ einer Datei basierend auf der Dateiendung.
        
        Args:
            file_path: Pfad zur Datei
            
        Returns:
            MIME-Typ der Datei
        """
        import mimetypes
        
        # MIME-Typen initialisieren
        mimetypes.init()
        
        # Dateierweiterung extrahieren
        ext = os.path.splitext(file_path)[1].lower()
        
        # Bekannte Typen definieren
        mime_types = {
            ".txt": "text/plain",
            ".json": "application/json",
            ".pdf": "application/pdf",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".csv": "text/csv",
            ".md": "text/markdown",
            ".html": "text/html",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".mp4": "video/mp4",
            ".avi": "video/x-msvideo",
            ".mov": "video/quicktime"
        }
        
        # Bekannten Typ zurückgeben, falls vorhanden
        if ext in mime_types:
            return mime_types[ext]
        
        # Ansonsten MIME-Typ über mimetypes bestimmen
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Fallback zu application/octet-stream
        return mime_type or "application/octet-stream"
```

## KI-Integration für erweiterte Funktionen

### Sprachausgabe und Objektbeschreibung

Die KI-Integration ermöglicht es, erkannte Objekte und Texte in natürlicher Sprache zu beschreiben und als Audiofeedback auszugeben.

#### KI-Sprachmodul:

```python
# ai/speech_module.py
import asyncio
import os
import tempfile
import logging
from typing import Dict, Any, List, Optional
import json
import time

class SpeechModule:
    """Modul für KI-gestützte Sprachgenerierung und -ausgabe."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert das Sprachmodul mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        self.logger = logging.getLogger("speech_module")
        
        # Text-to-Speech-Konfiguration
        self.tts_engine = config.get("tts_engine", "local")  # local oder cloud
        self.voice_id = config.get("voice_id", "default")
        self.speaking_rate = config.get("speaking_rate", 1.0)
        self.pitch = config.get("pitch", 0.0)
        
        # Sprach-Cache für häufige Phrasen
        self.speech_cache = {}
        self.cache_dir = config.get("cache_dir", "/tmp/speech_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Sprachdienst initialisieren
        self._initialize_tts_engine()
    
    def _initialize_tts_engine(self):
        """Initialisiert die Text-to-Speech-Engine basierend auf der Konfiguration."""
        if self.tts_engine == "local":
            try:
                # Lokale TTS-Engine (z.B. pyttsx3)
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', int(self.speaking_rate * 200))
                
                voices = self.engine.getProperty('voices')
                if voices and self.voice_id != "default":
                    # Versuchen, die gewünschte Stimme zu finden
                    for voice in voices:
                        if self.voice_id in voice.id:
                            self.engine.setProperty('voice', voice.id)
                            break
            except ImportError:
                self.logger.warning("pyttsx3 nicht installiert. Fallback zu temporären Audiodateien.")
                self.engine = None
        elif self.tts_engine == "google":
            try:
                # Google Cloud Text-to-Speech
                from google.cloud import texttospeech
                
                # Client initialisieren
                self.engine = texttospeech.TextToSpeechClient()
                
                # Stimme konfigurieren
                self.voice_config = texttospeech.VoiceSelectionParams(
                    language_code=config.get("language_code", "de-DE"),
                    name=self.voice_id
                )
                
                # Audio-Konfiguration
                self.audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=self.speaking_rate,
                    pitch=self.pitch
                )
            except ImportError:
                self.logger.warning("Google Cloud Text-to-Speech nicht installiert. Fallback zu lokalem TTS.")
                self.tts_engine = "local"
                self._initialize_tts_engine()
        else:
            self.logger.warning(f"Unbekannte TTS-Engine: {self.tts_engine}. Fallback zu lokalem TTS.")
            self.tts_engine = "local"
            self._initialize_tts_engine()
    
    async def generate_speech(self, text: str) -> Optional[str]:
        """Generiert Sprachausgabe für einen Text.
        
        Args:
            text: Zu sprechender Text
            
        Returns:
            Pfad zur generierten Audiodatei oder None bei Fehler
        """
        # Cache überprüfen
        cache_key = f"{self.tts_engine}_{self.voice_id}_{hash(text)}"
        if cache_key in self.speech_cache:
            return self.speech_cache[cache_key]
        
        # Dateinamen für die Ausgabe generieren
        output_file = os.path.join(self.cache_dir, f"{cache_key}.mp3")
        
        # Prüfen, ob bereits im Dateisystem gecacht
        if os.path.exists(output_file):
            self.speech_cache[cache_key] = output_file
            return output_file
        
        # Je nach Engine unterschiedlich verarbeiten
        try:
            if self.tts_engine == "local":
                # Lokale TTS-Engine
                if self.engine:
                    # pyttsx3 verwenden
                    self.engine.save_to_file(text, output_file)
                    self.engine.runAndWait()
                else:
                    # Fallback zu externem Befehl wie espeak
                    import subprocess
                    subprocess.run(["espeak", "-w", output_file, text], check=True)
            elif self.tts_engine == "google":
                # Google Cloud Text-to-Speech
                from google.cloud import texttospeech
                
                # Eingabetext konfigurieren
                synthesis_input = texttospeech.SynthesisInput(text=text)
                
                # TTS-Anfrage ausführen
                response = await asyncio.to_thread(
                    self.engine.synthesize_speech,
                    input=synthesis_input,
                    voice=self.voice_config,
                    audio_config=self.audio_config
                )
                
                # Audioinhalt in Datei speichern
                async with aiofiles.open(output_file, "wb") as out:
                    await out.write(response.audio_content)
            
            # In Cache speichern
            self.speech_cache[cache_key] = output_file
            return output_file
        except Exception as e:
            self.logger.error(f"Fehler bei der Sprachgenerierung: {str(e)}")
            return None
    
    async def speak(self, text: str, blocking: bool = False) -> bool:
        """Spricht einen Text aus.
        
        Args:
            text: Zu sprechender Text
            blocking: Ob auf Abschluss der Sprachausgabe gewartet werden soll
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        # Sprachdatei generieren
        audio_file = await self.generate_speech(text)
        if not audio_file:
            return False
        
        try:
            # Audio abspielen
            import pygame
            
            # Pygame mixer initialisieren, falls noch nicht geschehen
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Audio laden und abspielen
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Auf Abschluss warten, falls gewünscht
            if blocking:
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
            
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Abspielen der Sprachausgabe: {str(e)}")
            return False
    
    async def describe_objects(self, detections: List[Dict[str, Any]]) -> str:
        """Generiert eine natürlichsprachliche Beschreibung erkannter Objekte.
        
        Args:
            detections: Liste erkannter Objekte
            
        Returns:
            Natürlichsprachliche Beschreibung
        """
        if not detections:
            return "Keine Objekte erkannt."
        
        # Objekte nach Klassen gruppieren
        objects_by_class = {}
        for detection in detections:
            class_name = detection.get("class_name", "unbekannt")
            if class_name not in objects_by_class:
                objects_by_class[class_name] = []
            objects_by_class[class_name].append(detection)
        
        # Beschreibung generieren
        descriptions = []
        
        # Anzahl der Objekte jeder Klasse
        for class_name, objects in objects_by_class.items():
            if len(objects) == 1:
                descriptions.append(f"ein {class_name}")
            else:
                descriptions.append(f"{len(objects)} {class_name}s")
        
        # Beschreibung zusammensetzen
        if len(descriptions) == 1:
            text = f"Ich sehe {descriptions[0]}."
        elif len(descriptions) == 2:
            text = f"Ich sehe {descriptions[0]} und {descriptions[1]}."
        else:
            last = descriptions.pop()
            text = f"Ich sehe {', '.join(descriptions)} und {last}."
        
        return text
    
    async def describe_scene(self, detections: List[Dict[str, Any]], ocr_result: Optional[Dict[str, Any]] = None) -> str:
        """Generiert eine umfassende Beschreibung einer Szene mit Objekten und Text.
        
        Args:
            detections: Liste erkannter Objekte
            ocr_result: Optional Ergebnis der Texterkennung
            
        Returns:
            Natürlichsprachliche Beschreibung der Szene
        """
        # Objektbeschreibung
        object_description = await self.describe_objects(detections)
        
        # Textbeschreibung, falls vorhanden
        text_description = ""
        if ocr_result and "text" in ocr_result and ocr_result["text"].strip():
            recognized_text = ocr_result["text"].strip()
            # Text kürzen, wenn zu lang
            if len(recognized_text) > 100:
                recognized_text = recognized_text[:97] + "..."
            
            text_description = f" Ich erkenne folgenden Text: {recognized_text}"
        
        # Gesamtbeschreibung
        return object_description + text_description
    
    async def generate_distance_feedback(self, distance: float, object_name: str) -> str:
        """Generiert Feedback zur Entfernung eines Objekts.
        
        Args:
            distance: Entfernung in Metern
            object_name: Name des Objekts
            
        Returns:
            Natürlichsprachliche Beschreibung der Entfernung
        """
        # Feedback basierend auf Entfernung
        if distance < 0.5:
            return f"Achtung! {object_name} ist sehr nah, weniger als einen halben Meter entfernt."
        elif distance < 1.0:
            return f"{object_name} ist etwa {distance:.1f} Meter entfernt."
        elif distance < 10.0:
            return f"{object_name} ist {distance:.1f} Meter entfernt."
        else:
            return f"{object_name} ist weit entfernt, etwa {distance:.0f} Meter."
```

### Räumliches Bewusstsein und Distanzmessung

Das räumliche Bewusstsein ermöglicht es der Plattform, Distanzen zu erkannten Objekten zu messen und dem Benutzer Feedback über die räumliche Anordnung zu geben.

#### Räumliches Analysemodul:

```python
# ai/spatial_analysis.py
import numpy as np
import cv2
import math
from typing import Dict, Any, List, Optional, Tuple

class SpatialAnalysisModule:
    """Modul für räumliche Analyse und Distanzmessung."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert das räumliche Analysemodul mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        
        # Kamerakonfiguration
        self.camera_height = config.get("camera_height", 1.5)  # in Metern
        self.camera_angle = config.get("camera_angle", 15)  # in Grad
        self.focal_length = config.get("focal_length", 35)  # in mm
        self.sensor_height = config.get("sensor_height", 24)  # in mm
        
        # Tiefenkamera-Konfiguration
        self.use_depth_camera = config.get("use_depth_camera", False)
        self.depth_scale = config.get("depth_scale", 0.001)  # Umrechnungsfaktor für Tiefenwerte
        
        # Kalibrierungsdaten
        self.camera_matrix = None
        self.dist_coeffs = None
        
        # Referenzobjekte für Größenvergleich
        self.reference_objects = config.get("reference_objects", {
            "person": 1.7,  # Durchschnittliche Höhe in Metern
            "car": 1.5,     # Durchschnittliche Höhe in Metern
            "chair": 0.8,   # Durchschnittliche Höhe in Metern
            "bottle": 0.25  # Durchschnittliche Höhe in Metern
        })
        
        # Kamera kalibrieren, falls Kalibrierungsdaten vorhanden
        if "calibration" in config:
            self._load_calibration(config["calibration"])
    
    def _load_calibration(self, calibration: Dict[str, Any]):
        """Lädt Kamerakalibrierungsdaten.
        
        Args:
            calibration: Kalibrierungsdaten
        """
        if "camera_matrix" in calibration and "dist_coeffs" in calibration:
            self.camera_matrix = np.array(calibration["camera_matrix"])
            self.dist_coeffs = np.array(calibration["dist_coeffs"])
    
    def estimate_depth_from_stereo(self, left_img: np.ndarray, right_img: np.ndarray) -> np.ndarray:
        """Schätzt Tiefe aus Stereo-Bildpaar.
        
        Args:
            left_img: Linkes Bild
            right_img: Rechtes Bild
            
        Returns:
            Tiefenkarte
        """
        # Bilder in Graustufen konvertieren
        if len(left_img.shape) == 3:
            left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
            right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
        else:
            left_gray = left_img
            right_gray = right_img
        
        # Stereo-Block-Matcher erstellen
        window_size = 11
        min_disp = 0
        num_disp = 128 - min_disp
        
        stereo = cv2.StereoSGBM_create(
            minDisparity=min_disp,
            numDisparities=num_disp,
            blockSize=window_size,
            P1=8 * 3 * window_size ** 2,
            P2=32 * 3 * window_size ** 2,
            disp12MaxDiff=1,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32
        )
        
        # Disparitätskarte berechnen
        disparity = stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0
        
        # Disparitätskarte in Tiefenkarte umwandeln
        # In einer echten Implementierung würde hier die Baseline und Brennweite verwendet
        # für eine genaue Umrechnung in Meter
        baseline = self.config.get("stereo_baseline", 0.1)  # 10 cm zwischen Kameras
        focal_px = self.focal_length / self.sensor_height * left_img.shape[0]
        
        # Z = baseline * focal_length / disparity
        valid_mask = disparity > 0
        depth = np.zeros_like(disparity)
        depth[valid_mask] = baseline * focal_px / disparity[valid_mask]
        
        return depth
    
    def estimate_distance(self, detection: Dict[str, Any], depth_map: Optional[np.ndarray] = None) -> float:
        """Schätzt die Entfernung zu einem erkannten Objekt.
        
        Args:
            detection: Erkanntes Objekt
            depth_map: Optional Tiefenkarte
            
        Returns:
            Geschätzte Entfernung in Metern
        """
        # Tiefenkarte verwenden, falls vorhanden
        if depth_map is not None:
            return self._estimate_distance_from_depth(detection, depth_map)
        
        # Referenzgrößen verwenden
        return self._estimate_distance_from_size(detection)
    
    def _estimate_distance_from_depth(self, detection: Dict[str, Any], depth_map: np.ndarray) -> float:
        """Schätzt Entfernung aus Tiefenkarte.
        
        Args:
            detection: Erkanntes Objekt
            depth_map: Tiefenkarte
            
        Returns:
            Geschätzte Entfernung in Metern
        """
        # Begrenzungsrahmen des Objekts
        box = detection["box"]
        x, y, w, h = box["x"], box["y"], box["width"], box["height"]
        
        # Mittelpunkt des Objekts bestimmen
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Bereich um den Mittelpunkt für stabilere Messung
        region_size = 5
        x_min = max(0, center_x - region_size)
        x_max = min(depth_map.shape[1] - 1, center_x + region_size)
        y_min = max(0, center_y - region_size)
        y_max = min(depth_map.shape[0] - 1, center_y + region_size)
        
        # Mittlere Tiefe im Bereich
        roi = depth_map[y_min:y_max+1, x_min:x_max+1]
        valid_depths = roi[roi > 0]
        
        if len(valid_depths) > 0:
            # Median für Robustheit gegen Ausreißer
            return np.median(valid_depths) * self.depth_scale
        else:
            # Fallback auf Größenschätzung
            return self._estimate_distance_from_size(detection)
    
    def _estimate_distance_from_size(self, detection: Dict[str, Any]) -> float:
        """Schätzt Entfernung basierend auf bekannter Objektgröße.
        
        Args:
            detection: Erkanntes Objekt
            
        Returns:
            Geschätzte Entfernung in Metern
        """
        # Begrenzungsrahmen des Objekts
        box = detection["box"]
        _, _, _, h = box["x"], box["y"], box["width"], box["height"]
        
        # Klasse des Objekts
        class_name = detection.get("class_name", "unknown")
        
        # Referenzgröße für diese Klasse
        real_height = self.reference_objects.get(class_name)
        if real_height is None:
            # Fallback für unbekannte Objekte
            real_height = 1.0  # Annahme: 1 Meter
        
        # Brennweite in Pixeln
        focal_px = self.focal_length / self.sensor_height * 1000  # Annahme: 1000 Pixel Bildhöhe
        
        # Entfernung = (reale Höhe * Brennweite) / Bildhöhe
        distance = (real_height * focal_px) / h
        
        return distance
    
    def analyze_spatial_relations(self, detections: List[Dict[str, Any]], depth_map: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """Analysiert räumliche Beziehungen zwischen erkannten Objekten.
        
        Args:
            detections: Liste erkannter Objekte
            depth_map: Optional Tiefenkarte
            
        Returns:
            Liste räumlicher Beziehungen
        """
        # Entfernungen zu allen Objekten berechnen
        for detection in detections:
            detection["distance"] = self.estimate_distance(detection, depth_map)
        
        # Objekte nach Entfernung sortieren
        sorted_detections = sorted(detections, key=lambda x: x["distance"])
        
        # Räumliche Beziehungen analysieren
        relations = []
        
        for i, obj1 in enumerate(sorted_detections):
            for j, obj2 in enumerate(sorted_detections[i+1:], i+1):
                # Relative Position berechnen
                box1 = obj1["box"]
                box2 = obj2["box"]
                
                # Mittelpunkte
                center1_x = box1["x"] + box1["width"] // 2
                center1_y = box1["y"] + box1["height"] // 2
                center2_x = box2["x"] + box2["width"] // 2
                center2_y = box2["y"] + box2["height"] // 2
                
                # Horizontale Relation
                if center1_x < center2_x:
                    h_relation = "links von"
                else:
                    h_relation = "rechts von"
                
                # Vertikale Relation
                if center1_y < center2_y:
                    v_relation = "über"
                else:
                    v_relation = "unter"
                
                # Distanz zwischen Objekten
                dist_diff = abs(obj1["distance"] - obj2["distance"])
                
                # Relation hinzufügen
                relations.append({
                    "object1": {
                        "id": i,
                        "class": obj1.get("class_name", "unknown"),
                        "distance": obj1["distance"]
                    },
                    "object2": {
                        "id": j,
                        "class": obj2.get("class_name", "unknown"),
                        "distance": obj2["distance"]
                    },
                    "horizontal_relation": h_relation,
                    "vertical_relation": v_relation,
                    "distance_difference": dist_diff
                })
        
        return relations
    
    def generate_spatial_description(self, detections: List[Dict[str, Any]], depth_map: Optional[np.ndarray] = None) -> str:
        """Generiert eine natürlichsprachliche Beschreibung der räumlichen Szene.
        
        Args:
            detections: Liste erkannter Objekte
            depth_map: Optional Tiefenkarte
            
        Returns:
            Natürlichsprachliche Beschreibung
        """
        if not detections:
            return "Keine Objekte erkannt."
        
        # Räumliche Beziehungen analysieren
        for detection in detections:
            detection["distance"] = self.estimate_distance(detection, depth_map)
        
        # Objekte nach Entfernung sortieren
        sorted_detections = sorted(detections, key=lambda x: x["distance"])
        
        # Beschreibung der nächsten Objekte
        descriptions = []
        
        # Nächstes Objekt
        nearest = sorted_detections[0]
        descriptions.append(f"{nearest.get('class_name', 'Ein Objekt')} ist am nächsten, etwa {nearest['distance']:.1f} Meter entfernt.")
        
        # Weitere nahe Objekte (max. 3)
        for obj in sorted_detections[1:4]:
            descriptions.append(f"{obj.get('class_name', 'Ein Objekt')} ist ungefähr {obj['distance']:.1f} Meter entfernt.")
        
        # Warnung, falls Objekte sehr nah sind
        warnings = []
        for obj in sorted_detections:
            if obj["distance"] < 1.0:
                warnings.append(f"Achtung! {obj.get('class_name', 'Ein Objekt')} ist sehr nah!")
        
        # Beschreibung zusammensetzen
        result = " ".join(descriptions)
        if warnings:
            result += " " + " ".join(warnings)
        
        return result
```

## Sicherheitsimplementierung

### Authentifizierung und Autorisierung

Die Sicherheitsimplementierung stellt sicher, dass nur autorisierte Benutzer auf die Plattform zugreifen können und dass die Zugriffsrechte entsprechend den Rollen und Berechtigungen der Benutzer eingeschränkt sind.

#### Erweitertes Authentifizierungsmodul:

```python
# security/auth_manager.py
import jwt
import time
import uuid
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import os
import hashlib
import secrets
import bcrypt

class AuthManager:
    """Manager für Authentifizierung und Autorisierung."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert den Authentifizierungsmanager mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        self.logger = logging.getLogger("auth_manager")
        
        # JWT-Konfiguration
        self.jwt_secret = config.get("jwt_secret", os.environ.get("JWT_SECRET", secrets.token_hex(32)))
        self.jwt_algorithm = config.get("jwt_algorithm", "HS256")
        self.token_expiry = config.get("token_expiry", 3600)  # 1 Stunde
        self.refresh_token_expiry = config.get("refresh_token_expiry", 2592000)  # 30 Tage
        
        # Token-Blacklist für ungültige Tokens
        self.token_blacklist = set()
        
        # Benutzerdatenbank (in echter Implementierung würde hier eine DB-Verbindung erfolgen)
        self.user_db = None
        self._initialize_user_db()
    
    def _initialize_user_db(self):
        """Initialisiert die Benutzerdatenbank-Verbindung."""
        # In echter Implementierung würde hier eine Datenbankverbindung hergestellt werden
        # Für diese Demo verwenden wir ein einfaches Dictionary
        self.user_db = {}
    
    def register_user(self, username: str, password: str, email: str, roles: List[str] = None) -> Dict[str, Any]:
        """Registriert einen neuen Benutzer.
        
        Args:
            username: Benutzername
            password: Passwort
            email: E-Mail-Adresse
            roles: Rollen des Benutzers (Standard: ["user"])
            
        Returns:
            Benutzerinformationen
        
        Raises:
            ValueError: Wenn der Benutzername bereits existiert
        """
        if username in self.user_db:
            raise ValueError(f"Benutzername {username} existiert bereits")
        
        # Passwort hashen
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        # Standardrollen verwenden, falls nicht angegeben
        if roles is None:
            roles = ["user"]
        
        # Benutzer erstellen
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "roles": roles,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True
        }
        
        # Benutzer speichern
        self.user_db[username] = user
        
        # Sensible Daten aus Rückgabe entfernen
        user_info = user.copy()
        del user_info["password_hash"]
        
        return user_info
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authentifiziert einen Benutzer.
        
        Args:
            username: Benutzername
            password: Passwort
            
        Returns:
            Benutzerinformationen oder None bei Fehler
        """
        # Benutzer in der Datenbank suchen
        user = self.user_db.get(username)
        if not user:
            self.logger.warning(f"Authentifizierungsversuch für nicht existierenden Benutzer: {username}")
            return None
        
        # Prüfen, ob der Benutzer aktiv ist
        if not user.get("is_active", True):
            self.logger.warning(f"Authentifizierungsversuch für deaktivierten Benutzer: {username}")
            return None
        
        # Passwort prüfen
        if not bcrypt.checkpw(password.encode(), user["password_hash"]):
            self.logger.warning(f"Falsches Passwort für Benutzer: {username}")
            return None
        
        # Erfolgreiche Authentifizierung
        # Aktualisiere den letzten Login-Zeitpunkt
        user["last_login"] = datetime.now().isoformat()
        
        # Sensible Daten aus Rückgabe entfernen
        user_info = user.copy()
        del user_info["password_hash"]
        
        return user_info
    
    def create_token(self, user_id: str, additional_claims: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Erstellt ein JWT-Token und Refresh-Token für einen Benutzer.
        
        Args:
            user_id: Benutzer-ID
            additional_claims: Zusätzliche Claims für das Token
            
        Returns:
            Dictionary mit Token, Refresh-Token und Ablaufzeiten
        """
        now = datetime.now()
        expires_at = now + timedelta(seconds=self.token_expiry)
        refresh_expires_at = now + timedelta(seconds=self.refresh_token_expiry)
        
        # Basis-Claims
        claims = {
            "sub": user_id,
            "iat": now.timestamp(),
            "exp": expires_at.timestamp(),
            "jti": str(uuid.uuid4())
        }
        
        # Zusätzliche Claims hinzufügen
        if additional_claims:
            claims.update(additional_claims)
        
        # Token erstellen
        token = jwt.encode(claims, self.jwt_secret, algorithm=self.jwt_algorithm)
        
        # Refresh-Token erstellen
        refresh_claims = {
            "sub": user_id,
            "iat": now.timestamp(),
            "exp": refresh_expires_at.timestamp(),
            "jti": str(uuid.uuid4()),
            "type": "refresh"
        }
        refresh_token = jwt.encode(refresh_claims, self.jwt_secret, algorithm=self.jwt_algorithm)
        
        return {
            "token": token,
            "token_type": "Bearer",
            "expires_at": expires_at.isoformat(),
            "refresh_token": refresh_token,
            "refresh_expires_at": refresh_expires_at.isoformat()
        }
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validiert ein JWT-Token.
        
        Args:
            token: JWT-Token
            
        Returns:
            Token-Claims oder None bei ungültigem Token
        """
        try:
            # Prüfen, ob das Token in der Blacklist ist
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            if token_hash in self.token_blacklist:
                self.logger.warning("Token ist in der Blacklist")
                return None
            
            # Token dekodieren und validieren
            claims = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # Prüfen, ob es ein Refresh-Token ist
            if claims.get("type") == "refresh":
                self.logger.warning("Versuch, ein Refresh-Token als Access-Token zu verwenden")
                return None
            
            return claims
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token ist abgelaufen")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Ungültiges Token: {e}")
            return None
    
    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Erneuert ein Token mit einem Refresh-Token.
        
        Args:
            refresh_token: Refresh-Token
            
        Returns:
            Neues Token oder None bei Fehler
        """
        try:
            # Refresh-Token dekodieren und validieren
            claims = jwt.decode(refresh_token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # Prüfen, ob es ein Refresh-Token ist
            if claims.get("type") != "refresh":
                self.logger.warning("Token ist kein Refresh-Token")
                return None
            
            # Neues Token erstellen
            user_id = claims["sub"]
            
            # Benutzer suchen
            user = None
            for u in self.user_db.values():
                if u["id"] == user_id:
                    user = u
                    break
            
            if not user:
                self.logger.warning(f"Benutzer für Token nicht gefunden: {user_id}")
                return None
            
            # Prüfen, ob der Benutzer aktiv ist
            if not user.get("is_active", True):
                self.logger.warning(f"Benutzer ist deaktiviert: {user_id}")
                return None
            
            # Rollen als zusätzliche Claims hinzufügen
            additional_claims = {
                "roles": user["roles"]
            }
            
            # Neues Token erstellen
            return self.create_token(user_id, additional_claims)
        except jwt.ExpiredSignatureError:
            self.logger.warning("Refresh-Token ist abgelaufen")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Ungültiges Refresh-Token: {e}")
            return None
    
    def revoke_token(self, token: str):
        """Sperrt ein Token, indem es in die Blacklist aufgenommen wird.
        
        Args:
            token: Zu sperrendes Token
        """
        try:
            # Token dekodieren, um die Ablaufzeit zu erhalten
            claims = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # Hash des Tokens zur Blacklist hinzufügen
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            self.token_blacklist.add(token_hash)
            
            # In echter Implementierung würde das Token in einer Datenbank gespeichert werden
            # mit der Ablaufzeit, um die Blacklist regelmäßig zu bereinigen
        except Exception as e:
            self.logger.error(f"Fehler beim Sperren des Tokens: {e}")
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Gibt Benutzerinformationen anhand der ID zurück.
        
        Args:
            user_id: Benutzer-ID
            
        Returns:
            Benutzerinformationen oder None, wenn nicht gefunden
        """
        for user in self.user_db.values():
            if user["id"] == user_id:
                # Sensible Daten aus Rückgabe entfernen
                user_info = user.copy()
                if "password_hash" in user_info:
                    del user_info["password_hash"]
                return user_info
        
        return None
    
    def check_permission(self, user_id: str, permission: str) -> bool:
        """Prüft, ob ein Benutzer eine bestimmte Berechtigung hat.
        
        Args:
            user_id: Benutzer-ID
            permission: Zu prüfende Berechtigung
            
        Returns:
            True, wenn der Benutzer die Berechtigung hat, sonst False
        """
        # Benutzer finden
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Admin hat alle Berechtigungen
        if "admin" in user.get("roles", []):
            return True
        
        # Berechtigungen basierend auf Rollen
        role_permissions = {
            "user": ["read:own", "write:own", "delete:own"],
            "viewer": ["read:own"],
            "operator": ["read:all", "write:own", "delete:own"],
            "manager": ["read:all", "write:all", "delete:own"]
        }
        
        # Berechtigungen für alle Rollen des Benutzers sammeln
        user_permissions = []
        for role in user.get("roles", []):
            if role in role_permissions:
                user_permissions.extend(role_permissions[role])
        
        # Prüfen, ob die angeforderte Berechtigung vorhanden ist
        return permission in user_permissions
```

### Verschlüsselung und Datenschutz

Die Verschlüsselungs- und Datenschutzimplementierung stellt sicher, dass sensible Daten während der Verarbeitung und Speicherung geschützt sind.

#### Datenschutzmodul:

```python
# security/privacy_manager.py
import os
import hashlib
import base64
import logging
from typing import Dict, Any, List, Optional, Union, BinaryIO
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import json

class PrivacyManager:
    """Manager für Datenschutz und Verschlüsselung."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert den Datenschutzmanager mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        self.logger = logging.getLogger("privacy_manager")
        
        # Verschlüsselungskonfiguration
        self.encryption_enabled = config.get("encryption_enabled", True)
        self.encryption_key = None
        
        # Anonymisierungskonfiguration
        self.anonymize_faces = config.get("anonymize_faces", True)
        self.anonymize_license_plates = config.get("anonymize_license_plates", True)
        self.anonymize_personal_data = config.get("anonymize_personal_data", True)
        
        # Bereiche mit persönlichen Daten
        self.personal_data_patterns = config.get("personal_data_patterns", [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # E-Mail
            r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",                        # Telefonnummer
            r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b",                        # Datum
            r"\b[A-Z]{1,2}[-. ]?\d{1,2}[-. ]?\d{1,2}[-. ]?\d{1,2}\b" # Ausweisnummer
        ])
        
        # Verschlüsselung initialisieren
        if self.encryption_enabled:
            self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialisiert die Verschlüsselungsfunktionalität."""
        try:
            # Schlüssel aus Umgebungsvariable oder Konfiguration
            key_base = self.config.get("encryption_key", os.environ.get("ENCRYPTION_KEY"))
            
            if key_base:
                # PBKDF2 für sicheren Schlüssel
                salt = b'universal_vision_ocr_system'  # In Produktion: sicheren Salt verwenden
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000
                )
                key = base64.urlsafe_b64encode(kdf.derive(key_base.encode()))
            else:
                # Generiere einen neuen Schlüssel
                key = Fernet.generate_key()
                self.logger.warning("Kein Verschlüsselungsschlüssel konfiguriert. Generiere temporären Schlüssel.")
            
            # Fernet-Cipher erstellen
            self.encryption_key = key
            self.cipher = Fernet(key)
            self.logger.info("Verschlüsselung initialisiert.")
        except Exception as e:
            self.logger.error(f"Fehler bei der Initialisierung der Verschlüsselung: {str(e)}")
            self.encryption_enabled = False
    
    def encrypt_data(self, data: Union[str, bytes]) -> Optional[str]:
        """Verschlüsselt Daten.
        
        Args:
            data: Zu verschlüsselnde Daten
            
        Returns:
            Verschlüsselte Daten als Base64-String oder None bei Fehler
        """
        if not self.encryption_enabled or not self.encryption_key:
            self.logger.warning("Verschlüsselung ist deaktiviert. Daten werden unverschlüsselt zurückgegeben.")
            return data if isinstance(data, str) else data.decode('utf-8', errors='replace')
        
        try:
            # Daten in Bytes konvertieren, falls nötig
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            # Daten verschlüsseln
            encrypted = self.cipher.encrypt(data_bytes)
            
            # Als Base64 zurückgeben
            return base64.urlsafe_b64encode(encrypted).decode('ascii')
        except Exception as e:
            self.logger.error(f"Fehler bei der Verschlüsselung: {str(e)}")
            return None
    
    def decrypt_data(self, encrypted_data: Union[str, bytes]) -> Optional[str]:
        """Entschlüsselt Daten.
        
        Args:
            encrypted_data: Verschlüsselte Daten
            
        Returns:
            Entschlüsselte Daten als String oder None bei Fehler
        """
        if not self.encryption_enabled or not self.encryption_key:
            self.logger.warning("Verschlüsselung ist deaktiviert. Daten werden unverändert zurückgegeben.")
            return encrypted_data if isinstance(encrypted_data, str) else encrypted_data.decode('utf-8', errors='replace')
        
        try:
            # Daten in Bytes konvertieren, falls nötig
            if isinstance(encrypted_data, str):
                # Base64-decodieren
                encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
            else:
                encrypted_bytes = encrypted_data
            
            # Daten entschlüsseln
            decrypted = self.cipher.decrypt(encrypted_bytes)
            
            # Als String zurückgeben
            return decrypted.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Fehler bei der Entschlüsselung: {str(e)}")
            return None
    
    def encrypt_file(self, input_path: str, output_path: Optional[str] = None) -> Optional[str]:
        """Verschlüsselt eine Datei.
        
        Args:
            input_path: Pfad zur Quelldatei
            output_path: Pfad zur Zieldatei (optional)
            
        Returns:
            Pfad zur verschlüsselten Datei oder None bei Fehler
        """
        if not self.encryption_enabled or not self.encryption_key:
            self.logger.warning("Verschlüsselung ist deaktiviert. Datei wird unverschlüsselt kopiert.")
            
            if output_path:
                import shutil
                shutil.copy2(input_path, output_path)
                return output_path
            return input_path
        
        try:
            # Quelldatei lesen
            with open(input_path, 'rb') as f:
                data = f.read()
            
            # Daten verschlüsseln
            encrypted = self.cipher.encrypt(data)
            
            # Zieldateiname bestimmen
            if not output_path:
                output_path = input_path + '.enc'
            
            # Verschlüsselte Daten speichern
            with open(output_path, 'wb') as f:
                f.write(encrypted)
            
            return output_path
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiverschlüsselung: {str(e)}")
            return None
    
    def decrypt_file(self, input_path: str, output_path: Optional[str] = None) -> Optional[str]:
        """Entschlüsselt eine Datei.
        
        Args:
            input_path: Pfad zur verschlüsselten Datei
            output_path: Pfad zur entschlüsselten Datei (optional)
            
        Returns:
            Pfad zur entschlüsselten Datei oder None bei Fehler
        """
        if not self.encryption_enabled or not self.encryption_key:
            self.logger.warning("Verschlüsselung ist deaktiviert. Datei wird unverändert kopiert.")
            
            if output_path:
                import shutil
                shutil.copy2(input_path, output_path)
                return output_path
            return input_path
        
        try:
            # Quelldatei lesen
            with open(input_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Daten entschlüsseln
            decrypted = self.cipher.decrypt(encrypted_data)
            
            # Zieldateiname bestimmen
            if not output_path:
                # Entferne .enc-Erweiterung, falls vorhanden
                if input_path.endswith('.enc'):
                    output_path = input_path[:-4]
                else:
                    output_path = input_path + '.dec'
            
            # Entschlüsselte Daten speichern
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            return output_path
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateientschlüsselung: {str(e)}")
            return None
    
    def anonymize_image(self, image, detections: List[Dict[str, Any]]) -> Any:
        """Anonymisiert persönliche Informationen in einem Bild.
        
        Args:
            image: Eingabebild
            detections: Erkannte Objekte/Bereiche
            
        Returns:
            Anonymisiertes Bild
        """
        import cv2
        import numpy as np
        
        # Bild kopieren
        result = image.copy()
        
        # Gesichter anonymisieren
        if self.anonymize_faces:
            for detection in detections:
                if detection.get("class_name") in ["person", "face"]:
                    box = detection["box"]
                    x, y, w, h = box["x"], box["y"], box["width"], box["height"]
                    
                    # Bei Personen-Detektion, Kopfbereich schätzen
                    if detection.get("class_name") == "person":
                        # Oberes Drittel des Begrenzungsrahmens (ungefährer Kopfbereich)
                        h_face = h // 3
                        y_face = y
                        x_face = x
                        w_face = w
                    else:
                        # Bei Gesichtsdetektion direkt verwenden
                        x_face, y_face, w_face, h_face = x, y, w, h
                    
                    # Bereich pixelieren
                    face_roi = result[y_face:y_face+h_face, x_face:x_face+w_face]
                    
                    # Kleiner skalieren (pixelieren)
                    scale_factor = 0.1
                    small = cv2.resize(face_roi, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)
                    # Zurück zur Originalgröße
                    pixelated = cv2.resize(small, (w_face, h_face), interpolation=cv2.INTER_NEAREST)
                    
                    # Zurück ins Originalbild einfügen
                    result[y_face:y_face+h_face, x_face:x_face+w_face] = pixelated
        
        # Kennzeichen anonymisieren
        if self.anonymize_license_plates:
            for detection in detections:
                if detection.get("class_name") in ["license_plate", "car"]:
                    box = detection["box"]
                    x, y, w, h = box["x"], box["y"], box["width"], box["height"]
                    
                    # Bei Auto-Detektion, Kennzeichenbereich schätzen
                    if detection.get("class_name") == "car":
                        # Unteres Viertel des Begrenzungsrahmens (ungefährer Kennzeichenbereich)
                        h_plate = h // 4
                        y_plate = y + h - h_plate
                        x_plate = x + w // 4
                        w_plate = w // 2
                    else:
                        # Bei Kennzeichendetektion direkt verwenden
                        x_plate, y_plate, w_plate, h_plate = x, y, w, h
                    
                    # Bereich verpixeln
                    plate_roi = result[y_plate:y_plate+h_plate, x_plate:x_plate+w_plate]
                    
                    # Kleiner skalieren (pixelieren)
                    scale_factor = 0.1
                    small = cv2.resize(plate_roi, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)
                    # Zurück zur Originalgröße
                    pixelated = cv2.resize(small, (w_plate, h_plate), interpolation=cv2.INTER_NEAREST)
                    
                    # Zurück ins Originalbild einfügen
                    result[y_plate:y_plate+h_plate, x_plate:x_plate+w_plate] = pixelated
        
        return result
    
    def anonymize_text(self, text: str) -> str:
        """Anonymisiert persönliche Informationen in einem Text.
        
        Args:
            text: Zu anonymisierender Text
            
        Returns:
            Anonymisierter Text
        """
        ```python
        if not text or not self.anonymize_personal_data:
            return text
        
        import re
        
        # Anonymisierter Text (Ausgangspunkt ist der Originaltext)
        anonymized = text
        
        # Persönliche Daten erkennen und anonymisieren
        for pattern in self.personal_data_patterns:
            # Alle Treffer finden
            matches = re.finditer(pattern, anonymized)
            
            # Treffer durch Platzhalter ersetzen
            for match in matches:
                matched_text = match.group(0)
                pattern_type = "PERSÖNLICHE_DATEN"
                
                # Muster-Typ erkennen
                if re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", matched_text):
                    pattern_type = "E-MAIL"
                elif re.match(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", matched_text):
                    pattern_type = "TELEFON"
                elif re.match(r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b", matched_text):
                    pattern_type = "DATUM"
                elif re.match(r"\b[A-Z]{1,2}[-. ]?\d{1,2}[-. ]?\d{1,2}[-. ]?\d{1,2}\b", matched_text):
                    pattern_type = "ID-NUMMER"
                
                # Ersetzung vornehmen
                anonymized = anonymized.replace(matched_text, f"[{pattern_type}]")
        
        return anonymized
    
    def anonymize_detection_results(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Anonymisiert persönliche Informationen in Erkennungsergebnissen.
        
        Args:
            detections: Erkennungsergebnisse
            
        Returns:
            Anonymisierte Erkennungsergebnisse
        """
        if not detections or not self.anonymize_personal_data:
            return detections
        
        # Ergebnisse kopieren, um Original nicht zu verändern
        anonymized_detections = []
        
        for detection in detections:
            # Kopie des aktuellen Detektionsergebnisses erstellen
            anonymized = detection.copy()
            
            # Text anonymisieren, falls vorhanden
            if "text" in anonymized:
                anonymized["text"] = self.anonymize_text(anonymized["text"])
            
            # Klassennamen filtern
            if anonymized.get("class_name") in ["face", "license_plate", "person"]:
                # Position und Konfidenz beibehalten, aber Text und detaillierte Infos entfernen
                if "text" in anonymized:
                    del anonymized["text"]
                if "details" in anonymized:
                    del anonymized["details"]
            
            anonymized_detections.append(anonymized)
        
        return anonymized_detections
    
    def generate_privacy_report(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generiert einen Datenschutzbericht für verarbeitete Inhalte.
        
        Args:
            content: Verarbeiteter Inhalt
            
        Returns:
            Datenschutzbericht
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "privacy_features_enabled": {
                "encryption": self.encryption_enabled,
                "face_anonymization": self.anonymize_faces,
                "license_plate_anonymization": self.anonymize_license_plates,
                "personal_data_anonymization": self.anonymize_personal_data
            },
            "data_processing_summary": {}
        }
        
        # Zähle verarbeitete und anonymisierte Elemente
        if "detections" in content:
            detections = content["detections"]
            report["data_processing_summary"]["total_detections"] = len(detections)
            
            # Zähle nach Klassen
            class_counts = {}
            sensitive_classes = ["face", "license_plate", "person"]
            anonymized_count = 0
            
            for detection in detections:
                class_name = detection.get("class_name", "unknown")
                
                if class_name not in class_counts:
                    class_counts[class_name] = 0
                class_counts[class_name] += 1
                
                if class_name in sensitive_classes:
                    anonymized_count += 1
            
            report["data_processing_summary"]["class_distribution"] = class_counts
            report["data_processing_summary"]["anonymized_elements"] = anonymized_count
        
        # Text-Verarbeitungszusammenfassung
        if "text" in content:
            text = content["text"]
            report["data_processing_summary"]["text_length"] = len(text)
            
            # Zähle potenzielle persönliche Daten im Text
            personal_data_matches = 0
            for pattern in self.personal_data_patterns:
                import re
                matches = re.findall(pattern, text)
                personal_data_matches += len(matches)
            
            report["data_processing_summary"]["potential_personal_data_matches"] = personal_data_matches
        
        return report
```

### Secure Configuration Management

```python
# security/config_manager.py
import os
import json
import logging
from typing import Dict, Any, Optional
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureConfigManager:
    """Manager für sichere Konfigurationsverwaltung."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialisiert den Konfigurationsmanager.
        
        Args:
            config_path: Pfad zur Konfigurationsdatei
        """
        self.logger = logging.getLogger("config_manager")
        
        # Konfigurationspfad bestimmen
        self.config_path = config_path or os.environ.get("CONFIG_PATH", "config.json")
        
        # Verschlüsselung initialisieren
        self.encryption_enabled = False
        self.cipher = None
        self._initialize_encryption()
        
        # Konfiguration laden
        self.config = self._load_config()
    
    def _initialize_encryption(self):
        """Initialisiert die Verschlüsselung für sensible Konfigurationswerte."""
        # Schlüssel aus Umgebungsvariable oder Datei
        key_base = os.environ.get("CONFIG_ENCRYPTION_KEY")
        key_file = os.environ.get("CONFIG_ENCRYPTION_KEY_FILE")
        
        if key_file and os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key_base = f.read().strip().decode('utf-8')
        
        if not key_base:
            self.logger.warning("Kein Verschlüsselungsschlüssel gefunden. Sensible Konfigurationswerte werden nicht verschlüsselt.")
            return
        
        try:
            # PBKDF2 für sicheren Schlüssel
            salt = b'secure_config_manager_salt'  # In Produktion: sicheren Salt verwenden
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(key_base.encode()))
            
            # Fernet-Cipher erstellen
            self.cipher = Fernet(key)
            self.encryption_enabled = True
            
            self.logger.info("Verschlüsselung für Konfiguration initialisiert.")
        except Exception as e:
            self.logger.error(f"Fehler bei der Initialisierung der Verschlüsselung: {str(e)}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Lädt die Konfiguration aus der Datei.
        
        Returns:
            Konfigurationsdaten
        """
        if not os.path.exists(self.config_path):
            self.logger.warning(f"Konfigurationsdatei nicht gefunden: {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Verschlüsselte Werte entschlüsseln
            if self.encryption_enabled:
                config = self._decrypt_config_values(config)
            
            return config
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Konfiguration: {str(e)}")
            return {}
    
    def _decrypt_config_values(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Entschlüsselt verschlüsselte Werte in der Konfiguration.
        
        Args:
            config: Konfigurationsdaten
            
        Returns:
            Konfiguration mit entschlüsselten Werten
        """
        if not self.encryption_enabled or not self.cipher:
            return config
        
        result = {}
        
        for key, value in config.items():
            if isinstance(value, dict):
                # Rekursiv für verschachtelte Dictionaries
                result[key] = self._decrypt_config_values(value)
            elif isinstance(value, str) and key.endswith("_encrypted"):
                # Verschlüsselten Wert entschlüsseln
                try:
                    # Name ohne _encrypted suffix
                    plain_key = key[:-10]
                    
                    # Base64-decodieren und entschlüsseln
                    encrypted_bytes = base64.urlsafe_b64decode(value)
                    decrypted = self.cipher.decrypt(encrypted_bytes).decode('utf-8')
                    
                    # Als entschlüsselten Wert speichern
                    result[plain_key] = decrypted
                except Exception as e:
                    self.logger.error(f"Fehler beim Entschlüsseln von {key}: {str(e)}")
                    # Original behalten
                    result[key] = value
            else:
                # Unverschlüsselten Wert übernehmen
                result[key] = value
        
        return result
    
    def _encrypt_config_values(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Verschlüsselt sensible Werte in der Konfiguration.
        
        Args:
            config: Konfigurationsdaten
            
        Returns:
            Konfiguration mit verschlüsselten Werten
        """
        if not self.encryption_enabled or not self.cipher:
            return config
        
        result = {}
        
        # Liste sensibler Schlüssel
        sensitive_keys = [
            "password", "secret", "key", "token", "credential",
            "api_key", "access_key", "auth_token", "auth_key"
        ]
        
        for key, value in config.items():
            if isinstance(value, dict):
                # Rekursiv für verschachtelte Dictionaries
                result[key] = self._encrypt_config_values(value)
            elif isinstance(value, str) and any(sensitive in key.lower() for sensitive in sensitive_keys):
                # Sensiblen Wert verschlüsseln
                try:
                    # Verschlüsseln
                    encrypted = self.cipher.encrypt(value.encode('utf-8'))
                    
                    # Als Base64 speichern
                    result[f"{key}_encrypted"] = base64.urlsafe_b64encode(encrypted).decode('ascii')
                except Exception as e:
                    self.logger.error(f"Fehler beim Verschlüsseln von {key}: {str(e)}")
                    # Original behalten
                    result[key] = value
            else:
                # Nicht-sensiblen Wert übernehmen
                result[key] = value
        
        return result
    
    def save_config(self) -> bool:
        """Speichert die Konfiguration in die Datei.
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            # Verschlüsseln, falls aktiviert
            save_config = self.config
            if self.encryption_enabled:
                save_config = self._encrypt_config_values(save_config)
            
            # Verzeichnis erstellen, falls nicht vorhanden
            os.makedirs(os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True)
            
            # Konfiguration speichern
            with open(self.config_path, 'w') as f:
                json.dump(save_config, f, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern der Konfiguration: {str(e)}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Liest einen Konfigurationswert.
        
        Args:
            key: Konfigurationsschlüssel (unterstützt Punktnotation für Verschachtelung)
            default: Standardwert, falls Schlüssel nicht gefunden
            
        Returns:
            Konfigurationswert oder Standardwert
        """
        if not key:
            return default
        
        # Punktnotation für verschachtelte Schlüssel
        parts = key.split('.')
        value = self.config
        
        # Durch die Verschachtelung navigieren
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Setzt einen Konfigurationswert.
        
        Args:
            key: Konfigurationsschlüssel (unterstützt Punktnotation für Verschachtelung)
            value: Zu setzender Wert
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        if not key:
            return False
        
        # Punktnotation für verschachtelte Schlüssel
        parts = key.split('.')
        
        # Bei einfachem Schlüssel
        if len(parts) == 1:
            self.config[key] = value
            return True
        
        # Bei verschachteltem Schlüssel
        current = self.config
        for i, part in enumerate(parts[:-1]):
            # Verschachtelte Dictionaries erstellen, falls nicht vorhanden
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        
        # Letzten Teil setzen
        current[parts[-1]] = value
        return True
    
    def delete(self, key: str) -> bool:
        """Löscht einen Konfigurationswert.
        
        Args:
            key: Konfigurationsschlüssel (unterstützt Punktnotation für Verschachtelung)
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        if not key:
            return False
        
        # Punktnotation für verschachtelte Schlüssel
        parts = key.split('.')
        
        # Bei einfachem Schlüssel
        if len(parts) == 1:
            if key in self.config:
                del self.config[key]
                return True
            return False
        
        # Bei verschachteltem Schlüssel
        current = self.config
        for i, part in enumerate(parts[:-1]):
            if part not in current or not isinstance(current[part], dict):
                return False
            current = current[part]
        
        # Letzten Teil löschen
        if parts[-1] in current:
            del current[parts[-1]]
            return True
        
        return False
```

## Performanceoptimierung

### Ressourcenmanagement

Das Ressourcenmanagement stellt sicher, dass die Plattform Systemressourcen effizient nutzt und sich dynamisch an die Last anpassen kann.

```python
# performance/resource_governor.py
import os
import psutil
import threading
import logging
from typing import Dict, Any, Optional, List, Tuple
import time
import json

class ResourceGovernor:
    """Manager für dynamisches Ressourcenmanagement und Leistungsoptimierung."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert den Ressourcen-Governor mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        self.logger = logging.getLogger("resource_governor")
        
        # Grenzwerte für Ressourcen
        self.max_memory_percent = config.get("max_memory_percent", 80)
        self.target_memory_percent = config.get("target_memory_percent", 70)
        self.max_cpu_percent = config.get("max_cpu_percent", 90)
        self.target_cpu_percent = config.get("target_cpu_percent", 70)
        
        # Ressourcenüberwachungsintervall
        self.monitoring_interval = config.get("monitoring_interval", 5)  # Sekunden
        
        # Adaptive Skalierung
        self.enable_adaptive_scaling = config.get("enable_adaptive_scaling", True)
        self.scaling_cooldown = config.get("scaling_cooldown", 60)  # Sekunden
        self.last_scaling_time = 0
        
        # Worker-Management
        self.min_workers = config.get("min_workers", 2)
        self.max_workers = config.get("max_workers", 8)
        self.current_workers = config.get("initial_workers", 4)
        
        # Batch-Verarbeitungslimits
        self.max_batch_size = config.get("max_batch_size", 100)
        self.target_batch_size = config.get("target_batch_size", 20)
        
        # Ressourcenstatistik
        self.usage_history = {
            "memory": [],
            "cpu": [],
            "timestamp": []
        }
        self.history_size = config.get("history_size", 60)  # 60 Datenpunkte
        
        # Flag für aktive Überwachung
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Überwachung starten
        self.start_monitoring()
    
    def start_monitoring(self):
        """Startet die Ressourcenüberwachung in einem separaten Thread."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("Ressourcenüberwachung gestartet.")
    
    def stop_monitoring(self):
        """Stoppt die Ressourcenüberwachung."""
        if not self.monitoring_active:
            return
        
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10)
        
        self.logger.info("Ressourcenüberwachung gestoppt.")
    
    def _monitoring_loop(self):
        """Hauptschleife für die Ressourcenüberwachung."""
        while self.monitoring_active:
            try:
                # Ressourcennutzung erfassen
                memory_percent = psutil.virtual_memory().percent
                cpu_percent = psutil.cpu_percent(interval=1)
                current_time = time.time()
                
                # Statistik aktualisieren
                self.usage_history["memory"].append(memory_percent)
                self.usage_history["cpu"].append(cpu_percent)
                self.usage_history["timestamp"].append(current_time)
                
                # Historie begrenzen
                if len(self.usage_history["memory"]) > self.history_size:
                    self.usage_history["memory"] = self.usage_history["memory"][-self.history_size:]
                    self.usage_history["cpu"] = self.usage_history["cpu"][-self.history_size:]
                    self.usage_history["timestamp"] = self.usage_history["timestamp"][-self.history_size:]
                
                # Ressourcennutzung protokollieren
                if len(self.usage_history["memory"]) % 12 == 0:  # Alle 12 Zyklen (bei 5s Intervall = 1 Minute)
                    self.logger.info(
                        f"Ressourcennutzung - RAM: {memory_percent:.1f}%, CPU: {cpu_percent:.1f}%, "
                        f"Worker: {self.current_workers}"
                    )
                
                # Adaptive Skalierung
                if self.enable_adaptive_scaling:
                    self._adjust_resources(memory_percent, cpu_percent)
                
                # Pause bis zum nächsten Zyklus
                time.sleep(self.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Fehler in der Ressourcenüberwachung: {str(e)}")
                time.sleep(self.monitoring_interval)
    
    def _adjust_resources(self, memory_percent: float, cpu_percent: float):
        """Passt Ressourcenzuweisungen basierend auf aktueller Nutzung an.
        
        Args:
            memory_percent: Aktuelle RAM-Nutzung in Prozent
            cpu_percent: Aktuelle CPU-Nutzung in Prozent
        """
        current_time = time.time()
        
        # Cooldown prüfen
        if current_time - self.last_scaling_time < self.scaling_cooldown:
            return
        
        # Speicherbasierte Skalierung (höhere Priorität)
        if memory_percent > self.max_memory_percent:
            # Kritische Speichernutzung - Sofortige Reduzierung
            self._scale_down("Kritischer Speichermangel")
            self.last_scaling_time = current_time
            return
        elif memory_percent > self.target_memory_percent:
            # Hohe Speichernutzung - Reduzierung, wenn CPU-Auslastung auch hoch ist
            if cpu_percent > self.target_cpu_percent:
                self._scale_down("Hohe Speicher- und CPU-Nutzung")
                self.last_scaling_time = current_time
                return
        
        # CPU-basierte Skalierung
        if cpu_percent > self.max_cpu_percent:
            # Kritische CPU-Auslastung - Reduzierung
            self._scale_down("Kritische CPU-Auslastung")
            self.last_scaling_time = current_time
            return
        elif cpu_percent > self.target_cpu_percent:
            # Hohe CPU-Auslastung - Reduzierung, wenn Trend steigend ist
            if self._is_trend_increasing("cpu"):
                self._scale_down("Steigende CPU-Auslastung")
                self.last_scaling_time = current_time
                return
        
        # Hochskalierung bei niedriger Auslastung
        if (memory_percent < self.target_memory_percent * 0.8 and 
            cpu_percent < self.target_cpu_percent * 0.8):
            # Niedrige Auslastung - Hochskalieren, wenn Trend stabil oder steigend ist
            if not self._is_trend_decreasing("cpu") and not self._is_trend_decreasing("memory"):
                self._scale_up("Niedrige Ressourcennutzung")
                self.last_scaling_time = current_time
    
    def _scale_up(self, reason: str):
        """Skaliert Ressourcen nach oben.
        
        Args:
            reason: Grund für die Skalierung
        """
        if self.current_workers >= self.max_workers:
            return
        
        self.current_workers = min(self.current_workers + 1, self.max_workers)
        self.logger.info(f"Skalierung nach oben auf {self.current_workers} Worker. Grund: {reason}")
    
    def _scale_down(self, reason: str):
        """Skaliert Ressourcen nach unten.
        
        Args:
            reason: Grund für die Skalierung
        """
        if self.current_workers <= self.min_workers:
            return
        
        self.current_workers = max(self.current_workers - 1, self.min_workers)
        self.logger.info(f"Skalierung nach unten auf {self.current_workers} Worker. Grund: {reason}")
    
    def _is_trend_increasing(self, metric: str) -> bool:
        """Prüft, ob ein Trend steigend ist.
        
        Args:
            metric: Zu prüfende Metrik ('memory' oder 'cpu')
            
        Returns:
            True, wenn der Trend steigend ist, sonst False
        """
        if len(self.usage_history[metric]) < 3:
            return False
        
        # Letzte 3 Messwerte
        recent = self.usage_history[metric][-3:]
        return recent[0] < recent[1] < recent[2]
    
    def _is_trend_decreasing(self, metric: str) -> bool:
        """Prüft, ob ein Trend fallend ist.
        
        Args:
            metric: Zu prüfende Metrik ('memory' oder 'cpu')
            
        Returns:
            True, wenn der Trend fallend ist, sonst False
        """
        if len(self.usage_history[metric]) < 3:
            return False
        
        # Letzte 3 Messwerte
        recent = self.usage_history[metric][-3:]
        return recent[0] > recent[1] > recent[2]
    
    def calculate_optimal_batch_size(self, item_type: str, avg_item_size: int) -> int:
        """Berechnet die optimale Batchgröße basierend auf Ressourcenverfügbarkeit.
        
        Args:
            item_type: Typ der zu verarbeitenden Elemente
            avg_item_size: Durchschnittliche Größe der Elemente in Bytes
            
        Returns:
            Optimale Batchgröße
        """
        # Verfügbarer Speicher
        memory_info = psutil.virtual_memory()
        available_memory = memory_info.available
        
        # Speichermodifikator je nach Elementtyp
        memory_multipliers = {
            "image": 5,       # Bilder benötigen ~5x ihre Größe im Speicher
            "document": 3,    # Dokumente ~3x
            "video_frame": 4, # Videoframes ~4x
            "text": 2         # Text ~2x
        }
        
        multiplier = memory_multipliers.get(item_type, 3)
        
        # Maximal nutzbare Speichermenge (70% des verfügbaren Speichers)
        max_usable_memory = available_memory * 0.7
        
        # Theoretische maximale Batchgröße basierend auf Speicher
        max_memory_batch_size = max_usable_memory / (avg_item_size * multiplier)
        
        # Batchgröße basierend auf CPU-Kernen und aktuellen Workern
        cpu_cores = os.cpu_count() or 4
        max_cpu_batch_size = (cpu_cores / self.current_workers) * self.target_batch_size
        
        # Kleinerer Wert ist limitierend
        optimal_batch_size = min(int(max_memory_batch_size), int(max_cpu_batch_size))
        
        # Mit konfiguriertem Maximum begrenzen
        optimal_batch_size = min(optimal_batch_size, self.max_batch_size)
        
        # Mindestens 1
        return max(1, optimal_batch_size)
    
    def get_current_worker_count(self) -> int:
        """Gibt die aktuelle Anzahl der Worker zurück.
        
        Returns:
            Aktuelle Worker-Anzahl
        """
        return self.current_workers
    
    def get_resource_limits(self) -> Dict[str, Any]:
        """Gibt aktuelle Ressourcenlimits zurück.
        
        Returns:
            Dictionary mit Ressourcenlimits
        """
        # Systeminformationen abrufen
        memory_info = psutil.virtual_memory()
        
        # Limits basierend auf aktueller Systemauslastung berechnen
        return {
            "memory_limit_bytes": int(memory_info.total * self.max_memory_percent / 100),
            "target_memory_bytes": int(memory_info.total * self.target_memory_percent / 100),
            "current_memory_usage_bytes": memory_info.used,
            "current_memory_percent": memory_info.percent,
            "max_batch_size": self.max_batch_size,
            "current_workers": self.current_workers,
            "min_workers": self.min_workers,
            "max_workers": self.max_workers
        }
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Gibt Nutzungsstatistiken zurück.
        
        Returns:
            Dictionary mit Nutzungsstatistiken
        """
        # Durchschnittswerte berechnen
        avg_memory = sum(self.usage_history["memory"]) / len(self.usage_history["memory"]) if self.usage_history["memory"] else 0
        avg_cpu = sum(self.usage_history["cpu"]) / len(self.usage_history["cpu"]) if self.usage_history["cpu"] else 0
        
        # Aktuelle Werte
        current_memory = psutil.virtual_memory().percent
        current_cpu = psutil.cpu_percent(interval=0.1)
        
        return {
            "current": {
                "memory_percent": current_memory,
                "cpu_percent": current_cpu,
                "workers": self.current_workers
            },
            "average": {
                "memory_percent": avg_memory,
                "cpu_percent": avg_cpu
            },
            "history": {
                "memory": self.usage_history["memory"],
                "cpu": self.usage_history["cpu"],
                "timestamp": self.usage_history["timestamp"],
                "samples": len(self.usage_history["memory"])
            }
        }
```

### Caching-Strategien

Die Caching-Strategien verbessern die Leistung durch intelligente Zwischenspeicherung häufig verwendeter Daten und Verarbeitungsergebnisse.

```python
# performance/caching_manager.py
import os
import hashlib
import time
import logging
import json
import pickle
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
import threading
import zlib

class CachingManager:
    """Manager für intelligentes Caching zur Leistungsoptimierung."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialisiert den Caching-Manager mit Konfiguration.
        
        Args:
            config: Konfigurationseinstellungen
        """
        self.config = config
        self.logger = logging.getLogger("caching_manager")
        
        # Cache-Verzeichnis
        self.cache_dir = config.get("cache_dir", "/tmp/vision_ocr_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Cache-Optionen
        self.memory_cache_enabled = config.get("memory_cache_enabled", True)
        self.disk_cache_enabled = config.get("disk_cache_enabled", True)
        self.cache_ttl = config.get("cache_ttl", 3600)  # 1 Stunde
        self.memory_cache_size = config.get("memory_cache_size", 100)  # Anzahl Items
        self.disk_cache_size_mb = config.get("disk_cache_size_mb", 1024)  # 1 GB
        
        # Kompressionsoptionen
        self.enable_compression = config.get("enable_compression", True)
        self.compression_threshold = config.get("compression_threshold", 10240)  # 10 KB
        self.compression_level = config.get("compression_level", 6)  # 1-9, wobei 9 höchste Kompression
        
        # Performance-Statistik
        self.enable_stats = config.get("enable_stats", True)
        self.stats = {
            "memory_hits": 0,
            "memory_misses": 0,
            "disk_hits": 0,
            "disk_misses": 0,
            "evictions": 0,
            "bytes_saved": 0
        }
        
        # Cache-Strukturen
        self.memory_cache = {}
        self.cache_access_times = {}
        self.cache_lock = threading.RLock()
        
        # Cache-Bereinigung in separatem Thread starten
        self.cleanup_interval = config.get("cleanup_interval", 300)  # 5 Minuten
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
    
    def get(self, key: str) -> Optional[Any]:
        """Ruft einen Wert aus dem Cache ab.
        
        Args:
            key: Cache-Schlüssel
            
        Returns:
            Cachedaten oder None, wenn nicht im Cache
        """
        # Cache-Schlüssel hashen
        key_hash = self._hash_key(key)
        
        with self.cache_lock:
            # Zuerst im Speicher-Cache suchen
            if self.memory_cache_enabled and key_hash in self.memory_cache:
                value, expiry = self.memory_cache[key_hash]
                
                # Prüfen, ob abgelaufen
                if expiry > time.time():
                    # Zugriffszeitstempel aktualisieren
                    self.cache_access_times[key_hash] = time.time()
                    
                    # Statistik aktualisieren
                    if self.enable_stats:
                        self.stats["memory_hits"] += 1
                    
                    return value
                else:
                    # Abgelaufenen Eintrag entfernen
                    del self.memory_cache[key_hash]
                    if key_hash in self.cache_access_times:
                        del self.cache_access_times[key_hash]
            
            # Statistik aktualisieren
            if self.memory_cache_enabled and self.enable_stats:
                self.stats["memory_misses"] += 1
            
            # Falls nicht im Speicher oder abgelaufen, auf Disk suchen
            if self.disk_cache_enabled:
                disk_value = self._get_from_disk(key_hash)
                
                if disk_value is not None:
                    # Statistik aktualisieren
                    if self.enable_stats:
                        self.stats["disk_hits"] += 1
                    
                    # In Speicher-Cache einfügen
                    if self.memory_cache_enabled:
                        self._set_in_memory(key_hash, disk_value)
                    
                    return disk_value
                
                # Statistik aktualisieren
                if self.enable_stats:
                    self.stats["disk_misses"] += 1
        
        # Nichts gefunden
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Speichert einen Wert im Cache.
        
        Args:
            key: Cache-Schlüssel
            value: Zu cachender Wert
            ttl: Time-to-Live in Sekunden (None für Standard-TTL)
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        if ttl is None:
            ttl = self.cache_ttl
        
        # Cache-Schlüssel hashen
        key_hash = self._hash_key(key)
        
        try:
            with self.cache_lock:
                # Ablaufzeit berechnen
                expiry = time.time() + ttl
                
                # In Speicher-Cache speichern
                if self.memory_cache_enabled:
                    self._set_in_memory(key_hash, value, expiry)
                
                # Auf Disk speichern
                if self.disk_cache_enabled:
                    self._set_on_disk(key_hash, value, expiry)
                    
                return True
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern im Cache: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Löscht einen Wert aus dem Cache.
        
        Args:
            key: Cache-Schlüssel
            
        Returns:
            True bei Erfolg, False wenn Schlüssel nicht im Cache
        """
        # Cache-Schlüssel hashen
        key_hash = self._hash_key(key)
        
        with self.cache_lock:
            deleted = False
            
            # Aus Speicher-Cache löschen
            if self.memory_cache_enabled and key_hash in self.memory_cache:
                del self.memory_cache[key_hash]
                if key_hash in self.cache_access_times:
                    del self.cache_access_times[key_hash]
                deleted = True
            
            # Aus Disk-Cache löschen
            if self.disk_cache_enabled:
                disk_path = os.path.join(self.cache_dir, key_hash + '.cache')
                if os.path.exists(disk_path):
                    try:
                        os.remove(disk_path)
                        deleted = True
                    except Exception as e:
                        self.logger.error(f"Fehler beim Löschen von Disk-Cache: {str(e)}")
            
            return deleted
    
    def clear(self) -> bool:
        """Löscht den gesamten Cache.
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            with self.cache_lock:
                # Speicher-Cache löschen
                if self.memory_cache_enabled:
                    self.memory_cache = {}
                    self.cache_access_times = {}
                
                # Disk-Cache löschen
                if self.disk_cache_enabled:
                    for filename in os.listdir(self.cache_dir):
                        if filename.endswith('.cache'):
                            try:
                                os.remove(os.path.join(self.cache_dir, filename))
                            except Exception as e:
                                self.logger.error(f"Fehler beim Löschen von {filename}: {str(e)}")
                
                # Statistik zurücksetzen
                if self.enable_stats:
                    self.stats = {
                        "memory_hits": 0,
                        "memory_misses": 0,
                        "disk_hits": 0,
                        "disk_misses": 0,
                        "evictions": 0,
                        "bytes_saved": 0
                    }
                
                return True
        except Exception as e:
            self.logger.error(f"Fehler beim Löschen des Cache: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Gibt Cache-Statistiken zurück.
        
        Returns:
            Dictionary mit Cache-Statistiken
        """
        with self.cache_lock:
            # Aktuelle Cache-Größen berechnen
            memory_items = len(self.memory_cache)
            
            disk_size = 0
            disk_items = 0
            if self.disk_cache_enabled:
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith('.cache'):
                        try:
                            disk_size += os.path.getsize(os.path.join(self.cache_dir, filename))
                            disk_items += 1
                        except:
                            pass
            
            # Trefferrate berechnen
            memory_total = self.stats["memory_hits"] + self.stats["memory_misses"]
            memory_hit_rate = (self.stats["memory_hits"] / memory_total * 100) if memory_total > 0 else 0
            
            disk_total = self.stats["disk_hits"] + self.stats["disk_misses"]
            disk_hit_rate = (self.stats["disk_hits"] / disk_total * 100) if disk_total > 0 else 0
            
            # Gesamtstatistik
            return {
                "memory_cache": {
                    "enabled": self.memory_cache_enabled,
                    "items": memory_items,
                    "max_items": self.memory_cache_size,
                    "hit_rate": memory_hit_rate,
                    "hits": self.stats["memory_hits"],
                    "misses": self.stats["memory_misses"]
                },
                "disk_cache": {
                    "enabled": self.disk_cache_enabled,
                    "items": disk_items,
                    "size_bytes": disk_size,
                    "max_size_bytes": self.disk_cache_size_mb * 1024 * 1024,
                    "hit_rate": disk_hit_rate,
                    "hits": self.stats["disk_hits"],
                    "misses": self.stats["disk_misses"]
                },
                "evictions": self.stats["evictions"],
                "bytes_saved": self.stats["bytes_saved"],
                "compression_enabled": self.enable_compression
            }
    
    def _set_in_memory(self, key_hash: str, value: Any, expiry: Optional[float] = None):
        """Speichert einen Wert im Speicher-Cache.
        
        Args:
            key_hash: Hash des Cache-Schlüssels
            value: Zu cachender Wert
            expiry: Ablaufzeitstempel (optional)
        """
        if not self.memory_cache_enabled:
            return
        
        if expiry is None:
            expiry = time.time() + self.cache_ttl
        
        # Platz freigeben, wenn Cache voll ist
        if len(self.memory_cache) >= self.memory_cache_size:
            self._evict_from_memory()
        
        # In Cache speichern
        self.memory_cache[key_hash] = (value, expiry)
        self.cache_access_times[key_hash] = time.time()
    
    def _evict_from_memory(self):
        """Entfernt den am längsten nicht verwendeten Eintrag aus dem Speicher-Cache."""
        if not self.cache_access_times:
            return
        
        # Ältesten Eintrag finden
        oldest_key = min(self.cache_access_times.items(), key=lambda x: x[1])[0]
        
        # Aus Cache entfernen
        if oldest_key in self.memory_cache:
            del self.memory_cache[oldest_key]
        
        if oldest_key in self.cache_access_times:
            del self.cache_access_times[oldest_key]
        
        # Statistik aktualisieren
        if self.enable_stats:
            self.stats["evictions"] += 1
    
    def _set_on_disk(self, key_hash: str, value: Any, expiry: float):
        """Speichert einen Wert im Disk-Cache.
        
        Args:
            key_hash: Hash des Cache-Schlüssels
            value: Zu cachender Wert
            expiry: Ablaufzeitstempel
        """
        if not self.disk_cache_enabled:
            return
        
        # Cache-Datei erstellen
        cache_file = os.path.join(self.cache_dir, key_hash + '.cache')
        
        # Platz freigeben, wenn Cache-Verzeichnis zu groß wird
        self._check_disk_cache_size()
        
        try:
            # Metadaten und Wert serialisieren
            metadata = {
                "expiry": expiry,
                "created": time.time()
            }
            
            # Wert serialisieren
            value_data = pickle.dumps(value)
            
            # Bei Bedarf komprimieren
            is_compressed = False
            original_size = len(value_data)
            
            if self.enable_compression and original_size > self.compression_threshold:
                try:
                    compressed_data = zlib.compress(value_data, self.compression_level)
                    compressed_size = len(compressed_data)
                    
                    # Nur verwenden, wenn Kompression effektiv ist
                    if compressed_size < original_size * 0.9:  # Mindestens 10% Einsparung
                        value_data = compressed_data
                        is_compressed = True
                        
                        # Statistik aktualisieren
                        if self.enable_stats:
                            self.stats["bytes_saved"] += (original_size - compressed_size)
                except Exception as e:
                    self.logger.warning(f"Komprimierung fehlgeschlagen: {str(e)}")
            
            # Kompressionsinfo zu Metadaten hinzufügen
            metadata["compressed"] = is_compressed
            
            # In Datei speichern
            with open(cache_file, 'wb') as f:
                # Zuerst Metadaten als JSON speichern
                metadata_bytes = json.dumps(metadata).encode('utf-8')
                metadata_length = len(metadata_bytes)
                
                # Metadaten-Länge und dann Metadaten schreiben
                f.write(metadata_length.to_bytes(4, byteorder='little'))
                f.write(metadata_bytes)
                
                # Dann den Wert schreiben
                f.write(value_data)
        
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern im Disk-Cache: {str(e)}")
            
            # Bei Fehler versuchen, die fehlgeschlagene Datei zu löschen
            if os.path.exists(cache_file):
                try:
                    os.remove(cache_file)
                except:
                    pass
    
    def _get_from_disk(self, key_hash: str) -> Optional[Any]:
        """Holt einen Wert aus dem Disk-Cache.
        
        Args:
            key_hash: Hash des Cache-Schlüssels
            
        Returns:
            Cachedaten oder None, wenn nicht im Cache oder abgelaufen
        """
        if not self.disk_cache_enabled:
            return None
        
        # Cache-Datei finden
        cache_file = os.path.join(self.cache_dir, key_hash + '.cache')
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                # Metadaten-Länge lesen
                metadata_length = int.from_bytes(f.read(4), byteorder='little')
                
                # Metadaten lesen und deserialisieren
                metadata_bytes = f.read(metadata_length)
                metadata = json.loads(metadata_bytes.decode('utf-8'))
                
                # Ablaufzeit prüfen
                if metadata.get("expiry", 0) < time.time():
                    # Abgelaufenen Eintrag löschen
                    try:
                        os.remove(cache_file)
                    except:
                        pass
                    return None
                
                # Wert lesen
                value_data = f.read()
                
                # Bei Bedarf dekomprimieren
                if metadata.get("compressed", False):
                    try:
                        value_data = zlib.decompress(value_data)
                    except Exception as e:
                        self.logger.error(f"Dekomprimierung fehlgeschlagen: {str(e)}")
                        return None
                
                # Wert deserialisieren
                return pickle.loads(value_data)
        
        except Exception as e:
            self.logger.error(f"Fehler beim Lesen aus Disk-Cache: {str(e)}")
            return None
    
    def _check_disk_cache_size(self):
        """Überprüft die Größe des Disk-Cache und räumt bei Bedarf auf."""
        if not self.disk_cache_enabled:
            return
        
        # Gesamtgröße berechnen
        total_size = 0
        file_info = []
        
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.cache'):
                continue
            
            file_path = os.path.join(self.cache_dir, filename)
            try:
                file_size = os.path.getsize(file_path)
                file_mtime = os.path.getmtime(file_path)
                total_size += file_size
                
                # Dateiinformationen für Sortierung speichern
                file_info.append((file_path, file_size, file_mtime))
            except:
                continue
        
        # Maximale Cache-Größe in Bytes
        max_size = self.disk_cache_size_mb * 1024 * 1024
        
        # Wenn Cache zu groß ist, älteste Dateien löschen
        if total_size > max_size:
            # Nach Änderungszeit sortieren (älteste zuerst)
            file_info.sort(key=lambda x: x[2])
            
            # Dateien löschen, bis Größe unter dem Limit liegt
            for file_path, file_size, _ in file_info:
                try:
                    os.remove(file_path)
                    total_size -= file_size
                    
                    # Statistik aktualisieren
                    if self.enable_stats:
                        self.stats["evictions"] += 1
                    
                    if total_size <= max_size * 0.8:  # 20% Puffer
                        break
                except:
                    continue
    
    def _cleanup_loop(self):
        """Hintergrund-Schleife zur regelmäßigen Cache-Bereinigung."""
        while True:
            try:
                # Cache-Statistik protokollieren
                if self.enable_stats:
                    stats = self.get_stats()
                    memory_usage = f"{stats['memory_cache']['items']}/{stats['memory_cache']['max_items']}"
                    disk_usage = f"{stats['disk_cache']['size_bytes']/1024/1024:.1f}MB/{stats['disk_cache']['max_size_bytes']/1024/1024:.1f}MB"
                    self.logger.info(f"Cache-Status - Memory: {memory_usage}, Disk: {disk_usage}, Hit-Raten: Memory {stats['memory_cache']['hit_rate']:.1f}%, Disk {stats['disk_cache']['hit_rate']:.1f}%")
                
                # Abgelaufene Einträge aus dem Speicher-Cache entfernen
                with self.cache_lock:
                    current_time = time.time()
                    expired_keys = []
                    
                    for key, (_, expiry) in self.memory_cache.items():
                        if expiry < current_time:
                            expired_keys.append(key)
                    
                    for key in expired_keys:
                        if key in self.memory_cache:
                            del self.memory_cache[key]
                        if key in self.cache_access_times:
                            del self.cache_access_times[key]
                
                # Abgelaufene Einträge aus dem Disk-Cache entfernen
                if self.disk_cache_enabled:
                    for filename in os.listdir(self.cache_dir):
                        if not filename.endswith('.cache'):
                            continue
                        
                        cache_file = os.path.join(self.cache_dir, filename)
                        try:
                            with open(cache_file, 'rb') as f:
                                # Metadaten-Länge lesen
                                metadata_length = int.from_bytes(f.read(4), byteorder='little')
                                
                                # Metadaten lesen und deserialisieren
                                metadata_bytes = f.read(metadata_length)
                                metadata = json.loads(metadata_bytes.decode('utf-8'))
                                
                                # Ablaufzeit prüfen
                                if metadata.get("expiry", 0) < current_time:
                                    # Abgelaufenen Eintrag löschen
                                    os.remove(cache_file)
                        except:
                            # Bei Fehler, beschädigte Datei löschen
                            try:
                                os.remove(cache_file)
                            except:
                                pass
            except Exception as e:
                self.logger.error(f"Fehler in der Cache-Bereinigung: {str(e)}")
            
            # Pause bis zum nächsten Zyklus
            time.sleep(self.cleanup_interval)
    
    def _hash_key(self, key: str) -> str:
        """Generiert einen Hash für den Cache-Schlüssel.
        
        Args:
            key: Cache-Schlüssel
            
        Returns:
            MD5-Hash des Schlüssels
        """
        return hashlib.md5(key.encode('utf-8')).hexdigest()
```

## Deployment-Anleitung

### Infrastruktur mit Rancher einrichten

```markdown
# Rancher-Einrichtung für Universal Vision & OCR Processing Platform

Die Universal Vision & OCR Processing Platform nutzt Rancher für die Verwaltung der Kubernetes-Cluster und die Orchestrierung der Container-Workloads. Diese Anleitung führt durch die Einrichtung der Rancher-basierten Infrastruktur.

## 1. Voraussetzungen

- Mindestens 3 Server für die Kubernetes-Controlplane-Nodes (jeweils 4 CPU, 8GB RAM)
- Mindestens 3 Server für Worker-Nodes (jeweils 8 CPU, 16GB RAM, 100GB SSD)
- 1 Server für Rancher (4 CPU, 8GB RAM)
- NFS- oder andere Storage-Lösungen für persistente Volumes
- Netzwerkzugriff zwischen allen Knoten und zu externen Paketquellen

## 2. Rancher-Installation

### 2.1 Docker auf dem Rancher-Server installieren

```bash
# System aktualisieren
sudo apt-get update
sudo apt-get upgrade -y

# Docker-Abhängigkeiten installieren
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Docker GPG-Schlüssel hinzufügen
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Docker installieren
sudo apt-get update
sudo apt-get install -y docker-ce

# Docker-Dienst konfigurieren
sudo systemctl enable docker
sudo systemctl start docker
```

### 2.2 Rancher mit Docker installieren

```bash
# Persistentes Volumen für Rancher erstellen
sudo mkdir -p /opt/rancher

# Rancher über Docker starten
sudo docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  -v /opt/rancher:/var/lib/rancher \
  --privileged \
  rancher/rancher:v2.7.0
```

### 2.3 Rancher-Benutzeroberfläche einrichten

1. Öffnen Sie die Rancher-UI im Browser: `https://RANCHER_SERVER_IP`
2. Setzen Sie ein sicheres Passwort für den Admin-Benutzer
3. Akzeptieren Sie das selbstsignierte Zertifikat oder konfigurieren Sie ein eigenes

## 3. Kubernetes-Cluster erstellen

### 3.1 RKE-Cluster über Rancher UI erstellen

1. Navigieren Sie zu "Cluster Management" > "Create Cluster"
2. Wählen Sie "Custom" als Cluster-Typ
3. Geben Sie einen Namen für den Cluster ein (z.B. "vision-ocr-production")
4. Konfigurieren Sie die Kubernetes-Version (empfohlen: v1.25.x oder höher)

### 3.2 Node-Pools konfigurieren

Für einen Produktionscluster empfehlen wir folgende Konfiguration:

1. **etcd-Nodes**:
   - Anzahl: 3 Nodes
   - Rolle: etcd
   - Ressourcen: 4 CPU, 8GB RAM, 50GB SSD

2. **Controlplane-Nodes**:
   - Anzahl: 3 Nodes
   - Rolle: controlplane
   - Ressourcen: 4 CPU, 8GB RAM

3. **Worker-Nodes für Vision-Verarbeitung**:
   - Anzahl: 3+ Nodes
   - Rolle: worker
   - Label: `node-type=vision`
   - Ressourcen: 8+ CPU, 16GB+ RAM, GPU (optional für verbesserte Leistung)

4. **Worker-Nodes für OCR-Verarbeitung**:
   - Anzahl: 3+ Nodes
   - Rolle: worker
   - Label: `node-type=ocr`
   - Ressourcen: 8+ CPU, 16GB+ RAM

5. **Worker-Nodes für allgemeine Workloads**:
   - Anzahl: 2+ Nodes
   - Rolle: worker
   - Label: `node-type=general`
   - Ressourcen: 4+ CPU, 8GB+ RAM

### 3.3 Netzwerk-Konfiguration

1. Wählen Sie Calico als Netzwerk-Provider
2. Passen Sie den Pod-CIDR und Service-CIDR nach Bedarf an
3. Aktivieren Sie Network Policy für erhöhte Sicherheit

### 3.4 Cloud-Provider Konfiguration (optional)

Falls Sie in der Cloud (AWS, GCP, Azure) arbeiten, konfigurieren Sie den entsprechenden Cloud-Provider, um Cloud-Ressourcen (Load Balancer, persistente Volumes) nutzen zu können.

## 4. Storage-Konfiguration

### 4.1 Storage Classes einrichten

Navigieren Sie zu "Storage" > "StorageClasses" und erstellen Sie folgende Storage Classes:

1. **Standard-Storage** (für allgemeine Daten):
   ```yaml
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: standard
   provisioner: kubernetes.io/no-provisioner
   volumeBindingMode: WaitForFirstConsumer
   ```

2. **Fast-Storage** (für Datenbanken und Cache):
   ```yaml
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: fast
   provisioner: kubernetes.io/no-provisioner
   volumeBindingMode: WaitForFirstConsumer
   ```

### 4.2 Persistente Volumes für Modelle konfigurieren

Die Plattform benötigt Speicherplatz für KI-Modelle. Erstellen Sie ein persistentes Volume:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: models-pv
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  nfs:
    server: NFS_SERVER_IP
    path: /path/to/models
```

## 5. Container-Registry einrichten

### 5.1 Harbor Registry für Anwendungs-Images

1. Navigieren Sie zu "Apps" > "Charts"
2. Suchen und installieren Sie Harbor

Konfigurationsempfehlungen:
```yaml
expose:
  type: ingress
  tls:
    enabled: true
persistence:
  enabled: true
  persistentVolumeClaim:
    registry:
      size: 50Gi
externalURL: https://harbor.your-domain.com
```

### 5.2 Zugriffstoken und Registry-Secret erstellen

```bash
# Secret für Registry-Zugriff erstellen
kubectl create secret docker-registry harbor-registry-secret \
  --namespace vision-ocr-system \
  --docker-server=harbor.your-domain.com \
  --docker-username=admin \
  --docker-password=your-password \
  --docker-email=admin@your-domain.com
```

## 6. Monitoring und Logging

### 6.1 Rancher Monitoring-Operator installieren

1. Navigieren Sie zu "Apps" > "Charts"
2. Suchen und installieren Sie "Monitoring"

Konfigurationsempfehlungen:
```yaml
prometheus:
  retention: 10d
  resources:
    limits:
      memory: 2Gi
grafana:
  persistence:
    enabled: true
    size: 10Gi
alertmanager:
  enabled: true
```

### 6.2 Rancher Logging-Operator installieren

1. Navigieren Sie zu "Apps" > "Charts" 
2. Suchen und installieren Sie "Logging"

Konfigurieren Sie Fluentd oder Fluent Bit für die Protokollerfassung und -weiterleitung:
```yaml
fluentd:
  enabled: true
  persistence:
    enabled: true
    size: 10Gi
```

## 7. Backup-Konfiguration

### 7.1 Velero für Cluster-Backups installieren

1. Navigieren Sie zu "Apps" > "Charts"
2. Suchen und installieren Sie "Velero"

Konfigurationsbeispiel mit S3-kompatiblem Speicher:
```yaml
configuration:
  provider: aws
  backupStorageLocation:
    name: default
    bucket: backup-bucket
    prefix: velero
    config:
      region: us-east-1
      s3ForcePathStyle: true
      s3Url: http://minio.default.svc:9000
```

### 7.2 Backup-Plan einrichten

Erstellen Sie einen Backup-Plan für regelmäßige Backups:

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 0 * * *"
  template:
    includedNamespaces:
      - vision-ocr-system
    includedResources:
      - deployments
      - statefulsets
      - configmaps
      - secrets
      - persistentvolumeclaims
    ttl: 720h
```

## 8. Abschluss und nächste Schritte

Nach Abschluss dieser Einrichtung verfügen Sie über eine leistungsfähige Kubernetes-Plattform, die über Rancher verwaltet wird und bereit für die Bereitstellung der Universal Vision & OCR Processing Platform ist.

Als nächstes:

1. Richten Sie CI/CD-Pipelines zur Automatisierung von Builds und Deployments ein
2. Konfigurieren Sie die Namespaces und Zugriffsberechtigungen
3. Deployen Sie die Vision- und OCR-Komponenten mit Ansible (siehe Abschnitt "Automatisierung mit Ansible")
```

### Automatisierung mit Ansible

```markdown
# Ansible-Automatisierung für die Universal Vision & OCR Processing Platform

Die Plattform verwendet Ansible für die automatisierte Konfiguration und das Deployment. Diese Anleitung erklärt, wie Sie Ansible einrichten und für dynamische Konfigurationen und Container-interne Anpassungen nutzen.

## 1. Ansible-Umgebung einrichten

### 1.1 Ansible auf dem Admin-Workstation installieren

```bash
# System aktualisieren
sudo apt-get update

# Ansible und benötigte Pakete installieren
sudo apt-get install -y ansible python3-pip git

# Benötigte Python-Module installieren
pip3 install kubernetes openshift jmespath pyyaml

# Ansible-Galaxy-Sammlungen installieren
ansible-galaxy collection install kubernetes.core
ansible-galaxy collection install community.kubernetes
ansible-galaxy collection install community.docker
```

### 1.2 Verzeichnisstruktur für Ansible-Konfiguration erstellen

```bash
# Verzeichnisstruktur erstellen
mkdir -p vision-ocr-ansible/inventory
mkdir -p vision-ocr-ansible/group_vars
mkdir -p vision-ocr-ansible/host_vars
mkdir -p vision-ocr-ansible/roles
mkdir -p vision-ocr-ansible/templates
mkdir -p vision-ocr-ansible/playbooks
mkdir -p vision-ocr-ansible/vars

# In das Projektverzeichnis wechseln
cd vision-ocr-ansible
```

### 1.3 Ansible-Konfigurationsdatei erstellen

Erstellen Sie eine `ansible.cfg` im Hauptverzeichnis:

```ini
[defaults]
inventory = ./inventory
roles_path = ./roles
host_key_checking = False
retry_files_enabled = False
jinja2_extensions = jinja2.ext.do
callback_whitelist = profile_tasks, timer
stdout_callback = yaml
bin_ansible_callbacks = True
deprecation_warnings = False

[privilege_escalation]
become = False

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o UserKnownHostsFile=/dev/null
pipelining = True
```

## 2. Inventar und Variablen konfigurieren

### 2.1 Erstellen Sie das Inventory für verschiedene Umgebungen

Erstellen Sie die Datei `inventory/hosts.yml`:

```yaml
all:
  children:
    kubernetes:
      children:
        production:
          hosts:
            k8s-prod:
              ansible_connection: local
              context: vision-ocr-production
        staging:
          hosts:
            k8s-staging:
              ansible_connection: local
              context: vision-ocr-staging
        development:
          hosts:
            k8s-dev:
              ansible_connection: local
              context: vision-ocr-development
```

### 2.2 Umgebungsspezifische Variablen konfigurieren

Erstellen Sie Dateien für jede Umgebung:

**group_vars/production.yml**:
```yaml
env: production
namespace: vision-ocr-system
replicas:
  vision_module: 3
  ocr_engine: 4
  api_gateway: 2
  worker: 6
resources:
  vision_module:
    cpu_request: "2"
    memory_request: "4Gi"
    cpu_limit: "4"
    memory_limit: "8Gi"
  ocr_engine:
    cpu_request: "2"
    memory_request: "4Gi"
    cpu_limit: "4"
    memory_limit: "8Gi"
storage:
  models_pvc_size: "50Gi"
  data_pvc_size: "100Gi"
registry_url: "harbor.example.com/vision-ocr"
ingress:
  host: "api.vision-ocr.example.com"
  tls_secret: "vision-ocr-tls"
monitoring:
  enabled: true
```

**group_vars/staging.yml**:
```yaml
env: staging
namespace: vision-ocr-staging
replicas:
  vision_module: 2
  ocr_engine: 2
  api_gateway: 1
  worker: 3
resources:
  vision_module:
    cpu_request: "1"
    memory_request: "2Gi"
    cpu_limit: "2"
    memory_limit: "4Gi"
  ocr_engine:
    cpu_request: "1"
    memory_request: "2Gi"
    cpu_limit: "2"
    memory_limit: "4Gi"
storage:
  models_pvc_size: "20Gi"
  data_pvc_size: "50Gi"
registry_url: "harbor.example.com/vision-ocr"
ingress:
  host: "api-staging.vision-ocr.example.com"
  tls_secret: "vision-ocr-staging-tls"
monitoring:
  enabled: true
```

**group_vars/development.yml**:
```yaml
env: development
namespace: vision-ocr-dev
replicas:
  vision_module: 1
  ocr_engine: 1
  api_gateway: 1
  worker: 2
resources:
  vision_module:
    cpu_request: "500m"
    memory_request: "1Gi"
    cpu_limit: "1"
    memory_limit: "2Gi"
  ocr_engine:
    cpu_request: "500m"
    memory_request: "1Gi"
    cpu_limit: "1"
    memory_limit: "2Gi"
storage:
  models_pvc_size: "10Gi"
  data_pvc_size: "20Gi"
registry_url: "harbor.example.com/vision-ocr"
ingress:
  host: "api-dev.vision-ocr.example.com"
  tls_secret: "vision-ocr-dev-tls"
monitoring:
  enabled: false
```

### 2.3 Komponenten-Versionen definieren

Erstellen Sie `vars/component_versions.yml`:

```yaml
component_versions:
  vision_module: "1.0.0"
  ocr_engine: "1.0.0"
  api_gateway: "1.0.0"
  worker: "1.0.0"
  multi_output_processor: "1.0.0"
  speech_module: "1.0.0"
  spatial_analysis: "1.0.0"
```

## 3. Dynamische YAML-Generierung für Kubernetes

### 3.1 Templates für Kubernetes-Ressourcen

Erstellen Sie Templates für Kubernetes-Manifeste:

**templates/namespace.yml.j2**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: {{ namespace }}
  labels:
    app: vision-ocr
    environment: {{ env }}
```

**templates/vision-module-deployment.yml.j2**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vision-module
  namespace: {{ namespace }}
  labels:
    app: vision-ocr
    component: vision-module
    environment: {{ env }}
spec:
  replicas: {{ replicas.vision_module }}
  selector:
    matchLabels:
      app: vision-ocr
      component: vision-module
  template:
    metadata:
      labels:
        app: vision-ocr
        component: vision-module
    spec:
      containers:
      - name: vision-module
        image: {{ registry_url }}/vision-module:{{ component_versions.vision_module }}
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: {{ resources.vision_module.cpu_request }}
            memory: {{ resources.vision_module.memory_request }}
          limits:
            cpu: {{ resources.vision_module.cpu_limit }}
            memory: {{ resources.vision_module.memory_limit }}
        env:
        - name: ENVIRONMENT
          value: {{ env }}
        - name: LOG_LEVEL
          value: {% if env == 'development' %}DEBUG{% else %}INFO{% endif %}
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: models-volume
          mountPath: /app/models
      initContainers:
      - name: config-init
        image: {{ registry_url }}/ansible-init:latest
        command: ['ansible-playbook', 'container-setup.yml']
        env:
        - name: COMPONENT_TYPE
          value: vision-module
        - name: CONFIG_VERSION
          value: "{{ component_versions.vision_module }}"
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: ansible-volume
          mountPath: /ansible
      volumes:
      - name: config-volume
        emptyDir: {}
      - name: models-volume
        persistentVolumeClaim:
          claimName: models-pvc
      - name: ansible-volume
        configMap:
          name: ansible-scripts
      imagePullSecrets:
      - name: harbor-registry-secret
      nodeSelector:
        node-type: vision
```

Ähnliche Templates erstellen Sie für die anderen Komponenten.

### 3.2 Hauptplaybook für das Deployment

Erstellen Sie `playbooks/deploy.yml`:

```yaml
---
- name: Deploy Vision OCR Platform
  hosts: "{{ target_env | default('development') }}"
  gather_facts: false
  vars_files:
    - "../vars/component_versions.yml"
  tasks:
    - name: Create target directory for generated manifests
      file:
        path: "generated_manifests/{{ env }}"
        state: directory
        mode: '0755'
      delegate_to: localhost

    - name: Generate namespace manifest
      template:
        src: ../templates/namespace.yml.j2
        dest: "generated_manifests/{{ env }}/00-namespace.yml"
      delegate_to: localhost

    - name: Generate storage manifests
      template:
        src: "../templates/{{ item }}.yml.j2"
        dest: "generated_manifests/{{ env }}/01-{{ item }}.yml"
      loop:
        - persistent-volumes
        - persistent-volume-claims
      delegate_to: localhost

    - name: Generate ConfigMaps and Secrets
      template:
        src: "../templates/{{ item }}.yml.j2"
        dest: "generated_manifests/{{ env }}/02-{{ item }}.yml"
      loop:
        - configmaps
        - secrets
      delegate_to: localhost

    - name: Generate Deployment manifests
      template:
        src: "../templates/{{ item }}-deployment.yml.j2"
        dest: "generated_manifests/{{ env }}/03-{{ item }}-deployment.yml"
      loop:
        - vision-module
        - ocr-engine
        - api-gateway
        - worker
      delegate_to: localhost

    - name: Generate Service manifests
      template:
        src: "../templates/{{ item }}-service.yml.j2"
        dest: "generated_manifests/{{ env }}/04-{{ item }}-service.yml"
      loop:
        - vision-module
        - ocr-engine
        - api-gateway
      delegate_to: localhost

    - name: Generate Ingress manifest
      template:
        src: "../templates/ingress.yml.j2"
        dest: "generated_manifests/{{ env }}/05-ingress.yml"
      delegate_to: localhost

    - name: Apply Kubernetes manifests
      kubernetes.core.k8s:
        state: present
        src: "generated_manifests/{{ env }}/{{ item }}"
        context: "{{ context }}"
      loop:
        - 00-namespace.yml
        - 01-persistent-volumes.yml
        - 01-persistent-volume-claims.yml
        - 02-configmaps.yml
        - 02-secrets.yml
        - 03-vision-module-deployment.yml
        - 03-ocr-engine-deployment.yml
        - 03-api-gateway-deployment.yml
        - 03-worker-deployment.yml
        - 04-vision-module-service.yml
        - 04-ocr-engine-service.yml
        - 04-api-gateway-service.yml
        - 05-ingress.yml
      when: apply_manifests | default(true) | bool
```

## 4. Container-interne Konfiguration mit Ansible

### 4.1 Ansible-Init-Container

Erstellen Sie ein Dockerfile für den Init-Container:

```dockerfile
FROM python:3.9-slim

# Benötigte Pakete installieren
RUN apt-get update && apt-get install -y \
    ansible \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Standardkonfiguration für Ansible
COPY ansible.cfg /etc/ansible/ansible.cfg

# Arbeitsverzeichnis
WORKDIR /ansible

# Playbooks und Rollen kopieren
COPY playbooks/ /ansible/playbooks/
COPY roles/ /ansible/roles/
COPY templates/ /ansible/templates/

# Entrypoint-Skript
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

### 4.2 Container-Setup-Playbook

Erstellen Sie `playbooks/container-setup.yml`:

```yaml
---
- name: Container-interne Konfiguration
  hosts: localhost
  connection: local
  vars:
    component_type: "{{ lookup('env', 'COMPONENT_TYPE') }}"
    config_version: "{{ lookup('env', 'CONFIG_VERSION') }}"
  tasks:
    - name: Include component-specific variables
      include_vars:
        file: "/ansible/config/{{ component_type }}-vars.yml"

    - name: Konfigurationsdateien erstellen
      template:
        src: "/ansible/templates/{{ component_type }}/{{ item.src }}"
        dest: "/app/config/{{ item.dest }}"
        mode: "{{ item.mode | default('0644') }}"
      loop: "{{ config_files }}"

    - name: Modell-Verzeichnisse erstellen
      file:
        path: "/app/models/{{ item.path }}"
        state: directory
        mode: '0755'
      loop: "{{ model_directories | default([]) }}"
      when: model_directories is defined

    - name: Modellabhängigkeiten herunterladen (falls konfiguriert)
      get_url:
        url: "{{ item.url }}"
        dest: "/app/models/{{ item.path }}"
        mode: '0644'
        checksum: "{{ item.checksum | default(omit) }}"
      loop: "{{ model_files | default([]) }}"
      when: model_files is defined and download_models | default(false) | bool
```

### 4.3 Beispielkonfiguration für Vision-Modul

Erstellen Sie die Datei `templates/vision-module/config.json.j2`:

```json
{
  "models_dir": "/app/models/vision",
  "enable_gpu": {{ enable_gpu | default(false) | lower }},
  "confidence_threshold": {{ confidence_threshold | default(0.5) }},
  "tracker_type": "{{ tracker_type | default('CSRT') }}",
  "detection_model": "{{ detection_model | default('yolo') }}",
  "yolo_version": "{{ yolo_version | default('yolov4') }}",
  "camera_index": {{ camera_index | default(0) }},
  "enable_morphological": {{ enable_morphological | default(true) | lower }},
  "enable_perspective_correction": {{ enable_perspective_correction | default(true) | lower }},
  "denoising_strength": {{ denoising_strength | default(10) }}
}
```

## 5. Automatisierung von Deployments mit GitLab CI/CD

### 5.1 GitLab CI/CD-Konfiguration

Erstellen Sie `.gitlab-ci.yml` im Hauptverzeichnis Ihres Projekts:

```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_REGISTRY: harbor.example.com/vision-ocr
  KUBE_CONFIG: ${KUBE_CONFIG_DATA}

# Build-Jobs für Container-Images
build-vision-module:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - docker login -u $REGISTRY_USER -p $REGISTRY_PASSWORD $DOCKER_REGISTRY
    - docker build -t $DOCKER_REGISTRY/vision-module:$CI_COMMIT_SHORT_SHA -f docker/vision-module/Dockerfile .
    - docker tag $DOCKER_REGISTRY/vision-module:$CI_COMMIT_SHORT_SHA $DOCKER_REGISTRY/vision-module:latest
    - docker push $DOCKER_REGISTRY/vision-module:$CI_COMMIT_SHORT_SHA
    - docker push $DOCKER_REGISTRY/vision-module:latest
  only:
    changes:
      - vision/**/*
      - docker/vision-module/**/*

# Weitere Build-Jobs für andere Komponenten...

# Test-Jobs
test-vision-module:
  stage: test
  image: python:3.9
  script:
    - pip install pytest pytest-cov
    - cd vision
    - python -m pytest --cov=.
  only:
    changes:
      - vision/**/*

# Deployment-Jobs
deploy-dev:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - mkdir -p ~/.kube
    - echo "$KUBE_CONFIG" | base64 -d > ~/.kube/config
    - chmod 600 ~/.kube/config
    - cd ansible
    - pip install ansible kubernetes openshift jinja2
    - ansible-galaxy collection install kubernetes.core
    - ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "target_env=development component_versions.vision_module=$CI_COMMIT_SHORT_SHA"
  environment:
    name: development
  only:
    - develop

deploy-staging:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - mkdir -p ~/.kube
    - echo "$KUBE_CONFIG" | base64 -d > ~/.kube/config
    - chmod 600 ~/.kube/config
    - cd ansible
    - pip install ansible kubernetes openshift jinja2
    - ansible-galaxy collection install kubernetes.core
    - ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "target_env=staging component_versions.vision_module=$CI_COMMIT_SHORT_SHA"
  environment:
    name: staging
  only:
    - staging

deploy-production:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - mkdir -p ~/.kube
    - echo "$KUBE_CONFIG" | base64 -d > ~/.kube/config
    - chmod 600 ~/.kube/config
    - cd ansible
    - pip install ansible kubernetes openshift jinja2
    - ansible-galaxy collection install kubernetes.core
    - ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "target_env=production component_versions.vision_module=$CI_COMMIT_SHORT_SHA"
  environment:
    name: production
  when: manual
  only:
    - master
```

## 6. Ansible-Anwendung für gesamte Plattform

### 6.1 Installation der gesamten Plattform

```bash
# Deployment in der Entwicklungsumgebung
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "target_env=development"

# Deployment in der Staging-Umgebung
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "target_env=staging"

# Deployment in der Produktionsumgebung
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "target_env=production"
```

### 6.2 Nur Konfiguration aktualisieren

```bash
# Nur Konfigurationen aktualisieren ohne Neustart der Pods
ansible-playbook -i inventory/hosts.yml playbooks/update_config.yml -e "target_env=production"
```

### 6.3 Plattformupgrades durchführen

```bash
# Komponenten-Upgrades mit neuen Versionen
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "target_env=production component_versions.vision_module=1.1.0 component_versions.ocr_engine=1.2.0"
```

## 7. Kontinuierliche Überwachung und Wartung

Erstellen Sie ein Playbook für die Überwachung und Wartung:

```yaml
---
- name: System-Wartung
  hosts: "{{ target_env | default('production') }}"
  gather_facts: false
  tasks:
    - name: Ressourcennutzung prüfen
      kubernetes.core.k8s_info:
        kind: Pod
        namespace: "{{ namespace }}"
        context: "{{ context }}"
      register: pods

    - name: Pod-Status anzeigen
      debug:
        msg: "Pod {{ item.metadata.name }} ist {{ item.status.phase }}"
      loop: "{{ pods.resources }}"

    - name: Nach veralteten Konfigurationen suchen
      kubernetes.core.k8s_info:
        kind: ConfigMap
        namespace: "{{ namespace }}"
        context: "{{ context }}"
      register: configmaps

    - name: Prüfen, ob Updates verfügbar sind
      uri:
        url: "{{ registry_url }}/versions"
        method: GET
        return_content: yes
      register: versions_check
      ignore_errors: yes

    - name: Zeige verfügbare Updates an
      debug:
        msg: "Neue Version verfügbar für {{ item.key }}: {{ item.value }}"
      loop: "{{ versions_check.json | default({}) | dict2items }}"
      when: 
        - versions_check is succeeded
        - item.value is version(component_versions[item.key], '>')
```

Mit diesem umfassenden Ansible-Setup haben Sie eine vollständig automatisierte Infrastruktur für die Bereitstellung, Konfiguration und Wartung der Universal Vision & OCR Processing Platform.
```

### Hochverfügbarkeits-Konfiguration

```markdown
# Hochverfügbarkeits-Konfiguration für die Vision & OCR Platform

Diese Anleitung beschreibt die Konfiguration einer hochverfügbaren Produktionsumgebung für die Universal Vision & OCR Processing Platform.

## 1. Architekturüberblick für Hochverfügbarkeit

Die hochverfügbare Architektur besteht aus folgenden Komponenten:

- Multi-AZ Kubernetes-Cluster mit mindestens 3 Availability Zones (AZs)
- Redundante API-Gateway-Instanzen mit Load Balancer
- Horizontale Pod-Autoskalierung (HPA) für alle Workload-Komponenten
- Pod-Disruption-Budgets für kontrollierte Wartung
- Anti-Affinity-Regeln für Knotenverteilung
- Selbstheilende Cluster-Konfiguration

## 2. Multi-AZ Kubernetes-Cluster

### 2.1 Knotendefinition für Multi-AZ

Für jede AZ sollte ein eigener Knotenpool mit folgendem Label definiert werden:

```yaml
apiVersion: cluster.x-k8s.io/v1beta1
kind: MachineDeployment
metadata:
  name: vision-ocr-worker-az1
  namespace: vision-ocr-system
spec:
  replicas: 3
  selector:
    matchLabels:
      node-pool: vision-ocr-worker
      failure-domain: az1
  template:
    spec:
      bootstrap:
        configRef:
          name: vision-ocr-worker-bootstrap
          namespace: vision-ocr-system
      infrastructureRef:
        name: vision-ocr-worker-infra
        namespace: vision-ocr-system
      labels:
        node-pool: vision-ocr-worker
        failure-domain: az1
        node-type: vision
```

Wiederholen Sie dies für `az2` und `az3`.

### 2.2 Pod-Anti-Affinity-Regeln

Um sicherzustellen, dass Pods auf verschiedene Knoten verteilt werden, fügen Sie Anti-Affinity-Regeln hinzu:

```yaml
spec:
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: component
                operator: In
                values:
                - vision-module
            topologyKey: "kubernetes.io/hostname"
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: component
                  operator: In
                  values:
                  - vision-module
              topologyKey: "failure-domain.beta.kubernetes.io/zone"
```

### 2.3 Ressourcen für Multi-AZ-Konfiguration

Erstellen Sie die Datei `templates/multi-az-config.yml.j2`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ component_name }}
  namespace: {{ namespace }}
spec:
  replicas: {{ replicas }}
  selector:
    matchLabels:
      app: vision-ocr
      component: {{ component_name }}
  template:
    metadata:
      labels:
        app: vision-ocr
        component: {{ component_name }}
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: component
                operator: In
                values:
                - {{ component_name }}
            topologyKey: "kubernetes.io/hostname"
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: component
                  operator: In
                  values:
                  - {{ component_name }}
              topologyKey: "failure-domain.beta.kubernetes.io/zone"
      containers:
      - name: {{ component_name }}
        image: {{ registry_url }}/{{ component_name }}:{{ component_version }}
        resources:
          requests:
            cpu: {{ resources.cpu_request }}
            memory: {{ resources.memory_request }}
          limits:
            cpu: {{ resources.cpu_limit }}
            memory: {{ resources.memory_limit }}
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 10
```

## 3. Horizontale Pod-Autoskalierung (HPA)

### 3.1 HPA-Definition für Komponenten

Erstellen Sie die Datei `templates/hpa.yml.j2`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ component_name }}
  namespace: {{ namespace }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ component_name }}
  minReplicas: {{ hpa.min_replicas }}
  maxReplicas: {{ hpa.max_replicas }}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{ hpa.cpu_target }}
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        ```yaml
        averageUtilization: {{ hpa.memory_target }}
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 600
      policies:
      - type: Percent
        value: 10
        periodSeconds: 300
```

### 3.2 HPA-Konfiguration für jede Komponente

Fügen Sie die HPA-Konfigurationsparameter in `group_vars/production.yml` hinzu:

```yaml
hpa:
  vision_module:
    min_replicas: 3
    max_replicas: 10
    cpu_target: 70
    memory_target: 80
  ocr_engine:
    min_replicas: 4
    max_replicas: 12
    cpu_target: 70
    memory_target: 80
  api_gateway:
    min_replicas: 2
    max_replicas: 8
    cpu_target: 75
    memory_target: 75
  worker:
    min_replicas: 6
    max_replicas: 20
    cpu_target: 80
    memory_target: 85
```

## 4. Pod Disruption Budgets (PDBs)

### 4.1 PDB-Definition

Erstellen Sie die Datei `templates/pdb.yml.j2`:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ component_name }}
  namespace: {{ namespace }}
spec:
  minAvailable: {{ pdb.min_available }}
  selector:
    matchLabels:
      app: vision-ocr
      component: {{ component_name }}
```

### 4.2 PDB-Konfiguration für kritische Komponenten

Fügen Sie die PDB-Konfiguration in `group_vars/production.yml` hinzu:

```yaml
pdb:
  vision_module:
    min_available: 2
  ocr_engine:
    min_available: 2
  api_gateway:
    min_available: 1
  worker:
    min_available: 3
```

## 5. Lastverteilung und Ingress-Konfiguration

### 5.1 Load Balancer Service

Erstellen Sie `templates/load-balancer.yml.j2`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-gateway-lb
  namespace: {{ namespace }}
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: "60"
spec:
  type: LoadBalancer
  ports:
  - port: 443
    targetPort: 8080
    protocol: TCP
    name: https
  selector:
    app: vision-ocr
    component: api-gateway
```

### 5.2 Ingress mit mehreren Zonen

Erstellen Sie `templates/ingress-multi-az.yml.j2`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vision-ocr-ingress
  namespace: {{ namespace }}
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - {{ ingress.host }}
    secretName: {{ ingress.tls_secret }}
  rules:
  - host: {{ ingress.host }}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway
            port:
              number: 8080
```

## 6. Datenbank-Hochverfügbarkeit

### 6.1 PostgreSQL mit Replikation

Erstellen Sie `templates/postgres-statefulset.yml.j2`:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: {{ namespace }}
spec:
  serviceName: "postgres"
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - postgres
            topologyKey: "kubernetes.io/hostname"
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - postgres
              topologyKey: "failure-domain.beta.kubernetes.io/zone"
      containers:
      - name: postgres
        image: postgres:14
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        ports:
        - containerPort: 5432
          name: postgres
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        - name: postgres-config
          mountPath: /etc/postgresql/conf.d
        livenessProbe:
          exec:
            command:
            - sh
            - -c
            - exec pg_isready -U ${POSTGRES_USER} -h localhost
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 6
        readinessProbe:
          exec:
            command:
            - sh
            - -c
            - exec pg_isready -U ${POSTGRES_USER} -h localhost
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
      volumes:
      - name: postgres-config
        configMap:
          name: postgres-config
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "fast"
      resources:
        requests:
          storage: {{ storage.postgres_size }}
```

### 6.2 Redis-Cluster für verteilten Cache

Erstellen Sie `templates/redis-cluster.yml.j2`:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: {{ namespace }}
spec:
  serviceName: "redis"
  replicas: 3
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - redis
            topologyKey: "kubernetes.io/hostname"
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - redis
              topologyKey: "failure-domain.beta.kubernetes.io/zone"
      containers:
      - name: redis
        image: redis:6.2-alpine
        command:
        - redis-server
        - "/redis-config/redis.conf"
        ports:
        - containerPort: 6379
          name: redis
        volumeMounts:
        - name: redis-data
          mountPath: /data
        - name: redis-config
          mountPath: /redis-config
        livenessProbe:
          exec:
            command:
            - sh
            - -c
            - redis-cli ping
          initialDelaySeconds: 15
          periodSeconds: 5
        readinessProbe:
          exec:
            command:
            - sh
            - -c
            - redis-cli ping
          initialDelaySeconds: 5
          periodSeconds: 3
      volumes:
      - name: redis-config
        configMap:
          name: redis-config
  volumeClaimTemplates:
  - metadata:
      name: redis-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "fast"
      resources:
        requests:
          storage: {{ storage.redis_size }}
```

## 7. Backup und Disaster Recovery

### 7.1 Regelmäßige Backups mit Velero

Erstellen Sie `templates/backup-schedule.yml.j2`:

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 1 * * *"
  template:
    includedNamespaces:
    - {{ namespace }}
    includedResources:
    - deployments
    - statefulsets
    - configmaps
    - secrets
    - persistentvolumeclaims
    - pods
    excludedResources:
    - pods/exec
    - pods/attach
    ttl: 720h
    storageLocation: default
    volumeSnapshotLocations:
    - default
  useOwnerReferencesInBackup: false
```

### 7.2 Disaster Recovery Plan

Erstellen Sie ein Disaster Recovery Playbook `playbooks/disaster-recovery.yml`:

```yaml
---
- name: Disaster Recovery
  hosts: "{{ target_env | default('production') }}"
  gather_facts: false
  tasks:
    - name: Check for latest backup
      shell: velero backup get | grep -v NAME | sort -k 2 | tail -1 | awk '{print $1}'
      register: latest_backup
      delegate_to: localhost

    - name: Restore from latest backup
      shell: velero restore create --from-backup {{ latest_backup.stdout }} --wait
      when: latest_backup.stdout != ""
      delegate_to: localhost

    - name: Verify restored resources
      kubernetes.core.k8s_info:
        kind: Pod
        namespace: "{{ namespace }}"
        context: "{{ context }}"
      register: restored_pods

    - name: Verify database connectivity
      shell: kubectl exec -n {{ namespace }} svc/postgres -- psql -U postgres -c "SELECT 1;"
      register: db_check
      ignore_errors: true
      delegate_to: localhost

    - name: Show recovery status
      debug:
        msg: >
          Recovery Status:
          Pods Restored: {{ restored_pods.resources | length }}
          Database Connection: {{ 'OK' if db_check.rc == 0 else 'Failed' }}
```

## 8. Monitoring und Alerting

### 8.1 Prometheus AlertManager Konfiguration

Erstellen Sie `templates/alertmanager-config.yml.j2`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
  namespace: monitoring
data:
  alertmanager.yml: |
    global:
      resolve_timeout: 5m
      slack_api_url: '{{ alerting.slack_webhook_url }}'

    route:
      group_by: ['namespace', 'job', 'alertname']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 3h
      receiver: 'slack-notifications'
      routes:
      - receiver: 'slack-critical'
        match:
          severity: critical
        continue: true
      - receiver: 'pagerduty-critical'
        match:
          severity: critical

    receivers:
    - name: 'slack-notifications'
      slack_configs:
      - channel: '#{{ alerting.slack_channel }}'
        title: '[{{ "{{" }} .Status | toUpper {{ "}}" }}] {{ "{{" }} .CommonLabels.alertname {{ "}}" }}'
        text: >-
          {{ "{{" }} range .Alerts {{ "}}" }}
            *Alert:* {{ "{{" }} .Annotations.summary {{ "}}" }}
            *Description:* {{ "{{" }} .Annotations.description {{ "}}" }}
            *Severity:* {{ "{{" }} .Labels.severity {{ "}}" }}
          {{ "{{" }} end {{ "}}" }}
    - name: 'slack-critical'
      slack_configs:
      - channel: '#{{ alerting.slack_critical_channel }}'
        title: '[CRITICAL] {{ "{{" }} .CommonLabels.alertname {{ "}}" }}'
        text: >-
          {{ "{{" }} range .Alerts {{ "}}" }}
            *Alert:* {{ "{{" }} .Annotations.summary {{ "}}" }}
            *Description:* {{ "{{" }} .Annotations.description {{ "}}" }}
          {{ "{{" }} end {{ "}}" }}
    - name: 'pagerduty-critical'
      pagerduty_configs:
      - service_key: {{ alerting.pagerduty_service_key }}
        description: '{{ "{{" }} .CommonLabels.alertname {{ "}}" }}'
        client: 'Prometheus'
        client_url: '{{ alerting.prometheus_url }}'
        details:
          firing: '{{ "{{" }} template "pagerduty.default.instances" .Alerts.Firing {{ "}}" }}'
```

### 8.2 Prometheus Alerting Rules

Erstellen Sie `templates/prometheus-rules.yml.j2`:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: vision-ocr-alerts
  namespace: monitoring
  labels:
    app: prometheus-operator
    release: prometheus
spec:
  groups:
  - name: vision-ocr.rules
    rules:
    - alert: HighCPUUsage
      expr: sum(rate(container_cpu_usage_seconds_total{namespace="{{ namespace }}",container!=""}[5m])) by (pod) / sum(container_spec_cpu_quota{namespace="{{ namespace }}",container!=""}) by (pod) > 0.85
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High CPU usage for pod {{ "{{" }} $labels.pod {{ "}}" }}"
        description: "Pod {{ "{{" }} $labels.pod {{ "}}" }} CPU usage is above 85% for 10 minutes"
    
    - alert: HighMemoryUsage
      expr: sum(container_memory_working_set_bytes{namespace="{{ namespace }}",container!=""}) by (pod) / sum(container_spec_memory_limit_bytes{namespace="{{ namespace }}",container!=""}) by (pod) > 0.85
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High memory usage for pod {{ "{{" }} $labels.pod {{ "}}" }}"
        description: "Pod {{ "{{" }} $labels.pod {{ "}}" }} memory usage is above 85% for 10 minutes"
    
    - alert: PodCrashLooping
      expr: rate(kube_pod_container_status_restarts_total{namespace="{{ namespace }}"}[15m]) * 60 * 5 > 5
      for: 15m
      labels:
        severity: critical
      annotations:
        summary: "Pod {{ "{{" }} $labels.pod {{ "}}" }} is crash looping"
        description: "Pod {{ "{{" }} $labels.pod {{ "}}" }} is restarting more than 5 times in 15 minutes"
    
    - alert: APIHighLatency
      expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{namespace="{{ namespace }}",service="api-gateway"}[5m])) by (le)) > 1
      for: 15m
      labels:
        severity: warning
      annotations:
        summary: "API High Latency"
        description: "95th percentile of API request duration is above 1 second for 15 minutes"
```

## 9. Zusammenfassung

Diese Hochverfügbarkeits-Konfiguration für die Universal Vision & OCR Processing Platform bietet:

1. **Ausfallsicherheit** durch Multi-AZ-Deployment und Anti-Affinity-Regeln
2. **Skalierbarkeit** durch Horizontale Pod-Autoskalierung und lastbasierte Ressourcenzuweisung
3. **Wartbarkeit** durch Pod Disruption Budgets und automatisierte Deployment-Prozesse
4. **Datensicherheit** durch regelmäßige Backups und Disaster-Recovery-Pläne
5. **Überwachbarkeit** durch umfassendes Monitoring und Alerting

Durch die Kombination dieser Konfigurationen wird eine robuste, hochverfügbare Plattform geschaffen, die auch bei Ausfällen einzelner Komponenten oder ganzer Availability Zones weiterhin betriebsbereit bleibt und konsistente Leistung bietet.

Die Plattform lässt sich bei Bedarf horizontal und vertikal skalieren, um verschiedene Workload-Anforderungen zu erfüllen, von kleinen Installationen bis hin zu unternehmenskritischen Produktionsumgebungen mit hohem Durchsatz.

## 10. Nächste Schritte

1. Implementieren Sie Service Mesh (z.B. Istio) für erweiterte Netzwerkfunktionen und Sicherheit
2. Automatisieren Sie Rollback-Verfahren im Falle fehlerhafter Deployments
3. Integrieren Sie fortschrittliche Überwachung für Systemressourcen und Anwendungsleistung
4. Implementieren Sie eine Blue-Green-Deployment-Strategie für risikoarme Updates
5. Implementieren Sie Chaos-Engineering-Tests zur Validierung der Ausfallsicherheit