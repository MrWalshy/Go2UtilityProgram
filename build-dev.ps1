#pyinstaller --onefile app/app.py --name Go2Utility --add-binary "app/logic/ryzenadj/libryzenadj.dll;." --add-binary "app/logic/ryzenadj/WinRing0x64.dll;." --add-binary "app/logic/ryzenadj/WinRing0x64.sys;."
#pyinstaller --onedir app/app.py --name Go2Utility --add-binary "app/logic/ryzenadj/libryzenadj.dll;." --add-binary "app/logic/ryzenadj/WinRing0x64.dll;." --add-binary "app/logic/ryzenadj/WinRing0x64.sys;."

# copy exe and dlls into release folder
#New-Item -ItemType Directory -Force -Path release

#Copy-Item dist/Go2Utility.exe release/
#Copy-Item app/logic/ryzenadj/WinRing0x64.sys dist/
#Copy-Item app/logic/ryzenadj/libryzenadj.dll dist/
#Copy-Item app/logic/ryzenadj/WinRing0x64.dll dist/

# config
$pythonVersion = "3.13.9"
$pythonInstallerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
$distDir = "$PSScriptRoot\dist"
$runtimeDir = "$distDir\runtime"
$appDir = "$PSScriptRoot\app"
$requirementsFile = "$PSScriptRoot\requirements.txt"

# clean
Write-Host "Cleaning $distDir"
if (Test-Path $distDir) { Remove-Item -Recurse -Force $distDir }
New-Item -ItemType Directory -Path $runtimeDir

# launcher file
Write-Host "Creating launcher"
pyinstaller --onefile --name launcher "$PSScriptRoot\launcher\launcher.py" --distpath $distDir

# download + install
Write-Host "Downloading and installing Python to distribution"
$installerPath = "$distDir\python-installer.exe"
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=0 TargetDir=$runtimeDir PrependPath=0" -Wait

$pythonExe = "$runtimeDir\python.exe"
$pythonPip = "$pythonExe"  # pip is included in modern Python
Start-Process -FilePath $pythonExe -ArgumentList "-m pip install --upgrade pip" -Wait
Start-Process -FilePath $pythonExe -ArgumentList "-m pip install -r $requirementsFile --target $runtimeDir\Lib\site-packages" -Wait

# copy app folder
Write-Host "Copying application files"
Copy-Item -Path $appDir -Destination $runtimeDir -Recurse -Force

Write-Host "Build complete. Distribution is in $distDir"
