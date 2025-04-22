import requests
import json
import datetime
import time
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

url = "https://www.hotukdeals.com/rest_api/v2/thread"

querystring = {
    "criteria": "{\n  \"merchant\" : null,\n  \"tab\" : \"new\",\n  \"user\" : null,\n  \"whereabouts\" : \"deals\",\n  \"show_clearance\" : true,\n  \"group\" : null,\n  \"query\" : null,\n  \"event\" : null,\n  \"location_ids\" : null\n}",
    "limit": "20",
    "page": "1"
}

headers = {
    # Replace with headers
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()

webhook_url = ""  # Replace with your Discord webhook URL
footer_image_url = "https://i.imgur.com/Yx4vbrg.gif"  # Replace with your footer image URL
seen_deals = []

# Iterate over the deals
while True:
    print(Fore.YELLOW + "Fetching new set of deals...")
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(Fore.YELLOW + f"Fetch status code: {response.status_code}")

    data = response.json()
    new_deals_found = False  # Whether or not we found any new deals this time

    for deal in data['data']:
        if deal['thread_id'] not in seen_deals:
            seen_deals.append(deal['thread_id'])

            title = deal['title']
            price = 'Free' if deal.get('price') is None else f'£{deal["price"]}'
            temperature = 'New' if deal.get('temperature_rating', 0) == 0 else deal.get('temperature_rating')
            image_url = deal.get('image', {}).get('uri', '')
            deal_url = deal['deal_uri']

            discord_data = {
                "username": "J Code",
                "avatar_url": "https://i.imgur.com/Yx4vbrg.gif",
                "attachments": [],
                "embeds": [{
                    "title": title,
                    "color": 4321431,    
                    "url": deal_url,
                    "description": f"Price: {price}\nTemperature: {temperature}",
                    "thumbnail": {"url": image_url},
                    "footer": {
                        "text": "J Code",
                        "icon_url": footer_image_url,
                    },
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z"

                }],
            }

            response = requests.post(webhook_url, data=json.dumps(discord_data), headers={"Content-Type": "application/json"})
            if response.status_code != 204:
                print(Fore.RED + f"Discord webhook returned an error {response.status_code}, the response is: {response.text}")
            else:
                new_deals_found = True
                print(Fore.GREEN + "New deal found and posted to Discord!")

    if not new_deals_found:
        print(Fore.RED + "No new deals found.")

    # Wait for 10-20 seconds
    time.sleep(15)
