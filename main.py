###### VAR ######
## INFO CLIENT
main_site = { 
    "name": "Donjon",
    "network": "10.54.133.128",
    "mask": "255.255.255.128"
}
address_server_dc = "10.54.133.133"
## INFO SITE CLIENT
site = {
    "name": "ABSOLUTE",
    "network": "10.54.70.0",
    "mask": "255.255.255.0"
}
hostname = "AU-ABSOLUTE"
local_domain = "fr02410"
netbios = "FVW5487S1DS"
ad_admin_pass = "xxxxx"
router_vgf = "10.54.75.1" 
box_internet_ip = "192.168.1.1"
passphrase_invite = "INVITE"
atelier_exist = True
site_principale = False

## WIFI
# Adresses réseaux des wifi, ajouter +10 sur le 3eme octet.
wifi_network = {
    "INVITE" : "172.16.190",
    "AGENT" : "172.16.200",
    "ATELIER" : "172.16.210",
    "DIGITAL" : "172.16.220"
}

##########################################################
############## NE PAS EDITER EN DESSOUS ##################
##########################################################

# Creation de bloc de configuration que l'on concatene à la fin.

# Liaison LDAP
cli_ldap = f"""config user ldap
edit "AD {main_site["name"]}"
set server "10.20.30.40"
set cnid "SAMAccountName"
set dn "dc={local_domain},dc=vw-group,dc=com"
set type regular
set username "{netbios}\\admin"
set password {ad_admin_pass}
next
end"""
# Groupes utilisateurs

cli_groups = f"""config user group
edit "GRP-USER-VPN-{site["name"]}"
set member "AD {main_site["name"]}"
config match
edit 1
set server-name "AD {main_site["name"]}"
set group-name "CN=AD-VPN-USERS,CN=Users,DC={local_domain},DC=vw-group,DC=com"
next
end
next
edit "GRP-AGENT-site"
set member "AD {main_site["name"]}"
config match
edit 1
set server-name "AD {main_site["name"]}"
set group-name "CN=AD-VPN-USERS,CN=Users,DC={local_domain},DC=vw-group,DC=com"
next
next
edit "GRP-DIGITAL-{site["name"]}"
next
end"""

if atelier_exist == True:
    cli_groups += f"""config user group
edit "GRP-ATELIER-{site["name"]}"
next
end
"""

## WIFI SSID

# Définition de la liste des SSID à créer
if atelier_exist == True:
    ssid_list = ["AGENT" ,"DIGITAL", "ATELIER"]
else:
    ssid_list = ["AGENT" ,"DIGITAL"]

cli_ssid = ""

# Création du bloc de commandes
for ssid in ssid_list:
    cli_ssid += f"""config wireless-controller vap
edit WIFI-{ssid}
set ssid "WIFI-{ssid}-{site["name"]}"
set broadcast-ssid enable
set security wpa2-only-enterprise
set auth usergroup
set usergroup "GRP-WIFI-{ssid}-{site["name"]}"
set schedule always
set vdom root
end
config system interface
edit WIFI-{ssid}
set ip {wifi_network[ssid]}.1 255.255.255.0
end"""

# Ajout du bloc de commande pour WIFI INVITE
cli_ssid += f"""config wireless-controller vap
edit WIFI-INVITE
set ssid "WIFI-INVITE-{site["name"]}"
set broadcast-ssid enable
set security wpa2-only-personnal
set passphrase {passphrase_invite}
set schedule PLAGE-{site["name"]}
set vdom root
end
config system interface
edit WIFI-INVITE
set ip {wifi_network["INVITE"]}.1 255.255.255.0
end"""

# Test bloc WIFI SSID
# with open("fortigate.conf","w") as file:
#     file.write(cli_ssid)

# DHCP Server
cli_dhcp = f"""config system dhcp server
edit 0
set default-gateway 10.10.120.1
set dns-service default
set interface WIFI-INVITE
set netmask 255.255.255.0
config ip-range
edit 1
set end-ip 10.10.120.9
set start-ip 10.10.120.2
end
"""

