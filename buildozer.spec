[app]

# App name
title = Dronet Financial Tracker

# Package information
package.name = dronetfinancialtracker
package.domain = com.dronet

# Main Python file
source.dir = .
source.include_exts = py,json,png,jpg,kv

# Application entry point
requirements = python3,kivy==2.2.1,kivymd==1.1.1

# Orientation
orientation = portrait

# Android version settings
android.api = 33
android.minapi = 21

# App permissions
android.permissions = INTERNET

# Screen/icon settings
fullscreen = 0

# Version
version = 1.0.0

# Build settings
android.archs = arm64-v8a

# Don't automatically include unnecessary files
exclude_exts = spec,pyc,pyo

[buildozer]

# Log level
log_level = 2

# Warning: don't run Buildozer as root
warn_on_root = 1
