extends "res://nucleo/zona.gd"

# El sendero del arroyo: la escena de exploracion aprobada por Guillermo en el motor (D-015), hecha jugable.
# El centro (composicion, materiales y luz de la tarde) es el del layout aprobado, sin cambios. Lo nuevo esta
# fuera del cuadro del ancla y lo escribe herramientas/mallas/sendero_ampliacion.py:
#   - layout.json: el layout aprobado con las rutas del juego, la ampliacion y los trazados ("jugable")
#   - modelos/sendero/: suelo y hierba prolongados, agua, mosaico, muro, antena reparada y farol
# Estados: tarde (la luz aprobada) y noche (cuando ya se vio la Luna en el Mirador; provisional).
#
# La copa del flamboyan queda entre la camara y el suelo. Para no tocarla (centro aprobado), la camara no sube
# al norte de z = -1 y la salida al Mirador esta donde el sendero se pierde bajo la copa; los "muros" del layout
# cierran el paso a lo que la copa tapa. Lo mide herramientas/mallas/sendero_visibilidad.py.

const LAYOUT := "res://zonas/sendero/layout.json"
const MODELOS := "res://modelos"
const ANTENA_LISTA := "res://modelos/sendero/COL-01_apuntada.glb"
const FAROL := "res://modelos/sendero/ARQ-09.glb"

# radio de colision de cada recurso a escala 1 (medio ancho de su malla); las plantas solo frenan en el tallo
const RADIOS := {
	"TER-01_a": 0.66, "TER-01_b": 0.54, "TER-02_a": 0.36, "TER-02_b": 0.33,
	"VEG-07": 0.16, "VEG-10": 0.16, "VEG-12": 0.14,
}
const VEL_ESPANTA := 2.8          # m/s: por encima de esto la iguana se esconde (caminar son 2,0 y correr 3,6)
const DIST_ESPANTA := 3.0         # m
const DIST_VUELVE := 3.6          # m: mas lejos que esto durante 1,5 s, la iguana vuelve a su roca

var _j: Dictionary = {}           # layout.json -> "jugable": trazados y puntos de la zona
var _inst: Dictionary = {}        # id del layout -> nodo
var _noche := false
var _panel_cuerpo: StaticBody3D
var _antena_lista: Node3D
var _iguana: Node3D
var _iguana_inter: Node3D
var _iguana_pos := Vector2.ZERO
var _iguana_escala := Vector3.ONE
var _iguana_escondida := false
var _iguana_calma := 0.0
var _destellos: Array[Node3D] = []
var _t := 0.0


func _construir() -> void:
	encuadre = 0.19
	_noche = bool(Juego.bandera("mir_luna"))
	var datos: Variant = JSON.parse_string(FileAccess.get_file_as_string(LAYOUT))
	if datos is Dictionary:
		_j = (datos as Dictionary).get("jugable", {})
	var lim: Dictionary = _j.get("limites", {"x": [-1.6, 3.2], "z": [-1.0, 2.9]})
	limites = Rect2(float(lim["x"][0]), float(lim["z"][0]), float(lim["x"][1]) - float(lim["x"][0]), float(lim["z"][1]) - float(lim["z"][0]))

	# luz: la tarde aprobada, sin cambios; la noche es provisional
	luces("noche" if _noche else "tarde")
	if _noche:
		# Para los shaders aprobados la caida de un farol con la distancia es una «sombra», y dejan un 30 % de
		# luz en las sombras (D-015): cada farol sumaria ese 30 % a toda la escena. De noche se pide la sombra
		# completa (igual que en el Mirador); al cambiar de zona el nucleo devuelve el valor aprobado.
		Materiales.ajustar_parametro("sombra_proyectada", 1.0)
	var r: Dictionary = montar_layout(LAYOUT, MODELOS, ["PER-01", "PER-09", "COL-01_tripo"])
	_inst = r["instancias"]
	if _noche:
		meta["momento"] = "Noche (provisional)"
		Materiales.ajustar_parametro("moteado_fuerza", 0.0)      # sin sol no hay motas bajo el flamboyan
		_poner_faroles()

	_colisiones(datos if datos is Dictionary else {})
	_entradas_y_umbrales()
	_interactuables()


