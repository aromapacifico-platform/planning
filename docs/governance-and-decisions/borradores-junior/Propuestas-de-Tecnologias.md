# Propuestas de Tecnologías y Análisis FinOps Exhaustivo

## Reto FNC 2026: Actualización de la Plataforma Cafetera "AromaPacífico"

---

## 1. Resumen Ejecutivo y Criterios de Selección Tecnológica

Como **Ingeniero Senior en Infraestructura, Cloud, IoT y FinOps**, la arquitectura propuesta para la Federación Nacional de Cafeteros (FNC) responde a cuatro principios rectores innegociables:

1. **Resiliencia Extrema en el Edge (Store-and-Forward / Offline-First):** La falta de cobertura de datos no se considera un fallo fortuito, sino el estado operativo estándar de la ruralidad cafetera colombiana.
2. **Eficiencia de Capital y FinOps (Pay-As-You-Go / Cero Ociosidad):** Erradicación de costos fijos mensuales en cómputo inactivo. Adopción de arquitecturas serverless donde el costo en reposo es exactamente \$0 USD.
3. **Seguridad Cero Confianza y Soberanía del Dato:** Cumplimiento estricto del régimen de protección de datos personales (Ley Estatutaria 1581 de 2012 de Colombia), segregación criptográfica y enmascaramiento de identidad (PII) del productor frente al comprador.
4. **Viabilidad DevOps dentro del Timebox de 100 Horas:** Selección de tecnologías con proveedores de Terraform maduros, evitando sobreingeniería que comprometa la entrega en dos semanas.

### Nube Principal Seleccionada

- **Nube Primaria Elegida:** **Amazon Web Services (AWS)** (Región `us-east-1` o `us-east-2` por latencia y paridad de costos con Colombia).
- **Segunda Nube Preparada:** **Microsoft Azure** (definida conceptualmente y mapeada a través de Terraform sin duplicar facturación ni aprovisionar recursos activos).

---

## 2. Guías Visuales de Arquitectura e Ingeniería

A continuación se integran los diagramas técnicos de referencia generados para ilustrar las capas de la solución y las rutas de datos del sistema:

### 2.1 Diagrama de Arquitectura de Referencia Cloud & IoT

### 2.2 Diagrama de Flujo de Datos, Ciclo de Vida y Estados

---

