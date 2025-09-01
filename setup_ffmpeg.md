# FFmpeg Setup for Nusify

## Windows Installation

### Option 1: Using Chocolatey (Recommended)
```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

### Option 2: Manual Installation
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Restart your terminal/command prompt

### Option 3: Using Conda
```bash
conda install -c conda-forge ffmpeg
```

## Verify Installation
```bash
ffmpeg -version
```

## Why FFmpeg is needed
FFmpeg is required by the `pydub` library for audio processing operations like:
- Audio format conversion
- Audio mixing and effects
- Audio file manipulation

Without FFmpeg, you'll see warnings and some audio features may not work properly.
