# Estrategia de producción de arte 2D y presupuesto Higgsfield — Fase 0

## Resumen ejecutivo

Recomiendo el **escenario equilibrado**: 553 créditos para arte, audio y pruebas; 160 protegidos para la transición a 3D; y 287 de contingencia. Son límites de gasto, no una obligación de consumirlos.

La producción debe apoyarse en tres herramientas principales: `gpt_image_2_6` para borradores, ilustraciones y transparencia; `nano_banana_pro` para consolidar personajes mediante referencias; y `recraft_v4_1` para símbolos vectoriales. Los demás modelos resolverían problemas concretos, después de una comparación pequeña.

La consistencia dependerá de una hoja maestra aprobada, referencias propias, bloques de prompt estables y revisión conjunta de los recursos. Ningún modelo garantiza por sí solo un turnaround correcto, continuidad de animación o exactitud científica.

El presupuesto cubre el **paquete 2D del vertical slice** y su audio. Las mallas, rigging y animaciones 3D requieren una puerta técnica independiente; su costo completo sigue sin verificar.

Se leyeron los archivos solicitados. No se instalaron programas, modificaron archivos, subieron recursos ni gastaron créditos de Higgsfield.

## Decisiones recomendadas

Las recomendaciones de esta tabla son **[inf]**, fundamentadas en los [costos locales][L1], los [parámetros disponibles][L3] y las fuentes desarrolladas más adelante.

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Presupuesto | Escenario equilibrado; liberar gasto por recurso aprobado | Consumir 1000 créditos al principio dejaría sin margen las correcciones e integración | Alta |
| Generador principal | GPT Image 2.6: borradores `low`, finales normalmente `high` | `max` y 4k para todo aumentan mucho el costo sin una necesidad demostrada | Alta en costo; media en resultado |
| Identidad de personajes | Nano Banana Pro a 2k con referencias maestras | Generar cada imagen únicamente desde texto facilita cambios de diseño | Media |
| Turnaround | Hoja conjunta para aprobar diseño; vistas individuales para producción | Tratar una hoja generada como geometría ortográfica exacta | Media |
| Soul ID | Excluirlo del presupuesto inicial | Su entrenamiento está orientado a rostros fotográficos; utilidad para chibi y gato sin verificar | Alta |
| Transparencia | PNG con alfa nativo cuando el modelo lo admite; revisar los bordes | Pagar eliminación de fondo para cada recurso, aunque ya pueda salir con alfa | Alta |
| Interfaz | Generar ilustración y materiales; componer texto, barras y estados en Godot | Una captura de HUD completa resulta difícil de adaptar y traducir | Alta |
| Texturas | Materiales pequeños, iluminación uniforme y verificación de repetición | Confiar únicamente en la palabra «seamless» del prompt | Alta |
| Música | Sonilo como primera opción económica; ElevenLabs para pruebas selectivas | Elegir una versión más reciente sin escucha comparativa ni comprobar su licencia | Media |
| Voz | Texto completo y pocas intervenciones; reservar 10 créditos en el equilibrado | Doblar todos los diálogos antes de cerrar guion y voces | Alta |
| Video | Opcional y posterior a la validación visual; tope inicial de 15 créditos | Usarlo como pipeline habitual de personajes o fondos | Alta |
| Adecuación al equipo | Generación remota y derivados locales pequeños, procesados por separado | Generación local de IA o recursos 4k masivos en este portátil | Media; rendimiento pendiente de medición |

## Afirmaciones que sostienen las decisiones

1. **[doc]** La matriz suministrada contiene cotizaciones de `generate cost`, no resultados de generaciones. Los casos con error carecen de precio válido; no cuestan cero. [Matriz local][L1].

2. **[doc]** GPT Image 2.6 cuesta 0,25 créditos en `low/1k`, 1,5 en `high/1k`, 2,75 en `high/2k` y 15 en `max/4k`. El lote medido de cuatro imágenes `high/1k` cuesta 6: no muestra descuento. [Costos locales][L1].

3. **[doc]** El esquema local admite hasta 14 referencias en Nano Banana Pro. Google documenta ese límite y controles para combinar referencias de personajes, objetos y estilo. No equivale a garantizar identidad perfecta. [Esquema local][L3]; [documentación de Google][W1].

4. **[doc]** GPT Image 2.6 ofrece fondo transparente y salida PNG. Su ruta SVG no acepta referencias según el contrato local. [Documentación de Higgsfield][W2]; [parámetros locales][L3].

5. **[doc]** `soul_location` y `recraft_v4_1` son rutas únicamente de texto en el esquema disponible. Recraft permite especificar colores hexadecimales y modo vectorial. [Parámetros locales][L3].

6. **[doc]** FLUX Kontext está diseñado para edición guiada por imágenes y conservación de elementos entre ediciones. La documentación describe esa capacidad, sin convertirla en una garantía para este proyecto. [Documentación de BFL][W3].

7. **[doc] [inf]** `3d_jutsu_angles` figura como modelo de **imagen**. Recomiendo probarlo para vistas adicionales; que entregue ortografía exacta o una malla es **sin verificar**. El espacio de trabajo público «3D Jutsu» es una función distinta y no demuestra esas propiedades del modelo. [Esquema local][L3]; [descripción pública de 3D Jutsu][W4].

8. **[doc]** La guía Soul ID solicita entre 5 y 20 fotografías de un rostro y excluye avatares no fotográficos de su uso previsto. No demuestra entrenamiento fiable de personajes chibi ni animales. [Guía local Soul ID][S6].

9. **[doc]** A 120 segundos, las cotizaciones son 7,5 créditos para Sonilo, 7,68 para ElevenLabs Music v2 y 17,44 para v2.5. Mirelo cuesta 0,75 por el caso medido de 3 segundos. [Matriz local][L1].

10. **[doc]** Higgsfield permite el uso comercial de resultados, pero exige cumplir también las políticas aplicables de proveedores terceros; prevalecen las más restrictivas. [Términos, §§4.4 y 8][W5].

11. **[doc]** Los créditos de suscripción de Higgsfield no se acumulan entre períodos. Las reservas propuestas deben utilizarse dentro de su vigencia real. [Términos, §9.4][W5].

