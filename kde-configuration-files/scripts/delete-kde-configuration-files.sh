#!/usr/bin/bash

fileList=(Trolltech.conf akregatorrc baloofilerc bluedevilglobalrc kactivitymanagerd-statsrc)
fileList+=(kactivitymanagerdrc kactivitymanagerd-pluginsrc kateschemarc kcmfonts kcminputrc kconf_updaterc kded5rc)
fileList+=(kdeglobals kfontinstuirc kglobalshortcutsrc khotkeysrc kmixctrlrc kmixrc)
fileList+=(kscreenlockerrc ksmserverrc ksplashrc ktimezonedrc kwinrc kwinrulesrc plasma-localerc)
fileList+=(plasma-nm plasma-org.kde.plasma.desktop-appletsrc plasmarc plasmashellrc)
fileList+=(powermanagementprofilesrc startupconfig startupconfigfiles startupconfigkeys)
fileList+=(krunnerrc touchpadxlibinputrc systemsettingsrc kxkbrc PlasmaUserFeedback)
fileList+=("kde.org/*" kiorc klipperrc knfsshare kuriikwsfilterrc kwalletmanager5rc kwalletrc)
fileList+=(plasma.emojierrc plasmanotifyrc PlasmaUserFeedback powerdevilrc kgammarc)
fileList+=(kded_device_automounterrc device_automounter_kcmrc klaunchrc)
fileList+=(trashrc kactivitymanagerd-switcher gtkrc-2.0 gtkrc baloofileinformationrc)
fileList+=(breezerc)

rm "${fileList[@]}"
