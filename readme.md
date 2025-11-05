# Go 2 Utility

A Windows only utility for quick tweaking of:

- P and E core limits
- Energy Performance preference
- CPU boost mode

This is only tested on the Legion Go 2 (Z2E), it should also work on other Z2E devices.

## Build

Due to difficulties in getting the RyzenAdj DLL files to work with a single file Python exe from `pyinstaller`, where it cannot access memory potentially due to the temporary folder nature, the app bundles a version of Python 3.13 with the app and uses a launcher file.

It is not recommended to build locally using the supplied `build.ps1` and `build-dev.ps1` Powershell files. I have noted these to be destructive on my own system and wipe out a system install of Python 3.13.

For local development, just run the `app/app.py` file with Python 3.13: `python .\app\app.py`

## Roadmap

### 0.1.0

- [X] Set min and max frequency (CPU)
- [X] Set EPP value
- [X] Enable/disable CPU boost mode

### 0.2.0

- [X] Paged layout 
- [X] Checkboxing features so only those selected are modified
- [X] Populate form fields with the currently set values

### 0.3.0

- [ ] System info overview page (WIP)
- [ ] RyzenAdj interface page
- [ ] Terminal-like page, logs info, accepts text commands, exportable to text file

### Unplanned

- [ ] Profiles (game process to pre configured settings)
- [ ] ML analysis features? (maybe, will think about it)
- [ ] GUI redesign (nice to have, back burner for now)
- [ ] Data exporting (CSV?)
- [ ] Power draw visualisation
- [ ] AutoTDP and AutoTSP features
- [ ] GPU clock limit (ryzenadj?)
- [ ] Look into single exe file deployment
- [ ] Support for other mobile AMD processors (AMD Z1, Z1E, etc...)
- [ ] Support for mobile Intel processors
- [ ] Tidy up build process files
- [ ] Tidy up codebase
- [ ] Testing

## Attributions

- [RyzenAdj 0.17.0](https://github.com/FlyGoat/RyzenAdj) library used for interfacing with the Ryzen SMU, licensed under the GNU Lesser General Public License v3.0.