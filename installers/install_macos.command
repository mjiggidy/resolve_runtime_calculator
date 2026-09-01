#!/usr/bin/env bash

# Configurable for you hackers out there
# ---
PACKAGE_VERSION="v0.4"
WORKFLOW_INTEGRATION_PATH="${1:-/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins}"
# ---
# END OF CONFIGURABLES.  LOOK NO FURTHER.

REPO_BASE="https://github.com/mjiggidy/resolve_runtime_calculator"
REPO_PACKAGE="git+$REPO_BASE.git@$PACKAGE_VERSION"
REPO_PACKAGE_BOOTSTRAP="$REPO_BASE/raw/refs/tags/$PACKAGE_VERSION/workflow_integration/Runtime%20Calculator.py"

REVERSE_DOMAIN="com.glowingpixel.runtimecalculator"

# Here we go

clear

echo "________              __________                                     "
echo "___  __ \___  __________  /___(_)______ ________                     "
echo "__  /_/ /  / / /_  __ \  __/_  /__  __ \__ \  _ \                    "
echo "_  _, _// /_/ /_  / / / /_ _  / _  / / / / /  __/                    "
echo "/_/ |_| \__,_/ /_/ /_/\__/ /_/  /_/ /_/ /_/\___/                     "
echo "     _________      ______            ______      _____              "
echo "     __  ____/_____ ___  /_________  ____  /_____ __  /______________"
echo "     _  /    _  __ \/_  /_  ___/  / / /_  /_  __ \/  __/  __ \_  ___/"
echo "     / /___  / /_/ /_  / / /__ / /_/ /_  / / /_/ // /_ / /_/ /  /    "
echo "     \____/  \__,_/ /_/  \___/ \__,_/ /_/  \__,_/ \__/ \____//_/     "
echo ""
echo " ${PACKAGE_VERSION} Installer By Michael Jordan <michael@glowingpixel.com>"
echo " https://github.com/mjiggidy/resolve_runtime_calculator/"
#echo "---------------------------------------------------------------------"
echo ""

if [ ! -d "$WORKFLOW_INTEGRATION_PATH" ]; then
	echo "Workflow Integration Plugins folder not found at $WORKFLOW_INTEGRATION_PATH." >> /dev/stderr
	echo "Please provide the path to the Workflow Integration folder as an argument:"
	echo ""
	echo "$0 \"/path/to/Workflow Itegration Plugins\""
	echo ""
	exit 1
fi

res_path="$WORKFLOW_INTEGRATION_PATH/$REVERSE_DOMAIN"
lib_path="$res_path/lib"

# Create the path
echo "Installing to $res_path"
mkdir -p "$lib_path"
echo ""

# Install the package
echo "[1/2] Downloading required packages..."
pip3 install -qq --upgrade "$REPO_PACKAGE" --target "$lib_path"

echo "[2/2] Downloading Workflow Integration..."
curl "$REPO_PACKAGE_BOOTSTRAP" -L -f -s -S -o "$WORKFLOW_INTEGRATION_PATH/Runtime Calculator.py"

echo ""
echo "Installation is complete.  Runtime Calculator will be available the next time you restart Davinci Resolve."
echo ""