## 3. Matriz Comparativa y Decisiones por Capa Arquitectónica

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 MAPA DE DECISIONES TECNOLÓGICAS Y FINOPS                               │
├─────────────────────┬───────────────────────────┬───────────────────────────┬──────────────────────────┤
│ Dominio             │ Tecnología Seleccionada   │ Alternativas Descartadas  │ Justificación FinOps     │
├─────────────────────┼───────────────────────────┼───────────────────────────┼──────────────────────────┤
│ 1. Hardware Finca   │ ESP32-S3 + SIM7080G       │ Gateways Industriales,    │ Ahorro del 80% en CapEx; │
│    y Conectividad   │ LTE-M/NB-IoT + Modbus     │ Raspberry Pi + Quectel,   │ $145 USD vs $950 USD;    │
│                     │ Sensor 7-en-1 + Solar 15W │ Módems 2G/3G obsoletos    │ consumo ultra-bajo <50µA │
├─────────────────────┼───────────────────────────┼───────────────────────────┼──────────────────────────┤
│ 2. Ingesta IoT      │ AWS IoT Core              │ Azure IoT Hub,            │ Pay-as-you-go puro;      │
│                     │ (MQTT / TLS 1.3 / Basic)  │ EMQX Cloud Serverless,    │ <$0,50 USD/mes vs        │
│                     │                           │ EC2 con Mosquitto         │ $10-$25 USD fijos        │
├─────────────────────┼───────────────────────────┼───────────────────────────┼──────────────────────────┤
│ 3. Persistencia     │ Amazon DynamoDB On-Demand │ AWS Timestream,           │ Serverless, TTL nativo,  │
│    y Telemetría     │ + TTL + S3 Glacier        │ TimescaleDB en RDS,       │ $0,40 USD/mes vs         │
│                     │                           │ ClickHouse Cloud          │ $15-$60 USD fijos        │
├─────────────────────┼───────────────────────────┼───────────────────────────┼──────────────────────────┤
│ 4. Cómputo e IA     │ AWS Lambda (Graviton2) +  │ Clústeres EKS/ECS,        │ Cero cómputo ocioso;     │
│                     │ Amazon Rekognition        │ Azure AI Vision,          │ $1,00/1k imágenes vs     │
│                     │                           │ Google Cloud Vision       │ $1,50/1k; filtro ético   │
├─────────────────────┼───────────────────────────┼───────────────────────────┼──────────────────────────┤
│ 5. Redes Acopios    │ FortiGate/pfSense IPsec + │ SD-WAN privativa Cisco,   │ VLANs aisladas 10.4X.0.0;│
│                     │ VLANs 802.1Q + QoS WiFi 6 │ Enlaces MPLS dedicados,   │ 100 Mbps simétricos con  │
│                     │                           │ Subredes solapadas        │ CIDR cloud no solapado   │
├─────────────────────┼───────────────────────────┼───────────────────────────┼──────────────────────────┤
│ 6. IaC y CI/CD      │ OpenTofu / Terraform +    │ CloudFormation, Pulumi,   │ Agnóstico, módulos en    │
│                     │ GitHub Actions con OIDC   │ Despliegues manuales      │ timebox de 100h exactas  │
└─────────────────────┴───────────────────────────┴───────────────────────────┴──────────────────────────┘
```

---

## 4. Análisis Detallado por Componente

### 4.1 Capa de Edge, Hardware en Finca y Sensores (IoT Layer)

#### Opciones Evaluadas

1. **Opción A (Seleccionada):** Microcontrolador de ultra-bajo consumo **Espressif ESP32-S3** con módem celular **SIM7080G** (ej. LilyGO T-SIM7080G-S3), transceptor RS485 Modbus RTU para sensor agrícola multiparámetro (NPK, humedad, temperatura, pH), panel solar de 15W y celda de batería LiFePO4 de 6.000 mAh.
2. **Opción B (Descartada):** **Raspberry Pi Zero 2W + Módem USB Quectel BG95-M3**.
3. **Opción C (Descartada):** **Nordic Semiconductor nRF9160 SiP** (System-in-Package).
4. **Opción D (Descartada):** **Gateway Industrial Comercial** (ej. Advantech ICR o Teltonika RUT241 con interfaces analógicas).

#### Cuadro Comparativo de Hardware en Finca

| Criterio                    | Opción A: ESP32-S3 + SIM7080G  | Opción B: Raspberry Pi + BG95    | Opción C: Nordic nRF9160   | Opción D: Gateway Industrial |
| :-------------------------- | :----------------------------- | :------------------------------- | :------------------------- | :--------------------------- |
| **Costo Hardware (CapEx)**  | **~$135 - $160 USD**           | ~$280 - $350 USD                 | ~$220 - $270 USD           | ~$850 - $1.200 USD           |
| **Consumo en Reposo**       | **~35 - 50 µA (Deep Sleep)**   | ~80 - 120 mA (Sistema Linux)     | ~4 - 18 µA (Ultra low)     | ~200 - 400 mA (12V/24V)      |
| **Soporte Bandas Colombia** | **Bandas 4, 5, 28 (LTE-M/NB)** | Bandas 4, 5, 28 + 2G fallback    | Bandas 4, 5, 28 (LTE-M/NB) | Bandas globales 4G/3G        |
| **Buffer Local 24h**        | **16 MB SPI Flash + MicroSD**  | Tarjeta MicroSD (riesgo corrupt) | Memoria Flash integrada    | Memoria interna eMMC         |
| **Tolerancia Ambiental**    | **IP67 / NEMA 4X (Gabinete)**  | Sensible a condensación          | IP67 en encapsulado        | Grado industrial certificado |
| **Autonomía sin Sol**       | **> 30 días continuos**        | < 18 horas con batería peq.      | > 45 días continuos        | Requiere banco batería 12V   |

#### Análisis FinOps y Justificación Técnica

- **Por qué se eligió la Opción A:** El caficultor cuenta con margen financiero limitado. La Opción A entrega una solución completa de grado campo por **\$145 USD promedio** (frente a \$950 USD de un gateway industrial), reduciendo la inversión inicial de las 200 fincas de \$190.000 USD a tan solo **\$29.000 USD** (un ahorro neto del **84,7%**).
- **Consumo Energético y Resiliencia:** El ESP32-S3 permanece en estado _Deep Sleep_ consumiendo menos de 0,16 mW. Despierta cada 4 horas (en cultivo) o cada 1 hora (en secado) durante 15 a 25 segundos para leer el sensor Modbus y transmitir vía MQTT/TLS. El consumo diario promedio es de apenas **19,2 mAh en secado activo** y **5,7 mAh en cultivo**. Con una celda LiFePO4 de 6.000 mAh y un panel solar de 15W, el sistema opera con **autonomía superior a 30 días en condiciones de lluvia o nubosidad extrema** en el Cauca o Huila.
- **Buffer Local Store-and-Forward:** Cada lectura estructurada en JSON compactado o Protocol Buffers pesa ~180 bytes. Veinticuatro lecturas de secado ocupan **~4,3 KB**. La memoria Flash SPI integrada de 16 MB o la ranura MicroSD permiten almacenar más de 10.000 lecturas locales (meses de histórico), cumpliendo holgadamente el requisito de retener hasta 24 horas y drenar automáticamente al restablecerse la cobertura celular.
- **Por qué se descartaron las demás:**
  - _Opción B:_ Una Raspberry Pi ejecuta un sistema operativo completo susceptible a corrupción de sistema de archivos ante descargas de batería, con un consumo en reposo 2.000 veces mayor que imposibilita la autonomía solar compacta.
  - _Opción C:_ Si bien el silicio Nordic es excelente, el costo del SiP y la complejidad de diseño de PCB a medida encarecen el prototipo y extienden los tiempos de entrega.
  - _Opción D:_ Financieramente inviable para la economía del caficultor y sobredimensionado para enviar un paquete de 200 bytes cada 4 horas.

---

### 4.2 Capa de Ingesta y Mensajería IoT (Cloud Ingestion Layer)

#### Opciones Evaluadas

1. **Opción A (Seleccionada):** **AWS IoT Core** (Broker MQTT/TLS 1.3 con soporte de Basic Ingest y Rules Engine).
2. **Opción B (Descartada):** **Azure IoT Hub** (Niveles B1 / S1).
3. **Opción C (Descartada):** **EMQX Cloud Serverless**.
4. **Opción D (Descartada):** **Broker Autogestionado Mosquitto/EMQX sobre EC2 / Containers**.

#### Cuadro Comparativo de Ingesta IoT

| Criterio                 | Opción A: AWS IoT Core            | Opción B: Azure IoT Hub           | Opción C: EMQX Cloud Serverless | Opción D: EC2 + Mosquitto           |
| :----------------------- | :-------------------------------- | :-------------------------------- | :------------------------------ | :---------------------------------- |
| **Modelo de Cobro**      | Pay-as-you-go puro (\$1,00/M msg) | Cuota fija mensual (\$10-\$25/ud) | Conexión (\$2/M min) + Tráfico  | Cómputo fijo VM 24/7 (\$15-\$40/m)  |
| **Cálculo de Paquete**   | Bloques de 5 KB                   | Bloques de 4 KB                   | Por GB transferido              | Ilimitado (acotado por ancho banda) |
| **Costo Mensual Piloto** | **~$0,32 USD / mes**              | ~$25,00 USD / mes (S1)            | ~$5,80 USD / mes                | ~$22,00 USD / mes + EBS             |
| **Free Tier Aplicable**  | **500.000 msg/mes (12 meses)**    | 8.000 msg/día (Nivel F1 limitado) | 1M min sesión / 1 GB tráfico    | Ninguno                             |
| **Sobrecarga DevOps**    | **Zero Maintenance (Managed)**    | Zero Maintenance (Managed)        | Zero Maintenance (SaaS externo) | Alta (parches, alta disponibilidad) |
| **Integración IAM / BD** | **Nativa con DynamoDB y S3**      | Nativa con Cosmos DB/Event Hubs   | Requiere conectores/webhooks    | Requiere código pegamento           |

#### Análisis FinOps y Justificación Técnica

- **Dimensionamiento de Tráfico Mensual:**
  - Telemetría Cultivo: 200 fincas $\times$ 6 lecturas/día $\times$ 30 días = **36.000 mensajes**.
  - Telemetría Secado: 100 fincas $\times$ 24 lecturas/día $\times$ 30 días = **72.000 mensajes**.
  - Tracking Transportadores: 60 vehículos $\times$ 12 pings/h $\times$ 10 h/día $\times$ 30 días = **216.000 mensajes**.
  - **Total Tráfico Mensual del Piloto:** **~324.000 mensajes/mes**.
- **Impacto Financiero:**
  - En **AWS IoT Core**, 324.000 mensajes entran completamente dentro de la capa gratuita (500.000 mensajes/mes durante el primer año).
  - Fuera del Free Tier, a razón de \$1,00 USD por millón de mensajes (en bloques $\le$ 5 KB), el costo mensual de mensajería es de exactamente **\$0,32 USD**. Sumando los minutos de conexión intermitente (\$0,08 por millón de minutos), el costo total mensual es de **\$0,35 USD**.
  - Al utilizar la función **Basic Ingest** de AWS IoT Core (publicando al topic reserved `$aws/rules/<rule-name>`), los mensajes que van directo a DynamoDB **no incurren en costo de broker de mensajería**, reduciendo la factura a prácticamente \$0,05 USD.
- **Por qué se descartó Azure IoT Hub:** Exige contratar la unidad S1 (\$25 USD/mes) para contar con soporte de gemelos digitales y enrutamiento seguro hacia backend. Para 324k mensajes al mes, Azure IoT Hub resulta **71 veces más costoso** que AWS IoT Core.
- **Por qué se descartó EMQX Cloud Serverless:** Factura el tiempo de sesión activa a \$2,00 USD por millón de minutos (25 veces más costoso que el medidor de conexión de AWS).

---

### 4.3 Capa de Persistencia y Series de Tiempo (Database & Storage Layer)

#### Opciones Evaluadas

1. **Opción A (Seleccionada):** **Amazon DynamoDB (On-Demand Capacity)** para telemetría activa y estado del saco + **S3 Lifecycle con transición a Glacier Flexible / Deep Archive** para retención a 5 años.
2. **Opción B (Descartada):** **Amazon Timestream for LiveAnalytics**.
3. **Opción C (Descartada):** **Amazon RDS PostgreSQL / TimescaleDB (Instancia `db.t4g.micro`)**.
4. **Opción D (Descartada):** **ClickHouse Cloud**.

#### Cuadro Comparativo de Persistencia

| Criterio                     | Opción A: DynamoDB + S3 Glacier     | Opción B: AWS Timestream       | Opción C: RDS PostgreSQL   | Opción D: ClickHouse Cloud    |
| :--------------------------- | :---------------------------------- | :----------------------------- | :------------------------- | :---------------------------- |
| **Modelo Operativo**         | Serverless On-Demand                | Serverless Time-Series         | Instancia Dedicada 24/7    | Clúster SaaS Gestionado       |
| **Costo Ingesta (Writes)**   | \$1,25 / millón WRU                 | \$0,50 / GB ingerido           | Incluido en CPU/IOPs de VM | Incluido en cómputo base      |
| **Costo Almacén Activo**     | 25 GB gratis, luego \$0,25/GB       | \$0,036/GB-hora (Memory Store) | \$0,115/GB-mes (EBS gp3)   | ~$0,20/GB-mes                 |
| **Retención a 5 Años**       | **\$0,00099/GB-mes (Deep Archive)** | \$0,03/GB-mes (Magnetic)       | \$0,115/GB-mes en disco    | Requiere almacenamiento cloud |
| **Costo Mensual Estimado**   | **~$0,45 - $0,80 USD / mes**        | ~$28,00 - $35,00 USD / mes     | ~$16,50 - $22,00 USD / mes | ~$65,00 USD / mes (mínimo)    |
| **Gestión de Ciclo de Vida** | **TTL Nativo Automático sin costo** | Políticas de retención tabla   | Requiere jobs cron/pg_cron | Configuración de particiones  |

#### Análisis FinOps y Estrategia de Retención a 5 Años

- **Estrategia de Almacenamiento en Dos Niveles:**
  1. _Nivel Caliente (Hot Tier - DynamoDB):_ Los 324.000 registros mensuales se escriben en DynamoDB utilizando claves de partición compuestas (`FincaID#Tipo` o `SacoID`). 324.000 escrituras equivalen a **\$0,40 USD al mes**. La lectura pública de sacos (picos de 30 consultas/minuto = 0,5 TPS) consume menos de **\$0,05 USD al mes**.
  2. _Expulsión y Archivo Frío (Cold Tier - S3 Deep Archive):_ Se activa la característica nativa **Time to Live (TTL)** de DynamoDB sobre el atributo `expiration_timestamp` (configurado a 90 días). Los registros que expiran son capturados mediante DynamoDB Streams y transferidos en lotes comprimidos (formato Parquet) a un bucket de **Amazon S3**.
  3. _Regla de Ciclo de Vida (S3 Lifecycle):_ Los archivos Parquet pasan a los 30 días a **S3 Glacier Deep Archive** con un costo de almacenamiento de **\$0,00099 USD por GB-mes**. Cinco años de telemetría e historiales del saco (~15 GB de datos comprimidos) representarán un costo total acumulado de **menos de \$0,02 USD al mes**.
