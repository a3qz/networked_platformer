import json

# loads in the two json libraries that we use as reference: {card_descriptor: card_imagename} and the other way around for use in loading images
fp1 = open("num_as_key.json")
fp2 = open("str_as_key.json")
num_as_key = json.load(fp1)
str_as_key = json.load(fp2)


