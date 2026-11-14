"""Prepara un humanoide para Mixamo con Blender 5.2, sin ventana.

Uso (PowerShell, desde esta carpeta):
  & 'C:/ruta/blender.exe' -b --factory-startup --python-exit-code 1 `
    --python ./glb_a_fbx_mixamo.py -- --entrada 'C:/modelos/PER-01.glb' `
    --salida ./salidas/PER-01_mixamo.fbx --frente=-x

El frente se expresa en ejes de Blender DESPUES de importar glTF.
Sin --frente se estima por la proyeccion de los pies; no es una garantia.
Conserva la pose geometrica de entrada: no puede crear una T/A-pose de una
malla sin rig. Un rig existente se evalua en reposo y se elimina del FBX.
Salidas limitadas a la carpeta de este script y sus subcarpetas.
Codigo preparado para 5.2; SIN PROBAR EN BLENDER.
"""

import argparse
import json
import math
import os
from pathlib import Path
import struct
import sys
import tempfile
import traceback

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parent


def argumentos():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada', required=True)
    parser.add_argument('--salida', required=True)
    parser.add_argument('--frente', choices=('+x', '-x', '+y', '-y'))
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    # argparse interpreta -x como otra opcion si llega separado de --frente.
    for i in range(len(argv) - 1):
        if argv[i] == '--frente' and argv[i + 1] in ('-x', '-y'):
            argv[i:i + 2] = [f'--frente={argv[i + 1]}']
            break
    return parser.parse_args(argv)


def rutas(args):
    entrada = Path(args.entrada).expanduser().resolve(strict=True)
    salida = Path(args.salida).expanduser().resolve()
    if entrada.suffix.lower() != '.glb' or salida.suffix.lower() != '.fbx':
        raise ValueError('Se requiere entrada .glb y salida .fbx.')
    if not salida.is_relative_to(ROOT) or salida == entrada:
        raise ValueError(f'La salida debe quedar dentro de {ROOT} y ser distinta de la entrada.')
    salida.parent.mkdir(parents=True, exist_ok=True)
    return entrada, salida


def operador(op, **kwargs):
    disponibles = op.get_rna_type().properties.keys()
    faltantes = set(kwargs) - set(disponibles)
    if faltantes:
        raise RuntimeError(f'API incompatible en {op.idname()}: {sorted(faltantes)}')
    resultado = op(**kwargs)
    if 'FINISHED' not in resultado:
        raise RuntimeError(f'Operacion incompleta: {op.idname()}: {resultado}')


def limites(puntos):
    return (Vector(tuple(min(p[i] for p in puntos) for i in range(3))),
            Vector(tuple(max(p[i] for p in puntos) for i in range(3))))


def detectar_frente(puntos):
    minimo, maximo = limites(puntos)
    altura = maximo.z - minimo.z
    pies = [p for p in puntos if p.z <= minimo.z + altura * 0.08]
    tobillos = [p for p in puntos if minimo.z + altura * 0.10 <= p.z
                <= minimo.z + altura * 0.20]
    if len(pies) < 8 or len(tobillos) < 8:
        raise ValueError('No se distinguen pies/tobillos. Indique --frente explicitamente.')
    # En un bipedo de pie, los dedos suelen sobresalir mas que los talones.
    # Los cuantiles reducen el efecto de unos pocos vertices aislados.
    def cuantil(valores, q):
        valores = sorted(valores)
        return valores[round((len(valores) - 1) * q)]
    candidatos = []
    for eje, nombre in ((0, 'x'), (1, 'y')):
        base = sum(p[eje] for p in tobillos) / len(tobillos)
        bajo = cuantil([p[eje] for p in pies], 0.05)
        alto = cuantil([p[eje] for p in pies], 0.95)
        diferencia = (alto - base) - (base - bajo)
        candidatos.append((abs(diferencia), ('+' if diferencia > 0 else '-') + nombre))
    candidatos.sort(reverse=True)
    mejor, segundo = candidatos
    if mejor[0] < altura * 0.015 or mejor[0] < segundo[0] * 1.5:
        raise ValueError('Frente ambiguo por geometria de pies. Use --frente=+x/-x/+y/-y.')
    print(f'AVISO: frente estimado {mejor[1]} por saliente pies/tobillos; '
          f'puntuaciones={candidatos}. Verificar visualmente; no detecta cara ni anatomia.')
    return mejor[1]


