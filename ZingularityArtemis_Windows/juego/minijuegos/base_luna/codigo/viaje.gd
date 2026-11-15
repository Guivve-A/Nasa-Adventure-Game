extends Node2D

# Capitulo 2: pantalla de carga animada. El cohete viaja de la Luna a Marte sobre una trayectoria de puntos.
# Si existe recursos/fondos_viaje/fondo.png (640 x 360) se usa de fondo; si no, el cielo de estrellas de la Luna.

signal llegada

const Hud := preload("hud.gd")
const DURACION := 9.0
const P0 := Vector2(112, 228)
const P1 := Vector2(300, 20)
const P2 := Vector2(528, 118)
const FRASES := [
	"El cohete deja atrás la Luna.",
	"Un viaje real a Marte dura muchos meses. En el libro, cabe en una página.",
	"Marte se acerca: prepara las banderas.",
]

var t := 0.0
var _cohete: Sprite2D
var _hud


func _ready() -> void:
	var raiz: String = (get_script() as Script).resource_path.get_base_dir().get_base_dir()
	var fondo := Sprite2D.new()
	var propio: String = raiz + "/recursos/fondos_viaje/fondo.png"
	fondo.texture = load(propio if ResourceLoader.exists(propio) else raiz + "/recursos/fondos_luna/5_polo_sur_sol_eterno/capa_0_espacio.png")
	fondo.centered = false
	fondo.z_index = -2
	add_child(fondo)
	_cohete = Sprite2D.new()
	_cohete.texture = load(raiz + "/recursos/props/cohete_4.png")
	_cohete.scale = Vector2(0.4, 0.4)
	_cohete.z_index = 2
	add_child(_cohete)
	var cam := Camera2D.new()
	cam.position = Vector2(320, 180)
	add_child(cam)
	cam.make_current()
	_hud = Hud.new()
	_hud.capitulo = "Capítulo 2 — El viaje"
	add_child(_hud)


func _punto(k: float) -> Vector2:
	return P0.lerp(P1, k).lerp(P1.lerp(P2, k), k)


func _process(delta: float) -> void:
	t += delta
	var k := clampf(t / DURACION, 0.0, 1.0)
	k = k * k * (3.0 - 2.0 * k)
	var p := _punto(k)
	_cohete.position = p
	_cohete.rotation = (_punto(minf(k + 0.01, 1.0)) - _punto(maxf(k - 0.01, 0.0))).angle() + PI * 0.5
	_hud.aviso = FRASES[mini(int(t / DURACION * FRASES.size()), FRASES.size() - 1)]
	_hud.pie = "Rumbo a Marte…"
	queue_redraw()
	if t >= DURACION:
		set_process(false)
		llegada.emit()


func _disco(c: Vector2, r: float, claro: Color, oscuro: Color, manchas: Array) -> void:
	for y in range(-int(r), int(r) + 1):
		var hw := floorf(sqrt(r * r - y * y))
		draw_rect(Rect2(c.x - hw, c.y + y, hw * 2.0, 1.0), claro)
		# lado en sombra, a la derecha, con borde escalonado
		var corte := hw * 0.25 + float((y & 1)) * 1.0
		draw_rect(Rect2(c.x + corte, c.y + y, hw - corte, 1.0), oscuro)
	for m in manchas:
		draw_circle(c + Vector2(m[0], m[1]), m[2], oscuro.lerp(claro, 0.35))


func _draw() -> void:
	_disco(Vector2(84, 258), 52.0, Color("b4b9d0"), Color("4a4e68"), [[-22, -14, 7], [-8, 16, 9], [-30, 12, 5], [-12, -30, 4]])
	_disco(Vector2(556, 100), 36.0, Color("d0703c"), Color("6e2f1c"), [[-14, -8, 6], [-6, 12, 8], [-20, 8, 3]])
	draw_rect(Rect2(548, 65, 12, 2), Color("f4e4d8"))      # casquete polar
	var k := clampf(t / DURACION, 0.0, 1.0)
	k = k * k * (3.0 - 2.0 * k)
	for i in 41:
		var q := i / 40.0
		draw_rect(Rect2(_punto(q) - Vector2(1, 1), Vector2(2, 2)), Color("62e4e0") if q <= k else Color("33405e"))
	# llama del motor
	var atras := -Vector2.from_angle(_cohete.rotation - PI * 0.5)
	for i in 5:
		draw_rect(Rect2(_cohete.position + atras * (34.0 + i * 3.0 + randf() * 3.0) - Vector2(1.5, 1.5), Vector2(3, 3)), Color("ffe08a") if i < 2 else Color("f08a5d"))
	# barra de avance
	draw_rect(Rect2(220, 330, 200, 6), Color("232a40"))
	draw_rect(Rect2(220, 330, 200.0 * clampf(t / DURACION, 0.0, 1.0), 6), Color("62e4e0"))
