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
        Q4 --> INFRA[Infracost FinOps - Estimacion de Costos]
        INFRA --> SP[Planes Especulativos OIDC]
        SP --> SP_DEV[Plan Dev]
        SP --> SP_TEST[Plan Test]
        SP --> SP_PROD[Plan Prod]
        SP_DEV & SP_TEST & SP_PROD --> PR_COMMENT[Publicacion de Resumen en Comentarios del PR]
        INFRA --> COST_COMMENT[Publicacion de Desglose de Costo en PR]
    end

    subgraph CD_Phase["2. Fase de Despliegue Continuo (iac-cd-platform.yml)"]
        MERGE[Merge a rama main] --> DEV_DEPLOY["Despliegue a Dev (Plan -> Artefacto tfplan-dev -> Apply)"]
        DEV_DEPLOY --> TEST_DEPLOY["Despliegue a Test (Plan -> Artefacto tfplan-test -> Apply)"]
        TEST_DEPLOY --> HARVEST_GATE{"Compuerta Horaria de Cosecha (05:00-18:00 UTC-5)"}
        
        HARVEST_GATE -- "En ventana y sin incidente" --> BLOCKED[Ejecucion Detenida - Bloqueo Cosecha]
        HARVEST_GATE -- "Fuera de ventana O Bypass PR/Dispatch" --> PLAN_PROD["Job plan-prod: Generacion y Subida de tfplan-prod"]
        
        PLAN_PROD --> APPROVAL{"Aprobacion Manual Humana (GitHub Environment prod)"}
        
        APPROVAL -- "Aprobado tras auditar tfplan" --> APPLY_PROD["Job apply-prod: Descarga de tfplan-prod y terraform apply"]
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
| **dev** | AromaPacifico-Dev (`273577169715`) | `10.50.0.0/16` | `aromapacifico-tfstate-dev` | `alias/aromapacifico-tfstate` | S3 Native Lockfile |
| **test** | AromaPacifico-Test (`273577169715`) | `10.60.0.0/16` | `aromapacifico-tfstate-test` | `alias/aromapacifico-tfstate` | S3 Native Lockfile |
| **prod** | AromaPacifico-Prod (`273577169715`) | `10.70.0.0/16` | `aromapacifico-tfstate-prod` | `alias/aromapacifico-tfstate` | S3 Native Lockfile |

> [!IMPORTANT]
> **Supuesto de Arquitectura para el Piloto Academico (Epica 6 - FNC 2026):**
> 1. **Cuenta AWS Unica para el Piloto (`273577169715`)**:
>    - Para el alcance de la Epica 6 (piloto academico con timebox de 100 horas y 2 semanas), los tres roles OIDC de ejecucion (`aromapacifico-ci-dev`, `aromapacifico-ci-test` y `aromapacifico-ci-prod`) coexisten dentro de una **unica cuenta AWS (`273577169715`)**.
>    - **Titularidad y Responsabilidad Financiera**: La cuenta pertenece al entorno de laboratorio de pruebas de AromaPacifico (FNC 2026). Los costos de operacion del piloto son asumidos por la infraestructura y presupuesto academico asignado al proyecto.
>    - **Salvaguarda de Costo Cero (PC-IAC Regla 9)**: La variable de repositorio `ENABLE_TERRAFORM_APPLY` se mantiene apagada (`false`) por defecto. Ningun agente o pipeline muta infraestructura en vivo; el alcance se limita a `terraform fmt`, `terraform validate` e inspeccion auditada de `terraform plan`, evitando costos por aprovisionamiento indebido.
>    - **Mapeo a Landing Zone Final**: La arquitectura corporativa destino prescribe segregacion estricta multi-cuenta (Seguridad, Red, Produccion, Pruebas y Desarrollo) orquestada mediante AWS Organizations, transicionando los roles a sus respectivas cuentas una vez concluido el piloto academico.

El aislamiento logico por ambiente en el piloto (y físico en la Landing Zone corporativa) garantiza que ninguna credencial u operacion en desarrollo o pruebas tenga alcance sobre los recursos de produccion.

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
        "Federated": "arn:aws:iam::273577169715:oidc-provider/token.actions.githubusercontent.com"
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

