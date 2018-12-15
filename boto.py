"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests
import time

data = {'insult': ['fuck', 'shit', 'asshole'],
        'good_mood': ['good', 'fine', 'great', 'ok', 'cool'],
        'bad_mood': ['not good', 'bad', ],
        'yes_words': ['yes', 'yep', 'amazing', 'really', 'great'],
        'no_words': ['no', 'nop', 'not', 'hate'],
        'counter ': 0
        }


def main_function(input):
    input = input.lower()

    if data['counter'] == 0:
        return name(input)
    elif data['counter'] == 1:
        return feeling(input)
    elif data['counter'] == 2:
        return chocolate(input)
    elif 'joke' in input:
        return joke()
    elif 'weather' in input:
        return weather()
    elif 'time' in input:
        return current_time()
    else:
        return bydefault(input)


def joke():
    response = requests.get('http://api.icndb.com/jokes/random/')
    data = response.json()
    print(data)
    return data['value']['joke'], 'laughing'


def name(input):
    data['counter'] += 1
    name_of_him = input.split(' ')

    return 'Hello {0}! How are you ?'.format(name_of_him[-1]), 'excited'


def feeling(input):
    data['counter'] += 1
    if 'you' in input:
        return "I don't know what is to be fine, I am a bot...Maybe you can ask me if I love chocolate ?", 'giggling'
    elif any(x in input for x in data['good_mood']):
        return "Great ! So eat more Chocolate ! It's what I do when I am happy ! You love chocolate ?", 'dancing'
    elif any(x in input for x in data['bad_mood']):
        return "Sorry to hear ! Maybe you can eat chocolate ! It's good against depression. You like eat ?", 'crying'
    else:
        return bydefault(input)


def chocolate(input):
    data['counter'] += 1
    if 'chocolate' and '?' in input:
        return "Do you see that I don't have a mouse ?", 'confused'
    elif any(x in input for x in data['yes_words']):
        return 'Me too ! We have one common point !!', 'inlove'
    elif any(x in input for x in data['no_words']):
        return 'You miss something !', 'heartbroke'
    else:
        return bydefault(input)


def bydefault(input):
    data['counter'] += 1
    if 'ok' or 'no' or 'lol' or 'yes' in input:
        return 'Do you want something else ? A joke, the weather , the time ...?', 'bored'


def weather():
    response = requests.get('https://api.darksky.net/forecast/23c4c8019ce8863da0a69ee108855c5f/32.0808800,34.7805700')
    data = response.json()
    summary = data['currently']['summary'], data['currently']['temperature']
    return 'The time and the temperature of the day in Fahrenheit are {0}'.format(summary), 'waiting'


''


def current_time():
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)
    return "I give you the time and the date ! I'm good no ? {0}".format(localtime), 'afraid'


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    (user_message, animation) = main_function(user_message)
    return json.dumps({"animation": animation, "msg": user_message})


@route("/test", method='POST')
def chat():
    data['counter'] = 0
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
