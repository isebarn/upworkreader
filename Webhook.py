import requests
from time import sleep

url = "https://discordapp.com/api/webhooks/735913557207548307/oYw_RP-TLMuSxaXPatcvQ0UTskgUbw4ana-jgUwX_Hdt0utu1qU8hjLEjjYIAwG9ZZcm"

def send_messages(ads):

  for message in ads:
    msg = '{}\n{}'.format(message['title'], message['payment'])
    data = {}
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["content"] = msg

    data["embeds"] = []
    embed = {}
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    embed["description"] = message["body"]
    embed["url"] = message['url']
    embed["title"] = message["url"]
    data["embeds"].append(embed)

    result = requests.post(url, json=data, headers={"Content-Type": "application/json"})

    '''
    if int(result.headers['x-ratelimit-remaining']) == 0:
        print("Ratelimit hit")
        sleep(int(result.headers['x-ratelimit-remaining']) + 2)
    '''
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


def send_html(html):

    data = {}
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["username"] = "New Ad"

    #leave this out if you dont want an embed
    data["embeds"] = []
    embed = {}
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    embed["description"] = html
    #embed["title"] = "embed title"
    data["embeds"].append(embed)

    result = requests.post(url, json=data, headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))



if __name__ == "__main__":

  ads = [{'id': '01d33e2d5b0742ea28', 'title': 'Lead generation to find MSPs in USLead generation to find MSPs in US', 'url': 'https://www.upwork.com/job/Lead-generation-find-MSPs_~01d33e2d5b0742ea28/', 'payment': 'Fixed: $10', 'body': 'Body'}]

  a = send_messages(ads)

