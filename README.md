# Cactus-Blockchain

**Cactus** is a modern community-centric green cryptocurrency based on a proof-of-space-and-time consensus algorithm. It is a community-supported fork of the [Chia Network](https://github.com/Chia-Network/chia-blockchain) codebase.

For more information, see our website and downloads at www.Cactus-Network.net. 
<p>You can learn more in the Cactus Wiki: <a href="https://github.com/Cactus-Network/cactus-blockchain/wiki/Cactus-Blockchain-Wiki">Quick Start Guide</a></p>
<p>Please check out the Cactus Discord Channel: (https://discord.gg/qfHBqZnXTj).</p>

<p>Full Node List Here:<a href="https://www.cactus-network.net/cactus-full-nodes/" rel="nofollow"> Full Node IP's</a></p>
<p>Introducer Port: 11444</p>

<h1>
<a id="user-content-windows" class="anchor" href="#windows" aria-hidden="true"><svg class="octicon octicon-link" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>Windows Installer</h1>
<p>Download the Windows installer (exe) or Zip file - <a https://github.com/Cactus-Network/cactus-blockchain/releases/download/v1.2.11/CactusSetup-1.2.11.exe" rel="nofollow">Cactus Blockchain Windows</a></p>
<p>As the Chia code signing certificate is new you will likely have to ask to keep the download and when you run the installer, you will have to choose "More Info" and "Run Anyway" to be able to run the installer. There is no need to use the command line. Some Windows anti-virus applications are seeing the download as a false positive. You can see the entire source code and build method here so we think it's safe for you to ask those tools to ignore it. Running the installer while plotting on a previous version will stop your plotting process, so be careful.</p>
<p>You can learn more through the Chia Quick Start Guide: <a href="https://github.com/Chia-Network/chia-blockchain/wiki/Quick-Start-Guide">Quick Start Guide</a></p>
<h1>

  <h1>
<a id="user-content-Ubuntu/Debian" class="anchor" href="#windows" aria-hidden="true"><svg class="octicon octicon-link" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>Ubuntu/Debian Install</h1>
  
<p>
sudo apt-get update 
 <p>
sudo apt-get upgrade -y
  </p>
  <p>
# Install Git
    <p>
sudo apt install git -y
  </p>
  <p>
# Checkout the source and install
    <p>
git clone https://github.com/Cactus-Network/cactus-blockchain.git -b latest --recurse-submodules
<p>
      cd cactus-blockchain
sh install.sh
<p>
. ./activate
cactus init
    <p>
#add your plot directories the /.cactus/main/config/config.yaml
      <p>
cactus start famer<p>
#add your harvesters - https://github.com/Chia-Network/chia-blockchain/wiki/Farming-on-many-machines
<p>
# The GUI requires you have Ubuntu Desktop or a similar windowing system installed.<p>
# You can not install and run the GUI as root
<p>
cd /home/'yourusername'/cactus-blockchain/
  <p>
. ./activate
sh install-gui.sh
<p>
cd chia-blockchain-gui
npm run electron &
  </p> 
  
 <h1> <a id="user-content-Ubuntu/Debian" class="anchor" href="#windows" aria-hidden="true"><svg class="octicon octicon-link" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>Update Cactus-Blockchain</h1>
<p>
  cd cactus-blockchain</p><p>
  . ./activate</p><p>
cactus stop -d all</p><p>
deactivate</p><p>
git fetch</p><p>
git checkout main</p><p>
git reset --hard FETCH_HEAD --recurse-submodules</p><p>
sh install.sh</p><p>
. ./activate</p><p>
cactus init</p><p>
cactus start farmer </p><p>
  </p><p>
  <b>##GUI Update (Updating from 1.2.1 to 1.2.11)</b></p><p>
#1.2.1 did not have a GUI submodule. 1.2.11 does. Therefore we remove 1.2.1 GUI directory, and initialize the new GUI submodule</p><p>
cd ~/cactus-blockchain</p><p>
rm -rf cactus-blockchain-gui/</p><p>
git submodule init</p><p>
git submodule update</p><p>

git fetch</p><p>
git checkout main</p><p>
sh install-gui.sh</p><p>
npm run electron &  </p><p>
  
  <p>
 *Note, if you would like to run the Timelord to support the Cactus ecosystem, run 'sh install-timelord.sh', then cactus start timelord. If you receive errors during the installation process, your system is missing dependencies. In this case, thank you for trying :)
  </p>
