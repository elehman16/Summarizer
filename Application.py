"""
Created on Mon Jan 22 17:54:50 2018

@author: Eric
"""

import flask
from Model import Model
from werkzeug.datastructures import FileStorage

application = flask.Flask(__name__)

"""
Display the main page.
"""
@application.route('/', methods=['GET']) 
def index():
    return flask.render_template('index.html', text = '', user_response = '')
    

"""
Start the program.
"""
@application.route('/summarize/', methods=['GET', 'POST'])
def summarize():
    text = flask.request.form['text-to-summarize']
    user_response = Model().summarize(text)
    user_response = user_response[0] # these are the actually important sentences (rest is vocab)
    return flask.render_template('index.html', 
                                 text = text, 
                                 user_response = user_response)

"""
Start the program.
"""
@application.route('/key_vocab/', methods=['GET', 'POST'])
def key_vocab():
    text = flask.request.form['text-to-summarize']
    user_response = Model().summarize(text)
    user_response = user_response[1] 
    return flask.render_template('index.html', 
                                 text = text, 
                                 user_response = user_response)
                                 
"""
Display text of an image.
"""
@application.route('/', methods = ['GET', 'POST'])
def upload():
    file = flask.request.files['pic']
    file.save(file.filename)
    try:
        text = Model().picture_to_text(file.filename)
    except:
        text = "Unable to convert file into text."
        
    import pdb; pdb.set_trace()
    return flask.render_template('index.html',  
                                 text = text, 
                                 user_response = '')



"""
Run the application.
"""
if __name__ == '__main__':
    application.run()

