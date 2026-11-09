# Arquitectura de Inferencia Administrada, Soberanía de Datos y Cumplimiento Normativo (Ley 1581 de 2012)

## Plataforma Cafetera AromaPacífico (Federación Nacional de Cafeteros 2026)

---

## 1. Resumen Ejecutivo y Marco Jurídico Institucional

El presente documento establece la especificación arquitectónica, el marco de soberanía de datos y el análisis de costo-eficiencia para el subsistema de **Inferencia Administrada y Protección de Datos Personales** de la plataforma cafetera **AromaPacífico**, diseñado para la **Federación Nacional de Cafeteros (FNC)** como caso de estudio de modernización del piloto de 2020 hacia el año 2026.

La operación digital de la plataforma articula 200 fincas cafeteras distribuidas en los departamentos de **Cauca, Huila y Tolima**, tres centros de acopio departamentales y un servicio centralizado de drones agrícolas que capturan imágenes aéreas para delimitar lotes, confirmar focos fitosanitarios de plagas (roya y broca), verificar aspersiones y estimar el rendimiento volumétrico de la cosecha.

Al procesarse los datos en la nube pública fuera del territorio de la República de Colombia, la Federación asume la condición jurídica de **Responsable del Tratamiento de Datos Personales**. Por consiguiente, la plataforma se somete de forma estricta a los mandatos de la legislación colombiana vigente:
1. **Ley Estatutaria 1581 de 2012**: Régimen General de Protección de Datos Personales (Habeas Data).
2. **Decreto Reglamentario 1377 de 2013**: Condiciones de autorización, aviso de privacidad y políticas de tratamiento.
3. **Circular Única de la Superintendencia de Industria y Comercio (SIC) - Título V**: Disposiciones sobre el Registro Nacional de Bases de Datos (RNBD) y estándares de seguridad para la transmisión y transferencia internacional de datos personales.
4. **Sentencia C-748 de 2011 de la Corte Constitucional**: Principios rectores de legalidad, finalidad, libertad, veracidad, transparencia, acceso y circulación restringida, seguridad y confidencialidad.

La premisa arquitectónica central del pliego establece que **no se entrena un modelo propio de inteligencia artificial**, sino que se consume visión por computador administrada bajo demanda. Asimismo, se impone la regla categórica de negocio según la cual **si una fotografía aérea contiene una persona identificable, el archivo se excluye de inmediato del flujo agronómico**, activando un protocolo de aislamiento y custodia probatoria con retención inmutable durante cinco años.

---

## 2. Servicio de Inferencia Seleccionado y Región Cloud

### 2.1 Arquitectura Híbrida de Visión Serverless: Amazon Rekognition y Amazon Bedrock

Para cumplir de forma simultánea con el marco de protección de datos personales (Ley 1581 de 2012) y las dos invariantes innegociables del pliego (*«No se entrena un modelo. Se usa inferencia administrada»* y *«No debe haber cómputo esperando objetos»*), se adopta una arquitectura de visión serverless en dos etapas desacopladas:

1. **Filtro Perimetral Anti-PII con Amazon Rekognition (`DetectFaces` y `DetectLabels`):**
   - Invoca las APIs administradas de Amazon Rekognition con filtro en categorías humanas (`Person`, `Human`, `Face`, `Worker`, `Farmer`) y umbral de confianza perimetral del 50%.
   - Si la imagen contiene personas identificables, la toma se excluye de inmediato del flujo agronómico, derivándola al bucket de cuarentena en la cuenta de Seguridad (`AromaPacifico-Security`). Esto asegura cumplimiento estricto del régimen de Habeas Data sin incurrir en gasto de inferencia fitosanitaria ($0 invertido en modelos botánicos ante tomas con personas).
2. **Diagnóstico Fitosanitario Administrado con Amazon Bedrock Multimodal Vision:**
   - El análisis foliar de roya (*Hemileia vastatrix*), broca (*Hypothenemus hampei*) y maduración de cosecha se delega a modelos fundacionales multimodales administrados en Amazon Bedrock (ej. Anthropic Claude 3 Haiku o Amazon Nova Lite).
   - **Cero entrenamiento propio:** El modelo fundacional consume directamente la imagen y un prompt agronómico tipificado con salida JSON estructurada (`diagnostico`, `severidad`, `confianza_pct`). No requiere recopilar, etiquetar ni mantener datasets propios de entrenamiento, cumpliendo a cabalidad con la regla de inferencia administrada.
   - **Cero cómputo en espera (Pay-per-Call estricto):** Bedrock factura exclusivamente por tokens de entrada y salida procesados (~$0,0006 a $0,0020 USD por inferencia). En periodos intermedios entre misiones de drones y fuera de temporada de cosecha, el costo de cómputo en reposo es **cero absoluto ($0,00 USD/mes)**.
3. **Garantías Contractuales de Tratamiento de Datos (AWS DPA):**
   - Amazon Web Services certifica bajo su anexo de procesamiento de datos que ni Rekognition ni Bedrock utilizan las imágenes transmitidas por la Federación para entrenar modelos públicos o comerciales de terceros.

### 2.2 Región Cloud Seleccionada: AWS us-east-1 (N. Virginia)

La región principal de despliegue para todos los servicios de cómputo, almacenamiento e inferencia es **US East (N. Virginia), `us-east-1`**, complementada con la región de respaldo **US East (Ohio), `us-east-2`** para el mecanismo de recuperación ante desastres (DR) de la consulta pública del saco de café (RTO de 4 horas y RPO de 15 minutos).