# ------------------------------------------------------------------ colisiones

func _v2(a: Array) -> Vector2:
	return Vector2(float(a[0]), float(a[1]))


func _muro(a: Vector2, b: Vector2, alto: float = 2.4, y: float = -1.0, grosor: float = 0.3) -> StaticBody3D:
	# pared invisible entre dos puntos del plano XZ
	var d := b - a
	if d.length() < 0.01:
		return null
	var c := (a + b) * 0.5
	return pared(Vector3(c.x, y + alto * 0.5, c.y), Vector3(d.length() + grosor, alto, grosor), rad_to_deg(atan2(-d.y, d.x)))


func _colisiones(datos: Dictionary) -> void:
	# suelo con relieve, cauce y terraza de la plaza baja
	if _inst.has("TER-suelo"):
		colision_de_malla(_inst["TER-suelo"])
	else:
		piso(Vector3.ZERO, Vector2(30, 26))
	# el arroyo solo se pisa desde el puente: muro por la orilla de este lado, con el hueco del puente
	for t in _j.get("orilla", []):
		var tramo: Array = t
		_muro(Vector2(float(tramo[0]), float(tramo[1])), Vector2(float(tramo[2]), float(tramo[3])))
	# puente TER-10: cuesta de entrada y tablero
	if _j.has("puente"):
		var p: Dictionary = _j["puente"]
		var ini := _v2(p["inicio"])
		var fin := _v2(p["fin"])
		var eje := _v2(p["eje"])
		var ty: float = p["tablero_y"]
		var ancho: float = float(p["medio_ancho"]) * 2.0 + 0.3
		var eje3 := Vector3(eje.x, 0.0, eje.y)
		rampa(Vector3(ini.x, -0.06, ini.y) - eje3 * 0.6, Vector3(ini.x, ty, ini.y) + eje3 * 0.06, ancho)
		rampa(Vector3(ini.x, ty, ini.y), Vector3(fin.x, ty, fin.y) + eje3 * 0.2, ancho)
	# barandas de la plaza baja (URB-09) y escalinata TER-11 bajo la baranda
	for clave in ["baranda_a", "baranda_b"]:
		if _j.has(clave):
			var b: Dictionary = _j[clave]
			_muro(_v2(b["desde"]), _v2(b["hasta"]), 1.8, -0.3)
	if _j.has("escalinata"):
		var esc: Dictionary = _j["escalinata"]
		var arriba := _v2(esc["arriba"])
		var abajo := _v2(esc["abajo"])
		rampa(Vector3(arriba.x, 0.0, arriba.y), Vector3(abajo.x, float(esc["y_abajo"]), abajo.y), float(esc["ancho"]))
	# rocas grandes y tallos de las plantas (las que estan en el cauce o en la plaza baja no hacen falta)
	for rec in datos.get("recursos", []):
		var recurso: Dictionary = rec
		var nombre: String = String(recurso["glb"]).get_file().get_basename()
		if not RADIOS.has(nombre) or not _inst.has(recurso["id"]) or float(recurso["pos"][1]) < -0.3:
			continue
		var radio: float = float(RADIOS[nombre]) * (float(recurso.get("escala", 1.0)) if nombre.begins_with("TER") else 1.0)
		columna(Vector3(float(recurso["pos"][0]), -0.1, float(recurso["pos"][2])), radio, 1.3)
	# tronco, raices altas y ramas bajas del flamboyan
	for c in _j.get("tronco", []):
		var celda: Array = c
		columna(Vector3(float(celda[0]), -0.1, float(celda[1])), 0.22, 1.3)
	# antena y panel
	if _j.has("antena"):
		var a := _v2(_j["antena"])
		columna(Vector3(a.x, -0.1, a.y), 0.5, 1.3)
	if _j.has("panel") and not Juego.bandera("sen_panel"):
		var pp := _v2(_j["panel"])
		_panel_cuerpo = pared(Vector3(pp.x, 0.15, pp.y), Vector3(1.75, 0.5, 1.4), 12.0)
	# nadie camina por donde la copa del flamboyan tapa a la protagonista
	for m in _j.get("muros", []):
		var tramo_m: Array = m
		_muro(Vector2(float(tramo_m[0]), float(tramo_m[1])), Vector2(float(tramo_m[2]), float(tramo_m[3])))
	# nadie se sale del decorado
	var cer: Dictionary = _j.get("cerco", {"x": [-5.6, 7.2], "z": [-5.6, 5.0]})
	cerco(Rect2(float(cer["x"][0]), float(cer["z"][0]), float(cer["x"][1]) - float(cer["x"][0]), float(cer["z"][1]) - float(cer["z"][0])), 3.0, -1.0)


