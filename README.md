# General
doxygen md main page ([source](https://stackoverflow.com/a/13442157))
```ini
INPUT                  = README.md other_sources
USE_MDFILE_AS_MAINPAGE = README.md
```

matlab enable hardware rendering (nvidia)
```matlab
opengl('save', 'hardware')
```
matlab launcher
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
