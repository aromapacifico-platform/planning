# Plantilla Estandarizada de Release Notes de Aplicacion

## Plataforma Cafetera AromaPacifico (Federacion Nacional de Cafeteros 2026)

**Historia:** [#32](https://github.com/aromapacifico-platform/planning/issues/32). **Dependencia:** [#19](https://github.com/aromapacifico-platform/planning/issues/19). **Responsable:** Lider de Operaciones de Plataforma / DevOps Senior.  
**Estado:** Estandar Oficial de Gestion del Cambio. **Cajas de Arquitectura:** E6-05 (Trazabilidad del Saco y Consulta Publica) / E6-03 (Ingesta IoT y Alertas de Cultivo).

---

## 1. Resumen Ejecutivo y Marco de Gestion del Cambio

El presente documento define la **Plantilla Oficial y Estandarizada de Release Notes de Aplicacion** de la plataforma cafetera **AromaPacifico**, operada en conjunto con la Federacion Nacional de Cafeteros (FNC) para el piloto 2026 en los departamentos de Cauca, Huila y Tolima.

El objetivo de esta plantilla es normalizar de manera estricta y auditable la comunicacion, aprobacion, ejecucion y posible reversión de cualquier actualizacion en las aplicaciones y servicios de la plataforma, garantizando que tanto los cambios en la **consulta publica del saco** como en las **alertas fitosanitarias y de cultivo** se comuniquen con el mismo nivel de rigor tecnico, institucional y financiero.

### Los Seis Campos Obligatorios del Estandar
Toda nota de liberacion de aplicacion en AromaPacifico debe contener obligatoriamente los seis nucleos de informacion definidos por la gobernanza de la plataforma:
1. **Que Cambia**: Descripcion de la modificacion funcional, version semantica, componentes involucrados, contratos de datos (JSON) y compatibilidad hacia atras.
2. **Ventana de Despliegue**: Cronograma exacto en horario local (COT, UTC-5) y UTC, duracion presupuestada y cumplimiento estricto de la ventana de congelamiento de cosecha (05:00 a 18:00 COT).
3. **Impacto Operativo y en Usuarios**: Evaluacion por perfil (Caficultor, Transportador, Operario de Acopio, Comprador Internacional), impacto en la disponibilidad y cumplimiento de los Acuerdos de Nivel de Servicio (SLO/SLA).
4. **Aprobacion Formal**: Registro de la compuerta humana colegiada con identificacion de los cuatro roles signatarios, autenticacion multifactor (MFA) y trazabilidad inmutable.
5. **Aviso a la Federacion**: Protocolo institucional de divulgacion a directivas, comites departamentales y mesas de ayuda con tiempos de pre-aviso y canales oficiales.
6. **Procedimiento de Vuelta Atras (Rollback)**: Pasos tecnicos deterministas, criterios de activacion de alarmas y tiempo de recuperacion (RTR) para restaurar el servicio en caso de contingencia.

---

## 2. Estructura de la Plantilla de Release Notes

A continuacion se presenta la estructura canonica que debe diligenciarse integramente para cada cambio de aplicacion:

```markdown
# Release Notes de Aplicacion: [Nombre del Release o Capacidad] - v[X.Y.Z]

## Plataforma Cafetera AromaPacifico (Federacion Nacional de Cafeteros 2026)

**Identificador de Release:** REL-APP-[ANIO]-[NUMERO_SECUENCIAL]  
**Version Semantica:** v[X.Y.Z]  
**Servicio / Componente:** [Nombre del Servicio o Modulo de Aplicacion]  
**Fecha Programada de Ejecucion:** [AAAA-MM-DD]  
**Responsable de Operaciones:** [Nombre y Cargo del Lider de Operaciones]  
**Estado:** [Borrador / En Revision / Aprobado / Desplegado / Revertido]  
**Caja de Arquitectura Asociada:** [E6-01 a E6-08]  
**Historia de Usuario / Issue:** [#[Numero]](URL_AL_ISSUE)

---

### Campo 1: Que Cambia

#### 1.1 Descripcion General del Cambio
[Resumen ejecutivo en lenguaje tecnico claro que detalle que funcionalidad se agrega, modifica, corrige o retira.]

#### 1.2 Componentes de Software y Servicios Afectados
- **Capa Edge / CDN:** [Amazon CloudFront, funciones CloudFront Functions / Lambda@Edge, AWS WAFv2]
- **Capa de Entrada / API:** [Amazon API Gateway HTTP/REST, rutas modificadas, politicas de throttling]
- **Capa de Computo:** [Funciones AWS Lambda modificadas, runtime, asignacion de memoria y timeout]
- **Capa de Datos y Persistencia:** [Amazon DynamoDB, tablas maestras y tablas proyectadas, indices GSI/LSI]
- **Capa de Mensajeria y Eventos:** [Amazon SNS, Amazon SQS, EventBridge, DynamoDB Streams]
- **Aplicaciones Cliente:** [App Caficultor (Flutter/React Native), App Transportador, Portal Web Consulta del Saco]

#### 1.3 Contrato de Interfaz y Esquema de Datos (Payload JSON)
[Especificar el contrato de interfaz antes y despues del cambio, resaltando los nuevos campos o modificaciones.]

##### Esquema Anterior (Baseline):
```json
{
  "campo_existente_1": "tipo_dato",
  "campo_existente_2": 123
}
```

##### Esquema Nuevo (Propuesto):
```json
{
  "campo_existente_1": "tipo_dato",
  "campo_existente_2": 123,
  "nuevo_campo_agronomo": "valor_nuevo"
}
```

#### 1.4 Compatibilidad Hacia Atras (Backward Compatibility)
[Detallar si el cambio es aditivo o no destructivo. Justificar por que los clientes que consumen la version previa continuaran operando sin requerir actualizaciones simultaneas forzadas.]

---

### Campo 2: Ventana de Despliegue

#### 2.1 Cronograma y Horarios Programados
| Fase de la Ventana | Horario Local (Colombia, COT / UTC-5) | Horario Universal (UTC) | Duracion Presupuestada |
|---|---|---|---|
| **Apertura de Ventana y Verificacion Previa** | HH:MM | HH:MM | XX minutos |
| **Despliegue en Ambiente de Staging / Canario** | HH:MM | HH:MM | XX minutos |
| **Promocion Progresiva de Trafico (Canary)** | HH:MM | HH:MM | XX minutos |
| **Validacion de Pruebas de Humo (Smoke Tests)** | HH:MM | HH:MM | XX minutos |
| **Cierre de Ventana y Emision de Reporte** | HH:MM | HH:MM | XX minutos |
| **Ventana Total Reservada** | **HH:MM a HH:MM** | **HH:MM a HH:MM** | **XX minutos maximo** |

#### 2.2 Validacion contra la Politica de Congelamiento de Cosecha (Harvest Freeze Gate)
- **Estado de Cosecha Activa:** [Si / No] en los departamentos de Cauca, Huila y Tolima.
- **Cumplimiento de la Restriccion:** [Confirmar que la ventana seleccionada esta estrictamente fuera del intervalo 05:00 a 18:00 COT, o adjuntar la justificacion y autorizacion de bypass en caso de incidente critico clasificado.]
- **Verificacion Automatizada:** [Resultado de ejecucion del validador de cosecha `check_harvest_window.py`.]

---

### Campo 3: Impacto Operativo y en Usuarios

#### 3.1 Evaluacion de Impacto por Perfil de Usuario
| Perfil de Usuario | Impacto Funcional | Tiempo de Indisponibilidad Previsto | Accion Requerida por el Usuario |
|---|---|---|---|
| **Comprador Internacional** | [Detalle del impacto] | 0 segundos (Cero caida via Canary/CloudFront) | Ninguna / Actualizar cache navegador |
| **Caficultor (App)** | [Detalle del impacto] | 0 segundos | Ninguna |
| **Transportador (App)** | [Detalle del impacto] | 0 segundos | Ninguna |
| **Operario de Acopio (Sistemas)** | [Detalle del impacto] | 0 segundos | Ninguna |
| **Operador de Plataforma** | [Detalle del impacto] | Monitoreo en panel de observabilidad | Supervision durante la ventana |

#### 3.2 Impacto en Rendimiento y Objetivos de Nivel de Servicio (SLO)
- **SLO de Latencia de Consulta (p99):** Objetivo <= 800 ms. Latencia estimada post-cambio: [XX ms].
- **SLO de Entrega de Alerta Fitosanitaria:** Objetivo <= 300 s (5 minutos). Tiempo presupuestado: [XX s].
- **Tasa de Acierto de Cache (Cache Hit Ratio en CloudFront):** Objetivo >= 95%. Estimacion post-cambio: [XX%].
- **Consumo de Capacidad en Persistencia (DynamoDB):** [Detalle del impacto en WCU/RCU o modo On-Demand].

---

### Campo 4: Aprobacion Formal y Compuerta Colegiada

Para autorizar el paso a produccion en el entorno protegido de GitHub Environments (`prod`), se requiere la aprobacion colegiada de los cuatro roles definidos, todos validados mediante MFA (FIDO2 o TOTP) e IAM Identity Center:

| Rol de Aprobacion | Nombre del Funcionario | Dependencia / Entidad | Canal de Firma / Aprobacion | Sello de Tiempo (UTC) |
|---|---|---|---|---|
| **Lider de Operaciones de Plataforma** | [Nombre] | Operaciones Cloud AromaPacifico | GitHub Environment `prod` | AAAA-MM-DD HH:MM |
| **Arquitecto Cloud / DevOps Senior** | [Nombre] | Ingenieria de Plataforma | Pull Request Review | AAAA-MM-DD HH:MM |
| **Representante Tecnico FNC** | [Nombre] | Federacion Nacional de Cafeteros | Aprobacion Formal Ticket | AAAA-MM-DD HH:MM |
| **Oficial de Seguridad / Privacidad** | [Nombre] | Comite de Seguridad (Ley 1581) | Dictamen de Cumplimiento | AAAA-MM-DD HH:MM |

---

### Campo 5: Aviso Institucional a la Federacion

#### 5.1 Matriz de Comunicaciones y Canales
| Hito de Comunicacion | Destinatarios Oficiales | Canal Oficial | Antelacion / Plazo | Contenido del Mensaje |
|---|---|---|---|---|
| **Pre-Aviso T-72h** | Directores TI FNC, Comites Departamentales | Correo Institucional Cifrado | 72 horas antes | Alcance del cambio, ventana y medidas preventivas |
| **Recordatorio T-24h** | Mesas de ayuda, Operarios de Centro | Boletin Operativo Interno | 24 horas antes | Confirmacion de ventana y contactos de guardia |
| **Inicio de Ventana T-0** | Equipo de Soporte y Monitoreo | Canal Dedicado Slack/Teams | Al iniciar | Notificacion de inicio de aplicacion |
| **Confirmacion T+15min** | Todos los involucrados | Correo y Portal de Estado | 15 min post-cierre | Informe de exito y metricas de rendimiento |

#### 5.2 Mesa de Ayuda y Soporte de Contingencia
- **Canal de Atencion 24/7:** [Numero de contacto o cola de tickets de soporte].
- **Ingeniero de Guardia:** [Nombre y contacto de escalamiento Nivel 3].

---

### Campo 6: Procedimiento de Vuelta Atras (Rollback)

#### 6.1 Criterios de Activacion de Vuelta Atras (Disparadores Automaticos y Manuales)
El rollback se activara de forma inmediata si se cumple cualquiera de las siguientes condiciones dentro de los 15 minutos posteriores a la promocion:
1. **Tasa de Errores HTTP 5xx:** Supera el 1.0% de las solicitudes totales durante 3 minutos consecutivos en CloudWatch Metrics.
2. **Degradacion de Latencia:** La latencia p99 en Amazon API Gateway excede 1.200 ms de forma sostenida.
3. **Anomalia en Datos / Privacidad:** Deteccion de exposicion inadvertida de datos personales (PII) bajo la Ley 1581 de 2012.
4. **Fallo en Pruebas de Humo:** Incumplimiento de cualquiera de las pruebas de validacion post-despliegue.

#### 6.2 Pasos Tecnicos Deterministas para la Vuelta Atras
```bash
# 1. Reversion del enrutamiento de trafico en API Gateway / Lambda Canary hacia la version anterior
aws lambda update-alias \
  --function-name fn-[nombre-servicio] \
  --name live \
  --function-version [VERSION_PREVIA] \
  --routing-config '{"AdditionalVersionWeights": {}}'

# 2. Invalidacion inmediata de la cache de borde en Amazon CloudFront
aws cloudfront create-invalidation \
  --distribution-id [DIST_ID] \
  --paths "/[ruta-afectada]/*"

# 3. Notificacion de evento de contingencia y apertura de post-mortem
# Emision de alerta SNS hacia canal de operaciones
```

#### 6.3 Tiempo Estimado de Recuperacion (Recovery Time - RTR)
- **Tiempo de Deteccion:** Menor a 180 segundos (3 minutos) mediante alarmas de CloudWatch.
- **Tiempo de Ejecucion de Reversion:** Menor a 60 segundos (1 minuto) mediante conmutacion de alias.
- **RTR Total Consolidado:** **Menor a 4 minutos**, restituyendo el 100% de la operatividad baseline.
```

---

## 3. Evaluacion FinOps y Analisis Comparativo de Despliegue

Toda solicitud de liberacion debe justificar el modelo de despliegue adoptado bajo la perspectiva de FinOps de AromaPacifico, asegurando la premisa de **cero computo ocioso en espera**:

### 3.1 Matriz Comparativa de Estrategias de Despliegue de Aplicacion

| Criterio de Evaluacion | Alternativa Seleccionada: Serverless Canary (Lambda Alias + API Gateway) | Alternativa Descartada A: Clúster Fijo en Contenedores (ECS Fargate + ALB) | Alternativa Descartada B: Despliegue Directo In-Place sin Verificacion |
|---|---|---|---|
| **Modelo de Facturacion** | OpEx Pay-per-Request ($0,00 USD en reposo) | Costo mensual continuo ($72,50 USD / mes fijo) | OpEx Pay-per-Request con alto riesgo de falla |
| **Costo en Valle / Reposo** | **$0,00 USD / mes** | $72,50 USD / mes (2 tareas Fargate minimas + ALB) | $0,00 USD / mes |
| **Costo en Pico de Cosecha** | $4,85 USD / mes (elasticidad segun volumen) | $98,40 USD / mes (autoescalado de contenedores) | $4,85 USD / mes |
| **Mecanismo de Vuelta Atras** | Conmutacion instantanea de puntero de alias (< 60 s) | Despliegue de tarea reversa lenta (3-5 min) | Re-despliegue completo desde pipeline (10-15 min) |
| **Riesgo de Disponibilidad** | Minimo (Desvio progresivo 10% -> 50% -> 100%) | Moderado (Tiempo de drenado de conexiones) | Critico (Impacto al 100% de usuarios simultaneamente) |
| **Veredicto FinOps** | **SELECCIONADA: Ahorro del 100% en reposo y alta resiliencia** | **RECHAZADA: Sobrecosto de $870,00 USD / ano en infraestructura ociosa** | **RECHAZADA: Costo inaceptable por riesgo de indisponibilidad** |

### 3.2 Calculo Detallado del Costo Evitado
$$\text{Costo Evitado Mensual} = \text{Costo Alternativa Descartada A} - \text{Costo Solucion Adoptada} = \$72,50 - \$0,00 = \$72,50 \text{ USD / mes}$$
$$\text{Costo Evitado Anual} = \$72,50 \times 12 = \$870,00 \text{ USD / ano}$$

### 3.3 Imputacion de Costos y Tag Policy de 7 Etiquetas
Los recursos de computo y almacenamiento involucrados en el release deben mantener intacta la politica de 7 etiquetas obligatorias:
- `FincaID`: `GLOBAL` (o el identificador predial especifico en ingesta).
- `DronID`: `NO-APLICA`.
- `AcopioID`: `MULTICENTRO`.
- `ViajeID`: `NO-APLICA`.
- `Ambiente`: `produccion` (o `desarrollo` / `pruebas`).
- `Propietario`: `devops-fnc`.
- `Proyecto`: `AromaPacifico`.

### 3.4 Invariante de Presupuestos (AWS Budgets)
Queda prohibido asociar politicas de apagado automatico a los presupuestos de AWS Budgets en las cuentas de produccion. Ante una desviacion presupuestal, la accion automatica se limitara a notificar via Amazon SNS al Lider de Operaciones y a la Federacion.

---

## 4. Marco Juridico y Soberania de Datos (Ley 1581 de 2012)

La aprobacion del release requiere la certificacion formal de no vulneracion del marco legal colombiano de proteccion de datos:
1. **Tokenizacion Irreversible**: Los identificadores de consulta publica deben derivarse mediante `HMAC-SHA-256` utilizando la llave KMS maestra administrada por la FNC. Ningun release de aplicacion puede introducir endpoints que permitan la reversibilidad hacia cedulas, nombres de caficultores o coordenadas intraprediales privadas.
2. **Frontera de Soberania de Datos**:
   - **Permanece estrictamente en Colombia (Local / Edge):** Datos nominativos de cedulacion cafetera, registros biometricos, padron de fincas y rutas GPS submétricas.
   - **Transito hacia AWS `us-east-1` (N. Virginia):** Identificadores anonimizados (`SACO-2026-CAU-7F3A9C12`), variables de calidad agronomica, telemetria agregada y estados logisticos.

---

## 5. Lista de Chequeo de Conformidad (Checklist de Aprobacion)

Antes de firmar y emitir el release note de aplicacion, el Lider de Operaciones debe validar:
- [ ] Los seis campos obligatorios estan completamente diligenciados sin campos vacios ni marcadores genericos pendientes.
- [ ] La ventana de ejecucion esta programada fuera de la ventana de congelamiento de cosecha (05:00 a 18:00 COT), o cuenta con autorizacion de emergencia.
- [ ] El procedimiento de vuelta atras (rollback) esta documentado con comandos exactos y un RTR menor a 5 minutos.
- [ ] Se adjunta la matriz comparativa FinOps con al menos 2 alternativas y demostracion del costo evitado.
- [ ] Se verifica el cumplimiento estricto de la Ley 1581 de 2012 (cero exposicion de PII).
- [ ] El documento cumple con la politica de Cero Emojis y redaccion tecnica profesional en espanol.
