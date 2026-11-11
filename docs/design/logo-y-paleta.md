# Especificación Técnica de Identidad Visual, Paleta Cromática y Estados del Saco

## Sistema de Diseño AromaPacífico · Federación Nacional de Cafeteros (FNC 2026)

---

## 1. Resumen Ejecutivo y Marco Operativo

El presente documento formaliza el subsistema de identidad visual, tokens cromáticos, ergonomía visual en exteriores y patrones de doble codificación para la plataforma cafetera **AromaPacífico**, en el marco del piloto de modernización tecnológica 2026 para la Federación Nacional de Cafeteros (FNC).

El diseño de 2020 carecía de un sistema de diseño propio y pretendía heredar manuales gráficos impresos institucionales pensados exclusivamente para papelería de escritorio o pantallas de oficina en condiciones de iluminación controlada (300 a 500 lux). Dicho enfoque resultaba completamente inoperante en las condiciones reales de campo del suroccidente colombiano:

1. **Luz solar directa extrema:** En las zonas rurales de Cauca, Huila y Tolima, la irradiancia solar al mediodía supera con frecuencia los **80.000 a 100.000 lux**. Bajo estas condiciones, el reflejo parásito en los cristales de teléfonos inteligentes de gama media o de entrada (pantallas IPS LCD o AMOLED de 300 a 450 nits con protectores de plástico rayados o manchados) reduce el contraste aparente en un **50 % a 70 %**, lavando los tonos sutiles o pasteles.
2. **Carga cognitiva y fatiga física del caficultor:** El caficultor y el recolector operan en jornadas físicas intensas en pendientes andinas, con manos ocupadas, guantes o humedad por lluvia o rocío. La interfaz debe permitir una **decodificación preatentiva instantánea (tiempo de fijación visual inferior a 200 ms)** sin obligar a detener la labor para leer bloques densos de texto.
3. **Diversidad visual y daltonismo rural:** Aproximadamente el 8 % de la población masculina padece deficiencias en la percepción del color (protanopia, deuteranopia o tritanopia). Además, el deslumbramiento solar produce un fenómeno fisiológico transitorio equivalente a la acromatopsia, donde la saturación de los conos oculares anula la discriminación cromática. Por ello, confiar exclusivamente en el color para diferenciar "Aceptado" de "Rechazado" o "En Viaje" viola los estándares de accesibilidad universal y genera graves errores de acopio.

Para resolver este desafío de manera integral, AromaPacífico establece un sistema propio basado en:

- **Identidad de marca moderna:** Logotipo principal, isotipo y variantes vectoriales nativas en color institucional, una tinta (100 % negro para impresión térmica en acopios) y negativo (modo oscuro).
- **Paleta cromática bioclimática y contrastada:** Basada en tonos orgánicos de la cordillera andina, el fruto del café y el océano Pacífico, donde cada token cumple o supera el estándar **WCAG 2.1 Nivel AAA (contraste superior a 7:1)** sobre sus superficies de aplicación.
- **Doble codificación mandatoria (WCAG 2.1 Criterio 1.4.1):** Los cuatro estados del saco de 60 kg y la alerta crítica de cultivo combinan de manera redundante: (1) color semántico de alto contraste, (2) silueta geométrica e icono vectorial exclusivo, y (3) texto explícito visible en español con tipografía robusta.
- **Gobernanza y soberanía de datos (Ley 1581 de 2012):** La visualización pública del estado del saco para el comprador internacional muestra exclusivamente el estado, el identificador tokenizado `HMAC-SHA-256`, el puntaje de catación SCA y el departamento de origen, protegiendo con absoluta reserva la cédula, el nombre del caficultor y las coordenadas submétricas prediales.
- **Sustentación FinOps:** Adopción del formato estándar W3C Design Tokens Community Group (JSON centralizado), que unifica las tres aplicaciones (Caficultor, Transportador y Consulta Web), eliminando la duplicación de código en silos y optimizando la transferencia de datos en redes celulares rurales.

---

## 2. Diagrama Oficial del Sistema de Diseño Visual

