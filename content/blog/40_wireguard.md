---
title: "Wireguard - VPN"
date: 2025-01-26
tags: ["security", "VPN"]
categories: ["linux", "software", "applications", "tools", "raspberrypi"]
description: "Wireguard - VPN"
draft: false
---

<img src="https://www.wireguard.com/img/wireguard.svg" alt="wireguard" width="800px" height="800px">

**WireGuard** is a simple, fast and modern VPN implementation. It is widely deployed and can be used cross-platform.

# Setup WireGuard

## Server - Raspberry Pi
<img src="https://www.raspberrypi.com/app/uploads/2020/06/raspberrry_pi_logo.png" alt="raspberypi" width="50px" height="50px">

1. **Enable Port Fowarding** via **systctl.conf** setting up the following
```shell
root@raspberrypi:~# vim /etc/sysctl.conf
net.ipv4.ip_forward = 1
```

2. Reload **sysctl** configurations.
```shell
root@raspberrypi:~# sysctl -p
```

3. Install **ufw** firewall.
```shell
root@raspberrypi:~# apt install ufw
```

4. Allow **openssh** and enable **ufw**.
```shell
root@raspberrypi:~# ufw allow openssh

root@raspberrypi:~# ufw enable
Firewall is active and enabled on system startup

root@raspberrypi:~# ufw status
Status: active
To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
```

5. Install **WireGuard**.
```shell
root@raspberrypi:~# apt install wireguard
```

6. Generate WireGuard Server keys (**privatekey** and **publickey**).
```shell
root@raspberrypi:~# cd /etc/wireguard/

root@raspberrypi:/etc/wireguard# umask 077; wg genkey | tee privatekey | wg pubkey > publickey

root@raspberrypi:/etc/wireguard# ls -lah /etc/wireguard/
total 24K
drwx------   2 root root 4.0K Jan 25 23:06 .
drwxr-xr-x 136 root root  12K Jan 25 23:06 ..
-rw-------   1 root root   45 Jan 25 22:56 privatekey
-rw-------   1 root root   45 Jan 25 22:56 publickey
```

7. Generate **WireGuard** Client keys.
```shell
root@raspberrypi:~# mkdir -p /etc/wireguard/clients/beja

root@raspberrypi:~# tree /etc/wireguard/
.
├── clients
│   └── beja
├── privatekey
└── publickey
3 directories, 2 files

root@raspberrypi:~# wg genkey | tee /etc/wireguard/clients/beja/beja.key
ekHeweGbOqDxzaPg1lKMwGAxpmh6zKhjSDZUoe2H2uQLNQyAC7zhRrVGeMtkwCTi

root@raspberrypi:~# cat /etc/wireguard/clients/beja/beja.key | wg pubkey | tee /etc/wireguard/clients/beja/beja.pub
sdrUDZLQ1S2mNP4J4xlE86GCo17zwkOy2z3an6AfQnn7xVu7BlhXIYeorZUnTpLG
```

8. Check default **gateway** interface that is used to connect to the internet.
```shell
root@raspberrypi:/etc/wireguard# ip route list default
default via 192.168.1.1 dev wlan0 proto dhcp src 192.168.1.13 metric 600
```

9. Create **WireGuard** configuration `/etc/wireguard/wg0.conf` and replace the interface in NAT configuration section from the previous step.
```shell
root@raspberrypi:~# vim /etc/wireguard/wg0.conf
[Interface]
# Wireguard interface will be run at 10.20.0.1
Address = 10.20.0.1/24
# Ensure any changes will be saved to the WireGuard config file
SaveConfig = true
# Setting up NAT for Wireguard Interface
PostUp = ufw route allow in on wg0 out on wlan0
PostUp = iptables -t nat -I POSTROUTING -o wlan0 -j MASQUERADE
PostUp = ip6tables -t nat -I POSTROUTING -o wlan0 -j MASQUERADE
PreDown = ufw route delete allow in on wg0 out on wlan0
PreDown = iptables -t nat -D POSTROUTING -o wlan0 -j MASQUERADE
PreDown = ip6tables -t nat -D POSTROUTING -o wlan0 -j MASQUERADE
# Clients will connect to UDP port 51820
ListenPort = 51820
# WireGuard Server private key
PrivateKey = 3eLT3XeFcTtviajcaXHEQMlMYM7j0PGY2SHNLX22YBOJwqrLzEiVmPsBui8qK90R

[Peer]
# WireGuard client public key - beja.pub
PublicKey = sdrUDZLQ1S2mNP4J4xlE86GCo17zwkOy2z3an6AfQnn7xVu7BlhXIYeorZUnTpLG

# clients VPN IP address you allow to connect
# Possible to specify subnet -> [10.20.0.0/24]
AllowedIPs = 10.20.0.2/24
```

