pyinstaller --onefile app/app.py --name Go2Utility --add-binary "app/logic/ryzenadj/libryzenadj.dll;." --add-binary "app/logic/ryzenadj/WinRing0x64.dll;." --add-binary "app/logic/ryzenadj/WinRing0x64.sys;."

# copy exe and dlls into release folder
#New-Item -ItemType Directory -Force -Path release
#Copy-Item dist/Go2Utility.exe release/
Copy-Item app/logic/ryzenadj/WinRing0x64.sys dist/
Copy-Item app/logic/ryzenadj/libryzenadj.dll dist/
Copy-Item app/logic/ryzenadj/WinRing0x64.dll dist/