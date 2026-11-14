extends "res://nucleo/zona.gd"

# Zona de plantilla: el ejemplo minimo de una zona completa y el banco de pruebas del nucleo.
# No sale en el juego (zona.json -> "oculta": true). Copia este archivo para empezar una zona nueva.


func _construir() -> void:
	# 1. Ajustes de la zona (todos opcionales)
	encuadre = 0.18
	limites = Rect2(-4.0, -4.0, 8.0, 8.0)       # hasta donde sigue la camara, en XZ

	# 2. Luz y ambiente pintado
	luces("tarde")
	ambiente(0.7)

	# 3. Geometria: piezas low-poly con color de vertice (o modelos GLB con modelo() y montar_layout())
	var suelo := Piezas.nueva()
	Piezas.plano(suelo, Vector3.ZERO, Vector2(12, 12), Color("af795e"))
	for i in 6:
		for k in 6:
			if (i + k) % 2 == 0:
				Piezas.plano(suelo, Vector3(-5.0 + i * 2.0, 0.005, -5.0 + k * 2.0), Vector2(1.9, 1.9), Color("d09880"))
	pieza(suelo, "facetado", Vector3.ZERO, 0.0, false)

	var cosas := Piezas.nueva()
	Piezas.caja(cosas, Vector3(-2.5, 0.4, -1.5), Vector3(1.2, 0.8, 0.8), Color("836258"), 20.0, Color("f8c991"))
	Piezas.prisma(cosas, Vector3(3.0, 0.0, -2.0), 0.35, 1.4, 6, Color("998385"), 0.25)
	Piezas.esfera(cosas, Vector3(3.0, 1.75, -2.0), 0.4, Color("6d6a2b"))
	Piezas.prisma(cosas, Vector3(-3.5, 0.0, 2.5), 0.5, 0.9, 5, Color("924930"), 0.0)
	pieza(cosas)

	# 4. Colisiones: suelo, obstaculos y cerco para no salirse
	piso(Vector3.ZERO, Vector2(12, 12))
	pared(Vector3(-2.5, 0.4, -1.5), Vector3(1.2, 0.8, 0.8), 20.0)
	columna(Vector3(3.0, 0.0, -2.0), 0.4)
	columna(Vector3(-3.5, 0.0, 2.5), 0.5, 0.9)
	cerco(Rect2(-5.5, -5.5, 11.0, 11.0))

	# 5. Entradas: donde aparece la protagonista (posicion y hacia donde mira)
	entrada("inicio", Vector3(0.0, 0.0, 0.0))
	entrada("fondo", Vector3(0.0, 0.0, 3.2), Vector3(0, 0, -1))

	# 6. Umbrales: la marca cian de entrada y salida, con 2 x 2 m despejados alrededor
	umbral("AlFondo", Vector3(0.0, 0.0, -4.2), "plantilla", "fondo", "Vuelve a entrar por el fondo", {"sin_carga": true})

	# 7. Interactuables
	interactuable("Cartel", Vector3(2.0, 0.0, 1.9), "Probar el minijuego", _usar_cartel)
	var poste := Piezas.nueva()
	Piezas.caja(poste, Vector3(2.0, 0.5, 2.2), Vector3(0.08, 1.0, 0.08), Color("583f22"))
	Piezas.caja(poste, Vector3(2.0, 0.95, 2.2), Vector3(0.7, 0.4, 0.06), Color("f8c991"))
	pieza(poste)
	pared(Vector3(2.0, 0.5, 2.2), Vector3(0.7, 1.0, 0.1))


func _usar_cartel() -> void:
	var r: Dictionary = await Interfaz.abrir_minijuego("plantilla", {"dificultad": 1})
	if r.get("superado", false):
		Juego.poner_bandera("plantilla_minijuego")
		await Interfaz.decir([{"quien": "Órbita", "texto": "Señal sintonizada. Así se enlaza una zona con su minijuego."}])


func al_entrar(nombre_entrada: String) -> void:
	if nombre_entrada == "inicio" and not Juego.bandera("plantilla_saludo"):
		Juego.poner_bandera("plantilla_saludo")
		await Interfaz.decir([{"quien": "Órbita", "texto": "Esta es la zona de plantilla. Camina hasta el cartel."}])


func orbita_dice() -> Array:
	return [{"quien": "Órbita", "texto": "Aquí se prueban las piezas del mundo antes de usarlas."}]


func ruta_de_prueba() -> Array:
	return [
		{"ir": Vector3(2.0, 0.0, 1.2)},
		{"usar": "Cartel"},
		{"bandera": "plantilla_minijuego"},
	]