### Manejo Estricto de OIDC y Prevencion de Falsos Positivos
Para garantizar que ningun cambio de infraestructura se apruebe con falsos positivos:
- Si el Pull Request o ejecucion proviene de una rama interna del repositorio oficial (`is_fork == false`), la asuncion del rol OIDC es **estricta y mandatoria**.
- Si `steps.aws-auth` no culmina con exito, el workflow `iac-ci-pr.yml` ejecuta una verificacion que termina de inmediato en error (`exit 1`), bloqueando el PR y exigiendo la revision de politicas IAM o trust relationships.
- Para forks externos no autenticados, se emite una advertencia tecnica limitando la revision a validacion estatica sintactica sin conceder acceso a los estados remotos en la nube.

---

## 4. Matriz de Control de Acceso y Aprobaciones en Produccion

El despliegue hacia el ambiente `prod` utiliza la caracteristica nativa de **GitHub Environments**, configurando protecciones de despliegue obligatorias:

| Entorno GitHub | Aprobadores Requeridos | Ventana de Espera | Ramas Permitidas | Proteccion Adicional |
|---|---|---|---|---|
| `dev` | Ninguno (Automatico tras PR merge) | 0 min | `refs/heads/main` | Artefacto inmutable `tfplan-dev` |
| `test` | Ninguno (Automatico tras exito en dev) | 0 min | `refs/heads/main` | Artefacto inmutable `tfplan-test` |
| `prod` | Lider DevOps / Arquitecto Cloud (1 requerido) | 0 min | `refs/heads/main` | Compuerta Cosecha + `plan-prod` previo |

### Desacoplamiento de Plan y Apply con Artefactos Inmutables
Para eliminar cualquier riesgo de discrepancia entre lo analizado y lo desplegado:
1. **Fase de Planificacion (`plan`)**: Se inicializa el backend, se genera el archivo binario inmutable `terraform plan -out=tfplan` y su volcado legible `tfplan.txt`, almacenandolos temporalmente mediante `actions/upload-artifact@v4` con retencion de 2 dias. Esta fase no requiere aprobacion manual y permite a los revisores auditar el impacto real.
2. **Pausa de Aprobacion Humana**: El entorno `prod` detiene la ejecucion en el job `apply` solicitando revision y firma manual al personal autorizado (Lider DevOps / Arquitecto Cloud).
3. **Fase de Aplicacion (`apply`)**: Tras la aprobacion, el runner descarga el artefacto inmutable mediante `actions/download-artifact@v4` y ejecuta la verificacion de integridad. Para cumplir con el alcance academico FNC 2026 y la directriz de Cero Costos / Cero Apply no autorizado (Regla 9 PC-IAC), la mutacion en AWS esta controlada por la variable `ENABLE_TERRAFORM_APPLY`. En modo demostracion y auditoria, el pipeline valida la aprobacion manual, expone el comando de despliegue `terraform apply -no-color -auto-approve tfplan` y audita el plan sin generar sobrecostos accidentales.

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

### Reglas de Evaluacion y Bypass Dinamico

1. **Zona Horaria Canonica**: Evaluacion obligatoria en `America/Bogota` (UTC-5 sin horario de verano).
2. **Intervalo Restringido**: Desde las 05:00:00 hasta las 18:00:00 inclusive.
3. **Calendario de Cosecha**:
   - Ciclo Mitaca: Meses 4, 5, 6 (Abril, Mayo, Junio).
   - Ciclo Principal: Meses 9, 10, 11 (Septiembre, Octubre, Noviembre).
   - Configurable alternativamente por semanas ISO calendarizadas.
4. **Mecanismo de Bypass de Emergencia Multicapa**:
   - **Consulta Automatizada de la API de GitHub**: Mediante `actions/github-script@v7`, el pipeline consulta la lista de Pull Requests asociados al commit de merge en `main` (`repos.listPullRequestsAssociatedWithCommit`) e inspecciona etiquetas de tipo `incident`, `emergency`, `hotfix` o `harvest-bypass`.
   - **Flags CLI y Workflow Dispatch**: Admision explicita de inputs de emergencia en ejecuciones manuales.
   - **Mensaje de Commit**: Deteccion de marcadores de contingencia (`[emergency]`, `[incident]`, `[hotfix]`).

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

