extends Node

# Sonido del juego (autoload "Audio"). PROVISIONAL: la Fase 4 (diseno acustico y musica) no esta validada.
#
#   Audio.sonar("ok")                 efecto suelto. Busca primero el archivo importado res://audio/<nombre>_<zona>.ogg
#                                     (variante de la zona actual, p. ej. paso_luna), luego res://audio/<nombre>.ogg
#                                     y, si no hay archivo, el pitido sintetizado de RECETAS.
#   Audio.paso()                      un paso de la protagonista: intervalo minimo y tono algo distinto cada vez.
#                                     sonar("paso", -26.0) (asi lo llama nucleo/jugador.gd) pasa por aqui; cualquier
#                                     otro sonar("paso", x) (la iguana) suena entero con su ajuste, sin limite.
#   Audio.ambiente("luna", -18.0)     fondo en bucle res://audio/ambiente_<nombre>.ogg con fundidos; "" lo para.
#                                     Al cambiar de zona arranca solo el ambiente de esa zona, si su archivo existe.
#
# Los archivos salen del lote A1 de Higgsfield (Nasa_Game/Fase_4_Audio/Lote_A1/registro.md), convertidos con
# Nasa_Game/Fase_4_Audio/Lote_A1/convertir.py. Se cargan con load() sobre el recurso importado, nunca con
# load_from_file sobre res:// (falla en el juego exportado).

const TASA := 22050
const CARPETA := "res://audio/"
const RECETAS := {
	# nombre: [frecuencia inicial, frecuencia final, duracion, forma, volumen]
	"ok": [660.0, 990.0, 0.16, "seno", 0.5],
	"error": [220.0, 165.0, 0.22, "triangulo", 0.45],
	"pulsar": [520.0, 620.0, 0.06, "seno", 0.35],
	"pagina": [900.0, 300.0, 0.09, "ruido", 0.25],
	"paso": [140.0, 90.0, 0.05, "ruido", 0.30],
	"salto": [300.0, 520.0, 0.14, "seno", 0.35],
	"recoger": [780.0, 1320.0, 0.18, "seno", 0.45],
	"umbral": [392.0, 784.0, 0.35, "seno", 0.40],
	"logro": [523.0, 1046.0, 0.50, "arpegio", 0.45],
	"tic": [1200.0, 1200.0, 0.03, "seno", 0.25],
	"radio": [1800.0, 1400.0, 0.12, "ruido", 0.18],
}
const PASO_INTERVALO_MS := 210      # dos pasos nunca suenan mas cerca que esto
const PASO_JUGADOR_DB := -26.0      # marca del paso de la protagonista: nucleo/jugador.gd llama sonar("paso", -26.0)
# paso con archivo: volumen_db + PASO_AJUSTE_DB = unos -30 dB, cerca del golpe sintetizado de antes (paso.ogg tiene
# RMS de -22,7 dB). SIN ESCUCHAR: lo valida Guillermo de oido.
const PASO_AJUSTE_DB := -22.0
const PASO_TONO := 0.07             # variacion de tono de un paso a otro (+-7 %)
const AMBIENTE_ENTRADA := 1.6       # s de fundido al entrar
const AMBIENTE_SALIDA := 1.1        # s de fundido al salir
const AMBIENTE_ATENUADO_DB := -9.0  # el ambiente baja mientras hay un minijuego abierto

var volumen_db := -8.0
var _muestras := {}                 # nombre -> AudioStreamWAV sintetizado
var _archivos := {}                 # ruta -> AudioStream importado o null si no existe
var _voces: Array[AudioStreamPlayer] = []
var _siguiente := 0
var _ultimo_paso_ms := -100000
var reproducidos := 0               # efectos que de verdad sonaron (lo leen las pruebas)
var _azar := RandomNumberGenerator.new()
var _fondo: Array[AudioStreamPlayer] = []   # dos reproductores para el fundido cruzado
var _fondo_activo := 0
var _fondo_nombre := ""
var _fondo_base_db := -18.0
var _fondo_tween: Tween = null
var _atenuado := 0.0


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_azar.seed = 7
	for i in 6:
		var voz := AudioStreamPlayer.new()
		add_child(voz)
		_voces.append(voz)
	for i in 2:
		var f := AudioStreamPlayer.new()
		f.volume_db = -80.0
		add_child(f)
		_fondo.append(f)
	# Zonas es un autoload que se crea despues de este: se conecta en el cuadro siguiente
	_conectar_zonas.call_deferred()


