// electron-builder afterSign hook.
//
// When no real signing identity is configured (NOTARIZE unset), electron-builder
// ad-hoc signs the app with the hardened-runtime flag, which enables library
// validation. Library validation requires frameworks signed by a real team, so
// arm64 dyld aborts at launch ("different Team IDs"). Deep ad-hoc re-signing
// without the runtime flag makes the bundle uniformly team-less and loadable.
// Signed/notarized builds (NOTARIZE=true) are left untouched.
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

exports.default = async function afterSign(context) {
  if (process.platform !== 'darwin' || process.env.NOTARIZE === 'true') {
    return;
  }
  const appPath = path.join(context.appOutDir, `${context.packager.appInfo.productFilename}.app`);
  if (!fs.existsSync(appPath)) {
    return;
  }
  const profile = path.join(appPath, 'Contents', 'embedded.provisionprofile');
  if (fs.existsSync(profile)) {
    fs.rmSync(profile);
  }
  console.log(`afterSign: ad-hoc re-signing ${appPath}`);
  execSync(`codesign --force --deep --sign - "${appPath}"`, { stdio: 'inherit' });
  execSync(`codesign --verify --deep --verbose=2 "${appPath}"`, { stdio: 'inherit' });
};
