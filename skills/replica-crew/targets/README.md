# Targets

The eleven phases are the same for every kind of software. What changes is
where recon looks, which stack the architect picks, how build, test and diff
work, and how the result ships. `replica/scope.md` records the target; every
phase agent reads the matching file here before starting.

| target | file | typical result |
| --- | --- | --- |
| `web-app` | `web-app.md` | SaaS or web tool with accounts and data |
| `website` | `website.md` | marketing site, landing, blog, docs |
| `desktop` | `desktop.md` | Windows, macOS or Linux app |
| `android` | `android.md` | Android app (APK / AAB on Play) |
| `game` | `game.md` | an original game inspired by a genre or a game's mechanics |
| `mashup` | `mashup.md` + skill `replica-mashup` | one new product that fuses two or more sources, e.g. "Minecraft building in a GTA-style open city" |

Rules that hold for every target:

- Rebuild behaviour, never the product's property: no source code, binaries,
  decompiled or extracted files, assets, names, logos, music, characters,
  maps or text of the original.
- Recon uses public material (store pages, docs, wikis, official videos,
  reviews) and normal use of a copy the user owns.
- No cheats, no bypassing DRM, licence checks, anti-cheat or online services,
  no touching other players or servers.
- The result ships under the user's own name, art and identity.
