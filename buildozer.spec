[app]
source.dir = .
title = SmartNotes
package.name = smartnotes
package.domain = org.smartnotes

android.sdk_path = ./android-sdk
android.ndk_path = ./android-sdk/ndk/25.1.8937393
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.arch = arm64-v8a, armeabi-v7a

source.include_exts = py,png,jpg,kv,atlas,mp3,wav,json,txt
version = 0.2
orientation = portrait
fullscreen = 0
entrypoint = main.py


# Required packages
requirements = python3,kivy==2.1.0,kivymd,requests,openai,pyspellchecker,plyer,gtts,pygame

android.api = 33
android.minapi = 21
android.ndk = 25b

# Permissions
android.permissions = INTERNET, RECORD_AUDIO, WAKE_LOCK, VIBRATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Architectures
android.arch = armeabi-v7a,arm64-v8a

log_level = 2
