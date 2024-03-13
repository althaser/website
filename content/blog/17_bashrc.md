---
title: "Bashrc"
date: 2024-03-13
tags: ["linux", "shell", "bash"]
categories: ["others"]
description: "Bashrc."
draft: false
---

<img src="https://raw.githubusercontent.com/althaser/website/67c0225b7e6216e4ba43ff7fd529d3feb8126b96/static/images/bash.svg" alt="bashrc" width="70" height="70">

Bashrc configuration file:

```shell
$ cat ~/.bashrc
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# ignore xdotool command to be saved in history
HISTIGNORE='xdotool'

alias yt-dlp="yt-dlp --no-playlist -S res:720"
alias genpw='pwgen -cns 64'
alias background_local='printf "\e]11;#2E3436\e\\"'
alias background_server='printf "\e]11;#012849\e\\"'
alias harbor="background_server; ssh -A <user>@<jump_server> -t ssh <user>@<private_harbor_ip>; background_local;"

ssh () { command ssh "$@"; background_local; }
```