def texturas_externas(mallas, carpeta):
    imagenes = {}
    vistos = set()
    for objeto in mallas:
        for material in objeto.data.materials:
            if material and material not in vistos and material.use_nodes:
                vistos.add(material)
                for nodo in material.node_tree.nodes:
                    if nodo.type == 'TEX_IMAGE' and nodo.image:
                        original = nodo.image
                        if original not in imagenes:
                            if not original.has_data:
                                # sin ventana, la imagen empaquetada del GLB no se carga hasta usarla:
                                # leer un pixel obliga a cargarla (probado en Blender 5.3)
                                try:
                                    original.pixels[0]
                                except Exception:
                                    pass
                            if not original.has_data or original.size[0] == 0:
                                raise ValueError(f'Textura sin pixeles: {original.name}')
                            if original.source not in {'FILE', 'GENERATED'}:
                                raise ValueError(f'Textura no soportada: {original.name}/{original.source}')
                            copia = original.copy()
                            copia.filepath_raw = str(carpeta / f'textura_{len(imagenes):03d}.png')
                            copia.file_format = 'PNG'
                            copia.save()
                            if not Path(copia.filepath_raw).is_file():
                                raise RuntimeError(f'No se pudo guardar {original.name}')
                            imagenes[original] = copia
                        nodo.image = imagenes[original]
    if not imagenes:
        raise ValueError('No hay texturas de imagen; se esperaba el material texturizado de Tripo.')
    return len(imagenes)


def contenidos_fbx(ruta):
    # Lee solo cabeceras/nombres del FBX binario; comprueba Video/Content incrustado.
    with ruta.open('rb') as f:
        if f.read(23) != b'Kaydara FBX Binary  \x00\x1a\x00':
            raise ValueError('El exportador no escribio un FBX binario valido.')
        version = struct.unpack('<I', f.read(4))[0]
        formato = '<QQQB' if version >= 7500 else '<IIIB'
        tamano = struct.calcsize(formato)
        limite = ruta.stat().st_size
        cantidad = 0

        def nodos(fin, padre=b''):
            nonlocal cantidad
            while f.tell() + tamano <= fin:
                inicio = f.tell()
                datos = f.read(tamano)
                final, numero, longitud, nombre_len = struct.unpack(formato, datos)
                if final == 0:
                    return
                if not inicio < final <= limite:
                    raise ValueError('Offsets FBX invalidos.')
                nombre = f.read(nombre_len)
                propiedades = f.tell()
                if padre == b'Video' and nombre == b'Content' and numero:
                    tipo = f.read(1)
                    if tipo == b'R' and struct.unpack('<I', f.read(4))[0] > 0:
                        cantidad += 1
                f.seek(propiedades + longitud)
                nodos(final, nombre)
                f.seek(final)
        nodos(limite)
        return cantidad


