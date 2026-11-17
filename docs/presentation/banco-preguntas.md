# Banco de Preguntas de Sustentación

## Plataforma Cafetera AromaPacífico (Federación Nacional de Cafeteros 2026)

**Historia:** #39. **Responsable:** Equipo Arquitectura & DevOps FNC 2026. **Fecha:** 17 de noviembre de 2026.  
**Estado:** Consolidado para sustentación. **Fase:** Fase 6 - Sustentación.

---

## 1. Preguntas Críticas del Arquitecto de la Federación y Respuestas Sustentadas

### P1. ¿Cómo garantizan la conectividad de las fincas sin señal celular sin instalar radiobases ni hacer visitas semanales?
- **Respuesta:** Las 60 fincas sin cobertura LTE-M/NB-IoT validadas se atienden con una arquitectura híbrida: **48 fincas (80 %)** se conectan vía LoRaWAN hacia 10 gateways solares compartidos ubicados en puntos con señal celular (vía principal o cabecera), y las **12 fincas restantes (20 %)** sin línea de vista utilizan satélite **Iridium SBD**. Todo nodo escribe primero en su buffer flash (retención máxima de 24 h) y solo borra tras recibir ACK de persistencia en DynamoDB.

### P2. ¿Por qué eligieron el modo combinado de drones y quién opera y autoriza la fumigación?
- **Respuesta:** Se combina **agricultura de áreas** (delimitación inicial del lote con zonas No-Fly y estimación anual de cosecha) con **agricultura de precisión** (confirmación de alerta en el foco, fumigación focalizada y verificación post-vuelo). El vuelo lo ejecutan **3 cuadrillas contratadas** (una por acopio) bajo **RAC 100 de Aerocivil**, evitando USD 105.486 de CapEx y USD 195.353/año en nómina fija. **Ninguna función automática autoriza fumigar:** únicamente el agrónomo FNC autenticado en Cognito con MFA firma la orden.

### P3. ¿Por qué el código de la Épica 6 cabe en 100 horas y 2 semanas?
- **Respuesta:** Porque el alcance está acotado al patrón replicable: bootstrap S3/KMS (`6 h`), módulo `network` (`22 h`), módulo `security` (`18 h`), pipeline CI/CD OIDC (`10 h`), módulos `ingest` y una `farm` patrón (`24 h`), módulo `function` únicamente para confirmación del foco (`16 h`) y evidencia de `plan` (`4 h`) = **100 horas exactas**. No se instancian las 200 fincas ni los 3 centros ni se codifican las otras 3 funciones ni la consulta pública.

### P4. ¿Cómo cumplen la Ley 1581 de 2012 si AWS `us-east-1` está fuera de Colombia?
- **Respuesta:** Bajo el **Artículo 26 de la Ley 1581 de 2012** (autorización expresa en onboarding y contrato DPA con AWS, manteniendo las llaves KMS bajo control de FNC). Además, la cédula del caficultor y las rutas intraprediales privadas **no salen a vistas públicas**: el código del saco (`SACO-AAAA-DEP-HASH8`) se tokeniza irreversiblemente con **HMAC-SHA-256** y la consulta pública lee únicamente la tabla proyectada `sacos_publicos`. Las fotos de drones pasan por **Rekognition `DetectFaces/DetectLabels`** y si detectan personas se aíslan en cuarentena WORM sin enviarse a Bedrock.

### P5. ¿Cuáles son las tres decisiones FinOps que más gasto evitan?
| Decisión FinOps | Alternativa Descartada | Costo Evitado |
| --- | --- | --- |
| **1. Contratación de servicio de drones por acopio** | Cuadrillas propias con compra de aeronaves y camionetas | **USD 195.353/año** OpEx + **USD 105.486** CapEx |
| **2. LoRaWAN compartido (48 fincas) + SBD (12 fincas)** | Iridium SBD en las 60 fincas sin cobertura | **USD 84.552/año** conectividad + **USD 14.104** hardware |
| **3. Retiro de AWS Network Firewall y Outbound Resolver** | Mantener Network Firewall + Resolver de salida en piloto | **USD 9.297/año** (`USD 774,78/mes`) |
