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

- Paged layout
- Checkboxing features so only those selected are modified
- Populate form fields with the currently set values
- AutoTDP and AutoTSP features (need to hook into some other tool like hwinfo for data)
- GPU clock limit (ryzenadj?)