def main():
    args = argumentos()
    entrada, salida = rutas(args)
    print(f'Blender {bpy.app.version_string}; objetivo API 5.2; script SIN PROBAR EN BLENDER.')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena = bpy.context.scene
    escena.unit_settings.system = 'METRIC'
    escena.unit_settings.scale_length = 1.0
    operador(bpy.ops.import_scene.gltf, filepath=str(entrada))
    objetos = list(escena.objects)
    huesos_entrada = sum(len(o.data.bones) for o in objetos if o.type == 'ARMATURE')
    for objeto in objetos:
        objeto.animation_data_clear()
        if objeto.type == 'ARMATURE':
            objeto.data.pose_position = 'REST'
        if objeto.type == 'MESH' and objeto.data.shape_keys:
            objeto.data.shape_keys.animation_data_clear()
            for clave in objeto.data.shape_keys.key_blocks:
                clave.value = 0.0
    bpy.context.view_layer.update()
    grafo = bpy.context.evaluated_depsgraph_get()
    nuevas = []
    # Hornea en coordenadas globales: conserva UV/materiales, elimina rig y padres.
    for objeto in objetos:
        if objeto.type != 'MESH':
            continue
        evaluado = objeto.evaluated_get(grafo)
        datos = bpy.data.meshes.new_from_object(evaluado, preserve_all_data_layers=True,
                                               depsgraph=grafo)
        datos.transform(evaluado.matrix_world)
        if evaluado.matrix_world.determinant() < 0:
            datos.flip_normals()
        nuevo = bpy.data.objects.new(objeto.name + '_Mixamo', datos)
        escena.collection.objects.link(nuevo)
        nuevas.append(nuevo)
    for objeto in objetos:
        bpy.data.objects.remove(objeto, do_unlink=True)
    puntos = [v.co.copy() for o in nuevas for v in o.data.vertices]
    if not puntos or not all(math.isfinite(c) for p in puntos for c in p):
        raise ValueError('Malla vacia o con coordenadas no finitas.')
    minimo, maximo = limites(puntos)
    if maximo.z - minimo.z <= 1e-6:
        raise ValueError('Altura nula; se esperaba un bipedo vertical con +Z arriba.')
    frente = args.frente or detectar_frente(puntos)
    print(f'Frente de entrada en Blender: {frente}; destino: -Y. '
          'Se conserva la pose geometrica; no se genera una T/A-pose.')
    angulos = {'+x': -math.pi / 2, '-x': math.pi / 2, '+y': math.pi, '-y': 0}
    giro = Matrix.Rotation(angulos[frente], 4, 'Z')
    minimo, maximo = limites([giro @ p for p in puntos])
    traslado = Matrix.Translation(Vector((-(minimo.x + maximo.x) / 2,
                                         -(minimo.y + maximo.y) / 2, -minimo.z)))
    for objeto in nuevas:
        objeto.data.transform(traslado @ giro)
        for poligono in objeto.data.polygons:
            poligono.use_smooth = False
        objeto.data.update()
        if not objeto.data.uv_layers:
            raise ValueError(f'{objeto.name} no tiene UV; no se conservaria la textura.')
        if not any(m and m.use_nodes for m in objeto.data.materials):
            raise ValueError(f'{objeto.name} no tiene un material de nodos exportable.')
    bpy.ops.object.select_all(action='DESELECT')
    for objeto in nuevas:
        objeto.select_set(True)
    bpy.context.view_layer.objects.active = nuevas[0]
    triangulos = 0
    for objeto in nuevas:
        objeto.data.calc_loop_triangles()
        triangulos += len(objeto.data.loop_triangles)
    if triangulos == 0:
        raise ValueError('No hay triangulos para exportar.')
    puntos = [v.co for o in nuevas for v in o.data.vertices]
    minimo, maximo = limites(puntos)
    if abs(minimo.z) > 1e-5 or abs(minimo.x + maximo.x) > 1e-5 or abs(minimo.y + maximo.y) > 1e-5:
        raise ValueError('Fallo al centrar o apoyar en el suelo.')
    # El temporal queda dentro del area de trabajo y se elimina incluso si hay error.
    with tempfile.TemporaryDirectory(prefix='.mixamo_', dir=salida.parent) as temporal:
        carpeta = Path(temporal)
        texturas = texturas_externas(nuevas, carpeta)
        provisional = carpeta / salida.name
        operador(bpy.ops.export_scene.fbx, filepath=str(provisional), use_selection=True,
                 object_types={'MESH'}, axis_forward='-Y', axis_up='Z', global_scale=1.0,
                 apply_unit_scale=True, apply_scale_options='FBX_SCALE_UNITS',
                 use_space_transform=True, bake_space_transform=False,
                 use_mesh_modifiers=True, mesh_smooth_type='FACE', use_triangles=True,
                 bake_anim=False, path_mode='COPY', embed_textures=True)
        incrustadas = contenidos_fbx(provisional)
        if incrustadas < texturas:
            raise ValueError(f'Texturas incrustadas insuficientes: {incrustadas}/{texturas}. '
                             'Compruebe enlaces a Principled BSDF; FBX no admite nodos arbitrarios.')
        os.replace(provisional, salida)
    print('RESUMEN ' + json.dumps({
        'blender': bpy.app.version_string, 'triangulos': triangulos,
        'huesos_entrada': huesos_entrada, 'huesos_salida': 0, 'acciones_salida': 0,
        'frente_entrada': frente, 'frente_salida_blender': '-y',
        'frente_metodo': 'argumento' if args.frente else 'heuristica_pies',
        'limites_m': [list(minimo), list(maximo)], 'texturas_incrustadas': incrustadas,
        'archivos_escritos': [str(salida)], 'bytes': salida.stat().st_size,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR glb_a_fbx_mixamo: {exc}', file=sys.stderr)
        traceback.print_exc()
        # os._exit asegura codigo no cero incluso sin --python-exit-code.
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
