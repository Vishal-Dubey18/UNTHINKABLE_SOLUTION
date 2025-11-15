$url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v25.11.0-0/Release-25.11.0-0.zip"
Invoke-WebRequest -Uri $url -OutFile "poppler-bin.zip"
Expand-Archive -Path "poppler-bin.zip" -DestinationPath "poppler-bin" -Force
Remove-Item "poppler-bin.zip"
