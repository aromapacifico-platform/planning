# Arquitectura y Automatizacion de Pipelines CI/CD de Infraestructura (IaC)

## 1. Resumen Ejecutivo y Cumplimiento de la Historia de Usuario

Este documento describe la arquitectura, diseño de seguridad y especificación técnica de la suite de pipelines de Integración Continua (CI), Despliegue Continuo (CD) y Detección de Desviación (Drift Detection) para la infraestructura en la nube de la **Plataforma Cafetera (Aroma Pacifico / Federacion Nacional de Cafeteros)**.

### Historia de Usuario
> **Como** lider de cambios,  
> **quiero** que todo cambio de infraestructura pase por un pipeline que genere el plan y pida aprobacion antes de produccion,  
> **para que** nadie aplique a mano ni en horario de cosecha.

### Contexto y Criterios Operativos 2026
1. **Ventana de Congelamiento en Cosecha**: Queda estrictamente prohibido realizar despliegues no emergentes a produccion entre las 05:00:00 y las 18:00:00 (hora local de Colombia, UTC-5 / `America/Bogota`) durante los ciclos calendarizados de cosecha en Cauca, Huila y Tolima. La unica excepcion admitida es la atencion de incidentes criticos mediante bypass explito y auditable.
2. **Cero Credenciales Estaticas**: Se elimina por completo el uso de llaves de acceso estaticas (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) en secretos de GitHub. La autenticacion con AWS se efectua exclusivamente mediante federacion de identidades OpenID Connect (OIDC).
3. **Flujo de Promocion Seguro**: Los cambios avanzan de manera unidireccional `dev` -> `test` -> `prod`. El entorno de produccion requiere aprobacion humana obligatoria configurada en GitHub Environments.
4. **Estados Remotos Aislados**: Cada cuenta y ambiente dispone de su propio bucket S3 cifrado con SSE-KMS y bloqueo nativo mediante archivo de bloqueo (`use_lockfile = true`), impidiendo que ejecuciones en ambientes inferiores impacten el estado de produccion.
5. **Auditoria Continua y Cero Emojis**: Deteccion automatica programada de cambios no autorizados fuera de banda y politica estricta de cero emojis en codigo, mensajes, herramientas y documentacion.

---

## 2. Topologia del Pipeline y Flujo de Promocion Multi-Ambiente

El ciclo de vida de la infraestructura se divide en dos fases principales: **Validacion en Pull Request** y **Despliegue Continuo por Promocion**.

### Diagrama de Flujo del Pipeline CI/CD

```mermaid
flowchart TD
    subgraph PR_Phase["1. Fase de Validacion en Pull Request (iac-ci-pr.yml)"]
        PR[Creacion o Actualizacion de Pull Request] --> Q1[terraform fmt -check]
        Q1 --> Q2[terraform validate]
        Q2 --> Q3[tflint recursivo con reglas AWS]
        Q3 --> Q4[trivy config - analisis estatico y misconfig]
        Q4 --> SP[Planes Especulativos OIDC]
        SP --> SP_DEV[Plan Dev]
        SP --> SP_TEST[Plan Test]
        SP --> SP_PROD[Plan Prod]
        SP_DEV & SP_TEST & SP_PROD --> PR_COMMENT[Publicacion de Resumen en Comentarios del PR]
    end

    subgraph CD_Phase["2. Fase de Despliegue Continuo (iac-cd-platform.yml)"]
        MERGE[Merge a rama main] --> DEV_DEPLOY[Despliegue Automatico a Dev]
        DEV_DEPLOY --> TEST_DEPLOY[Despliegue Automatico a Test]
        TEST_DEPLOY --> HARVEST_GATE{"Compuerta Horaria de Cosecha (05:00-18:00 UTC-5)"}
        
        HARVEST_GATE -- "En ventana y sin incidente" --> BLOCKED[Ejecucion Detenida - Bloqueo Cosecha]
        HARVEST_GATE -- "Fuera de ventana O Bypass Incidente" --> APPROVAL{"Aprobacion Manual (GitHub Environment prod)"}
        
        APPROVAL -- "Aprobado por Lider DevOps" --> PROD_DEPLOY[Despliegue Controlado a Produccion]
        APPROVAL -- "Rechazado" --> ABORT[Despliegue Cancelado]
    end

    subgraph DRIFT_Phase["3. Auditoria Continua (iac-drift-detection.yml)"]
        CRON[Programacion Nocturna 02:00 COT] --> DRIFT_AUDIT[terraform plan -detailed-exitcode]
        DRIFT_AUDIT --> DRIFT_CHECK{"Existe Desviacion?"}
        DRIFT_CHECK -- "Codigo de Salida 2" --> ISSUE[Creacion de Issue de Alerta en GitHub]
        DRIFT_CHECK -- "Codigo de Salida 0" --> SYNC[Infraestructura Sincronizada]
    end
```

