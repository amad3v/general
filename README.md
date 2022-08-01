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
Edit the `[daemon]` section of `/etc/gdm/gdm.conf`:
```
# full path to chooser.
Chooser=/usr/bin/chooser --disabe-sounds
```
