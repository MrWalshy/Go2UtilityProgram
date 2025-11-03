# Go 2 Utility

Allows for quick tweaking of:

- P and E core limits
- Energy Performance preference
- CPU boost mode

## Build

Using `pyinstaller` to package as exe:

```
pyinstaller --onefile app/app.py
```

## Roadmap

- [X] Paged layout 
- [X] Checkboxing features so only those selected are modified
- [X] Populate form fields with the currently set values
- [ ] AutoTDP and AutoTSP features (need to hook into some other tool like hwinfo for data)
- [ ] GPU clock limit (ryzenadj?)
- [ ] Power draw visualisation
- [ ] Data exporting (CSV?)
- [ ] ML analysis features? (maybe)
- [ ] GUI redesign (nice to have, back burner for now)

## Attributions

- [RyzenAdj](https://github.com/FlyGoat/RyzenAdj) library used for interfacing with the Ryzen SMU, licensed under the GNU Lesser General Public License v3.0.