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
