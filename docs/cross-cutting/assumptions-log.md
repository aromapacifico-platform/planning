# Registro de supuestos

Supuestos que no están en el enunciado y que tomó el equipo al diseñar la plataforma. Cada historia agrega sus filas.

| Supuesto | Justificación | Issue que lo originó | Estado |
|---|---|---|---|
| La nube principal es AWS, en `us-east-1`, y la segunda nube preparada es Azure | Decisión base de los Senior; ver `docs/governance-and-decisions/briefing-inicial-juniors.md` | Fase 0 | Decidido |
| La Épica 6 codifica el módulo de ingesta de telemetría y la función de confirmación del foco | Decisión base de los Senior; el módulo de consulta del saco queda solo en la arquitectura | Fase 0 | Decidido |
| Se reserva `10.90.0.0/16` para la VNet hub de Azure, sin crear recursos | No se solapa con los acopios (10.41-43) ni con las VPC de AWS (10.50, 10.60, 10.70, 10.71, 10.80) propuestas en la #7 | #10 | Asumido en el diseño; se revisa si cambia el plan de la #7 |
| La primera pieza candidata para Azure es la consulta pública del saco; ingesta, identidad de dispositivos, órdenes de fumigación y datos personales nunca se mueven | Es pública, de solo lectura, con datos ya anonimizados y con el SLO de disponibilidad más alto; mover lo demás sería duplicar la plataforma | #10 | Asumido en el diseño |
| El directorio de personas para las dos nubes es Entra ID si la Federación ya lo usa; si no, IAM Identity Center sigue como directorio | No se conoce el directorio corporativo de la Federación | #10 | Por confirmar con la Federación |
| Azure se activa solo por decisión de la Federación y con su costo estimado antes de construir | La segunda nube preparada no factura durante el piloto | #10 | Asumido en el diseño |