La selección de `us-east-1` frente a regiones geográficamente más cercanas (como São Paulo, `sa-east-1`) se fundamenta exclusivamente en criterios objetivos de ingeniería de redes y disponibilidad tecnológica:
1. **Topología de Cables Submarinos y Baja Latencia**: El tráfico internacional de internet de Colombia transcurre directamente a través de las rutas de fibra óptica submarina del Caribe y el Atlántico (Arcos-1, Maya-1, South America-1 / SAC) que enlazan las estaciones de amarre nacionales (Cartagena, Barranquilla y Cali) con los puntos de presencia e interconexión en Florida y Virginia. La latencia típica hacia `us-east-1` oscila entre 45 y 55 ms, ofreciendo una respuesta altamente reactiva para la telemetría IoT y las cargas de imágenes de drones. En contraste, enrutar hacia São Paulo (`sa-east-1`) implica un trazado por el Cono Sur con múltiples saltos de tránsito internacional, elevando la latencia a 110 - 135 ms (más del doble).
2. **Disponibilidad Integral y Paridad de Servicios Serverless**: `us-east-1` es la región insignia de AWS con paridad completa e inmediata para todos los servicios requeridos por la plataforma: Amazon Bedrock (disponibilidad nativa y cuotas estándar de modelos multimodales Claude 3 Haiku y Nova Lite), Amazon Rekognition (`DetectFaces` y `DetectLabels`), AWS IoT Core con Basic Ingest, AWS Lambda Graviton2 arm64, Amazon DynamoDB On-Demand y Amazon S3 Object Lock en modo Compliance. En regiones alternativas como `sa-east-1`, la oferta de modelos multimodales en Bedrock y las cuotas de concurrencia serverless son significativamente más limitadas.
3. **Respaldo Multi-Región Nativo en Estados Unidos**: La troncal privada de alta velocidad de AWS entre `us-east-1` (Virginia) y `us-east-2` (Ohio) permite replicación asíncrona de datos con latencias inter-región inferiores a 15 ms, garantizando la viabilidad del esquema de alta disponibilidad y recuperación ante desastres exigido por el negocio.

### 2.3 Matriz Comparativa de Motores de Inferencia

| Criterio de Selección | Solución Adoptada: Rekognition (PII) + Bedrock Multimodal | Amazon Rekognition Custom Labels (Rechazada) | Amazon SageMaker Endpoints Dedicados | Clúster EC2 con GPUs (g4dn.xlarge) | Inferencia en Borde / Drones (Edge GPUs) |
|---|---|---|---|---|---|
| **Modelo de Costo** | **Pay-per-Call puro por petición y token** (~$0,0010 PII + ~$0,0020 Bedrock). | Facturación por hora de Unidad de Inferencia ($4,00 USD/hora por IU) + entrenamiento. | Instancia dedicada continua ($0,20 USD / hora). | Servidor dedicado continuo ($0,526 USD / hora). | CapEx elevado: módulo GPU adicional por aeronave. |
| **Costo en Reposo** | **$0,00 USD / mes** (Zero cómputo esperando objetos). | **Inviable**: ~$2.880 USD/mes si permanece activo 24/7 (~$96 USD/día). | ~$144,00 USD / mes por endpoint ml.m5.xlarge. | ~$378,72 USD / mes por instancia g4dn.xlarge. | Inversión inicial de ~$8.000 USD por cuadrilla (~$24.000 USD). |
| **Requisito de Entrenamiento** | **Cero entrenamiento propio**: Modelos fundacionales zero-shot/few-shot. | **Exige entrenamiento propio** con dataset de cientos de fotos etiquetadas. | Exige entrenar, versionar y mantener contenedores MLOps. | Exige compilar modelos TensorRT y mantener AMIs. | Exige compilar y optimizar modelos para edge. |
| **Mantenimiento Operativo** | Cero administración de servidores, parches o cuotas de GPU. | Gestión de arranque/apagado de IUs y versionamiento de proyectos. | Gestión de balanceadores, escalado y artefactos en S3. | Administración de SO Linux, controladores CUDA y parches. | Calibración térmica, vibración y riesgo de daño por caída. |
| **Filtro Anti-PII Integrado** | Nativo perimetral (`DetectFaces` + `DetectLabels`). | No filtra PII; requiere llamada separada a APIs base. | Requiere pipeline dual con red neuronal adicional. | Requiere mantener modelo de segmentación en GPU. | Factible pero drena severamente baterías de vuelo. |
| **Alineación con el Reto** | **100% CUMPLE** ambas reglas (sin entrenamiento y sin espera). | **VIOLA AMBAS REGLAS** (exige entrenamiento y cobra en espera). | Ineficiente para volumen bajo de cosechas (99.8% ocioso). | Descartada por alta complejidad y sobrecostos fijos. | Viola la restricción de costos de hardware e inversión moderada. |

### 2.4 Matriz Comparativa de Regiones Cloud y Soberanía

| Criterio de Selección | AWS us-east-1 (N. Virginia, USA) - Seleccionada | AWS sa-east-1 (São Paulo, Brasil) | Datacenter Local en Colombia / AWS Local Zone |
|---|---|---|---|
| **Estatus Legal SIC (Circular 005/2017)** | País con nivel adecuado reconocido bajo garantías contractuales DPA. | País con nivel adecuado bajo acuerdo Mercosur. | Jurisdicción local directa (Ley 1581 de 2012). |
| **Latencia de Red desde Colombia** | **Óptima: 45 - 55 ms** vía cables submarinos directos del Caribe/Atlántico. | Variable: 110 - 135 ms (enrutamiento por el Cono Sur). | Mínima: 10 - 20 ms. |
| **Disponibilidad de Servicios Serverless** | **100% de servicios disponibles** (Bedrock Multimodal, Rekognition, KMS, IoT Core). | Subconjunto de servicios; oferta restringida de modelos Bedrock y cuotas reducidas. | Sin servicios administrados de visión artificial ni modelos fundacionales. |
| **Respaldo Multi-Región Nativo** | Excelente paridad y enlace de alta velocidad con `us-east-2` (Ohio). | Compleja replicación hacia otras regiones del continente. | Sin redundancia regional nativa dentro del país. |
| **Línea Base Económica de Catálogo** | Región con la estructura de precios base más eficiente a nivel global de AWS. | Precios de catálogo más elevados para cómputo, almacenamiento y APIs. | Elevada inversión en hardware dedicado y licenciamiento local. |

---

## 3. Delimitación de Datos Transfronterizos y Soberanía Nacional