func _poner_faroles() -> void:
	# noche provisional: faroles ARQ-09 con luz calida, sin sombra
	for f in _j.get("faroles", []):
		var p := _v2(f)
		modelo(FAROL, Vector3(p.x, -0.03, p.y))
		farol(Vector3(p.x, 1.9, p.y), Color("ffc98a"), 1.2, 5.0)
		columna(Vector3(p.x, -0.1, p.y), 0.12, 2.0)


# ------------------------------------------------------------------ entradas y umbrales

func _entradas_y_umbrales() -> void:
	var casa := _v2(_j.get("entrada_casa", [0.0, 2.55]))
	var arriba := _v2(_j.get("entrada_mirador", [1.45, -2.95]))
	var a_ciudad := _v2(_j.get("umbral_ciudad", [-0.1, 4.1]))
	var a_mirador := _v2(_j.get("umbral_mirador", [1.4, -4.4]))
	entrada("inicio", Vector3(casa.x, 0.0, casa.y), Vector3(0, 0, -1))
	entrada("casa", Vector3(casa.x, 0.0, casa.y), Vector3(0, 0, -1))
	entrada("mirador", Vector3(arriba.x, 0.0, arriba.y), Vector3(0, 0, 1))
	umbral("ACiudad", Vector3(a_ciudad.x, -0.01, a_ciudad.y), "ciudad", "sendero", "A la plaza")
	umbral("AlMirador", Vector3(a_mirador.x, -0.01, a_mirador.y), "mirador", "sendero", "Al Mirador del Faro", {
		"requiere": "sen_antena",
		"mensaje_cerrado": "La antena sigue caída. Sin ella no sabremos por dónde pasa el satélite.",
	})


# ------------------------------------------------------------------ interactuables

func _interactuables() -> void:
	for clave in ["FX-01_panel", "FX-01_antena"]:
		if _inst.has(clave):
			_destellos.append(_inst[clave])
	# panel solar COL-02: se recoge una vez
	var pp := _v2(_j.get("panel", [3.19, 0.61]))
	if Juego.bandera("sen_panel"):
		_quitar_panel()
	else:
		interactuable("Panel", Vector3(pp.x, 0.0, pp.y), "Recoger el panel solar", _usar_panel, {"radio": 1.75, "altura_marca": 0.85, "una_vez": true})
	# antena COL-01: minijuego de la ganancia
	var pa := _v2(_j.get("antena", [3.01, -0.91]))
	interactuable("Antena", Vector3(pa.x, 0.0, pa.y), "Reapuntar la antena", _usar_antena, {"radio": 1.6, "altura_marca": 1.3})
	if Juego.bandera("sen_antena"):
		_antena_reparada()
	# iguana FAU-01 sobre su roca: mirar sin espantar
	_iguana = _inst.get("FAU-01")
	_iguana_pos = _v2(_j.get("iguana", [-2.63, -0.74]))
	if _iguana != null:
		_iguana_escala = _iguana.scale
		_iguana_inter = interactuable("Iguana", Vector3(_iguana_pos.x, 0.35, _iguana_pos.y), "Observar la iguana", _usar_iguana, {"radio": 1.75, "altura_marca": 0.95})
	# el arroyo, desde el puente
	if _j.has("puente"):
		var p: Dictionary = _j["puente"]
		var punto := _v2(p["fin"]) - _v2(p["eje"]) * 0.5
		interactuable("Arroyo", Vector3(punto.x, float(p["tablero_y"]), punto.y), "Mirar el arroyo", _usar_arroyo, {"radio": 1.1, "altura_marca": 1.15})


