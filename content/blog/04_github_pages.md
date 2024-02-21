---
title: "Hugo - Deploy on GitHub and set Custom Domain GitHub Pages"
date: 2024-02-21
tags: ["linux", "hugo", "software", "domain", "github"]
categories: ["medium"]
description: "Hugo - Deploy on GitHub and set Custom Domain GitHub Pages."
draft: false
---

# Hugo - Deploy on GitHub and set Custom Domain GitHub Pages

https://gohugo.io/hosting-and-deployment/hosting-on-github/

https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages

https://medium.com/@isphinxs/using-a-custom-domain-name-with-github-pages-c9cdc2084d54

#### GitHub Pages -> Custom Domain
https://github.com/althaser/website/settings/pages

> Custom domain: althaser.eu
>
> * DNS check successful

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
