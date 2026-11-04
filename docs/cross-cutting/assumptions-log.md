# Registro de supuestos

Supuestos que no están en el enunciado y que tomó el equipo al diseñar la plataforma. Cada historia agrega sus filas.

| Supuesto | Justificación | Issue que lo originó | Estado |
|---|---|---|---|
| La nube principal es AWS, en `us-east-1`, y la segunda nube preparada es Azure | Decisión base de los Senior; ver `docs/governance-and-decisions/briefing-inicial-juniors.md` | Fase 0 | Decidido |
| La Épica 6 codifica el módulo de ingesta de telemetría y la función de confirmación del foco | Decisión base de los Senior; el módulo de consulta del saco queda solo en la arquitectura | Fase 0 | Decidido |
| Modo de vuelo de drones combinado: áreas para delimitación/estimación y precisión para foco/aspersión | Maximiza cobertura espacial, reduce insumos químicos y optimiza el consumo de baterías LiPo | #13 (b-drones) | Decidido |
| Modelo de operación UAS centralizado en 3 cuadrillas (Cauca, Huila, Tolima) bajo RAC 100 de Aerocivil | Cumple con MTOW > 25 kg, dispersión de plaguicidas ICA y evita sobrecosto de hardware por finca | #13 (b-drones) | Decidido |
| Invariante Zero Trust en aspersión: autorización atribuible exclusivamente a agrónomo FNC con MFA | Previene dispersión no controlada de químicos; la inferencia IA solo asiste el diagnóstico | #13 (b-drones) | Decidido |
| Cadencia anual de drones: 1.300 vuelos en año 1 (200 delimitación, 280 confirmación, 210 fumigación, 210 verificación, 400 estimación) | Proyección basada en 6 meses de cosecha y 6 meses fuera de cosecha para 200 fincas | #13 (b-drones) | Decidido |
| Incidencia de alertas fitosanitarias en sensores: 20% en cosecha y 10% fuera de cosecha | Basado en históricos de proliferación de roya y broca según humedad relativa y temperatura | #13 (b-drones) | Decidido |
| Tasa de confirmación de foco hacia orden de fumigación del 75% | El 25% restante corresponde a falsas alarmas de sensor o deficiencias nutricionales que no requieren agroquímicos | #13 (b-drones) | Decidido |
| Distribución fenológica anual: 2 cosechas al año (principal y mitaca) estructuradas en 6 meses de cosecha y 6 meses fuera de cosecha | Fenología cafetera estándar en Cauca, Huila y Tolima que rige la cadencia de vuelos | #13 (b-drones) | Decidido |
| Modelo de atención de alertas fuera de cosecha: consolidación trimestral con despacho bajo demanda (< 72h SLA) para alertas críticas | Concilia la disponibilidad permanente de sensores con la logística eficiente de cuadrillas | #13 (b-drones) | Decidido |
