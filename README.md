# Stalker Configurator Aiming & Movement (SCAM)

GUI tool for S.T.A.L.K.E.R. 2: Heart of Chornobyl to configuring vaulting, movement, and aiming parameters.
This tool makes changes to the Player only and uses a different approach that doesn't directly modify ObjPrototypes.cfg,
so every mod should be compatible.

- Play how you like with a Easy-to-use interface for adjusting movement and aiming settings
- Save and load custom presets
- Built-in recommended configurations
- Automatic mod creation and installation
- Mouse smoothing/acceleration removal utility
- 1:1 XY Sensitivity Fix Included
- Compatible with everything (so far)

[![Nexus Mods](https://img.shields.io/badge/Nexus%20Mods-SCAM-orange)](https://www.nexusmods.com/stalker2heartofchornobyl/mods/672)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R5R21752O5)

## Download

You can download SCAM from either:
- [Nexus Mods](https://www.nexusmods.com/stalker2heartofchornobyl/mods/672) (Recommended - Download and Endorse :))
- [GitHub Releases](https://github.com/v3fish/SCAMStalkerConfigurator/releases)

## Usage

1. Extract all files to a location of your choice
2. Run `Stalker Configurator Aiming Movement.exe`
4. Set your game directory (required for automatic mod installation)
5. Adjust settings or load a preset
7. Click "Create Mod" to generate and install the mod

### Game Directory Examples

```console
Steam: C:\Program Files (x86)\Steam\steamapps\common\S.T.A.L.K.E.R. 2 Heart of Chornobyl
Xbox: C:\XboxGames\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\Content
```

## Features

### Character Configuration
- Stamina System: Adjust stamina costs for jumping, sprinting, climbing, and combat actions
- Health & Vitals: Configure HP, stamina, bleeding, radiation, hunger, and thirst parameters
- Regeneration Rates: Fine-tune health and stamina recovery speeds
### Movement & Mobility
- Vaulting System: Customize vaulting angles, distances, and obstacle height limits
- Movement Speed: Adjust walking, crouching, and air control coefficients
- Jump Mechanics: Configure jump heights and movement modifiers
### Aiming & Controls
- Mouse Sensitivity: Fine-tune horizontal and vertical look rates
- Input Enhancement: Remove mouse smoothing and acceleration for precise aiming
- Sync Option: Synchronize turn and look rates for consistent sensitivity
### Preset Management
- Built-in Presets: Access Default, V3Fish Recommended, and XY Sensitivity Fix configurations
- Custom Presets: Save and load your personal configuration profiles
- Quick Switching: Easily swap between different setups
### Mod Integration
- Auto-Installation: Direct mod installation to your S.T.A.L.K.E.R. 2 directory
- Conflict Detection: Warns about incompatible mods before installation
- Advanced Options: Force default values to prevent other mods from overriding settings
### Multilingual Support
- 5 Languages: English, Russian, Ukrainian, Korean, and Chinese localizations
- Easy Switching: Change language from within the application

## Third-Party Components

This tool uses the following third-party components:

### repak.exe
- Author: trumank (https://github.com/trumank)
- Usage: Pak file creation for mod packaging
- Licensed under:
  - MIT License
  - Apache License 2.0
- Original source: https://github.com/trumank/repak

Full license texts can be found in the `repak` directory of this distribution.

## Installation Requirements

- Windows 10 or newer
- .NET Framework 4.7.2 or newer
- S.T.A.L.K.E.R. 2: Heart of Chornobyl game installation

## Directory Structure

```
📁 Installation Folder
   └─📄 Stalker Configurator Aiming Movement.exe
   └─📁 repak
      └─📄 repak.exe
        📄 LICENSE-APACHE
        📄 LICENSE-MIT
```

## Mod Installation Location

If directory is configured Mods are automatically installed to:
```
Example Directories
Steam: <Game Directory>\Stalker2\Content\Paks\~mods
Xbox Game Pass: <Game Directory>\Stalker2\Content\Paks\~mods
```

## Troubleshooting

TBD

For additional help or to report issues, please visit:
- [Nexus Mods Page](https://www.nexusmods.com/stalker2heartofchornobyl/mods/672) (Post in the comments section or bug reports)

Note: For GitHub issues relating to the source code itself, you can use the [GitHub repository](https://github.com/v3fish/SCAMStalkerConfigurator).
