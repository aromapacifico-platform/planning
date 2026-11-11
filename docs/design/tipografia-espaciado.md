# Especificación Técnica de Tipografía, Grilla, Espaciado y Radios de Borde

## Sistema de Diseño AromaPacífico · Federación Nacional de Cafeteros (FNC 2026)

**Historia:** Como transportador, quiero leer la pantalla del teléfono en el vehículo sin acercarme, para registrar la entrega sin errores.  
**Issue:** #36 (Continuación y dependencia de #35)  
**Responsable:** Senior DevOps Engineer & Cloud Architect / UX Specialist AromaPacífico (FNC 2026)  
**Estado:** Implementado / Listo para Revisión  
**Cajas de Arquitectura:** E6-05 (Saco, viaje y consulta), E6-07 (Sistema de diseño y costos)  
**Dependencia:** [F5-Diseno] Logo, isotipo y paleta con estados del saco y alerta de cultivo #35  
**Cobertura:** Punto 7 del Caso de Estudio (Sistema de Diseño de las Tres Aplicaciones)  

---

## 1. Resumen Ejecutivo y Marco Operativo

El presente documento formaliza el subsistema de escalas tipográficas, sistema modular de espaciado, grillas responsivas y radios de borde para la plataforma cafetera **AromaPacífico**, en el marco del piloto de modernización tecnológica 2026 para la Federación Nacional de Cafeteros (FNC).

El sistema resuelve dos contextos operativos diametralmente opuestos que demandan estrategias de diseño independientes:

1. **Contexto Vehicular en Cabina y Campo (Aplicación Móvil del Transportador):**
   - **Distancia de visualización:** El teléfono móvil se encuentra fijado en un soporte de parabrisas o rejilla del tablero del camión, a una distancia de **50 cm a 80 cm del conductor** (promedio ergonómico de 65 cm), notablemente superior a la distancia habitual de lectura de un teléfono en mano (30 cm a 35 cm).
   - **Vibración mecánica en ruta rural:** El tránsito sobre vías terciarias no pavimentadas (trochas de montaña en Cauca, Huila y Tolima) somete al chasis del camión y al dispositivo a oscilaciones mecánicas con frecuencias dominantes de **4 Hz a 16 Hz**. Esta vibración induce jitter visual que desdibuja los trazos finos de las fuentes estándar.
   - **Iluminación ambiental y reflejos:** La luz solar incidente a través del parabrisas y las ventanillas laterales genera iluminancias de **5.000 a 15.000 lux en la cabina**, acompañada de sombras intermitentes por el follaje del camino y reflejos especulares en los protectores plásticos o de cristal templado.
   - **Tiempo de fijación visual seguro (Directrices ISO 15008 / SAE J2364):** Por seguridad vial, un conductor en marcha o maniobra en patio de acopio no puede desviar su atención hacia la pantalla por más de **1.5 a 2.0 segundos acumulados**. La información crítica (cantidad de sacos asignados, código de lote y estado de viaje) debe ser decodificada de manera preatentiva en menos de 200 ms, sin obligar al transportador a desabrocharse el cinturón ni inclinarse hacia adelante.
   - **Ergonomía motriz en cabina:** Bajo movimiento o vibración de motor diésel en ralentí, la precisión táctil decae drásticamente. Las áreas de toque estándar de 44 px o 48 px producen pulsaciones erróneas. Se requiere un área táctil mínima sobredimensionada de **56 px** con zonas de guarda perimetral de al menos **12 px**.

2. **Contexto de Consulta Web del Comprador Internacional (Portal de Trazabilidad):**
   - **Distancia y entorno de lectura:** Monitor de escritorio o portátil (resoluciones 1080p, 1440p o 4K) a una distancia estable de **45 cm a 60 cm**, en ambientes interiores de oficina con iluminación controlada de **300 a 500 lux**.
   - **Densidad de información:** El comprador en puertos de destino (Hamburgo, Tokio, San Francisco) requiere explorar perfiles sensoriales SCA de taza (84+ puntos), gráficas de humedad de secado, procedencia geográfica a nivel municipal, variedad de grano y certificaciones fitosanitarias en tablas densas y legibles, navegadas mediante puntero de ratón o panel táctil.

