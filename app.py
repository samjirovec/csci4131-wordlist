from flask import Flask, request, Response, render_template, json, jsonify, flash
import requests
import re
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

#Key to use on webster api
key = '325142d6-6793-4d6f-8f67-8b23d76755e0'


# Select field added in the template, validation inside of the function itself, not the form.
class WordForm(FlaskForm):
    avail_letters = StringField("Letters")
    submit = SubmitField("Go")

csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    form = WordForm()
    return render_template("index.html", form=form)


@app.route('/words', methods=['POST','GET'])
def letters_2_words():


    form = WordForm()
    if form.validate_on_submit():
        letters = form.avail_letters.data
        # This is just to show how to get the word length from the request form.
        print(request.form.get('wordlength'))
        word_length = request.form.get('wordlength')
        pattern = request.form.get('pattern')
        print(request.form.get('pattern'))
        if ((letters == '' and pattern == '')):
            return render_template("index.html", form=form)
        elif (word_length != 'default' and len(pattern) != int(word_length) and pattern != ''):
            return render_template("index.html", form=form)
    else:
        return render_template("index.html", form=form)

    with open('sowpods.txt') as f:
        good_words = set(x.strip().lower() for x in f.readlines())

    #build the set and depending on the parameters passed in via the form, utilize word length or pattern.
    word_set = set()
    if letters != '':
        for l in range(3,len(letters)+1):
            for word in itertools.permutations(letters,l):
                w = "".join(word)
                if w in good_words:
                    if word_length != 'default':
                        if int(word_length) == len(w) and re.fullmatch(pattern,w) != None and pattern != '':
                            word_set.add(w)
                        elif int(word_length) == len(w) and pattern == '':
                            word_set.add(w)
                    else:
                        if re.fullmatch(pattern,w) != None and pattern != '':
                            word_set.add(w)
                        elif pattern == '':
                            word_set.add(w)
    #Same Pattern, just go through all words if none are specified.
    else:
        for w in good_words:
             if word_length != 'default':
                if int(word_length) == len(w) and re.fullmatch(pattern,w) != None and pattern != '':
                    word_set.add(w)
                elif int(word_length) == len(w) and pattern == '':
                    word_set.add(w)
             else:
                if re.fullmatch(pattern,w) != None and pattern != '':
                    word_set.add(w)
                elif pattern == '':
                    word_set.add(w)


    #sorting the word list first by alphabet and then by length.
    wordlist = list(word_set)
    wordlist = sorted(wordlist)
    wordlist = sorted(wordlist,key=len,reverse=True)

    return render_template('wordlist.html',
        wordlist=wordlist,
        name="CS4131")


#New Route to make requests from the flask app, this hides the api key from the users who can see the Javascript.
@app.route('/def/<word>', methods=['GET'])
def getDef(word):
    resp = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + key)
    data = resp.json()
    if type(data[0]) != dict:
        return jsonify('No Def. Found')
    else:
        alt_def = data[0]['shortdef']
        return jsonify(alt_def)


@app.route('/proxy')
def proxy():
    result = requests.get(request.args['url'])
    resp = Response(result.text)
    resp.headers['Content-Type'] = 'application/json'
    return resp