func _quitar_panel() -> void:
	if _inst.has("COL-02") and is_instance_valid(_inst["COL-02"]):
		_inst["COL-02"].visible = false
	if _inst.has("FX-01_panel") and is_instance_valid(_inst["FX-01_panel"]):
		_inst["FX-01_panel"].visible = false
	if _panel_cuerpo != null and is_instance_valid(_panel_cuerpo):
		_panel_cuerpo.queue_free()
		_panel_cuerpo = null


func _usar_panel() -> void:
	var total := Juego.sumar("panel_solar")
	Juego.poner_bandera("sen_panel")
	Audio.sonar("recoger")
	_quitar_panel()
	# la marca "Panel" no se libera aqui: su corrutina usar() espera a esta funcion (una_vez ya la apaga)
	Interfaz.aviso("+1 panel solar (%d)" % total, 2.5)
	Juego.anotar("pegaso")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Un panel solar entero. Pegaso, el primer satélite ecuatoriano, llevaba dos de 27 cm."},
		{"quien": "Órbita", "texto": "Guárdalo: dará energía al seguidor."},
	])


func _antena_reparada() -> void:
	# la antena caida se cambia por el mismo modelo con el plato hacia el cielo
	var caida: Node3D = _inst.get("COL-01_script")
	if _inst.has("FX-01_antena") and is_instance_valid(_inst["FX-01_antena"]):
		_inst["FX-01_antena"].visible = false
	var marca := get_node_or_null("Antena")
	if marca != null:
		marca.set("texto", "Mirar la antena")
	if caida == null or _antena_lista != null:
		return
	_antena_lista = modelo(ANTENA_LISTA, caida.position, rad_to_deg(caida.rotation.y))
	if _antena_lista != null:
		caida.visible = false
	else:
		caida.rotation.y += PI      # sin el modelo nuevo: al menos cambia de rumbo


func _usar_antena() -> void:
	if Juego.bandera("sen_antena"):
		await Interfaz.decir([{"quien": "Órbita", "texto": "La antena sigue al satélite sin pasarse ni quedarse atrás. La ganancia quedó en su punto."}])
		return
	if not Juego.bandera("sen_antena_vista"):
		Juego.poner_bandera("sen_antena_vista")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "Una antena caída. La estación Quito, al pie del Cotopaxi y a 3 650 m, operó de 1957 a 1981."},
			{"quien": "Órbita", "texto": "Levantémosla. Si la ganancia es baja, el plato se atrasa; si es alta, oscila."},
		])
	var r: Dictionary = await Interfaz.abrir_minijuego("antena", {"dificultad": 1})
	if r.get("superado", false):
		Juego.poner_bandera("sen_antena")
		_antena_reparada()
		Audio.sonar("logro")
		Juego.anotar("estacion_cotopaxi")
		await Interfaz.decir([{"quien": "Órbita", "texto": "La antena ya apunta al cielo. Desde el Mirador del Faro sabremos por dónde pasa el satélite."}])
	else:
		Interfaz.aviso("La antena sigue caída. Puedes intentarlo otra vez.", 3.0)


func _usar_iguana() -> void:
	if _iguana_escondida:
		return
	if Juego.bandera("sen_iguana"):
		await Interfaz.decir([{"quien": "Órbita", "texto": "Sigue al sol sobre su roca. No la molestemos."}])
		return
	Juego.poner_bandera("sen_iguana")
	Audio.sonar("ok")
	Interfaz.aviso("Observación anotada: iguana al sol sobre la roca.", 3.0)
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Llegaste caminando y no se asustó. Para observar, primero hay que no espantar."},
	])


func _usar_arroyo() -> void:
	Juego.anotar("gravedad_lunar")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "El agua baja sola por las cascadas: la gravedad tira de ella."},
		{"quien": "Órbita", "texto": "En la Luna caería más despacio. Allá la gravedad es de 1,624 m/s², cerca de 1/6 de la de aquí."},
	])


# ------------------------------------------------------------------ vida de la zona

