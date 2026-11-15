extends Node

# Mide los fps de la habitacion (de noche o de dia) ocultando una parte cada vez, para saber que cuesta.
# Mide "todo" al principio y al final para ver el ruido (hay otros agentes usando el equipo).
# Uso:
#   python -I herramientas/juego_ejecutar.py --ventana --max=400 -- --auto
#     --prueba=guion:<ruta absoluta de este archivo> [--momento=noche] [--segundos=3]
#     [--grupos=omni,omni_noche,cajas_brillo,HAB-19,HAB-18,HAB-13,HAB-12,VEG]

var p: Node


func _esperar(s: float) -> void:
	await get_tree().create_timer(s).timeout


func _medir(segundos: float) -> Array:
	await _esperar(0.8)
	var cuadros := 0
	var t0 := Time.get_ticks_usec()
	var llamadas := 0
	while Time.get_ticks_usec() - t0 < int(segundos * 1000000.0):
		await get_tree().process_frame
		cuadros += 1
		llamadas = RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)
	var dt := float(Time.get_ticks_usec() - t0) / 1000000.0
	return [float(cuadros) / dt, llamadas]


func _poner(lista: Array, visible: bool) -> void:
	for n in lista:
		if is_instance_valid(n):
			(n as Node3D).visible = visible


func correr(pruebas: Node) -> void:
	p = pruebas
	var momento: String = String(Juego.args.get("momento", "noche"))
	var segundos: float = float(Juego.args.get("segundos", "3"))
	var pedidos: PackedStringArray = String(Juego.args.get("grupos", "omni,omni_noche,cajas_brillo,HAB-19,HAB-18,HAB-13,HAB-12,VEG")).split(",", false)
	Juego.nueva_partida()
	Juego.poner_bandera("visita_libre")
	Juego.poner_bandera("hab_saludo")
	if momento == "noche":
		Juego.poner_bandera("mir_luna")
		Juego.poner_bandera("mir_linea")
		Juego.poner_bandera("hab_noche")
	Zonas.id_actual = ""
	var llego: bool = await Zonas.ir_a("habitacion", "inicio")
	if not p.comprobar(llego, "medir.carga"):
		return
	await _esperar(1.0)
	while Zonas.ocupado:
		await get_tree().process_frame
	var con_hud: Array = await _medir(segundos)
	print("MEDIDA_PARTE todo_con_hud fps=%.1f llamadas=%d" % [con_hud[0], con_hud[1]])
	Interfaz.mostrar_hud(false)
	var z: Node3D = Zonas.actual
	var cuarto: Node3D = z.get_node("Cuarto")
	var grupos := {}
	for h in cuarto.get_children():
		var clave: String = String(h.name).substr(0, 6)
		if h is MeshInstance3D:
			clave = "cajas_brillo"
		elif clave.begins_with("VEG"):
			clave = "VEG"
		grupos[clave] = (grupos.get(clave, []) as Array) + [h]
	var omni: Array = z.find_children("*", "OmniLight3D", true, false)
	grupos["omni"] = omni
	# las dos luces que solo hay de noche (lampara del banco y brillo de la cama) son las dos ultimas
	grupos["omni_noche"] = omni.slice(2) if omni.size() > 2 else []
	print("MEDIDA_PARTE omni=%d" % omni.size())
	var base: Array = await _medir(segundos)
	print("MEDIDA_PARTE todo fps=%.1f llamadas=%d" % [base[0], base[1]])
	for clave in pedidos:
		if not grupos.has(clave):
			continue
		var lista: Array = grupos[clave]
		_poner(lista, false)
		var r: Array = await _medir(segundos)
		print("MEDIDA_PARTE sin_%s n=%d fps=%.1f llamadas=%d" % [clave, lista.size(), r[0], r[1]])
		_poner(lista, true)
	var fin: Array = await _medir(segundos)
	print("MEDIDA_PARTE todo_fin fps=%.1f llamadas=%d" % [fin[0], fin[1]])
	Interfaz.mostrar_hud(true)
	p.comprobar(true, "medir.hecho")
