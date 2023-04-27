#!/usr/bin/env python
# -*- coding: utf-8 -*-


import spacy

load_model = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

requirements = ["budget", "insurance", "chronic", ]  # "disease", "annual",
# "income", "package", "job", "beneficiary"]


def requirement_check(message):

    doc = load_model(message)
    message = " ".join([token.lemma_ for token in doc])
    message_split = message.split(" ")

    if set([text.lower() for text in requirements]).issubset(set([text.lower() for text in message_split])):
        return True, set(message_split).intersection(requirements)
    else:
        return False, set(message_split).intersection(requirements)


def question_user(intents):

    base = "Sorry, can we also have information about your "

    if ("insurance" or "package") in intents:
        base += " insurance package, "
    if ("chronic" or "disease") in intents:
        base += "chronics diseases, "
    if ("annual" or "income") in intents:
        base += "annual income, "
    if "beneficiary" in intents:
        base += "beneficiary "
    if "job" in intents:
        base += " and your current job "
    else:
        for intent in intents:
            base += intent + ", "

    base = base[:-2] + "?"
    return base


def user_requirement(message):
    key, value = requirement_check(message)

    if not key:
        value = set([requirement.lower()
                    for requirement in requirements]).difference(set(value))
        print("New value: ", value)
        return False, message, question_user(value)
    else:
        return True, message

# test the function


# if __name__ == "__main__":
    # message = "I am looking for a suitable medical insurance package based on the following specifications:\n
    #  I have a chronics diseases like diabete and but  is 2000 dollard. My yearly income is 60000 dollard. my current job is developer add the beneficire is my son "
    # print(user_requirement(message))

 #   message = "I am looking for a suitable medical insurance package based on the following specification. I have a chronic disease like diabetes, but budget my  is $2000. My annual income is $16,000. My current job is developer and the beneficiary is my son."
  #  print(user_requirement(message))
