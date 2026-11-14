extends Node

# Sonidos PROVISIONALES generados por codigo (autoload "Audio"). La Fase 4 (diseno acustico y musica) no esta
# hecha ni validada: aqui solo hay pitidos suaves para que la interfaz y el mundo respondan.
# Uso: Audio.sonar("ok")   nombres: ok, error, pulsar, pagina, paso, salto, recoger, umbral, logro, tic, radio

const TASA := 22050
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

var volumen_db := -8.0
var _muestras := {}
var _voces: Array[AudioStreamPlayer] = []
var _siguiente := 0


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	for i in 6:
		var voz := AudioStreamPlayer.new()
		add_child(voz)
		_voces.append(voz)


func sonar(nombre: String, ajuste_db: float = 0.0) -> void:
	if not RECETAS.has(nombre) or Juego.args.has("sin_sonido"):
		return
	if not _muestras.has(nombre):
		_muestras[nombre] = _crear(RECETAS[nombre])
	var voz := _voces[_siguiente]
	_siguiente = (_siguiente + 1) % _voces.size()
	voz.stream = _muestras[nombre]
	voz.volume_db = volumen_db + ajuste_db
	voz.play()


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
