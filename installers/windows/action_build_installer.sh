# NOTE: Run this from installers/macos

VERSION="${1#v}"
INSTALLATION_DEST="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
REVERSE_DOMAIN="com.glowingpixel.runtimecalculator"

DIST_STAGING="pkg_staging"
DIST_BASE="$DIST_STAGING/$REVERSE_DOMAIN"
DIST_LIB="$DIST_BASE/lib"

DIST_PKG="dist"

PACKAGE_NAME="runtimecalculator_v${VERSION}_windows.exe"

echo "Dir looks like:"
ls -la

mkdir -p "$DIST_PKG"
mkdir -p "$DIST_LIB"

echo "Staging python package to $DIST_STAGING"
pip install . --target "$DIST_LIB"
cp workflow_integration/Runtime\ Calculator.py "$DIST_STAGING/"

echo "Building installer"
iscc /DMyAppVersion="$VERSION" -o"$DIST_PKG" -f"$PACKAGE_NAME" installer.iss

DIST_PKG_FULL="$(realpath "$DIST_PKG/$PACKAGE_NAME")"

echo "Done!  Written to $DIST_PKG_FULL"

# Write it to the env
echo "PKG_PATH=$DIST_PKG_FULL" >> "$GITHUB_ENV"