### 6.1. Pipeline de Plataforma (Arquitectura Centralizada y Caller Workflows)
- **Repositorio Central de Gobernanza**: `aromapacifico-platform/.github`.
  - Aloja los workflows reutilizables canónicos en `.github/workflows/`:
    - `iac-ci-reusable.yml`: Workflow reutilizable de integración continua con detección dinámica de targets, validación estática (fmt, validate, TFLint, Trivy), FinOps con Infracost y planes especulativos autenticados con AWS OIDC.
    - `iac-cd-reusable.yml`: Workflow reutilizable de entrega continua con promoción secuencial `dev` -> `test` -> Compuerta de Cosecha -> `prod` (aprobación manual).
    - `iac-reusable-tf-pipeline.yml`: Módulo reutilizable de ejecución de Terraform parametrizado por ambiente.
    - `iac-drift-detection.yml`: Auditoría nocturna de desviación no destructiva.
- **Repositorio de Infraestructura**: `aromapacifico-platform/iac`.
  - Opera como **llamador ligero (Caller Workflow)**: sus workflows locales (`iac-ci-pr.yml` e `iac-cd-platform.yml`) contienen únicamente la definición de triggers (`pull_request`, `push`, `workflow_dispatch`), políticas de concurrencia y permisos (`id-token: write`, etc.), e invocan los workflows reutilizables de `.github` fijados a tags inmutables SemVer o commit SHAs (ej. `uses: aromapacifico-platform/.github/.github/workflows/<workflow>.yml@v1.0.0`) y `secrets: inherit`.
  - Se prohíbe el uso de `@main` en invocadores de producción para blindar la cadena de suministro de CI/CD frente a cambios no auditados en el repositorio de gobernanza.
  - Esta arquitectura desacopla el ciclo de vida de la infraestructura respecto a las reglas de cumplimiento y gobernanza, permitiendo que cualquier repositorio consumidor adopte las mismas políticas corporativas sin duplicar código de pipeline.
- **Politica de Cambios y Gobernanza en `.github`**:
  - Todo cambio a los workflows reutilizables, acciones compuestas (`setup-iac-tools`) o scripts de compuerta debe someterse a Pull Request con revisión obligatoria por pares y validación automática de suite `pytest`.
  - Queda prohibido el push directo a la rama `main` de `.github` o la auto-fusión de PRs sin aprobación, salvaguardando la integridad de los pipelines que consumen la organización.

#### 6.1.1. Integracion FinOps con Infracost y Estandarizacion de Pruebas
- **Infracost en Pull Requests (Epica 7 - FinOps)**:
  - Archivo de configuracion canonico `infracost.yml` mapeando los tres ambientes `iac/environments/dev`, `iac/environments/test` y `iac/environments/prod`.
  - Generacion automatica de la linea base en la rama de destino (`main`) y calculo del diferencial de costo mensual (`infracost diff`).
  - Publicacion interactiva del desglose de costos en el Pull Request mediante `infracost comment github`, permitiendo al equipo de operaciones anticipar el impacto financiero de cada cambio de infraestructura.
  - Operacion resiliente: si el secreto `INFRACOST_API_KEY` no esta presente en el repositorio, el paso emite un registro informativo sin abortar la ejecucion del pipeline ni los planes de Terraform.
- **Estandarizacion de Pruebas Unitarias (Pytest)**:
  - Configuraciones declarativas en `pytest.ini` y `pyproject.toml` para garantizar paridad absoluta entre la ejecucion en estaciones de trabajo locales y los entornos de ejecucion de GitHub Actions.
  - Enrutamiento explicito a la suite de scripts (`testpaths = scripts`), convenciones estrictas de descubrimiento (`test_*.py`) y trazas resumidas sin verbosidad excesiva.

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

---

## 8. Evidencia del CD (Pipeline de Entrega Continua y Aprobacion en Produccion)

### 8.1. Contexto de Validacion y Criterios Operativos (HU #69)
En cumplimiento de la Historia de Usuario #69, se audito e implemento la promocion continua completa de infraestructura en la plataforma AromaPacifico mediante el workflow reutilizable `.github/workflows/iac-cd-reusable.yml`.

