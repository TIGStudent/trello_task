from flask import Flask, render_template
import ivy_trello_api as trello_api

app = Flask(__name__)

@app.route('/')
def newivy():

    cards_active = trello_api.get_list(trello_api.list_id_aktive)
    cards_done = trello_api.get_list(trello_api.list_id_done)

    card_list_active = ""
    card_list_done = ""
    
    for card in cards_active:
        card_list_active += card['name']+"\n"
    
    for card in cards_done:
        card_list_done += card['name']+"\n"
    
    return render_template('index.html', card_list=card_list_active, card_list_done=card_list_done)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