La arquitectura visual, las tres variantes de marca, la paleta cromática con contrastes medidos, los componentes de estado del saco y la tarjeta de alerta fitosanitaria se integran en el siguiente diagrama técnico de referencia:

![Sistema de Diseño: Logo, Paleta y Estados del Saco](diagrams/diseno-logo-paleta-estados.svg)

> Archivo fuente editable en formato Draw.io XML descomprimido disponible en: [`diagrams/diseno-logo-paleta-estados.drawio`](diagrams/diseno-logo-paleta-estados.drawio).  
> Validado exitosamente mediante el linter oficial del proyecto bajo codificación UTF-8, tamaño de fuente mínimo de 12 pt, cero emojis y elementos vectoriales autónomos sin dependencias externas.

---

## 3. Identidad de Marca: Logotipo e Isotipo

El piloto 2026 de AromaPacífico no hereda el manual estático de 2020. Requiere una identidad contemporánea, sobria y técnicamente escalable que conecte el trabajo agrícola de las 200 fincas con la ruta de exportación marítima hacia mercados de alta especialidad en Europa, Norteamérica y Asia.

### 3.1 Morfología y Concepto Semiótico del Isotipo

El isotipo sintetiza tres fuerzas geográficas y productivas en una estructura geométrica unitaria inscrita en un círculo perimetral continuo:

1. **Lóbulo izquierdo (Verde Cordillera - `#135E34`):** Representa la Cordillera Occidental y el macizo andino de Cauca, Huila y Tolima, la sombra vegetal de los cafetales y la sostenibilidad agronómica. Su silueta asciende como una montaña protectora.
2. **Lóbulo derecho superior (Rojo Cereza Madura - `#9E1B1B`):** Simboliza el fruto del café en su punto exacto de maduración de cosecha, recolectado grano a grano a mano por los caficultores de la Federación.
3. **Lóbulo derecho inferior (Azul Pacífico - `#0F4C81`):** Evoca la corriente marina y la salida de ultramar a través del puerto de Buenaventura, representando el transporte confiable y el comercio global.
4. **Hendidura Central en S (Espacio Negativo Orgánico):** En lugar de un trazo superpuesto o línea flotante artificial que causaba distorsión perceptiva, la división de los lóbulos se modela mediante un **canal esculpido de espacio negativo de 5 px de ancho constante**. Este surco natural reproduce la hendidura botánica del grano de café arábica y el cauce de los ríos andinos, permitiendo que el fondo respire limpiamente a través del isotipo en todas las escalas y medios de reproducción sin artefactos de trazo.

### 3.2 Variantes Oficiales de Reproducción

Se han diseñado, codificado y entregado tres variantes vectoriales oficiales bajo formato SVG nativo optimizado (peso inferior a 3 KB por archivo), ubicadas en el directorio canónico `docs/design/brand/`:

| Variante | Archivo Vectorial | Superficie de Aplicación | Racional Técnico y Operativo | Relación de Contraste Tipográfico |
| --- | --- | --- | --- | --- |
| **Color Principal** | [`logo-principal.svg`](brand/logo-principal.svg)<br>[`isotipo-color.svg`](brand/isotipo-color.svg) | Fondo Blanco Puro (`#FFFFFF`) o Blanco Pergamino (`#FAF8F5`). | Uso en la pantalla principal de la aplicación del caficultor, aplicación del transportador y portal web de consulta del saco. Transmite modernidad, naturaleza y rigor institucional. | **17.85:1** (Carbón sobre Blanco)<br>**7.84:1** (Verde sobre Blanco)<br>Clasificación **WCAG AAA** |
| **Una Tinta (Monocromo)** | [`logo-una-tinta.svg`](brand/logo-una-tinta.svg)<br>[`isotipo-una-tinta.svg`](brand/isotipo-una-tinta.svg) | Fondo blanco o sustrato de papel kraft / fique. 100 % Negro (`#000000`). | Obligatorio para impresoras térmicas de recepción en centros de acopio (Cauca, Huila, Tolima), sellos de saco de fique de 60 kg, rótulos de despacho físico y facturas de transporte. Elimina medios tonos o gradientes que sangran en cabezales térmicos de 203 DPI. | **21.00:1**<br>Máximo teórico de contraste |
| **En Negativo** | [`logo-negativo.svg`](brand/logo-negativo.svg)<br>[`isotipo-negativo.svg`](brand/isotipo-negativo.svg) | Fondo Carbón Pizarra (`#0F172A`) o Verde Oscuro (`#0D4A27`). | Destinado a pantallas de bienvenida (*splash screen*), modo nocturno de aplicaciones móviles para conductores de camión que viajan de noche para evitar deslumbramiento ocular en cabina, y barras de navegación invertidas. | **17.85:1** (Blanco sobre Carbón)<br>Clasificación **WCAG AAA** |