func _conectar_zonas() -> void:
	var zonas: Node = get_node_or_null("/root/Zonas")
	if zonas != null and not zonas.zona_cambiada.is_connected(_al_cambiar_zona):
		zonas.zona_cambiada.connect(_al_cambiar_zona)


func _process(delta: float) -> void:
	# sin zona (menu principal) no hay ambiente; con un minijuego abierto, el ambiente se aparta
	var zonas: Node = get_node_or_null("/root/Zonas")
	if _fondo_nombre != "" and zonas != null and zonas.get("actual") == null and not bool(zonas.get("ocupado")):
		ambiente("")
	var interfaz: Node = get_node_or_null("/root/Interfaz")
	var meta := 0.0
	if interfaz != null and interfaz.get("anfitrion") != null and interfaz.anfitrion.visible:
		meta = AMBIENTE_ATENUADO_DB
	if absf(meta - _atenuado) > 0.01:
		_atenuado = move_toward(_atenuado, meta, delta * 12.0)
		if _fondo_nombre != "" and (_fondo_tween == null or not _fondo_tween.is_running()):
			_fondo[_fondo_activo].volume_db = _fondo_base_db + _atenuado


# ------------------------------------------------------------------ efectos

func sonar(nombre: String, ajuste_db: float = 0.0, tono: float = 1.0) -> void:
	if Juego.args.has("sin_sonido"):
		return
	# el paso de la protagonista (nucleo/jugador.gd llama sonar("paso", -26.0)) pasa por paso(): intervalo minimo
	# y tono variable. Cualquier otro "paso" (la iguana de la plaza) suena entero, con su ajuste y sin limite.
	if nombre == "paso" and is_equal_approx(ajuste_db, PASO_JUGADOR_DB):
		paso()
		return
	var stream: AudioStream = null
	if nombre == "paso":
		stream = _archivo_para("paso_animal")      # nombre propio si algun dia hay archivo; si no, paso.ogg
	if stream == null:
		stream = _archivo_para(nombre)
	if stream == null:
		if not RECETAS.has(nombre):
			return
		if not _muestras.has(nombre):
			_muestras[nombre] = _crear(RECETAS[nombre])
		stream = _muestras[nombre]
	_reproducir(stream, volumen_db + ajuste_db, tono)


func paso(ajuste_db: float = 0.0) -> void:
	# un paso de la protagonista: lo llama quien anima la caminata (hoy, nucleo/jugador.gd via sonar("paso", -26.0))
	if Juego.args.has("sin_sonido"):
		return
	var ahora := Time.get_ticks_msec()
	if ahora - _ultimo_paso_ms < PASO_INTERVALO_MS:
		return
	_ultimo_paso_ms = ahora
	var tono := _azar.randf_range(1.0 - PASO_TONO, 1.0 + PASO_TONO)
	var stream: AudioStream = _archivo_para("paso")
	if stream == null:
		# sin archivo: el golpecito sintetizado de siempre, muy bajo
		if not _muestras.has("paso"):
			_muestras["paso"] = _crear(RECETAS["paso"])
		_reproducir(_muestras["paso"], volumen_db + PASO_JUGADOR_DB + ajuste_db, tono)
		return
	_reproducir(stream, volumen_db + PASO_AJUSTE_DB + ajuste_db + _azar.randf_range(-1.5, 1.0), tono)


func _reproducir(stream: AudioStream, db: float, tono: float) -> void:
	var voz := _voces[_siguiente]
	_siguiente = (_siguiente + 1) % _voces.size()
	voz.stream = stream
	voz.volume_db = db
	voz.pitch_scale = tono
	voz.play()
	reproducidos += 1


func tiene_archivo(nombre: String) -> bool:
	return _archivo_para(nombre) != null


func _archivo_para(nombre: String) -> AudioStream:
	# variante de la zona actual (paso_luna) y, si no hay, el archivo general (paso)
	var zonas: Node = get_node_or_null("/root/Zonas")
	var zona := String(zonas.get("id_actual")) if zonas != null else ""
	if zona != "":
		var propio := _cargar(CARPETA + nombre + "_" + zona + ".ogg")
		if propio != null:
			return propio
	return _cargar(CARPETA + nombre + ".ogg")