func _physics_process(delta: float) -> void:
	_t += delta
	for d in _destellos:
		if is_instance_valid(d) and d.visible:
			d.scale = Vector3.ONE * (1.0 + 0.12 * sin(_t * 3.0))
	var j: CharacterBody3D = Zonas.jugador
	if _iguana == null or j == null or not is_instance_valid(j):
		return
	var lejos := Vector2(j.global_position.x - _iguana_pos.x, j.global_position.z - _iguana_pos.y).length()
	var rapidez := Vector2(j.velocity.x, j.velocity.z).length()
	if not _iguana_escondida:
		if lejos < DIST_ESPANTA and rapidez > VEL_ESPANTA:
			_esconder_iguana()
	elif lejos > DIST_VUELVE:
		_iguana_calma += delta
		if _iguana_calma > 1.5:
			_mostrar_iguana()
	else:
		_iguana_calma = 0.0


func _esconder_iguana() -> void:
	_iguana_escondida = true
	_iguana_calma = 0.0
	if _iguana_inter != null:
		_iguana_inter.set("habilitado", false)
	var giro := create_tween()
	giro.tween_property(_iguana, "scale", _iguana_escala * 0.05, 0.22)
	giro.tween_callback(func() -> void: _iguana.visible = false)
	if not Juego.bandera("sen_iguana"):
		Interfaz.aviso("La iguana se escondió tras la roca. Aléjate y vuelve caminando.", 3.5)


func _mostrar_iguana() -> void:
	_iguana_escondida = false
	_iguana.visible = true
	var giro := create_tween()
	giro.tween_property(_iguana, "scale", _iguana_escala, 0.4)
	if _iguana_inter != null:
		_iguana_inter.set("habilitado", true)


func al_entrar(nombre_entrada: String) -> void:
	if not Juego.bandera("sendero_visitado"):
		Juego.poner_bandera("sendero_visitado")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "El sendero del arroyo. Los destellos cian marcan lo que se puede recoger o arreglar."},
			{"quien": "Órbita", "texto": "El Mirador del Faro queda cuesta arriba: el sendero sigue bajo la copa del flamboyán."},
		])
	elif _noche and nombre_entrada == "mirador" and not Juego.bandera("sendero_noche_visto"):
		Juego.poner_bandera("sendero_noche_visto")
		await Interfaz.decir([{"quien": "Órbita", "texto": "De noche el sendero se sigue por los faroles. La plaza queda abajo."}])


func orbita_dice() -> Array:
	if _noche:
		return [{"quien": "Órbita", "texto": "Sigue los faroles sendero abajo: la plaza queda al final."}]
	if Juego.bandera("sen_panel") and Juego.bandera("sen_antena"):
		return [{"quien": "Órbita", "texto": "Panel recogido y antena apuntada. El Mirador del Faro queda cuesta arriba."}]
	return []


func ruta_de_prueba() -> Array:
	var a_ciudad := _v2(_j.get("umbral_ciudad", [-0.1, 4.1]))
	var a_mirador := _v2(_j.get("umbral_mirador", [1.4, -4.4]))
	if _noche:
		# de noche se baja desde el Mirador hasta la plaza
		return [
			{"ir": Vector3(0.95, 0.0, -2.1)}, {"ir": Vector3(0.1, 0.0, -0.3)}, {"ir": Vector3(-0.2, 0.0, 1.5)},
			{"ir": Vector3(-0.1, 0.0, 2.9)}, {"ir": Vector3(a_ciudad.x, 0.0, a_ciudad.y)},
		]
	var pasos: Array = [{"ir": Vector3(2.2, 0.0, 2.2)}, {"ir": Vector3(1.95, 0.0, 0.75)}]
	if not Juego.bandera("sen_panel"):
		pasos.append({"usar": "Panel"})
	pasos.append({"bandera": "sen_panel"})
	pasos.append({"ir": Vector3(2.0, 0.0, -0.65)})
	pasos.append({"usar": "Antena"})
	pasos.append({"bandera": "sen_antena"})
	for p in _j.get("ruta_norte", [[0.98, -2.11], [1.35, -2.92], [1.61, -3.33]]):
		var punto: Array = p
		pasos.append({"ir": Vector3(float(punto[0]), 0.0, float(punto[1]))})
	pasos.append({"ir": Vector3(a_mirador.x, 0.0, a_mirador.y)})
	return pasos