# Plages horaires
cli_schedule = f"""
config firewall schedule recurring
edit "PLAGE ACCES WIFI INVITE"
set start 08:00
set end 19:00
set day monday tuesday wednesday thursday friday saturday
next
end"""

# FortiAP profile
cli_fortiap_profile = f"""
edit "FAPU421EV"
config platform
set type U421E
end
set handoff-sta-thresh 30
set ap-country FR
set allowaccess https ssh snmp
config radio-1
set band 802.11n
set frequency-handoff enable
set ap-handoff enable
set vap-all enable
set channel "1" "6" "11"
end
config radio-2
set band 802.11ac
set frequency-handoff enable
set ap-handoff enable
set channel "36" "40" "44" "48" "52" "56" "60" "64" "100" "104" "108" "112" "116" "120" "124" "128" "132" "136" "140"
end
next
"""

# Routes statiques
cli_static_routes = f"""config router static
edit 1
set dst 0.0.0.0 0.0.0.0
set gateway {box_internet_ip}
set device "wan1"
set comment "Internet"
next
edit 2
set dst 10.6.0.0 255.255.0.0
set gateway {router_vgf}
set device "internal"
set comment "Plateforme Internet Datacenter SFR"
next
edit 3
set dst 10.54.240.157 255.255.255.255
set gateway {router_vgf}
set device "internal"
set comment "cpn.gvf"
next
edit 4
set dst 10.54.94.0 255.255.255.128
set gateway {router_vgf}
set device "internal"
set comment "Liaison Roissy CE CAR*Base"
next
edit 5
set dst 10.112.224.0 255.255.248.0
set gateway {router_vgf}
set device "internal"
set comment "Extranet GVF"
next
edit 6
set dst 10.54.248.0 255.255.248.0
set gateway {router_vgf}
set device "internal"
set comment "SD Creator"
next
edit 7
set dst 10.60.0.0 255.255.0.0
set gateway {router_vgf}
set device "internal"
set comment "Support N2, Services EPO/WSUS VAS, Reverse Proxy 071219"
next
edit 8
set dst 10.112.192.0 255.255.192.0
set gateway {router_vgf}
set device "internal"
set comment "Coeur de réseau partenaire (sur-réseau)"
next
edit 9
set dst 10.54.240.128 255.255.255.192
set gateway {router_vgf}
set device "internal"
set comment "(cpn.gvf ; SD Creator) Services DNS/DHCP/Infrastructures Partenaires"
next
edit 10
set dst 10.54.170.0 255.255.255.192
set gateway {router_vgf}
set device "internal"
set comment "Services Infrastructures SFR"
next
edit 11
set dst {main_site["network"]} {main_site["mask"]}
set gateway {router_vgf}
set device "internal"
set comment "Site principale {main_site["name"]}"
next
end
"""

# Objets addresse
cli_firewall_address = f"""config firewall address
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
edit "LAN-SITE-PRINCIPALE-{main_site["name"]}"
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
set member "emul_3270" "h_10.112.198.242" "h_10.54.112.123" "h_10.54.112.125" "h_10.54.240.151 rpnbb" "LAN-{site["name"]}" "LAN-SITE-PRINCIPALE-{main_site["name"]}" "LIAISON VERS CARBASE Roissy" "KASPERSKY CARBASE"
set color 15
next
end
"""

# Règles de firewall
cli_policy = f"""config firewall policy
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
"""
# Config système : DNS, port 4430, timeout, etc...
cli_system = f"""config system dns
set primary {address_server_dc}
set secondary 8.8.8.8
set domain "{local_domain}.vw-group.com"
config system global
set admin-sport 4430
set admintimeout 10
set hostname "{hostname}"
set timezone 28
"""
# Ouverture/Création du fichier de config
config_file = open("fortigate.conf", "w")

# Concaténation des différents bloc
config_file.write(cli_dhcp + cli_firewall_address + cli_policy + cli_ssid + cli_static_routes + cli_system)

config_file.close()