# libraries
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request, Response
# from flask_ngrok import run_with_ngrok
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

base_folder ="/home/kratos-chatbot/chatbot"
# chat initialization
model = load_model(f"{base_folder}/bot_model.h5")
intents_file_path = f"{base_folder}/trained_bot.json"
with open(intents_file_path, encoding="utf-8") as json_file:
    intents = json.load(json_file)
#intents = json.loads(open(f"{base_folder}/trained_bot.json").read(encoding="utf-8"))
words = pickle.load(open(f"{base_folder}/words.pkl", "rb"))
classes = pickle.load(open(f"{base_folder}/classes.pkl", "rb"))

app = Flask(__name__)
# run_with_ngrok(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chatbot_response():
    print("HIT IN CHAT")
    msg = request.form["msg"]
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}", name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}", name)
    elif msg is None:
        msg = "Message is required"
        res = Response(msg)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    return res


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_words_from_sentence(sentence):
    sentence_words = sentence.split("*")
    words = []
    for word in sentence_words:
        word = word.strip()
        print(word,"word")
        words.append(word)
    words.pop(0) 
    return words


def get_question(sentence):
    sentence_words = sentence.split("*")
    question = sentence_words[0].strip()
    return question

def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            print(get_words_from_sentence(result))
            question = get_question(result)
            data = {
                
                "data": {
                    "message":question,
                    "options": get_words_from_sentence(result)
                }
            }
    return Response(json.dumps(data), content_type="application/json")


if __name__ == "__main__":
    app.run()
   # app.run(host='127.0.0.1', port=80)

