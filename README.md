# Zingularity: Artemis

An educational space-exploration adventure made in Guayaquil, Ecuador. A control-engineering student dreams of the Apollo 11 landing, wakes up wanting to understand it, and sets out with Órbita, her scientist cat, to learn how a space mission is actually designed.

**Website:** https://zingularity-artemis.vercel.app
**Download (Windows):** [latest release](https://github.com/Guivve-A/Nasa-Adventure-Game/releases/latest)

> Prototype build, November 2026. Parts of it are provisional; see [Status](#status).

## Why this game

On 20 July 1969, more than 500 million people watched the first step on the Moon on television. In Guayaquil it was 9:56 p.m. Some of the children watching became engineers and scientists because of that image.

Humanity is going back to the Moon with the Artemis program, yet most material about it reaches young people in South America in another language, about other countries, and as text rather than as an experience.

**Goal:** get young people aged 10 to 16 in South America interested in how a space mission is designed (its processes, its instruments and the Artemis program) by letting them play it.

## What you do

- **Explore** five playable locations: the bedroom workshop, Plaza de las Iguanas, the creek trail, the Lighthouse Lookout, and the Moon in a dream.
- **Play nine arcade minigames**, each built around one real idea:

| Minigame | Idea |
|---|---|
| Tracker | Closed-loop control with inertia and feedforward |
| Antenna | Tracking satellites across the sky |
| Satellite | Assembling a CubeSat |
| Telescope | Finding and focusing on the Moon |
| Timeline | Milestones of Ecuador's space history |
| Samples | Choosing the right lunar sampling tool |
| Flags | Planting a flag where there is no wind |
| Re-entry | Keeping the heat shield forward |
| Orbit | Reaching the orbit of Ecuador's Pegaso satellite |

- **Run a base on the Moon and on Mars.** Two pixel-art games, *Misión Artemis* (lunar south pole) and *Misión Artemis — Marte*, where you balance oxygen, energy, food and radiation.
- **Fill an engineering notebook** with 55 fact cards. Every card cites its source.

## Real data

- The Moon in the telescope prototype uses Lunar Reconnaissance Orbiter (LRO) textures. Its illuminated fraction was measured at 12.15 % against 12.2 % from JPL Horizons for the same instant.
- Apollo 11 dates, times and quotes were checked against primary sources.
- Data sources are listed in `juego/datos/FUENTES.md` and `Nasa_Game/Propuestas/Datos/`.

This project uses open NASA data. It is not affiliated with, sponsored by, or endorsed by NASA. "Artemis" in the title is a tribute to the program.

## Install and play

Requirements: Windows 10 or 11 (64-bit) and a Vulkan-capable graphics card. Tested on a laptop with Intel HD Graphics 620 and 8 GB of RAM. You do not need to install Godot.

1. Download `Zingularity-Artemis-Windows.zip` from the [latest release](https://github.com/Guivve-A/Nasa-Adventure-Game/releases/latest) and extract all of it.
2. Double-click `Instalar.cmd` to install (no administrator rights needed), or `Jugar.cmd` to play without installing.
3. Windows SmartScreen may warn about an unsigned program: choose **More info**, then **Run anyway**.

### Controls

| Action | Keys |
|---|---|
| Move | W A S D or arrow keys |
| Run | Shift (hold) |
| Interact / talk | E or Enter |
| Jump | Space |
| World map | M |
| Minimap | N |
| Notebook | Tab or C |
| Pause | Esc or P |
| Zoom in / out | Z and X |
| Fullscreen | F11 |

## Run from source

The game is a Godot 4.7.2 project (Mobile renderer, 1280 × 720) built entirely in GDScript.

```bash
git lfs install
git clone https://github.com/Guivve-A/Nasa-Adventure-Game.git
```

Open `juego/project.godot` in Godot 4.7.2 and press F5. Models, images and audio are stored with Git LFS, so a plain "Download ZIP" from GitHub will not include them.

## Repository layout

| Path | Contents |
|---|---|
| `juego/` | Main game: core, zones, minigames, UI, shaders and tests |
| `ZingularityArtemis_Windows/` | Unified portable Windows package (Moon and Mars) |
| `Misión Artemis/`, `Marte_Gravedad2DHD/` | The two base-building games, as standalone Godot projects |
| `landing/` | Static website deployed on Vercel |
| `herramientas/` | Python tooling: asset generation, capture, packaging, test runner |
| `Nasa_Game/` | Project vault (in Spanish): art bible, reference sheets, narrative, presentation |
| `pruebas/` | Technical prototypes, including the real-data Moon telescope |

## Tests

Tests drive the game with simulated key presses, so they exercise the same input path a player uses.

```bash
python -I herramientas/juego_ejecutar.py -- --prueba=nucleo
```

```bash
python -I herramientas/juego_ejecutar.py -- --prueba=minijuegos --ritmo=8
```

On 15 November 2026 the nine minigames passed their keyboard tests (212 checks, 0 failures).

## Status

- **Working:** the five locations, the nine minigames, the notebook, the world map, the minimap and the Windows package.
- **Provisional:** the art of the Plaza, the Lookout and the Moon, and the painted loading screens, which await final review.
- **In production:** the opening cinematic, *Un punto de luz*.
- **Known issue:** the full-story automated walkthrough currently fails at the Lookout (7 of 126 checks) because of a script error in the fireflies interaction.
- **Performance:** measured between 38 and 60 fps at 1280 × 720 on Intel HD 620, depending on the location.

## How it was made

- Art direction: hand-painted low-poly with a 2.5D finish for the main world, and pixel art for the minigames and the base games.
- Concept art, reference sheets, cinematic frames, music and sound effects were generated with AI tools and then selected and edited by the team. Cinematic images are labelled as AI recreations.
- A large part of the code was written with AI coding assistants under the team's direction and verified with automated tests.

## Team

Guillermo, Jean, Joel and Domenica. Guayaquil, Ecuador.

Jean, Joel and Domenica built the Moon and Mars base games. Guillermo built the main world, the minigames and the rest of the project.

## Credits and licenses

- Engine: [Godot Engine](https://godotengine.org/license), MIT license.
- Data: NASA Lunar Reconnaissance Orbiter and JPL Horizons.
- No license has been chosen yet for this project's own code and art. Until one is added, all rights are reserved by the team.

A Spanish version of this document is in [LEEME.md](LEEME.md).
