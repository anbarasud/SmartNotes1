[app]
title = SmartNotes1
package.name = smartnotes
package.domain = org.smartnotes
source.dir = .
android.sdk_path = ./android-sdk
android.ndk_path = ./android-sdk/ndk/25.1.8937393
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.arch = arm64-v8a, armeabi-v7a
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,json,txt
version = 0.3
entrypoint = main.py
requirements = python3,kivy==2.1.0,kivymd,requests,openai,pyspellchecker,plyer,gtts,pygame