12. **[doc] [inf]** Las dimensiones de una textura afectan su memoria, aunque el PNG pese poco en disco. Una imagen RGBA8 de 4096² contiene aproximadamente 64 MiB de píxeles antes de compresión, mipmaps y otras copias. Recomiendo limitar los derivados de juego por tamaño visible. [Importación de imágenes en Godot][W6]; cálculo: `4096 × 4096 × 4`.

## Riesgos y cómo mitigarlos

| Riesgo | Mitigación propuesta |
|---|---|
| Cambian rostro, vestuario o marcas del gato | Comparar cada resultado con la hoja maestra; corregir desde la última versión aprobada |
| Las vistas contradicen la forma del personaje | Superponer guías de altura, cabeza, hombros y accesorios; validar espalda y perfil antes del paso a 3D |
| El acabado deriva hacia fotografía o fantasía genérica | Mantener una referencia propia de estilo y revisar una composición con personaje, suelo, prop e interfaz |
| Una edición modifica zonas correctas | Comparar antes/después y conservar solamente la región útil mediante composición local |
| Texturas con costuras o patrones evidentes | Revisar repetición 2×2, desplazamiento de media imagen y vista cercana de las uniones |
| Alfa con halos o pérdida de pelo/hierba | Inspeccionar sobre fondos claro, oscuro y de juego; evitar recortes agresivos |
| Concept art confundido con recurso jugable | Aprobar por separado diseño, preparación técnica e integración |
| Saturación de RAM o disco | Derivados pequeños; lotes locales secuenciales; conservar originales elegidos y eliminar duplicados solamente en una fase autorizada |
| Gasto repetido ante un trabajo lento | Consultar primero el estado del trabajo existente; un timeout no demuestra que haya fallado |
| Licencia musical insuficiente | Registrar la ruta de generación y comprobar cobertura para videojuego, tráiler y eventual publicación separada |
| Error científico en instrumentos o diagramas | Revisar su funcionamiento con documentación técnica; usar la IA para presentación, no como validación científica |
| Reserva que caduca sin utilizarse | Planificar las puertas de revisión dentro del período disponible; no apresurar generaciones para consumir saldo |

Estas son medidas de producción **[inf]**, apoyadas en las [guías de edición y diagnóstico][S1], [texturas][S3], [estilización][S2] y [términos comerciales][W5].

## Preguntas que debe decidir el usuario

- **Presupuesto:** adoptar el equilibrado, el conservador o el ambicioso.
- **Representación jugable:** mantener personajes 3D como requisito del slice o permitir sprites como alternativa si falla la puerta técnica.
- **Alcance del protagonista:** un aspecto fijo durante el slice o personalización. Los presupuestos siguientes contemplan **un aspecto aprobado por personaje**.
- **Presentación narrativa:** cuántas expresiones necesitan realmente los NPC y si las viñetas de carga aportan información durante el tiempo de carga previsto.
- **Audio:** aprobar cinco pistas de aproximadamente dos minutos y voz limitada, o redistribuir esa reserva.
- **Identidad final:** definir el nombre público antes de producir el logotipo definitivo.

## Desarrollo

### 1. Alcance y criterio de evidencia

Fecha de corte: **12 de noviembre de 2026**.

- **[doc]:** documentación primaria, contratos y registros técnicos locales.
- **[sec]:** fuente secundaria. No se necesita ninguna para sostener las decisiones principales.
- **[inf]:** propuesta o deducción que debe validarse en producción.
- **Sin verificar:** falta evidencia suficiente sobre capacidad, costo, licencia o comportamiento.

Los costos proceden de los tres archivos solicitados: [matriz][L1], [valores predeterminados][L2] y [esquemas de modelos][L3]. Las comparaciones de calidad son hipótesis de selección: **no se realizaron generaciones ni una evaluación visual comparativa entre modelos**.

El tablero aporta principios observables: siluetas compactas, materiales pintados, profundidad atmosférica, vegetación por masas y una interfaz de papel. La propuesta es convertirlos en una dirección propia. Las capturas no deben convertirse automáticamente en referencias subidas: contienen obra ajena, superposiciones y personas. **[inf]**

También hay instrucciones locales que requieren actualización para este caso:

- La afirmación de que ningún modelo produce alfa contradice el esquema actual y la documentación de GPT Image 2.6.
- El requisito de insertar un prompt en toda animación no aplica literalmente a los modos normales de `autosprite`: el esquema reserva `prompt` y `name` para `kind=custom`.
- Las recetas web de tableros no justifican generar una imagen por cada pantalla del juego.
- Las recomendaciones de dos pistas y cinco efectos para juegos pequeños quedan sustituidas por el alcance explícito de cinco pistas y treinta efectos. **[doc] [inf]** [Referencias locales][S2] [S4] [S5]; [esquemas][L3].

### 2. Qué modelo usar por entregable

**[inf]** Esta es la asignación recomendada. Los precios son los casos medidos en la [matriz][L1]; los controles corresponden al [esquema local][L3]. No se extrapola un precio predeterminado a modos no cotizados.