### 3.1 Lista Exhaustiva de Datos: Qué Sale del País vs. Qué Permanece en Colombia

La siguiente tabla técnica delimita con absoluta precisión jurídica y técnica el destino de cada categoría de información procesada por la plataforma:

| Categoría de Información | Objeto o Atributo Concreto | Destino Físico y Territorial | Mecanismo de Seguridad y Justificación Técnica |
|---|---|---|---|
| **Dato Personal Sensible (Titular)** | Cédula de ciudadanía en texto plano del caficultor | **Permanece en Colombia** (Bases de datos locales FNC) | **NUNCA sale del país**. En la nube solo se almacena un identificador seudonimizado (`FincaID`) o un hash criptográfico HMAC-SHA-256. |
| **Dato Privado de Movilidad** | Rutas y caminos intraprediales privados de la finca | **Permanece en Colombia** (Tableta de cuadrilla en acopio) | No se transmiten rutas internas a la nube. Hacia AWS solo viajan las coordenadas GPS del foco o de la vía principal. |
| **Datos Biométricos Accidentales** | Fotografías crudas con rostros o figuras humanas | **Aisladas en Cuarentena de Seguridad** | Se bloquean antes de inferencia fitosanitaria. Quedan en bóveda restringida con acceso exclusivo para el Oficial de Datos. |
| **Evidencia Agronómica de Cultivo** | Fotografías aéreas de dosel vegetal y hojas de café | **Se transmite a AWS us-east-1** (EE.UU.) | Se transmite vía HTTPS (TLS 1.3) a Amazon S3 con cifrado SSE-KMS para inferencia foliar. Exclusivamente fotos sin personas. |
| **Metadatos de Vuelo Aeronáutico** | Coordenadas GPS del foco, altitud, DronID, UTC | **Se transmite a AWS us-east-1** (EE.UU.) | Permiten situar el diagnóstico en el expediente digital y verificar que el vuelo ocurrió dentro del polígono registrado. |
| **Telemetría Ambiental e IoT** | Valores NPK, humedad de suelo, temperatura de aire | **Se transmite a AWS us-east-1** (EE.UU.) | Publicación MQTT sobre TLS a AWS IoT Core; datos agronómicos no identificables con personas naturales. |
| **Cadena de Custodia del Grano** | Código alfanumérico del saco de 60 kg, peso y estado | **Se transmite a AWS us-east-1** (EE.UU.) | Trazabilidad pública de exportación. No serializa datos privados del caficultor ni del transportador terrestre. |

### 3.2 Fundamentación Legal de la Transmisión Internacional (Ley 1581 de 2012)

El Artículo 26 de la Ley 1581 de 2012 prohíbe la transferencia de datos personales a países que no proporcionen niveles adecuados de protección, salvo cuando se configure alguna de las excepciones expresamente consagradas en la ley. La arquitectura de AromaPacífico fundamenta la legalidad del flujo transfronterizo en tres pilares jurídicos y contractuales:

1. **Contrato de Transmisión de Datos (Data Processing Addendum - DPA)**:
   Entre la Federación Nacional de Cafeteros (como Responsable del Tratamiento) y Amazon Web Services, Inc. (como Encargado del Tratamiento en EE.UU.) se suscribe el anexo de tratamiento de datos de AWS, el cual incorpora **Cláusulas Contractuales Tipo** que vinculan jurídicamente al proveedor a no utilizar, divulgar, indexar ni alterar los datos para fines distintos a la ejecución de las funciones delegadas.
2. **Autorización Expresa del Titular (Consentimiento Informado)**:
   En cumplimiento del Decreto 1377 de 2013, la aplicación móvil del caficultor y la del transportador incluyen un módulo de consentimiento previo, expreso e informado. En dicho formulario digital se advierte explícitamente al usuario que la infraestructura de computación en la nube reside en Estados Unidos y se especifican las finalidades exclusivas de asistencia agronómica y trazabilidad comercial.
3. **Reconocimiento de Estándar Adecuado por la SIC**:
   La Superintendencia de Industria y Comercio, mediante la Circular Externa 005 de 2017 y la Circular Externa 008 de 2020, reconoció que las transferencias internacionales hacia los Estados Unidos de América son viables siempre que medien acuerdos contractuales que garanticen estándares equivalentes de protección, condición que cumple plenamente la certificación corporativa de AWS bajo ISO/IEC 27018 (Código de Práctica para la Protección de Datos Personales en Servicios de Nube) y sus reportes independientes SOC 2 Tipo II.

### 3.3 Salvaguardas Técnicas Criptográficas de la Transmisión

Para garantizar que ningún dato pueda ser interceptado, alterado o desviado en tránsito internacional, se despliegan las siguientes medidas técnicas permanentes:
- **Cifrado de Tránsito de Grado Militar**: Toda comunicación entre las tabletas de campo, los centros de acopio y la nube utiliza canales HTTPS forzados con **TLS 1.3** y suites de cifrado autenticado AES-GCM-256 o ChaCha20-Poly1305. Se rechaza cualquier negociación en protocolos obsoletos (TLS 1.0, 1.1 o SSL).
- **URLs Prefirmadas con Expiración Corta**: La subida de imágenes a Amazon S3 no se realiza mediante credenciales fijas de IAM expuestas en los dispositivos, sino a través de URLs prefirmadas emitidas por la API de la plataforma con un tiempo máximo de vida de 15 minutos (`ExpiresIn: 900`).
- **Túneles VPN IPsec Redundantes para Centros de Acopio**: La interconexión física entre los centros de acopio departamentales (Cauca, Huila y Tolima) y la VPC de nube transcurre a través de túneles redundantes IPsec BGP hacia AWS Transit Gateway, aislando el tráfico operativo de la internet pública.

---

## 4. Tratamiento Integral de Imágenes con Personas (Ciclo Anti-PII de Punta a Punta)

El núcleo del requerimiento de protección de datos personales exige especificar el ciclo de vida completo que sufre una imagen cuando el dron captura inadvertidamente una persona en campo.

