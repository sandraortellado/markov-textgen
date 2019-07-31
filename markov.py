from flask import Flask, render_template, redirect, request, session
import sys
import random
import numpy as np
import os
 
app = Flask(__name__)
IMG_FOLDER = os.path.join('static','images')
CSS = os.path.join('static','css')
JS = os.path.join('static','js')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER
# Trump3 = os.path.join(app.config['UPLOAD_FOLDER'], 'Trump3.jpg')
# coldone= os.path.join(app.config['UPLOAD_FOLDER'], 'coldone.jpg')
donniedrawing= os.path.join(app.config['UPLOAD_FOLDER'], 'donniedrawing.jpg')
merged= os.path.join(app.config['UPLOAD_FOLDER'], 'merged.jpg')

app.config['CSS_FILES'] = CSS
index_css = os.path.join(app.config['CSS_FILES'], 'index.css')
production_css = os.path.join(app.config['CSS_FILES'], 'production.css')
gradient_css = os.path.join(app.config['CSS_FILES'], 'gradient-buttons.min.css')
fontawesome_css = os.path.join(app.config['CSS_FILES'], 'fontawesome.css')

app.config['JS'] = JS
profile = os.path.join(app.config['JS'], 'profile.js')






@app.route("/")
def home():
    return render_template('index.html',
    donniedrawing=donniedrawing,
    merged=merged,
    index_css=index_css,
    production_css = production_css,
    gradient_css = gradient_css,
    fontawesome_css = fontawesome_css,
    profile = profile
    )

@app.route("/tweet", methods=['POST']) 
def run():
    def make_dict(file, N):
        #Inputs: text file and window size
        #Outputs: a dictionary mapping keys of windows to following words

        #Read text file into a numpy array split on spaces
        with open(file) as f: 
            contents = f.read()
        words = contents.split(' ')


        #Loop through the words and construct the dictionary for the N-gram
        word_dict = {}
        index = N
        for word in words[index:]:
            #Splits words into windows and formats into a space separated string
            key = ' '.join(words[index-N:index])
            if key in word_dict:
                word_dict[key].append(word)
            else:
                word_dict[key] = [word]
            index += 1
    
        return word_dict
    
    
    def generate(word_dict, seq_len):    
        #Inputs: dictionary mapping windows of words to following words, words to sample
        #Outputs: returns a generated string by sampling from the dictionary


        #starting window
        key_list = list(word_dict.keys())
        curr_window = random.choice(key_list)

        #String to eventually return
        string = curr_window
    
        for i in range(seq_len):
            try:
                new_word = random.choice(word_dict[curr_window])
                string += ' ' + new_word 
                #Slide the window forward by 1
                temp_window = curr_window.split(' ')
                temp_window.append(new_word)
                temp_window = temp_window[1:]
                curr_window = ' '.join(temp_window)

            except KeyError:
                return string

        return string

    # if __name__ == '__main__':
    my_dict = make_dict('combined.txt', 3)
    random_string = generate(my_dict, 50)
        # print(random_string)
    return render_template('index_with_tweet.html',tweet=random_string,
    donniedrawing=donniedrawing,
    merged=merged,
    index_css=index_css,
    production_css = production_css,
    gradient_css = gradient_css,
    fontawesome_css = fontawesome_css,
    profile = profile)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)