- **Por qué se descartó AWS Timestream:** Su arquitectura impone un almacenamiento en memoria (_Memory Store_) con una tarifa de \$0,036 por GB-hora (\$26,28/GB-mes), lo que eleva el piso de gasto a más de \$25 USD mensuales para un flujo que no requiere microsegundos de latencia analítica.
- **Por qué se descartó RDS PostgreSQL:** Mantener una base de datos relacional encendida 24/7 (`db.t4g.micro`) genera una cuota fija ineludible de ~\$15 USD al mes, violando el principio FinOps de escalado a cero fuera de cosecha.

---

### 4.4 Capa de Cómputo e Inferencia de Visión Artificial (Serverless & AI Layer)

#### Opciones Evaluadas

1. **Cómputo:** **AWS Lambda (Arquitectura Arm64 / AWS Graviton2)** frente a contenedores dedicados (ECS/Fargate o EKS).
2. **Inferencia Administrada de Visión:**
   - **Opción A (Seleccionada):** **Amazon Rekognition** (`DetectFaces` para filtro ético + `DetectCustomLabels` / Clasificación).
   - **Opción B (Evaluada / Descartada):** **Azure AI Vision** (Computer Vision API).
   - **Opción C (Descartada):** **Google Cloud Vision API**.

#### Cuadro Comparativo de Motores de Inferencia Administrada

