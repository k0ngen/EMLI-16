sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
nmcli d wifi hotspot ifname wlan0 ssid EMLI_Team16 password emliteam16
sudo sysctl -w net.ipv4.ip_forward=1
