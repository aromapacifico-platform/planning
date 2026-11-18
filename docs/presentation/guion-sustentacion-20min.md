# Guion de Sustentación (20 Minutos) y Control de Tiempo

## Plataforma Cafetera AromaPacífico (Federación Nacional de Cafeteros 2026)

**Historias:** #39, #40. **Responsable:** Equipo Arquitectura & DevOps FNC 2026. **Fecha:** 17 de noviembre de 2026.  
**Estado:** Consolidado para sustentación. **Fase:** Fase 6 - Sustentación.

---

## 1. Resumen Ejecutivo y Estructura del Ensayo

Este documento establece el guion cronometrado para la sustentación de **20 minutos** ante el arquitecto de la Federación Nacional de Cafeteros, cubriendo la estrategia de modernización 2026, conectividad sin señal, modo combinado de vuelo de drones, justificación del timebox de **100 horas** de Infraestructura como Código (Épica 6), análisis FinOps y sistema de diseño.

---

## 2. Distribución de Tiempo (20 Minutos Exactos)

| Bloque | Minuto Inicio – Fin | Duración | Tema Principal | Puntos Clave a Demostrar |
| --- | --- | ---: | --- | --- |
| **B1** | `00:00 – 05:00` | 5 min | **Contexto 2020 vs. 2026 y Conectividad sin Señal** | Retiro de 2G/3G, buffer flash 24 h, ACK de persistencia, híbrido **48 fincas LoRaWAN + 12 Iridium SBD**, 3 acopios (`10.41/42/43`), cero infraestructura en Buenaventura. |
| **B2** | `05:00 – 09:00` | 4 min | **Arquitectura Cloud, Seguridad y Ley 1581 de 2012** | AWS `us-east-1` + DR `us-east-2` (RPO 15 min / RTO 4 h) + Azure preparada (`10.90.0.0/16`), Landing Zone 6 cuentas, tokenización HMAC-SHA-256 del saco, filtro anti-PII Rekognition. |
| **B3** | `09:00 – 13:00` | 4 min | **Drones: 5 Servicios y Modo Combinado** | Áreas (delimitación/estimación) + Precisión (confirmación/fumigación/verificación), contratación por acopio bajo RAC 100, **compuerta humana del agrónomo con MFA** y misión precargada 48 h. |
| **B4** | `13:00 – 17:00` | 4 min | **Épica 6 IaC en 100 Horas y Gobernanza CI/CD** | Por qué cabe en 100 h / 2 semanas (1 ambiente, 1 finca patrón, 1 función `FN-CONF-FOCO`), 26 reglas `PC-IAC`, OIDC, **Cero Apply Mandatorio** y ventana de cosecha (05:00–18:00 COT). |
| **B5** | `17:00 – 20:00` | 3 min | **FinOps, Sistema de Diseño y Cierre** | Ahorro de **USD 289.216/año** (contratación drones, LoRaWAN compartido, retiro Network Firewall), presupuestos USD 811/841, sistema de diseño unificado para las 3 aplicaciones. |

---

## 3. Comparativa FinOps de Enfoque de Sustentación

| Criterio | Alternativa Seleccionada: Sustentación Estructurada de 20 Minutos con Evidencia Trazable | Alternativa Descartada A: Demostración en Vivo con Recursos Desplegados (`terraform apply`) | Alternativa Descartada B: Presentación Genérica sin Cifras del Piloto |
| --- | --- | --- | --- |
| **Costo Cloud Generado** | **$0,00 USD** (evidencia de `terraform validate`, `plan` y `tftest.hcl`) | Costo operativo innecesario y violación de Cero Apply Mandatorio | $0,00 USD, pero falla criterios de viabilidad y costo |
| **Riesgo de Tiempo (> 20 min)** | Mínimo (bloques cronometrados 5+4+4+4+3 min) | Alto (latencias de consola o fallos de red en vivo) | Alto (preguntas sin respaldo numérico) |

---

## 4. Registro de Control de Tiempo en Ensayo (#40)

- **Meta total:** `20:00` minutos (margen de reserva de `1:00` minuto dentro de los bloques para transiciones).
- **Regla de corte:** Si el bloque B1 supera el minuto `05:30`, se resume la tabla de VLANs del acopio para proteger los bloques B3 (drones) y B4 (100 horas IaC).
