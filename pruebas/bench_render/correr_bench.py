"""Ejecutor secuencial del benchmark; Python 3.13, solo biblioteca estandar."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
from typing import Any


PROJECT = Path(__file__).resolve().parent
METHODS = ("forward_plus", "mobile", "gl_compatibility")
SCENES = ("base", "hierba", "sprites", "sdfgi")
DRIVERS = {"forward_plus": "vulkan", "mobile": "vulkan", "gl_compatibility": "opengl3"}


def positive_seconds(text: str) -> float:
    value = float(text)
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError("El tiempo debe ser positivo y finito.")
    return value


def combinations(quick: bool) -> list[tuple[str, str, str]]:
    resolutions = ("1280x720",) if quick else ("1280x720", "1920x1080")
    return [
        (method, scene, resolution)
        for method in METHODS
        for scene in SCENES
        if scene != "sdfgi" or method == "forward_plus"
        for resolution in resolutions
    ]


def build_command(
    executable: Path, method: str, scene: str, resolution: str, seconds: int, output: Path
) -> list[str]:
    return [
        str(executable),
        "--path", str(PROJECT),
        "--rendering-method", method,
        "--rendering-driver", DRIVERS[method],
        "--resolution", resolution,
        "--windowed",
        "--disable-vsync",
        "--max-fps", "0",
        "--audio-driver", "Dummy",
        "--disable-crash-handler",
        "--",
        f"--escena={scene}",
        f"--segundos={seconds}",
        f"--salida={output}",
    ]


def terminate_process(process: subprocess.Popen[bytes]) -> str:
    notes = []
    if os.name == "nt":
        # Termina tambien el hijo de un ejecutable de consola de Godot.
        taskkill = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "taskkill.exe"
        try:
            killed = subprocess.run(
                [str(taskkill), "/PID", str(process.pid), "/T", "/F"],
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=5, check=False, creationflags=subprocess.CREATE_NO_WINDOW,
            )
            if killed.returncode:
                notes.append(killed.stdout.decode("utf-8", errors="replace")[-1000:])
        except (OSError, subprocess.TimeoutExpired) as error:
            notes.append(str(error))
    if process.poll() is None:
        try:
            process.kill()
        except OSError as error:
            notes.append(str(error))
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        notes.append("El proceso no confirmo el cierre tras kill().")
    return "; ".join(notes)


def log_tail(path: Path) -> str:
    try:
        with path.open("rb") as log:
            log.seek(0, os.SEEK_END)
            log.seek(max(0, log.tell() - 6000))
            return log.read().decode("utf-8", errors="replace")
    except OSError:
        return ""


def reject_nonfinite(value: str) -> None:
    raise ValueError(f"Numero JSON no finito: {value}")


def validate_result(
    data: Any, method: str, scene: str, resolution: str, seconds: int
) -> None:
    if not isinstance(data, dict):
        raise ValueError("El JSON de Godot no es un objeto.")
    version = data.get("godot_version", {})
    if not isinstance(version, dict) or (version.get("major"), version.get("minor")) != (4, 7):
        raise ValueError("La corrida no uso Godot 4.7.")
    if data.get("schema_version") != 1 or data.get("scene") != scene:
        raise ValueError("Esquema o escena inesperados.")
    # En la Intel HD 620, Compatibility cae a ANGLE (opengl3_angle): se acepta y queda anotado en la tabla.
    if data.get("rendering_method") != method or data.get("rendering_driver") not in (DRIVERS[method], DRIVERS[method] + "_angle"):
        raise ValueError("El metodo o controlador efectivo difiere del solicitado (fallback).")
    width, height = map(int, resolution.split("x"))
    if data.get("resolution") != {"width": width, "height": height} or data.get("resolution_changed") is not False:
        raise ValueError("La resolucion efectiva difiere de la solicitada o cambio durante la corrida.")
    if data.get("vsync_mode") != 0:
        raise ValueError("Godot no confirmo vsync desactivado.")
    if data.get("requested_seconds") != seconds or data.get("warmup_seconds") != 3:
        raise ValueError("Duracion o calentamiento inesperados.")
    expected_effects = dict.fromkeys(("sdfgi", "ssao", "glow"), scene == "sdfgi")
    if data.get("effects") != expected_effects:
        raise ValueError("Los efectos de Environment difieren de la escena solicitada.")
    positive = (
        "frames", "measured_seconds", "fps_mean", "fps_1pct_low",
        "frame_time_mean_ms", "frame_time_max_ms",
    )
    nonnegative = (
        "draw_calls_mean", "draw_calls_max", "primitives_mean", "primitives_max",
        "video_memory_mean_bytes", "video_memory_max_bytes", "video_memory_last_bytes",
    )
    for field in positive + nonnegative:
        value = data.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"Metrica ausente o no finita: {field}")
        if value < 0 or (field in positive and value == 0):
            raise ValueError(f"Metrica fuera de rango: {field}")
    if data["measured_seconds"] < seconds:
        raise ValueError("La medicion termino antes del tiempo solicitado.")
    for field in ("adapter_name", "graphics_api_version"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"Identificacion grafica ausente: {field}")


def run_one(
    executable: Path, method: str, scene: str, resolution: str,
    seconds: int, timeout: float, run_dir: Path,
) -> dict[str, Any]:
    stem = f"{method}_{scene}_{resolution}"
    output = run_dir / f"{stem}.json"
    log_path = run_dir / f"{stem}.log"
    command = build_command(executable, method, scene, resolution, seconds, output)
    record: dict[str, Any] = {
        "requested_method": method, "requested_driver": DRIVERS[method],
        "scene": scene, "requested_resolution": resolution,
        "requested_seconds": seconds, "timeout_seconds": timeout,
        "command": command, "output": str(output.relative_to(PROJECT)),
        "log": str(log_path.relative_to(PROJECT)),
        "status": "error", "returncode": None, "error": None, "result": None,
    }
    started = time.monotonic()
    process = None
    try:
        with log_path.open("wb") as log:
            process = subprocess.Popen(
                command, cwd=PROJECT, stdin=subprocess.DEVNULL,
                stdout=log, stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            try:
                record["returncode"] = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                record["status"] = "timeout"
                record["error"] = f"Tiempo limite excedido ({timeout:g} s)."
                cleanup_note = terminate_process(process)
                record["returncode"] = process.returncode
                if cleanup_note:
                    record["error"] += " " + cleanup_note
        if record["status"] != "timeout":
            if record["returncode"] != 0:
                raise ValueError(f"Godot termino con codigo {record['returncode']}.")
            if not output.is_file():
                raise ValueError("Godot termino sin producir el JSON.")
            with output.open(encoding="utf-8") as source:
                data = json.load(source, parse_constant=reject_nonfinite)
            record["result"] = data
            validate_result(data, method, scene, resolution, seconds)
            record["status"] = "ok"
    except (OSError, ValueError) as error:
        record["error"] = str(error)
    except BaseException:
        # No deja Godot abierto si el usuario interrumpe el ejecutor.
        if process is not None and process.poll() is None:
            terminate_process(process)
        raise
    finally:
        record["wall_seconds"] = time.monotonic() - started
        if record["status"] != "ok":
            record["log_tail"] = log_tail(log_path)
    return record


def cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def make_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Resultados del benchmark de renderizado", "",
        f"Fecha UTC: {report['started_utc']}. Python: {report['python_version']}.", "",
        "Forward+ y Mobile: Vulkan. Compatibility: OpenGL 3. Calentamiento: 3 s.",
        "FPS 1 %: inversa del tiempo medio del 1 % de cuadros mas lentos (redondeo hacia arriba).",
        "Tiempos de cuadro: reloj real de CPU entre callbacks, no tiempo exclusivo de GPU.",
        "Draw calls y primitivas: media por cuadro. Memoria: maximo reportado por el motor, en MiB.",
        "Un contador 0 puede indicar informacion no disponible; la HD 620 usa memoria compartida.", "",
        "| Metodo solicitado | Escena | Resolucion | Estado | FPS medio | FPS 1 % | Cuadro medio ms | Cuadro max ms | Draw calls | Primitivas | Memoria MiB | Metodo efectivo | Controlador | Adaptador | API | Error |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for run in report["runs"]:
        result = run.get("result")
        details = result if isinstance(result, dict) else {}
        metrics = ["—"] * 7
        if run["status"] == "ok":
            metrics = [
                f"{details['fps_mean']:.2f}", f"{details['fps_1pct_low']:.2f}",
                f"{details['frame_time_mean_ms']:.3f}", f"{details['frame_time_max_ms']:.3f}",
                f"{details['draw_calls_mean']:.1f}", f"{details['primitives_mean']:.1f}",
                f"{details['video_memory_max_bytes'] / (1024 * 1024):.2f}",
            ]
        values = [
            run["requested_method"], run["scene"], run["requested_resolution"], run["status"],
            *metrics, details.get("rendering_method", "—"), details.get("rendering_driver", "—"),
            details.get("adapter_name", "—"), details.get("graphics_api_version", "—"),
            run.get("error") or "",
        ]
        lines.append("| " + " | ".join(map(cell, values)) + " |")
    lines.extend(["", f"JSON individuales y logs: `{report['run_directory']}`.", ""])
    return "\n".join(lines)


def write_reports(report: dict[str, Any]) -> None:
    # Sustitucion atomica de cada informe; no mezcla JSON de ejecuciones anteriores.
    for name, contents in (
        ("resultados.json", json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"),
        ("resultados.md", make_markdown(report)),
    ):
        destination = PROJECT / name
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        temporary.write_text(contents, encoding="utf-8")
        temporary.replace(destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("godot", type=Path, help="Ruta del ejecutable de Godot 4.7.")
    parser.add_argument("--rapido", action="store_true", help="Solo 1280x720 y 6 s de medicion.")
    parser.add_argument("--timeout", type=positive_seconds, default=120.0, metavar="SEGUNDOS",
                        help="Tiempo limite por corrida, incluido arranque (por defecto: 120).")
    args = parser.parse_args()
    executable = args.godot.expanduser().resolve()
    if not executable.is_file():
        parser.error(f"No existe el ejecutable: {executable}")
    seconds = 6 if args.rapido else 12
    (PROJECT / "corridas").mkdir(exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="run_", dir=PROJECT / "corridas"))
    report: dict[str, Any] = {
        "schema_version": 1, "started_utc": datetime.now(timezone.utc).isoformat(),
        "godot_executable": str(executable), "python_version": platform.python_version(),
        "platform": platform.platform(), "quick": args.rapido,
        "run_directory": str(run_dir.relative_to(PROJECT)), "runs": [],
    }
    jobs = combinations(args.rapido)
    write_reports(report)
    try:
        for index, (method, scene, resolution) in enumerate(jobs, start=1):
            print(f"[{index}/{len(jobs)}] {method} / {scene} / {resolution}", flush=True)
            record = run_one(executable, method, scene, resolution, seconds, args.timeout, run_dir)
            report["runs"].append(record)
            write_reports(report)
            print(f"  {record['status']}: {record['error'] or 'medicion guardada'}", flush=True)
    except KeyboardInterrupt:
        report["interrupted"] = True
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        write_reports(report)
        print("Interrumpido. Se conservaron las corridas completadas.", file=sys.stderr)
        return 130
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_reports(report)
    failures = sum(run["status"] != "ok" for run in report["runs"])
    print(f"Terminadas {len(jobs)} corridas; {failures} fallos. Informes: {PROJECT}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
