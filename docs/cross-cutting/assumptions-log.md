# Registro de supuestos



Supuestos que no están en el enunciado y que tomó el equipo al diseñar la plataforma. Cada historia agrega sus filas.



| Supuesto | Justificación | Issue que lo originó | Estado |

| --- | --- | --- | --- |

| La nube principal es AWS, en `us-east-1`, y la segunda nube preparada es Azure | Decisión base de los Senior; ver `docs/governance-and-decisions/briefing-inicial-juniors.md` | Fase 0 | Decidido |

| La Épica 6 codifica el módulo de ingesta de telemetría y la función de confirmación del foco | Decisión base de los Senior; el módulo de consulta del saco queda solo en la arquitectura | Fase 0 | Decidido |

| Estructura multicuenta de Landing Zone con 6 cuentas (AromaPacifico-Root, AromaPacifico-Security, AromaPacifico-Network, AromaPacifico-Prod, AromaPacifico-Test, AromaPacifico-Dev) en 2 OUs | Aislamiento de blast radius, control de estado de Terraform y cumplimiento de retención inmutable de 5 años | #1 (gob-lz) | Decidido |

| Invariante de Budgets: Notificar sin apagar servicios de ingesta ni consulta del saco | La interrupción de ingesta provocaría pérdida de cosechas por fallas de alertas agronómicas en secado | #1 (gob-lz) | Decidido |