| Entregable | Modelo y configuración recomendados | Motivo y preparación |
|---|---|---|
| Exploración de estilo | GPT `low/1k`: **0,25**. Opcional: Z Image **0,15** o Soul Location **0,12**, predeterminados | GPT permite continuar mediante referencias. Los otros sirven para explorar composición o ambiente, no para fijar identidad |
| Concept de personaje | Borrador GPT; maestro Nano Banana Pro `2k`: **2** | Concentrar referencias de proporción, rostro, vestuario y acabado en una sola generación controlada |
| Hoja de modelo / turnaround | Hoja conjunta Nano Banana Pro `2k`: **2**. Vistas adicionales con Jutsu `1k/1.5k`: **1,25** cada una; `2k`: **2,5** | La hoja permite detectar contradicciones; las vistas individuales dan más espacio al detalle |
| Hoja de expresiones | Nano Banana Pro `2k`: **2**; alternativa GPT `high/1k`: **1,5** | Mantener encuadre, anatomía y peinado; cambiar solamente la expresión |
| Hoja de props | GPT para diseños individuales; componer la hoja localmente | Evita perder recursos porque una sola celda de una hoja grande sale incorrecta |
| Concept de entorno | Soul Location para miniaturas **0,12**; consolidación con Nano Banana Pro `2k`: **2** o GPT `high/2k`: **2,75** | La composición barata se transforma después en una referencia propia que sí admite edición |
| Texturas repetibles pintadas | GPT `high/1k`: **1,5**, con patrón y luz uniforme | Acompañar con corrección y comprobación local de bordes; la repetición no queda garantizada por generar |
| Capas de parallax | GPT con referencia del escenario aprobado; `high/1k–2k`: **1,5–2,75** | Repetir encuadre, horizonte y escala; alfa para elementos aislados |
| Cielos | GPT `medium/2k`: **1** o `high/2k`: **2,75** | Trabajar nubes, horizonte y color como piezas reutilizables; no tratar una imagen corriente como iluminación HDR |
| Iconos y kit de interfaz | GPT para acabado pintado; Recraft para símbolos simples | Usar hojas pequeñas de iconos. Mantener palabras, cifras y estados fuera de la imagen |
| Logotipo | Recraft `model_type=vector`, tres candidatos comparables | Control de paleta y geometría simple. **1,25 es el costo predeterminado registrado; el modo vectorial concreto está sin verificar** |
| Mapa ilustrado | GPT `high/2k`: **2,75**, con referencias propias | Generar decoración y terreno; colocar ubicaciones, rutas y leyenda desde los datos del nivel |
| Viñetas de carga | Nano Banana Pro `2k`: **2** o GPT `high/2k`: **2,75** por ilustración | Generar viñetas separadas; montar marcos y texto localmente |
| Retratos de diálogo | Nano Banana Pro `2k`: **2** o GPT `high/1k`: **1,5** | Reutilizar expresión y encuadre aprobados; derivar recortes cuando tengan resolución suficiente |

Una cámara 3/4 elevada y una vista lateral necesitan **dos especificaciones de cámara**, aunque compartan el mismo estilo. La hoja de modelado puede emplear cámara ortográfica a la altura del personaje y un 3/4 ortográfico; no debe confundirse con la cámara elevada del juego. **[inf]**

#### Modelos especializados y utilidades

| Modelo | Uso recomendado | Costo y límite relevante |
|---|---|---|
| `seedream_5_5` | Comparación puntual para expresiones, anatomía o una hoja que falle repetidamente | **2,5** a 1k/1.5k; **3,5** a 2k; hasta diez referencias. Declara fondo transparente, cuyo resultado efectivo no se probó |
| `flux_kontext` | Edición concreta: accesorio, color o cambio localizado | **1,5**; hasta cuatro referencias. Volver al maestro si aparecen cambios acumulados |
| `ideogram_vector` | Vectorización de un diseño propio ya elegido o alternativa vectorial evaluada | `vectorize`: **3**; `generate`: **4 / 5 / 6,5** según calidad |
| `image_background_remover` | Rescatar una imagen aprobada cuyo fondo impide utilizarla | **1** por imagen; revisar pelo, huecos y objetos finos |
| `bytedance_image_upscale` | Ampliación excepcional de una ilustración aprobada | **2** tanto en el caso 2k como 4k medido |
| `topaz_image` | Evaluación excepcional cuando importe preservar un original | Costo **sin verificar**: falló la estimación. No incluirlo como gasto automático |
| `nano_banana_2_relight` | Pruebas de ambiente o iluminación de una ilustración | **2**. No sustituye luces, normales ni relighting físico en Godot |
| `outpaint` | Extender un fondo aprobado para cubrir desplazamiento de cámara | **2** en el caso medido; comprobar continuidad |
| `autosprite` | Piloto de animación 2D y alternativa de representación | **2 / 3 / 14** por los casos turbo/pro/max medidos |

**[doc]** Estos parámetros y precios están en [L1][L1] y [L3][L3]. **[inf]** No recomiendo utilizar todos: cada incorporación añade otra fuente de variación.

Nano Banana Pro ofrece texto legible según Google, y GPT dispone de herramientas de diseño y edición; aun así, el texto del producto se compondrá de forma determinista. La legibilidad generada no elimina errores ortográficos ni resuelve localización. [doc] [Documentación de Google][W1]; **[inf]** decisión de producción.

### 3. Consistencia de estilo y personaje

#### Hoja maestra y referencias

**[inf]** Antes de producir en volumen, aprobar:

- Una composición del protagonista y el gato dentro del entorno.
- Una referencia de material pintado y vegetación.
- Una muestra de retrato.
- Un panel e iconos representativos.
- Una paleta con funciones: entorno, personaje, interacción y texto.

Cada personaje necesita una ficha con proporción, silueta, colores, peinado, vestuario, accesorios, asimetrías y detalles que puedan simplificarse. El gato necesita marcas del pelaje y accesorios inequívocos; su identidad no debe descansar solamente en el color.

Para Nano Banana Pro empezaría con **cuatro a seis referencias seleccionadas**, aunque admita catorce: maestro corporal, rostro, vistas aprobadas y acabado. Asignaría explícitamente el papel de cada imagen. Usar el máximo no es un objetivo. **[inf]**, apoyado en [los controles de referencias][W1].

#### Biblia de prompts

Mantener estos bloques versionados:

```text
ESTILO_FIJO
IDENTIDAD_FIJA
CAMARA_DEL_ENTREGABLE
ILUMINACION_DEL_ENTREGABLE
CAMBIO_SOLICITADO
FORMATO_Y_PREPARACION
```

Ejemplo de **estilo propuesto, todavía sin aprobación**:

> Original hand-painted adventure game art with rounded, readable shapes and restrained surface detail. Characters use compact chibi proportions and clear silhouettes. Environments use muted botanical greens, mineral blues and warm earth tones; characters receive contrasting warm accents, while scientific interactions use a consistent signal color. Brushwork remains visible without photographic noise. Lighting feels soft and atmospheric. Material boundaries stay clear at gameplay scale. Preserve the approved character anatomy, costume construction and visual hierarchy.

La cámara se añade aparte para permitir hub lateral, exploración elevada, retratos y hojas de modelo. Conservar el bloque de estilo sin cambios entre generaciones deriva de la [guía local de estilización][S2]; la separación en bloques es **[inf]** para este proyecto.

