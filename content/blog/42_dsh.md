---
title: "Dsh"
date: 2025-02-11
tags: ["ssh", "bash"]
categories: ["linux", "software", "applications", "tools"]
description: "Dsh"
draft: false
---

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Bash_Logo_Colored.svg/2048px-Bash_Logo_Colored.svg.png" alt="dsh" width="70" height="70">

**dsh** dancer's shell, or distributed shell.

https://www.netfort.gr.jp/~dancer/software/dsh.html

https://www.tecmint.com/using-dsh-distributed-shell-to-run-linux-commands-across-multiple-machines/

```shell
$ sudo apt install dsh

$ sudo vim /etc/dsh/dsh.conf
replace remoteshell =rsh to remoteshell =ssh

$ mkdir -p ~/.dsh/group

$ vim ~/.dsh/group/machine-group
machine1.bla.org
machine2.bla.org
machine3.bla.org

$ dsh -M -g machine-group -c "lsb_release -a"
```