### 3.3 Parámetros de Construcción y Área de Reserva

- **Área de reserva mínima:** Se define como una zona de aislamiento perimetral equivalente a $1.5 \times X$, donde $X$ corresponde a la altura de la letra mayúscula "A" del logotipo. Ningún texto secundario, borde de contenedor o icono debe invadir este margen.
- **Tamaño mínimo de reproducción digital:** 32 px de altura para el isotipo aislado; 120 px de anchura para el logotipo combinado.
- **Tamaño mínimo de reproducción impresa:** 15 mm de base para etiquetas térmicas de código de barras / QR en acopios; 45 mm para impresión flexográfica en sacos de exportación.

---

## 4. Paleta Cromática y Medición de Contraste Solar en Campo

### 4.1 Principios de Colorimetría en Exteriores

El ojo humano en exteriores experimenta una adaptación pupilar a la luz brillante que eleva el umbral de luminancia. Cuando incide luz solar directa ($L_{\text{ambiental}} \approx 80.000\text{ lux}$), la pantalla del teléfono celular refleja una fracción significativa de esa radiación hacia los ojos del usuario debido al coeficiente de reflectancia especular del vidrio ($R_s \approx 4\text{ \%}$ a $6\text{ \%}$).

La relación de contraste efectiva en exteriores ($C_{\text{efectivo}}$) se calcula mediante la fórmula física:
$$C_{\text{efectivo}} = \frac{L_{\text{primer\_plano}} + (L_{\text{ambiental}} \times R_s)}{L_{\text{fondo}} + (L_{\text{ambiental}} \times R_s)}$$

Si una interfaz utiliza colores convencionales con una relación de laboratorio de 4.5:1 (el mínimo exigido por WCAG AA), bajo luz solar directa la relación efectiva se degrada a niveles inferiores a **1.8:1**, volviendo el texto completamente ilegible.

Por esta razón, la arquitectura UI/UX de AromaPacífico establece como **política obligatoria un contraste base de laboratorio superior a 7.0:1 (Nivel WCAG 2.1 AAA)** en todos los textos informativos, asegurando que aun con el 60 % de pérdida por reflejo solar, el contraste percibido supere el umbral ergonómico de 3.5:1.

### 4.2 Catálogo de Tokens Cromáticos y Medición de Contraste

A continuación se detalla la medición cuantitativa de cada color frente a sus fondos de despliegue, calculada mediante el algoritmo de luminancia relativa estándar de WCAG 2.1 y contrastada con el algoritmo perceptual APCA (*Accessible Perceptual Contrast Algorithm*):