En una edición, describir el cambio: «cambia únicamente la expresión a sorpresa; conserva rostro, peinado, vestuario y encuadre». Evitar volver a describir toda la escena e introducir detalles nuevos. [doc] [Guía de prompts][S1].

#### Qué no funciona de forma fiable

**[inf]**, a partir de las limitaciones de [referencias][L3] y [edición][W3]:

- Repetir solamente el nombre del personaje.
- Esperar que el servicio recuerde imágenes de trabajos anteriores sin adjuntarlas.
- Cambiar de modelo en cada variante.
- Utilizar una semilla como sustituto de identidad; varios modelos considerados ni siquiera exponen ese parámetro.
- Encadenar muchas ediciones sobre una imagen que ya se ha desviado.
- Solicitar una hoja enorme con demasiadas acciones o expresiones.
- Confiar en «no cambies nada más» sin comparar el resultado.
- Resolver una asimetría mediante espejo sin revisar sus consecuencias.
- Suponer que subir calidad corrige un diseño contradictorio.

Soul ID no entra en el pipeline inicial. Además de su orientación fotográfica, los términos de Higgsfield restringen entrenar otros modelos con sus resultados; no debe proponerse entrenar una identidad con hojas generadas sin comprobar autorización específica. [doc] [Soul ID][S6]; [términos, §5.2(iv)][W5].

### 4. Protocolo de iteración y aprobación

**[inf]** Cada recurso pasa por estas etapas:

| Etapa | Trabajo | Condición para avanzar |
|---|---|---|
| Definición | Uso, cámara, tamaño visible, referencias y límite de gasto | Existe una necesidad concreta y se conoce el contrato del modelo |
| Borrador | Dos a cuatro propuestas GPT `low/1k` | Una opción resuelve silueta, composición y contenido |
| Consolidación | Maestro con referencias; comparar alternativas solamente si hace falta | Diseño coherente y aceptado por el usuario |
| Final | Generación o edición a calidad suficiente para su tamaño de uso | No aparecen defectos relevantes en la vista de juego |
| Preparación | Recorte, alfa, tamaño, atlas, repetición o ajuste de audio | Archivo utilizable y trazable |
| Integración | Probar dentro de Godot | Se ve, responde y rinde correctamente |
| Aprobación | Presentar el recurso en contexto al usuario | Aprobación explícita registrada |

#### Borradores y calidad final

GPT `low/1k` es la opción inicial: cuatro propuestas cuestan **1 crédito**. Z Image y Soul Location son más baratos por llamada, pero su falta de entrada por referencia en este contrato limita su utilidad tras fijar un diseño. [doc] [Costos][L1]; [esquemas][L3].

**[inf]** Pasaría a calidad final cuando estén resueltos contenido, cámara, silueta e identidad. Utilizaría:

- `medium`: materiales sencillos o fondos discretos que ya funcionan.
- `high`: opción habitual para finales.
- `xhigh`: solamente si una comparación demuestra una mejora visible.
- `max`: excepción justificada para una pieza importante.

Un recurso aceptable no necesita regenerarse por estar etiquetado como borrador.

#### Lotes, reintentos y ediciones

**[inf]**

- Lotes de dos a cuatro candidatos para una decisión, seguidos de revisión.
- Recursos dependientes del maestro solamente después de aprobarlo.
- Primer error localizado: editar.
- Error de composición o identidad general: volver al maestro o rehacer el borrador.
- Dos fallos equivalentes: cambiar el enfoque, la referencia o el modelo.
- Ante timeout: consultar el trabajo existente antes de reenviar.
- Ante rechazo de contenido: revisar derechos y restricciones; no intentar eludir filtros.

Como referencia económica, cuatro borradores GPT y un final `high/1k` cuestan **2,5 créditos**. Eso permite planificar intentos sin tratar cada imagen fallida como una razón para subir calidad. [doc] [Matriz][L1].

### 5. Preparación técnica para el portátil

Los siguientes tamaños son **presupuestos iniciales propuestos**, no límites demostrados de Godot ni mediciones de esta máquina. **[inf]**

| Recurso | Derivado inicial de juego |
|---|---|
| Retrato de diálogo | 512–1024 px |
| Iconos | 64–128 px; maestro mayor si hace falta |
| Props pequeños | 128–512 px |
| Texturas de superficies | 512–1024 px |
| Capas de fondo | Hasta 2048 px por dimensión cuando el encuadre lo justifique |
| Hojas de animación | Dividir por personaje, acción o dirección; evitar atlas gigantes |

Mantener originales elegidos fuera de las carpetas que Godot importa automáticamente. Probar una escena representativa a 1280×720 antes de aumentar resolución y densidad. La viabilidad final del acabado en HD 620 continúa **sin verificar mediante ejecución**.

#### Alfa y texturas

**[inf]** Para GPT, solicitar PNG con `background=transparent`; comprobar que existe canal alfa real y que los bordes funcionan sobre distintos fondos. Para modelos sin alfa, utilizar fondo separable y reservar el eliminador solamente para resultados que merezca salvar.

Para texturas repetibles:

1. Generar superficie frontal, sin perspectiva ni iluminación direccional marcada.
2. Revisar repetición 2×2 y detalle al 100 %.
3. Desplazar media imagen para llevar la unión al centro.
4. Corregir la región problemática y conservar el resto mediante composición.
5. Revisar patrón, color y escala dentro de Godot.

La guía local de texturas incluye herramientas deterministas, pero sus dependencias no se verificaron ni instalaron. Sus afirmaciones de garantía matemática no sustituyen una prueba visual del resultado. [doc] [Pipeline local de texturas][S3].

**[inf]** Empezaría con color base y materiales sencillos. No convertiría automáticamente luminosidad pintada en relieve o normales: una sombra dibujada no demuestra geometría.

#### Interfaz y parallax

El kit debe entregar papel, bordes, pinceladas, marcos e iconos separados. Godot dispone de `NinePatchRect` para adaptar paneles conservando esquinas. [doc] [NinePatchRect][W7].

**[inf]** DotGothic16, cifras, leyendas, combos y avisos se montan en el motor. El mapa debe obedecer a las ubicaciones reales del nivel. En el hub, separar cielo, montañas, arquitectura, elementos interactivos y vegetación frontal; prever margen para el desplazamiento. La zona elevada necesita geometría y oclusiones coherentes: sus capas ilustradas no reemplazan esa estructura.

