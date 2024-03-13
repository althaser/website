---
title: "Bash - Prompt With Branch Name"
date: 2024-02-20
tags: ["linux", "bash", "branch", "git", "configuration"]
categories: ["medium"]
description: "How to setup bashrc to support branch name in its prompt."
draft: false
---

<img src="https://raw.githubusercontent.com/althaser/website/67c0225b7e6216e4ba43ff7fd529d3feb8126b96/static/images/bash.svg" alt="Bash" width="70" height="70">

https://medium.com/@chiraggandhi70726/how-to-add-git-branch-name-to-bash-prompt-b112b93606e

```shell
$ code ~/.bashrc
```

Append the following:
```shell
# Show git branch name
force_color_prompt=yes
color_prompt=yes
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "

mine:
PS1='${debian_chroot:+($debian_chroot)}\[\033[1;33m\]\t \u@\h\[\033[0m\]:\[\033[34m\]\w\[\033[00m\]\[\033[31m\]$(parse_git_branch)\[\033[00m\] $ '
```

Reload
```shell
$ exec bash
```
