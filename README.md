# Stalker Character Adjustment Manager (SCAM)

GUI tool for S.T.A.L.K.E.R. 2: Heart of Chornobyl to configure character movement, aiming, stamina, and health parameters. This tool creates custom player configurations that override default settings without modifying core game files, ensuring compatibility with other mods.

- Easy-to-use interface for adjusting character settings
- Save and load custom presets
- Built-in recommended configurations
- Automatic mod creation and installation
- Input and movement toggles (mouse smoothing, slowdown, camera shake, and more)
- XY Sensitivity Fix included
- Multilingual support (5 languages)
- Compatible with other mods
- Verified for Stalker 2.0

[![Nexus Mods](https://img.shields.io/badge/Nexus%20Mods-SCAM-orange)](https://www.nexusmods.com/stalker2heartofchornobyl/mods/672)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R5R21752O5)

## Download

You can download SCAM:
- [Nexus Mods](https://www.nexusmods.com/stalker2heartofchornobyl/mods/672) (Download and Endorse :))

## Usage

1. Extract all files to a location of your choice
2. Run `Stalker Character Adjustment Manager.exe`
3. Set your game directory (required for automatic mod installation)
4. Adjust settings or load a preset
5. Click "Create Mod" to generate and install the mod

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
- Toggles: Allow movement while overweight, remove water movement slowdown
### Aiming & Controls
- Mouse Sensitivity: Fine-tune horizontal and vertical look rates
- Input Enhancement: Toggles for mouse smoothing, mouse slowdown, camera shake, and ADS aim block removal
- Sync Option: Synchronize turn and look rates for consistent sensitivity
### Preset Management
- Built-in Presets: Access Default, Recommended, and XY Sensitivity Fix configurations
- Custom Presets: Save and load your personal configuration profiles
- Quick Switching: Easily swap between different setups
### Mod Integration
- Auto-Installation: Direct mod installation to your S.T.A.L.K.E.R. 2 directory
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

Full license texts can be found in the `data/repak` directory of this distribution.

## Installation Requirements

- Windows 10 or newer
- S.T.A.L.K.E.R. 2: Heart of Chornobyl game installation

## Directory Structure

```
📁 Installation Folder
   └─📄 Stalker Character Adjustment Manager.exe
   └─📁 data
      └─📄 default_config.db
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
