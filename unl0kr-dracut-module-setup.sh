#!/usr/bin/bash
# SPDX-License-Identifier: LGPL-2.1-or-later

check() {
    require_binaries unl0kr || return 1
    
    return 255
}

depends() {
    return 0
}

install() {
    inst_multiple -o \
         $systemdsystemunitdir/unl0kr-ask-password.path \
         $systemdsystemunitdir/unl0kr-ask-password.service \
         $systemdsystemunitdir/sysinit.target.wants/unl0kr-ask-password.path \
         /lib/systemd/systemd-reply-password \
         /etc/unl0kr.conf \
         /usr/lib*/dri/* \
         /usr/lib*/libdrm.so* \
         /usr/lib*/libgbm.so* \
         /usr/lib*/libEGL*.so* \
         /usr/lib*/libGLES*.so* \
         /usr/lib/udev/rules.d/* \
         /usr/share/glvnd/egl_vendor.d/50_mesa.json \
         /usr/share/libinput/* \
         /usr/share/X11/xkb/* \
         unl0kr \
         cut
    inst_simple "$moddir/unl0kr-ask-password.sh" /usr/bin/unl0kr-ask-password
    
    $SYSTEMCTL -q --root "$initdir" mask systemd-ask-password-console.service || :
    $SYSTEMCTL -q --root "$initdir" mask systemd-ask-password-plymouth.service || :
    $SYSTEMCTL -q --root "$initdir" mask systemd-ask-password-console.path || :
    $SYSTEMCTL -q --root "$initdir" mask systemd-ask-password-plymouth.path || :
}

