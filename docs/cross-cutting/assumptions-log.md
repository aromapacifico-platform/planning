# Registro de supuestos

Supuestos que no están en el enunciado y que tomó el equipo al diseñar la plataforma. Cada historia agrega sus filas.

| Supuesto | Justificación | Issue que lo originó | Estado |
|---|---|---|---|
| La nube principal es AWS, en `us-east-1`, y la segunda nube preparada es Azure | Decisión base de los Senior; ver `docs/governance-and-decisions/briefing-inicial-juniors.md` | Fase 0 | Decidido |
| La Épica 6 codifica el módulo de ingesta de telemetría y la función de confirmación del foco | Decisión base de los Senior; el módulo de consulta del saco queda solo en la arquitectura | Fase 0 | Decidido |
| Del diseño de 2020 solo se toma como referencia lo que describe el enunciado (alcance, capacidades y supuestos de conectividad); no hay inventario de equipos ni de servicios de 2020 | El enunciado no entrega el documento de 2020; inventar componentes no verificables debilita la matriz | #3 | Asumido en el diseño |
| Ninguna pieza del piloto usa 2G ni 3G; el nodo de finca usa LTE-M o NB-IoT | Los operadores colombianos están apagando 2G y 3G, y el enunciado prohíbe depender de una red que se apague durante el piloto. Falta confirmar la cobertura LTE-M/NB-IoT por operador en las veredas del piloto | #3 | Por confirmar con el operador |
| La entrega en Buenaventura se registra desde la aplicación del transportador o del operario, sin infraestructura de la Federación en el puerto | El enunciado prohíbe desplegar infraestructura en el puerto y deja la telemetría del barco a la naviera | #3 | Asumido en el diseño |
