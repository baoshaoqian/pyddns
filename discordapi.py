import requests


# Post a message to a discord webhook
def message_discord_webhook(message, webhook_url, proxies=None):
    headers = {"Content-Type": "application/json"}
    json = {"content": "{}".format(message)}
    response = requests.post(webhook_url, headers=headers, json=json, proxies=proxies)
    return response