| Taxonomía de etiquetas obligatorias: FincaID, DronID, AcopioID, ViajeID, Ambiente, Propietario y Proyecto | Requisito del caso para costeo granular en AWS Cost Explorer y aplicación de Tag Policies | #1 (gob-lz) | Decidido |
| Plan de direccionamiento cloud no solapado: 10.50.0.0/16 (Dev), 10.60.0.0/16 (Test), 10.70.0.0/16 (Prod us-east-1), 10.71.0.0/16 (Prod DR us-east-2) y 10.80.0.0/16 (Hub Network) | Garantiza matemáticamente cero solapamiento con acopios (10.41/42/43.0.0/16) y aislamiento total de ambientes bajo RFC 1918 | #7 (red-cidr) | Decidido |
| Distribución de 7 subredes mínimas en 2 AZs (us-east-1a y us-east-1b) con tamaño /24 por subred (251 IPs útiles) | Permite alta disponibilidad multi-AZ, paridad de entornos y capacidad para más de 50.000 fincas vía ENIs de Hyperplane | #7 (red-cidr) | Decidido |
| Interconexión híbrida mediante AWS Transit Gateway centralizado en la cuenta AromaPacifico-Network con 3 Route Tables | Centraliza túneles IPsec VPN hacia acopios y aísla físicamente ambientes de desarrollo y pruebas de los sitios reales | #7 (red-cidr) | Decidido |
| Uso intensivo de Gateway VPC Endpoints para S3 y DynamoDB ($0 USD/GB) | Evita el aprovisionamiento de múltiples NAT Gateways redundantes, ahorrando más de $270 USD mensuales | #7 (red-cidr) | Decidido |
| Modo de vuelo de drones combinado: áreas para delimitación/estimación y precisión para foco/aspersión | Maximiza cobertura espacial, reduce insumos químicos y optimiza el consumo de baterías LiPo | #13 (b-drones) | Decidido |
| Modelo de operación UAS centralizado en 3 cuadrillas (Cauca, Huila, Tolima) bajo RAC 100 de Aerocivil | Cumple con MTOW > 25 kg, dispersión de plaguicidas ICA y evita sobrecosto de hardware por finca | #13 (b-drones) | Decidido |
| Invariante Zero Trust en aspersión: autorización atribuible exclusivamente a agrónomo FNC con MFA | Previene dispersión no controlada de químicos; la inferencia IA solo asiste el diagnóstico | #13 (b-drones) | Decidido |
| Cadencia anual de drones: 1.300 vuelos en año 1 (200 delimitación, 280 confirmación, 210 fumigación, 210 verificación, 400 estimación) | Proyección basada en 6 meses de cosecha y 6 meses fuera de cosecha para 200 fincas | #13 (b-drones) | Decidido |
| Incidencia de alertas fitosanitarias en sensores: 20% en cosecha y 10% fuera de cosecha | Basado en históricos de proliferación de roya y broca según humedad relativa y temperatura | #13 (b-drones) | Decidido |
| Tasa de confirmación de foco hacia orden de fumigación del 75% | El 25% restante corresponde a falsas alarmas de sensor o deficiencias nutricionales que no requieren agroquímicos | #13 (b-drones) | Decidido |
| Distribución fenológica anual: 2 cosechas al año (principal y mitaca) estructuradas en 6 meses de cosecha y 6 meses fuera de cosecha | Fenología cafetera estándar en Cauca, Huila y Tolima que rige la cadencia de vuelos | #13 (b-drones) | Decidido |
| Modelo de atención de alertas fuera de cosecha: consolidación trimestral con despacho bajo demanda (< 72h SLA) para alertas críticas | Concilia la disponibilidad permanente de sensores con la logística eficiente de cuadrillas | #13 (b-drones) | Decidido |
| Preposicionamiento offline de órdenes de fumigación con token criptográfico (Lease 48h) | Evita aplicaciones desincronizadas con la fenología o vencimiento de la ventana meteorológica | #14 (b-orden) | Decidido |
| Resiliencia ante desconexión celular en finca: operación nominal autónoma por GNSS RTK y buffer local | La falta de cobertura en lote no interrumpe el vuelo; los logs de aspersión se retienen en flash SPI | #14 (b-orden) | Decidido |
| Cierre probatorio inmutable condicionado a doble factor: hash SHA-256 de vuelo y foto de verificación S4 | Garantiza trazabilidad legal ante el ICA y Aerocivil, impidiendo cerrar casos sin evidencia física | #14 (b-orden) | Decidido |
| Zonas No-Fly compiladas en hardware de navegación para corte instantáneo de aspersión | Protege fuentes hídricas y viviendas incluso si la cuadrilla opera 100% desconectada | #14 (b-orden) | Decidido |
| Invariante de no-mutación en fallas serverless: preservación íntegra de objetos en S3 y estado inalterado en DynamoDB | Evita que interrupciones de red o cuotas de inferencia dejen casos en estados falsos o descarten plagas erróneamente | #16 (e-funciones) | Decidido |
| Idempotencia transaccional en DynamoDB mediante ConditionExpression y hash SHA-256 del objeto fuente | Garantiza cero registros duplicados ante reintentos automáticos del runtime Lambda o ejecuciones de DLQ Redrive | #16 (e-funciones) | Decidido |
| Retención de 14 días en colas SQS DLQ con cifrado KMS y alerta CloudWatch P1 | Proporciona ventana operativa suficiente para remediación y redrive sin requerir nuevos vuelos de drones a campo | #16 (e-funciones) | Decidido |
| Filtro perimetral anti-PII con Amazon Rekognition DetectFaces y DetectLabels | Destinado exclusivamente a detectar presencia humana antes del análisis agronómico, derivando tomas a cuarentena S3 en cumplimiento de la Ley 1581 de 2012 | #16 (e-funciones) | Decidido |
| Diagnóstico fitosanitario foliar con modelo fundacional multimodal en Amazon Bedrock | Inferencia 100% administrada sin entrenamiento previo y costo de $0 USD en inactividad (pago estricto por invocación), descartando Rekognition Custom Labels | #16 (e-funciones) | Decidido |
| Agregación de telemetría (FN-04) acoplada a la cola SQS de ingesta de la HU #12 | FN-04 consume por lotes de 10 mensajes desde SQS telemetry-live (alimentada por IoT Basic Ingest y el normalizador de #12), garantizando desacoplamiento e idempotencia | #16 (e-funciones) | Decidido |
| Simplificación de alcance IaC en Épica 6 (#25) por inferencia serverless sin unidades dedicadas | El módulo Terraform para FN-CONF-FOCO prescinde de orquestación de Inference Units persistentes o datasets de entrenamiento, asegurando el cumplimiento del límite de 100 horas | #16 (e-funciones) | Decidido |
