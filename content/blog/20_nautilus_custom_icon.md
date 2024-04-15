---
title: "Nautilus Custom Icon File"
date: 2024-04-15
tags: ["linux", "GNOME", "nautilus", "file-manager", "custom-icon"]
categories: ["linux"]
description: "Nautilus Custom Icon File."
draft: false
---

<img src="https://upload.wikimedia.org/wikipedia/commons/6/65/GNOME_Files_icon_2019.svg" alt="Nautilus-custom-icon" width="90" height="90">

https://discourse.gnome.org/t/survey-custom-file-thumbnail-usage/18241

Custom Icons in Nautilus is not allowed anymore since version 46. It  works for directories from UI only. Thus it is required to set a custom icon through command-line:

```shell
$ gio set $HOME/AppImage/BLAH.AppImage metadata::custom-icon file://$HOME/Pictures/BLAH.png

delete:
$ gio set -t string BLAH.AppImage metadata::custom-icon-name -d
```