### 6. Audio con los mismos créditos

#### Música

| Modelo | 30 s | 120 s | Uso propuesto |
|---|---:|---:|---|
| `sonilo_music` | 1,88 | 7,50 | Primera opción para las cinco pistas |
| `elevenlabs_music_v2` | 1,92 | 7,68 | Comparación puntual cuando Sonilo no resuelva una pieza |
| `elevenlabs_music_v2_5` | 4,36 | 17,44 | Selección excepcional tras escuchar una mejora suficiente |

Precios **[doc]** de [L1][L1]. La superioridad musical de v2.5 sobre v2 para este estilo está **sin verificar**.

**[inf]** Propuesta de cinco pistas: título, hub, exploración, trabajo científico y descubrimiento/cierre. Aproximadamente dos minutos cada una, con reproducción en bucle.

Fijar una guía común de tempo, instrumentos, densidad, carácter armónico y energía. Describir ambient/shoegaze mediante sus rasgos sonoros; evitar pedir imitación de artistas o canciones. Probar fragmentos de 15–30 segundos antes de producir la duración completa.

Ni Sonilo ni las dos rutas ElevenLabs examinadas exponen aquí referencias de audio como control de continuidad; Sonilo recibe texto y duración. Mantener exactamente una melodía entre generaciones está **sin verificar**. [doc] [Esquemas][L3].

#### Efectos y voz

Mirelo ofrece un costo sencillo de planificar: treinta efectos de tres segundos cuestan **22,5 créditos** antes de rechazos. [doc] [Matriz][L1].

**[inf]** Distribución inicial de treinta efectos:

| Familia | Cantidad |
|---|---:|
| Movimiento y superficies | 8 |
| Objetos e interacción | 8 |
| Instrumentos y mecanismos científicos | 6 |
| Interfaz y notificaciones | 6 |
| Gato | 2 |
| **Total** | **30** |

Generar un evento por archivo, con aislamiento sonoro y longitud ajustada a su uso. Variaciones pequeñas pueden derivarse localmente cuando resulten convincentes.

Para voz, reservar **0 / 10 / 15 créditos** según escenario. Son provisiones: costo por línea y duración **sin verificar**. El esquema Inworld incluye voces españolas; habría que probar pronunciación y consistencia antes de ampliar el uso. Qwen no incluye `es` en el selector de idioma del archivo disponible. [doc] [Parámetros][L3].

El costo predeterminado de Seed Audio es **0,1**, pero no demuestra un precio por segundo ni garantiza una duración concreta. Puede evaluarse en un piloto, sin reemplazar con esa cifra la planificación de voz o efectos. [doc] [Costos][L2]; [esquema][L3].

Godot admite WAV, Ogg Vorbis y MP3. WAV tiene menor exigencia de reproducción; Ogg reduce tamaño a cambio de más procesamiento. [doc] [Importación de audio][W8]. **[inf]** Recomiendo WAV para efectos cortos y evaluar Ogg o MP3 para música, con pocos streams simultáneos. Conservar originales y preparar bucles, entradas y salidas con ffmpeg.

### 7. Video: cuándo compensa

| Uso | Evaluación propuesta |
|---|---|
| Tráiler | Capturar primero gameplay real. Generación solamente para planos complementarios claramente presentados como tales |
| Cinemática | Opcional tras cerrar diseño y guion; una viñeta ilustrada con movimiento de cámara puede ser suficiente |
| VFX convertido a sprites | Prueba limitada para humo, energía o fenómenos abstractos; comprobar cámara fija, alfa y continuidad |
| Fondo animado | Preferir capas y movimientos controlados en Godot; video solamente si aporta algo que esas piezas no resuelven |
| Animación habitual de personajes | Priorizar rig 3D o evaluar `autosprite`; el video común no garantiza escala, pies ni direcciones estables |

Todo lo anterior es **[inf]**.

| Modelo | Caso predeterminado documentado | Créditos |
|---|---|---:|
| `seedance1_5` | 4 s, 720p | 4,8 |
| `seedance_2_0_mini` | 5 s, 720p | 5 |
| `kling3_0_turbo` | 5 s, 720p | 7,5 |
| `seedance_2_5` | 5 s, 720p, texto a video | 35 |

**[doc]** [Costos][L1] y [parámetros][L3]. Son esos casos concretos, no tarifas universales por segundo. El intento de cotizar Seedance 2.5 con referencias en modo `t2v` falló: para referencias corresponde revisar `omni_reference` y cotizarlo por separado.

Un piloto y una corrección con Seedance 1.5 suman **9,6 créditos**, bajo las condiciones medidas. Los escenarios asignan video **0 / 15 / 30**; cualquier cotización distinta debe caber dentro de ese límite. **[inf]**

Para `autosprite`, comenzar con turbo, tamaño 256 y pocos fotogramas útiles. Los casos locales muestran igual precio entre varios tamaños y cantidades de fotogramas, pero eso no justifica producir el atlas mayor. El gato debe usar `is_humanoid=false`. La continuidad y correspondencia con la cámara elevada deben probarse. [doc] [Matriz][L1]; [esquema][L3].

### 8. Tres escenarios para 1000 créditos

#### Alcance común

**[inf]** Los tres contemplan:

- Ocho personajes: protagonista, gato y seis NPC.
- Maestro, hoja de vistas, hoja de expresiones y retrato por personaje.
- Un hub lateral y una zona elevada, con conceptos, capas ambientales, cielos y ocho materiales base.
- Cuarenta diseños de props y sus recursos 2D necesarios.
- Kit de interfaz con aproximadamente 24 iconos, ocho piezas estructurales y estados derivados.
- Logotipo, mapa y hasta tres ilustraciones de carga.
- Cinco pistas de unos 120 segundos y treinta efectos.

**No implica cuarenta mallas distintas ni ocho personajes ya riggeados.** Esta tarea presupuesta el arte 2D y reserva una cantidad para la puerta 3D. La integración jugable completa continúa dependiendo de esa validación.

#### Desglose

