# Plantilla Estandarizada de Release Notes de Infraestructura

## Plataforma Cafetera AromaPacifico (Federacion Nacional de Cafeteros 2026)

**Historia:** [#33](https://github.com/aromapacifico-platform/planning/issues/33). **Dependencias:** [#19](https://github.com/aromapacifico-platform/planning/issues/19), [#26](https://github.com/aromapacifico-platform/planning/issues/26). **Responsable:** Lider de Cambios / Senior DevOps & Cloud Architect.  
**Estado:** Estandar Oficial de Gestion del Cambio de Infraestructura. **Cajas de Arquitectura:** E6-04 (Seguridad y Red Perimetral) / E6-01 a E6-08 (Transversal de Infraestructura).

---

## 1. Resumen Ejecutivo y Marco de Gestion del Cambio

El presente documento define la **Plantilla Oficial y Estandarizada de Release Notes de Infraestructura** de la plataforma cafetera **AromaPacifico**, operada conjuntamente con la Federacion Nacional de Cafeteros (FNC) para el piloto 2026 en los departamentos de **Cauca, Huila y Tolima**, tres centros de acopio departamentales y el puerto de exportacion en Buenaventura.

El proposito de este estandar es normalizar de manera determinista, auditable y trazable la planificacion, aprobacion, ejecucion y posible reversion de cualquier modificacion sobre la infraestructura como codigo (IaC en Terraform), incluyendo cambios en **redes hibridas, politicas de firewall perimetral (Security Groups y NACLs), endpoints de ingesta IoT o caminos de comunicacion y misiones de drones**.

### Correspondencia Codigo-Diagrama y Trazabilidad de la Epica 6
En estricto cumplimiento con la gobernanza de la Epica 6, cada cambio de infraestructura debe certificar la correspondencia biunivoca entre el codigo HCL desplegado en el repositorio `iac` y los diagramas oficiales de arquitectura aprobados en el repositorio `planning` (`docs/architecture/diagrams/`):
- **Arquitectura de Seguridad y Firewall:** `seguridad-firewall-iac.drawio` / `seguridad-firewall-iac.svg`.
- **Topologia de Red Hibrida y Transito:** `red-topologia-hibrida.drawio` / `red-topologia-hibrida.svg`.
- **Caminos de Datos y Segmentacion:** `red-data-paths.drawio` / `red-data-paths.svg`.
- **Flujo de Drones y Carga de Misiones:** `carga-b-flujo-drones.drawio` / `carga-b-flujo-drones.svg`.

### Los Seis Campos Obligatorios del Estandar mas el Plan de Terraform
Toda solicitud de liberacion de infraestructura debe documentar obligatoriamente los siete nucleos tecnicos de informacion requeridos por el Comite de Cambios de AromaPacifico:
1. **Que Cambia**: Descripcion de la modificacion en la infraestructura, recursos de AWS/Azure afectados, mapeo al catalogo de firewall (`C01` a `C20`, `N01` a `N16`, o excepciones temporales `T01` a `T03`), reglas PC-IAC aplicadas y correspondencia codigo-diagrama.
2. **Ventana de Despliegue**: Cronograma exacto en horario local de Colombia (COT, UTC-5) y UTC, duracion presupuestada y cumplimiento estricto del congelamiento de cosecha (*Harvest Window Freeze* de 05:00 a 18:00 COT).
3. **Impacto Operativo y en Red/Usuarios**: Evaluacion por perfil (Acopio, Drones, Caficultores, Administradores), blast radius, continuidad del servicio y cumplimiento de los Acuerdos de Nivel de Servicio (SLO de red y latencia).
4. **Aprobacion Formal**: Registro de la compuerta humana colegiada con cuatro roles signatarios validados mediante IAM Identity Center (SSO) y autenticacion multifactor fisica (MFA FIDO2/WebAuthn).
5. **Aviso a la Federacion**: Protocolo institucional de comunicaciones con antelaciones T-72h, T-24h, T-0 y T+15min hacia directivas, comites departamentales y mesas de soporte.
6. **Procedimiento de Vuelta Atras (Rollback)**: Pasos tecnicos deterministas, criterios de aborto cuantitativos en CloudWatch Alarms / VPC Flow Logs y tiempo de recuperacion (RTR) menor a 5 minutos.
7. **Plan de Terraform Asociado**: Inspeccion formal del plan (`terraform plan -out=... -detailed-exitcode`), desglose de recursos (`+`, `~`, `-`), hashes de integridad y adhesion al mandato innegociable de Cero Apply en tiempo de revision.

---

## 2. Estructura Canonica de la Plantilla de Release Notes

A continuacion se presenta la estructura que debe ser diligenciada en su totalidad para cada cambio de infraestructura:

```markdown
# Release Notes de Infraestructura: [Nombre Descriptivo del Cambio]

## Plataforma Cafetera AromaPacifico (Federacion Nacional de Cafeteros 2026)

**Identificador de Release:** REL-INFRA-[ANIO]-[NUMERO_SECUENCIAL]  
**Tipo de Cambio:** [RED / FIREWALL / INGESTA / CAMINO_DEL_DRON / SEGURIDAD]  
**Modulos IaC Afectados:** [`modules/network`, `modules/security`, `modules/function`, `environments/prod`, etc.]  
**Recursos HCL Especificos:** [Lista de nombres de recursos Terraform afectados, ej. `aws_vpc_security_group_ingress_rule.c05`]  
**Fecha Programada de Ejecucion:** [AAAA-MM-DD, HH:MM a HH:MM COT]  
**Responsable del Cambio:** [Nombre y Cargo del Ingeniero DevOps / Arquitecto Cloud]  
**Estado:** [Borrador / En Revision / Aprobado / Ejecutado / Revertido]  
**Cajas de Arquitectura Asociadas:** [E6-01 a E6-08]  
**Historia de Usuario / Issue:** [#[Numero]](URL_AL_ISSUE). **Dependencias:** [#[Numero]](URL_A_DEPENDENCIA)

---

### Campo 1: Que Cambia

#### 1.1 Descripcion Tecnica General del Cambio
[Descripcion precisa de la alteracion en la infraestructura. Detallar si se trata de apertura de puertos, modificacion de rutas en Route Tables o Transit Gateway, actualizacion de Security Groups, adicion de VPC Endpoints o ajuste en politicas IAM.]

#### 1.2 Recursos de Infraestructura Afectados en el Repositorio IaC
Enumerar los recursos de Terraform afectados especificando el archivo HCL y la ruta del modulo:
- **Modulo de Origen:** `[iac/modules/... o iac/environments/...]`
- **Recursos Creados (`+`):** `[Tipo y nombre de recurso HCL, ej. aws_vpc_security_group_ingress_rule.c05]`
- **Recursos Modificados (`~`):** `[Tipo y nombre de recurso HCL, ej. aws_security_group.vpce_s3]`
- **Recursos Destruidos (`-`):** `[Tipo y nombre de recurso HCL, o Ninguno]`

#### 1.3 Mapeo al Catalogo Oficial de Firewall y Politicas de Red
Vincular el cambio con el catalogo oficial de politicas de red (`planning/docs/architecture/red-firewall.md` y `iac/modules/security/`):
- **ID de Regla de Catalogo:** [C01 a C20 / N01 a N16 / T01 a T03]
- **Clave de Contrato (`rule_catalog`):** [ej. `sg_ingress["C05"]`]
- **Tipo de Control:** [SG-IN / SG-OUT / NACL-IN / NACL-OUT / LOCAL / HOST]
- **Recurso Contenedor Padre (`parent_id`):** [ID del Security Group o NACL]
- **Prefijo de Origen Autorizado:** [CIDR /32 o /24 autorizado, sin 0.0.0.0/0 innecesario]
- **Prefijo / Recurso de Destino:** [CIDR o Recurso de destino]
- **Protocolo y Puertos:** [ej. TCP 443 / HTTPS con TLS 1.3]
- **Vigencia del Control:** [Permanente (P) / Temporal (T, con expiracion max. 4h)]

#### 1.4 Correspondencia Codigo-Diagrama
Identificar los diagramas tecnicos oficiales que reflejan este componente:
- **Diagrama Principal:** `[planning/docs/architecture/diagrams/<nombre>.svg]`
- **Fuente Editable:** `[planning/docs/architecture/diagrams/<nombre>.drawio]`
- **Elementos Representados:** [Identificar las cajas y conectores visuales que representan el flujo de datos modificado]

---

### Campo 2: Ventana de Despliegue

#### 2.1 Cronograma de Ejecucion
- **Fecha de Ejecucion:** [AAAA-MM-DD]
- **Hora de Inicio:** [HH:MM COT] ([HH:MM UTC])
- **Hora de Finalizacion:** [HH:MM COT] ([HH:MM UTC])
- **Duracion Presupuestada:** [XX minutos]

#### 2.2 Verificacion de Congelamiento en Cosecha (Harvest Window Freeze)
En AromaPacifico esta terminantemente prohibido ejecutar cambios de infraestructura en produccion entre las **05:00 y las 18:00 (hora local de Colombia, COT)** durante semanas de cosecha cafetera:
- **Estado de Cosecha:** [Activa / Inactiva]
- **Validacion Horaria:** [Confirmar que la ventana esta fuera del rango 05:00 - 18:00 COT]
- **Resultado del Script Automatizado (`iac/.github/scripts/check_harvest_window.py`):**
```text
Timestamp Evaluado: [AAAA-MM-DDTHH:MM:SS-05:00]
Hora Local COT: [HH]
Rango Permitido: [18:01 a 04:59 COT]
Estado: COMPLIANT (Ventana autorizada para ejecucion)
```

---

### Campo 3: Impacto Operativo y en Red/Usuarios

#### 3.1 Evaluacion de Impacto por Perfil de Usuario y Actor
- **Centros de Acopio (Cauca, Huila, Tolima):** [Impacto en conectividad local, estaciones de pesaje y recepcion]
- **Operacion de Drones y Cuadrillas:** [Impacto en carga de misiones, planes de vuelo y sincronizacion de ortofotos]
- **Caficultores:** [Impacto en telemetria de fincas, nodos LoRaWAN y recepcion de alertas]
- **Compradores Internacionales:** [Impacto en el servicio de consulta publica del saco]
- **Administradores de Red:** [Impacto en tuneles IPsec, enlaces BGP y resolvers DNS]

#### 3.2 Radio de Afectacion (Blast Radius) y Continuidad
- **Aislamiento de Red:** [Detallar la subred, VLAN o grupo de seguridad al que se restringe el impacto]
- **Disponibilidad del Servicio:** [Zero-downtime, sin reinicio de interfaces criticas ni reconexion BGP forzada]
- **SLO de Red Comprometidos:**
  - Latencia en Transit Gateway: [p95 <= 25 ms]
  - Tasa de paquetes descartados en firewall: [<= 0.001%]
  - Disponibilidad de tuneles VPN IPsec: [>= 99.95%]

---

### Campo 4: Aprobacion Formal Colegiada

La aprobacion del cambio exige la firma electronica mediante credenciales federadas de IAM Identity Center (SSO) con autenticacion multifactor fisica obligatoria (FIDO2/WebAuthn):

| Rol de Aprobacion | Nombre del Titular | Dependencia / Area | Identificador de Sesion SSO | Estado de Aprobacion |
|---|---|---|---|---|
| **Lider de Operaciones y DevOps Senior** | [Nombre] | DevOps & Infraestructura FNC | `[FNC-SSO-OPS-XXXXX]` | Aprobado con MFA |
| **Arquitecto Cloud y de Seguridad** | [Nombre] | Arquitectura & Ciberseguridad | `[FNC-SSO-SEC-XXXXX]` | Aprobado con MFA |
| **Director de Logistica de Acopio** | [Nombre] | Gerencia Tecnica FNC | `[FNC-SSO-LOG-XXXXX]` | Aprobado con MFA |
| **Oficial de Privacidad y Cumplimiento** | [Nombre] | Juridica FNC (Ley 1581 / RAC 100) | `[FNC-SSO-LEGAL-XXXXX]` | Aprobado con MFA |

---

### Campo 5: Aviso Institucional a la Federacion

Protocolo formal de comunicaciones escalonadas:
- **T-72 Horas:** Comunicado tecnico formal remitido a Comites Departamentales de Cafeteros y Gerencia de Tecnologia.
- **T-24 Horas:** Boletin de confirmacion operativa a coordinadores de acopio y cuadrillas de campo.
- **T-0 (Inicio de Ventana):** Alerta en canal operativo de Microsoft Teams (`#ops-infraestructura`) y notificacion SNS.
- **T+15 Minutos (Post-Ejecucion):** Certificacion de estabilidad de red, telemetria validada y cierre formal de la ventana.

---

### Campo 6: Procedimiento de Vuelta Atras (Rollback)

#### 6.1 Criterios Cuantitativos de Aborto y Activacion de Reversion
Se procedera a la reversion inmediata y automatica si durante la ejecucion o ventana de estabilizacion ocurre:
1. Incremento superior a 5 paquetes descartados/segundo en VPC Flow Logs sobre el recurso modificado.
2. Disparo de alarma de CloudWatch asociada al endpoint o subred afectada.
3. Degradacion de latencia en Transit Gateway superior a 30 ms durante mas de 60 segundos.

#### 6.2 Pasos Tecnicos Deterministas de Reversion
1. **Reversion en Repositorio Git:**
   ```bash
   git revert --no-edit [COMMIT_HASH_DEL_CAMBIO]
   git push origin main
   ```
2. **Despliegue del Plan Inverso via CI/CD:**
   - Ejecutar el pipeline de Terraform sobre el ambiente destino para retirar la regla o configuracion.
3. **Restablecimiento Inmediato en Firewall Local (si aplica):**
   - Comando directo de purga de regla en el equipo perimetral.

#### 6.3 Tiempo Estimado de Recuperacion (RTR)
- **Deteccion:** < 60 segundos mediante metricas de flujo de red.
- **Ejecucion del Rollback:** < 180 segundos mediante pipeline o comando directo.
- **RTR Total Consolidado:** **< 4 minutos**, restituyendo el estado previo sin degradacion residual.

---

### Campo 7: Plan de Terraform Asociado

#### 7.1 Metadatos y Comandos de Generacion
- **Comando de Generacion del Plan:**
  ```bash
  terraform plan -var-file="terraform.tfvars" -out=tfplan-[ID_RELEASE].binary -detailed-exitcode
  ```
- **Checksum SHA-256 del Plan:** `[HASH_SHA256_DEL_BINARIO]`
- **Hash de Commit de Git:** `[HASH_GIT_40_CARACTERES]`
- **Ambiente de Destino:** `[environments/prod / environments/network]`

#### 7.2 Salida Estructurada del Plan de Terraform (Diff HCL)
```terraform
Terraform will perform the following actions:

  # [Recurso modificado o creado]
  + resource "[tipo_de_recurso]" "[nombre_recurso]" {
      + [atributo_1] = "valor_1"
      + [atributo_2] = "valor_2"
    }

Plan: X to add, Y to change, Z to destroy.
```

#### 7.3 Certificacion de Alcance Estricto y Cero Apply
En cumplimiento de la regla de gobierno del proyecto AromaPacifico, **esta terminantemente prohibida la ejecucion manual o no autorizada de `terraform apply`**. El plan de Terraform incluido en este documento constituye la evidencia inmutable y auditable de los cambios aprobados por la compuerta colegiada.
```

---

## 3. Sustentacion FinOps y Analisis Comparativo de Infraestructura

Cada liberacion de infraestructura debe respaldarse mediante un analisis FinOps que compare la solucion adoptada contra alternativas descartadas, verificando el principio de **cero computo esperando trafico o paquetes ociosos**:

### 3.1 Matriz Comparativa Multicriterio de Alternativas de Red y Seguridad

| Criterio de Evaluacion | Alternativa Seleccionada: VPC Interface Endpoints + Reglas SG/NACL Nativas | Alternativa Descartada A: Firewall Centralizado Dedicado (AWS Network Firewall) | Alternativa Descartada B: Gateway NAT Publico con Sincronizacion por Internet |
|---|---|---|---|
| **Modelo de Facturacion** | Pay-per-Usage (Horas de endpoint + GB transferido) | Cargo fijo mensual continuo por AZ + trafico | Cargo fijo por NAT Gateway + costo de datos de salida |
| **Costo en Reposo / Valle** | **$0,00 USD / mes** (en subredes sin provision fija) | $577,00 USD / mes ($0,395/h por endpoint de firewall) | $32,40 USD / mes ($0,045/h fijo por NAT Gateway) |
| **Costo en Pico de Cosecha** | $2,10 USD / mes (segun volumen transferido) | $612,50 USD / mes | $48,90 USD / mes |
| **Aislamiento de Red** | Totalmente privado a traves de AWS PrivateLink y VPN | Privado con punto unico de inspeccion centralizado | Riesgo de exposicion en internet publico |
| **Tiempo de Vuelta Atras** | Inmediato (< 3 minutos) mediante HCL declarativo | Lento (3-8 minutos por propagacion de politicas) | Moderado (requiere reconfiguracion de tablas de ruta) |
| **Veredicto FinOps** | **SELECCIONADA: Ahorro masivo en reposo y zero-egress publico** | **RECHAZADA: Sobrecosto inaceptable de $6.924,00 USD / ano** | **RECHAZADA: Riesgo de seguridad y costo fijo innecesario** |

### 3.2 Calculo Detallado del Costo Evitado
$$\text{Costo Evitado Mensual} = \text{Costo Alternativa Descartada A} - \text{Costo Solucion Adoptada} = \$577,00 - \$0,00 = \$577,00 \text{ USD / mes}$$
$$\text{Costo Evitado Anual} = \$577,00 \times 12 = \$6.924,00 \text{ USD / ano}$$

### 3.3 Politica de 7 Etiquetas Obligatorias (Tag Policy)
Todos los recursos de infraestructura declarados en el release deben incluir o heredar las 7 etiquetas corporativas:
- `FincaID`: `GLOBAL` (o el identificador predial especifico en nodos de finca).
- `DronID`: `NO-APLICA` (o el identificador del dron autorizado, ej. `DRON-CAUCA-01`).
- `AcopioID`: `MULTICENTRO` (o `ACOPIO-CAUCA`, `ACOPIO-HUILA`, `ACOPIO-TOLIMA`).
- `ViajeID`: `NO-APLICA`.
- `Ambiente`: `produccion` (o `desarrollo` / `pruebas`).
- `Propietario`: `devops-fnc`.
- `Proyecto`: `AromaPacifico`.

### 3.4 Invariante de Presupuestos (AWS Budgets)
Los presupuestos configurados en AWS Budgets emiten alertas a traves de Amazon SNS cuando el consumo real alcanza el **80% del presupuesto proyectado**. Bajo ninguna circunstancia se configuran acciones automaticas de terminacion o corte de interfaces de red, VPC Endpoints o túneles VPN.

---

## 4. Marco Juridico y Soberania de Datos (Ley 1581 de 2012 / RAC 100)

1. **Soberania de Datos y Trafico Hibrido:** Las modificaciones en el firewall y la red deben garantizar que el trafico entre los centros de acopio y la nube de AWS se canalice exclusivamente a traves de tuneles IPsec cifrados (IKEv2, AES-256-GCM) y VPC Endpoints privados, sin exposicion de paquetes a la red publica de internet.
2. **Proteccion de Datos Personales (Ley 1581):** Ninguna regla de red o configuracion de enrutamiento puede habilitar accesos no autorizados a bases de datos que contengan nombres, cedulas cafeteras o coordenadas intraprediales privadas de caficultores.
3. **Reglamentacion Aeronautica (RAC 100 de la Aerocivil):** Las misiones de vuelo y ortomosaicos transferidos a traves de endpoints de drones corresponden a inspeccion agronomica autorizada con geocercas predefinidas y altitudes de vuelo seguras.

---

## 5. Lista de Chequeo de Conformidad (Checklist de Aprobacion)

Antes de presentar el release note de infraestructura ante el comite de cambios, el responsable debe verificar:
- [ ] La plantilla incluye los seis campos obligatorios y la seccion del plan de Terraform asociado.
- [ ] Los recursos HCL modificados existen y estan validados en el repositorio `iac`.
- [ ] Se verifica la correspondencia exacta entre las reglas de red y los diagramas de arquitectura en `planning/docs/architecture/diagrams/`.
- [ ] La ventana de ejecucion respeta estrictamente el congelamiento de cosecha (05:00 a 18:00 COT).
- [ ] Se incluye la compuerta humana colegiada con los 4 roles y autenticacion MFA.
- [ ] Se presenta la matriz comparativa FinOps con al menos 2 alternativas y el calculo matematico del costo evitado.
- [ ] Se cumple estrictamente el principio de Cero Emojis y redaccion tecnica profesional en espanol.