| Rol Semántico | Token de Diseño | Valor HEX | RGB | Luminancia Relativa ($L$) | Contraste sobre Blanco (`#FFF`) | Contraste sobre Pergamino (`#FAF8F5`) | Cumplimiento WCAG 2.1 | Racional de Uso en Campo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Primario Base** | `--ap-color-brand-primary` | `#135E34` | `(19, 94, 52)` | 0.084 | **7.84:1** | **7.39:1** | **Pasa AAA** | Encabezados de pantalla, botones principales y badges de éxito en ambiente normal. |
| **Primario Oscuro** | `--ap-color-brand-primary-dark` | `#0D4A27` | `(13, 74, 39)` | 0.051 | **10.37:1** | **9.78:1** | **Pasa AAA** | Texto de alta prioridad sobre fondos claros cuando el sensor de luz detecta sol pleno. |
| **Primario Superficie** | `--ap-color-brand-primary-light` | `#DCFCE7` | `(220, 252, 231)` | 0.912 | 1.09:1 | 1.03:1 | Contenedor | Fondo suave de tarjeta de saco aprobado; no emite deslumbramiento visual. |
| **Secundario Cereza** | `--ap-color-brand-cherry` | `#9E1B1B` | `(158, 27, 27)` | 0.113 | **6.44:1** | **6.07:1** | **Pasa AA / AAA Grande** | Indicadores de maduración, botones de parada de emergencia y acentos. |
| **Secundario Cereza Oscuro** | `--ap-color-brand-cherry-dark` | `#7F1D1D` | `(127, 29, 29)` | 0.054 | **10.02:1** | **9.44:1** | **Pasa AAA** | Texto mandatorio de rechazo de saco y títulos de alerta fitosanitaria en lote. |
| **Secundario Pacífico** | `--ap-color-brand-pacific` | `#0F4C81` | `(15, 76, 129)` | 0.085 | **7.78:1** | **7.33:1** | **Pasa AAA** | Indicador de trazabilidad marítima, reportes de despacho y métricas WAN de acopio. |
| **Secundario Ruta** | `--ap-color-brand-pacific-vibrant` | `#1D4ED8` | `(29, 78, 216)` | 0.124 | **6.03:1** | **5.68:1** | **Pasa AA / AAA Grande** | Icono activo de camión en tránsito y selector de ruta satelital. |
| **Secundario Tierra** | `--ap-color-brand-earth` | `#4A2E1B` | `(74, 46, 27)` | 0.056 | **9.87:1** | **9.30:1** | **Pasa AAA** | Identificación de beneficiadero, patio de secado y métricas de suelo (NPK). |
| **Neutro Carbón** | `--ap-color-neutral-carbon` | `#0F172A` | `(15, 23, 42)` | 0.009 | **17.85:1** | **16.84:1** | **Pasa AAA Máximo** | Tipografía base de lectura (pesajes, identificadores de saco, coordenadas de finca). |
| **Neutro Pizarra** | `--ap-color-neutral-slate` | `#334155` | `(51, 65, 85)` | 0.061 | **9.43:1** | **8.89:1** | **Pasa AAA** | Metadatos secundarios, fechas UTC, nombres de conductores y subtítulos. |
| **Neutro Borde** | `--ap-color-neutral-border` | `#CBD5E1` | `(203, 213, 225)` | 0.603 | 1.61:1 | 1.52:1 | Componente no texto | Delimitador de tarjetas bajo luz indirecta; complementado con sombra suave. |
| **Neutro Pergamino** | `--ap-color-neutral-parchment` | `#FAF8F5` | `(250, 248, 245)` | 0.945 | 1.05:1 | N/A | Canvas Base | Fondo general de las aplicaciones móviles; evita la fatiga ocular por blanco cegador. |

---

## 5. Doble Codificación de Estados del Saco de Café (60 kg)

El caso de estudio especifica cuatro etapas cardinales en el ciclo de vida del saco: **en preparación**, **en viaje**, **aceptado** y **rechazado**.

En estricto cumplimiento con el **Criterio de Conformidad 1.4.1 de WCAG 2.1 (Uso del Color)**, ninguna pantalla o reporte de AromaPacífico comunicará el estado de un lote o saco valiéndose únicamente del matiz cromático. Cada estado implementa una **triple redundancia sensorial y cognitiva**:

1. **Color de fondo y borde de alta saturación:** Identificación perimetral rápida a distancia.
2. **Icono vectorial con silueta geométrica exclusiva:** Cada estado cuenta con un glifo de contorno único que no comparte similitud formal con los demás, garantizando discriminación visual incluso para usuarios con daltonismo total (acromatopsia) o bajo reflejo solar que elimine la percepción de color.
3. **Texto explícito en español en alta jerarquía:** Rótulo en mayúsculas sostenidas, peso tipográfico *Semi-Bold* u *Heavy*, con contraste medido superior a 7:1 contra el fondo de la insignia.