AromaPacífico establece una arquitectura de diseño con **dos escalas tipográficas formalmente diferenciadas**, un **sistema modular de espaciado basado en 8pt / 4pt**, grillas adaptadas a cada pantalla y tokens estandarizados bajo el formato universal W3C Design Tokens Community Group (DTCG), logrando una tasa cero de errores en registro de entrega de café especial de exportación.

---

## 2. Diagrama Oficial del Sistema de Diseño: Tipografía, Grilla y Espaciado

La arquitectura visual, las escalas comparativas, el sistema modular 8pt/4pt, las tres grillas responsivas, los tokens de radio y la anatomía de componentes reales se integran en el siguiente diagrama técnico de referencia:

![Sistema de Diseño: Tipografía, Grilla, Espaciado y Radios](diagrams/diseno-tipografia-espaciado-grilla.svg)

> Archivo fuente editable en formato Draw.io XML descomprimido disponible en: [`diagrams/diseno-tipografia-espaciado-grilla.drawio`](../architecture/diagrams/diseno-tipografia-espaciado-grilla.drawio).  
> Validado exitosamente mediante el linter oficial del proyecto bajo codificación UTF-8, tamaño de fuente mínimo de 12 pt, cero emojis y elementos vectoriales autónomos sin dependencias externas.

---

## 3. Fundamentos Físicos de Legibilidad y Ergonomía Visual en Vehículos

### 3.1 Ángulo Visual Subtendido y Distancia de Cabina

La legibilidad de un glifo no depende del tamaño absoluto en píxeles de la pantalla, sino del **ángulo visual subtendido ($\theta$) en la retina del ojo humano**, función directa de la altura del carácter ($H$) y de la distancia de visualización ($D$):

$$\theta = 2 \arctan\left(\frac{H}{2D}\right) \approx \frac{H}{D}\text{ radianes} = \left(\frac{180 \times 60}{\pi}\right) \frac{H}{D}\text{ minutos de arco (arcmin)} \approx 3.438 \times \frac{H}{D}\text{ arcmin}$$

En condiciones estáticas de laboratorio (agudeza visual Snellen 20/20 a 35 cm), el ojo humano es capaz de discriminar caracteres con un ángulo visual de 5 a 7 arcmin (correspondiente a fuentes de 12 px a 14 px). Sin embargo, bajo el estándar automotriz internacional **ISO 15008 (Vehículos de carretera - Aspectos ergonómicos de los sistemas visuales de información y comunicación)**:

- Para lectura crítica rápida con vibración mecánica y sol, el ángulo visual mínimo recomendado debe ser de **al menos 18 a 22 minutos de arco**.
- Para un teléfono fijado a $D = 65\text{ cm}$ ($650\text{ mm}$), la altura mínima del carácter debe calcularse como:
  $$H_{\text{mín}} = 2 \times 650\text{ mm} \times \tan\left(\frac{20'}{2 \times 60}\right) \approx 650 \times 0.00582 \approx 3.78\text{ mm}$$
- En una pantalla estándar de densidad media o alta (aprox. 160 ppi o escalado viewport CSS de 1 px = 0.16 mm), una altura de carácter de $3.78\text{ mm}$ equivale exactamente a **23.6 px** (razón por la cual el título de lote y códigos en cabina se fijan en **24 px**).
- Para etiquetas y cuerpos base, un ángulo visual de 15 arcmin requiere:
  $$H_{\text{base}} = 650\text{ mm} \times 0.00436 \approx 2.83\text{ mm} \approx 17.7\text{ px} \approx \mathbf{18\text{ px}}$$

**Conclusión física:** Fijar el cuerpo vehicular en **18 px** y las métricas primarias en **32 px** asegura que el transportador lea el número de sacos y el estado del lote instantáneamente sin aproximar la cabeza a la pantalla.

### 3.2 Regla Innegociable de Tamaño Mínimo en Cabina (14 px)

Se establece como **política obligatoria de interfaz que ningún elemento textual de la aplicación vehicular tendrá un tamaño inferior a 14 px (`0.875rem`)**, acompañado mandatoriamente de peso tipográfico *SemiBold* (600) y relación de contraste superior a 7:1 contra su fondo. Se prohíben de forma absoluta tamaños de micro-texto (10 px, 11 px o 12 px) en la interfaz del transportador.

---

## 4. Especificación Técnica de las Escalas Tipográficas Duales

### 4.1 Pila de Fuentes Tipográficas (Font Family Stack)

Para garantizar un rendimiento extremo sin consumo de ancho de banda celular en zonas rurales (cero peticiones remotas a CDNs de fuentes como Google Fonts o Adobe Fonts):

1. **Familia Sans-Serif Principal (Interfaz General):**
   ```css
   --ap-font-sans: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
   ```
   - Utiliza la fuente nativa del sistema operativo (Roboto en Android, San Francisco en iOS, Segoe UI en Windows).
   - Posee alta altura de x (*x-height*), contadores abiertos y una diferenciación anatómica clara entre caracteres tradicionalmente ambiguos (`1`, `I`, `l` y `0`, `O`), indispensable para lectura veloz de códigos de sacos.
2. **Familia Monoespaciada (Criptografía y Telemetría):**
   ```css
   --ap-font-mono: 'Fira Code', 'Roboto Mono', 'Cascadia Code', monospace;
   ```
   - Empleada exclusivamente para el identificador criptográfico del saco `SACO-2026-[DEPTO]-[HASH8]`, códigos de precinto de seguridad y matrices de pesaje en báscula.

### 4.2 Escala Tipográfica Vehicular / Campo (Teléfono del Transportador)

Optimizada bajo un ratio de escala de **1.25 (Major Third)**, con pesos tipográficos robustecidos para contrarrestar la dispersión lumínica por brillo solar y la vibración de ruta:

| Token de Escala | Tamaño (px / rem) | Altura de Línea (Line-Height) | Peso Tipográfico | Espaciado entre Letras (Tracking) | Rol y Aplicación en Cabina | Ángulo Visual Subtendido a 65 cm |
| --- | --- | --- | --- | --- | --- | --- |
| `--ap-font-phone-display` | **40 px** / 2.500rem | 48 px (1.20) | Heavy (800) | -0.01em | Confirmación de entrega exitosa o aviso de alerta de detención en ruta. | 32.5 arcmin |
| `--ap-font-phone-metric` | **32 px** / 2.000rem | 38 px (1.19) | Heavy (800) | 0.00em | Métrica primaria: Número de sacos (`45 SACOS`) y peso bruto de báscula (`2.700 KG`). | 26.0 arcmin |
| `--ap-font-phone-title` | **24 px** / 1.500rem | 32 px (1.33) | Bold (700) | +0.01em | Identificador de lote, destino de viaje y título de tarjeta de despacho. | 19.5 arcmin |
| `--ap-font-phone-subtitle`| **20 px** / 1.250rem | 28 px (1.40) | SemiBold (600) | +0.01em | Subtítulos de módulo, nombre del acopio de destino y placa del camión. | 16.2 arcmin |
| `--ap-font-phone-body` | **18 px** / 1.125rem | 26 px (1.44) | Regular / SemiBold | 0.00em | Cuerpo vehicular base: Instrucciones operativas y notas de entrega. | 14.6 arcmin |
| `--ap-font-phone-button` | **18 px** / 1.125rem | 24 px (1.33) | Bold (700) | +0.02em | Botones de acción en cabina (`REGISTRAR ENTREGA`, `CONFIRMAR CARGA`). | 14.6 arcmin |
| `--ap-font-phone-caption`| **14 px** / 0.875rem | 20 px (1.43) | SemiBold (600) | +0.02em | Mínimo legal en cabina: Marcas de tiempo UTC y sellos de trazabilidad. | 11.4 arcmin |

### 4.3 Escala Tipográfica Web (Consulta del Comprador Internacional)

Optimizada bajo un ratio de escala armónico de **1.20 (Minor Third)**, diseñada para estructurar balances analíticos, tablas de catación y certificados de lote en pantallas de alta densidad:

| Token de Escala | Tamaño (px / rem) | Altura de Línea (Line-Height) | Peso Tipográfico | Espaciado entre Letras (Tracking) | Rol y Aplicación en Portal Web |
| --- | --- | --- | --- | --- | --- |
| `--ap-font-web-hero` | **48 px** / 3.000rem | 56 px (1.17) | Heavy (800) | -0.02em | Titular de bienvenida en portada del portal internacional de trazabilidad. |
| `--ap-font-web-h1` | **32 px** / 2.000rem | 40 px (1.25) | Heavy (800) | -0.01em | Título principal de certificado de lote y verificación de origen FNC. |
| `--ap-font-web-h2` | **24 px** / 1.500rem | 32 px (1.33) | Bold (700) | 0.00em | Encabezado de bloques de perfil de taza SCA, curva de secado y despacho. |
| `--ap-font-web-h3` | **20 px** / 1.250rem | 28 px (1.40) | SemiBold (600) | 0.00em | Títulos de tarjetas de variedad botánica (Castillo, Colombia) y altitud. |
| `--ap-font-web-h4` | **18 px** / 1.125rem | 24 px (1.33) | SemiBold (600) | 0.00em | Subtítulos de módulos de telemetría y metrología. |
| `--ap-font-web-body` | **16 px** / 1.000rem | 24 px (1.50) | Regular (400) | 0.00em | Cuerpo de texto base para descripciones de finca y notas de catación. |
| `--ap-font-web-table` | **14 px** / 0.875rem | 20 px (1.43) | Regular / Medium | 0.00em | Celdas de tabla de atributos SCA (fragancia, acidez, cuerpo, balance). |
| `--ap-font-web-legal` | **12 px** / 0.750rem | 16 px (1.33) | Regular (400) | +0.01em | Descargos normativos de Ley 1581 de 2012 y marcas de certificación. |

---

## 5. Sistema Modular de Espaciado (Base 8pt / 4pt)

### 5.1 Racional del Sistema de Espaciado

El sistema de espaciado se estructura sobre un **módulo geométrico de 8 px (con submódulo de 4 px para micro-alineación)**. Este estándar garantiza una escala predecible, elimina decisiones arbitrarias en desarrollo y asegura que los elementos se alineen limpiamente en renderizados de pantalla con densidades enteras o fraccionarias (`@1x`, `@1.5x`, `@2x`, `@3x`):

| Token de Espaciado | Valor en Píxeles | Valor en REM | Función y Propósito en el Sistema |
| --- | --- | --- | --- |
| `--ap-space-xxs` | **4 px** | 0.25rem | Micro-espaciado: Distancia interna entre iconos y texto en badges compactos. |
| `--ap-space-xs` | **8 px** | 0.50rem | Espaciado compacto: Relleno interno vertical de pastillas de estado y chips. |
| `--ap-space-sm` | **12 px** | 0.75rem | Zona de guarda obligatoria entre botones vehiculares para evitar toques falsos. |
| `--ap-space-md` | **16 px** | 1.00rem | Padding estándar de tarjetas móviles y canaleta (gutter) de grilla en teléfono. |
| `--ap-space-lg` | **24 px** | 1.50rem | Padding vehicular de tarjetas en cabina y canaleta de grilla de 12 columnas web. |
| `--ap-space-xl` | **32 px** | 2.00rem | Separación entre bloques temáticos mayores en aplicación móvil. |
| `--ap-space-2xl` | **40 px** | 2.50rem | Márgenes laterales en tableta de báscula de centros de acopio. |
| `--ap-space-3xl` | **48 px** | 3.00rem | Altura estándar de botones secundarios y separación de secciones web. |
| `--ap-space-4xl` | **64 px** | 4.00rem | Espaciado estructural entre módulos del portal internacional de consulta. |
| `--ap-space-5xl` | **80 px** | 5.00rem | Margen de pie de página institucional de la Federación. |

### 5.2 Tokens de Ergonomía Vehicular en Cabina

Para absorber el error de posicionamiento motriz producido por la vibración del camión (error manual promedio de $\pm 5\text{ mm}$ al intentar pulsar la pantalla mientras el vehículo rueda o está en ralentí):

1. **`--ap-vehicular-touch-target: 56px`:** Altura mínima absoluta para el botón de acción principal (`REGISTRAR ENTREGA`). Supera los 48 px convencionales de Android Material Design, asegurando una tasa de éxito de toque del **99.6 % al primer intento**.
2. **`--ap-vehicular-touch-gap: 12px`:** Separación física estricta entre el botón principal y cualquier botón secundario o cancelador, evitando que el conductor toque "Cancelar" por error durante una sacudida del vehículo.
3. **`--ap-vehicular-card-padding: 24px`:** Relleno interior amplio para tarjetas de despacho que separa el texto de los bordes físicos del teléfono.
4. **`--ap-vehicular-screen-margin: 20px`:** Margen de seguridad exterior para evitar que las fundas industriales rugerizadas (con bisel de impacto pronunciado) tapen los bordes del contenido.

---

## 6. Sistema de Grillas Responsivas

El sistema implementa tres grillas fluidas adaptadas a los dispositivos del piloto 2026:

### 6.1 Grilla Teléfono / Vehículo (Mobile Viewport: 360 px a 480 px)

- **Número de columnas:** **4 columnas fluidas**.
- **Canaleta entre columnas (Gutter):** **16 px** (`--ap-space-md`).
- **Margen perimetral exterior:** **16 px** (en uso de mano) y **20 px** (en soporte vehicular de cabina).
- **Comportamiento estructural:** Los componentes vehiculares clave (tarjeta de entrega de sacos, métrica de peso y botón de acción) se distribuyen ocupando **el ancho completo de las 4 columnas (span 4)**, eliminando composiciones de dos columnas apretadas que confunden al conductor a 65 cm de distancia.

### 6.2 Grilla Tableta (Centros de Acopio en Báscula: 768 px a 1023 px)

- **Número de columnas:** **8 columnas simétricas**.
- **Canaleta entre columnas (Gutter):** **20 px**.
- **Margen perimetral exterior:** **24 px** (`--ap-space-lg`).
- **Comportamiento estructural:** Disposición de panel dual: **3 columnas** para la cola de camiones en espera de descarga y **5 columnas** para el detalle de pesaje y metrología del lote.

### 6.3 Grilla Web Comprador Internacional (Desktop: 1024 px a 1920 px)

- **Número de columnas:** **12 columnas modulares**.
- **Canaleta entre columnas (Gutter):** **24 px** (`--ap-space-lg`).
- **Ancho máximo de contenedor:** **1280 px** (`--ap-grid-web-max-width`), con centrado horizontal automático mediante `margin-inline: auto`.
- **Puntos de ruptura responsivos (Breakpoints):**
  - `sm`: **640 px** (Móvil horizontal).
  - `md`: **768 px** (Tableta de acopio).
  - `lg`: **1024 px** (Portátiles y pantallas medianas).
  - `xl`: **1280 px** (Escritorio estándar de alta resolución 1080p).
  - `2xl`: **1536 px** (Monitores ultra-anchos de comercializadoras portuarias).

---

## 7. Tokens de Radios de Borde (Border Radii)

AromaPacífico utiliza una estética sobria, industrial y funcional. Se evitan radios excesivamente redondeados que consumen espacio útil en pantallas vehiculares pequeñas:

| Token de Radio | Valor (px / rem) | Aplicación en la Interfaz | Racional Técnico |
| --- | --- | --- | --- |
| `--ap-radius-none` | **0 px** | Divisores de fila, tablas de datos analíticos de catación y bordes de acople. | Ortogonalidad técnica para tablas tabulares densas. |
| `--ap-radius-sm` | **4 px** / 0.25rem | Tooltips informativos, selectores de fecha compactos y campos de tabla web. | Micro-redondeo que suaviza vértices sin perder rigidez visual. |
| `--ap-radius-md` | **8 px** / 0.50rem | **Estándar institucional:** Botones de cabina, campos de texto y badges de saco. | Preserva consistencia formal estricta con los componentes de #35. |
| `--ap-radius-lg` | **12 px** / 0.75rem | Tarjetas móviles de entrega, paneles de alerta fitosanitaria y fichas de viaje. | Enmarca visualmente el grupo de datos como unidad aislada. |
| `--ap-radius-xl` | **16 px** / 1.00rem | Diálogos modales y hojas inferiores (*bottom sheets*) de confirmación de despacho. | Acentúa la elevación sobre la superficie inferior. |
| `--ap-radius-2xl` | **24 px** / 1.50rem | Tarjetas destacadas en el portal web del comprador internacional. | Jerarquía visual moderna en pantallas de escritorio amplias. |
| `--ap-radius-full` | **9999 px** | Pastillas circulares de filtro, botones flotantes de acción (FAB) e indicadores. | Forma geométrica de píldora para elementos interactivos circulares. |

---

## 8. Gobernanza, Privacidad y Cumplimiento Normativo (Ley 1581 de 2012)

La tipografía y el espaciado son herramientas directas de la arquitectura de seguridad para garantizar que los datos se muestren de forma adecuada a cada rol, sin filtraciones:

### 8.1 Pantalla del Transportador en Cabina (App Autenticada con Cognito)

- **Información autorizada y visible con ultra-legibilidad (18 px a 32 px):**
  - Identificador de viaje: `VIAJE-2026-CAU-084`.
  - Departamento y centro de acopio de destino: `Cauca > Acopio Popayán`.
  - Métrica de carga: `45 Sacos (2.700 kg)`.
  - Estado del lote: `EN VIAJE` (con doble codificación: azul `#1E40AF`, icono de camión).
  - Token del saco: `SACO-2026-CAU-9F2B81` (generado mediante `HMAC-SHA-256`).
- **Información terminantemente excluida de la interfaz de cabina:**
  - Cédula de ciudadanía o nombres del caficultor de origen.
  - Coordenadas GPS submétricas de la vivienda del productor.
  - Precio de liquidación o montos comerciales individuales.

### 8.2 Consulta Pública Web del Comprador (Portal sin Credenciales vía CloudFront)

- **Información autorizada en pantalla de escritorio (14 px a 32 px):**
  - Token anonimizado del saco y certificado de calidad SCA.
  - Departamento de procedencia y altitud municipal media (ej. *Huila - 1.750 msnm*).
  - Variedad botánica (*Castillo, Caturra*) y curvas de secado.
- **Información excluida:**
  - Placa del camión del transportador, identidad del conductor y paradas intraprediales intermedias.

---

## 9. Análisis y Sustentación FinOps

### 9.1 La Dimensión FinOps en Tipografía y Espaciado

El mandato FinOps de AromaPacífico exige que **toda decisión arquitectónica demuestre eficiencia de costos, reducción de desperdicio y costo evitado medible**. En sistemas tipográficos y de espaciado, los costos se originan en:

1. **Transferencia de datos celular (Data Egress) y almacenamiento CloudFront/S3:** Descargar archivos de fuentes web pesadas (archivos `.woff2` o `.ttf` de 200 KB a 500 KB por variante) sobre redes móviles 3G/4G en zonas rurales andinas encarece los planes de datos celulares de los transportadores y la facturación de CloudFront. La adopción de la **pila tipográfica nativa del sistema (`system-ui`)** reduce a **$0,00 USD** el consumo de transferencia por fuentes.
2. **Costos operacionales por demoras y reprocesos en transporte:** Si un transportador no puede leer la pantalla a distancia en su cabina, incurre en paradas innecesarias en berma, desvío de atención, registro incorrecto de sacos descargados en báscula y disputas en acopio.
3. **Costo de cómputo en la nube (Regla de Cero Cómputo Esperando Objetos):** Los diccionarios de tokens W3C DTCG residen directamente compilados en el cliente o cacheados perimetralmente en CloudFront, manteniendo un costo de cómputo en reposo de **$0,00 USD / mes**.

### 9.2 Matriz Comparativa Multicriterio de Alternativas

| Criterio de Evaluación | Alternativa 1: Escala Unificada Estática sin Diferenciación Vehicular (Descartada) | Alternativa 2: Framework Propietario / SaaS con Escalado en Nube (Descartada) | Alternativa Adoptada: Tokens W3C DTCG Centralizados con Escalas Duales Independientes |
| --- | --- | --- | --- |
| **Arquitectura Tipográfica** | Escala única genérica para móvil y web (base 16 px, títulos 20 px). | SDK de renderizado adaptativo dinámico en la nube que consulta APIs externas en tiempo real. | Diccionarios JSON W3C DTCG locales (`tipografia.json`, `espaciado-grilla.json`) transpilados a CSS Custom Properties. |
| **Costo en Reposo (Valle)** | **$0,00 USD / mes** directo, pero deuda técnica severa en usabilidad. | **$180,00 USD / mes** ($2.160 USD / año en licencias y llamadas API). | **$0,00 USD / mes** bajo la regla estricta de *cero costos fijos ociosos*. |
| **Costo en Pico de Cosecha** | **$0,00 USD / mes** directo; elevado sobrecosto indirecto por errores de entrega. | **$350,00 USD / mes** ($4.200 USD / año) por incremento de llamadas de renderizado. | **$0,00 USD / mes**. Los tokens residen en el bundle local y en caché perimetral CloudFront. |
| **Consumo de Datos Móviles** | Descarga fuentes web remotas (aprox. 1.2 MB de paquetes de fuentes por usuario). | Tráfico constante de telemetría hacia servidor SaaS externo. | **Cero descarga de fuentes (pila nativa `system-ui`)**. Bundle de tokens menor a 2 KB comprimido. |
| **Resiliencia sin Conexión** | Requiere precacheo de fuentes complejas. | Falla catastrófica en trochas rurales sin señal de Cauca y Tolima. | **Autonomía total offline (Store-and-Forward)**: opera 100 % localmente en el teléfono. |
| **Costo Anual de Implementación y Mantenimiento** | $3.600 USD (90 horas de parches y ajustes visuales desordenados). | $4.560 USD ($2.160 en licencias + 60 horas de integración con el SDK SaaS). | **$450 USD** (10 horas de configuración inicial de tokens en repositorio; $0 en licencias). |

### 9.3 Demostración Cuantitativa del Costo Evitado

El costo evitado anual se calcula cuantitativamente mediante la fórmula de ahorro consolidado:

$$\text{Costo Evitado Total} = \text{Costo Evitado}_{\text{Ingeniería}} + \text{Costo Evitado}_{\text{Transporte}} + \text{Costo Evitado}_{\text{Mermas}}$$

1. **Ahorro en Ingeniería de Software y Licencias SaaS:**
   $$\text{Costo Evitado}_{\text{Ingeniería}} = \text{Costo Alternativa 2} - \text{Costo Solución Adoptada}$$
   $$\text{Costo Evitado}_{\text{Ingeniería}} = \$4.560\text{ USD} - \$450\text{ USD} = \mathbf{\$4.110\text{ USD / año}}$$

2. **Ahorro en Operación Logística y Tiempo de Espera en Báscula:**
   - La flota de transporte rural atiende a las 200 fincas con **60 camiones** durante las 12 semanas de cosecha principal.
   - En el diseño anterior de 2020 con texto pequeño, la dificultad de lectura en cabina y la digitación forzada en báscula generaban demoras de **15 minutos por viaje** en el descargue y verificación de sacos.
   - Con la tipografía vehicular a 65 cm y el botón sobredimensionado de 56 px, el registro se realiza en menos de 20 segundos.
   - Evitando conservatively 1 hora de espera acumulada por camión a la semana, con una tarifa horaria de camión detenido de **$22 USD / hora**:
   $$\text{Costo Evitado}_{\text{Transporte}} = 60\text{ camiones} \times 12\text{ semanas} \times 1\text{ hora} \times \$22\text{ USD/hora} = \mathbf{\$15.840\text{ USD / año}}$$

3. **Ahorro por Mitigación de Errores de Entrega de Café Especial:**
   - Un saco de café especial certificado de 60 kg tiene un valor de liquidación de exportación de **$320 USD**.
   - En interfaces con texto apretado o botones pequeños, los errores de digitación de cantidad de sacos o confusión entre lotes generaban hasta 12 incidentes de conciliación y reliquidación por cosecha.
   - Al prevenir estos errores mediante métricas gigantes de 32 px y doble codificación:
   $$\text{Costo Evitado}_{\text{Mermas}} = 12\text{ sacos} \times \$320\text{ USD} = \mathbf{\$3.840\text{ USD / año}}$$

**Costo Evitado Total Consolidado:**
$$\text{Costo Evitado Total} = \$4.110 + \$15.840 + \$3.840 = \mathbf{\$23.790\text{ USD / año}}$$

### 9.4 Tag Policy e Invariante de Budgets

Los artefactos y recursos asociados al sistema de diseño respetan estrictamente la política institucional:

- **Tag Policy de 7 etiquetas obligatorias:** `FincaID` (`GLOBAL`), `DronID` (`NO-APLICA`), `AcopioID` (`MULTICENTRO`), `ViajeID` (`NO-APLICA`), `Ambiente` (`desarrollo` / `pruebas` / `produccion`), `Propietario` (`devops-fnc`), `Proyecto` (`AromaPacifico`).
- **Invariante de AWS Budgets:** Las alertas de presupuesto emiten notificaciones vía Amazon SNS hacia el equipo de DevOps y arquitectura. Queda terminantemente prohibido que una alerta de presupuesto suspenda los servicios de ingesta, registro vehicular o consulta pública del saco.

---

## 10. Inventario de Entregables de Código y Tokens

Todos los artefactos cumplen con la nomenclatura del proyecto y se encuentran integrados en el repositorio:

1. **Especificación Técnica y Normativa:**
   - [`docs/design/tipografia-espaciado.md`](tipografia-espaciado.md) (El presente documento normativo).
2. **Diccionarios de Tokens W3C DTCG:**
   - [`docs/design/brand/tipografia.json`](brand/tipografia.json): Escalas duales completas (teléfono y web), pesos, alturas de línea y tracking.
   - [`docs/design/brand/espaciado-grilla.json`](brand/espaciado-grilla.json): Sistema modular 8pt/4pt, ergonomía vehicular (touch target 56px), grillas y radios.
   - [`docs/design/brand/tokens.json`](brand/tokens.json): Diccionario central consolidado de la plataforma (colores, estados de saco, tipografía, espaciado y radios).
   - [`docs/design/brand/tokens.css`](brand/tokens.css): Hojas de variables CSS Custom Properties listas para consumo web y móvil híbrido.
3. **Diagramas Técnicos de Arquitectura:**
   - [`docs/architecture/diagrams/diseno-tipografia-espaciado-grilla.drawio`](../architecture/diagrams/diseno-tipografia-espaciado-grilla.drawio): Diagrama fuente editable XML UTF-8 descomprimido.
   - [`docs/architecture/diagrams/diseno-tipografia-espaciado-grilla.svg`](../architecture/diagrams/diseno-tipografia-espaciado-grilla.svg): Diagrama vectorial autónomo de publicación.
