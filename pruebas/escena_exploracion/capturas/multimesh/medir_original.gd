extends SceneTree

# Ejecuta la fuente original con los mismos argumentos de medicion de la escena.
func _initialize() -> void:
	call_deferred("_montar")


func _montar() -> void:
	var programa := GDScript.new()
	programa.source_code = FileAccess.get_file_as_string("res://capturas/multimesh/escena_antes.gd.txt")
	if programa.reload() != OK:
		quit(1)
		return
	root.add_child(programa.new())