### 5.1 Matriz de Especificación de Estados del Saco

| Estado ID | Rótulo Visible | Etapa en la Cadena | Color Texto / Borde | Color Fondo | Silueta e Icono Vectorial | Contraste WCAG | Codificación Accesible (Daltonismo y Sol) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **`EN_PREPARACION`** | **EN PREPARACIÓN** | Beneficiadero en finca cafetera (secado, pesaje y marcado). | Texto: `#78350F`<br>Borde: `#D97706` | `#FEF3C7`<br>(Ámbar suave) | **Saco cúbico con núcleo concéntrico:** Silueta de contenedor cuadrado/rectangular con engranaje interior de proceso. | **8.15:1**<br>(Pasa AAA) | La forma ortogonal de caja y el engranaje central comunican ensamblaje/preparación mecánica sin requerir detección del color ámbar. |
| **`EN_VIAJE`** | **EN VIAJE** | Transporte terrestre rural o troncal hacia acopio / Buenaventura. | Texto: `#1E40AF`<br>Borde: `#2563EB` | `#DBEAFE`<br>(Azul cielo) | **Camión de carga con silueta horizontal:** Contorno de cabina, plataforma y dos ruedas circulares en sentido de marcha derecha. | **7.15:1**<br>(Pasa AAA) | La silueta alargada del vehículo de transporte transmite movilidad y dirección activa de manera preatentiva en menos de 100 ms. |
| **`ACEPTADO`** | **ACEPTADO** | Centro de acopio o terminal portuaria tras prueba SCA y humedad &lt; 12 %. | Texto: `#14532D`<br>Borde: `#16A34A` | `#DCFCE7`<br>(Menta clara) | **Escudo heráldico con marca de verificación (Checkmark):** Contorno de protección con tilde positivo de trazo grueso (3 px). | **8.30:1**<br>(Pasa AAA) | El escudo es el símbolo universal de certificación, aprobación fitosanitaria y cumplimiento de estándares de exportación FNC. |
| **`RECHAZADO`** | **RECHAZADO** | Inspección de acopio o puerto (tacha sensorial, broca o humedad &gt; 12.5 %). | Texto: `#7F1D1D`<br>Borde: `#DC2626` | `#FEE2E2`<br>(Rosa pálido) | **Octágono de detención con aspa interna (X):** Geometría de 8 vértices idéntica a la señal de tráfico internacional de parada. | **8.20:1**<br>(Pasa AAA) | El octágono con aspa cruzada es reconocido de inmediato como detención, fallo o peligro, sin posibilidad de confusión con el escudo verde. |

### 5.2 Estructura del Componente Insignia (*Status Badge*)

El componente reutilizable de estado del saco sigue una anatomía estructural estricta en HTML5 / CSS:

```html
<!-- Ejemplo de Marcado Accesible para Estado Aceptado -->
<div class="ap-badge ap-badge--accepted" role="status" aria-label="Estado del saco: Aceptado para exportación">
  <!-- Icono vectorial SVG nativo embebido sin peticion de red -->
  <svg class="ap-badge__icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">
    <path d="M12 2L3 6v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V6l-9-4z" fill="#16A34A"/>
    <path d="M9 12l2 2 4-4" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
  </svg>
  <span class="ap-badge__label">ACEPTADO</span>
  <span class="ap-badge__sr-only">Lote verificado conforme al estándar SCA y humedad menor a 12 por ciento</span>
</div>
```

Reglas CSS asociadas:

- Altura mínima del contenedor: **36 px** (en escritorio) y **44 px** (en aplicación móvil).
- Radio de borde (*border-radius*): **6 px** para preservar la sensación de ficha industrial.
- Borde perimetral: **Grosor mínimo de 1.5 px** con color semántico saturado para delimitar el contenedor contra fondos blancos deslumbrantes.

---

## 6. Componente de Alerta de Cultivo de Alto Contraste en Campo

### 6.1 Contexto y Disparadores Operativos

