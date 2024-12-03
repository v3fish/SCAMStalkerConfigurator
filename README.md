# Stalker Configurator Aiming & Movement (SCAM)

GUI tool for configuring vaulting, movement, and aiming parameters in S.T.A.L.K.E.R. 2: Heart of Chornobyl.

- Easy-to-use interface for adjusting movement and aiming settings
- Save and load custom presets
- Built-in recommended configurations
- Automatic mod creation and installation
- Mouse smoothing/acceleration removal utility

## Usage

1. Download the latest release from the [releases page](https://github.com/v3fish/SCAMStalkerConfigurator/releases)
2. Extract all files to a location of your choice
3. Run `Stalker Configurator Aiming Movement.exe`
4. Set your game directory (required for automatic mod installation)
5. Adjust settings or load a preset
6. Click "Create Mod" to generate and install the mod

### Game Directory Examples

```console
Steam: C:\Program Files (x86)\Steam\steamapps\common\S.T.A.L.K.E.R. 2 Heart of Chornobyl
Xbox: C:\XboxGames\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\Content
```

## Features

### Movement Configuration
- Base movement speed adjustments
- Sprint and crouch modifiers
- Jump height configuration
- Movement acceleration tuning

### Aiming Configuration
- Horizontal and vertical sensitivity
- Option to sync turn/look rates
- Mouse smoothing/acceleration removal
- Advanced aim configuration options

### Preset Management
- Save custom configurations
- Load built-in recommended presets
- Import/export settings
- Quick switching between configurations

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

Mods are automatically installed to:
```
Steam: <Game Directory>\Stalker2\Content\Paks\~mods
Xbox: <Game Directory>\Stalker2\Content\Paks\~mods
```

## Troubleshooting

If the mod doesn't appear to be working:

1. Verify the game directory is set correctly
2. Check that the mod file exists in the `~mods` folder

For additional help or to report issues, please visit the [GitHub repository](https://github.com/v3fish/SCAMStalkerConfigurator).
