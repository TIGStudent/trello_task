
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
list_id_done = os.getenv('LIST_ID_DONE')
list_id_aktive = os.getenv('LIST_ID_AKTIVE')


#timer for whan tha api call incounters a error
def retry_timer():
    min_retry = 60

    for t in range(min_retry, 0, -1):
        print(f'Will retry API in {t} min')
        time.sleep(60)

#gets tha list "Har gjort" which is tha done list
def get_list(list_id: str) -> list:
    url = f'https://api.trello.com/1/lists/{list_id}/cards?key={api_key}&token={token}'

    while True:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                cards = response.json()
                return cards
            else:
                print(f"Failed to get cards with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed with error: {e}")
            retry_timer()

#cates the actions for the card
def get_card_actions(card_id: str):
    url = f"https://api.trello.com/1/cards/{card_id}/actions?key={api_key}&token={token}"

    response = requests.get(url)

    if response.status_code == 200:
        actions = response.json()
        return actions
    else:
        print(f"Failed to fetch actions for card {card_id}: {response.status_code}")
        return []

#moves the card to new list
def move_trello_card(card_id: str, new_list_id: str) -> None:
    url = f"https://api.trello.com/1/cards/{card_id}"
    headers = {"Accept": "application/json"}
    query = {
        'key': api_key,
        'token': token,
        'idList': new_list_id,
        'pos': 'top'
    }

    while True:
        try:
            response = requests.put(url, headers=headers, params=query)

            if response.status_code == 200:
                print("Card moved successfully.")
                return
            else:
                print(f"Failed to move card: {response.status_code} {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed with error: {e}")
            retry_timer()


if __name__ == "__main__":

    move_trello_card(card_id="6612575d4bc444e08919869a", new_list_id=list_id_aktive)
    cards = get_list(list_id_aktive)
    cards2 = get_list(list_id_done)
    
    print("\nAktiv")
    for card in cards:
            print(f"{card['name']}{card['id']}")

    print("\ndone")
    for card in cards2:
        print(f"{card['name']}{card['id']}")