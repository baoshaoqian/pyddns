import requests
import json


def list_dns_records(auth_email, api_key, zone_identifier, proxies=None):
    url = (
        "https://api.cloudflare.com/client/v4/zones/%(zone_identifier)s/dns_records"
        % {"zone_identifier": zone_identifier}
    )

    headers = {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, proxies=proxies)
    return response


def update_dns_record(auth_email, api_key, zone_identifier, record_identifier, record_name, ip):
    url = (
        "https://api.cloudflare.com/client/v4/zones/%(zone_identifier)s/dns_records/%(record_identifier)s"
        % {"zone_identifier": zone_identifier, "record_identifier": record_identifier}
    )

    headers = {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = json.dumps(
        {
            "name": record_name,
            "type": "A",
            "content": ip,
            "ttl": 1,
            "proxied": False,
            "comment": "Updated with Cloudflare API",
        }
    )
    response = requests.put(url, headers=headers, data=payload)
    return response


def is_dns_update_sccessful(response):
    if response.status_code == 200:
        response_json = json.loads(response.text)
        # Check if the update was successful
        if response_json["success"]:
            return True
    return False
