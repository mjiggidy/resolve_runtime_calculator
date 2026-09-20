#!/usr/bin/env bash
# NOTE: Run this from installers/windows
set -euo pipefail

VERSION="${1#v}"
REVERSE_DOMAIN="com.glowingpixel.runtimecalculator"

DIST_STAGING="pkg_staging"
DIST_BASE="$DIST_STAGING/$REVERSE_DOMAIN"
DIST_LIB="$DIST_BASE/lib"
DIST_PKG="dist"

PACKAGE_BASENAME="runtimecalculator_v${VERSION}_windows"   # Inno appends .exe

rm -rf "$DIST_STAGING"
mkdir -p "$DIST_PKG" "$DIST_LIB"

echo "Staging python package to $DIST_BASE"
pip install . --target "$DIST_LIB"
cp "workflow_integration/Runtime Calculator.py" "$DIST_BASE/"
# cp workflow_integration/manifest.xml "$DIST_BASE/"   # if applicable

echo "Building installer"
MSYS2_ARG_CONV_EXCL="*" iscc \
	"/DMyAppVersion=$VERSION" \
	"/O$DIST_PKG" \
	"/F$PACKAGE_BASENAME" \
	installer.iss

DIST_PKG_FULL="$DIST_PKG/$PACKAGE_BASENAME.exe"
echo "Done! Written to $DIST_PKG_FULL"

echo "PKG_PATH=$DIST_PKG_FULL" >> "$GITHUB_ENV"