### Matriz de Ambientes y Aislamiento de Estados

| Ambiente | Cuenta AWS | Rango VPC | Bucket de Estado S3 | Llave KMS de Estado | Mecanismo de Bloqueo |
|---|---|---|---|---|---|
| **dev** | AromaPacifico-Dev | `10.50.0.0/16` | `aromapacifico-tfstate-dev` | `alias/aromapacifico-tfstate` | S3 Native Lockfile |
| **test** | AromaPacifico-Test | `10.60.0.0/16` | `aromapacifico-tfstate-test` | `alias/aromapacifico-tfstate` | S3 Native Lockfile |
| **prod** | AromaPacifico-Prod | `10.70.0.0/16` | `aromapacifico-tfstate-prod` | `alias/aromapacifico-tfstate` | S3 Native Lockfile |

El aislamiento estricto por cuenta garantiza que ninguna credencial u operacion en desarrollo o pruebas tenga alcance sobre los recursos de produccion.

---

## 3. Arquitectura de Seguridad y Autenticacion OIDC

### Comparativa: Credenciales Estaticas vs Autenticacion Federada OIDC

| Criterio | Claves de Acceso Estaticas (Legacy 2020) | Federacion GitHub OIDC (Estandar 2026) |
|---|---|---|
| **Almacenamiento** | Guardadas en GitHub Secrets a largo plazo | Ningun secreto guardado; generacion bajo demanda |
| **Tiempo de Vida del Token** | Indefinido hasta rotacion manual | Maximo 1 hora (configurable a 15-60 min) |
| **Vector de Fuga** | Exfiltracion por logs, scripts maliciosos o compromisos | Inutilizable fuera del contexto del runner y repo |
| **Politica de Confianza** | Global a nivel de usuario IAM | Estricta por `sub` (organizacion, repositorio, rama) |
| **Auditoria en CloudTrail** | Usuario IAM generico | Sesion federada con run_id, sha y ref exactos |

### Configuracion de la Politica de Confianza IAM (Trust Policy)

