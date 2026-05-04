#!/bin/bash

echo "Building Fake News Detector APK..."

# Create necessary directories
mkdir -p android/app/src/main/res/drawable
mkdir -p android/app/src/main/res/values
mkdir -p android/app/src/main/java/com/m1microelectronique/fakenewsdetector

# Create strings.xml
cat > android/app/src/main/res/values/strings.xml << 'STRINGS'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Fake News Detector</string>
    <string name="app_version">1.0.0</string>
    <string name="developer">Youness Bourek</string>
    <string name="organization">M1 Microélectronique</string>
</resources>
STRINGS

# Create styles.xml
cat > android/app/src/main/res/values/styles.xml << 'STYLES'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <item name="colorPrimary">#E86D3A</item>
        <item name="colorPrimaryDark">#D85A2A</item>
        <item name="colorAccent">#E86D3A</item>
    </style>
</resources>
STYLES

echo "Android resources created successfully!"
