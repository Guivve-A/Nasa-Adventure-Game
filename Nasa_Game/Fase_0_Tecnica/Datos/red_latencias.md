---
tipo: datos
fase: 0
fecha: 2026-11-12
---

# Conexión desde Guayaquil hacia centros de datos

Medido el 2026-11-12 a las 02:22 (hora local) desde el portátil, por Wi-Fi, con `herramientas/red_nube.py`. La latencia es el tiempo de abrir una conexión TCP: equivale a una ida y vuelta de red. Ocho muestras por destino.

| Destino | Mínimo ms | Mediana ms | Máximo ms |
|---|---:|---:|---:|
| Miami (Vultr) | 62 | 62 | 96 |
| Atlanta (Vultr) | 74 | 74 | 77 |
| Chicago (Vultr) | 92 | 93 | 105 |
| Virginia (AWS us-east-1) | 93 | 94 | 107 |
| Nueva Jersey (Vultr) | 94 | 96 | 109 |
| Dallas (Vultr) | 95 | 99 | 109 |
| Ohio (AWS us-east-2) | 107 | 118 | 153 |
| Ciudad de México (Vultr) | 118 | 121 | 123 |
| México (AWS mx-central-1) | 128 | 130 | 136 |
| Santiago de Chile (Vultr) | 129 | 131 | 133 |
| Los Ángeles (Vultr) | 125 | 132 | 137 |
| São Paulo (AWS sa-east-1) | 149 | 153 | 157 |
| Oregón (AWS us-west-2) | 159 | 164 | 166 |
| São Paulo (Vultr) | 184 | 193 | 196 |

## Ancho de banda

| Prueba | Resultado |
|---|---|
| Bajada desde un nodo cercano de Cloudflare (25 MB) | 106 Mbps |
| Subida a Cloudflare (8 MB) | 45 Mbps |
| Bajada desde Atlanta, una conexión TCP (25 MB) | 46 Mbps |
| Bajada desde Miami, una conexión TCP (25 MB) | 10 Mbps |

## El portátil como cliente de streaming

Prueba con ffmpeg sobre dos clips sintéticos de 1920×1080 a 60 cuadros por segundo.

| Códec | Decodificación por hardware (d3d11va) | Decodificación por software |
|---|---|---|
| H.264 a 20 Mbps | 72 cuadros por segundo | 11 veces el tiempo real |
| H.265 a 15 Mbps | 62 cuadros por segundo | 3,7 veces el tiempo real |

La Intel HD 620 decodifica 1080p a 60 cuadros en los dos códecs. La cifra por hardware incluye copiar cada cuadro a memoria, cosa que un cliente de streaming no hace.

## Lectura

- El sureste de Estados Unidos es la zona más cercana: Miami y Atlanta. Sudamérica queda más lejos por red que Estados Unidos.
- La latencia de red es solo una parte. El streaming de un escritorio añade la codificación, la decodificación y la pantalla.
- Es una sola medición, de madrugada. Conviene repetirla en horario de trabajo y con cable.