Cada rol IAM asumido por los workflows (`aromapacifico-ci-dev`, `aromapacifico-ci-test`, `aromapacifico-ci-prod`) implementa una politica de confianza que restringe el acceso exclusivamente al repositorio de la plataforma:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "GitHubOIDCAuthentication",
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:aromapacifico-platform/*:*"
        }
      }
    }
  ]
}
```

Los workflows solicitan unicamente los permisos de token estrictamente necesarios:
```yaml
permissions:
  id-token: write
  contents: read
```

---

## 4. Matriz de Control de Acceso y Aprobaciones en Produccion

El despliegue hacia el ambiente `prod` utiliza la caracteristica nativa de **GitHub Environments**, configurando protecciones de despliegue obligatorias:

| Entorno GitHub | Aprobadores Requeridos | Ventana de Espera | Ramas Permitidas | Proteccion Adicional |
|---|---|---|---|---|
| `dev` | Ninguno (Automatico tras PR merge) | 0 min | `refs/heads/main` | Ninguna |
| `test` | Ninguno (Automatico tras exito en dev) | 0 min | `refs/heads/main` | Ninguna |
| `prod` | Lider DevOps / Arquitecto Cloud (1 requerido) | 0 min | `refs/heads/main` | Compuerta de Cosecha previa |

### Politica de Concurrencia
Para evitar condiciones de carrera o bloqueos simultaneos sobre el estado de Terraform, los workflows de despliegue definen grupos de concurrencia:
- `concurrency.group = iac-cd-platform-deployment` con `cancel-in-progress = false`. Esto asegura que los despliegues en cola se ejecuten ordenadamente sin abortar despliegues en curso.

---

## 5. Compuerta Horaria de Cosecha (Harvest Window Gate)

### Justificacion Operativa y Agronomica
Durante las temporadas de cosecha en Cauca, Huila y Tolima, la plataforma opera a su maxima capacidad:
- Recepcion de hasta 400 sacos diarios de 60 kg por centro de acopio (3 centros, total 1.200 sacos/dia).
- 10.800 lecturas diarias de telemetria continua (suelo NPK, humedad ambiental y secado cada hora en 200 fincas).
- Monitoreo en tiempo real de 60 transportadores con emision de posicion satelital cada 5 minutos.
- Inferencia serverless de deteccion fitosanitaria con camaras de drones.

Cualquier interrupcion o latencia inducida por despliegues en horario de operacion activa (05:00 a 18:00 hora de Colombia) pone en riesgo el secado de cafe de alta calidad, la deteccion de anomalías y la emision oportuna de alertas a caficultores.

### Reglas de Evaluacion del Script `check_harvest_window.py`

1. **Zona Horaria Canonica**: Evaluacion obligatoria en `America/Bogota` (UTC-5 sin horario de verano).
2. **Intervalo Restringido**: Desde las 05:00:00 hasta las 18:00:00 inclusive.
3. **Calendario de Cosecha**:
   - Ciclo Mitaca: Meses 4, 5, 6 (Abril, Mayo, Junio).
   - Ciclo Principal: Meses 9, 10, 11 (Septiembre, Octubre, Noviembre).
   - Configurable alternativamente por semanas ISO calendarizadas.
4. **Mecanismo de Bypass de Emergencia**:
   - Admision de flags CLI: `--emergency`, `--incident`, `--hotfix`, `--override`.
   - Variables de entorno: `EMERGENCY_OVERRIDE=true`, `INCIDENT_FLAG=true`, `HOTFIX=true`.
   - Etiquetas en GitHub PR / Issue: etiquetas que contengan `incident`, `emergency` o `hotfix`.
   - Marcador en mensaje de commit: Deteccion automatica de palabras clave en `head_commit.message`.

### Evidencias de Pruebas Unitarias Automatizadas

El script `.github/scripts/check_harvest_window.py` cuenta con una suite completa de pruebas unitarias en `.github/scripts/test_harvest_window.py` ejecutada mediante `pytest`.

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: Proyecto
collected 49 items

.github/scripts/test_harvest_window.py::TestTimestampParsingAndTimezone (5 pruebas)      PASSED
.github/scripts/test_harvest_window.py::TestRestrictedHours (7 pruebas)                  PASSED
.github/scripts/test_harvest_window.py::TestHarvestSeasonDetection (13 pruebas)           PASSED
.github/scripts/test_harvest_window.py::TestEvaluationScenarios (5 pruebas)              PASSED
.github/scripts/test_harvest_window.py::TestEmergencyBypass (13 pruebas)                PASSED
.github/scripts/test_harvest_window.py::TestCommandLineInterface (6 pruebas)             PASSED

============================= 49 passed in 0.18s ==============================
```

Casos de prueba clave cubiertos:
- Limite exacto 04:59:59 (Permitido).
- Limite exacto 05:00:00 (Bloqueado).
- Mediodia 12:00:00 durante cosecha (Bloqueado).
- Limite exacto 18:00:00 (Bloqueado).
- Limite exacto 18:00:01 (Permitido).
- Operacion nocturna 20:00:00 durante cosecha (Permitido).
- Mediodia 12:00:00 en meses fuera de cosecha (Enero, Julio, Diciembre) (Permitido).
- Mediodia 12:00:00 durante cosecha con flag de incidente o etiqueta PR (Permitido con bypass auditado).
- Conversion de sellos de tiempo UTC (`15:00:00Z` -> `10:00:00 COT` -> Bloqueado).

---

## 6. Arquitectura de los Tres Pipelines de la Plataforma

Siguiendo lo estipulado en la Historia de Usuario y la arquitectura global de Aroma Pacifico, se definen los tres pipelines de la solucion:

```mermaid
flowchart LR
    subgraph P1["Pipeline 1: Plataforma Cloud (Codificado)"]
        P1_CODE[Terraform iac/] --> P1_CI[CI: fmt, validate, tflint, trivy]
        P1_CI --> P1_CD[CD: dev -> test -> harvest gate -> prod]
    end

    subgraph P2["Pipeline 2: Ingesta IoT (Fincas y Centros)"]
        P2_CODE[Firmware y Config IoT] --> P2_TEST[Pruebas Unitarias y Simulacion CBOR]
        P2_TEST --> P2_CANARY[Despliegue Canario en Finca Patron]
        P2_CANARY --> P2_FLEET[Despliegue Progresivo a 200 Fincas y 3 Acopios]
    end

    subgraph P3["Pipeline 3: Objetos de Vuelo (Drones)"]
        P3_CODE[Funciones Serverless y Modelos] --> P3_VAL[Validacion de Contratos y Privacidad]
        P3_VAL --> P3_STAGE[Staging S3 y Notificaciones Lambda]
        P3_STAGE --> P3_HUMAN{"Compuerta Humana Previa a Fumigacion"}
        P3_HUMAN --> P3_EXEC[Despliegue a Flota de Drones]
    end
```

### 6.1. Pipeline de Plataforma (Codificado en `.github/workflows/`)
- **Repositorio**: `aromapacifico-platform/iac` (o `.github` compartido).
- **Alcance**: Despliegue de componentes base de AWS (VPC, subredes, endpoints de VPC para S3/DynamoDB/KMS/Logs, politicas de firewall, colas SQS con DLQ, tablas DynamoDB y roles IAM de minimo privilegio).
- **Workflows Implementados**:
  - `iac-ci-pr.yml`: Evaluacion estatica de formato, linter, seguridad y generacion de planes especulativos en PRs.
  - `iac-reusable-tf-pipeline.yml`: Modulo reutilizable de ejecucion `init`, `plan` y `apply` parametrizado por ambiente.
  - `iac-cd-platform.yml`: Orquestador de despliegue continuo con promocion secuencial `dev` -> `test` -> `prod`, compuerta de cosecha y aprobacion manual.
  - `iac-drift-detection.yml`: Deteccion de desviacion nocturna sin ejecucion destructiva.

### 6.2. Pipeline de Ingesta IoT (Fincas y Borde)
- **Alcance**: Gestion y despliegue del software de borde para los microcontroladores y sensores en las 200 fincas y 3 centros de acopio.
- **Caracteristicas Arquitectonicas**:
  1. **Pruebas de Codificacion CBOR y Delta**: Verificacion de empaquetado binario ligero para enlaces de bajo ancho de banda (2G/4G rural).
  2. **Validacion de Buffer Store-and-Forward**: Simulacion automatizada de desconexion celular por 24 horas; verificacion de almacenamiento en memoria no volatil y drenado por prioridad al restablecerse la conectividad.
  3. **Despliegue Canario (Canary Rollout)**: Las actualizaciones de firmware o umbrales agronómicos se aplican primero en la **Finca Patron** instanciada en el ambiente. Solo tras 48 horas sin alarmas de desconexion o degradacion de bateria, se liberan por lotes del 10% a la flota general de fincas mediante AWS IoT Jobs.
  4. **Aislamiento Criptografico**: Cada dispositivo posee su propio certificado X.509 unico y politicas de IoT Core con variables de sustitucion (`${iot:Connection.Thing.ThingName}`), impidiendo que un nodo comprometido publique en temas de otra finca.

### 6.3. Pipeline de Recepcion de Objetos de Vuelo (Drones)
- **Alcance**: Funciones Lambda de procesamiento de misiones, buckets S3 con replicacion entre regiones (`us-east-1` a `us-east-2`), maquinas de estado de fumigacion y canalizaciones hacia AWS Rekognition y Bedrock.
- **Caracteristicas Arquitectonicas**:
  1. **Compuerta Innegociable de Autorizacion Humana**: Ninguna orden de vuelo del Servicio 3 (Fumigacion de Precision) puede publicarse al dron sin la confirmacion explicita, firma digital y cierre del registro de vuelo por parte del agrónomo responsable.
  2. **Filtro Estricto de Privacidad (Ley 1581 de 2012)**: En la canalizacion de inferencia serverless, si una imagen aerea contiene personas o rostros identificables, se descarta automaticamente de la inferencia agronómica y no se almacena en el catalogo general.
  3. **Tolerancia a Fallos y DLQ**: Las notificaciones de S3 disparan funciones Lambda protegidas por colas de descarte (DLQ) con retencion de 14 dias y cifrado KMS, garantizando que ninguna evidencia de vuelo se pierda ante cortes transitorios.

---

## 7. Procedimiento Operativo de Emergencia (Runbook)

En caso de requerirse un despliegue correctivo durante la ventana de congelamiento de cosecha (05:00 a 18:00 UTC-5):

1. **Creacion de Rama de Hotfix**:
   Nombrar la rama con prefijo de incidente: `hotfix/issue-<numero>-<descripcion>`.
2. **Etiquetado del Pull Request**:
   Asignar obligatoriamente la etiqueta `incident` o `emergency` en GitHub.
3. **Validacion Automatizada**:
   El pipeline `iac-ci-pr.yml` ejecuta los controles de calidad y genera el plan especulativo.
4. **Merge y Aprobacion**:
   Al fusionarse en `main`, el workflow `iac-cd-platform.yml` detectara la etiqueta o el mensaje de commit (`fix(sec): resolve critical vulnerability [emergency]`).
5. **Paso de la Compuerta**:
   El script `check_harvest_window.py` detectara el bypass, registrara la justificacion en los logs de ejecucion y emitira codigo de salida `0`.
6. **Aprobacion Humana en Produccion**:
   El lider DevOps revisa el plan final y autoriza el despliegue en el GitHub Environment `prod`.
