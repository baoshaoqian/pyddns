import subprocess
import requests
import re


def get_ip_from_url(url) -> str:
    response = requests.get(url)
    # Use regular expression to get the ip from the string
    ip = re.findall(r"\d+.\d+.\d+.\d+", response.text)[0]
    return ip


def get_ip_from_interface(interface) -> str:
    command = "ip -4 addr show %s | sed -Ene 's/^.*inet ([0-9.]+)\\/.*$/\\1/p'" % interface
    ip = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    return ip


def get_ipv6_from_interface(interface) -> str:
    command = "ip -6 addr show %s | sed -Ene 's/^.*inet6 ([0-9a-fA-F:]+)\\/.*$/\\1/p'" % interface
    ip = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    return ip


# This fuction is for OpenWRT
def get_ip_from_wan() -> str:
    command = "ifstatus wan | jsonfilter -e '@[\"ipv4-address\"][0].address'"
    # Alternatively:
    # command = '. /lib/functions/network.sh; network_find_wan NET_IF; network_get_ipaddr NET_ADDR "${NET_IF}"; echo "${NET_ADDR}"'
    ip = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    return ip


# This fuction is for OpenWRT
def get_ipv6_from_wan() -> str:
    command = "ifstatus wan6 | jsonfilter -e '@[\"ipv6-address\"][0].address'"
    # Alternatively:
    # command = '. /lib/functions/network.sh; network_find_wan6 NET_IF6; network_get_ipaddr6 NET_ADDR6 "${NET_IF6}"; echo "${NET_ADDR6}"'
    ip = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    return ip


# Reference: https://forum.openwrt.org/t/how-to-get-current-public-ip-address-using-uci/40870/23
