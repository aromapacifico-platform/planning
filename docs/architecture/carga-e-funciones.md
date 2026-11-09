# Arquitectura de Funciones por Eventos, Inferencia Serverless y Resiliencia

## Plataforma Cafetera AromaPacífico (Federación Nacional de Cafeteros 2026)

---

## 1. Resumen Ejecutivo y Propósito Arquitectónico

El presente documento define la arquitectura técnica del subsistema de **funciones orientadas por eventos** (*Event-Driven Serverless Compute*) e **inferencia administrada** para la plataforma cafetera **AromaPacífico**, diseñada para la Federación Nacional de Cafeteros (FNC) para la vigencia 2026.

En el marco del estudio del caso y la modernización del piloto en los departamentos de **Cauca, Huila y Tolima** (200 fincas, 3 centros de acopio, 60 transportadores y entrega en Buenaventura), la arquitectura erradica por completo el aprovisionamiento de cómputo inactivo en espera de archivos. La inferencia y el procesamiento agronómico operan bajo un paradigma estrictamente serverless: **la función se invoca únicamente ante la ocurrencia de un evento verificado, procesa de forma transaccional y finaliza de inmediato persistiendo su resultado en el expediente digital**.

### Principios e Invariantes Críticas del Subsistema

1. **Invariante de Cero Mutación Destructiva en Fallas:**
   Si una invocación falla (por interrupción de red, agotamiento de cuota, timeout o excepción del servicio de visión), **el objeto de origen en Amazon S3 permanece 100% intacto y el estado del caso en el expediente no sufre ninguna alteración**. Se prohíbe terminantemente que una falla técnica induzca al sistema a asumir un diagnóstico falso (por ejemplo, declarar erróneamente un foco como descartado o cerrar una orden sin verificar).
2. **Invariante Zero Trust en Fumigación:**
   Ningún disparador, función serverless ni modelo de inteligencia artificial posee la atribución ni los privilegios para autorizar una fumigación ni emitir una orden de aspersión agroquímica. La inferencia asiste y complementa el diagnóstico técnico; **la autorización de fumigación es un acto legal y agronómico atribuible exclusivamente a una identidad humana (agrónomo titular de la FNC) autenticada con MFA**.
3. **Mínimo Privilegio y Cero Comodines:**
   Cada función dispone de un rol de ejecución IAM dedicado, acotado estrictamente a los recursos que requiere para su ciclo de vida (lectura del objeto origen, invocación al servicio de inferencia, escritura idempotente del resultado y enrutamiento a su cola de fallos dedicada).
4. **Patrón de Implementación para la Épica 6:**
   De las cuatro funciones diseñadas en la arquitectura, la **Función de Confirmación del Foco (`FN-CONF-FOCO`)** constituye el patrón canónico que se codifica en Terraform dentro del límite de 100 horas y dos semanas de esfuerzo. Las otras tres funciones quedan formalizadas y acotadas en este diseño de arquitectura.

---

## 2. Diagramas Oficiales de Arquitectura

El diseño del subsistema se sustenta en tres diagramas técnicos elaborados bajo el estándar XML Draw.io descomprimido UTF-8 y exportados en formato vectorial autónomo SVG de alta resolución:

### 2.1 Diagrama 1: Arquitectura General de Funciones por Eventos

Ilustra la topología integral de las cuatro funciones serverless en AWS Lambda, sus respectivos orígenes de eventos, los roles IAM de mínimo privilegio, los servicios de inferencia administrada, la persistencia en DynamoDB/S3 y el desacoplamiento con colas Dead Letter Queue (DLQ):

![Arquitectura General de Funciones Serverless por Eventos](diagrams/carga-e-funciones-arquitectura.svg)

> Archivo fuente editable en formato Draw.io XML descomprimido disponible en: [`diagrams/carga-e-funciones-arquitectura.drawio`](diagrams/carga-e-funciones-arquitectura.drawio).

### 2.2 Diagrama 2: Patrón Arquitectónico de la Función de Confirmación del Foco (Épica 6)

Detalla el flujo paso a paso de la función a codificar en Terraform: lectura en streaming, filtro ético anti-PII con Amazon Rekognition (Ley 1581 de 2012), diagnóstico fitosanitario multimodal administrado con Amazon Bedrock (sin entrenamiento y sin cómputo en espera), evaluación de umbral de confianza, escritura atómica condicional en DynamoDB y derivación segura a DLQ:

![Patrón Arquitectónico de Confirmación del Foco](diagrams/carga-e-funciones-foco-patron.svg)

> Archivo fuente editable en formato Draw.io XML descomprimido disponible en: [`diagrams/carga-e-funciones-foco-patron.drawio`](diagrams/carga-e-funciones-foco-patron.drawio).

### 2.3 Diagrama 3: Ciclo de Vida de Resiliencia, Reintentos Exponenciales y Aislamiento de Fallas (DLQ)

Modela la máquina de estados de ejecución, la política de reintentos exponenciales con jitter aleatorio, el destino de fallos asíncrono, la preservación del objeto intacto, la activación de alarmas CloudWatch P1 y el procedimiento de redrive operativo:

![Ciclo de Vida de Resiliencia y DLQ](diagrams/carga-e-funciones-resiliencia-dlq.svg)

> Archivo fuente editable en formato Draw.io XML descomprimido disponible en: [`diagrams/carga-e-funciones-resiliencia-dlq.drawio`](diagrams/carga-e-funciones-resiliencia-dlq.drawio).

---

## 3. Especificación Técnica Exhaustiva de las Cuatro Funciones

