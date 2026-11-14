# Brief común

Trabajas en el «Proyecto NASA-Ecuador» (nombre interno), un RPG educativo en Godot 4.7.2. La raíz del repositorio es tu carpeta de trabajo. Responde y escribe en español, con tildes en los textos que ve el jugador.

Reglas fijas:

- No instales ni descargues nada. No uses Higgsfield. No uses Firecrawl ni búsqueda web: todo lo que necesitas ya está verificado en los documentos del repositorio.
- Solo puedes crear o cambiar los archivos que nombra tu tarea.
- Nada de insignias, logotipos ni emblemas de la NASA ni de misiones. Nada que sugiera respaldo de la NASA.
- La estación de rastreo de Quito (Cotopaxi) **nunca** se relaciona con el Apolo 11: no hay prueba.
- Un dato marcado «pv» (pendiente de verificar), «sin verificar» o «no se usa» en los documentos **no entra**.
- Texto corto y con cifras concretas. Los números van como en la fuente verificada, sin redondear de más.

@@TAREA id=fichas_cuaderno salida=Nasa_Game/Construccion/Tareas_Codex/informes/fichas_cuaderno.md sandbox=workspace-write timeout=40 esfuerzo=medium

Escribe el archivo `juego/datos/datos_espaciales.json`: las fichas del cuaderno del juego (datos espaciales reales que el jugador desbloquea y que también salen en las ventanas de carga). Escribe además `juego/datos/FUENTES.md`, una tabla de trazabilidad.

## Fuentes que debes leer (todas, completas)

1. `Nasa_Game/Fase_2_Narrativa/Investigacion/03a_verificacion_ecuador.md` (datos de Ecuador: confirmados, corregidos y sin verificar).
2. `Nasa_Game/Fase_2_Narrativa/Investigacion/03b_verificacion_apolo.md` (Apolo y Luna).
3. `Nasa_Game/Fase_2_Narrativa/Fase 2 - Analisis.md`: la tabla de escenas (sección 3.1), el sueño lunar (sección 4) y, sobre todo, la sección 8 «Datos: qué se usa y con qué verificación» (8.1 confirmados, 8.2 cálculos propios, 8.3 pendientes: NO entran, 8.4 no se usan: NO entran) y la «Revisión C7» del final (correcciones aplicadas).
4. `Nasa_Game/Auditoria/Investigacion/02_datos_pendientes.md` (incluye la Luna del 13-11-2026 verificada con Horizons).
5. `Nasa_Game/Propuestas/Mirador del Faro - Luna con datos reales.md` (la Luna del 12-11-2026 medida).

## Formato exacto

```json
{
  "version": 1,
  "fichas": {
    "id_en_snake_case": {
      "titulo": "Hasta 40 caracteres",
      "texto": "De 1 a 3 frases cortas, 240 caracteres como máximo, para leer en 6 segundos.",
      "fuente": "Cita breve y legible: institución y documento o año. Sin URL.",
      "sello": "Dato verificado",
      "categoria": "Ecuador",
      "verificacion": "03a E6"
    }
  }
}
```

- `sello`: uno de `Dato verificado` (fuente primaria confirmada en 03a o 03b), `Dato medido` (medido en el proyecto con JPL Horizons o NASA SVS), `Cálculo propio` (calculado en el proyecto; se dice así), `Concepto` (idea de ingeniería de control que la protagonista estudia) o `Sueño` (licencia declarada del sueño lunar).
- `categoria`: una de `Ecuador`, `Luna`, `Apolo`, `Satélites`, `Control`, `Derecho espacial`.
- `verificacion`: la fila exacta que respalda la ficha (por ejemplo `03a E6`, `03b L10`, `Horizons 12-11-2026`, `Fase 2 §8.2`). No se muestra al jugador.
- UTF-8, sin comentarios, JSON válido, sangría de 2 espacios. Los ids, sin tildes ni eñes.

## Ids obligatorios (el juego ya los referencia)

`observatorio_quito`, `cielo_15_grados`, `realimentacion`, `ganancia`, `amortiguacion`, `prealimentacion`, `chimborazo`, `pegaso`, `cubesat`, `exa_2007`, `estacion_cotopaxi`, `apolo_soyuz_1975`, `sts2_despedida`, `luna_sonriente`, `luz_cenicienta`, `terminador`, `mare_crisium`, `mar_tranquilidad`, `luna_12_noviembre`, `luna_13_noviembre`, `luna_se_mueve`, `disco_apolo11`, `acuerdos_artemisa`, `gravedad_lunar`, `masa_y_peso`, `regolito`, `herramientas_apolo11`, `bolsas_numeradas`, `muestras_apolo11`, `etapa_descenso`, `zona_75_m`, `bandera_lunar`, `tratado_espacio`, `tierra_en_cielo_lunar`, `noche_lunar`, `modulo_mando`, `regreso_seis_pasos`, `limite_2_km`, `polo_sur_celeste`.

Si alguno de esos ids no tiene un dato verificado detrás, **no lo inventes**: escribe la ficha solo con lo que sí esté verificado y dilo en tu informe. Añade además todas las fichas extra que salgan de datos confirmados (por ejemplo la historia completa de Pegaso, las 578 160 horas de la estación, la temperatura lunar), hasta unas 55 en total.

## Reglas de contenido

- Cada cifra debe aparecer igual en una fuente de la lista. Si dos documentos difieren, vale la corrección más reciente (03a, 03b o la Revisión C7).
- «Luz cenicienta», «Luna sonriente», «terminador»: explica el fenómeno en una frase y da la cifra medida si existe.
- Conceptos de control (`realimentacion`, `ganancia`, `amortiguacion`, `prealimentacion`): definiciones correctas de ingeniería, en lenguaje de primer año, con el ejemplo del seguidor de la Luna. Sello `Concepto`.
- Lo que el borrador de la historia declara ficción (el abuelo, la Dra. Vega, la Loma de las Dos Banderas) no es una ficha.
- Banderas: tono respetuoso. La bandera del Apolo 11 no se afirma en pie.

## `juego/datos/FUENTES.md`

Tabla Markdown con una fila por ficha: id, sello, fila de verificación, documento y cita textual corta (hasta 25 palabras) de la línea del documento que la respalda. Al final, la lista de datos que dejaste fuera y por qué.

## Comprobación antes de terminar

Ejecuta este control y pega su salida en el informe:

```
python -I -c "import json;d=json.load(open('juego/datos/datos_espaciales.json',encoding='utf-8'));f=d['fichas'];print(len(f));print([k for k,v in f.items() if len(v['texto'])>240 or len(v['titulo'])>40 or not v.get('fuente') or not v.get('verificacion')])"
```

Debe imprimir el número de fichas y una lista vacía.

## Informe final

Qué archivos escribiste, cuántas fichas por categoría y por sello, qué ids obligatorios quedaron incompletos y qué datos descartaste.