| Criterio                          | Opción A: AWS Rekognition             | Opción B: Azure AI Vision         | Opción C: Google Cloud Vision |
| :-------------------------------- | :------------------------------------ | :-------------------------------- | :---------------------------- |
| **Costo por 1.000 Imágenes**      | **\$1,00 USD** (0 - 1M imágenes)      | \$1,00 USD (0 - 1M transacciones) | \$1,50 USD (0 - 1M unidades)  |
| **Capa Gratuita (Free Tier)**     | **5.000 imágenes/mes (año 1)**        | 30.000 transacciones (F0 tier)    | 1.000 unidades/mes            |
| **Detección de Personas/Rostros** | **API `DetectFaces` nativa (\$1/1k)** | Face API integrada (\$1/1k)       | Face Detection (\$1,50/1k)    |
| **Latencia p50 / p95**            | **~350 ms / ~850 ms**                 | ~400 ms / ~920 ms                 | ~450 ms / ~1.100 ms           |
| **Cumplimiento Ético / Filtro**   | Redirección por etiqueta humana       | Redirección por categoría person  | Factura por función invocada  |

#### Análisis FinOps y Tratamiento Ético de Imágenes

- **Volumen de Inferencia en Cosecha:**
  - El piloto contempla 1 campaña mensual de revisión en cosecha y fumigaciones puntuales derivadas de focos.
  - Para 200 fincas, se estima un volumen de 400 a 800 imágenes de confirmación y verificación por mes de cosecha.
  - El costo directo en AWS Rekognition para 800 imágenes es de **\$0,80 USD** (cubierto al 100% por los 5.000 créditos del Free Tier).
