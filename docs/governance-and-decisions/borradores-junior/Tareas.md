# Plan Maestro de Tareas y Ejecución: Plataforma Cafetera "AromaPacífico" (FNC 2026)

---

## 1. Enfoque Metodológico y Estándares de Ingeniería

Este documento establece la **hoja de ruta integral y exhaustiva de tareas** requeridas para planificar, diseñar, implementar, auditar y sustentar con éxito el proyecto de actualización de la plataforma cafetera **AromaPacífico** para la Federación Nacional de Cafeteros (FNC).

El plan abarca desde las tareas iniciales de aprovisionamiento de repositorios y gobernanza del código hasta la sustentación formal ante el comité técnico y arquitecto delegado de la Federación.

### Principios de Ejecución y Prácticas de la Industria Aplicadas:

- **Gestión de Versiones y Ramas:** Adopción de _GitHub Flow / Trunk-Based Development_ con ramas efímeras (`feature/*`, `fix/*`), commits bajo el estándar **Conventional Commits** (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`) y firmas criptográficas obligatorias (GPG/SSH).
- **Seguridad en la Cadena de Suministro (DevSecOps):** Cero secretos en repositorios (uso de herramientas de escaneo pre-commit `gitleaks`/`trufflehog`), análisis estático de seguridad en IaC (`tfsec`, `trivy`, `checkov`) y autenticación de pipelines mediante **OIDC (OpenID Connect)** federado con AWS, erradicando llaves estáticas permanentes.
- **Disciplina Estricta de Timebox (Épica 6):** Límite inflexible de **100 horas y 2 semanas** de esfuerzo humano para el código ejecutable de infraestructura (módulos, variables, estado remoto y pipeline).
- **Alineación con Plantillas del Proyecto:** Integración directa con los artefactos estándar del proyecto ubicados en `agentes/templates/` (`RELEASE_NOTES_APPLICATION_TEMPLATE.md`, `RELEASE_NOTES_INFRASTRUCTURE_TEMPLATE.md`, `PULL_REQUEST_TEMPLATE.md`, `commit-template.txt`).

---

## 2. Mapa General de Fases del Proyecto

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CICLO DE VIDA DE EJECUCIÓN AROMAPACÍFICO                        │
├─────────┬──────────────────────────────────┬───────────────────────────────────────────┤
│ Fase    │ Nombre de la Fase                │ Alcance Principal                         │
├─────────┼──────────────────────────────────┼───────────────────────────────────────────┤
│ Fase 0  │ Inicialización y Gobernanza      │ Repositorios, Git hooks, CI base, templates│
│ Fase 1  │ Diseño Arquitectónico y Redes    │ 7 puntos del reto, diagramas, CIDR, drones│
│ Fase 2  │ WBS y Planificación de 100 Horas │ Desglose de Épica 6, horas, RACI, ruta    │
│ Fase 3  │ Implementación IaC (Épica 6)     │ Terraform/OpenTofu, CI/CD, change freeze  │
│ Fase 4  │ Observabilidad y Confiabilidad   │ SLOs/SLIs, CloudWatch, dashboards FinOps  │
│ Fase 5  │ Gestión del Cambio y Releases    │ Diligenciamiento de Release Notes y rollback│
│ Fase 6  │ Dossier FinOps y Design System   │ Cotizaciones 2026, BOM, lámina UI/UX      │
│ Fase 7  │ Preparación y Sustentación       │ Presentación, guion, defensa técnica 20m  │
└─────────┴──────────────────────────────────┴───────────────────────────────────────────┘
```

---

## 3. Fase 0: Inicialización del Entorno, Repositorios y Gobernanza (Setup Base)

### TSK-00-01: Configuración del Repositorio Git y Políticas de Protección de Ramas

- **Fase:** Fase 0 (Inicialización).
- **Responsable:** DevOps Lead / Tech Lead.
- **Precondiciones:** Acceso administrativo a la organización de GitHub / GitLab de la FNC.
- **Descripción Técnica Paso a Paso:**
  1. Inicializar el repositorio Git estructurado:
     ```bash
     git init
     git branch -M main
     ```
  2. Configurar la estructura de carpetas estándar:
     ```text
     ├── .github/
     │   ├── workflows/             # Pipelines CI/CD
     │   └── PULL_REQUEST_TEMPLATE.md
     ├── agentes/templates/         # Plantillas de release y commits
     ├── docs/                      # Arquitectura, FinOps y sustentación
     │   ├── architecture/
     │   ├── diagrams/
     │   └── finops/
     ├── terraform/                 # Código IaC (Épica 6)
     │   ├── environments/
     │   │   ├── dev/
     │   │   ├── test/
     │   │   └── prod/
     │   └── modules/
     │       ├── network/
     │       ├── security/
     │       ├── ingest_telemetry/
     │       └── serverless_function/
     ├── scripts/                   # Scripts de validación y automatización
     └── README.md
     ```
  3. Vincular las plantillas de PR existentes copiando `agentes/templates/PULL_REQUEST_TEMPLATE.md` a `.github/PULL_REQUEST_TEMPLATE.md`.
  4. Configurar plantilla de commit local:
     ```bash
     git config commit.template agentes/templates/commit-template.txt
     ```
  5. Configurar reglas de protección de rama (`Branch Protection Rules`) sobre `main`:
     - Exigir Pull Request con al menos 1 revisión aprobada (_Required Reviewers_).
     - Exigir que los checks de CI (`lint-iac`, `security-scan`, `terraform-plan`) pasen en verde antes del merge.
     - Bloquear _force push_ y eliminación de ramas.
     - Exigir commits firmados (_Require signed commits_).
- **Entregables:** Repositorio estructurado, plantilla de PR configurada y reglas de rama activas.
- **Criterio de Aceptación (DoD):** Un intento de push directo a `main` debe ser rechazado por la política de GitHub; un PR debe cargar automáticamente la plantilla de `agentes/templates/`.
- **Estimación:** 3 horas.

---

### TSK-00-02: Implementación de Hooks de Pre-Commit y Escaneo de Secretos

- **Fase:** Fase 0 (Inicialización).
- **Responsable:** Security Engineer / DevOps Engineer.
- **Precondiciones:** Repositorio inicializado, Python / Node.js disponible en estaciones de trabajo.
- **Descripción Técnica Paso a Paso:**
  1. Crear archivo `.pre-commit-config.yaml` en la raíz del repositorio con hooks industriales:
     ```yaml
     repos:
       - repo: https://github.com/pre-commit/pre-commit-hooks
         rev: v4.5.0
         hooks:
           - id: trailing-whitespace
           - id: end-of-file-fixer
           - id: check-yaml
           - id: check-json
           - id: check-merge-conflict
       - repo: https://github.com/antonbabenko/pre-commit-terraform
         rev: v1.86.0
         hooks:
           - id: terraform_fmt
           - id: terraform_tflint
           - id: terraform_docs
       - repo: https://github.com/gitleaks/gitleaks
         rev: v8.18.2
         hooks:
           - id: gitleaks
     ```
  2. Instalar y activar hooks:
     ```bash
     pip install pre-commit gitleaks
     pre-commit install
     ```
  3. Ejecutar escaneo baseline sobre el repositorio:
     ```bash
     pre-commit run --all-files
     ```
- **Entregables:** Archivo `.pre-commit-config.yaml` activo y validación de cero secretos en el histórico.
- **Criterio de Aceptación (DoD):** Si un desarrollador intenta commitear una cadena que parezca una llave privada o API key (ej. `AKIA...` o secretos planos), el hook de pre-commit debe abortar el commit inmediatamente.
- **Estimación:** 2 horas.

---

## 4. Fase 1: Diseño y Arquitectura de la Solución (Entregable 1)

### TSK-01-01: Documento de Arquitectura General y Matriz de Baja 2020

- **Fase:** Fase 1 (Arquitectura).
- **Responsable:** Cloud Solutions Architect.
- **Precondiciones:** Comprensión del enunciado oficial y análisis de `Fuente-de-Verdad-AromaPacifico.md`.
- **Descripción Técnica Paso a Paso:**
  1. Redactar el documento central `docs/architecture/ARQUITECTURA_DETALLADA.md` cubriendo los 7 puntos del reto:
     - _Gobierno:_ Estructura de Landing Zone multicuenta en AWS (Cuentas: `Master/Billing`, `Security/Audit`, `Shared-Network`, `Workload-Prod`, `Workload-Test`).
     - _Seguridad:_ Matriz RBAC para las 6 identidades y esquema Zero Trust.
     - _Red y Conectividad:_ Topología híbrida Acopios - Cloud.
     - _Automatización:_ Modelo de pipeline CI/CD y gestión de secretos.
     - _Cargas y Flujos:_ Telemetría, drones, sacos e inferencia IA.
     - _Observabilidad:_ Métricas, trazas, logs y SLOs.
     - _Sistema de Diseño:_ Tokens visuales y ergonomía de campo.
  2. Elaborar la **Matriz de Obsolescencia y Retiro de Componentes 2020**:
     - _Componente Retirado:_ Módems celulares 2G/3G $\rightarrow$ _Razón:_ Apagado del espectro en Colombia $\rightarrow$ _Reemplazo:_ Módulos LTE-M / NB-IoT (B28/B4).
     - _Componente Retirado:_ Envío sincrónico directo sin buffer $\rightarrow$ _Razón:_ Falta de señal en veredas cafeteras $\rightarrow$ _Reemplazo:_ Store-and-Forward con buffer de 24h.
     - _Componente Retirado:_ Acopios aislados sin red $\rightarrow$ _Razón:_ Silos logísticos $\rightarrow$ _Reemplazo:_ LAN segmentada en 7 zonas con salida WAN de 100 Mbps y VPN IPsec.
     - _Componente Retirado:_ Cotizaciones 2020 $\rightarrow$ _Razón:_ Desactualización comercial $\rightarrow$ _Reemplazo:_ Precios oficiales Cloud/Hardware 2026.
- **Entregables:** Documento `ARQUITECTURA_DETALLADA.md` formalizado con su matriz de transición.
- **Criterio de Aceptación (DoD):** El documento cubre exhaustivamente los 7 puntos exigidos por el enunciado del reto académico sin omitir ninguna restricción.
- **Estimación:** 12 horas.

---

### TSK-01-02: Plan de Direccionamiento IP y Políticas de Seguridad de Red

- **Fase:** Fase 1 (Arquitectura).
- **Responsable:** Network & Security Engineer.
- **Precondiciones:** Conocimiento del bloque reservado de centros de acopio (`10.41.0.0/16`, `10.42.0.0/16`, `10.43.0.0/16`).
- **Descripción Técnica Paso a Paso:**
  1. Diseñar la tabla de subredes y VLANs para los tres centros de acopio:
     - Cauca (`10.41.X.0/24`), Huila (`10.42.X.0/24`), Tolima (`10.43.X.0/24`).
     - VLAN 10 (`10.X.1.0/24`): Gerencia.
     - VLAN 20 (`10.X.2.0/24`): Soporte.
     - VLAN 30 (`10.X.3.0/24`): Logística y Básculas.
     - VLAN 40 (`10.X.4.0/24`): Transporte / Patio de Camiones.
     - VLAN 50 (`10.X.5.0/24`): Visitantes (aislada totalmente de Gerencia y Logística).
     - VLAN 100 (`10.X.10.0/24`): Servidores locales e impresión de códigos.
     - VLAN 200 (`10.X.20.0/24`): Borde de red y Firewall.
  2. Dimensionar el plan de direccionamiento en la nube (AWS VPCs) asegurando **cero solapamiento**:
     - VPC Producción: `10.100.0.0/16` (Subredes: Ingesta `10.100.1.0/24`, Drones `10.100.2.0/24`, Apps `10.100.10.0/24`, Datos `10.100.20.0/24`, VPN Borde `10.100.30.0/24`, Pública `10.100.50.0/24`).
     - VPC Staging: `10.101.0.0/16`.
     - VPC Desarrollo: `10.102.0.0/16`.
  3. Redactar la **Tabla de Políticas de Firewall Perimetral y de Nube**:
     - Especificar: ID Regla, Origen, Destino, Protocolo, Puerto, Acción (ACCEPT/DROP), Tipo (Permanente o Temporal) y Justificación Operacional.
     - Aislar explícitamente el tráfico de la VLAN de Visitantes impidiendo saltos hacia las subredes operativas de recepción.
- **Entregables:** Tabla de subredes, matriz de enrutamiento y tabla de políticas de firewall perimetral y cloud en markdown.
- **Criterio de Aceptación (DoD):** Demostración matemática y lógica de que ninguna subred de la nube colisiona con los rangos `10.41/16`, `10.42/16` ni `10.43/16`, y que las reglas de firewall bloquean el tráfico inter-VLAN prohibido.
- **Estimación:** 8 horas.

---

### TSK-01-03: Modelado del Subsistema IoT (Store-and-Forward y Hardware de Finca)

- **Fase:** Fase 1 (Arquitectura).
- **Responsable:** IoT & Embedded Systems Specialist.
- **Precondiciones:** Datos de sensores Modbus y consumo energético validados.
- **Descripción Técnica Paso a Paso:**
  1. Documentar la arquitectura del nodo sensor en finca:
     - Microcontrolador: ESP32-S3 con módem SIM7080G (LTE-M/NB-IoT).
     - Protocolo industrial: RS485 Modbus RTU para integración con sensor multiparámetro 7-en-1 (NPK, humedad de suelo, temperatura de suelo, pH, conductividad eléctrica).
  2. Formalizar el algoritmo de **Store-and-Forward de 24 Horas**:
     - _Paso 1 (Muestreo):_ El microcontrolador despierta de Deep Sleep cada 4 horas (en cultivo) o cada 1 hora (en secado).
     - _Paso 2 (Lectura y Buffer):_ Lee los registros Modbus, arma el payload JSON/Protobuf y lo persiste en la memoria Flash SPI local / tarjeta MicroSD con timestamp Unix e indicador de sincronización (`synced = false`).
     - _Paso 3 (Intento de Transmisión):_ Enciende el módem celular y evalúa registro en red celular (LTE-M B28/B4).
     - _Paso 4 (Conectividad Positiva):_ Establece sesión TLS 1.3 mutual (mTLS con certificados X.509) hacia AWS IoT Core, publica los registros pendientes en orden FIFO y marca `synced = true`.
     - _Paso 5 (Falla de Conectividad):_ Si no hay señal en 30 segundos, incrementa el contador de reintentos con backoff exponencial, apaga el módem celular y regresa a Deep Sleep. El buffer local retiene hasta 24 horas (capacidad física para >30 días).
     - _Paso 6 (Drenado):_ Al recuperar señal en cualquier momento, el dispositivo drena en ráfaga el buffer acumulado.
  3. Diseñar el circuito de alimentación solar fotovoltaica (Panel 10W monocristalino + Batería LiFePO4 32700 6.000 mAh + Cargador MPPT CN3791).
- **Entregables:** Documento técnico de especificación de firmware y hardware IoT en `docs/architecture/IOT_EDGE_SPEC.md`.
- **Criterio de Aceptación (DoD):** El algoritmo garantiza cero pérdida de datos durante 24 horas continuas de desconexión y el cálculo energético demuestra autonomía > 30 días sin luz solar directa.
- **Estimación:** 8 horas.

---

### TSK-01-04: Diseño del Flujo de Drones, Estados de Fumigación y Puertas Humanas

- **Fase:** Fase 1 (Arquitectura).
- **Responsable:** Cloud Solutions Architect / Systems Engineer.
- **Precondiciones:** Requisitos aeronáuticos y de privacidad del enunciado.
- **Descripción Técnica Paso a Paso:**
  1. Diseñar el diagrama de estados de la orden de fumigación:
     - Estados: `CREADA` $\rightarrow$ `LOTE_DELIMITADO` $\rightarrow$ `FOCO_CONFIRMADO` $\rightarrow$ `AUTORIZACION_PENDIENTE` $\rightarrow$ `AUTORIZADA` $\rightarrow$ `EN_VUELO` $\rightarrow$ `VERIFICACION_PENDIENTE` $\rightarrow$ `CERRADA`.
  2. Implementar la regla de negocio de **Delimitación Previa**:
     - El sistema bloquea la creación de órdenes de aspersión si el lote no cuenta con un polígono GeoJSON registrado en la plataforma que especifique las zonas de exclusión (_No-Fly Zones_: casas, beneficiaderos, caminos, fuentes hídricas).
  3. Formalizar el **Mecanismo de Preposicionamiento Offline**:
     - Las coordenadas del plan de vuelo se sincronizan en la tablet del operador en la cabecera municipal o acopio departamental. El dron vuela sin dependencia del smartphone del caficultor. Los datos se descargan al aterrizar mediante enlace WiFi/USB local.
  4. Diseñar la compuerta humana (_Human-in-the-Loop_):
     - La función Lambda procesa la imagen del foco y calcula un score de confianza de roya/plaga. Sin embargo, **ninguna función puede transicionar el estado a `AUTORIZADA`**. La transición exige un request firmado por un usuario autenticado con rol `Agrónomo / Operador FNC` vía Cognito/IAM con MFA activo.
- **Entregables:** Máquina de estados modelada, esquema GeoJSON de zonas y especificación de compuerta humana en `docs/architecture/DRONES_WORKFLOW.md`.
- **Criterio de Aceptación (DoD):** El modelo demuestra que es imposible autorizar una fumigación sin delimitación previa de lote y sin aprobación manual de identidad humana.
- **Estimación:** 6 horas.

---

### TSK-01-05: Diseño de Trazabilidad del Saco, RPO/RTO y Sanitización de Datos

- **Fase:** Fase 1 (Arquitectura).
- **Responsable:** Data Architect / Backend Engineer.
- **Precondiciones:** Definición de estados del saco en el enunciado.
- **Descripción Técnica Paso a Paso:**
  1. Especificar el modelo de datos de ciclo de vida del saco de 60 kg:
     - Estados: `EN_PREPARACION` (finca), `EN_VIAJE_ACOPIO` (transportador), `EN_ACOPIO_ACEPTADO` o `EN_ACOPIO_RECHAZADO`, `EN_VIAJE_PUERTO`, `ENTREGADO_PUERTO_ACEPTADO` o `ENTREGADO_PUERTO_RECHAZADO`.
  2. Diseñar el pipeline de persistencia con **RPO de 15 minutos**:
     - Eventos transaccionales capturados mediante API Gateway $\rightarrow$ DynamoDB On-Demand con replicación y backups continuos (_Point-in-Time Recovery - PITR_ habilitado).
  3. Diseñar la arquitectura de alta disponibilidad para la **Consulta Pública Web (RTO de 4 horas)**:
     - Distribución estática mediante Amazon CloudFront + S3 Website Hosting.
     - Backend serverless desacoplado (API Gateway HTTP API + AWS Lambda).
  4. Implementar el algoritmo de **Sanitización y Enmascaramiento de Datos para Compradores (Habeas Data)**:
     - El endpoint público `/api/v1/sacks/{code}` consulta una proyección restringida de DynamoDB o ejecuta una transformación en Lambda que elimina los campos: `cedula_caficultor`, `nombre_productor`, `coordenadas_exactas_finca`, `precio_pagado` y `telemetria_detallada_camion`.
     - El comprador únicamente recibe: `codigo_saco`, `departamento_origen`, `fechas_cosecha_beneficio`, `humedad_promedio_secado`, `temperatura_secado` y `certificado_calidad`.
- **Entregables:** Especificación de API OpenAPI 3.0, modelo de datos y reglas de proyección segura en `docs/architecture/SACK_TRACEABILITY.md`.
- **Criterio de Aceptación (DoD):** La especificación de API demuestra que un comprador externo no tiene acceso bajo ninguna circunstancia a la cédula del productor ni a la traza logística interna.
- **Estimación:** 6 horas.

---

### TSK-01-06: Generación y Validación de Diagramas Técnicos Oficiales (PNG)

- **Fase:** Fase 1 (Arquitectura).
- **Responsable:** Cloud Architect / DevOps Lead.
- **Precondiciones:** Diseños de las tareas TSK-01-01 a TSK-01-05 aprobados.
- **Descripción Técnica Paso a Paso:**
  1. Generar los diagramas oficiales de arquitectura utilizando los agentes visuales:
     - Diagrama 1: Arquitectura Global Cloud & IoT en 4 capas (`aromapacifico_arquitectura.png`).
     - Diagrama 2: Diagrama de Flujos de Datos, Ciclos de Vida y Estados (`aromapacifico_flujos_datos.png`).
  2. Validar que los diagramas incorporen todas las cajas de componentes exigidas por el enunciado:
     - Fincas IoT, Store-and-Forward 24h, LTE-M/NB-IoT.
     - Transportadores GPS emitiendo cada 5 minutos.
     - Centros de Acopio con segmentación `10.41/42/43` y firewalls.
     - Nube central AWS con IoT Core, DynamoDB, S3, Lambda, Rekognition, CloudWatch.
     - Portal público de consulta sanitizada para compradores.
  3. Verificar resolución, nitidez y enlaces markdown en los documentos del proyecto.
- **Entregables:** Archivos PNG en la raíz del proyecto e incrustados correctamente en `Fuente-de-Verdad-AromaPacifico.md` y `Propuestas-de-Tecnologias.md`.
- **Criterio de Aceptación (DoD):** Los diagramas son legibles, profesionales, en formato PNG y representan el 100% de los data paths del sistema.
- **Estimación:** 4 horas.

---

## 5. Fase 2: Planificación y WBS de la Épica 6 (Entregable 2)

### TSK-02-01: Desglose de Estructura de Trabajo (WBS) Estricto en 100 Horas / 2 Semanas

- **Fase:** Fase 2 (Planificación).
- **Responsable:** Project Manager / DevOps Lead.
- **Precondiciones:** Diagrama de arquitectura aprobado (TSK-01-06).
- **Descripción Técnica Paso a Paso:**
  1. Construir la matriz de desglose WBS de la **Épica 6: Infraestructura como Código**, garantizando que la suma acumulada sea **exactamente $\le$ 100 horas hombre**:
     - _Módulo de Red del Ambiente (22 horas):_ VPC, subredes, tablas de rutas, VPN Gateway y asociación lógica con acopio.
     - _Módulo de Seguridad e Identidades (18 horas):_ Roles IAM de mínimo privilegio, llaves KMS y Security Groups permanentes.
     - _Módulo de Ingesta IoT y Persistencia (24 horas):_ IoT Core Topic Rule, endpoint MQTT y tabla DynamoDB con TTL.
     - _Patrón de Función Serverless de Inferencia (16 horas):_ Función Lambda patrón con permisos S3, DynamoDB y Rekognition + DLQ.
     - _Pipeline CI/CD y Automatización (14 horas):_ GitHub Actions con OIDC, validación de calidad y approval gate de producción.
     - _Parametrización Multi-ambiente y Pruebas del Plan (6 horas):_ `dev.tfvars`, `prod.tfvars`, ejecución y verificación de `terraform plan`.
  2. Mapear cada tarea del WBS directamente a una caja del diagrama de arquitectura (`aromapacifico_arquitectura.png`).
  3. Establecer la matriz de responsables y la secuencia temporal en dos semanas de trabajo (Sprint de 10 días hábiles, 10 horas/día distribuidas en el equipo).
- **Entregables:** Documento `docs/PLAN_100_HORAS.md` con cronograma, dependencias y matriz RACI.
- **Criterio de Aceptación (DoD):** La sumatoria total no excede 100 horas ni 2 semanas de calendario; cada tarea apunta a un recurso de infraestructura concreto del diagrama.
- **Estimación:** 4 horas.

---

## 6. Fase 3: Implementación de Infraestructura como Código (Épica 6 - Entregable 3)

### TSK-03-01: Configuración del Backend Remoto Seguro de Terraform

- **Fase:** Fase 3 (IaC - Épica 6).
- **Responsable:** DevOps Engineer.
- **Precondiciones:** Cuenta AWS aprovisionada con permisos IAM adecuados.
- **Descripción Técnica Paso a Paso:**
  1. Crear script de inicialización del backend remoto `scripts/init_remote_backend.sh`:
     - Crear bucket S3 privado con versionamiento activo y bloqueo de acceso público:
       ```bash
       aws s3api create-bucket --bucket aromapacifico-tfstate-prod --region us-east-1
       aws s3api put-bucket-versioning --bucket aromapacifico-tfstate-prod --versioning-configuration Status=Enabled
       aws s3api put-bucket-encryption --bucket aromapacifico-tfstate-prod --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
       aws s3api put-public-access-block --bucket aromapacifico-tfstate-prod --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
       ```
     - Crear tabla DynamoDB para bloqueo distribuido de estado (_State Locking_):
       ```bash
       aws dynamodb create-table \
         --table-name aromapacifico-tflocks \
         --attribute-definitions AttributeName=LockID,AttributeType=S \
         --key-schema AttributeName=LockID,KeyType=HASH \
         --billing-mode PAY_PER_REQUEST \
         --region us-east-1
       ```
  2. Configurar el bloque de backend en `terraform/main.tf`:
     ```hcl
     terraform {
       required_version = ">= 1.7.0"
       required_providers {
         aws = {
           source  = "hashicorp/aws"
           version = "~> 5.40.0"
         }
       }
       backend "s3" {
         bucket         = "aromapacifico-tfstate-prod"
         key            = "environments/prod/terraform.tfstate"
         region         = "us-east-1"
         dynamodb_table = "aromapacifico-tflocks"
         encrypt        = true
       }
     }
     ```
- **Entregables:** Bucket S3 y tabla DynamoDB aprovisionados; configuración de backend remoto en Terraform.
- **Criterio de Aceptación (DoD):** `terraform init` inicializa el backend remoto exitosamente; dos ejecuciones simultáneas detectan el lock en DynamoDB evitando corrupción de estado.
- **Estimación:** 4 horas (imputables a las 100h).

---

### TSK-03-02: Desarrollo del Módulo de Red (`modules/network`)

- **Fase:** Fase 3 (IaC - Épica 6).
- **Responsable:** Network & Cloud Engineer.
- **Precondiciones:** TSK-03-01 completada; direccionamiento de TSK-01-02 validado.
- **Descripción Técnica Paso a Paso:**
  1. Desarrollar `terraform/modules/network/main.tf`:
     - Crear la VPC del ambiente con bloque CIDR parametrizado (ej. `10.100.0.0/16` para Prod).
     - Crear subredes privadas y públicas segmentadas:
       - Subred Ingesta IoT (`10.X.1.0/24`).
       - Subred Objetos Dron / S3 Endpoints (`10.X.2.0/24`).
       - Subred Aplicación Backend (`10.X.10.0/24`).
       - Subred Capa de Datos (`10.X.20.0/24`).
       - Subred Borde / VPN Gateway (`10.X.30.0/24`).
       - Subred Pública Consulta Web (`10.X.50.0/24`).
     - Aprovisionar Internet Gateway para la subred pública.
     - Aprovisionar Virtual Private Gateway (VGW) o Transit Gateway Attachment para la asociación con el centro de acopio departamental (`10.41.0.0/16`).
     - Configurar tablas de rutas y asociaciones garantizando que las subredes privadas no tengan rutas directas hacia Internet.
  2. Declarar variables en `variables.tf` y salidas en `outputs.tf` (`vpc_id`, `private_subnet_ids`, `public_subnet_ids`).
- **Entregables:** Módulo Terraform en `terraform/modules/network/`.
- **Criterio de Aceptación (DoD):** `terraform validate` pasa sin advertencias; las rutas hacia el acopio quedan declaradas sin solapamiento CIDR.
- **Estimación:** 18 horas (imputables a las 100h).

---

### TSK-03-03: Desarrollo del Módulo de Seguridad y Cifrado (`modules/security`)

- **Fase:** Fase 3 (IaC - Épica 6).
- **Responsable:** Security & Cloud Engineer.
- **Precondiciones:** TSK-03-02 completada.
- **Descripción Técnica Paso a Paso:**
  1. Desarrollar `terraform/modules/security/main.tf`:
     - Aprovisionar llaves maestras **AWS KMS** gestionadas por el cliente (CMK) con rotación automática anual habilitada para cifrado de DynamoDB, S3 y logs de CloudWatch.
     - Definir roles y políticas IAM con mínimo privilegio:
       - `role_iot_basic_ingest`: Permiso exclusivo de escribir (`dynamodb:PutItem`) en la tabla de telemetría.
       - `role_lambda_inference_pattern`: Permiso exclusivo de lectura sobre el bucket de drones, invocación a `rekognition:DetectFaces` / `rekognition:DetectLabels` y escritura en DynamoDB.
       - `role_public_sack_query`: Permiso exclusivo de lectura (`dynamodb:GetItem`, `dynamodb:Query`) sobre atributos enmascarados de sacos.
     - Implementar los **Security Groups Permanentes** definidos en el diagrama de red:
       - `sg_vpn_edge`: Permite tráfico IPsec UDP 500/4500 desde la IP estática del centro de acopio.
       - `sg_app_internal`: Permite tráfico TCP 443 únicamente desde la subred de aplicación hacia los endpoints privados de datos.
- **Entregables:** Módulo Terraform en `terraform/modules/security/`.
- **Criterio de Aceptación (DoD):** Toda política IAM implementa mínimo privilegio estricto sin comodines `*` en acciones ni recursos; escaneo de `tfsec` arroja cero severidades altas/críticas.
- **Estimación:** 14 horas (imputables a las 100h).

---

### TSK-03-04: Desarrollo del Módulo de Ingesta IoT y Persistencia (`modules/ingest_telemetry`)

- **Fase:** Fase 3 (IaC - Épica 6).
- **Responsable:** Cloud & Data Engineer.
- **Precondiciones:** Módulos de red y seguridad completados.
- **Descripción Técnica Paso a Paso:**
  1. Desarrollar `terraform/modules/ingest_telemetry/main.tf`:
     - Aprovisionar tabla **Amazon DynamoDB** en modo On-Demand (`billing_mode = "PAY_PER_REQUEST"`):
       - Clave de partición: `PK` (String, ej. `FINCA#001`).
       - Clave de ordenación: `SK` (String, ej. `METRIC#2026-10-30T10:00:00Z`).
       - Cifrado en reposo utilizando la llave KMS de seguridad.
       - Habilitar **Time-To-Live (TTL)** sobre el atributo `ttl_expiration` (configurado a 90 días para drenado automático hacia S3 Glacier).
       - Habilitar DynamoDB Streams (`NEW_AND_OLD_IMAGES`) para captura de cambios.
     - Configurar regla de **AWS IoT Core Topic Rule**:
       - Filtro SQL: `SELECT * FROM 'aromapacifico/fincas/+/telemetria'`.
       - Acción: Insertar directamente en la tabla DynamoDB utilizando el rol `role_iot_basic_ingest`.
       - Error Action: Enrutar mensajes malformados hacia una cola SQS Dead-Letter Queue (`dlq-iot-ingest`).
- **Entregables:** Módulo Terraform en `terraform/modules/ingest_telemetry/`.
- **Criterio de Aceptación (DoD):** La regla de IoT Core enruta el payload JSON a DynamoDB sin invocar cómputo intermedio innecesario, y el atributo TTL queda activo en la tabla.
- **Estimación:** 20 horas (imputables a las 100h).

---

### TSK-03-05: Desarrollo del Patrón de Función Serverless de Inferencia (`modules/serverless_function`)

- **Fase:** Fase 3 (IaC - Épica 6).
- **Responsable:** Serverless & Cloud Engineer.
- **Precondiciones:** Bucket S3 y tabla DynamoDB aprovisionados.
- **Descripción Técnica Paso a Paso:**
  1. Implementar el código en Python 3.12 optimizado para arquitectura Arm64 (Graviton2) en `terraform/modules/serverless_function/src/handler.py`:
     - Disparador: Evento S3 `ObjectCreated` en el prefijo `drone/confirmacion/`.
     - Permiso 1: Lectura del objeto en S3.
     - Permiso 2: Invocación a la API administrada de visión (`rekognition.detect_faces` y `rekognition.detect_labels`).
     - Lógica ética de salvaguarda: Si detecta rostros humanos con confianza > 80%, clasifica como PII, mueve la imagen a cuarentena y aborta el flujo agronómico.
     - Permiso 3: Escritura del resultado (etiqueta de plaga, porcentaje de confianza y timestamp) en el expediente de la finca en DynamoDB.
  2. Implementar Dead-Letter Queue (DLQ) en **Amazon SQS** para captura de fallos de invocación con alarma de CloudWatch asociada.
  3. Declarar el recurso `aws_lambda_function` en Terraform con runtime `python3.12`, arquitecturas `["arm64"]`, memoria de 512 MB y timeout de 30 segundos.
- **Entregables:** Módulo Terraform y código fuente Python de la función patrón en `terraform/modules/serverless_function/`.
- **Criterio de Aceptación (DoD):** La función Lambda se despliega exitosamente con sus roles IAM exactos; no existen servidores EC2 permanentes en espera de imágenes.
- **Estimación:** 16 horas (imputables a las 100h).

---

### TSK-03-06: Parametrización Multi-Ambiente y Configuración de Secretos

- **Fase:** Fase 3 (IaC - Épica 6).
- **Responsable:** DevOps Engineer.
- **Precondiciones:** Los 4 módulos de Terraform terminados.
- **Descripción Técnica Paso a Paso:**
  1. Crear la raíz de despliegue en `terraform/environments/prod/`:
     - `main.tf`: Instanciación de los módulos `network`, `security`, `ingest_telemetry` y `serverless_function`.
     - `variables.tf`: Definición de variables tipadas.
     - `prod.tfvars`: Asignación de valores para Producción (`environment = "prod"`, CIDR `10.100.0.0/16`, tags FinOps obligatorios).
  2. Crear entorno de pruebas en `terraform/environments/test/`:
     - `test.tfvars`: Asignación de valores para Pruebas (`environment = "test"`, CIDR `10.101.0.0/16`).
  3. Validar que **ningún archivo de variables ni de código contenga contraseñas, llaves privadas ni secretos** (los parámetros sensibles se referencian vía AWS Secrets Manager mediante data sources).
- **Entregables:** Archivos `prod.tfvars` y `test.tfvars` completamente parametrizados.
- **Criterio de Aceptación (DoD):** `terraform plan -var-file=prod.tfvars` y `terraform plan -var-file=test.tfvars` se ejecutan limpiamente generando planes distintos y sin solapamiento de CIDR.
- **Estimación:** 6 horas (imputables a las 100h).

---

### TSK-03-07: Construcción del Pipeline CI/CD con OIDC y Change Freeze en Cosecha

- **Fase:** Fase 3 (IaC - Épica 6).
- **Responsable:** DevOps Lead / CI/CD Engineer.
- **Precondiciones:** Repositorio en GitHub y cuenta AWS con IAM OIDC Identity Provider configurado.
- **Descripción Técnica Paso a Paso:**
  1. Crear el workflow `.github/workflows/iac-pipeline.yml`:
     - _Trigger:_ Push a ramas `feature/*` y PRs hacia `main`.
     - _Job 1: Lint & Security Scan:_
       - `terraform fmt -check`
       - `tflint --init && tflint`
       - `tfsec . --soft-fail=false`
     - _Job 2: Terraform Plan:_
       - Autenticación segura mediante **GitHub OIDC** asumiendo el rol IAM `arn:aws:iam::123456789012:role/GitHubActionsTerraformRole`.
       - `terraform plan -no-color -out=tfplan`
       - Comentar el output del plan automáticamente en el PR.
     - _Job 3: Terraform Apply (Producción):_
       - Se ejecuta exclusivamente en push a `main`.
       - Requiere aprobación en el ambiente de GitHub `production` (_Manual Approval Gate_).
       - **Validación Automática de Change Freeze:**

         ```bash
         # Validar ventana de cosecha en horario Colombia (COT, UTC-5)
         CURRENT_HOUR=$(TZ="America/Bogota" date +%H)
         IS_HARVEST_WEEK=$(cat config/harvest_calendar.json | jq -r --arg today "$(date +%F)" '.[$today] // "false"')

         if [ "$IS_HARVEST_WEEK" = "true" ] && [ "$CURRENT_HOUR" -ge 5 ] && [ "$CURRENT_HOUR" -lt 18 ]; then
           if [ "$FORCE_EMERGENCY_OVERRIDE" != "true" ]; then
             echo "ERROR: Change Freeze activo en semana de cosecha entre 05:00 y 18:00 COT. Despliegue cancelado."
             exit 1
           fi
         fi
         terraform apply -auto-approve tfplan
         ```
- **Entregables:** Archivo `.github/workflows/iac-pipeline.yml` funcional y validado.
- **Criterio de Aceptación (DoD):** Un commit en horario diurno durante semana de cosecha debe abortar automáticamente el job de despliegue a producción en el pipeline; el pipeline utiliza tokens OIDC efímeros.
- **Estimación:** 14 horas (imputables a las 100h).

---

## 7. Fase 4: Observabilidad, SLOs y Confiabilidad (SRE)

### TSK-04-01: Instrumentación de SLOs/SLIs y Monitoreo de Alertas Agronómicas

- **Fase:** Fase 4 (Observabilidad).
- **Responsable:** SRE / Cloud Engineer.
- **Precondiciones:** Ingesta y base de datos desplegadas en ambiente de pruebas.
- **Descripción Técnica Paso a Paso:**
  1. Instrumentar el **SLO 1: Entrega de Alerta de Cultivo**:
     - _SLI:_ Porcentaje de alertas críticas notificadas en menos de 5 minutos desde la lectura fuera de rango cuando existe red disponible (o dentro de las 24 horas al drenar el buffer).
     - _Fórmula:_
       $$\text{SLI}_{\text{alerta}} = \frac{\text{Alertas entregadas en } \le 5\text{ min}}{\text{Total de lecturas fuera de rango}} \times 100 \ge 99,0\%$$
     - _Implementación:_ Métrica personalizada en CloudWatch (`AromaPacifico/AlertLatency`) calculada por la diferencia entre `ingest_timestamp` y `device_reading_timestamp`.
  2. Instrumentar el **SLO 2: Disponibilidad de la Consulta Pública del Saco**:
     - _SLI:_ Porcentaje de solicitudes exitosas (código HTTP 2xx/3xx) sobre la API de consulta pública en periodos de 30 días.
     - _Fórmula:_
       $$\text{SLI}_{\text{consulta}} = \frac{\text{Requests HTTP 2xx/3xx}}{\text{Total Requests válidos}} \times 100 \ge 99,9\%$$
     - _RPO:_ 15 minutos (respaldado por PITR en DynamoDB).
     - _RTO:_ 4 horas (tiempo máximo de restauración del portal público ante desastre de región).
- **Entregables:** Alarmas y métricas declaradas en `terraform/modules/observability/slos.tf`.
- **Criterio de Aceptación (DoD):** Las métricas de latencia de alerta y disponibilidad de consulta se registran y emiten alertas a SNS si el presupuesto de error (_Error Budget_) se agota.
- **Estimación:** 6 horas.

---

### TSK-04-02: Configuración de Alarmas Operativas y Dashboards de Control

- **Fase:** Fase 4 (Observabilidad).
- **Responsable:** SRE / Cloud Engineer.
- **Precondiciones:** TSK-04-01 completada.
- **Descripción Técnica Paso a Paso:**
  1. Configurar alarmas operativas críticas en Amazon CloudWatch:
     - _Alarma 1 (Fincas caídas):_ Notificar si un `FincaID` no registra telemetría durante más de **24 horas consecutivas** (detección de batería agotada o falla de hardware en finca).
     - _Alarma 2 (Vuelos sin registro):_ Alarma si una orden de fumigación permanece en estado `EN_VUELO` por más de 6 horas sin recibir la bitácora `.log` de cierre.
     - _Alarma 3 (Fallas de Inferencia):_ Alarma si la Dead-Letter Queue `dlq-lambda-inference` contiene mensajes no procesados (>0 mensajes por 5 min).
  2. Diseñar el **Dashboard Operativo**:
     - Vista en tiempo real de transacciones por segundo (TPS), estado de los tres enlaces IPsec de acopios (Cauca, Huila, Tolima), estado de batería reportado por fincas y volumen de sacos recibidos al día.
  3. Diseñar el **Dashboard FinOps**:
     - Particionado por las etiquetas obligatorias: `FincaID`, `DronID`, `AcopioID`, `ViajeID` y `Ambiente`, proyectando el gasto acumulado del mes frente al presupuesto federativo.
- **Entregables:** Dashboards definidos en código JSON de CloudWatch en `docs/dashboards/`.
- **Criterio de Aceptación (DoD):** El panel muestra la segmentación de costos por etiqueta y la alarma de desconexión de 24 horas se activa correctamente en simulación.
- **Estimación:** 6 horas.

---

## 8. Fase 5: Diligenciamiento de Release Notes y Procedimientos de Rollback (Entregable 4)

### TSK-05-01: Diligenciamiento de Plantilla de Release Notes - Aplicación

- **Fase:** Fase 5 (Releases).
- **Responsable:** DevOps Lead / Backend Developer.
- **Precondiciones:** Plantilla `agentes/templates/RELEASE_NOTES_APPLICATION_TEMPLATE.md` disponible.
- **Descripción Técnica Paso a Paso:**
  1. Tomar como base `agentes/templates/RELEASE_NOTES_APPLICATION_TEMPLATE.md` y generar el documento diligenciado `docs/releases/RELEASE_NOTES_APP_v1.4.2.md`.
  2. Diligenciar exhaustivamente todos los campos obligatorios:
     - _ID de Release:_ `REL-APP-20261104-01`.
     - _Aplicación:_ Servicio de Consulta Web del Saco y Alertas.
     - _Versión:_ `v1.4.2`.
     - _Ventana de Despliegue:_ 19:30 - 20:15 COT (cumpliendo la prohibición de desplegar entre 05:00 y 18:00 en cosecha).
     - _Alcance:_ Implementación de la proyección segura que suprime la cédula del caficultor y la traza de transporte hacia el comprador.
     - _Impacto:_ Cero downtime (Rolling update en microservicios/Lambda).
     - _Aprobación:_ Aprobado por el Arquitecto Delegado de la FNC.
     - _Aviso a la Federación:_ Radicado formal `FNC-CHG-9412`.
     - _Procedimiento de Rollback:_ Comando exacto de reversión de versión en API Gateway / Lambda alias y verificación con pruebas de humo.
- **Entregables:** Documento `RELEASE_NOTES_APP_v1.4.2.md` formalizado.
- **Criterio de Aceptación (DoD):** El release note cumple al 100% con la estructura de la plantilla y detalla de punta a punta el plan de contingencia y vuelta atrás.
- **Estimación:** 3 horas.

---

### TSK-05-02: Diligenciamiento de Plantilla de Release Notes - Infraestructura

- **Fase:** Fase 5 (Releases).
- **Responsable:** DevOps Lead / Network Engineer.
- **Precondiciones:** Plantilla `agentes/templates/RELEASE_NOTES_INFRASTRUCTURE_TEMPLATE.md` disponible.
- **Descripción Técnica Paso a Paso:**
  1. Tomar como base `agentes/templates/RELEASE_NOTES_INFRASTRUCTURE_TEMPLATE.md` y generar el documento diligenciado `docs/releases/RELEASE_NOTES_INFRA_20261110-02.md`.
  2. Diligenciar exhaustivamente todos los campos obligatorios:
     - _ID de Release:_ `REL-INFRA-20261110-02`.
     - _Componente:_ Firewall de Perímetro Acopio Cauca y Reglas de Ingesta Nube.
     - _Módulo IaC:_ `terraform/modules/security` y configuración de firewall en borde `10.41.20.1`.
     - _Ventana de Despliegue:_ 21:00 - 22:30 COT (nocturna, fuera de horario de cosecha).
     - _Alcance:_ Apertura de puerto HTTPS 443 exclusivo hacia el endpoint de carga de drones y endurecimiento del aislamiento de la VLAN de Visitantes (`10.41.5.0/24`).
     - _Impacto:_ Corte transitorio del túnel IPsec de 45 segundos; los puestos de acopio persisten en servidores locales (`10.41.10.0/24`) sin pérdida de sacos.
     - _Aviso a la Federación:_ Radicado `FNC-SEC-1044` enviado con 48 horas de anticipación.
     - _Procedimiento de Rollback:_ Reversión de commit en Terraform (`git checkout tags/v1.3.0-infra && terraform apply`) y restauración de configuración en firewall local.
- **Entregables:** Documento `RELEASE_NOTES_INFRA_20261110-02.md` formalizado.
- **Criterio de Aceptación (DoD):** Documento diligenciado sin campos pendientes, con comandos de rollback verificables y tiempos de recuperación definidos.
- **Estimación:** 3 horas.

---

## 9. Fase 6: Dossier FinOps y Sistema de Diseño (Épica 7 - Entregables 5 y 6)

### TSK-06-01: Documento Formal de Costos FinOps a Precios 2026

- **Fase:** Fase 6 (FinOps & Diseño).
- **Responsable:** FinOps Practitioner / Cloud Architect.
- **Precondiciones:** Dimensionamiento técnico de `Propuestas-de-Tecnologias.md`.
- **Descripción Técnica Paso a Paso:**
  1. Estructurar el documento formal `docs/finops/MODELO_COSTOS_2026.md`:
     - _Modelo de Hardware Finca:_ Bill of Materials (BOM) detallado para 200 fincas con precios en COP y USD (LilyGO ESP32-S3 + SIM7080G, sensor Modbus 7-en-1, batería LiFePO4, panel solar 10W, gabinete IP67, SIM M2M). Inversión total: **\$39.390 USD** (~$808.000 COP/finca).
     - _Factura Cloud en Mes Normal:_ Ingesta de 252k msgs, DynamoDB On-Demand, Lambda Graviton2, CloudWatch, KMS y VPNs = **\$78,60 USD/mes** (o **\$6,60 USD/mes** si se usa IoT Greengrass en vez de VPN dedicada).
     - _Factura Cloud en Mes de Cosecha:_ Ingesta de 324k msgs, inferencia de 800 imágenes en Rekognition, transferencias de sacos = **\$82,08 USD/mes** (o **\$10,08 USD/mes** sin VPN).
     - _Retención a 5 Años:_ Transición automatizada de datos fríos hacia **S3 Glacier Deep Archive** (\$0,00099/GB-mes) acumulando menos de **\$0,59 USD/mes** para 600 GB de fotos y telemetría.
     - _Campaña de Drones (DaaS):_ Modelo de contratación por servicio a \$20 USD/hectárea vs. CapEx de \$18.000 USD por dron propio.
  2. Documentar formalmente las **Tres Decisiones Clave que Reducen y Evitan Gasto** exigidas por los criterios de evaluación.
- **Entregables:** Dossier de costos completo y justificado en `docs/finops/MODELO_COSTOS_2026.md`.
- **Criterio de Aceptación (DoD):** Todos los valores cuentan con fuentes públicas verificadas de 2026 y la tasa representativa del mercado (TRM) oficial colombiana se encuentra declarada.
- **Estimación:** 8 horas.

---

### TSK-06-02: Creación de la Lámina del Sistema de Diseño Accesible para Campo

- **Fase:** Fase 6 (FinOps & Diseño).
- **Responsable:** UI/UX Designer / Frontend Architect.
- **Precondiciones:** Requisitos de usabilidad del enunciado oficial.
- **Descripción Técnica Paso a Paso:**
  1. Elaborar el documento y lámina visual `docs/design/SISTEMA_DISENO.md`:
     - _Identidad de Marca:_ Isotipo del grano de café con ondas telemáticas, versiones en positivo, monocromático y negativo.
     - _Paleta Cromática Semántica:_
       - Primario: Verde Cafetal (`#1B4D3E`).
       - Secundario: Ocre / Tostión (`#C4823F`).
       - Neutros: Blanco Puro (`#FFFFFF`), Fondo Pantalla (`#F8FAFC`), Texto Principal (`#0F172A`).
       - Estados del Saco: En preparación (`#E2E8F0`), En viaje (`#3B82F6`), Aceptado acopio (`#10B981`), Rechazado acopio (`#EF4444`), Entregado puerto (`#6366F1`).
       - Alerta de Cultivo: Ámbar Crítico (`#F59E0B`) y Rojo Emergencia (`#DC2626`).
     - _Tipografía:_ Familia sans-serif legible en pantallas pequeñas (Inter o Roboto), escalas móviles de 14px a 24px.
     - _Ergonomía de Campo y Accesibilidad Solar:_
       - Ratio de contraste mínimo **WCAG 2.1 AAA ($\ge 7:1$)** para visualización bajo radiación solar directa en cafetales.
       - Áreas táctiles mínimas de 48x48 dp para operación con manos húmedas o guantes de recolección.
       - Iconografía intuitiva sin tecnicismos ("Gota" para humedad, "Termómetro" para calor, "Saco" para pesaje).
     - _Componentes Base:_ Botón táctil primario, campo de captura numérica simple, tarjeta de estado del saco con distintivo de color, banner de alerta agronómica y modal de confirmación.
     - _Vista Sanitizada del Comprador:_ Layout web limpio, enfocado exclusivamente en las variables de calidad del grano.
- **Entregables:** Especificación y lámina de componentes UI en markdown/SVG en `docs/design/SISTEMA_DISENO.md`.
- **Criterio de Aceptación (DoD):** El sistema de diseño no hereda el manual obsoleto de 2020 y resuelve los problemas de visibilidad bajo luz solar directa.
- **Estimación:** 8 horas.

---

## 10. Fase 7: Preparación de la Sustentación Técnica y Cierre (Entregables 7 y 8)

### TSK-07-01: Elaboración de la Presentación Técnica Ejecutiva

- **Fase:** Fase 7 (Sustentación).
- **Responsable:** DevOps Lead / Cloud Architect.
- **Precondiciones:** Todos los entregables técnicos de las fases 1 a 6 aprobados.
- **Descripción Técnica Paso a Paso:**
  1. Diseñar el diapositivero ejecutivo (PDF / Slides) estructurado para una defensa de **exactamente 20 minutos**:
     - _Slide 1:_ Portada institucional: Actualización de la Plataforma AromaPacífico (FNC 2026).
     - _Slide 2:_ Ruptura 2020 vs 2026: Por qué el diseño anterior no funcionó y cómo cerramos la brecha rural.
     - _Slide 3:_ Arquitectura Global Cloud/IoT: Vista en 4 capas y topología híbrida (con el diagrama PNG oficial).
     - _Slide 4:_ Conectividad y Resiliencia en el Edge: El patrón Store-and-Forward de 24h y hardware de bajo costo.
     - _Slide 5:_ Red de Centros de Acopio: Segmentación `10.41/42/43`, aislamiento de visitantes y salida WAN de 100 Mbps.
     - _Slide 6:_ Subsistema Aeronáutico de Drones: Los 5 servicios, precarga offline y la compuerta de aprobación humana obligatoria.
     - _Slide 7:_ Trazabilidad del Saco y Privacidad: Ciclo de vida, RPO de 15m, RTO de 4h y enmascaramiento de PII.
     - _Slide 8:_ Inferencia Serverless Ética: Lambda Arm64, Rekognition y protocolo de protección de datos personales.
     - _Slide 9:_ Demostración de IaC (Épica 6): Módulos de Terraform, pipeline CI/CD y enforcement del Change Freeze.
     - _Slide 10:_ Justificación del Timebox de 100 Horas: WBS, responsabilidades y trazabilidad estricta al diagrama.
     - _Slide 11:_ Modelo FinOps y TCO: Presupuesto normal vs. cosecha, BOM de fincas y las 3 decisiones de ahorro.
     - _Slide 12:_ Conclusiones y Compromisos de Nivel de Servicio (SLOs/SLIs).
- **Entregables:** Diapositivas ejecutivas en `docs/sustentacion/PRESENTACION_AROMAPACIFICO.pdf`.
- **Criterio de Aceptación (DoD):** La presentación contiene la totalidad de los puntos evaluados por la FNC y puede ser expuesta de manera rigurosa en 20 minutos de reloj.
- **Estimación:** 6 horas.

---

### TSK-07-02: Preparación del Guion de Defensa y Banco de Preguntas Críticas

- **Fase:** Fase 7 (Sustentación).
- **Responsable:** Equipo Completo (Lead, Architect, Security, FinOps).
- **Precondiciones:** Diapositivas terminadas.
- **Descripción Técnica Paso a Paso:**
  1. Redactar el guion de sustentación técnica con distribución de tiempos:
     - Minutos 0 - 3: Introducción, contexto 2026 y decisiones estratégicas.
     - Minutos 3 - 8: Redes, conectividad Store-and-Forward y subsistema de drones.
     - Minutos 8 - 14: Demostración del código IaC, pipeline CI/CD y sustento de por qué cabe en 100 horas.
     - Minutos 14 - 18: Análisis FinOps, costos comparativos y privacidad ética.
     - Minutos 18 - 20: Conclusión y apertura a preguntas.
  2. Preparar el **Banco de Respuestas Técnicas para los 30 Minutos de Aclaraciones** (simulando los cuestionamientos del Arquitecto de la Federación):
     - _Pregunta 1:_ ¿Por qué no usar LoRaWAN o satelital en las 200 fincas? $\rightarrow$ _Defensa:_ CapEx de antenas satelitales supera \$600 USD por finca; LoRaWAN requiere gateways comunitarios que violan la restricción de "instalar en una sola visita y con poco hardware". LTE-M/NB-IoT aprovecha la red celular existente con inversión mínima de \$145 USD.
     - _Pregunta 2:_ ¿Cómo garantizan que la inferencia de IA no fumigue zonas habitadas? $\rightarrow$ _Defensa:_ Demostración de la compuerta humana: ningún disparador automático puede mutar el estado a `AUTORIZADA`; se requieren credenciales firmadas de un agrónomo humano y el polígono previo de exclusión.
     - _Pregunta 3:_ ¿Por qué la Épica 6 solo codifica una función serverless y un módulo de finca? $\rightarrow$ _Defensa:_ Rigor de alcance. Intentar programar las 4 funciones o 200 fincas viola el límite de 100 horas. Se entrega el patrón reproducible, escalable y modular.
- **Entregables:** Documento `docs/sustentacion/GUION_Y_BANCO_PREGUNTAS.md`.
- **Criterio de Aceptación (DoD):** El equipo domina las respuestas a las tres preguntas críticas exigidas por el enunciado (conectividad, drones y viabilidad de 100h en IaC).
- **Estimación:** 4 horas.

---

## 11. Matriz de Trazabilidad entre Tareas, Entregables y Criterios FNC

| Tarea              | Entregable Oficial Asociado                | Criterio de Éxito FNC Evaluado                                      |
| :----------------- | :----------------------------------------- | :------------------------------------------------------------------ |
| **TSK-00-01 / 02** | Repositorio Base y Gobernanza              | Criterio 4: Automatización y cambio                                 |
| **TSK-01-01 / 02** | Documento de Arquitectura y Redes          | Criterio 1: Estrategia coherente / Criterio 2: Conectividad cerrada |
| **TSK-01-03 / 04** | Especificaciones IoT y Drones              | Criterio 2: Conectividad / Criterio 3: Viabilidad de vuelo          |
| **TSK-01-05**      | Trazabilidad del Saco                      | Criterio 5: Seguridad y vista del comprador                         |
| **TSK-01-06**      | Diagramas Oficiales PNG                    | Criterio 1: Estrategia actualizada                                  |
| **TSK-02-01**      | Plan de 100 Horas (WBS)                    | Criterio 3: Viabilidad de IaC $\le 100$ horas y 2 semanas           |
| **TSK-03-01 a 07** | Repositorio de Infraestructura como Código | Criterio 4: Código coincide con diagrama y change freeze            |
| **TSK-04-01 / 02** | Observabilidad y SLOs                      | Criterio 1: Compromisos de servicio formalizados                    |
| **TSK-05-01 / 02** | Plantillas de Release Notes Diligenciadas  | Criterio 4: Plantillas de cambio y vuelta atrás                     |
| **TSK-06-01**      | Documento de Costos FinOps                 | Criterio 6: Costo actual y tres decisiones de ahorro                |
| **TSK-06-02**      | Sistema de Diseño en Lámina                | Criterio 7: Sistema de diseño aplicado                              |
| **TSK-07-01 / 02** | Presentación y Sustentación (20 min)       | Criterio 8: Claridad de la sustentación técnica                     |
