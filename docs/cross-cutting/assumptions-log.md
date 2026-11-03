# Registro de supuestos

Supuestos que no están en el enunciado y que tomó el equipo al diseñar la plataforma. Cada historia agrega sus filas.

| Supuesto | Justificación | Issue que lo originó | Estado |
|---|---|---|---|
| La nube principal es AWS, en `us-east-1`, y la segunda nube preparada es Azure | Decisión base de los Senior; ver `docs/governance-and-decisions/briefing-inicial-juniors.md` | Fase 0 | Decidido |
| La Épica 6 codifica el módulo de ingesta de telemetría y la función de confirmación del foco | Decisión base de los Senior; el módulo de consulta del saco queda solo en la arquitectura | Fase 0 | Decidido |
| Modo de vuelo de drones combinado: áreas para delimitación/estimación y precisión para foco/aspersión | Maximiza cobertura espacial, reduce insumos químicos y optimiza el consumo de baterías LiPo | #4 (b-drones) | Decidido |
| Modelo de operación UAS centralizado en 3 cuadrillas (Cauca, Huila, Tolima) bajo RAC 100 de Aerocivil | Cumple con MTOW > 25 kg, dispersión de plaguicidas ICA y evita sobrecosto de hardware por finca | #4 (b-drones) | Decidido |
| Invariante Zero Trust en aspersión: autorización atribuible exclusivamente a agrónomo FNC con MFA | Previene dispersión no controlada de químicos; la inferencia IA solo asiste el diagnóstico | #4 (b-drones) | Decidido |
| Cadencia anual de drones: 1.300 vuelos en año 1 (200 delimitación, 280 confirmación, 210 fumigación, 210 verificación, 400 estimación) | Proyección basada en 6 meses de cosecha y 6 meses fuera de cosecha para 200 fincas | #4 (b-drones) | Decidido |
| Preposicionamiento offline de órdenes de fumigación con token criptográfico (Lease 48h) | Evita aplicaciones desincronizadas con la fenología o vencimiento de la ventana meteorológica | #14 (b-orden) | Decidido |
| Resiliencia ante desconexión celular en finca: operación nominal autónoma por GNSS RTK y buffer local | La falta de cobertura en lote no interrumpe el vuelo; los logs de aspersión se retienen en flash SPI | #14 (b-orden) | Decidido |
| Cierre probatorio inmutable condicionado a doble factor: hash SHA-256 de vuelo y foto de verificación S4 | Garantiza trazabilidad legal ante el ICA y Aerocivil, impidiendo cerrar casos sin evidencia física | #14 (b-orden) | Decidido |
| Zonas No-Fly compiladas en hardware de navegación para corte instantáneo de aspersión | Protege fuentes hídricas y viviendas incluso si la cuadrilla opera 100% desconectada | #14 (b-orden) | Decidido |
