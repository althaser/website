---
title: "Mirroring Windows"
date: 2025-08-18
tags: ["obs", "obs-studio", "pipewire", "screen-capture", "cmatrix", "matrix", "feedback", "fun"]
categories: ["linux", "software", "applications", "tools"]
description: "Infinite Mirror with OBS"
draft: false
hero_images:
  - src: "https://upload.wikimedia.org/wikipedia/commons/d/d3/OBS_Studio_Logo.svg"
    alt: "obs-studio"
    width: "80"
    height: "80"
---

**An infinite tunnel of windows.** When OBS Studio captures the screen it is running on, its own preview ends up inside the capture: every frame shows the previous one, a bit smaller, again and again. With `cmatrix` raining in the terminal behind it, the result looks like a trip down the Matrix. Video on Mastodon [#matrix #linux](https://mastodon.social/@Althaser/115052359755707153).

{{< video src="/images/obs/mirroring-windows.mp4" poster="/images/obs/mirroring-windows.webp" alt="obs-studio-mirroring-windows" caption="OBS Studio capturing its own window, with cmatrix in the background" >}}

{{< toc >}}

## Setup

Install OBS Studio and `cmatrix`, then start the digital rain in a terminal and leave it full screen:

```shell
$ sudo apt install obs-studio cmatrix

$ cmatrix -b
```

## Mirror

In OBS, add a **Screen Capture (PipeWire)** source and share the whole screen (not a single window). Keep the OBS window open on top of the terminal: the preview shows the screen, which already contains the preview, which contains the screen…

- **Moving or resizing** the OBS window changes where the tunnel bends.
- **Opening a menu** copies it into every level of the tunnel, as in the picture above.
- **The depth** is limited by the preview scale: each copy is smaller until it is just a few pixels.

This is video feedback, the same effect as pointing a camera at the screen that shows its own image.
