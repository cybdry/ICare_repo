#!/usr/bin/env python
# -*- coding: utf-8 -*-


import spacy

load_model = spacy.load('en_core_web_sm',disable= ['parser','ner'])

requirements = ["budget","insurance","chronic","disease","yearly",
                "income","family","package","job","beneficiary"]

def requirement_check(message):
    
    doc = load_model(message)
    message = " ".join([token.lemma_ for token in doc])
    print(message)
    message_split = message.split(" ")

    if set(requirements).issubset(set(message_split)):
        return True, set(message_split).intersection(requirements)
    else:
        return False,set(message_split).intersection(requirements)

def question_user(intents):

    base = "Sorry, can we also have information about your "
    for intent in intents:
        if intent.upper() == "INSURANCE":
            base += intent + " package,"
        else:
            base += intent + ", "
    # Replacing the end "," by "?"
    base = base[:-1] + "?"
    return base


def user_requirement(message):
    key,value = requirement_check(message)

    if not key:
        value = set(requirements).difference(set(value))
        return False, message, question_user(value)
    else:
        True, message

# test the function

if __name__ == "__main__":
    pass
    #message = "I am looking for a suitable medical insurance package based on the following specifications:\n I have a chronics diseases like diabete and but budget is 2000 dollard. My yearly income is 60000 dollard.My family have "
    #print(user_requirement(message))