Todas las cifras son **créditos máximos asignados [inf]**, calculados a partir de [L1][L1] y [L2][L2]. Voz, modo vectorial y trabajos 3D no cotizados conservan carácter provisional.

| Partida | Conservador | Equilibrado | Ambicioso |
|---|---:|---:|---:|
| Exploración y biblia visual | 12 | 20 | 25 |
| Ocho personajes: maestros, vistas, expresiones y retratos | 70 | 110 | 125 |
| Hub, zona, materiales, cielos y capas | 50 | 70 | 90 |
| Cuarenta props | 70 | 85 | 100 |
| Iconos y kit de interfaz | 35 | 50 | 60 |
| Logotipo vectorial: provisión | 10 | 12 | 15 |
| Mapa y viñetas de carga | 15 | 25 | 35 |
| Alfa, ediciones, ampliaciones y otras utilidades | 15 | 25 | 30 |
| Piloto de animación 2D | 12 | 16 | 20 |
| Cinco pistas musicales | 50 | 75 | 100 |
| Treinta efectos | 30 | 40 | 45 |
| Voz: provisión | 0 | 10 | 15 |
| Video opcional | 0 | 15 | 30 |
| **Subtotal de producción 2D, audio y pruebas** | **369** | **553** | **690** |
| **Reserva específica para transición a 3D** | **160** | **160** | **160** |
| **Contingencia general** | **471** | **287** | **150** |
| **Total** | **1000** | **1000** | **1000** |

El conservador conserva más saldo para resolver incertidumbres. El equilibrado permite vistas individuales y más correcciones. El ambicioso incrementa acabado y experimentación; conviene solamente después de validar el pipeline. **[inf]**

#### Comprobaciones de las partidas principales

**Personajes conservadores: 70 créditos.**

| Operación | Cálculo |
|---|---:|
| Ocho maestros Nano Banana Pro | `8 × 2 = 16` |
| Ocho hojas conjuntas de vistas | `8 × 2 = 16` |
| Ocho hojas de expresiones GPT high/1k | `8 × 1,5 = 12` |
| Ocho retratos GPT high/1k | `8 × 1,5 = 12` |
| Ocho borradores GPT low/1k | `8 × 0,25 = 2` |
| Hasta ocho ediciones GPT high/1k | `8 × 1,5 = 12` |
| **Total** | **70** |

El equilibrado añade **32 vistas Jutsu a 1k/1.5k: 40 créditos**, para llegar a 110. Su uso depende de aprobar el piloto; si no conserva el diseño, ese dinero queda disponible para otra solución. **[inf]**, precios [L1][L1].

**Props conservadores: 70 créditos.** Cuarenta borradores a 0,25 y cuarenta finales a 1,5: `10 + 60`. Las hojas de catálogo se montan localmente. Las correcciones adicionales salen de utilidades o contingencia.

**Música:**

| Escenario | Plan de intentos | Costo calculado | Reserva |
|---|---|---:|---:|
| Conservador | Cinco pruebas Sonilo de 15 s y cinco finales de 120 s | 42,20 | 50 |
| Equilibrado | Diez pruebas Sonilo de 30 s y hasta siete versiones de 120 s para seleccionar cinco | 71,30 | 75 |
| Ambicioso | Ocho pruebas ElevenLabs v2.5 de 30 s, dos finales v2.5 de 120 s, tres pruebas Sonilo de 15 s y tres finales Sonilo de 120 s | 95,08 | 100 |

Estos son **planes de intentos [inf]**, no tasas de éxito garantizadas. Si la licencia de la ruta intermediaria no queda documentada, las pruebas no pasan a publicación.

**Efectos:** el mínimo medido para treinta archivos de tres segundos es 22,5. Las asignaciones de 30, 40 y 45 permiten correcciones progresivamente mayores.

#### Reserva 3D y alternativa con sprites

La matriz registra **9 créditos** para Tripo H3.1 imagen a 3D en el caso predeterminado y **6** para Meshy Remesh. Un ejemplo de utilización sería:

`8 personajes × 9 + 4 props seleccionados × 9 + 2 remesh × 6 = 120`

Los 40 restantes de esa reserva no demuestran que alcance para rigging y animación: esos costos están **sin verificar**. Tampoco garantizan mallas utilizables. [doc] [Matriz][L1]; **[inf]** ejemplo de asignación.

Si se aprueba una alternativa íntegramente de sprites, ocho personajes con cinco direcciones, dos acciones y turbo implican **80 llamadas = 160 créditos**; dos acciones laterales adicionales por personaje sumarían **32**, para un total base de **192**, antes de rechazos. Las direcciones reflejadas requieren revisar asimetrías. **[inf]**, usando el costo medido de `autosprite` [L1][L1].

Ese cambio exige redistribuir la reserva 3D y contingencia; no debe añadirse silenciosamente al presupuesto existente.

### 9. Derechos comerciales y restricciones

#### Higgsfield

La ayuda oficial confirma el uso comercial de generaciones en productos y trabajo para clientes. El contrato mantiene los derechos de resultados exportados después de cancelar y permite transferirlos o sublicenciarlos. No garantiza exclusividad u originalidad. [doc] [Ayuda comercial][W9]; [términos, §4.4][W5].

El servicio conserva permisos de procesamiento y contempla entrenamiento con contenido del usuario; la privacidad del contenido no debe confundirse con exclusión del entrenamiento. [doc] [§§4.3–4.4][W5].

Entre las restricciones relevantes figuran infracción de derechos, abuso de menores, suplantación, elusión de filtros y presentación engañosa de resultados como humanos. [doc] [§5][W5].

#### Proveedores terceros

La siguiente tabla distingue las condiciones públicas del proveedor de la cobertura específica de Higgsfield. **No se encontraron los contratos privados entre las empresas; su alcance está sin verificar.**

