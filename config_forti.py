# GUI avec TkInter ou Dear PyGUI

#############
# VAR

routerVGF = "10.54.75.1" 
boxInternet = "192.168.1.1"
mainSite = { 
    "name": "Donjon",
    "network": "10.54.133.128",
    "mask": "255.255.255.128"
}
#brand = "Audi"
site = {
    "name": "ABSOLUTE",
    "network": "10.54.70.0",
    "mask": "255.255.255.0"
}
#city = "Les ulis"
hostname = "AU-ABSOLUTE"
addressServerDC = "10.54.133.133"
localDomain = "fr02410.vw-group.com"
##############


configFile = open("fortigate.conf", "w")

configFile.write(f"""config router static
edit 1
set dst 0.0.0.0 0.0.0.0
set gateway {boxInternet}
set device "wan1"
set comment "Internet"
next
edit 2
set dst 10.6.0.0 255.255.0.0
set gateway {routerVGF}
set device "internal"
set comment "Plateforme Internet Datacenter SFR"
next
edit 3
set dst 10.54.240.157 255.255.255.255
set gateway {routerVGF}
set device "internal"
set comment "cpn.gvf"
next
edit 4
set dst 10.54.94.0 255.255.255.128
set gateway {routerVGF}
set device "internal"
set comment "Liaison Roissy CE CAR*Base"
next
edit 5
set dst 10.112.224.0 255.255.248.0
set gateway {routerVGF}
set device "internal"
set comment "Extranet GVF"
next
edit 6
set dst 10.54.248.0 255.255.248.0
set gateway {routerVGF}
set device "internal"
set comment "SD Creator"
next
edit 7
set dst 10.60.0.0 255.255.0.0
set gateway {routerVGF}
set device "internal"
set comment "Support N2, Services EPO/WSUS VAS, Reverse Proxy 071219"
next
edit 8
set dst 10.112.192.0 255.255.192.0
set gateway {routerVGF}
set device "internal"
set comment "Coeur de réseau partenaire (sur-réseau)"
next
edit 9
set dst 10.54.240.128 255.255.255.192
set gateway {routerVGF}
set device "internal"
set comment "(cpn.gvf ; SD Creator) Services DNS/DHCP/Infrastructures Partenaires"
next
edit 10
set dst 10.54.170.0 255.255.255.192
set gateway {routerVGF}
set device "internal"
set comment "Services Infrastructures SFR"
next
edit 11
set dst {mainSite["network"]} {mainSite["mask"]}
set gateway {routerVGF}
set device "internal"
set comment "Site principale {mainSite["name"]}"
next
end
config firewall address
edit "emul_3270"
set subnet 10.112.200.171 255.255.255.255
next
edit "KASPERSKY CARBASE"
set subnet 10.54.151.224 255.255.255.240
next
edit "LIAISON VERS CARBASE Roissy"
set subnet 10.54.94.0 255.255.255.128
next
edit "LAN-SITE-{site["name"]}"
set subnet 10.54.92.192 255.255.255.192
next
edit "LAN-SITE-PRINCIPALE-{mainSite["name"]}"
set subnet 10.54.167.192 255.255.255.192
next
edit "h_10.54.240.151 rpnbb"
set subnet 10.54.240.151 255.255.255.255
next
edit "h_10.54.112.123"
set subnet 10.54.112.123 255.255.255.255
next
edit "h_10.54.112.125"
set subnet 10.54.112.125 255.255.255.255
next
edit "h_10.112.198.242"
set subnet 10.112.198.242 255.255.255.255
next
edit "PLAGE-IP-VPNSSL-{site["name"]}"
set type iprange
set start-ip 10.91.142.5
set end-ip 10.91.142.65
next
end
config firewall addrgrp
edit "RESSOURCES-SSL-VPN"
set member "emul_3270" "h_10.112.198.242" "h_10.54.112.123" "h_10.54.112.125" "h_10.54.240.151 rpnbb" "LAN-{site["name"]}" "LAN-SITE-PRINCIPALE-{mainSite["name"]}" "LIAISON VERS CARBASE Roissy" "KASPERSKY CARBASE"
set color 15
next
end
config firewall policy
edit 1
set name "LAN vers WAN"
set srcintf "internal"
set dstintf "wan1"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "always"
set service "ALL"
set nat enable
next
edit 2
set name "INVITE vers WAN"
set srcintf "INVITE"
set dstintf "wan1"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "PLAGE ACCES WIFI INVITE"
set service "ALL"
set nat enable
next
edit 3
set name "LAN vers SSL-VPN"
set srcintf "internal"
set dstintf "ssl.root"
set srcaddr "LAN-{site["name"]}"
set dstaddr "PLAGE-IP-VPNSSL-{site["name"]}"
set action accept
set schedule "always"
set service "ALL"
set groups "GRP-USER-VPN-{site["name"]}"
next
edit 4
set name "SSL-VPN vers LAN"
set srcintf "ssl.root"
set dstintf "internal"
set srcaddr "PLAGE-IP-VPNSSL-{site["name"]}"
set dstaddr "LAN-{site["name"]}" "RESSOURCES-SSL-VPN"
set action accept
set schedule "always"
set service "ALL"
set groups "GRP-USER-VPN-{site["name"]}"
set nat enable
next
edit 5
set name "WIFI-AGENT vers LAN"
set srcintf "WIFI-AGENT"
set dstintf "internal"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "always"
set service "ALL"
set nat enable
next
edit 6
set name "WIFI AGENT vers WAN"
set srcintf "WIFI-AGENT"
set dstintf "wan1"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "always"
set service "ALL"
set nat enable
next
edit 7
set name "WIFI ATELIER vers WAN"
set srcintf "WIFI-ATELIER"
set dstintf "wan1"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "always"
set service "ALL"
set nat enable
next
edit 8
set name "WIFI ATELIER vers LAN"
set srcintf "WIFI-ATELIER"
set dstintf "internal"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "always"
set service "ALL"
set nat enable
next
edit 9
set name "WIFI DIGITAL vers LAN"
set srcintf "WIFI-DIGITAL"
set dstintf "internal"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "always"
set service "ALL"
set nat enable
next
edit 10
set name "WIFI DIGITAL vers WAN"
set srcintf "WIFI-DIGITAL"
set dstintf "wan1"
set srcaddr "all"
set dstaddr "all"
set action accept
set schedule "always"
set service "ALL"
set nat enable
next
end
config system dns
set primary {addressServerDC}
set secondary 8.8.8.8
set domain "{localDomain}"
config system global
set admin-sport 4430
set admintimeout 10
set hostname "{hostname}"
set timezone 28
""")

configFile.close()