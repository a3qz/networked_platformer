import json


num_as_key = {}
str_as_key = {}
with open("cardlist") as f:
    for card in f:
        card = card.strip()
        build = "9"
        if "spades" in card:
            build += "1"
        elif "hearts" in card:
            build += "2"
        elif "diamonds" in card:
            build += "3"
        elif "clubs" in card:
            build += "4"
        
        build += "9"

        if "ace" in card:
            build += "1"
        elif "king" in card:
            build += "13"
        elif "queen" in card:
            build += "12"
        elif "jack" in card:
            build += "11"
        else:
            if card[0] == "1":
                build += "10"
            else:
                build += card[0]
        
        str_as_key[card] = build
        num_as_key[build] = card
    


print json.dumps(num_as_key)    
