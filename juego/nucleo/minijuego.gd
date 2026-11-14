extends Control

# Base de todo minijuego. Cada uno vive en res://minijuegos/<id>/<id>.gd, empieza con
#   extends "res://nucleo/minijuego.gd"
# y tiene al lado su minijuego.json (titulo, instrucciones, controles, pistas y ficha del cuaderno).
#
# El anfitrion (interfaz/anfitrion.gd) pone el marco, el titulo, las instrucciones, las pistas de Orbita y la
# pantalla de resultado. El minijuego solo dibuja y juega dentro de su lienzo.
#
# Contrato:
#   _preparar()      arma los nodos y el estado inicial. El lienzo ya mide LIENZO (1120 x 520 px): usa "size".
#   _empezar()       el jugador pulso «Empezar»: arranca el juego.
#   _paso(delta)     se llama en cada cuadro mientras "activo" es true. Usa SIEMPRE delta para el tiempo
#                    (las pruebas aceleran el reloj); nunca la hora del sistema.
#   terminar(superado, puntos, detalle)   cierra la partida. "detalle" explica la causa en una frase:
#                    nunca «incorrecto», siempre el porque (regla de Orbita).
#   jugar_solo(acierta)   OBLIGATORIO para las pruebas: hace que el minijuego se juegue solo y termine,
#                    superado si acierta = true y no superado si es false, en menos de 40 s de juego.
#
# Dificultad: parametros.get("dificultad", 1) va de 1 (primera vez en la historia) a 3.
# Entradas: teclado (acciones mover_*, interactuar, saltar) y raton; todo lo que se pueda hacer con el raton
# debe poder hacerse tambien con el teclado.

signal terminado(resultado: Dictionary)

const Estilo := preload("res://interfaz/estilo.gd")
const LIENZO := Vector2(1120, 520)

var parametros: Dictionary = {}
var meta: Dictionary = {}       # contenido de minijuego.json
var activo := false
var tiempo := 0.0               # segundos de juego desde _empezar()
var dificultad := 1
var _solo := 0                  # 0 = juega la persona; 1 = solo y acierta; -1 = solo y falla


func preparar(p: Dictionary, m: Dictionary) -> void:
	parametros = p
	meta = m
	dificultad = clampi(int(p.get("dificultad", 1)), 1, 3)
	custom_minimum_size = LIENZO
	size = LIENZO
	clip_contents = true
	focus_mode = Control.FOCUS_ALL
	_preparar()


func empezar() -> void:
	activo = true
	tiempo = 0.0
	grab_focus()
	_empezar()
	if _solo != 0:
		jugar_solo(_solo > 0)


func terminar(superado: bool, puntos: float = 0.0, detalle: String = "") -> void:
	if not activo:
		return
	activo = false
	terminado.emit({"superado": superado, "puntos": puntos, "detalle": detalle, "tiempo": tiempo})


func _process(delta: float) -> void:
	if activo:
		tiempo += delta
		_paso(delta)


# ------------------------------------------------------------------ para sobrescribir

func _preparar() -> void:
	pass


func _empezar() -> void:
	pass


func _paso(_delta: float) -> void:
	pass


func jugar_solo(_acierta: bool) -> void:
	# cada minijuego lo implementa; por defecto termina sin jugar para que la prueba lo delate
	terminar(false, 0.0, "Este minijuego todavía no sabe jugarse solo.")


# ------------------------------------------------------------------ utilidades

func eje_x() -> float:
	# -1..1 con izquierda y derecha (teclado o mando)
	return Input.get_axis("mover_izquierda", "mover_derecha")


func eje_y() -> float:
	# -1..1 con abajo y arriba (arriba = +1)
	return Input.get_axis("mover_abajo", "mover_arriba")


func texto(contenido: String, tam: int = 20, color: Color = Estilo.TINTA, peso: int = 500) -> Label:
	return Estilo.texto(contenido, tam, color, peso)


func sonar(nombre: String) -> void:
	Audio.sonar(nombre)
