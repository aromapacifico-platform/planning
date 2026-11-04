# Registro de supuestos

Supuestos que no están en el enunciado y que tomó el equipo al diseñar la plataforma. Cada historia agrega sus filas.

| Supuesto | Justificación | Issue que lo originó | Estado |
| --- | --- | --- | --- |
| La nube principal es AWS, en `us-east-1`, y la segunda nube preparada es Azure | Decisión base de los Senior; ver `docs/governance-and-decisions/briefing-inicial-juniors.md` | Fase 0 | Decidido |
| La Épica 6 codifica el módulo de ingesta de telemetría y la función de confirmación del foco | Decisión base de los Senior; el módulo de consulta del saco queda solo en la arquitectura | Fase 0 | Decidido |
| Estructura multicuenta de Landing Zone con 6 cuentas (AromaPacifico-Root, AromaPacifico-Security, AromaPacifico-Network, AromaPacifico-Prod, AromaPacifico-Test, AromaPacifico-Dev) en 2 OUs | Aislamiento de blast radius, control de estado de Terraform y cumplimiento de retención inmutable de 5 años | #1 (gob-lz) | Decidido |
| Invariante de Budgets: Notificar sin apagar servicios de ingesta ni consulta del saco | La interrupción de ingesta provocaría pérdida de cosechas por fallas de alertas agronómicas en secado | #1 (gob-lz) | Decidido |
| Taxonomía de etiquetas obligatorias: FincaID, DronID, AcopioID, ViajeID, Ambiente, Propietario y Proyecto | Requisito del caso para costeo granular en AWS Cost Explorer y aplicación de Tag Policies | #1 (gob-lz) | Decidido |
