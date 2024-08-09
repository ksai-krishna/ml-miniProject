from flask import Flask, request, render_template, redirect, url_for
import openai
import os
import json

app = Flask(__name__)

# Set your OpenAI API key here
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

poetry_chat_history_file = 'poetry_chat_history.json'
creative_writing_chat_history_file = 'creative_writing_chat_history.json'
kannada_poetry_chat_history_file = 'kannada_poetry_chat_history.json'

def load_chat_history(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_chat_history(chat_history, filename):
    with open(filename, 'w') as f:
        json.dump(chat_history, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/poetry', methods=['GET', 'POST'])
def poetry():
    chat_history = load_chat_history(poetry_chat_history_file)
    if request.method == 'POST':
        user_message = request.form['poetry_text'].strip()
        if user_message:
            chat_history.append({'sender': 'User', 'message': user_message})

            # Get the response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a famous poet."},
                    {"role": "user", "content": f"Generate a poem based on the following text:\n{user_message}"}
                ],
                max_tokens=50
            )
            bot_message = response['choices'][0]['message']['content']
            chat_history.append({'sender': 'Bot', 'message': bot_message.replace('\n', '<br>')})
            save_chat_history(chat_history, poetry_chat_history_file)
            return redirect(url_for('poetry'))

    return render_template('poetry.html', chat_history=chat_history)

@app.route('/creative_writing', methods=['GET', 'POST'])
def creative_writing():
    chat_history = load_chat_history(creative_writing_chat_history_file)
    if request.method == 'POST':
        user_message = request.form['creative_writing_text'].strip()
        if user_message:
            chat_history.append({'sender': 'User', 'message': user_message})

            # Get the response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative assistant."},
                    {"role": "user", "content": f"Generate a creative writing based on the following text:\n{user_message}"}
                ],
                max_tokens=300
            )
            bot_message = response['choices'][0]['message']['content']
            chat_history.append({'sender': 'Bot', 'message': bot_message.replace('\n', '<br>')})
            save_chat_history(chat_history, creative_writing_chat_history_file)
            return redirect(url_for('creative_writing'))

    return render_template('creative_writing.html', chat_history=chat_history)

@app.route('/kannada_poems', methods=['GET', 'POST'])
def kannada_poems():
    chat_history = load_chat_history(kannada_poetry_chat_history_file)
    if request.method == 'POST':
        user_message = request.form['poetry_text'].strip()
        if user_message:
            chat_history.append({'sender': 'User', 'message': user_message})

            # Get the response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a famous Kannada poet."},
                    {"role": "user", "content": f"Generate a Kannada poem based on the following text:\n{user_message}"}
                ],
                max_tokens=500
            )
            bot_message = response['choices'][0]['message']['content']
            chat_history.append({'sender': 'Bot', 'message': bot_message.replace('\n', '<br>')})
            save_chat_history(chat_history, kannada_poetry_chat_history_file)
            return redirect(url_for('kannada_poems'))

    return render_template('kannada_poetry.html', chat_history=chat_history)

@app.route('/poet_clear_chat')
def p_clear_chat():
    with open(poetry_chat_history_file, 'w') as f:
        json.dump([], f)
    return redirect(url_for('poetry'))

@app.route('/cw_clear_chat')
def cw_clear_chat():
    with open(creative_writing_chat_history_file, 'w') as f:
        json.dump([], f)
    return redirect(url_for('creative_writing'))

@app.route('/kannada_clear_chat')
def kannada_clear_chat():
    with open(kannada_poetry_chat_history_file, 'w') as f:
        json.dump([], f)
    return redirect(url_for('kannada_poems'))

if __name__ == '__main__':
    app.run(debug=True)
