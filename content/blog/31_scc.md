---
title: "SCC - Sloc Cloc and Code"
date: 2024-12-28
tags: ["scc", "code"]
categories: ["linux", "software", "applications", "tools"]
description: "SCC - Sloc Cloc and Code"
draft: false
---

<img src="https://github.com/boyter/scc/raw/master/scc.jpg" alt="scc" width="300px" height="100px">

**Sloc, Cloc and Code**: **scc** is a very fast accurate code counter with complexity calculations and COCOMO estimates written in pure Go

https://github.com/boyter/scc

```shell
beja@Sirius:~/go$ bin/scc -p ~/Downloads/linux-6.12.7/
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
C                        34659  24607503  3544664   2752197 18310642    2433177
Percentage               42.3%     62.9%    72.3%     61.7%    61.6%      96.7%
-------------------------------------------------------------------------------
C Header                 25301  10055998   749819   1499867  7806312      53870
Percentage               30.9%     25.7%    15.3%     33.6%    26.2%       2.1%
-------------------------------------------------------------------------------
Device Tree               5333   1645272   215544     79641  1350087         37
Percentage                6.5%      4.2%     4.4%      1.8%     4.5%       0.0%
-------------------------------------------------------------------------------
YAML                      4388    491303    80699     20156   390448          0
Percentage                5.4%      1.3%     1.6%      0.5%     1.3%       0.0%
-------------------------------------------------------------------------------
ReStructuredText          3599    745499   180112         0   565387          0
Percentage                4.4%      1.9%     3.7%      0.0%     1.9%       0.0%
-------------------------------------------------------------------------------
Makefile                  3035     80834    12207     12974    55653        439
Percentage                3.7%      0.2%     0.2%      0.3%     0.2%       0.0%
-------------------------------------------------------------------------------
Plain Text                1511    136766    24723         0   112043          0
Percentage                1.8%      0.3%     0.5%      0.0%     0.4%       0.0%
-------------------------------------------------------------------------------
Assembly                  1348    376587    42166     50137   284284       3345
Percentage                1.6%      1.0%     0.9%      1.1%     1.0%       0.1%
-------------------------------------------------------------------------------
Shell                      967    184590    30973     23168   130449      10020
Percentage                1.2%      0.5%     0.6%      0.5%     0.4%       0.4%
-------------------------------------------------------------------------------
JSON                       866    537457        2         0   537455          0
Percentage                1.1%      1.4%     0.0%      0.0%     1.8%       0.0%
-------------------------------------------------------------------------------
Python                     272     81823     9923      7491    64409      10704
Percentage                0.3%      0.2%     0.2%      0.2%     0.2%       0.4%
-------------------------------------------------------------------------------
Jinja                      127      1042       65       123      854        172
Percentage                0.2%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
SVG                         77     50659       90      1301    49268          0
Percentage                0.1%      0.1%     0.0%      0.0%     0.2%       0.0%
-------------------------------------------------------------------------------
Rust                        76     18802     1483      7981     9338        824
Percentage                0.1%      0.0%     0.0%      0.2%     0.0%       0.0%
-------------------------------------------------------------------------------
Perl                        70     50525     5230      3964    41331       3128
Percentage                0.1%      0.1%     0.1%      0.1%     0.1%       0.1%
-------------------------------------------------------------------------------
BASH                        60      2394      378       356     1660        250
Percentage                0.1%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
XML                         23     22150     1171      1709    19270          0
Percentage                0.0%      0.1%     0.0%      0.0%     0.1%       0.0%
-------------------------------------------------------------------------------
DOT                         21       873       78        42      753          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
AWK                         15      2854      262       213     2379        447
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
CSV                         11      1373      106         0     1267          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Extensible Styleshe…        10       200       26         0      174          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Happy                       10      6081      721         0     5360          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
LEX                         10      2980      370       335     2275          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
LD Script                    8       377       59        29      289          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
C++                          7      2350      241        85     2024        342
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Autoconf                     5       433       30        26      377         11
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
License                      5       422       84         0      338          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Unreal Script                5       671       98       158      415         23
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Snakemake                    4       118       13        13       92          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
CSS                          3       295       54        69      172          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Systemd                      3       167       25         0      142          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Bazel                        2       692      155       140      397          6
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
C++ Header                   2       125       11        55       59          2
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
HEX                          2       173        0         0      173          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
HTML                         2        33        3         8       22          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
INI                          2        13        2         5        6          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Module-Definition            2       128       15         0      113          4
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
sed                          2       100       21        51       28          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Alex                         1        36        4         0       32          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Gherkin Specificati…         1       311       37        62      212          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
MATLAB                       1        89       17        37       35          3
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Markdown                     1       270       73         0      197          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Ruby                         1        29        4         0       25          1
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
TOML                         1        12        1         9        2          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
TeX                          1       234        6        73      155          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
Vim Script                   1        42        3        12       27          5
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
-------------------------------------------------------------------------------
XML Schema                   1       404       46         0      358          0
Percentage                0.0%      0.0%     0.0%      0.0%     0.0%       0.0%
───────────────────────────────────────────────────────────────────────────────
Total                    81852  39111089  4901814   4462487 29746788    2516810
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $1,344,953,930
Estimated Schedule Effort (organic) 212.48 months
Estimated People Required (organic) 562.34
───────────────────────────────────────────────────────────────────────────────
Processed 1459971652 bytes, 1459.972 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────

beja@Sirius:~$ docker run --rm -it -v "/home/beja/Development/github-althaser/website:/pwd"  ghcr.io/lhoupert/scc:master scc --version
scc version 3.3.0 (beta)

beja@Sirius:~$ docker run --rm -it -v "/home/beja/Development/github-althaser/website:/pwd"  ghcr.io/lhoupert/scc:master scc /pwd
```