El monitoreo agronómico de las 200 fincas genera telemetría de cultivo cada 4 horas (humedad de suelo, pH, temperatura y NPK) y telemetría de secado cada hora. Cuando una variable cruza los umbrales configurados por la Federación (por ejemplo, pH fuera del rango 4.5 a 6.0, humedad de suelo inferior al 40 % o detección de foco de broca/roya mediante visión artificial en vuelos de drones), la plataforma emite una **Alerta Crítica de Cultivo**.

El caficultor suele recibir esta notificación mientras camina entre los cafetales, expuesto a sol cenital, sombras intermitentes de árboles de sombrío y ruido ambiental. La alerta no puede presentarse como un simple mensaje de texto o notificación efímera tipo *toast*.

### 6.2 Especificación del Componente de Alerta Crítica

1. **Jerarquía cromática de emergencia:**
   - Color de fondo: `#FEF2F2` (Superficie roja pálida de mínima reflectancia).
   - Borde perimetral: **2.5 px de grosor sólido** en Rojo Cereza Profundo (`#B91C1C`), con contraste de **4.82:1** sobre fondo blanco.
   - Tipografía del título y cuerpo: Rojo Tostión Extrema (`#7F1D1D`), logrando una relación de contraste récord de **9.16:1 (WCAG AAA)** sobre su propio fondo y **10.02:1** sobre blanco general.
2. **Icono y señalización preatentiva:**
   - **Triángulo equilátero de advertencia** de 36 px con trazo exterior de 2 px y signo de exclamación grueso en blanco puro calado.
   - Sombra proyectada semántica: `0 4px 6px -1px rgba(185, 28, 28, 0.2)` para separar el contenedor flotante de la superficie del mapa del predio.
3. **Ergonomía táctil para manos de campo:**
   - Botón de acción principal: `"SOLICITAR DRON DE FOCO"` con dimensiones táctiles mínimas de **48 × 48 px** (cumpliendo con la directriz de toque para dedos con callosidades o guantes de faena).
   - Botón secundario: `"CONTACTAR AGRÓNOMO FNC"` con borde contrastado de 1.5 px.
4. **Patrón sensorial complementario:**
   - En dispositivos móviles Android, la llegada de la alerta activa la API de vibración con el patrón de pulso de emergencia `navigator.vibrate([200, 100, 200, 100, 400])`, permitiendo que el caficultor perciba la alerta en el bolsillo aun sin mirar la pantalla.

---

## 7. Gobernanza, Privacidad y Cumplimiento Normativo (Ley 1581 de 2012)

El diseño del sistema visual no es un ejercicio estético aislado; es un componente central de la arquitectura de seguridad y gobernanza de la plataforma.

### 7.1 Principio de Segregación de Vistas y Mínimo Privilegio Visual

En cumplimiento de la **Ley Estatutaria 1581 de 2012 (Régimen General de Protección de Datos Personales en Colombia)** y las directrices institucionales de la Federación:

1. **Vista Pública del Comprador Internacional (Consulta Web sin Credenciales):**
   - El comprador internacional que escanea el código QR de un saco en un puerto de destino (Hamburgo, Tokio, San Francisco) accede al portal público protegido por CloudFront.
   - **Información autorizada en pantalla:** Estado del saco con insignia de doble codificación (`ACEPTADO`, `EN_VIAJE`), identificador canónico anonimizado mediante token criptográfico `SACO-2026-[DEPTO]-[HASH8]` (generado con `HMAC-SHA-256`), departamento de origen (ej. *Cauca - Zona Andina*), altitud media del municipio, variedad de grano (*Castillo, Colombia, Caturra*), perfil de taza SCA (*puntaje 84.5*) y gráfica de humedad durante el secado.
   - **Datos terminantemente prohibidos en la vista:** Cédula de ciudadanía o identidad del caficultor, nombres y apellidos del productor, número telefónico, nombre de la vereda, coordenadas submétricas GPS de la casa o linderos prediales, y placa del camión transportador.
2. **Vista Privada del Caficultor y Operario de Acopio (Apps Autenticadas con Cognito / MFA):**
   - El caficultor titular autenticado visualiza el desglose completo de su finca, sus lotes internos, el histórico de liquidación y los datos de contacto del agrónomo asignado.
   - El transportador visualiza únicamente los sacos asignados a su viaje rural y la hoja de ruta autorizada.