| Proveedor | Condición pública verificada | Consecuencia para el proyecto |
|---|---|---|
| OpenAI | El acuerdo comercial atribuye al cliente los derechos sobre resultados, dentro de lo permitido legalmente; exige derechos sobre entradas y cumplimiento de políticas. [doc] [Acuerdo][W10] | No demuestra por sí solo la cobertura contractual particular de cada alias de Higgsfield |
| Google / Nano Banana | Google no reclama propiedad del contenido generado; exige cumplir leyes y su política de usos prohibidos. [doc] [Términos][W11] [Política][W12] | Conservar referencias autorizadas y señales de procedencia |
| BFL / FLUX | Permite utilización comercial de resultados bajo sus términos y política. [doc] [Términos][W13] [Política][W14] | No confundir licencia del servicio alojado con licencias para ejecutar pesos localmente |
| Recraft | Sus términos API contemplan propiedad y uso comercial de resultados; prohíben utilizarlos para entrenar IA. El acceso MCP ligado a una cuenta sigue reglas del plan correspondiente. [doc] [Developer Terms][W15] | Usar la documentación de la ruta real; no asumir condiciones del plan gratuito |
| Ideogram | Sus términos permiten uso comercial y no reclaman propiedad de los resultados; exige respetar derechos y políticas. [doc] [Términos][W16] [Política][W17] | Revisar también su acuerdo API si interviene una integración |
| ByteDance / Seedream / Seedance y utilidades | Se localizaron términos y políticas oficiales, pero no se recuperó un cuerpo completo suficiente para verificar esta integración. [doc] [Términos AI][W18] | Derechos específicos y restricciones de la ruta: **sin verificar** |
| Sonilo | Distingue licencias de web y API; permite ciertos usos comerciales y videojuegos según modalidad y elegibilidad. [doc] [Licencia][W19] [Términos][W20] | Documentar cobertura de la generación efectuada mediante Higgsfield |
| Mirelo | Sus términos atribuyen derechos que puedan surgir en resultados al usuario, sujetos al plan y política; el uso comercial depende del acceso contratado. [doc] [Términos][W21] | La cobertura concreta del intermediario permanece **sin verificar** |
| ElevenLabs Music | Los derechos dependen del plan, tipo de videojuego y autorización del distribuidor del modelo. [doc] [Music Terms][W22] | No trasladar automáticamente las condiciones de una suscripción directa a Higgsfield |
| Topaz y otras utilidades | Condiciones específicas de cada integración no verificadas | No aprobarlas como paso obligatorio hasta documentarlas |

Para OpenAI se tomó la política de **29-10-2025** como referencia vigente al corte: la página principal consultada anunciaba otra con entrada en vigor el **20-11-2026**, posterior a este informe. [doc] [Versión aplicable consultada][W23].

#### Música: diferencias que afectan la publicación

**Sonilo.** Sus términos de octubre de 2026 incluyen videojuegos indie desde Pro en la ruta web y distinguen la API. La definición web utiliza ingresos y financiación combinados inferiores a USD 200 000 en doce meses. La licencia pública excluye distribuir las pistas como lanzamientos en servicios musicales; editar o poner en bucle no amplía derechos. **[doc]** [Licencia][W19]; [términos][W20]. La modalidad exacta aplicable a Higgsfield sigue **sin verificar**.

**ElevenLabs.** Los términos del 9-10-2026 separan *Indie Game* de *Studio Game*. Para la primera categoría establecen menos de USD 500 000 acumulados por el juego y menos de USD 1 millón de ingresos anuales por juegos de la entidad, con las reglas de cálculo indicadas en el contrato. Si deja de cumplir, existe un plazo de 60 días para ajustar licencia o uso. La reventa del modelo requiere autorización escrita. **[doc]** [Music Terms][W22].

**[inf]** Antes de publicar cada pista, registrar permiso para incluirla en el juego, distribuir el juego, editarla, usarla en el tráiler y, por separado, lanzar una banda sonora. Permiso de uso comercial no significa permiso para todas esas modalidades.

### 10. Plantilla de registro de generación

**[inf]** Una entrada por trabajo enviado; cada resultado debe tener veredicto propio. La cotización y el cargo real se registran por separado.

```yaml
id: GEN-0001
asset_id: personaje_protagonista_maestro
fecha_hora: "AAAA-MM-DDThh:mm:ss-05:00"
responsable: ""
entregable: ""
uso_previsto: ""
version_estilo: estilo_v01
version_identidad: protagonista_v01

modelo:
  job_type: ""
  nombre_mostrado: ""
  proveedor_declarado: ""
  version_o_alias_verificado: ""
  fuente_del_contrato: ""
  fecha_verificacion: ""

parametros:
  quality: ""
  resolution: ""
  aspect_ratio: ""
  background: ""
  output_format: ""
  batch_size: 1
  otros: {}
  ajustes_aplicados_por_servicio: {}
# Omitir parámetros no admitidos; no enviarlos como valores vacíos.

prompt:
  completo: |
    ...
  cambio_solicitado: ""
  hash_del_prompt: ""

referencias:
  - archivo_o_id: ""
    sha256: ""
    funcion: "identidad | estilo | camara | material"
    origen: ""
    derechos_o_permiso: ""
    version_aprobada: ""

costo:
  cotizado_creditos: null
  cotizacion_fecha: ""
  cobrado_creditos: null
  partida_presupuestaria: ""
  gasto_acumulado_del_recurso: null

trabajo:
  id: ""
  estado: ""
  error_o_rechazo: ""
  reembolso_confirmado: null

resultado:
  url_original: ""
  archivo_original: ""
  sha256_original: ""
  dimensiones_o_duracion_reales: ""
  alfa_verificado: null
  derivados: []
  operaciones_locales: []
  trabajo_padre: ""

derechos:
  ruta: "Higgsfield"
  terminos_url: ""
  fecha_de_los_terminos: ""
  evidencia_de_licencia: ""
  usos_permitidos_verificados: []
  atribucion_o_procedencia: ""
  pendiente_sin_verificar: []

revision:
  identidad: ""
  estilo: ""
  camara_y_escala: ""
  preparacion_tecnica: ""
  exactitud_cientifica_si_aplica: ""
  prueba_en_godot: ""
  defecto_principal: ""
  veredicto: "aprobar | editar | rehacer | descartar"
  proxima_accion: ""

aprobacion_usuario:
  estado: "pendiente"
  fecha: ""
  evidencia: ""
```

Conservar los resultados descartados en el registro de costos evita ocultar el gasto por recurso aprobado. El original aprobado, sus referencias, la licencia y los derivados deben poder relacionarse sin depender exclusivamente del historial remoto.

## Fuentes