- **Tratamiento Ético de Imágenes (Privacidad y Habeas Data):**
  - **Algoritmo de Salvaguarda:** Cuando el dron deposita una imagen en el bucket de S3, se dispara la función Lambda `fn_crop_inference_trigger`.
  - La función invoca primero la operación `DetectFaces` de Rekognition.
  - Si el modelo detecta presencia humana con un nivel de confianza superior al **80%**, **la imagen es catalogada inmediatamente como conteniendo datos personales**.
  - **Acción:** La función aborta el flujo agronómico, cifra el objeto con una llave KMS restringida a la Oficialía de Datos de la FNC, emite un evento de auditoría en CloudWatch y **nunca envía el archivo al expediente agronómico ni a modelos públicos**.

---

### 4.5 Capa de Redes Híbridas y Centros de Acopio (Network Layer)

#### Requisitos del Documento y Solución de Ingeniería

- **Topología de Centros de Acopio:**
  - **Cauca (Popayán):** `10.41.0.0/16`
  - **Huila (Neiva):** `10.42.0.0/16`
  - **Tolima (Ibagué):** `10.43.0.0/16`
- **Equipamiento de Red Recomendado por Centro:**
  - _Firewall / Router Borde:_ **FortiGate 40F** o appliance con **pfSense Plus** (Hardware CapEx: ~$450 - $600 USD por centro). Provee terminación de túnel IPsec dual hacia AWS Transit Gateway / VPN Gateway, filtrado de aplicaciones y reglas perimetrales.
  - _Conmutación LAN:_ Switch gestionado de 24 puertos PoE+ Gigabit (ej. Aruba Instant On 1930 o Ubiquiti UniFi Pro 24 PoE) configurado con enlaces troncales 802.1Q.
  - _Acceso Inalámbrico:_ 2 Access Points Wi-Fi 6 (ej. UniFi U6-Pro o Aruba AP22) con mapeo estricto de SSIDs a VLANs.