### 4.1 Principio de Exclusión Agronómica Preventiva

> [!IMPORTANT]
> **REGLA MANDATORIA DE GOBIERNO DE DATOS: CERO INFERENCIA FITOSANITARIA SOBRE PERSONAS**
> Queda terminantemente prohibido que una imagen que contenga personas identificables sea sometida a algoritmos de detección fitosanitaria de plagas o de estimación de cosecha. La presencia humana aborta el procesamiento agronómico y conmuta automáticamente el archivo hacia el subsistema de aislamiento ético y custodia probatoria.

### 4.2 Fases del Ciclo de Vida Anti-PII y Árbol de Decisión

El flujo de decisión y el tratamiento perimetral se formalizan en el siguiente diagrama arquitectónico desarrollado con el Agente de Diagramas (`diagram-agent`):

![Diagrama de Flujo del Filtro de Privacidad y Árbol de Decisión Anti-PII](diagrams/carga-e-inferencia-filtro-pii.svg)

> Archivo fuente Draw.io editable: [`diagrams/carga-e-inferencia-filtro-pii.drawio`](diagrams/carga-e-inferencia-filtro-pii.drawio).

El árbol de decisión anterior estructura la operación técnica a través de las fases consecutivas del pipeline:

#### Fase 1: Detección Automática Perimetral (Filtro Anti-PII Serverless)
1. Al depositarse una nueva fotografía en `s3://aromapacifico-objetos-prod/raw-images/focos/`, el evento `s3:ObjectCreated:Put` dispara la función Lambda perimetral `PrivacyFilterFunction` (ejecutada en runtime Graviton2 arm64).
2. La función lee el archivo en memoria RAM efímera (sin almacenamiento persistente en disco local) e invoca en paralelo dos endpoints de Amazon Rekognition:
   - `DetectFaces`: Detecta rostros humanos individuales, posición cefálica y cajas delimitadoras (*bounding boxes*).
   - `DetectLabels`: Detecta etiquetas contextuales con un umbral de confianza mínimo del 50.0% (`MinConfidence: 50.0`), evaluando específicamente las categorías humanas: `Person`, `Human`, `Face`, `Worker`, `Farmer`.
3. Si el nivel de confianza arrojado por cualquiera de las dos llamadas supera el 50%, la función concluye de forma determinista que la imagen contiene información personal biométrica o fisonómica protegida por la Ley 1581 de 2012.

#### Fase 2: Bloqueo Operativo e Interrupción del Pipeline
1. La función interrumpe inmediatamente el flujo de trabajo agronómico: se inhibe cualquier llamada hacia los modelos multimodales de visión en Amazon Bedrock para el diagnóstico foliar de roya o broca.
2. Esta decisión ahorra el cómputo y el costo de inferencia fitosanitaria ($0 invertidos en plagas) e impide que datos personales ingresen a modelos de clasificación botánica.
3. En la tabla DynamoDB `ExpedienteFitosanitario`, el caso se actualiza atómicamente con el estado `PII_DETECTED_BLOQUEADO`. La orden fitosanitaria no muta a autorizada ni se aprueba fumigación alguna.

#### Fase 3: Almacenamiento Seguro y Aislamiento en Cuarentena
1. La imagen original cruda es copiada al bucket de cuarentena dedicado:
   `s3://aromapacifico-quarantine-pii/` radicado en la cuenta **AromaPacifico-Security**.
2. Una vez confirmada la copia íntegra en la cuenta de Seguridad mediante verificación de hash SHA-256, el objeto es eliminado de inmediato del bucket de producción (`raw-images/`).
3. El bucket de cuarentena cuenta con una política de cifrado forzado del lado del servidor con llaves administradas por el cliente (**SSE-KMS CMK**). La política de la llave KMS estipula un aislamiento Zero Trust absoluto:
   - Únicamente la identidad del **Oficial de Protección de Datos de la FNC** (`DataPrivacyOfficerRole`) posee permisos de desencriptado (`kms:Decrypt`).
   - Los roles de administradores de infraestructura, agrónomos, operadores de drones, transportadores y caficultores tienen denegado de forma explícita el acceso de lectura y descarga sobre este almacén.

#### Fase 4: Retención Normativa WORM a 5 Años (S3 Object Lock)
1. De acuerdo con el requerimiento del caso y las facultades sancionatorias de la Superintendencia de Industria y Comercio (cuyas investigaciones administrativas por infracción a la Ley 1581 prescriben a los cinco años), las imágenes en cuarentena deben conservarse como evidencia probatoria inmutable.
2. La plataforma activa **Amazon S3 Object Lock** en modo **Compliance**:
   - `RetentionPeriod`: 1.825 días (5 años calendarios exactos).
   - En modo Compliance, **ninguna identidad de AWS (ni siquiera la cuenta Root de la organización)** puede borrar, sobrescribir ni acortar el plazo de retención del objeto antes de que expire la ventana legal.
   - Esto blinda jurídicamente a la Federación frente a acusaciones de alteración o destrucción no autorizada de evidencia en incidentes de privacidad.

#### Fase 5: Procedimiento de Anonimización Opcional para Rescate Agronómico
Si el agrónomo titular de la Federación certifica que el lote sobrevolado presenta un foco de alta severidad epidemiológica y requiere imperativamente el diagnóstico fitosanitario de esa toma, la plataforma habilita un flujo de remediación ética:
1. Una función especializada de procesamiento de imagen lee la imagen desde la cuarentena (bajo autorización delegada del Oficial de Datos).
2. Utilizando las coordenadas de la caja delimitadora (*bounding box*) provistas por Rekognition, se aplica una técnica de **ofuscación irreversible mediante desenfoque gaussiano de radio 25 px (box blur) o máscara opaca total (black-box pixelation)** sobre el área donde se ubica la persona.
3. La imagen resultante anonimizada se guarda como `foto_anonimizada_foco.jpg` y se reinyecta al pipeline de diagnóstico foliar. La foto original permanece intacta en el bucket de cuarentena durante sus cinco años de retención.

