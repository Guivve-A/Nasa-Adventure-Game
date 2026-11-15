extends Node

# Capturas de diagnostico y verificacion de la habitacion (carril v2: bordes y hueco de la derecha).
# Una sola corrida de Godot saca todas las capturas (un solo turno del candado).
# Uso:
#   python -I herramientas/juego_ejecutar.py --ventana --max=600 -- --auto
#     --prueba=guion:<ruta absoluta de este archivo> --salida=<carpeta> [--momentos=dia,noche] [--encuadres=0.20,0.125]
#     [--puntos=centro,cama]

const PUNTOS := {
	"esq_fondo_izq": Vector3(-2.6, 0.0, -0.6),
	"esq_fondo_der": Vector3(2.2, 0.0, -2.3),
	"esq_frente_izq": Vector3(-2.8, 0.0, 2.2),
	"esq_frente_der": Vector3(2.0, 0.0, 2.3),
	"centro": Vector3(0.0, 0.0, 0.3),
	"baranda": Vector3(2.9, 0.0, 1.5),
	"descanso": Vector3(3.0, 0.0, 2.2),
	"cama": Vector3(-1.75, 0.0, -1.0),
	# v3: junto a la ventana del fondo (la vista del barrio, punto focal del concepto)
	"ventana": Vector3(0.1, 0.0, -1.9),
}

var p: Node


func _esperar(s: float) -> void:
	await get_tree().create_timer(s).timeout


func _libre() -> void:
	await _esperar(0.4)
	while Zonas.ocupado:
		await get_tree().process_frame
	await _esperar(0.6)


func correr(pruebas: Node) -> void:
	p = pruebas
	var salida: String = String(Juego.args.get("salida", OS.get_user_data_dir()))
	DirAccess.make_dir_recursive_absolute(salida)
	var momentos: PackedStringArray = String(Juego.args.get("momentos", "dia,noche")).split(",", false)
	var encuadres: PackedStringArray = String(Juego.args.get("encuadres", "0.20,0.125")).split(",", false)
	var nombres: PackedStringArray = String(Juego.args.get("puntos", ",".join(PUNTOS.keys()))).split(",", false)
	for momento in momentos:
		Juego.nueva_partida()
		Juego.poner_bandera("visita_libre")
		Juego.poner_bandera("hab_saludo")
		if momento == "noche":
			Juego.poner_bandera("mir_luna")
			Juego.poner_bandera("mir_linea")
			Juego.poner_bandera("hab_noche")
		# la misma zona no se recarga (ir_a solo recoloca): se olvida la actual para que se arme con las banderas nuevas
		Zonas.id_actual = ""
		var llego: bool = await Zonas.ir_a("habitacion", "inicio")
		if not p.comprobar(llego, "cap.%s.carga" % momento):
			continue
		await _libre()
		Interfaz.mostrar_hud(false)
		var z: Node3D = Zonas.actual
		var j: CharacterBody3D = Zonas.jugador
		for e in encuadres:
			var etiqueta := "normal" if float(e) >= 0.18 else "lejos"
			for n in nombres:
				if not PUNTOS.has(n):
					continue
				var pos: Vector3 = z._m(PUNTOS[n])
				j.colocar(pos + Vector3(0.0, 0.05, 0.0), Vector3(0, 0, 1))
				Zonas.companero.colocar_junto(j.global_position, Vector3(0, 0, 1))
				await _esperar(0.3)
				Zonas.camara.encuadre = float(e)
				Zonas.camara.centrar()
				await _esperar(0.5)
				var ruta := "%s/%s_%s_%s.png" % [salida, momento, etiqueta, n]
				await Interfaz.capturar(ruta)
		Interfaz.mostrar_hud(true)
	p.comprobar(true, "cap.hecho")
