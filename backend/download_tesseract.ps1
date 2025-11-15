# Download Tesseract OCR installer for Windows
$url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.0/tesseract-ocr-w64-setup-v5.3.0.20221214.exe"
$output = "tesseract-installer.exe"

Write-Host "Downloading Tesseract OCR installer..."
Invoke-WebRequest -Uri $url -OutFile $output

Write-Host "Download complete. Running installer..."
Start-Process -FilePath $output -ArgumentList "/S" -Wait

Write-Host "Tesseract OCR installation complete."
