# SmartNotes (Fixed GitHub template)

This repository template contains a ready-to-use GitHub Actions workflow that installs the modern Android SDK (cmdline-tools), accepts licenses, copies the SDK into the repository, installs the latest Buildozer from GitHub (supports modern sdkmanager layout), and runs buildozer to produce an Android debug APK.

Files included:
- main.py (placeholder)
- buildozer.spec (configured to use ./android-sdk)
- .github/workflows/build_apk.yml (workflow that installs SDK + buildozer + builds APK)

Usage:
1. Create a new GitHub repo (e.g. SmartNotes)
2. Upload all files/folders in this template (do NOT upload the zip itself; upload its contents)
3. In GitHub Actions, run the "Build Android APK" workflow
4. Wait for the job to complete and download the APK artifact