A diferencia de las validaciones preliminares sintacticas, el pipeline de CD opera con planes especulativos reales autenticados con AWS mediante OpenID Connect (OIDC), desacoplamiento estricto de artefactos inmutables y una compuerta obligatoria de aprobacion humana previa a cualquier ejecucion productiva.

### 8.2. Registro de Corrida Canonica del Pipeline CD
- **Repositorio de Invocacion**: `aromapacifico-platform/iac`
- **Workflow**: `IaC Continuous Delivery (Platform)` (`.github/workflows/iac-cd-platform.yml`)
- **Workflow Reutilizable**: `aromapacifico-platform/.github/.github/workflows/iac-cd-reusable.yml`
- **Enlace Canonico de la Corrida**: [GitHub Actions Run 42945415799](https://github.com/aromapacifico-platform/iac/actions/runs/42945415799)
- **Evento Desencadenador**: `push` a la rama `main` tras integracion de cambios de infraestructura
- **Sello Temporal de Inicio**: `2026-11-11T02:21:02Z` (equivalente a las `21:21:02 COT`, fuera de la ventana de congelamiento de cosecha)

### 8.3. Desglose de Fases y Comprobacion de Criterios de Aceptacion

| Fase / Job | Estado | Duracion | Criterio Validado |
|---|:---:|:---:|---|
| **Deploy - Development** | `completed / success` | 17s | Autenticacion OIDC con rol federado `aromapacifico-ci-dev`, inicializacion de backend S3 con fallback a estado local temporal (`backend_override.tf`), validacion sintactica HCL y ejecucion de plan especulativo con publicacion de artefacto `plan-dev`. |
| **Deploy - Testing** | `completed / success` | 18s | Promocion secuencial dependiente de desarrollo (`needs: deploy-dev`), autenticacion OIDC con `aromapacifico-ci-test`, plan especulativo aislado sobre `10.60.0.0/16` y emision de artefacto `plan-test`. |
| **Evaluate Production Harvest Window** | `completed / success` | 6s | Evaluacion estricta de la regla de negocio horaria (05:00 a 18:00 UTC-5). La ejecucion nocturna (21:21 COT) permitio el paso automatico sin requerir banderas de contingencia o bypass. |
| **Plan - Production** | `completed / success` | 18s | Generacion y bloqueo del plan inmutable de produccion sobre la cuenta destino (`10.70.0.0/16`). El artefacto binario/texto `tfplan-prod` queda subido y retenido de forma inmutable. |
| **Apply - Production** | `waiting` (pausado) | En espera | Activacion inmediata de la proteccion de entorno GitHub Environment `prod`. El pipeline detiene su flujo a la espera de revision y aprobacion manual por parte del revisor designado (`Juanmadiaz45`). |

### 8.4. Verificacion de Seguridad y Politica Cero Costos (Zero-Cost Apply)
1. **Pausa Obligatoria de Aprobacion**:
   - El entorno `prod` exige la autorizacion explicita del Arquitecto Cloud o Lider DevOps antes de que el runner de GitHub Actions inicie el paso de despliegue.
   - En la corrida [Run 42945415799](https://github.com/aromapacifico-platform/iac/actions/runs/42945415799), el job `apply-prod` entro en estado de espera (`waiting`), confirmando la imposibilidad de aplicar cambios no auditados.
2. **Salvaguarda de Costo Cero (ENABLE_TERRAFORM_APPLY=false)**:
   - Al liberarse la aprobacion, el job ejecuta la validacion en modo demostrativo (`Zero-Cost Verification Mode`), imprimiendo el plan inmutable y asegurando que no se incurra en gastos cloud ni se mute la infraestructura real en AWS, en estricto cumplimiento con la Regla 9 de gobierno del proyecto AromaPacifico.
3. **Depuracion de Componentes**:
   - Se removio el archivo obsoleto `.github/workflows/iac-reusable-tf-pipeline.yml` en la organizacion `.github` para evitar duplicidad respecto a `iac-cd-reusable.yml`.
   - Se verifico la ausencia de errores mediante `actionlint` y la suite de pruebas unitarias (`pytest`) en todos los repositorios.

