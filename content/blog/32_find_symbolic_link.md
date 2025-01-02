---
title: "Find symbolic links"
date: 2025-01-02
tags: ["linux", "shell"]
categories: ["tools"]
description: "Find symbolic links"
draft: false
---

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Bash_Logo_Colored.svg/2048px-Bash_Logo_Colored.svg.png" alt="ls" width="70px" height="70px">

**Find symbolic links**

```shell
$ ls -lR |grep '^l'|grep keypair.yml
lrwxrwxrwx 1 pbeja pbeja  60 jan  2 12:36 cpe-gitlab-ci-keypair.yml -> ../../Templates/domain.com/keypair/v2/keypair.yml
lrwxrwxrwx 1 pbeja pbeja  57 ago  4  2023 cpe-gitlab-ci-keypair.yml -> ../../Templates/domain.com/keypair/keypair.yml
lrwxrwxrwx 1 pbeja pbeja   57 jun  7  2023 cpe-gitlab-ci-keypair.yml -> ../../Templates/domain.com/keypair/keypair.yml
lrwxrwxrwx 1 pbeja pbeja  60 jul  1  2024 cpe-gitlab-ci-keypair.yml -> ../../Templates/domain.com/keypair/v1/keypair.yml
lrwxrwxrwx 1 pbeja pbeja  57 ago 20 17:07 cpe-gitlab-ci-keypair.yml -> ../../Templates/domain.com/keypair/keypair.yml
lrwxrwxrwx 1 pbeja pbeja  57 abr 19  2024 cpe-gitlab-ci-keypair.yml -> ../../Templates/domain.com/keypair/keypair.yml
lrwxrwxrwx 1 pbeja pbeja  60 jun  7  2023 gitlab-ci-keypair.yml -> ../../../Templates/domain.com/keypair/keypair.yml

$ find -L . -xtype l
```
