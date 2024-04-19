import ivy_trello_api as trello_api
import datetime
import time

#calculates the diffrences between date the card was last don with the current date
def date_diff(card_done_date:str) -> int:
    done_date = datetime.datetime.strptime(card_done_date, '%Y-%m-%d').date()
    current_date = datetime.date.today()
    date_diff = (current_date-done_date).days

    return date_diff

#finds tha last time the card where moved to tha "Har gjort" list, which is tha done list
def date_last_time_done(card_id):
    actions = trello_api.get_card_actions(card_id)

    for action in actions:
        if action['type'] == 'updateCard' and 'listAfter' in action['data']:
            if action['data']['listAfter']['name'] == "Har gjort":
                
                return action['date'][:10]
    return "9999-12-31"

#used to set the target for the next time the ecript will update the list when run as main
def set_terget_time() -> datetime:
    target_hour = 1
    target_minute = 0
    now = datetime.datetime.now()
    target_time = datetime.datetime(now.year, now.month, now.day, target_hour, target_minute)

    return target_time

#The main function responsible for chaking and updating the cards
def renew_cards() -> None:
    cards = trello_api.get_list(trello_api.list_id_done)

    for card in cards:
        card_id = card["id"]

        for card_tag in card["labels"]:
            if card_tag["name"][:11] == "Tillbaka om":
                card_done_date = date_last_time_done(card_id)
                dagar = int(card_tag["name"][12:16])
                date_to_update = date_diff(card_done_date)

                print(f"Ska updaters om: {dagar}")
                print(f"Dagar kvar till updatering: {dagar-date_to_update}")
                            
                if date_to_update >= dagar:
                    trello_api.move_trello_card(card_id=card_id, new_list_id=trello_api.list_id_aktive)
                    print("   card moved")
                    break
                else:
                    print("   card not moved, too early")
                    break

if __name__ == "__main__":

    while True:
        renew_cards()

        target_time = set_terget_time()
        now = datetime.datetime.now()

        if now >= target_time:
            target_time += datetime.timedelta(days=1)

        sleep_seconds = (target_time - now).total_seconds()
        time.sleep(sleep_seconds)