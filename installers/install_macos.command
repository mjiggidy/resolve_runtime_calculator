#!/usr/bin/env bash

# Configurable for you hackers out there

PACKAGE_VERSION="v0.2"
WORKFLOW_INTEGRATIONS_PATH="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"

# END OF CONFIGURABLES.  LOOK NO FURTHER.

REPO_BASE="https://github.com/mjiggidy/resolve_runtime_calculator"
REPO_PACKAGE="git+$REPO_BASE.git@$PACKAGE_VERSION"
REPO_PACKAGE_BOOTSTRAP="$REPO_BASE/blob/$PACKAGE_VERSION/workflow_integration/Runtime Calculator.py"

REVERSE_DOMAIN="com.glowingpixel.runtimecalculator"

if [ ! -d "$WORKFLOW_INTEGRATIONS_PATH" ]; then
	echo "Workflow Integration Plugins folder not found." >> /dev/stderr
	exit 1
fi

res_path="$WORKFLOW_INTEGRATIONS_PATH/$REVERSE_DOMAIN"
lib_path="$res_path/lib"

# Create the path
echo "Installing to $res_path"
mkdir -p "$lib_path"

# Install the package
echo "[1/2] Downloading required packages..."
pip3 install -qq --upgrade "$REPO_PACKAGE" --target "$lib_path"

echo "[2/2] Downloading Workflow Integration..."
curl -s "$REPO_PACKAGE_BOOTSTRAP" -o "$WORKFLOW_INTEGRATIONS_PATH/Runtime Calculator.py"

echo "Installation is complete.  Runtime Calculator will be available the next time you restart Davinci Resolve."