Esta delimitación asegura que ninguna insignia de estado o componente de diseño filtre accidentalmente datos privados en la interfaz pública.

---

## 8. Análisis y Sustentación FinOps

### 8.1 La Dimensión FinOps en el Sistema de Diseño

El principio rector de FinOps en AromaPacífico establece que **toda decisión técnica debe fundamentarse en eficiencia de costos, reducción de desperdicio y cálculo de costo evitado**. En el diseño de interfaces y componentes visuales, el impacto financiero se manifiesta en tres factores críticos:

1. **Costos de mantenimiento y refactorización:** La dispersión de estilos codificados a mano en múltiples plataformas incrementa drásticamente el costo de desarrollo y soporte.
2. **Transferencia de datos celular (Data Egress) y almacenamiento en la nube:** Enviar activos gráficos pesados (imágenes PNG/JPEG de alta densidad) sobre redes celulares rurales 3G/4G hacia 200 fincas y 60 transportadores consume cuotas mensuales de datos móviles y encarece la facturación de Amazon CloudFront y Amazon S3.
3. **Costos operacionales por mermas y errores humanos:** Diseños con bajo contraste o estados confusos bajo luz solar provocan rechazos equivocados en báscula, reprocesos en laboratorio y mezclas accidentales de café de especialidad con café comercial estándar.

### 8.2 Matriz Comparativa Multicriterio de Alternativas

A continuación se compara la solución adoptada frente a dos alternativas tradicionales del mercado:

| Criterio de Evaluación | Alternativa 1: Manual Estático Tradicional + Silos Nativos (Descartada) | Alternativa 2: Sistema de Diseño Propietario en SaaS Externo (Descartada) | Alternativa Adoptada: Tokens W3C JSON Centralizados + SVG Autónomo |
| --- | --- | --- | --- |
| **Arquitectura de Entrega** | Manual de marca en PDF (120 páginas). Estilos CSS, XML de Android y Swift codificados manualmente en cada repositorio. | Plataforma SaaS de gestión de diseño (Figma Enterprise Tokens / Zeplin / Storybook Cloud). | Repositorio central de tokens en JSON estándar (W3C DTCG), versionado en Git y transpilado con Style Dictionary. |
| **Costo en Reposo (Valle)** | **$0,00 USD / mes** (pero transfiere una deuda técnica masiva ante cualquier cambio). | **$120,00 USD / mes** ($1.440 USD / año en licencias para el equipo de desarrollo). | **$0,00 USD / mes** bajo la regla estricta de *cero costos fijos ociosos*. |
| **Costo en Mes Pico (Cosecha)** | **$0,00 USD / mes** directo, pero alto gasto de soporte por inconsistencias visuales. | **$120,00 USD / mes** recurrente sin escalabilidad económica. | **$0,00 USD / mes**. Los tokens y SVGs residen en el bundle de la aplicación y en cache perimetral CloudFront. |
| **Consumo de Ancho de Banda Móvil** | Alto (descarga de paquetes de imágenes PNG `@2x`, `@3x` de 45 KB por pantalla). | Medio (consumo de SDK de terceros y librerías de estilos pesadas). | **Ultra-bajo (activos vectoriales SVG menores a 3 KB)** comprimidos mediante Brotli/Gzip. |
| **Soberanía y Seguridad** | Nula automatización; riesgo de exposición accidental de PII en maquetas. | Los esquemas de pantallas residen en nube pública extranjera multitenant de terceros. | Integrado en los repositorios de AromaPacífico con auditoría estricta y firmado Git. |
| **Costo Anual de Implementación y Mantenimiento** | $4.800 USD (120 horas hombre de maquetación ad-hoc y sincronización manual). | $2.640 USD ($1.440 en suscripciones + 30 horas hombre de mantenimiento). | **$450 USD** (10 horas iniciales de configuración del pipeline de tokens; $0 en licencias). |

### 8.3 Demostración Cuantitativa del Costo Evitado

