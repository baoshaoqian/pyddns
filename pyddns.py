import time
from dotenv import dotenv_values
from iputils import *
from cloudflareapi import *
from discordapi import *


CHECK_INTERVAL = 300

IP_DETECTION_URLS = ["http://myip.ipip.net", "ip.qaros.com", "ip.3322.net"]

# Load config from .env file
config = dotenv_values(".env")
AUTH_EMAIL = config.get("AUTH_EMAIL")
API_KEY = config.get("API_KEY")
ZONE_IDENTIFIER = config.get("ZONE_IDENTIFIER")
RECORD_IDENTIFIER = config.get("RECORD_IDENTIFIER")
RECORD_NAME = config.get("RECORD_NAME")
IP_SOURCE = config.get("IP_SOURCE")
IPV6_SOURCE = config.get("IPV6_SOURCE")
DISCORD_WEBHOOK = config.get("DISCORD_WEBHOOK")


def get_ip_from_urls(url_list):
    for url in url_list:
        ip = get_ip_from_url(url)
        if ip:
            return ip
        else:
            post_message("Failed to get IP from %s" % url)
    return None


# Source can be "url", "wan"(for OpenWrt) or interface name(e.g. "eth1", "enp0s0")
def get_ip(source):
    if source == "wan":
        ip = get_ip_from_wan()
    elif source == "url":
        ip = get_ip_from_urls(IP_DETECTION_URLS)
    else:
        ip = get_ip_from_interface(source)
    return ip


def post_message(message):
    print(message)
    if DISCORD_WEBHOOK:
        message_discord_webhook(message, DISCORD_WEBHOOK)


def main():
    last_ip = ""
    while True:
        ip = get_ip(IP_SOURCE)
        if ip:
            if ip != last_ip:
                response = update_dns_record(
                    AUTH_EMAIL,
                    API_KEY,
                    ZONE_IDENTIFIER,
                    RECORD_IDENTIFIER,
                    RECORD_NAME,
                    ip,
                )
                if is_dns_update_sccessful(response):
                    post_message("Successfully updated DNS record: \n" + response.text)
                    last_ip = ip
                else:
                    post_message("Failed to update DNS record: \n" + response.text)
        else:
            post_message("Failed to get IP from %s" % IP_SOURCE)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
