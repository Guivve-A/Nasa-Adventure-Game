**Consulta de todas las fuentes: 12-11-2026.** Verificación parcial: quedan pendientes la vigencia jurídica ecuatoriana y los resultados de Horizons. No guardé archivos: el entorno permite solo lectura.

1. **Banderas**

- **Ecuador:** el instructivo de Presidencia de noviembre de 2009 establece **3:2 (largo:alto)**, con medidas de **2,20 × 1,47 m**, y escudo en ambas caras. Incluye instituciones públicas y privadas. Documento primario conservado en [copia externa, §§1.1–1.2](https://www.fotw.info/misc/ec_2009.pdf). **Vigencia normativa actual: sin verificar.**
- El decreto de **1900**, arts. **2, 3 y 6**, distingue el tricolor civil y mercante **sin escudo** del pabellón con escudo para edificios nacionales, buques de guerra, fortalezas y representación diplomática. [Texto del decreto reproducido en la Biblioteca de la Universidad de Cuenca](https://biblioteca.ucuenca.edu.ec/digital/files/original/01beb7e24d02380470ab3dfe4ca56fbf1f4d5bc9.pdf). **Su conciliación jurídica actual con el instructivo de 2009: sin verificar.**
- **Resolución R-24-047:** publicada en el **R. O. 45, 21-03-2003**; el texto está fechado **25-02-2003**, no 13-03-2003. Declara oficial e intangible el diseño del escudo y obligatorio en documentos y actos públicos. **No contiene una prohibición específica de representarlo en videojuegos.** [Registro Oficial, p. 4, copia del documento primario](https://esilecstorage.s3.amazonaws.com/biblioteca_silec/REGOFORIGINAL/2003/4AEB3E0773AEBE73DA86E23431C0C30DA783ACC7.pdf).
- La restricción a particulares del instructivo, §2.3, se refiere a **documentación y tarjetas**. Extenderla a obras sería una inferencia. **Ley de Símbolos Patrios vigente y régimen específico para obras: sin verificar.** [Instructivo](https://www.fotw.info/misc/ec_2009.pdf).
- **Estados Unidos:** **4 U.S.C. §8** recomienda trato respetuoso, sin añadidos sobre la bandera ni uso publicitario; no establece una licencia específica para representarla en obras. El CRS explica que la mayoría de estas disposiciones son orientativas y carecen de mecanismos sancionadores. [Código oficial](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title4-section8&num=0&edition=prelim), [CRS R45945](https://www.congress.gov/crs-product/R45945).

2. **Disco del Apolo 11**

Texto de Ecuador atribuido a **Jose Maria Velasco Ibarra, President**, en la transcripción inglesa de NASA:

> “I express my sincere wishes for the success of the heroic young astronauts who, with sublime valor, will set foot on the Moon, dominating the laws of outer space and consecrating the grandeur of human understanding and goodwill. Best regards.”

[NASA, comunicado 69-83F, 13-07-1969, p. 18](https://www.nasa.gov/wp-content/uploads/2024/05/apollo-11-goodwill-messages.pdf).

El disco original quedó **en la superficie lunar**, en el sitio del Apolo 11, transportado en una cápsula de aluminio. **Posición exacta y estado actual: sin verificar.** [NASA, Memorial Items](https://www.nasa.gov/wp-content/uploads/static/history/alsj/a11/a11memorials.html).

3. **Luna desde Guayaquil**

**13-11-2026, 19:30 UTC−5 = 14-11-2026, 00:30 UTC.** Las consultas parametrizadas a Horizons fallaron por web y por conexión directa; no obtuve efemérides.

| Magnitud | Documento F2-02 / escena 4.2 | Veredicto |
|---|---:|---|
| Fracción iluminada | 19,0 % | **Sin verificar** |
| Altura | 31,0° | **Sin verificar** |
| Azimut | No indicado | **Sin verificar** |
| Puesta local | 21:50–22:00 | **Sin verificar** |

La consulta reproducible debe usar **COMMAND=301**, **CENTER=coord@399**, **SITE_COORD=−79.8891,−2.1894,0** —altitud asumida: **0 km**— y cantidades **4 y 10**. La puesta exige declarar horizonte, refracción y criterio de limbo. **No corresponde aprobar ni corregir las cifras existentes todavía.** [API y parámetros oficiales de JPL](https://ssd-api.jpl.nasa.gov/doc/horizons.html), [manual de Horizons](https://ssd.jpl.nasa.gov/horizons/manual.html).
---

## Verificación propia de la Luna del 13-11-2026 (Claude, 12-11-2026)

Codex no pudo consultar Horizons desde su entorno. Se consultó con `herramientas/luna_efemerides.py`, que usa la API pública de JPL Horizons con el observador en Guayaquil.

| Hora local (UTC−5) | Altura | Iluminación | Situación |
|---|---:|---:|---|
| 19:20 | 33,1° | 18,9 % | Crepúsculo astronómico |
| **19:30** | **31,0°** | **19,0 %** | Noche |
| 21:50 | 0,8° | 19,6 % | Noche |
| 22:00 | −1,4° | 19,6 % | Ya puesta |

**Veredicto:** F2-02 queda **confirmado**: 19,0 % de fase y 31,0° a las 19:30, puesta hacia las 21:54 por interpolación lineal. Es Luna creciente, a unos 402 300 km.
