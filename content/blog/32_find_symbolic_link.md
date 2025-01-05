---
title: "Find symbolic links"
date: 2025-01-02
tags: ["shell", "find"]
categories: ["linux", "software", "applications", "tools"]
description: "Find symbolic links"
draft: false
---

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Bash_Logo_Colored.svg/2048px-Bash_Logo_Colored.svg.png" alt="ls" width="70px" height="70px">

**Find symbolic links**

```shell
$ ls -lR |grep "^l" |grep backend-swarm.yml
lrwxrwxrwx 1 pbeja pbeja  58 ago  4  2023 cpe-securitygroup-swarm.yml -> ../../Templates/domain.com/sg/backend-swarm.yml
lrwxrwxrwx 1 pbeja pbeja  58 ago  4  2023 cpe-securitygroup-swarm.yml -> ../../Templates/domain.com/sg/backend-swarm.yml
lrwxrwxrwx 1 pbeja pbeja  58 abr 19  2024 cpe-securitygroup-back-swarm.yml -> ../../Templates/domain.com/sg/backend-swarm.yml

$ find . -name "cpe-securitygroup-swarm.yml"
./Europe/Backend/cpe-securitygroup-swarm.yml
./Asia/Backend/cpe-securitygroup-swarm.yml
```
