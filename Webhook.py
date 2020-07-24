import requests

def send_messages(ads):
  url = "https://discordapp.com/api/webhooks/735913557207548307/oYw_RP-TLMuSxaXPatcvQ0UTskgUbw4ana-jgUwX_Hdt0utu1qU8hjLEjjYIAwG9ZZcm"

  for message in ads:
    msg = '{}\n{}\n{}'.format(message['title'], message['payment'], message['url'])
    data = {}
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["content"] = msg
    data["username"] = "New Ad"

    #leave this out if you dont want an embed
    #data["embeds"] = []
    #embed = {}
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    #embed["description"] = "text in embed"
    #embed["title"] = "embed title"
    #data["embeds"].append(embed)

    result = requests.post(url, json=data, headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


if __name__ == "__main__":

  ads = [{'id': '01d33e2d5b0742ea28', 'title': 'Lead generation to find MSPs in USLead generation to find MSPs in US', 'url': 'https://www.upwork.com/job/Lead-generation-find-MSPs_~01d33e2d5b0742ea28/', 'payment': 'Fixed: $10'}]

  send_messages(ads)

