Creado en `pruebas/bench_render/`.  
`project.godot`: Godot 4.7, 1280×720 y vsync desactivado.  
`bench.tscn`: escena principal mínima.  
`bench.gd`: cuatro escenarios, mediciones y salida JSON.  
`correr_bench.py`: matriz de pruebas, timeout y registro de fallos.  
`README.md`: instrucciones y referencias oficiales de [Godot 4.7](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html).  
Desde la raíz: `py -3.13 pruebas/bench_render/correr_bench.py "C:\Godot\Godot.exe"`.  
Añade `--rapido` para ejecutar 10 corridas de 6 segundos a 720p.  
Genera `resultados.json`, `resultados.md` y registros por corrida; admite `--timeout 180`.  
Validación estática y pruebas simuladas completadas; no ejecuté Godot, instalé ni descargué nada.