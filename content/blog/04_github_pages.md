---
title: "Hugo - Deploy and Set Custom Domain on GitHub Pages"
date: 2024-02-21
tags: ["linux", "hugo", "software", "domain", "github"]
categories: ["medium"]
description: "Hugo - Deploy and Set Custom Domain on GitHub Pages."
draft: false
---

<img src="https://raw.githubusercontent.com/althaser/website/96f6c74f638ff3ac5e4f29225a88c2534ee3cd6a/static/images/github.svg" alt="GitHub" width="70" height="70">
<img src="https://raw.githubusercontent.com/althaser/website/7f6d0aa95d19c343d266a074e0fff78d201372a0/static/images/hugo.svg" alt="Hugo" width="140" height="140">


https://gohugo.io/hosting-and-deployment/hosting-on-github/

https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages

https://medium.com/@isphinxs/using-a-custom-domain-name-with-github-pages-c9cdc2084d54

#### GitHub Pages -> Custom Domain
https://github.com/althaser/website/settings/pages

> Custom domain: althaser.eu

![](https://github.githubassets.com/images/icons/emoji/unicode/2714.png?v8)
DNS check successful

#### baseURL in config.yaml
```
baseURL: "https://althaser.eu"
```

#### DNS Server Configurations
```
A	    @	    185.199.108.153	    1 hour
A	    @	    185.199.109.153	    1 hour
A	    @	    185.199.110.153	    1 hour
A	    @	    185.199.111.153	    1 hour
CNAME	www	    althaser.eu.	    1 hour
```

#### dig outputs
```shell
$ dig althaser.eu +nostats +nocomments +nocmd
;althaser.eu. 	        IN	A
althaser.eu. 	3600	IN	A	185.199.111.153
althaser.eu.	3600	IN	A	185.199.110.153
althaser.eu.	3600	IN	A	185.199.109.153
althaser.eu.	3600	IN	A	185.199.108.153
```
```shell
$ dig www.althaser.eu +nostats +nocomments +nocmd
;www.althaser.eu.		        IN	A
www.althaser.eu.	    1244	IN	CNAME	althaser.eu.
althaser.eu.		    3600	IN	A	    185.199.110.153
althaser.eu.		    3600	IN	A	    185.199.109.153
althaser.eu.		    3600	IN	A	    185.199.108.153
althaser.eu.		    3600	IN	A	    185.199.111.153
```
```shell
$ dig althaser.github.io +nostats +nocomments +nocmd
;althaser.github.io.		    IN	A
althaser.github.io.	    3413	IN	A	185.199.110.153
althaser.github.io.	    3413	IN	A	185.199.111.153
althaser.github.io.	    3413	IN	A	185.199.109.153
althaser.github.io.	    3413	IN	A	185.199.108.153
```
