VERSION="0.5"
INSTALLATION_DEST="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
REVERSE_DOMAIN="com.glowingpixel.runtimecalculator"

DIST_BUILD="dist"
DIST_BASE="$DIST_BUILD/$REVERSE_DOMAIN"
DIST_LIB="$DIST_BASE/lib"

mkdir -p "$DIST_LIB"
echo "Staging payload to $(realpath "$DIST_BUILD")"

pip3 install --target "$DIST_LIB" .
cp "workflow_integration/Runtime Calculator.py" "$DIST_BUILD/"

echo "Payload staged"

echo "Building .pkg"

pkgbuild --root "$DIST_BUILD" --install-location "$INSTALLATION_DEST" --identifier "$REVERSE_DOMAIN.installer" --version "$VERSION" RuntimeCalculator.pkg