### 4.3 Matriz Comparativa de Mecanismos de Filtrado Anti-PII

| Mecanismo de Filtrado | Filtro Serverless con Rekognition (Seleccionado) | Inspección Visual Humana Previa | Anonimización Ciega en Borde (Dron) | Bloqueo y Eliminación Instantánea |
|---|---|---|---|---|
| **Efectividad y Detección** | Alta (> 98% en rostros y perfiles con Rekognition). | Variable: fatiga visual y subjetividad humana. | Limitada por la capacidad computacional en vuelo. | Absoluta en bloqueo; nula en rescate agronómico. |
| **Tiempo de Procesamiento** | Instantáneo: < 200 ms por fotografía en nube. | Lento: horas o días hábiles según disponibilidad. | Real-time pero ralentiza la cadencia de disparo. | Inmediato pero destructivo para el expediente. |
| **Costo Operativo** | Mínimo: **$0.0010 USD por imagen analizada**. | Muy costoso: salarios de personal de revisión. | Alto en hardware embebido (GPUs en drones). | $0 en inferencia; alto en pérdida de cosechas. |
| **Rigor Legal (Ley 1581)** | Pleno: registro inmutable en CloudTrail y S3 WORM. | Riesgo de divulgación no autorizada por revisores. | Cumple privacidad pero no genera evidencia forense. | Dificulta la defensa probatoria ante la SIC. |

---

## 5. Cadencia Operativa de Drones e Invocaciones en Cosecha

Para calcular con rigor matemático el volumen de invocaciones y los costos asociados, se toman como base inmutable las cifras de cadencia aeronáutica modeladas en la arquitectura del servicio de drones (`docs/architecture/carga-b-servicio-drones.md`):
- **Alcance Operativo**: 200 fincas cafeteras repartidas en Cauca, Huila y Tolima.
- **Cuadrillas Especializadas**: 3 cuadrillas departamentales operando desde los centros de acopio.
- **Estructura Fenológica Anual**: Dos semestres claramente diferenciados:
  - **Semestre de Cosecha (Cosecha Principal y Mitaca)**: 6 meses de alta actividad (ejemplo: Abril a Junio, y Septiembre a Noviembre).
  - **Semestre Fuera de Cosecha (Mantenimiento y Desarrollo)**: 6 meses de actividad basal.

### 5.1 Desglose de Fotografías Sujetas a Inferencia por Servicio

De los cinco servicios obligatorios de drones, únicamente los servicios fotográficos (S2, S4 y S5) capturan imágenes que ingresan al motor de inferencia de visión:
1. **Servicio 2: Confirmar Alerta de Sensor**:
   - En cosecha, los sensores de suelo y clima reportan alertas fitosanitarias en el 20% de las fincas de manera mensual ($200 \times 0{,}20 = 40\text{ fincas/mes}$).
   - Cada misión táctica captura 1 fotografía de detalle del foco alertado.
   - Total mensual en cosecha: **40 fotografías / mes**.
   - Total semestre de cosecha: $40 \times 6 = \mathbf{240\text{ fotografías}}$.
2. **Servicio 4: Verificar Post-Fumigación**:
   - De los focos evaluados en S2, la combinación de inferencia y criterio agronómico confirma la plaga y emite orden de fumigación en el 75% de los casos ($40 \times 0{,}75 = 30\text{ fincas fumigadas/mes}$).
   - Toda fumigación exige obligatoriamente un vuelo de verificación fotográfica de cierre a los 7-10 días (relación 1:1).
   - Total mensual en cosecha: **30 fotografías / mes**.
   - Total semestre de cosecha: $30 \times 6 = \mathbf{180\text{ fotografías}}$.
3. **Servicio 5: Estimar Rendimiento de Cosecha**:
   - Se ejecuta una vez por ciclo de cosecha sobre las 200 fincas del programa piloto, concentrándose en las 4 a 6 semanas previas a la recolección.
   - En el semestre de cosecha se evalúan las 200 fincas (distribuidas en ~67 fincas por mes durante los 3 meses de la ventana de maduración).
   - Total semestre de cosecha: **200 fotografías / ciclo**.

### 5.2 Matriz Consolidada de Carga de Inferencia en Cosecha

| Servicio de Dron | Fotos en Mes Pico Cosecha | Fotos en Todo el Semestre de Cosecha (6 Meses) | Promedio por Centro de Acopio / Mes Pico |
|---|---|---|---|
| **S2. Confirmar Foco** | 40 | 240 | ~13 fotos / mes |
| **S4. Verificar Cierre** | 30 | 180 | 10 fotos / mes |
| **S5. Estimar Cosecha** | ~67 | 200 | ~22 fotos / mes |
| **Total Imágenes a Inferencia** | **~137 a 150 fotos / mes** | **620 fotos / semestre** | **~45 a 50 fotos / mes / acopio** |

---

## 6. Modelo de Costos FinOps y Costo por Mil Invocaciones en Cosecha

El modelo financiero se estructura a partir de la lista oficial de precios públicos de Amazon Web Services para la región `us-east-1` (vigentes y consultados para 2026).

### 6.1 Tarifas Unitarias Oficiales de Componentes y Páginas de Precios (AWS us-east-1)