| ID | Nombre de Función | Disparador Principal | Servicio de Inferencia | Expediente Destino |
|---|---|---|---|---|
| **FN-01** | `FN-CONF-FOCO` | S3 Event (`raw-images/focos/`) | Rekognition (PII) + Bedrock Multimodal (Diagnóstico) | `ExpedienteFitosanitario` |
| **FN-02** | `FN-VERIF-POST` | S3 Event (`raw-images/verificaciones/`) | Bedrock Multimodal (Eficacia y Remisión) | `ExpedienteFitosanitario` |
| **FN-03** | `FN-ESTIM-COSECHA` | S3 Event (`raw-images/estimaciones/`) | Bedrock Multimodal (Fenología y Maduración) | `ExpedienteCosecha` |
| **FN-04** | `FN-TELEMETRIA-BATCH` | SQS Batch (`telemetry-live`, HU #12) | Motor de Reglas FNC (Umbrales Dinámicos) | `telemetry` (DynamoDB) |

### 3.1 Función 1 (Patrón Épica 6): Confirmación del Foco (`FN-CONF-FOCO`)

- **Identificador Lógico:** `FN-CONF-FOCO`
- **Nombre Físico en AWS:** `aromapacifico-prod-focus-confirmation-fn`
- **Propósito:** Procesar la evidencia fotográfica recolectada por el dron agrícola durante el Servicio 2 (confirmación de alerta de plaga en lote), verificar perimetralmente que no exponga datos personales identificables (Ley 1581 de 2012), diagnosticar la patología foliar presente (roya o broca) mediante visión multimodal administrada sin entrenamiento y registrar el resultado en el expediente fitosanitario.
- **Disparador:** Notificación de eventos de Amazon S3 (`s3:ObjectCreated:Put`) sobre el prefijo `raw-images/focos/{FincaID}/{LoteID}/` en el bucket de producción `aromapacifico-objetos-prod`.
- **Entrada y Formato de Carga Útil:** Evento estándar S3 Event Notification en JSON:
  ```json
  {
    "Records": [
      {
        "eventVersion": "2.1",
        "eventSource": "aws:s3",
        "awsRegion": "us-east-1",
        "eventTime": "2026-11-08T15:00:00.000Z",
        "eventName": "ObjectCreated:Put",
        "s3": {
          "bucket": {
            "name": "aromapacifico-objetos-prod",
            "arn": "arn:aws:s3:::aromapacifico-objetos-prod"
          },
          "object": {
            "key": "raw-images/focos/FINCA-CAUCA-012/LOTE-02/foto_foco_9412.jpg",
            "size": 4194304,
            "eTag": "d41d8cd98f00b204e9800998ecf8427e"
          }
        }
      }
    ]
  }
  ```
- **Inferencia Invocada (Dos Etapas Serverless Desacopladas):**
  1. *Filtro Perimetral de Privacidad Anti-PII (Amazon Rekognition):*
     - Invoca `rekognition:DetectFaces` y `rekognition:DetectLabels` (evaluando categorías humanas: `Person`, `Human`, `Worker` con umbral de confianza > 50%).
     - Si se detecta un rostro o persona identificable, la función copia la imagen al bucket de cuarentena `s3://aromapacifico-quarantine-pii/` en la cuenta de Seguridad (`AromaPacifico-Security`), elimina el objeto del bucket de producción y suspende de inmediato la inferencia fitosanitaria ($0 invertido en modelos de plagas, protegiendo los derechos fundamentales del titular bajo la Ley 1581 de 2012).
     - El expediente registra el estado `PII_DETECTED_BLOQUEADO` y no se emite ninguna orden fitosanitaria.
  2. *Diagnóstico Agronómico Multimodal Administrado (Amazon Bedrock):*
     - En cumplimiento de las dos reglas categóricas del enunciado:
       - *"No se entrena un modelo. Se usa inferencia administrada."* (Se erradica Rekognition Custom Labels que exigía etiquetar y entrenar un modelo).
       - *"No hay cómputo persistente en espera de objetos."* (Se erradica Custom Labels que cobraba ~$4.00 USD por hora de unidad de inferencia activa, pasando a un modelo Pay-per-Call de $0.00 USD en reposo).
     - Se invoca la API administrada `bedrock-runtime:InvokeModel` en `us-east-1` utilizando un Modelo Fundacional Multimodal de Visión pre-entrenado (ej. `anthropic.claude-3-haiku-20240307-v1:0` o `amazon.nova-lite-v1:0`).
     - Se envía la imagen codificada en base64 junto con un prompt de sistema agronómico estructurado que instruye al modelo a evaluar signos de *Hemileia vastatrix* (roya: pústulas amarillas/anaranjadas en el envés, clorosis) o *Hypothenemus hampei* (broca: perforaciones en el ápice de la cereza) y retornar un esquema JSON determinista:
       ```json
       {
         "diagnostic_label": "ROYA_NIVEL_3",
         "confidence_score": 92.4,
         "affected_area_pct": 28.5,
         "severity": "ALTA",
         "reasoning": "Presencia densa de pústulas esporulantes anaranjadas en el envés foliar con necrosis foliar incipiente en rama terciaria."
       }
       ```
     - Costo por llamada: ~$0.0016 - $0.0025 USD por imagen (facturación por tokens de entrada/salida).
- **Salida Escrita en el Expediente:** Actualización atómica condicional en la tabla DynamoDB `ExpedienteFitosanitario`:
  ```json
  {
    "FincaID": "FINCA-CAUCA-012",
    "FocoID#Timestamp": "FOCO-9412#2026-11-08T15:00:05Z",
    "LoteID": "LOTE-02",
    "TimestampUTC": "2026-11-08T15:00:05Z",
    "SourceObjectID": "raw-images/focos/FINCA-CAUCA-012/LOTE-02/foto_foco_9412.jpg",
    "SourceSHA256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "ConfidenceScore": 92.4,
    "DiagnosticLabel": "ROYA_NIVEL_3",
    "EvaluatorID": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
    "EstadoFoco": "CONFIRMADO",
    "RequiereAtencionHumana": true,
    "OrdenFumigacionID": null
  }
  ```
- **Permisos IAM Mínimos (Zero Trust):**
  - `s3:GetObject` y `kms:Decrypt` sobre `arn:aws:s3:::aromapacifico-objetos-prod/raw-images/focos/*`.
  - `rekognition:DetectFaces` y `rekognition:DetectLabels` sobre `*` (para filtro PII perimetral).
  - `bedrock:InvokeModel` sobre `arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0`.
  - `dynamodb:UpdateItem` y `dynamodb:PutItem` sobre `arn:aws:dynamodb:us-east-1:*:table/ExpedienteFitosanitario`.
  - `sqs:SendMessage` sobre `arn:aws:sqs:us-east-1:*:dlq-confirmacion-foco`.

---

### 3.2 Función 2: Verificación Post-Fumigación (`FN-VERIF-POST`)

- **Identificador Lógico:** `FN-VERIF-POST`
- **Nombre Físico en AWS:** `aromapacifico-prod-fumigation-verification-fn`
- **Propósito:** Evaluar la evidencia fotográfica de verificación capturada por el dron durante el Servicio 4 posterior a una aspersión autorizada. Determina si el foco de plaga fue efectivamente controlado (remisión foliar, estabilización necrótica de pústulas) o si persiste actividad biológica patógena.
- **Disparador:** Notificación de eventos de Amazon S3 (`s3:ObjectCreated:Put`) sobre el prefijo `raw-images/verificaciones/{FincaID}/{OrdenFumigacionID}/` en el bucket de producción `aromapacifico-objetos-prod`.
- **Entrada y Formato:** Evento JSON S3 con puntero al objeto fotográfico y metadatos del vuelo post-aplicación (tiempo transcurrido, cuadrilla UAS, identificador de orden).
- **Inferencia Invocada (Amazon Bedrock Multimodal):**
  - Invoca la API administrada `bedrock-runtime:InvokeModel` en `us-east-1` (sin entrenamiento previo ni servidores en espera).
  - Compara la evidencia fotográfica actual contra el diagnóstico inicial del foco (`DiagnosticLabel` previo), evaluando el porcentaje de tejido foliar recuperado y el cese de esporulación activa de roya o broca.
  - Retorna un dictamen cuantitativo en JSON con `remision_pct`, `remanencia_activa_pct` y `confidence_score`.
- **Salida Escrita en el Expediente:** Modificación del expediente de la orden en `ExpedienteFitosanitario`:
  - `EficaciaAspersion`: Porcentaje de remisión foliar.
  - `TimestampVerificacionUTC`: Fecha y hora del análisis.
  - `SourceVerificacionID`: Clave del archivo S3 evaluado.
  - `EvaluatorID`: `arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0`.
  - `HabilitadoParaCierre`: Booleano en `true` si la eficacia supera el umbral agronómico (> 85%).
  - **Invariante crítica de negocio:** Si la imagen no llega, la invocación a Bedrock falla o la eficacia es insuficiente, **el estado de la fumigación sigue ABIERTA**. Bajo ninguna circunstancia esta función muta la orden a cerrada ni emite un cierre ficticio.
- **Permisos IAM Mínimos:**
  - `s3:GetObject` y `kms:Decrypt` sobre `raw-images/verificaciones/*`.
  - `bedrock:InvokeModel` sobre el modelo fundacional multimodal de visión.
  - `dynamodb:UpdateItem` en `ExpedienteFitosanitario` condicionado a `attribute_exists(OrdenID)`.
  - `sqs:SendMessage` en `dlq-verificacion-fumigacion`.

---

### 3.3 Función 3: Estimación de Rendimiento de Cosecha (`FN-ESTIM-COSECHA`)

- **Identificador Lógico:** `FN-ESTIM-COSECHA`
- **Nombre Físico en AWS:** `aromapacifico-prod-harvest-estimation-fn`
- **Propósito:** Procesar ortofotos multiespectrales o de alta resolución obtenidas en el Servicio 5 (vuelo de área previo a cosecha) para proyectar el volumen de café cereza maduro y la cantidad estimada de sacos estándar de 60 kg que ingresarán a cada centro de acopio departamental.
- **Disparador:** Notificación de eventos de Amazon S3 (`s3:ObjectCreated:Put`) sobre el prefijo `raw-images/estimaciones/{DepartamentoID}/{FincaID}/`.
- **Entrada y Formato:** Puntero a imagen de alta resolución o composición ortomosaica acompañada del polígono GeoJSON delimitador del lote.
- **Inferencia Invocada (Amazon Bedrock Multimodal):**
  - Invoca `bedrock-runtime:InvokeModel` en `us-east-1` (modelo multimodal administrado sin entrenamiento).
  - Evalúa la distribución cromática y fenológica del fruto (conteo y proporción relativa de frutos maduros rojo cereza vs. verdes) y la densidad de carga de copa vegetativa.
  - Aplica la fórmula agronómica calibrada por Cenicafé para proyectar la biomasa cosechable en sacos de 60 kg.
- **Salida Escrita en el Expediente:** Registro en la tabla DynamoDB `ExpedienteCosecha`:
  - `SacosEstimados60kg`: Proyección matemática entera para la finca y lote.
  - `MargenIncertidumbrePct`: Intervalo de confianza de la estimación (+/- 12%).
  - `FechaProyeccionUTC`: Marca temporal UTC.
  - `AcopioDestinoID`: Acopio receptor programado (`ACOPIO-CAUCA`, `ACOPIO-HUILA` o `ACOPIO-TOLIMA`).
  - `EvaluatorID`: `arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0`.
  - **Restricción Categórica de Negocio:** Este resultado es un pronóstico volumétrico para balance logístico de acopios y bodegas. **NUNCA genera automáticamente órdenes de empaque de sacos ni altas en la tabla de sacos de 60 kg**.
- **Permisos IAM Mínimos:**
  - `s3:GetObject` y `kms:Decrypt` sobre `raw-images/estimaciones/*`.
  - `bedrock:InvokeModel` sobre el modelo fundacional multimodal de visión.
  - `dynamodb:PutItem` en `ExpedienteCosecha`.
  - `sqs:SendMessage` en `dlq-estimacion-cosecha`.

---

### 3.4 Función 4: Lote de Telemetría y Detección de Anomalías (`FN-TELEMETRIA-BATCH`)

- **Identificador Lógico:** `FN-TELEMETRIA-BATCH`
- **Nombre Físico en AWS:** `aromapacifico-prod-telemetry-batch-fn`
- **Propósito:** Ingerir lotes de lecturas normalizadas de cultivo y secadero, evaluar las variables contra la versión activa de umbrales agronómicos de la Federación, persistir la serie temporal de forma idempotente en DynamoDB y despachar alertas al teléfono del caficultor en menos de 5 minutos ante desviaciones críticas.
- **Disparador Oficial (Alineación con HU #12):**
  - **Cola Amazon SQS `telemetry-live`** (y `telemetry-replay` para lecturas recuperadas tras cortes celulares de hasta 24 horas), definida formalmente en [`carga-a-ingesta-telemetria.md`](carga-a-ingesta-telemetria.md).
  - Se erradica por completo la propuesta de una regla MQTT aislada (`SELECT * FROM 'fincas/+/telemetria'`), integrándose plenamente con el flujo institucional:
    $$\text{Nodo IoT} \xrightarrow{\text{MQTT / SBD}} \text{AWS IoT Core Basic Ingest} \xrightarrow{\text{Regla SQL}} \text{Lambda Normalizador} \xrightarrow{\text{SQS}} \textbf{FN-04}$$
  - Configuración del Event Source Mapping de Lambda:
    - `BatchSize`: 10 mensajes por invocación.
    - `MaximumBatchingWindowInSeconds`: 0 segundos (procesamiento reactivo inmediato para preservar el presupuesto de latencia < 5 minutos).
    - `FunctionResponseTypes`: `["ReportBatchItemFailures"]` (manejo granular de fallos por mensaje individual).
- **Entrada y Formato de Carga Útil (Sobre Normalizado de HU #12):**
  ```json
  {
    "Records": [
      {
        "messageId": "sqs-msg-45812903",
        "receiptHandle": "AQEBwJn...",
        "body": "{\"schema_version\":1,\"event_id\":\"cultivo-000151\",\"sequence\":151,\"occurred_at\":\"2026-11-08T14:00:00Z\",\"device_id\":\"FINCA-HUILA-045-NODE-01\",\"farm_id\":\"FINCA-HUILA-045\",\"kind\":\"cultivo\",\"calibration_version\":\"cultivo-v1\",\"measurements\":{\"soil_n_mg_kg\":50,\"soil_p_mg_kg\":20,\"soil_k_mg_kg\":80,\"soil_moisture_pct\":55.0,\"soil_temperature_c\":21.5,\"soil_ph\":5.2,\"air_rh_pct\":65.0,\"air_temperature_c\":31.2},\"quality\":{\"status\":\"valid\",\"clock\":\"trusted\"},\"transport\":\"cellular\",\"payload_hash\":\"a4f89b6c43...\"}"
      }
    ]
  }
  ```
- **Evaluación de Reglas y Umbrales Agronómicos:**
  - No consume visión por computador. Lee con consistencia fuerte (`ConsistentRead = true`) el puntero activo de la tabla `thresholds` en DynamoDB.
  - Evalúa cada medición contra los límites oficiales configurables:
    - pH fuera de 4,5 a 6,0 (recomendado entre 4,9 y 5,6).
    - Temperatura del aire fuera de 14 °C a 30 °C (recomendado entre 17 °C y 23 °C).
    - Humedad relativa del aire fuera de 40% a 80%.
    - Temperatura de secadero superior a 40 °C (riesgo de daño térmico al embrión del grano).
    - Humedad de secadero cercana al 12% (indicador de cierre de lote).
- **Salida Escrita en el Expediente y Notificación:**
  1. *Persistencia Idempotente:* Escritura transaccional en la tabla `telemetry` de DynamoDB con clave primaria `PK: DEVICE#{device_id}`, `SK: EVENT#{event_id}`, y registro de control en `ingest_control` para deduplicación estricta ante drenado de buffers de 24 horas.
  2. *Despacho de Alerta Inmediata:* Si alguna variable excede el umbral, publica un mensaje estructurado en Amazon SNS (`arn:aws:sns:us-east-1:*:alertas-cultivo-caficultores`), entregando la notificación push/SMS al teléfono móvil del productor en **menos de 5 minutos (presupuesto medido: 245 segundos)**.
- **Permisos IAM Mínimos:**
  - `sqs:ReceiveMessage`, `sqs:DeleteMessage` y `sqs:GetQueueAttributes` sobre `telemetry-live` y `telemetry-replay`.
  - `dynamodb:GetItem` sobre `arn:aws:dynamodb:us-east-1:*:table/thresholds`.
  - `dynamodb:PutItem`, `dynamodb:UpdateItem` y `dynamodb:TransactWriteItems` sobre `telemetry` e `ingest_control`.
  - `sns:Publish` sobre `arn:aws:sns:us-east-1:*:alertas-cultivo-caficultores`.
  - `sqs:SendMessage` sobre `arn:aws:sqs:us-east-1:*:telemetry-dlq`.

---

## 4. Invariante de No Mutación en Falla y Preservación del Objeto de Origen

El requerimiento central de esta historia de usuario estipula: *"que cada función se dispare con un evento, escriba su resultado en el expediente y no cambie nada si falla, para que una invocación caída no deje un caso en un estado falso"*.

Para dar cumplimiento matemático y arquitectónico a este mandato, la plataforma implementa cuatro salvaguardas formales:

| Principio Técnico | Mecanismo de Implementación en la Plataforma |
|---|---|
| **1. Preservación Objeto de Origen en S3** | Modos de acceso `s3:GetObject` en solo lectura; prohibición estricta de `s3:PutObject`/`DeleteObject` en buckets raw para la Lambda. |
| **2. Escritura Atómica Condicional (DDB)** | Inserción condicional DynamoDB (`attribute_not_exists`) que aborta la transacción si el estado previo del expediente ha mutado. |
| **3. Aislamiento Asíncrono en Colas DLQ** | Máximo 2 reintentos con backoff exponencial y jitter; enrutamiento directo a SQS DLQ sin alterar el expediente. |
| **4. Estado Nominal Conservado** | El expediente permanece en `PENDIENTE_EVALUACION`; una falla técnica nunca genera un estado `FALSO_POSITIVO` o `DESCARTADO`. |

### 4.1 Garantía 1: Inmutabilidad del Almacén de Objetos (S3)
Las funciones Lambda bajo ninguna circunstancia modifican, renombran ni eliminan los archivos fotográficos ni los registros de vuelo depositados en `s3://aromapacifico-objetos-prod/`. 
- El permiso concedido en IAM es exclusivamente `s3:GetObject` acotado al prefijo del evento.
- El bucket S3 cuenta con **S3 Versioning** y **S3 Object Lock** en modo Gobernanza. Cualquier intento de mutación destructiva es rechazado a nivel del kernel de almacenamiento de AWS.
- La imagen original permanece íntegra como evidencia pericial y agronómica exigible por la FNC y el ICA durante los 5 años reglamentarios.

### 4.2 Garantía 2: Transaccionalidad Condicional en DynamoDB
Para evitar estados falsos producidos por invocaciones intermedias caídas o ejecuciones duplicadas de red, la escritura en DynamoDB emplea expresiones de condición (`ConditionExpression`):
```python
# Ejemplo de inserción condicional segura
response = dynamodb_table.update_item(
    Key={'FincaID': finca_id, 'FocoID#Timestamp': foco_key},
    UpdateExpression="SET EstadoFoco = :conf, ConfidenceScore = :score, SourceObjectID = :obj, EvaluatorID = :eval",
    ConditionExpression="attribute_not_exists(EstadoFoco) OR EstadoFoco = :espera",
    ExpressionAttributeValues={
        ':conf': 'CONFIRMADO',
        ':score': decimal.Decimal(str(confidence)),
        ':obj': s3_key,
        ':eval': model_arn,
        ':espera': 'PENDIENTE_EVALUACION'
    }
)
```
Si la función falla antes de ejecutar este bloque, la base de datos no registra absolutamente nada. Si falla durante la invocación del servicio Rekognition, la transacción en DynamoDB nunca se inicia.

### 4.3 Garantía 3: Preservación del Estado Previo en el Flujo de Negocio
- En la función de confirmación (`FN-CONF-FOCO`), si el procesamiento se interrumpe, el foco permanece como `PENDIENTE_EVALUACION`. El caso **no pasa a descartado ni a confirmado**.
- En la función de verificación (`FN-VERIF-POST`), si la llamada a visión falla, la orden de fumigación **sigue ABIERTA**. No se emite la habilitación de cierre.
- En la función de telemetría (`FN-TELEMETRIA-BATCH`), si falla la validación, el lote permanece en la cola SQS para reintento y el buffer local del nodo retiene las lecturas hasta recibir la confirmación de la plataforma.

---

## 5. Detalle de Implementación para Codificación en la Épica 6 (Terraform IaC)

Conforme a la delimitación del proyecto, la función `FN-CONF-FOCO` se codifica como el patrón formal de cómputo serverless en la Épica 6 (`aromapacifico-platform/iac`). A continuación se suministra la especificación exacta de recursos, variables y políticas listas para su materialización en Terraform.

### 5.1 Estructura del Módulo Terraform `serverless_function`

```text
iac/modules/serverless_function/
|-- main.tf              # Recursos Lambda, permisos S3, destinos asíncronos y SQS DLQ
|-- variables.tf         # Variables tipadas con validaciones de entorno y prefijos
|-- outputs.tf           # ARNs de la función, del rol IAM y de la cola DLQ
\-- iam.tf               # Políticas de mínimo privilegio sin comodines
```

### 5.2 Definición de Recursos en Terraform (`main.tf`)

```hcl
# Cola Dead Letter Queue dedicada para aislamiento de fallas
resource "aws_sqs_queue" "dlq_focus_confirmation" {
  name                      = "aromapacifico-${var.environment}-dlq-confirmacion-foco"
  message_retention_seconds = 1209600 # 14 días reglamentarios
  kms_master_key_id         = var.kms_data_key_arn

  tags = merge(var.mandatory_tags, {
    Componente = "DLQ"
    Funcion    = "FN-CONF-FOCO"
  })
}

# Alarma de CloudWatch para detectar fallas encoladas en DLQ
resource "aws_cloudwatch_metric_alarm" "dlq_messages_alarm" {
  alarm_name          = "aromapacifico-${var.environment}-alarm-dlq-confirmacion-foco"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 60
  statistic           = "Maximum"
  threshold           = 0
  alarm_description   = "Alerta P1: Existen mensajes en la DLQ de confirmación de foco. Inferencia fallida."
  alarm_actions       = [var.sre_alerts_sns_topic_arn]

  dimensions = {
    QueueName = aws_sqs_queue.dlq_focus_confirmation.name
  }

  tags = var.mandatory_tags
}

# Función AWS Lambda ejecutada en subred privada VPC
resource "aws_lambda_function" "focus_confirmation" {
  function_name = "aromapacifico-${var.environment}-process-focus-confirmation"
  role          = aws_iam_role.focus_confirmation_role.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  architectures = ["arm64"] # Graviton2 para eficiencia de costo FinOps
  memory_size   = 512
  timeout       = 30

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [var.lambda_security_group_id]
  }

  environment {
    variables = {
      ENVIRONMENT          = var.environment
      DYNAMODB_TABLE_NAME  = var.dynamodb_expediente_table_name
      QUARANTINE_BUCKET    = var.quarantine_s3_bucket_name
      BEDROCK_MODEL_ID     = "anthropic.claude-3-haiku-20240307-v1:0"
      CONFIDENCE_THRESHOLD = "80.0"
    }
  }

  tags = merge(var.mandatory_tags, {
    Componente = "LambdaInferencia"
    FuncionID  = "FN-CONF-FOCO"
  })
}

# Configuración de destinos asíncronos y reintentos automáticos
resource "aws_lambda_function_event_invoke_config" "focus_confirmation_invoke_config" {
  function_name                = aws_lambda_function.focus_confirmation.function_name
  maximum_retry_attempts       = 2
  maximum_event_age_in_seconds = 3600

  destination_config {
    on_failure {
      destination = aws_sqs_queue.dlq_focus_confirmation.arn
    }
  }
}

# Permiso para que Amazon S3 invoque la función Lambda
resource "aws_lambda_permission" "allow_s3_invocation" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.focus_confirmation.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = var.objects_s3_bucket_arn
}
```

### 5.3 Política de Mínimo Privilegio en IAM (`iam.tf`)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadRawImages",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Resource": "arn:aws:s3:::aromapacifico-objetos-prod/raw-images/focos/*"
    },
    {
      "Sid": "AllowKMSDecryptSource",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/cmk-data-objects-prod"
    },
    {
      "Sid": "AllowRekognitionPIIFilter",
      "Effect": "Allow",
      "Action": [
        "rekognition:DetectFaces",
        "rekognition:DetectLabels"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowBedrockMultimodalInference",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
    },
    {
      "Sid": "AllowDynamoDBUpdateExpediente",
      "Effect": "Allow",
      "Action": [
        "dynamodb:UpdateItem",
        "dynamodb:PutItem",
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/ExpedienteFitosanitario"
    },
    {
      "Sid": "AllowSQSSendDLQ",
      "Effect": "Allow",
      "Action": [
        "sqs:SendMessage"
      ],
      "Resource": "arn:aws:sqs:us-east-1:123456789012:aromapacifico-prod-dlq-confirmacion-foco"
    },
    {
      "Sid": "AllowVPCAccessExecution",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface"
      ],
      "Resource": "*"
    }
  ]
}
```

### 5.4 Impacto del Rediseño Serverless en el Patrón de la Épica 6 (Issue #25 y Tarea T6)

El reemplazo de Rekognition Custom Labels por **Amazon Bedrock (Multimodal Vision API)** y la alineación de la ingesta con la cola SQS de la HU #12 transforman positivamente la implementación de la Épica 6:

1. **Eliminación Total de Cómputo Ocioso y Complejidad MLOps:**
   Rekognition Custom Labels exigía aprovisionar recursos `aws_rekognition_project`, cargar y etiquetar imágenes de entrenamiento, y orquestar llamadas `StartProjectVersion` / `StopProjectVersion` para encender Unidades de Inferencia (Inference Units). Dichas unidades conllevaban un costo fijo obligatorio de **~$4,00 USD por hora** ($96 USD diarios o $2.880 USD mensuales si quedaba encendido 24/7), violando la regla de "cero cómputo en espera". Con Bedrock, la invocación es puramente Pay-per-Call vía SDK (`boto3.client('bedrock-runtime').invoke_model()`), con costo **estrictamente de $0,00 USD en reposo**.
2. **Cero Entrenamiento Requerido:**
   Se cumple al 100% la restricción del enunciado: *"No se entrena un modelo. Se usa inferencia administrada"*. Bedrock opera mediante modelos fundacionales pre-entrenados con capacidades multimodales avanzadas, guiados mediante prompts agronómicos estructurados.
3. **Viabilidad Estricta dentro del Límite de 100 Horas (Tarea T6):**
   La tarea T6 del plan de 100 horas tenía asignadas 16 horas. Al no tener que codificar pipelines de entrenamiento, datasets de S3 ni orquestadores de encendido/apagado de Custom Labels, el módulo Terraform `serverless_function` se enfoca en recursos nativos simples y reproducibles (bucket S3, Lambda arm64, rol IAM, SQS DLQ y mapeo de eventos), garantizando que `terraform plan` corra limpiamente y sin dependencias bloqueantes de infraestructura.

---

## 6. Cuadro Integral de Parámetros, Tags, IDs y Nueva Nomenclatura de Verificaciones

Para asegurar la coherencia arquitectónica entre las historias de usuario de gobierno, red, drones y funciones, se integra el catálogo de identificadores del proyecto y se formula una **nueva nomenclatura sistemática de verificaciones (`CHK-XXX`)**.

### 6.1 Taxonomía de Identificadores y Tags de Plataforma

| Dimensión | Formato Canónico de Identificador | Ejemplo de Identificador | Tag Obligatorio Asociado |
|---|---|---|---|
| **Fincas** | `FINCA-{DPTO}-{NUM3}` | `FINCA-CAUCA-012` | `FincaID` |
| **Drones** | `DRON-{DPTO}-{NUM2}` | `DRON-HUILA-02` | `DronID` |
| **Centros Acopio** | `ACOPIO-{DPTO}` | `ACOPIO-TOLIMA` | `AcopioID` |
| **Viajes Camión** | `VIAJE-{DPTO}-{FECHA}-{NUM3}` | `VIAJE-CAU-20261108-005` | `ViajeID` |
| **Órdenes Fumiga** | `ORD-FUM-{FECHA}-{NUM4}` | `ORD-FUM-20261108-0142` | `OrdenID` |
| **Sacos de Café** | `SACO-{DPTO}-{ANO}-{NUM5}` | `SACO-TOL-2026-04812` | `SacoID` |
| **Ambientes Cloud**| `dev`, `test`, `prod` | `prod` | `Ambiente` |

### 6.2 Nueva Nomenclatura Formal de Verificaciones (`CHK-XXX`)

Se define un esquema de códigos estandarizados para gobernar las verificaciones que ejecutan las funciones serverless de extremo a extremo:

- **`CHK-INT-01` (Integridad y Origen del Objeto):** Valida que el archivo en S3 o el paquete IoT no esté truncado, contenga un hash SHA-256 válido y provenga de un dispositivo autenticado (mTLS o URL prefirmada).
- **`CHK-ETH-02` (Filtro Ético de Privacidad Anti-PII):** Evaluación perimetral de presencia de personas y rostros mediante Amazon Rekognition (`DetectFaces` y `DetectLabels`). Exclusión inmediata de imágenes a cuarentena bajo Ley 1581 de 2012.
- **`CHK-AGR-03` (Diagnóstico Agronómico Multimodal y Umbrales):** Ejecución de inferencia de patología mediante Amazon Bedrock o evaluación de reglas de variables de suelo/secado sobre la tabla `thresholds`. Asignación del vector de confianza $C \in [0, 100\%]$.
- **`CHK-EXP-04` (Persistencia Idempotente en Expediente):** Escritura atómica condicional con tupla `{TimestampUTC, ConfidenceScore, SourceObjectID, EvaluatorID}` impidiendo duplicidades por reintentos o drenado de buffer.
- **`CHK-ST-05` (Invarianza de Estados y Protección Humana):** Garantiza que si la confianza es baja o la función falla, el estado nominal del caso no muta; bloquea cualquier emisión de orden sin firma humana MFA.
- **`CHK-DLQ-06` (Aislamiento en Cola de Fallos y Telemetría SRE):** Enrutamiento del mensaje fallido a SQS DLQ tras agotar reintentos, preservando el archivo original intacto y emitiendo alarma CloudWatch P1.

### 6.3 Matriz Exhaustiva de Parámetros, Tags y Verificaciones Complementadas

| Función ID | Tags Obligatorios Asignados | Entrada y Origen | Inferencia / Servicio | Expediente y Salida | Cadena de Verificación Complementaria (CHK) |
|---|---|---|---|---|---|
| **FN-CONF-FOCO** | `FincaID`, `DronID`, `Ambiente`, `Propietario`, `Proyecto` | S3 PutObject `raw-images/focos/` (SSE-KMS) | Rekognition (PII) + Bedrock (Multimodal) | `ExpedienteFitosanitario`: TimestampUTC, Confianza%, SourceID, EstadoFoco | `CHK-INT-01` -> `CHK-ETH-02` -> `CHK-AGR-03` -> `CHK-EXP-04` -> `CHK-ST-05` |
| **FN-VERIF-POST** | `FincaID`, `DronID`, `OrdenID`, `Propietario`, `Proyecto` | S3 PutObject `raw-images/verificaciones/` (Token misión) | Amazon Bedrock Multimodal (Remisión foliar) | `ExpedienteFitosanitario`: EficaciaAspersion, HabilitaCierre: true | `CHK-INT-01` -> `CHK-AGR-03` -> `CHK-EXP-04` -> `CHK-ST-05` (Orden sigue abierta si falla) |
| **FN-ESTIM-COSECHA** | `DronID`, `AcopioID`, `Ambiente`, `Propietario`, `Proyecto` | S3 PutObject `raw-images/estimaciones/` (GeoJSON Lote) | Amazon Bedrock Multimodal (Fenología/Biomasa) | `ExpedienteCosecha`: SacosEstimados60kg, MargenIncertidumbre | `CHK-INT-01` -> `CHK-AGR-03` -> `CHK-EXP-04` -> `CHK-ST-05` (Cero órdenes de empaque) |
| **FN-TELEMETRIA-BATCH** | `FincaID`, `DispositivoID`, `Ambiente`, `Propietario`, `Proyecto` | SQS `telemetry-live` / `telemetry-replay` (HU #12) | Motor de Reglas Umbrales FNC (`thresholds`) | `telemetry` (DynamoDB): Serie temporal NPK, Alerta SNS | `CHK-INT-01` -> `CHK-AGR-03` -> `CHK-EXP-04` -> `CHK-DLQ-06` (Reintento automático) |

---

## 7. Justificación de Decisiones Arquitectónicas y Tablas Comparativas

A continuación se presentan las matrices analíticas que sustentan las elecciones de ingeniería, demostrando cómo la solución adoptada maximiza el valor para el negocio cafetero sin incurrir en sobrecostos ni arquitecturas frágiles:

### 7.1 Comparativa de Cómputo: AWS Lambda Serverless vs. Amazon ECS/EKS vs. EC2 Dedicado

| Criterio de Selección | Opción Seleccionada: AWS Lambda (Graviton2) | Alternativa 1: Amazon ECS en Fargate | Alternativa 2: Servidores EC2 Dedicados |
|---|---|---|---|
| **Costo en Reposo ($)** | **$0,00 USD (Cero costo sin eventos)** | ~$35,00 USD/mes por tarea activa mínima | ~$48,00 USD/mes por instancia t4g.medium |
| **Tiempo de Arranque (Cold Start)** | **< 350 ms en subred privada VPC** | 30 a 60 segundos por aprovisionamiento | Inmediato si está encendido (desperdicio) |
| **Escalabilidad ante Ráfagas** | **Instantánea (hasta 1.000 concurrentes)** | Lenta (minutos en escalar tareas) | Rígida (fija o requiere Auto Scaling) |
| **Mantenimiento Operativo** | **Cero parches de SO ni gestión de clúster** | Gestión de plantillas de tarea y redes | Parcheo mensual de Linux y vulnerabilidades |
| **Justificación de Negocio** | El piloto procesa imágenes de drones esporádicas y lotes IoT espaciados (cada 4 horas). Pagar por servidores o tareas en espera consumiría presupuesto innecesariamente. Lambda garantiza pagar **exclusivamente por milisegundo de ejecución real**. |

### 7.2 Comparativa de Visión e Inferencia Administrada: Por qué Bedrock Multimodal vs. Rekognition Custom Labels

El pliego del caso de estudio establece dos restricciones explícitas e innegociables:
1. *"No se entrena un modelo. Se usa inferencia administrada."*
2. *"No hay cómputo persistente en espera de objetos."*

A continuación se evalúan las cuatro alternativas tecnológicas del ecosistema AWS:

| Criterio de Análisis | Opción Seleccionada: Amazon Bedrock Multimodal | Alternativa 1: Rekognition Custom Labels (RECHAZADA) | Alternativa 2: Rekognition DetectLabels Estándar | Alternativa 3: Amazon SageMaker Serverless |
|---|---|---|---|---|
| **Entrenamiento Previo** | **CERO entrenamiento**. Modelo fundacional multimodal pre-entrenado. | **EXIGE entrenamiento** con imágenes etiquetadas del cultivo. | **Cero entrenamiento** (pero sin clases de roya ni broca). | Exige empaquetar y versionar un artefacto de modelo propio. |
| **Costo Fijo en Reposo** | **$0,00 USD / mes** ($0 cuando no hay vuelos). | **~$4,00 USD / hora** (~$96/día o ~$2.880/mes si queda activo). | **$0,00 USD / mes** (pago por imagen pura). | **$0,00 USD / mes** (pero frío de 3-10 segundos en arranque). |
| **Modelo de Facturación** | **Pay-per-Call por token** (~$0,0016 - $0,0025 USD / imagen). | Cobro por hora de Unidad de Inferencia activa (Inference Unit). | Pay-per-Call ($0,0010 USD / imagen analizada). | Cobro por GB-segundo de inferencia invocada. |
| **Precisión Diagnóstica** | **Alta**: Comprende contexto foliar, envés, pústulas y severidad. | Alta (pero requiere dataset inicial de cientos de fotos). | **Insuficiente**: Detecta "planta", "hoja", pero no patologías. | Alta (si se entrena un modelo ResNet/YOLO botánico). |
| **Filtro Anti-PII Integrado** | Se delega a Rekognition `DetectFaces`/`DetectLabels` ($0,0010). | No filtra PII de forma nativa en la misma llamada. | Excelente para detectar `Person`, `Human`, `Worker`. | Requiere pipeline dual con modelo de rostros. |
| **Cumplimiento del Pliego** | **100% CUMPLE** ambas reglas (sin entrenamiento y sin espera). | **VIOLA AMBAS REGLAS** (exige entrenamiento y cobra en espera). | Cumple reglas pero **no diagnostica roya/broca**. | Viola la regla de inferencia administrada sin modelo. |

**Conclusión y Sustentación Técnica:**
Amazon Rekognition Custom Labels queda formalmente **rechazado** por violar la premisa de no-entrenamiento y por incurrir en cómputo esperando objetos de alto costo ($4,00 USD/hora por unidad de inferencia). La combinación arquitectónica óptima adoptada consiste en:
- **Amazon Rekognition (`DetectFaces` + `DetectLabels`):** Utilizado exclusivamente como filtro perimetral ético y de privacidad anti-PII ($0,0010 USD por llamada).
- **Amazon Bedrock (Modelos Multimodales):** Utilizado como motor agronómico administrado para diagnóstico foliar de roya y broca, verificación post-fumigación y estimación de cosecha volumétrica, pagando estrictamente por invocación real (~$0,002 USD por llamada) y garantizando **$0,00 USD de costo fijo**.

### 7.3 Comparativa de Resiliencia: SQS DLQ vs. Reintentos Infinitos vs. Descarte Silencioso

| Criterio de Selección | Opción Seleccionada: Amazon SQS DLQ | Alternativa 1: Reintentos Infinitos | Alternativa 2: Descarte Silencioso (Drop) |
|---|---|---|---|
| **Impacto en Facturación** | **Predecible y acotado (máximo 2 reintentos)** | Facturación descontrolada por bucle infinito | Nulo (pero con pérdida crítica de datos) |
| **Preservación de Evidencias** | **Mensaje retenido 14 días con contexto** | Riesgo de bloqueo de la cola de ingesta | Destrucción de la traza de la plaga |
| **Tiempo de Recuperación (MTTR)** | **< 30 minutos vía SQS DLQ Redrive** | Horas intentando desbloquear el pipeline | Imposible recuperar (requiere volar dron) |
| **Justificación de Negocio** | La FNC no puede permitir que una falla transitoria de red descarte un brote de roya en una finca, ni tampoco que un error reintente indefinidamente multiplicando los costos de Lambda. SQS DLQ logra el equilibrio perfecto entre **resiliencia total y disciplina FinOps**. |

---

## 8. Análisis FinOps Detallado y Retorno de Valor al Negocio

### 8.1 Modelado Matemático de Consumo y Costeo en Mes Normal vs. Mes de Cosecha

El dimensionamiento económico se fundamenta en las cifras consolidadas del pliego: 200 fincas, 60 transportadores, cadencia de 1.300 vuelos anuales (distribuidos en 6 meses de cosecha y 6 meses fuera de cosecha):

| Componente / Servicio AWS | Mes Normal (Fuera Cosecha) | Mes de Cosecha (Pico Carga) |
|---|---|---|
| Invocaciones Lambda FN-01 (Focos) | 15 vuelos/mes: $0,001 USD | 45 vuelos/mes: $0,003 USD |
| Invocaciones Lambda FN-02 (Verificación) | 10 vuelos/mes: $0,001 USD | 35 vuelos/mes: $0,002 USD |
| Invocaciones Lambda FN-03 (Estimación) | 0 vuelos/mes: $0,000 USD | 65 vuelos/mes: $0,008 USD |
| Invocaciones Lambda FN-04 (Telemetría SQS HU #12) | 36.000 msgs: $0,008 USD | 108.000 msgs: $0,022 USD |
| Filtro PII Amazon Rekognition (Llamadas API) | 25 imágenes: $0,025 USD | 145 imágenes: $0,145 USD |
| Inferencia Multimodal Amazon Bedrock (Tokens) | 25 imágenes: $0,050 USD | 145 imágenes: $0,290 USD |
| Persistencia Amazon DynamoDB (`telemetry`/`thresholds`) | 36.000 ops: $0,045 USD | 108.000 ops: $0,135 USD |
| Colas Amazon SQS + DLQs (Requests) | 36.000 reqs: $0,014 USD | 108.000 reqs: $0,043 USD |
| Monitoreo CloudWatch (Métricas/Logs) | 2 GB ingest: $1,140 USD | 5 GB ingest: $2,850 USD |
| **TOTAL MENSUAL CONSOLIDADO** | **$1,284 USD / mes** | **$3,498 USD / mes** |
| **COSTO ANUAL ESTIMADO SUBSISTEMA** | **~$28,69 USD / año** | **~$28,69 USD / año** |
| Monitoreo CloudWatch (Métricas/Logs) | 2 GB ingest: $1,140 USD | 5 GB ingest: $2,850 USD |
| **TOTAL MENSUAL CONSOLIDADO** | **$1,234 USD / mes** | **$3,208 USD / mes** |
| **COSTO ANUAL ESTIMADO SUBSISTEMA** | **~$26,65 USD / año** | **~$26,65 USD / año** |

### 8.2 Valor Aportado al Negocio Cafetero
1. **Erradicación del CapEx Ocioso:** Un clúster tradicional de Kubernetes o máquinas virtuales costaría al menos $150 USD mensuales ($1.800 USD/año). La arquitectura serverless diseñada cuesta **menos de $27 USD anuales**, liberando recursos financieros para subsidiar kits de sensores a los caficultores.
2. **Mitigación de Pérdidas Agrícolas:** Al entregar alertas de secadero en menos de 5 minutos y confirmar focos fitosanitarios con precisión > 80%, se previene la sobrefermentación del grano y la pérdida de lotes enteros de 60 kg (cuyo valor comercial supera los $250 USD por saco).
3. **Soberanía del Dato y Blindaje Legal:** El filtro ético automatizado en Lambda previene sanciones de la Superintendencia de Industria y Comercio (SIC) bajo la Ley 1581 de 2012, al impedir que fotos con campesinos o familias rurales salgan sin autorización hacia modelos públicos de inteligencia artificial.

---

## 9. Matriz de Gestión de Errores, Fallas y Procedimiento de SRE / Redrive

| Escenario de Falla | Impacto Técnico Inmediato | Comportamiento del Sistema | Acción SRE Requerida |
|---|---|---|---|
| **1. Throttling en API Rekognition (503)** | Rekognition retorna HTTP 503 ProvisionedThroughput. | Lambda reintenta con backoff; objeto en S3 intacto; DynamoDB no muta. | Si persiste tras 2 retries, cae a DLQ; auto-alarma CloudWatch P1. |
| **2. Falla en Endpoint VPC Privado S3/DDB** | Lambda pierde conectividad a través de Gateway VPCE. | Transacción aborta; cero registros parciales en expediente; orden nominal. | Restaurar ruta TGW en subred; ejecutar DLQ Redrive sin re-volar. |
| **3. Detección de Rostro Humano (Ley 1581)** | La toma contiene personas en el campo de cultivo. | Exclusión inmediata; copia a `quarantine-pii`; estado de foco no muta a plaga. | Ninguna acción de corrección; expediente queda protegido. |
| **4. Archivo S3 Truncado o Corrupto al Cargar** | Error de paridad o CRC al leer cabecera EXIF. | Inferencia no se ejecuta; mensaje pasa a DLQ; orden sigue PENDIENTE. | Notificar a piloto UAS para sincronización desde buffer local. |

### 9.1 Procedimiento Operativo Estándar (SOP) de Redrive desde DLQ
Cuando una alarma de CloudWatch alerta sobre mensajes acumulados en `dlq-confirmacion-foco`:
1. El ingeniero de guardia consulta el log de error en CloudWatch Logs Insights usando el `RequestID`.
2. Una vez restablecido el servicio degradado (ej. ampliación de cuota de Rekognition en la consola de AWS), se ejecuta el comando seguro de redrive:
   ```bash
   aws sqs start-message-move-task \
     --source-arn arn:aws:sqs:us-east-1:123456789012:aromapacifico-prod-dlq-confirmacion-foco \
     --destination-arn arn:aws:lambda:us-east-1:123456789012:function:aromapacifico-prod-process-focus-confirmation
   ```
3. Lambda vuelve a consumir el mensaje, lee la imagen original de S3 (que permaneció inalterada) y completa la escritura en DynamoDB con éxito rotundo.
4. **Cero desplazamientos a campo y cero horas de vuelo adicionales de drones.**

---

## 10. Registro de Supuestos de Arquitectura

Se incorporan al registro transversal de arquitectura (`assumptions-log.md`) los siguientes supuestos técnicos derivados de este subsistema:

1. **Tokens de Idempotencia en DynamoDB:** Cada actualización en el expediente utiliza como clave única la combinación `FincaID#FocoID#SHA256`, garantizando que reintentos de red o redrives de DLQ no generen registros duplicados ni incrementen contadores fitosanitarios erróneamente.
2. **Retención de 14 Días en DLQ:** Tiempo de vida de mensajes en colas de fallos fijado en 14 días (1.209.600 segundos), suficiente para cubrir contingencias operativas o periodos festivos sin pérdida de expedientes.
3. **Umbral de Confianza Fitosanitaria del 80%:** Focos detectados con confianza $\ge 80\%$ pasan a confirmación con notificación inmediata; focos con confianza $< 80\%$ se catalogan como descarte por baja confianza, requiriendo revisión agronómica secundaria solo si se repite en el siguiente vuelo.
4. **Alineación con la Ventana de Congelamiento en Cosecha:** Ninguna actualización de código Lambda ni de modelos de Rekognition puede desplegarse en producción entre las 05:00 y las 18:00 durante semanas de cosecha, en estricto cumplimiento de la gobernanza del proyecto.
