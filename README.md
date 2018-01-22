License: Affero General Public License v3.0

The purpose of this project is to summarize text, and also highlight key vocab terms that appear often. This project will follow the model, view, and controller template. 

The model has two main jobs:
	1. Summarize text and return main vocab words
	2. Take a document and parse it into text.

The View will be written in JavaScript + HTML + CSS. This has yet to be done.

The Controller will be written in Python using Flask. It will be the bridge between the JavaScript and the Python code.

Future Work improvements:
	1. Try various AI techniques for selecting sentences. This could mean expanding the current model to deal with similar words. For example, the model, working with a passage about computers, would classify a "Laptop" and a "computer" differently.
	2. Add Neural Networks and other NLP methods to replace the simplistic AI model.