10. Add `51820/udp` rule to **ufw** firewall.
```shell
root@raspberrypi:/etc/wireguard# ufw allow 51820/udp
Rule added
Rule added (v6)

root@raspberrypi:/etc/wireguard# ufw status
Status: active
To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
51820/udp                  ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
51820/udp (v6)             ALLOW       Anywhere (v6)
```

11. Managing **WireGuard** service.
```shell
root@raspberrypi:/etc/wireguard# systemctl start wg-quick@wg0.service

root@raspberrypi:/etc/wireguard# systemctl enable wg-quick@wg0.service
Created symlink /etc/systemd/system/multi-user.target.wants/wg-quick@wg0.service → /lib/systemd/system/wg-quick@.service.

root@raspberrypi:/etc/wireguard# systemctl status wg-quick@wg0.service
● wg-quick@wg0.service - WireGuard via wg-quick(8) for wg0
     Loaded: loaded (/lib/systemd/system/wg-quick@.service; enabled; preset: enabled)
     Active: active (exited) since Sat 2025-01-25 23:20:02 WET; 27s ago
       Docs: man:wg-quick(8)
             man:wg(8)
             https://www.wireguard.com/
             https://www.wireguard.com/quickstart/
             https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8
             https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8
   Main PID: 4346 (code=exited, status=0/SUCCESS)
        CPU: 176ms
Jan 25 23:20:02 raspberrypi wg-quick[4346]: [#] wg setconf wg0 /dev/fd/63
Jan 25 23:20:02 raspberrypi wg-quick[4362]: Warning: AllowedIP has nonzero host part: 10.20.0>
Jan 25 23:20:02 raspberrypi wg-quick[4346]: [#] ip -4 address add 10.20.0.1/24 dev wg0
Jan 25 23:20:02 raspberrypi wg-quick[4346]: [#] ip link set mtu 1420 up dev wg0
Jan 25 23:20:02 raspberrypi wg-quick[4346]: [#] ufw route allow in on wg0 out on wlan0
Jan 25 23:20:02 raspberrypi wg-quick[4377]: Rule added
Jan 25 23:20:02 raspberrypi wg-quick[4377]: Rule added (v6)
Jan 25 23:20:02 raspberrypi wg-quick[4346]: [#] iptables -t nat -I POSTROUTING -o wlan0 -j MA>
Jan 25 23:20:02 raspberrypi wg-quick[4346]: [#] ip6tables -t nat -I POSTROUTING -o wlan0 -j M>
Jan 25 23:20:02 raspberrypi systemd[1]: Finished wg-quick@wg0.service - WireGuard via wg-quic>

root@raspberrypi:/etc/wireguard# ip a show wg0
5: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.20.0.1/24 scope global wg0
       valid_lft forever preferred_lft forever

root@raspberrypi:/etc/wireguard# ip --color a show wg0
5: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.20.0.1/24 scope global wg0
       valid_lft forever preferred_lft forever
```

12. Manual managing **WireGuard** connections.
```shell
$ sudo wg-quick up /etc/wireguard/wg0.conf
$ sudo wg-quick down /etc/wireguard/wg0.conf
```

## Client - Laptop
<img src="https://static.thenounproject.com/png/1388614-200.png" alt="laptop" width="80px" height="80px">

1. Install **WireGuard**.
```shell
root@laptop:~# apt install wireguard-tools
```

2. Create **WireGuard** configurations.
```shell
root@laptop:~# vim /etc/wireguard/wg1.conf
[Interface]
# Define the IP address for the client - must be matched with wg0 on the Wireguard Server
Address = 10.20.0.2/24

# specific DNS Server
DNS = 1.1.1.1

# Private key for the client - alice.key
PrivateKey = ekHeweGbOqDxzaPg1lKMwGAxpmh6zKhjSDZUoe2H2uQLNQyAC7zhRrVGeMtkwCTi

[Peer]
# Public key of the Wireguard server - server.pub
PublicKey = JRKg8QbQqYMTMwDjHHw4Lba5ZfdsUjIQQMuOyQwHCMsJKGpFuduaVnnnhQy14rmI

# Allow all traffic to be routed via Wireguard VPN
AllowedIPs = 0.0.0.0/0

# Public IP address of the Wireguard Server
Endpoint = 192.168.1.13:51820

# Sending Keepalive every 25 sec
PersistentKeepalive = 25
```

