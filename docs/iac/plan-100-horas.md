# Plan de 100 horas de la Épica 6

Este plan reparte el código de infraestructura de la Épica 6 en **100 horas y diez días hábiles**. Solo cuenta trabajo que termina en el repositorio [`iac`](https://github.com/aromapacifico-platform/iac): módulos, variables, estado remoto, pipeline y la ejecución del `plan`. La arquitectura, los costos, el sistema de diseño, las release notes y la sustentación quedan fuera.

El patrón que se codifica es el que fijó el briefing: el **módulo de ingesta de telemetría** con una **finca patrón**, y la **función de confirmación del foco**. La consulta pública del saco queda diseñada en la arquitectura, pero no se codifica.

## 1. Cajas del diagrama que implementa el código

Cada tarea apunta a una caja del diagrama de arquitectura. Los identificadores `E6-xx` son los que lleva el diagrama consolidado de la [#19](https://github.com/aromapacifico-platform/planning/issues/19).

| Caja | Qué es | Diseño de origen |
| --- | --- | --- |
| **E6-01** | Estado remoto y ambientes: bucket S3 cifrado con KMS y bloqueo, un estado por cuenta | Briefing, #1 |
| **E6-02** | VPC del ambiente: subredes del plan de direccionamiento en dos zonas, rutas y Gateway Endpoints de S3 y DynamoDB | #7 |
| **E6-03** | Conexión con un centro de acopio: VPN sitio a sitio hacia el rango de un acopio parametrizado | #7, #8 |
| **E6-04** | Seguridad de plataforma: llaves KMS, roles IAM de mínimo privilegio y reglas permanentes de firewall | #4, #5, #9 |
| **E6-05** | Ingesta de telemetría: política y reglas de IoT Core, cola, tabla de telemetría y tabla de umbrales | #12 |
| **E6-06** | Finca patrón: cosa de IoT, vínculo con su certificado y etiquetas `FincaID` | #11, #12 |
| **E6-07** | Función de confirmación del foco: bucket, notificación de S3, Lambda, inferencia administrada y DLQ | #16, #17 |
| **E6-08** | Pipeline CI/CD: GitHub Actions con OIDC, `plan` por ambiente y aprobación en producción | #26 |

## 2. Tareas, horas y responsables

| # | Tarea | Issue | Caja | Responsable | Horas | Depende de |
| --- | --- | --- | --- | --- | ---: | --- |
| T1 | Estructura del repo, backend del estado, variables por ambiente y pre-commit | [#21](https://github.com/aromapacifico-platform/planning/issues/21) | E6-01 | Juanmadiaz45 | 6 | — |
| T2 | Módulo `network`: VPC, subredes, rutas, endpoints y conexión con un acopio | [#22](https://github.com/aromapacifico-platform/planning/issues/22) | E6-02, E6-03 | juandavid175 | 22 | T1 |
| T3 | Módulo `security`: KMS, roles IAM, security groups y NACL del catálogo, verificación regla a regla | [#23](https://github.com/aromapacifico-platform/planning/issues/23) | E6-04 | Juanda-2880 | 18 | T1 |
| T4 | Pipeline CI/CD con OIDC, promoción y congelamiento en cosecha | [#26](https://github.com/aromapacifico-platform/planning/issues/26) | E6-08 | Juanda-2880 | 10 | T1 |
| T5 | Módulos `ingest` y `farm`, instanciados una vez en el ambiente | [#24](https://github.com/aromapacifico-platform/planning/issues/24) | E6-05, E6-06 | juandavid175 | 24 | T2, T3 |
| T6 | Módulo `function` de confirmación del foco | [#25](https://github.com/aromapacifico-platform/planning/issues/25) | E6-07 | Juanda-2880 | 16 | T3 |
| T7 | `plan` limpio del ambiente desde el pipeline y su evidencia | [#27](https://github.com/aromapacifico-platform/planning/issues/27) | Todas | Juanmadiaz45 | 4 | T2–T6 |
| | **Total** | | | | **100** | |

Por persona: juandavid175 46 h, Juanda-2880 44 h y Juanmadiaz45 10 h. Los juniors llevan los módulos; el senior pone la base (T1) y cierra con la evidencia (T7).

Cada junior codifica lo que diseñó en la Fase 1: juandavid175 diseñó la red, el acopio, el firewall y la ingesta (#6, #8, #9, #11, #12), y Juanda-2880 diseñó las identidades, el cifrado y las funciones (#1, #4, #5, #16, #17). Así nadie gasta horas en entender un diseño ajeno.

### Desglose de cada tarea

**T1 · 6 h**
- Estructura `bootstrap/`, `modules/` y `environments/{dev,test,prod}`: 1 h.
- Bucket del estado, llave KMS y backend con `use_lockfile`: 2 h.
- Variables con validación y `terraform.tfvars` por ambiente: 1,5 h.
- Pre-commit con `fmt`, TFLint y gitleaks, y README: 1,5 h.

**T2 · 22 h**
- VPC y siete subredes en dos zonas con `cidrsubnet` sobre el `/16` del ambiente: 6 h.
- Tablas de rutas por tipo de subred: 3 h.
- Gateway Endpoints de S3 y DynamoDB, y los endpoints de interfaz que usan las funciones (KMS y Logs): 4 h.
- Customer gateway, VPN con dos túneles y rutas hacia el acopio parametrizado: 6 h.
- Outputs, README y `validate`: 3 h.

**T3 · 18 h**
- Llaves KMS de datos, objetos y logs con su política: 4 h.
- Roles IAM de la ingesta, de la función y del despliegue, sin comodines: 5 h.
- Security groups y NACL generados con `for_each` desde las filas permanentes del `rule_catalog` de la #9: 6 h.
- Documento que cruza cada ID de regla con su recurso: 3 h.

**T4 · 10 h**
- Proveedor OIDC de GitHub y rol de despliegue por cuenta: 3 h.
- Workflow reutilizable: `fmt`, `validate`, TFLint y escaneo en cada PR, y `plan` por ambiente: 4 h.
- Ambiente `prod` con revisores obligatorios y paso que bloquea el `apply` en la ventana de cosecha salvo etiqueta de incidente: 3 h.

**T5 · 24 h**
- Tabla de telemetría (llaves, TTL, cifrado y Streams) y tabla de umbrales versionada: 6 h.
- Política de IoT por dispositivo con variables de sustitución, sin comodines: 4 h.
- Reglas de IoT hacia la cola y la cola con su DLQ: 6 h.
- Módulo `farm`: cosa, tipo, vínculo con un certificado creado fuera del estado y etiquetas: 5 h.
- Instancia de una finca en el ambiente, README y `validate`: 3 h.

**T6 · 16 h**
- Bucket de objetos de confirmación con versionado, cifrado y bloqueo público: 3 h.
- Lambda con su empaquetado mínimo, rol y notificación de S3 por prefijo: 6 h.
- Reintentos, destino de fallos (DLQ), alarma y grupo de logs con retención: 4 h.
- Permiso de invocación al servicio de inferencia, README y `validate`: 3 h.

**T7 · 4 h**
- Correr el `plan` del ambiente desde el pipeline con todos los módulos: 2 h.
- Documentar la salida, el commit exacto y la fecha: 2 h.

## 3. Calendario de dos semanas

Jornada de referencia de 5 horas por persona y día hábil. La semana 1 deja la base, la red, la seguridad y el pipeline; la semana 2 monta la ingesta y la función sobre esa base.

| Día | juandavid175 | Juanda-2880 | Juanmadiaz45 |
| --- | --- | --- | --- |
| 1 | T2 red (5 h) | T3 seguridad (5 h) | T1 base del repo (6 h) |
| 2 | T2 red (5 h) | T3 seguridad (5 h) | Revisión de PR |
| 3 | T2 red (5 h) | T3 seguridad (5 h) | Revisión de PR |
| 4 | T2 red (5 h) | T3 seguridad (3 h) + T4 pipeline (2 h) | Revisión de PR |
| 5 | T2 red (2 h) + T5 ingesta (3 h) | T4 pipeline (5 h) | Revisión de PR |
| 6 | T5 ingesta (5 h) | T4 pipeline (3 h) + T6 función (2 h) | Revisión de PR |
| 7 | T5 ingesta (5 h) | T6 función (5 h) | Revisión de PR |
| 8 | T5 ingesta (5 h) | T6 función (5 h) | Revisión de PR |
| 9 | T5 ingesta (5 h) | T6 función (4 h) | Revisión de PR |
| 10 | T5 ingesta (1 h) | — | T7 `plan` y evidencia (4 h) |

T1 ya está hecha ([iac#1](https://github.com/aromapacifico-platform/iac/pull/1)), así que los juniors arrancan el día 1 sobre una base común. La revisión de PR del senior no se cuenta en las 100 horas porque no produce código.

El orden respeta las dependencias:
- La red (T2) y la seguridad (T3) solo necesitan la base. Corren en paralelo la primera semana.
- El pipeline (T4) también depende solo de la base. Se hace antes que la función para que desde el día 6 cada PR de módulos pase por `plan` en el pipeline.
- La ingesta (T5) empieza cuando la red está terminada, el día 5. Usa las llaves y los roles de T3, que quedan listos el día 4.
- La función (T6) necesita las llaves y los roles de T3 y el diseño corregido de la #16 y la #17.
- El `plan` final (T7) espera a que estén todos los módulos.

## 4. Cambios frente al borrador junior

El borrador proponía red 22 h, seguridad 18 h, ingesta 24 h, función 16 h, CI/CD 14 h y variables y `plan` 6 h. Se conservan las cuatro primeras cifras y se cambian dos cosas:

- **CI/CD baja de 14 a 10 horas.** Un solo workflow reutilizable sirve para los tres ambientes. El rol de despliegue se define una vez y se instancia por cuenta.
- **Variables y `plan` se separan.** La base del repo con variables y estado remoto (T1) toma 6 horas, y la ejecución y evidencia del `plan` (T7) toma 4 horas, con las horas que salen del pipeline. El borrador metía ambas cosas en 6 horas, sin tiempo para el backend cifrado ni para la evidencia que pide la #27.

## 5. Riesgos y qué se recorta si una tarea se pasa

El plan suma exactamente 100 horas y no tiene reserva. Si una tarea se pasa, se recorta alcance en este orden, sin mover el límite:

1. **Endpoints de interfaz de T2.** Se dejan solo los Gateway Endpoints de S3 y DynamoDB, y la función sale por el endpoint de inferencia cuando exista.
2. **Ambiente de pruebas en T4.** Se promueve de desarrollo a producción con aprobación, y pruebas queda con `plan` sin `apply`.
3. **Expansión del catálogo en T3.** Se codifican primero las reglas del patrón (ingesta y función) y las de la consulta pública quedan en el documento de verificación como no instanciadas, tal como permite la #9.

Hay un riesgo que se controla antes de empezar T6: el servicio de inferencia está en corrección en la #16 y la #17, porque Rekognition Custom Labels exige entrenar un modelo. T6 solo cambia el permiso de invocación y la llamada, así que la corrección no mueve sus 16 horas, pero debe estar fusionada antes del día 6.

## 6. Verificación de los criterios de la #20

| Criterio | Dónde se cumple |
| --- | --- |
| La suma no pasa de 100 horas y cabe en dos semanas | Sección 2 (100 h) y sección 3 (diez días hábiles) |
| Cada tarea tiene responsable, dependencia y caja del diagrama | Tabla de la sección 2 |
| Ninguna tarea es documental | T1–T7 producen código o el `plan`. El documento de verificación de T3 y la evidencia de T7 son la salida de verificación de su código, que piden la #23 y la #27 |
