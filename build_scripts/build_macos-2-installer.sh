#!/usr/bin/env bash

set -o errexit -o nounset

git status
git submodule

# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG.

if [ ! "${CACTUS_INSTALLER_VERSION:-}" ]; then
  echo "WARNING: No environment variable CACTUS_INSTALLER_VERSION set. Using 0.0.0."
  CACTUS_INSTALLER_VERSION="0.0.0"
fi
if [ ! "${CACTUS_SEMVER_VERSION:-}" ]; then
  echo "WARNING: No environment variable CACTUS_SEMVER_VERSION set. Using $CACTUS_INSTALLER_VERSION."
  CACTUS_SEMVER_VERSION="$CACTUS_INSTALLER_VERSION"
fi

echo "Cactus Installer Version is: $CACTUS_INSTALLER_VERSION"
echo "Cactus Semver Version is: $CACTUS_SEMVER_VERSION"

echo "Installing npm utilities"
cd npm_macos || exit 1
npm ci
NPM_PATH="$(pwd)/node_modules/.bin"
cd .. || exit 1

echo "Create dist/"
sudo rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
SPEC_FILE=$(python -c 'import sys; from pathlib import Path; path = Path(sys.argv[1]); print(path.absolute().as_posix())' "pyinstaller.spec")
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
  echo >&2 "pyinstaller failed!"
  exit $LAST_EXIT_CODE
fi

# Creates a directory of licenses
echo "Building pip and NPM license directory"
pwd
bash ./build_license_directory.sh

# Remove rpaths on some libraries to homebrew directories that
# appears sometimes m-series chips (prefer bundled from @loader_path/..)
bash ./remove_brew_rpaths.sh

cp -a dist/daemon ../cactus-blockchain-gui/packages/gui
# Change to the gui package
cd ../cactus-blockchain-gui/packages/gui || exit 1

# sets the version for cactus-blockchain in package.json
brew install jq
cp package.json package.json.orig
jq --arg VER "$CACTUS_SEMVER_VERSION" '.version=$VER' package.json >temp.json && mv temp.json package.json

echo "Building macOS Electron app"
OPT_ARCH="--x64"
if [ "$(arch)" = "arm64" ]; then
  OPT_ARCH="--arm64"
fi
if [ "${NOTARIZE:-}" == true ]; then
  echo "Signing with the Developer ID identity imported into the runner keychain"
  # identity comes from the keychain populated by Apple-Actions/import-codesign-certs;
  # electron-builder auto-discovers it (do NOT pass CSC_LINK: its internal
  # p12 import fails to yield a usable identity and falls back to ad-hoc)
else
  echo "Not on ci or no secrets so not signing"
  export CSC_IDENTITY_AUTO_DISCOVERY=false
  # Unsigned builds are ad-hoc re-signed uniformly by the afterSign hook
  # (build_scripts/mac-adhoc-sign.js) so arm64 dyld does not abort on the
  # hardened-runtime/Team ID mismatch electron-builder's default leaves behind.
fi
echo "${NPM_PATH}/electron-builder" build --mac "${OPT_ARCH}" \
  --config.productName="Cactus" \
  --config ../../../build_scripts/electron-builder.json \
  --publish never
"${NPM_PATH}/electron-builder" build --mac "${OPT_ARCH}" \
  --config.productName="Cactus" \
  --config ../../../build_scripts/electron-builder.json \
  --publish never
LAST_EXIT_CODE=$?
ls -l dist/mac*/Cactus.app/Contents/Resources/app.asar

# reset the package.json to the original
mv package.json.orig package.json

if [ "$LAST_EXIT_CODE" -ne 0 ]; then
  echo >&2 "electron-builder failed!"
  exit $LAST_EXIT_CODE
fi

mv dist/* ../../../build_scripts/dist/
cd ../../../build_scripts || exit 1

mkdir final_installer
ORIGINAL_DMG_NAME="Cactus-${CACTUS_INSTALLER_VERSION}.dmg"
if [ "$(arch)" = "arm64" ]; then
  DMG_NAME=Cactus-${CACTUS_INSTALLER_VERSION}-macos-apple-silicon.dmg
else
  DMG_NAME=Cactus-${CACTUS_INSTALLER_VERSION}-macos-intel.dmg
fi
mv dist/"$ORIGINAL_DMG_NAME" final_installer/"$DMG_NAME"

ls -lh final_installer

if [ "${NOTARIZE:-}" == true ]; then
  echo "Notarize $DMG_NAME on ci"
  cd final_installer || exit 1
  xcrun notarytool submit --wait --apple-id "$APPLE_NOTARIZE_USERNAME" --password "$APPLE_NOTARIZE_PASSWORD" --team-id "$APPLE_TEAM_ID" "$DMG_NAME"
  xcrun stapler staple "$DMG_NAME"
  echo "Notarization step complete"
else
  echo "Not on ci or no secrets so skipping Notarize"
fi

# Notes on how to manually notarize
#
# Ask for username and password. password should be an app specific password.
# Generate app specific password https://support.apple.com/en-us/HT204397
# xcrun notarytool submit --wait --apple-id username --password password --team-id team-id Cactus-0.1.X.dmg
# Wait until the command returns a success message
#
# Once that is successful, execute the following command":
# xcrun stapler staple Cactus-0.1.X.dmg
#
# Validate DMG:
# xcrun stapler validate Cactus-0.1.X.dmg
