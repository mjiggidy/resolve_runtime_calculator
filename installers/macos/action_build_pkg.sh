# NOTE: Run this from installers/macos

VERSION="${1#v}"
INSTALLATION_DEST="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
REVERSE_DOMAIN="com.glowingpixel.runtimecalculator"

DIST_STAGING="pkg_staging"
DIST_PKG="dist"
DIST_BASE="$DIST_STAGING/$REVERSE_DOMAIN"
DIST_LIB="$DIST_BASE/lib"

PACKAGE_NAME="runtimecalculator_v${VERSION}_macos.pkg"

#security find-identity -v

cd resolve_runtime_calculator/installers/macos/

mkdir -p "$DIST_PKG"
mkdir -p "$DIST_LIB"

pip3 install ../../ --target "$DIST_LIB"
cp ../../workflow_integration/Runtime\ Calculator.py "$DIST_STAGING/"

echo "Building component .pkg"
pkgbuild --root "$DIST_STAGING" --install-location "$INSTALLATION_DEST" --identifier "$REVERSE_DOMAIN.installer" --version "$VERSION" runtimecalculator_component.pkg

echo "Buidling product .pkg"
productbuild --distribution Distribution.xml --resources ./resources --package-path . --sign "Developer ID Installer: Michael Jordan ($MACOS_TEAM_ID)" "$DIST_PKG/$PACKAGE_NAME"

pkgutil --check-signature ../RuntimeCalculator_signed.pkg  

echo "Notarizing package..."
xcrun notarytool submit "$DIST_PKG/$PACKAGE_NAME" --apple-id "$MACOS_APPLE_ID" --password "$MACOS_APPLE_ID_PASSWORD" --team-id "$MACOS_TEAM_ID" --wait
xcrun stapler staple "$DIST_PKG/$PACKAGE_NAME"

echo "Done!"
open "$DIST_PKG/"