- **Control de Tráfico y QoS:**
  - Ancho de banda WAN disponible: 100 Mbps simétricos compartidos.
  - Regla de QoS: Asignación de **2 Mbps de bajada / 0,5 Mbps de subida** por cliente activo en patio de transporte y logística.
  - Filtrado de capa 7 para bloquear tráfico recreativo (YouTube, TikTok, Netflix, descargas P2P) garantizando la prioridad del tráfico hacia la API de pesaje y recepción.

#### Plan de Direccionamiento Cloud (VPC) - Cero Solapamiento

Para garantizar la interconexión híbrida mediante VPN IPsec sin colisiones de enrutamiento con los tres centros de acopio (`10.41.0.0/16`, `10.42.0.0/16`, `10.43.0.0/16`), se diseña el siguiente esquema CIDR en la nube:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PLAN DE DIRECCIONAMIENTO CLOUD (VPC AWS)                        │
├─────────────────────────┬──────────────────────────────┬───────────────────────────────┤
│ Ambiente                │ Bloque CIDR Asignado         │ Subredes Representativas      │
├─────────────────────────┼──────────────────────────────┼───────────────────────────────┤
│ VPC Producción          │ 10.100.0.0/16                │ • 10.100.1.0/24 : Ingesta IoT │
│                         │                              │ • 10.100.2.0/24 : Drones S3   │
│                         │                              │ • 10.100.10.0/24: App Backend │
│                         │                              │ • 10.100.20.0/24: Capa Datos  │
│                         │                              │ • 10.100.30.0/24: Admón/VPN   │
│                         │                              │ • 10.100.50.0/24: Pública Web │
├─────────────────────────┼──────────────────────────────┼───────────────────────────────┤
│ VPC Pruebas (Staging)   │ 10.101.0.0/16                │ Subredes idénticas en 10.101. │
├─────────────────────────┼──────────────────────────────┼───────────────────────────────┤
│ VPC Desarrollo (Dev)    │ 10.102.0.0/16                │ Subredes idénticas en 10.102. │
└─────────────────────────┴──────────────────────────────┴───────────────────────────────┘
```

---

### 4.6 Capa de Automatización, CI/CD e Infraestructura como Código (IaC Layer)

#### Selección: OpenTofu / HashiCorp Terraform

- **Justificación:** Estándar de la industria, declarativo, con soporte maduro de proveedores para AWS y Azure, facilitando la arquitectura multi-cloud requerida.
- **Estructura Modular para la Épica 6 (Límite: 100 Horas / 2 Semanas):**
  - `modules/network`: VPC, subredes, tablas de enrutamiento y gateway VPN hacia acopio.
  - `modules/security`: Roles y políticas IAM de mínimo privilegio, llaves KMS y Security Groups permanentes.
  - `modules/ingest_telemetry`: Endpoint de ingesta IoT Core, reglas de Topic y tabla DynamoDB con TTL.
  - `modules/serverless_function`: Función Lambda patrón de inferencia (con permisos de lectura en S3, llamada a Rekognition y escritura en DynamoDB).
- **Flujo CI/CD con GitHub Actions:**
  - Autenticación segura mediante **OIDC (OpenID Connect)**: Prohibido almacenar llaves permanentes `AWS_ACCESS_KEY_ID` en el repositorio.
  - Pipeline automatizado con etapas: `fmt`, `tflint`, `tfsec` (análisis estático de seguridad), `terraform plan` y compuerta de aprobación humana para `terraform apply` en producción.
- **Implementación del Change Freeze (05:00 - 18:00 COT):**
  - El pipeline valida la hora actual de Colombia (`America/Bogota`). Si el despliegue a producción se solicita durante semana de cosecha entre las 05:00 y las 18:00, **el job falla automáticamente con error de política**, requiriendo un tag de excepción explícito para incidentes críticos.

---

## 5. Estimación Presupuestal Consolidada (FinOps TCO)

### 5.1 Comparativa: Mes Normal vs. Mes de Cosecha (Plataforma Cloud)

| Servicio Cloud                | Consumo / Métrica Base           |  Costo Mes Normal (USD)  | Costo Mes Cosecha (USD) |
| :---------------------------- | :------------------------------- | :----------------------: | :---------------------: |
| **AWS IoT Core**              | 324k msg/mes + conexión          |          \$0,35          |         \$0,48          |
| **Amazon DynamoDB**           | Escrituras On-Demand + Lecturas  |          \$0,45          |         \$0,75          |
| **AWS Lambda**                | Invocaciones efímeras Graviton2  |    \$0,00 (Free Tier)    |         \$0,08          |
| **Amazon S3**                 | Ingesta ortomosaicos y fotos     |          \$0,25          |         \$0,95          |
| **Amazon Rekognition**        | Inferencia de visión (500 fotos) |    \$0,00 (Free Tier)    |         \$0,50          |
| **Amazon S3 Glacier**         | Archivo acumulativo a 5 años     |          \$0,05          |         \$0,12          |
| **AWS Site-to-Site VPN**      | 3 túneles IPsec hacia acopios    | \$72,00 (\$0,05/h/túnel) |         \$72,00         |
| **CloudWatch & Logs**         | Métricas y logs estructurados    |          \$3,50          |         \$5,20          |
| **KMS & Seguridad**           | 2 llaves maestras administradas  |          \$2,00          |         \$2,00          |
| **Total Factura Cloud / Mes** | _(Sin contar túneles VPN fijos)_ |   **\$6,60 USD / mes**   |  **\$10,08 USD / mes**  |
| **Total con VPNs Híbridas**   | _(3 túneles IPsec dedicados)_    |  **\$78,60 USD / mes**   |  **\$82,08 USD / mes**  |

> [!TIP]
> **Decisión FinOps de Ahorro Crítico en Red:** Si la FNC opta por conectar los centros de acopio mediante **AWS IoT Greengrass / TLS sobre Internet seguro** en lugar de mantener túneles IPsec VPN dedicados las 24 horas, **el costo mensual total de la nube desciende a menos de \$12 USD al mes**.

### 5.2 Desglose Exhaustivo de Hardware de Finca (Bill of Materials - BOM)

Los costos corresponden a cotizaciones de mercado en Colombia a una tasa de cambio oficial de **\$3.167 - \$4.100 COP/USD**:

| Ítem | Componente / Especificación Técnica                                                                        | Cantidad | Costo Unitario (COP) | Costo Unitario (USD) | Fuente / Proveedor                  |
| :--- | :--------------------------------------------------------------------------------------------------------- | :------: | :------------------: | :------------------: | :---------------------------------- |
| 1    | **Placa Central IoT:** LilyGO T-SIM7080G-S3 (ESP32-S3 Dual-Core + SIM7080G LTE-M/NB-IoT + GNSS + solar in) |    1     |     $185.000 COP     |      $45,10 USD      | Distribuidor oficial / Vistronica   |
| 2    | **Sensor Suelo Multiparámetro:** Sonda industrial RS485 Modbus RTU IP68 (NPK + Humedad + Temp + pH)        |    1     |     $320.000 COP     |      $78,05 USD      | MercadoLibre / Sigma Sensores       |
| 3    | **Sensor Secado / Ambiente:** Sensor industrial de alta precisión SHT30/SHT35 con filtro sinterizado IP65  |    1     |     $65.000 COP      |      $15,85 USD      | Sigma Electrónica                   |
| 4    | **Batería:** Celda LiFePO4 32700 3,2V 6.000 mAh + BMS 1S 10A con corte térmico (vida útil > 5 años)        |    1     |     $48.000 COP      |      $11,70 USD      | Baterías Colombia / Dinastía        |
| 5    | **Panel Solar:** Panel monocristalino 10W 6V/18V con marco de aluminio anodizado IP65                      |    1     |     $55.000 COP      |      $13,40 USD      | Tiendas Energía Solar Cali/Medellín |
| 6    | **Regulador de Carga MPPT:** Módulo controlador solar CN3791 MPPT optimizado para LiFePO4                  |    1     |     $22.000 COP      |      $5,35 USD       | Sigma Electrónica                   |
| 7    | **Gabinete y Montaje:** Caja estanca IP67 con prensaestopas PG7/PG9, soporte para poste y herrajes         |    1     |     $45.000 COP      |      $10,95 USD      | Fabristore / Ferretería industrial  |
| 8    | **Almacenamiento Local:** Tarjeta MicroSD Industrial 16GB High Endurance (Buffer 24h store-and-forward)    |    1     |     $28.000 COP      |      $6,80 USD       | Kingston / SanDisk Colombia         |
| 9    | **SIM Card M2M Multi-operador:** SIM Claro/Movistar M2M con plan de datos 20MB/mes anualizado              |    1     |     $40.000 COP      |      $9,75 USD       | SimCards IoT Colombia               |
| --   | **TOTAL POR FINCA (BOM Hardware Completo)**                                                                |    --    |   **$808.000 COP**   |   **$196,95 USD**    | --                                  |

#### Presupuesto Total Hardware para el Piloto (200 Fincas):

- **Costo Base 200 Fincas:** 200 $\times$ $808.000 COP = **$161.600.000 COP (~$39.390 USD)**.
- **Stock de Contingencia y Repuestos en Campo (5%):** 10 unidades completas de respaldo = **$8.080.000 COP (~$1.970 USD)**.
- **Inversión Total Hardware Piloto FNC:** **$169.680.000 COP (~$41.360 USD)**.
- **Amortización a 3 Años (36 meses):** **$5,47 USD / mes por finca**, plenamente accesible para los comités departamentales.

### 5.3 Costo de la Campaña de Drones

- Se propone contratar el servicio de vuelo bajo modelo de **DaaS (Drone-as-a-Service)** con operadores locales certificados por la Aeronáutica Civil en lugar de comprar drones de aspersión (que cuestan \$12.000 - \$20.000 USD por unidad más pilotos y seguros).
- **Costo Operador Local:** ~$18 - $25 USD por hectárea inspeccionada/fumigada bajo demanda.
- El costo de la plataforma por almacenar y procesar el vuelo en la nube es de **menos de \$0,01 USD por misión**.

---

## 6. Las Tres Decisiones Clave que Reducen y Evitan Gasto (FinOps Guardrails)

1. **Arquitectura Serverless Pura en Base de Datos y Cómputo:** Se evitó el aprovisionamiento de instancias fijas (RDS PostgreSQL o clústeres EC2/EKS). Esto genera un **ahorro superior a \$1.400 USD anuales** al pagar únicamente por milisegundos de cómputo y solicitudes de escritura efectivas.
2. **Ciclo de Vida Automatizado a S3 Deep Archive:** El uso combinado de TTL en DynamoDB y políticas de transición hacia Glacier Deep Archive reduce el costo de retención de 5 años en un **96%** frente a mantener los datos en volúmenes transaccionales tradicionales.
3. **Hardware Modular de Código Abierto (ESP32-S3) vs. Gateways Propietarios:** Selección de microcontroladores industriales abiertos en lugar de soluciones cerradas tipo Siemens o Advantech, produciendo un **ahorro de CapEx de \$161.000 USD** en el despliegue de las 200 fincas.