1. **Amazon Rekognition (Filtro Perimetral Anti-PII)**:
   - **Página oficial de precios:** [Amazon Rekognition Pricing](https://aws.amazon.com/rekognition/pricing/) (Consultada: Febrero de 2026).
   - Operaciones `DetectFaces` y `DetectLabels`: **$0,0010 USD** por imagen analizada (Nivel 1 de consumo: de 0 a 1 millón de imágenes al mes, equivalente a $1,00 USD por cada 1.000 imágenes).
   - Se utiliza de manera exclusiva para detectar presencia humana perimetral antes de cualquier análisis fitosanitario. Si detecta personas, la imagen se desvía a cuarentena S3 y se aborta el flujo, evitando costos de inferencia posteriores.

2. **Amazon Bedrock Multimodal Vision (Inferencia Fitosanitaria Administrada)**:
   - **Página oficial de precios:** [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) (Consultada: Febrero de 2026).
   - Modelo fundacional multimodal de visión seleccionado: **Anthropic Claude 3 Haiku** (o alternativamente **Amazon Nova Lite** en la misma consola de Bedrock).
   - **Modelo de Cobro:** Tarificación puramente elástica por token de entrada y salida (Pay-per-Call estricto). No requiere instancias aprovisionadas ni unidades de inferencia dedicadas.
   - **Desglose de Tokens por Inferencia Foliar (Claude 3 Haiku):**
     - Tarifa de Tokens de Entrada: **$0,00025 USD** por 1.000 tokens ($0,25 USD por millón).
     - Tarifa de Tokens de Salida: **$0,00125 USD** por 1.000 tokens ($1,25 USD por millón).
     - Procesamiento visual de fotografía foliar (resolución estandarizada 1024x1024 px): ~1.600 tokens de imagen.
     - Prompt taxonómico agronómico del sistema (instrucciones para roya, broca y severidad): ~200 tokens de entrada.
     - Total tokens de entrada: $1.800\text{ tokens} \times (\$0,00025 / 1.000) = \mathbf{\$0,000450\text{ USD}}$.
     - Respuesta estructurada en JSON (`diagnostico`, `confianza_pct`, `severidad`, `observaciones`): ~150 tokens de salida.
     - Total tokens de salida: $150\text{ tokens} \times (\$0,00125 / 1.000) = \mathbf{\$0,000188\text{ USD}}$.
     - **Costo Real por Inferencia con Claude 3 Haiku:** $\$0,000450 + \$0,000188 = \mathbf{\$0,000638\text{ USD}}$ por imagen analizada (~$0,64 USD por cada 1.000 imágenes).
     - **Presupuesto Conservador de Contingencia FinOps:** Para absorber posibles variaciones en longitud de salida, prompts detallados o imágenes de mayor resolución, el modelo adopta un valor conservador de **$0,0020 USD por inferencia** ($2,00 USD por cada 1.000 imágenes).
     - *(Escenario de ultra-bajo costo con Amazon Nova Lite: $0,06 USD/M tokens entrada y $0,24 USD/M tokens salida, arrojando un costo unitario de apenas **$0,00030 USD por imagen**, o $0,30 USD por cada 1.000 imágenes).*
   - **Costo en Reposo:** **$0,00 USD / mes** (Zero cómputo esperando objetos; si no hay vuelos de drones en la semana, la facturación es $0,00 USD).
   - **Costo de Entrenamiento:** **$0,00 USD** (Cero recolección de datasets etiquetados y cero horas de GPU de entrenamiento).

3. **Invalidación Formal de Amazon Rekognition Custom Labels:**
   - **Página oficial de precios:** [Amazon Rekognition Custom Labels Pricing](https://aws.amazon.com/rekognition/pricing/) (Consultada: Febrero de 2026).
   - **Costo de Inferencia:** Facturación fija de **$4,00 USD por hora** por cada Unidad de Inferencia (Inference Unit - IU) aprovisionada mientras el modelo se encuentre en estado activo (`RUNNING`), independientemente del número de imágenes evaluadas.
   - **Impacto Financiero:** Si un modelo de Custom Labels permaneciera activo 24/7 durante un mes, generaría una factura fija de $4,00 \times 720\text{ h} = \mathbf{\$2.880,00\text{ USD / mes}}$ por modelo. Incluso encendiéndolo y apagándolo únicamente en las 4 horas operativas diarias de días hábiles, costaría $4,00 \times 4\text{ h} \times 20\text{ días} = \mathbf{\$320,00\text{ USD / mes}}$.
   - **Costo de Entrenamiento:** Tarifa obligatoria de **$1,00 USD por hora** de entrenamiento del modelo, requiriendo cientos de fotos etiquetadas manualmente.
   - **Conclusión:** No existe la modalidad "Custom Labels Serverless Pay-per-Call a $0,001 por imagen". Custom Labels queda completamente invalidado y descartado por chocar con las dos directrices del enunciado.

4. **AWS Lambda (Arquitectura AWS Graviton2 arm64)**:
   - **Página oficial de precios:** [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/) (Consultada: Febrero de 2026).
   - Configuración de memoria: 512 MB (0.5 GB).
   - Duración media de ejecución por imagen: 400 milisegundos (0.4 s).
   - Consumo de cómputo por invocación: $0,4\text{ s} \times 0,5\text{ GB} = 0,2\text{ GB-s}$.
   - Tarifa Graviton2 (us-east-1): **$0,0000133334 USD** por GB-segundo.
   - Costo de cómputo por 1.000 invocaciones: $200\text{ GB-s} \times \$0,0000133334 = \$0,00267\text{ USD}$.
   - Peticiones Lambda: **$0,0000002 USD** por invocación ($0,20 USD por millón de peticiones).
   - Subtotal Lambda por 1.000 invocaciones: **$0,00287 USD**.

5. **Amazon S3 Standard (Almacenamiento Temporal y Cuarentena)**:
   - **Página oficial de precios:** [Amazon S3 Pricing](https://aws.amazon.com/s3/pricing/) (Consultada: Febrero de 2026).
   - Tamaño medio por fotografía en alta definición: 3.5 MB.
   - 1.000 imágenes equivalen a: $1.000 \times 3,5\text{ MB} = 3.500\text{ MB} = 3,5\text{ GB}$.
   - Tarifa S3 Standard (us-east-1): **$0,023 USD** por GB-mes.
   - Costo de almacenar 3.5 GB durante un mes: $3,5\text{ GB} \times \$0,023 = \mathbf{\$0,0805\text{ USD}}$.

6. **AWS Key Management Service (KMS)**:
   - **Página oficial de precios:** [AWS KMS Pricing](https://aws.amazon.com/kms/pricing/) (Consultada: Febrero de 2026).
   - Solicitudes de cifrado y descifrado SSE-KMS: **$0,0300 USD** por cada 10.000 peticiones ($0,000003 USD por petición).
   - Costo por 1.000 peticiones de encriptación: **$0,0300 USD**.

7. **Enrutamiento de Red (Gateway VPC Endpoints)**:
   - El tráfico interno entre subredes privadas de VPC, Amazon S3 y Amazon DynamoDB transcurre a través de Gateway VPC Endpoints gratuitos: **$0,0000 USD** por GB procesado.

### 6.2 Desglose Matemático del Costo por 1.000 Invocaciones Completas

Un ciclo completo de inferencia comprende: lectura en S3, filtro perimetral anti-PII con Rekognition, inferencia fitosanitaria multimodal con Bedrock, cómputo serverless en Lambda y cifrado KMS:

| Componente del Subsistema | Concepto Técnico y Operación | Costo Nominal Claude 3 Haiku (USD) | Costo Conservador FinOps (USD) |
|---|---|---|---|
| **Rekognition Filtro Anti-PII** | Detección perimetral de personas (`DetectFaces` / `DetectLabels`) | $1,0000 USD | $1,0000 USD |
| **Bedrock Inferencia Multimodal** | Diagnóstico foliar administrado de roya, broca o maduración | $0,6375 USD | $2,0000 USD |
| **AWS Lambda (Graviton2 512 MB)** | Cómputo serverless de ingesta, orquestación y persistencia | $0,0029 USD | $0,0029 USD |
| **Amazon S3 Standard (3.5 GB)** | Retención mensual de 1.000 fotografías de 3.5 MB en la nube | $0,0805 USD | $0,0805 USD |
| **AWS KMS (Cifrado Criptográfico)** | Operaciones de encriptado en reposo SSE-KMS | $0,0300 USD | $0,0300 USD |
| **Gateway VPC Endpoints** | Tráfico de red privado entre VPC, S3 y DynamoDB | $0,0000 USD | $0,0000 USD |
| **TOTAL POR 1.000 INVOCACIONES** | **Pipeline completo de extremo a extremo** | **$1,7509 USD** | **$3,1134 USD** |

### 6.3 Factura Real del Semestre de Cosecha para AromaPacífico (620 Fotos)

Al aplicar la cadencia real calculada para las 200 fincas en los 6 meses de cosecha (240 fotos de foco en S2 + 180 fotos de verificación en S4 + 200 fotos de estimación en S5 = 620 fotos):

1. **Bajo el Escenario Conservador de Presupuesto ($3,1134 USD / 1.000 fotos):**

$$\text{Costo Total Cosecha} = 620\text{ imágenes} \times \left(\frac{\$3{,}1134\text{ USD}}{1.000\text{ imágenes}}\right) = \mathbf{\$1{,}9303\text{ USD en todo el semestre}}$$

$$\text{Costo Promedio Mensual en Cosecha} = \frac{\$1{,}9303\text{ USD}}{6\text{ meses}} = \mathbf{\$0{,}3217\text{ USD / mes}}$$

En el mes de mayor demanda aeronáutica (mes pico con ~150 fotografías evaluadas):

$$\text{Costo Mes Pico} = 150\text{ imágenes} \times \$0{,}0031134\text{ USD} = \mathbf{\$0{,}4670\text{ USD / mes}}$$

2. **Bajo el Escenario Nominal con Claude 3 Haiku ($1,7509 USD / 1.000 fotos):**

$$\text{Costo Total Cosecha} = 620\text{ imágenes} \times \left(\frac{\$1{,}7509\text{ USD}}{1.000\text{ imágenes}}\right) = \mathbf{\$1{,}0856\text{ USD en todo el semestre}}$$

$$\text{Costo Promedio Mensual} = \mathbf{\$0{,}1809\text{ USD / mes}}$$

3. **Costo en Periodos Fuera de Cosecha (Semestre de Mantenimiento):**
En los meses donde no se despliegan vuelos de inspección, el costo de inferencia es de **$0,00 USD**. No existen servidores esperando peticiones ni cargos mínimos de infraestructura.

### 6.4 Análisis FinOps y Comparativa de Ahorro del Negocio

La adopción de una arquitectura de visión administrada serverless responde a una decisión deliberada de maximización del valor del negocio y minimización radical del desperdicio:

```text
[Inferencia Serverless Pay-per-Call]  -->  $1.93 USD / semestre  (Zero cómputo en reposo)
[SageMaker Endpoint Dedicado 24/7]    -->  $864.00 USD / semestre (99.78% sobrecosto inútil)
[Custom Labels (si operara 24/7)]     -->  $17.280.00 USD / semestre (99.99% sobrecosto inútil)
[Clúster EC2 con GPUs Dedicadas]      -->  $2.272.32 USD / semestre (99.91% sobrecosto inútil)
```

1. **Ahorro Superior al 99.7% frente a SageMaker Dedicado**:
   Mantener un endpoint continuo en Amazon SageMaker con una instancia mínima `ml.m5.xlarge` encendida las 24 horas del día cuesta **$144,00 USD mensuales** ($864,00 USD durante los seis meses de cosecha). Con un volumen de apenas 620 fotos en el semestre, el costo unitario por imagen se elevaría absurdamente a **$1,39 USD por foto procesada**, incurriendo en un 99.78% de ineficiencia por servidores desocupados. La solución serverless reduce el gasto a solo **$1,93 USD en todo el semestre**.
2. **Eliminación Total del Riesgo Financiero de Custom Labels**:
   Custom Labels obligaría a pagar al menos $4,00 USD por cada hora de vuelo de las cuadrillas, más $1,00 USD/hora por entrenar modelos con fotos de fincas. Con Bedrock, la Federación accede de forma inmediata a modelos de última generación sin pagar un solo centavo por preparación ni horas ociosas de cómputo.
3. **Eliminación Total de CapEx en Cuadrillas**:
   Embarcar GPUs en los drones de las tres cuadrillas departamentales requeriría computadores de abordo especializados (tipo Nvidia Jetson Orin Industrial) con un sobrecosto de al menos **$8.000 USD por aeronave** ($24.000 USD de CapEx adicional para la Federación). Además, el elevado consumo térmico y eléctrico de estos chips en vuelo reduce la autonomía de las baterías LiPo en más del 40%, obligando a comprar bancos de baterías adicionales y degradando la vida útil del equipo.
4. **Escalabilidad Elástica sin Refactorización**:
   Si el piloto de la Federación se expande en años posteriores de 200 a 1.000 o 5.000 fincas, la arquitectura serverless escala de forma transparente e instantánea sin necesidad de rediseñar contratos, redimensionar clústeres ni gestionar ventanas de mantenimiento en cosecha.

---

## 7. Diagramas de Arquitectura y Referencias de Implementación

La solución técnica se formaliza a través de tres diagramas especializados desarrollados conforme a las directrices del Agente de Diagramas (`diagram-agent`):

### 7.1 Diagrama de Soberanía de Datos y Flujo Transfronterizo
Ilustra la delimitación entre los datos que permanecen en Colombia (cédula del caficultor en bases de datos locales, rutas privadas y fotos con PII) y los objetos técnicos que viajan a la región `us-east-1` bajo el amparo de la Ley 1581 de 2012 y el contrato DPA de AWS.

![Soberanía de Datos y Flujo Transfronterizo](diagrams/carga-e-inferencia-soberania-datos.svg)

> Archivo fuente Draw.io editable: [`diagrams/carga-e-inferencia-soberania-datos.drawio`](diagrams/carga-e-inferencia-soberania-datos.drawio).

### 7.2 Diagrama del Pipeline Perimetral Anti-PII y Aislamiento en Cuarentena
Detalla la detección de figuras humanas y rostros con Amazon Rekognition, la bifurcación condicional, el etiquetado de seguridad, el traslado hacia la cuenta `AromaPacifico-Security`, la retención inmutable WORM a 5 años bajo S3 Object Lock y el proceso opcional de difuminado irreversible.

![Pipeline Perimetral Anti-PII y Cuarentena](diagrams/carga-e-inferencia-filtro-pii.svg)

> Archivo fuente Draw.io editable: [`diagrams/carga-e-inferencia-filtro-pii.drawio`](diagrams/carga-e-inferencia-filtro-pii.drawio).

### 7.3 Diagrama del Modelo FinOps de Inferencia y Costos en Cosecha
Muestra la correlación entre la cadencia matemática de vuelos de drones en las 200 fincas (620 imágenes semestrales), el desglose de tarifas por cada 1.000 invocaciones ($3,11 USD conservador / $1,75 USD nominal) y la comparativa de ahorro de más del 99.7% frente a infraestructura fija.

![Modelo FinOps de Inferencia y Costos en Cosecha](diagrams/carga-e-inferencia-finops-costos.svg)

> Archivo fuente Draw.io editable: [`diagrams/carga-e-inferencia-finops-costos.drawio`](diagrams/carga-e-inferencia-finops-costos.drawio).

---

## 8. Parámetros Técnicos, Nomenclatura y Tags de Seguridad

Para garantizar un gobierno estricto de los recursos en Terraform y en la consola de AWS, se establece la siguiente matriz de parámetros, identificadores y etiquetas de cumplimiento:

| Parámetro o Recurso | Identificador Técnico Estándar | Propósito y Configuración Mandatoria |
|---|---|---|
| **Función Filtro PII** | `aromapacifico-prod-privacy-filter-fn` | Lambda Graviton2 arm64, 512 MB, Timeout 30s. Invoca `DetectFaces` y `DetectLabels`. |
| **Bucket de Cuarentena** | `aromapacifico-quarantine-pii-prod` | Bucket S3 en cuenta Security. Cifrado SSE-KMS CMK. S3 Object Lock Compliance 5 años. |
| **Llave KMS de Cuarentena** | `alias/aromapacifico-quarantine-cmk` | Llave CMK cuya política deniega el descifrado a todos excepto a `DataPrivacyOfficerRole`. |
| **Tabla Expediente** | `aromapacifico-prod-expediente-fitosanitario` | DynamoDB On-Demand. Almacena estado `PII_DETECTED_BLOQUEADO` o `FOCO_CONFIRMADO`. |
| **Tópico SNS Seguridad** | `arn:aws:sns:us-east-1:...:alerta-violacion-pii` | Notificación crítica enviada al correo del Oficial de Datos al detectar personas en fotos. |
| **Tag de Clasificación** | `fnc:security:data-classification = RESTRICTED_PII` | Etiqueta obligatoria asignada a cualquier objeto o expediente con presencia humana. |
| **Tag de Retención Legal** | `fnc:regulatory:retention-policy = LEY1581_5Y_WORM` | Rige la regla de ciclo de vida e inmutabilidad estricta exigida por la SIC. |
| **Tag de Centro Acopio** | `fnc:operations:acopio-id = ACOPIO-CAUCA-01` | Identificador para costeo y segmentación granular de operaciones en AWS Cost Explorer. |

---

## 9. Sincronización de Gobernanza y Registro de Supuestos

Las decisiones de ingeniería y cumplimiento legal adoptadas en este documento se sincronizan en la bitácora central [`assumptions-log.md`](../cross-cutting/assumptions-log.md) bajo las siguientes entradas de gobierno:
- **Supuesto 008**: Adopción de arquitectura dual serverless en `us-east-1` (Amazon Rekognition para filtro perimetral anti-PII y Amazon Bedrock Multimodal Vision para diagnóstico fitosanitario) bajo contrato DPA y autorización de transferencia internacional (Ley 1581 de 2012).
- **Supuesto 009**: Exclusión absoluta y bloqueo preventivo de inferencia agronómica ante presencia humana en imágenes, con retención inmutable WORM de 5 años bajo S3 Object Lock Compliance en la cuenta Security.
- **Supuesto 010**: Modelo de costos serverless Pay-per-Call ($3,11 USD conservador / $1,75 USD nominal por 1.000 fotos completas), garantizando $0,00 USD en reposo y un gasto de inferencia inferior a $2,00 USD para todo el semestre de cosecha.

