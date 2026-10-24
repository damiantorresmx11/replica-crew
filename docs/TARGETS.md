# Target types

Replica Crew clones five kinds of software. The phase pipeline (recon →
architect → design → build → backend → test → diff → brand → launch → deploy)
is the same; what changes per target is the stack the architect picks, the
tools the recon and build agents use, and how the test and deploy agents run.
`replica-capabilities` decides which of these the machine can build before the
plan is made.

The clean-room rule holds for every target: rebuild **features, flows and
mechanics** from public sources and the user's own account or owned copy.
Never ship the original's code, assets, art, audio, trademarks or content.

## web (default)

Web pages and web apps. Everything in the original Replica pipeline. Default
stack: Next.js + Postgres + Tailwind. Faithful-clone mode (`clone-team`,
`clone-website`, `web-clone`) is for sites the user owns or is authorized to
copy.

## desktop

Cross-platform desktop apps. Default stack: **Tauri** (Rust shell + web UI,
small binaries) when Rust is present, else **Electron** (Node only). Native
options: .NET/WPF, or Python + Qt. The recon agent studies the app from its
public site, docs, screenshots and the user's own installed copy (menus,
windows, flows) - it does **not** decompile the binary unless the user owns it
and says so in `scope.md`. The deploy agent builds installers (`.msi`/`.dmg`/
`AppImage`) and signs them with the user's own certificates.

## android

Android apps only (the user asked to skip iOS). Default stack: **Flutter**
(one codebase, recommended) or native **Kotlin + Gradle**. Needs the Android
SDK and either an emulator or a device on `adb` to test. Recon works from the
Play listing, screenshots, the app's site and the user's own use of it. The
test agent drives an emulator; the deploy agent builds a signed `.aab` and
hands the user the Play Console steps (the user owns the developer account).

## game

2D/3D games. Default stack: a **web-canvas** engine (Phaser 2D, Three.js /
PixiJS, runs on Node alone) or **Godot** (GDScript or C#) for a native engine.
Blender for 3D assets. Recon studies mechanics, loops and systems from public
gameplay videos, wikis and the user's own play - never the game's assets or
decompiled code. The build agent writes original art, or uses open/CC assets,
or the user commissions them.

## mashup

An **original** game that blends the *mechanics* of two games (the user's
example: Minecraft's voxel building with GTA V's open-world driving and
missions). This is the clearest clean-room case and the one to be strict about:

- You rebuild **mechanics and systems** - voxel terrain, a driving model, a
  mission loop - as your own design. These are not ownable.
- You never use either game's assets, maps, characters, names, logos, music or
  code, and never load or decompile either game. Minecraft worlds, GTA models,
  the names "Minecraft" and "GTA" and their look all stay out.
- The result is a new game with its own name and art (`replica-brand`), that
  *plays* like the blend the user wants. `recon` writes one feature matrix per
  source game tagged with which mechanic comes from where; `architect` designs
  one engine that serves both; `build` makes a vertical slice (walk, place a
  block, get in a car, drive) before anything else.
- Modding an existing game you own (loading into Minecraft or GTA to change
  them) is a different thing, allowed only for a game the user owns, recorded
  in `scope.md`, and it uses that game's official mod tools, not Replica Crew's
  clean-room build.

## How a target flows through the pipeline

| phase | what changes by target |
| --- | --- |
| capabilities | picks ready targets; blocks a target the machine can't build |
| recon | sources differ: site/docs (web, desktop), Play listing (android), gameplay videos + wikis (game, mashup). Mashup writes one matrix per source game. |
| architect | stack from the table above; one engine for a mashup |
| design | web/desktop/android: tokens + components. game/mashup: art direction, HUD, not DTCG tokens |
| build | web-canvas / Godot / Flutter / Tauri instead of only Next.js; vertical slice first |
| backend | same (auth, saves, leaderboards, payments) when the target has a server |
| test | Playwright (web, Electron), emulator (android), in-engine play test (game) |
| diff | web/app: feature + layout parity. game/mashup: mechanic parity, "does it play like it" |
| brand, launch, deploy | per-store: web host, `.msi`/`.dmg`, Play `.aab`, itch.io/Steam for games |