3. Start **WireGuard** connection.
```shell
root@laptop:~# wg-quick up wg1
[#] ip link add wg1 type wireguard
[#] wg setconf wg1 /dev/fd/63
[#] ip -4 address add 10.20.0.2/24 dev wg1
[#] ip link set mtu 1420 up dev wg1
[#] resolvconf -a wg1 -m 0 -x
[#] wg set wg1 fwmark 51820
[#] ip -4 rule add not fwmark 51820 table 51820
[#] ip -4 rule add table main suppress_prefixlength 0
[#] ip -4 route add 0.0.0.0/0 dev wg1 table 51820
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1
[#] nft -f /dev/fd/63
```

4. Check connections
```shell
root@laptop:~# ip a show wg1
13: wg1: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.20.0.2/24 scope global wg1
       valid_lft forever preferred_lft forever

root@laptop:~# ping -c3 10.20.0.1
PING 10.20.0.1 (10.20.0.1) 56(84) bytes of data.
64 bytes from 10.20.0.1: icmp_seq=1 ttl=64 time=4.02 ms
64 bytes from 10.20.0.1: icmp_seq=2 ttl=64 time=6.69 ms
64 bytes from 10.20.0.1: icmp_seq=3 ttl=64 time=7.01 ms
--- 10.20.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 4.017/5.905/7.009/1.341 ms

root@laptop:~# ping -c3 10.20.0.2
PING 10.20.0.2 (10.20.0.2) 56(84) bytes of data.
64 bytes from 10.20.0.2: icmp_seq=1 ttl=64 time=0.077 ms
64 bytes from 10.20.0.2: icmp_seq=2 ttl=64 time=0.062 ms
64 bytes from 10.20.0.2: icmp_seq=3 ttl=64 time=0.058 ms
--- 10.20.0.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2035ms
rtt min/avg/max/mdev = 0.058/0.065/0.077/0.008 ms

root@laptop:~# ping -c3 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=58 time=26.0 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=58 time=27.1 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=58 time=28.5 ms
--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 26.007/27.202/28.545/1.041 ms

root@laptop:~# ping -c3 google.com
PING google.com (2a00:1450:4003:80d::200e) 56 data bytes
64 bytes from mad07s24-in-x0e.1e100.net (2a00:1450:4003:80d::200e): icmp_seq=1 ttl=118 time=29.2 ms
64 bytes from mad07s24-in-x0e.1e100.net (2a00:1450:4003:80d::200e): icmp_seq=2 ttl=118 time=29.7 ms
64 bytes from mad07s24-in-x0e.1e100.net (2a00:1450:4003:80d::200e): icmp_seq=3 ttl=118 time=24.3 ms
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 24.318/27.749/29.713/2.434 ms

root@laptop:~# sudo wg show
interface: wg1
  public key: sdrUDZLQ1S2mNP4J4xlE86GCo17zwkOy2z3an6AfQnn7xVu7BlhXIYeorZUnTpLG
  private key: (hidden)
  listening port: 42869
  fwmark: 0xca6c

peer: JRKg8QbQqYMTMwDjHHw4Lba5ZfdsUjIQQMuOyQwHCMsJKGpFuduaVnnnhQy14rmI
  endpoint: 192.168.1.13:51820
  allowed ips: 0.0.0.0/0
  latest handshake: 1 minute, 12 seconds ago
  transfer: 1.89 MiB received, 1.75 MiB sent
  persistent keepalive: every 25 seconds
```

5. Manage connection
```shell
$ sudo wg-quick down wg1
```

6. done :)

## Reference links
- https://wiki.debian.org/WireGuard
- https://www.howtoforge.com/guide-to-install-wireguard-vpn-on-debian-12/
- https://documentation.ubuntu.com/server/explanation/intro-to/wireguard-vpn
- https://docs.vultr.com/how-to-install-wireguard-vpn-on-ubuntu-24-04
