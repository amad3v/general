# General

### doxygen md main page ([source](https://stackoverflow.com/a/13442157))

```ini
INPUT                  = README.md other_sources
USE_MDFILE_AS_MAINPAGE = README.md
```

### matlab enable hardware rendering (nvidia)

```matlab
opengl('save', 'hardware')
```

### matlab launcher

```bash
#!/usr/bin/env bash
#-------------------
# Run matlab
#-------------------
# Path to java
export MATLAB_JAVA="/usr/lib/jvm/java-8-openjdk/jre"
# Logs directory
export MATLAB_LOG_DIR="/tmp"
export LD_PRELOAD=/usr/lib/libfreetype.so
# export LD_PRELOAD=/usr/lib/libstdc++.so
# export LD_LIBRARY_PATH=/usr/lib/xorg/modules/dri/
prime-run /PATH/TO/MATLAB -desktop

exit 0
```

### disable workspace trust in vscode

```json
"security.workspace.trust.enabled": false
```

### github: setup multiple accounts

From [section.io](https://www.section.io/engineering-education/using-multiple-ssh-keys-for-multiple-github-accounts/#how-to-manage-ssh-keys-on-github-accounts), __didn't work__

File to edit `~/.ssh/config`

```yml
# USER_1 account - the default config
Host github.com-USER_1
   HostName github.com
   User git
   IdentityFile ~/.ssh/id_rsa_USER_1
   
# USER_2 account
Host github.com-USER_2
   HostName github.com
   User git
   IdentityFile ~/.ssh/id_rsa_USER_2
```

From [oanhnn](https://gist.github.com/oanhnn/80a89405ab9023894df7)

```yaml
# Default github account: USER_1
Host github.com
   HostName github.com
   User git
   IdentityFile ~/.ssh/id_rsa_USER_1
   IdentitiesOnly yes

# Other github account: USER_2
Host github.com-USER_2
   HostName github.com
   User git
   IdentityFile ~/.ssh/id_rsa_USER_2
   IdentitiesOnly yes
```

### github: use multiple accounts

The default account is used as usual. Any other account, replace `github.com` in the URL with the value of `Host`
```bash
# git remote add origin git@<Host>:<user_name>/<repository>.git
git remote add origin git@github.com-USER_2:user_name/repository.git
```

### disable pc speaker

```bash
# disable for the session
sudo rmmod pcspkr
```

To disable it permanently create file `nobeep.conf` under `/etc/modprobe.d/nobeep.conf` with the following content:

```
blacklist pcspkr
```

### Superblock corrupted

Get the list of all superblocks

```bash
dumpe2fs /dev/<partition> | grep -i superblock
```

Use a backup superblock

```bash
e2fsck -f -b 98304 /dev/<partition>
```

To mount the filesystem using a superblock (e.g. 98304)

```bash
mount -o sb=98304 /dev/<partition> <mount point>
```

### Change `visudo` default editor

```bash
sudo visudo
```

Scroll to the bottom and add

```bash
# Full path is required
Defaults editor=/usr/bin/vim
```

### Enable GDM session chooser

Edit the `[daemon]` section of `/etc/gdm/gdm.conf` :

```
# full path to chooser.
Chooser=/usr/bin/chooser --disabe-sounds
```

### disable KDE wallet

```bash
kwriteconfig5 --file kwalletrc --group 'Wallet' --key 'Enabled' 'false' 
kwriteconfig5 --file kwalletrc --group 'Wallet' --key 'First Use' 'false'
```

### plasma-nm

if connected but `plasma-nm` keeps trying to connect, uninstall it, remove `kdewallet` and reinstall `plasma-nm`

### useful groups

```bash
sudo usermod -aG network,audio,power,kvm,lp,storage,tty $USER
```

### grub

```bash
# install in device not partition
# e.g. /dev/sda
sudo grub-install <device>

# configure
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

### `sudo` without password

open sudoers file

```bash
sudo visudo
```

uncomment the line

```bash
%wheel ALL=(ALL) NOPASSWD: ALL
```

if it doesn't work check the files `/etc/sudoers.d/` and remove the one resetting this option.

A better aproach is to set this option for the concerned user by creating a file in `/etc/sudoers.d` with the name of the user preceeded by a number (priority) and an underscore

```bash
# create file (replace `user_name`)
sudo vim /etc/sudoers.d/00_user_name
```

add the following line, save and exit

```
user_name ALL=(ALL) NOPASSWD: ALL
```

### vscodium ms marketplace

open the file

```bash
/opt/vscodium-bin/resources/app/product.json
```

replace

```json
  "nameLong": "VSCodium"
  "extensionsGallery": {
    "serviceUrl": "https://open-vsx.org/vscode/gallery",
    "itemUrl": "https://open-vsx.org/vscode/item"
  }
```

with

```json
  "nameLong": "Code - OSS",
  "extensionsGallery": {
    "serviceUrl": "https://marketplace.visualstudio.com/_apis/public/gallery",
    "itemUrl": "https://marketplace.visualstudio.com/items"
  }
```