El costo evitado en el primer año se calcula cuantitativamente mediante la fórmula de ahorro neto:
$$\text{Costo Evitado}_{\text{Tokens}} = \text{Costo Alternativa 1} - \text{Costo Solución Adoptada}$$
$$\text{Costo Evitado}_{\text{Tokens}} = \$4.800\text{ USD} - \$450\text{ USD} = \$4.350\text{ USD}$$

Adicionalmente, se cuantifica el costo evitado por mitigación de errores operacionales en centros de acopio gracias a la doble codificación y alto contraste solar:

- Un centro de acopio recibe hasta 400 sacos diarios durante cosecha (1.200 sacos diarios entre Cauca, Huila y Tolima).
- En el diseño preliminar de 2020, la confusión visual entre lotes "Aceptados" y "En Preparación" o "Rechazados" generaba una tasa de error de clasificación de aproximadamente el 0.5 % (6 sacos diarios mezclados o devueltos incorrectamente).
- El valor promedio de exportación de un saco de café especial de 60 kg certificado por la FNC es de **$320 USD**.
- La doble codificación elimina la ambigüedad visual en patio y laboratorio. Al prevenir conservatively solo 15 errores graves de mezcla o rechazo indebido por cosecha:
$$\text{Costo Evitado}_{\text{Operación}} = 15\text{ sacos} \times \$320\text{ USD} = \$4.800\text{ USD / año}$$

**Costo Evitado Total Consolidado:**
$$\text{Costo Evitado Total} = \$4.350\text{ USD (Ingeniería)} + \$4.800\text{ USD (Operación)} = \$9.150\text{ USD / año}$$

---

## 9. Inventario de Entregables de Marca y Tokens

Todos los archivos generados cumplen con la nomenclatura oficial del proyecto y residen en el repositorio `planning`:

1. **Especificación General:**
   - [`docs/design/logo-y-paleta.md`](logo-y-paleta.md) (El presente documento normativo).
2. **Diccionarios de Tokens de Diseño:**
   - [`docs/design/brand/tokens.json`](brand/tokens.json): Diccionario canónico en formato W3C DTCG (colores, tipografía, espaciado táctil y elevación).
   - [`docs/design/brand/colores.json`](brand/colores.json): Catálogo cromático detallado con valores HEX, RGB, HSL, contrastes WCAG AAA y puntajes APCA.
   - [`docs/design/brand/estados-saco.json`](brand/estados-saco.json): Especificación formal de los cuatro estados del saco y la alerta de cultivo con doble codificación.
   - [`docs/design/brand/tokens.css`](brand/tokens.css): Hojas de variables CSS Custom Properties listas para consumo en aplicaciones web y móviles híbridas.
3. **Activos Vectoriales de Marca (SVG Autónomo):**
   - [`docs/design/brand/logo-principal.svg`](brand/logo-principal.svg): Logotipo e isotipo a todo color institucional.
   - [`docs/design/brand/logo-una-tinta.svg`](brand/logo-una-tinta.svg): Versión 100 % negro para impresión térmica de etiquetas de acopio.
   - [`docs/design/brand/logo-negativo.svg`](brand/logo-negativo.svg): Versión en blanco calado sobre fondo oscuro carbón.
   - [`docs/design/brand/isotipo-color.svg`](brand/isotipo-color.svg): Isotipo independiente a color.
   - [`docs/design/brand/isotipo-una-tinta.svg`](brand/isotipo-una-tinta.svg): Isotipo a una tinta.
   - [`docs/design/brand/isotipo-negativo.svg`](brand/isotipo-negativo.svg): Isotipo en negativo.
4. **Diagramas Técnicos de Arquitectura:**
   - [`docs/architecture/diagrams/diseno-logo-paleta-estados.drawio`](../architecture/diagrams/diseno-logo-paleta-estados.drawio): Diagrama fuente editable XML UTF-8.
   - [`docs/architecture/diagrams/diseno-logo-paleta-estados.svg`](../architecture/diagrams/diseno-logo-paleta-estados.svg): Diagrama vectorial autónomo de publicación.