func _cargar(ruta: String) -> AudioStream:
	if not _archivos.has(ruta):
		var r: AudioStream = null
		if ResourceLoader.exists(ruta):
			r = load(ruta) as AudioStream
		_archivos[ruta] = r
	return _archivos[ruta]


# ------------------------------------------------------------------ ambiente

func ambiente(nombre: String, volumen_ambiente_db: float = -18.0) -> void:
	# fondo en bucle con fundido; "" lo apaga. Si ya suena el mismo, solo ajusta el volumen.
	if Juego.args.has("sin_sonido"):
		nombre = ""
	var stream: AudioStream = null
	if nombre != "":
		stream = _cargar(CARPETA + "ambiente_" + nombre + ".ogg")
		if stream == null:
			nombre = ""
	if nombre == _fondo_nombre:
		if nombre != "":
			_fondo_base_db = volumen_ambiente_db
			_fundir(_fondo[_fondo_activo], volumen_ambiente_db + _atenuado, 0.5, false)
		return
	# sale el que sonaba
	var viejo := _fondo[_fondo_activo]
	if _fondo_nombre != "":
		_fundir(viejo, -80.0, AMBIENTE_SALIDA, true)
	_fondo_nombre = nombre
	if nombre == "":
		return
	# entra el nuevo por el otro reproductor
	_fondo_activo = 1 - _fondo_activo
	var nuevo := _fondo[_fondo_activo]
	if stream is AudioStreamOggVorbis:
		(stream as AudioStreamOggVorbis).loop = true
	elif stream is AudioStreamWAV:
		(stream as AudioStreamWAV).loop_mode = AudioStreamWAV.LOOP_FORWARD
	nuevo.stream = stream
	nuevo.volume_db = -60.0
	nuevo.play()
	_fondo_base_db = volumen_ambiente_db
	_fondo_tween = _fundir(nuevo, volumen_ambiente_db + _atenuado, AMBIENTE_ENTRADA, false)


func ambiente_actual() -> String:
	return _fondo_nombre


func _fundir(reproductor: AudioStreamPlayer, destino_db: float, segundos: float, parar: bool) -> Tween:
	var t := create_tween()
	t.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	t.set_ignore_time_scale(true)
	t.tween_property(reproductor, "volume_db", destino_db, segundos).set_trans(Tween.TRANS_SINE)
	if parar:
		t.tween_callback(reproductor.stop)
	return t


func _al_cambiar_zona(id: String) -> void:
	ambiente(id)


# ------------------------------------------------------------------ sintesis de respaldo

func _crear(receta: Array) -> AudioStreamWAV:
	var f0: float = receta[0]
	var f1: float = receta[1]
	var duracion: float = receta[2]
	var forma: String = receta[3]
	var volumen: float = receta[4]
	var n := int(duracion * TASA)
	var datos := PackedByteArray()
	datos.resize(n * 2)
	var fase := 0.0
	var semilla := 12345
	for i in n:
		var t := float(i) / float(n)
		var f := lerpf(f0, f1, t)
		if forma == "arpegio":
			# tres notas: do, mi, sol
			f = f0 * [1.0, 1.26, 1.5, 2.0][mini(int(t * 4.0), 3)]
		fase += TAU * f / float(TASA)
		var s := 0.0
		match forma:
			"triangulo":
				s = asin(sin(fase)) * 2.0 / PI
			"ruido":
				semilla = (semilla * 1103515245 + 12345) & 0x7fffffff
				s = (float(semilla) / float(0x7fffffff)) * 2.0 - 1.0
				s = s * 0.6 + sin(fase) * 0.4
			_:
				s = sin(fase)
		# ataque corto y caida suave
		var envolvente := minf(t * 30.0, 1.0) * pow(1.0 - t, 1.6)
		datos.encode_s16(i * 2, int(clampf(s * envolvente * volumen, -1.0, 1.0) * 32767.0))
	var onda := AudioStreamWAV.new()
	onda.format = AudioStreamWAV.FORMAT_16_BITS
	onda.mix_rate = TASA
	onda.stereo = false
	onda.data = datos
	return onda