Todas las fuentes utilizadas para sostener decisiones son **[doc]**. Las propuestas identificadas como **[inf]** son elaboración de este informe.

**Datos locales**

- **L1:** [Matriz de costos medida][L1].
- **L2:** [Costos predeterminados y errores][L2].
- **L3:** [Parámetros y reglas de modelos][L3].

**Guías locales leídas**

- **S1:** [`higgsfield-generate/SKILL.md`][S1] y sus referencias [modelos][S1a], [prompts][S1b], [medios][S1c], [workflows][S1d] y [diagnóstico][S1e].
- **S2:** [Sistema de diseño de juego][S2a] y [estilización][S2].
- **S3:** [Texturas][S3].
- **S4:** [Audio][S4].
- **S5:** [Tableros de referencia][S5].
- **S6:** [Soul ID][S6].
- **S7:** [Logotipo][S7a] y [concept boards][S7b].
- Guías auxiliares: [Firecrawl][S8] y [OpenAI Docs][S9].

**Documentación pública y términos**

- [W1 — Google: generación y referencias de imágenes][W1].
- [W2 — Higgsfield: GPT Image 2.6, 04-11-2026][W2].
- [W3 — BFL: edición con Kontext][W3].
- [W4 — Higgsfield: espacio 3D Jutsu, 05-09-2026][W4].
- [W5 — Higgsfield: términos, 23-10-2026][W5].
- [W6 — Godot: importación de imágenes][W6].
- [W7 — Godot: NinePatchRect][W7].
- [W8 — Godot: importación de audio][W8].
- [W9 — Higgsfield: propiedad y uso comercial][W9].
- [W10 — OpenAI: acuerdo de servicios][W10].
- [W11 — Google: términos Gemini API][W11].
- [W12 — Google: política de usos prohibidos][W12].
- [W13 — BFL: términos para desarrolladores][W13].
- [W14 — BFL: política de uso][W14].
- [W15 — Recraft: Developer Terms, 20-10-2026][W15].
- [W16 — Ideogram: términos][W16].
- [W17 — Ideogram: política de uso][W17].
- [W18 — BytePlus: términos AI; recuperación incompleta][W18].
- [W19 — Sonilo: licencia comercial][W19].
- [W20 — Sonilo: términos, 02-10-2026][W20].
- [W21 — Mirelo: términos, 19-10-2026][W21].
- [W22 — ElevenLabs: Music Terms, 09-10-2026][W22].
- [W23 — OpenAI: política de uso, revisión 29-10-2025][W23].

[L1]: <C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>
[L2]: <C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_default.md>
[L3]: <C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>
[S1]: C:/Users/guill/.agents/skills/higgsfield-generate/SKILL.md
[S1a]: C:/Users/guill/.agents/skills/higgsfield-generate/references/model-catalog.md
[S1b]: C:/Users/guill/.agents/skills/higgsfield-generate/references/prompt-engineering.md
[S1c]: C:/Users/guill/.agents/skills/higgsfield-generate/references/media-inputs.md
[S1d]: C:/Users/guill/.agents/skills/higgsfield-generate/references/workflows.md
[S1e]: C:/Users/guill/.agents/skills/higgsfield-generate/references/troubleshooting.md
[S2a]: C:/Users/guill/.agents/skills/higgsfield-websites/references/game-design-system.md
[S2]: C:/Users/guill/.agents/skills/higgsfield-websites/references/game-stylization.md
[S3]: C:/Users/guill/.agents/skills/higgsfield-websites/references/game-textures.md
[S4]: C:/Users/guill/.agents/skills/higgsfield-websites/references/game-audio.md
[S5]: C:/Users/guill/.agents/skills/higgsfield-websites/references/reference-boards.md
[S6]: C:/Users/guill/.agents/skills/higgsfield-soul-id/SKILL.md
[S7a]: C:/Users/guill/.agents/skills/higgsfield-brandkit/references/logo.md
[S7b]: C:/Users/guill/.agents/skills/higgsfield-brandkit/references/concept-boards.md
[S8]: C:/Users/guill/.codex/plugins/cache/openai-curated-remote/app-6a314a73f8ac819195b0d55e36b9c609/2.11.0/skills/firecrawl/SKILL.md
[S9]: C:/Users/guill/.codex/skills/.system/openai-docs/SKILL.md
[W1]: https://aistudio.google.com/docs/image-generation
[W2]: https://higgsfield.ai/blog/gpt-image-2-6-higgsfield
[W3]: https://docs.bfl.ml/kontext/kontext_image_editing
[W4]: https://higgsfield.ai/blog/higgsfield-3d-jutsu
[W5]: https://higgsfield.ai/terms-of-use-agreement
[W6]: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html
[W7]: https://docs.godotengine.org/en/stable/classes/class_ninepatchrect.html
[W8]: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html
[W9]: https://higgsfield.ai/creator-hub/help-center/account/who-owns-my-generations-and-can-i-use-them-commercially
[W10]: https://openai.com/policies/services-agreement/
[W11]: https://aistudio.google.com/docs/terms
[W12]: https://policies.google.com/terms/generative-ai/use-policy
[W13]: https://bfl.ai/legal/developer-terms-of-service
[W14]: https://bfl.ai/legal/usage-policy
[W15]: https://www.recraft.ai/legal/developer-terms
[W16]: https://ideogram.ai/legal/tos/
[W17]: https://ideogram.ai/legal/usage-policy/
[W18]: https://docs.byteplus.com/en/docs/legal/AI-Services-terms
[W19]: https://sonilo.com/licensing
[W20]: https://sonilo.com/terms-of-service
[W21]: https://mirelo.ai/terms
[W22]: https://elevenlabs.io/music-terms
[W23]: https://openai.com/policies/usage-policies/revisions/2025-10-29/

Aviso literal de Firecrawl sobre su cuota de investigación; no corresponde al saldo de Higgsfield:

> Insufficient credits for this connected-app request. Hosted MCP calls (from apps such as ChatGPT, Claude or Codex) spend a daily MCP credit allowance first and then your team's credits, and neither can cover this request; the allowance resets at 2026-11-13T03:58:34.314Z. To continue now, add credits or upgrade your plan at https://firecrawl.dev/pricing.