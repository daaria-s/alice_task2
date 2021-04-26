from flask import Flask, request
import logging
import json
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}
targets = [['слона', 'слон'], ['кролика', 'кролик']]


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'target': 0,
        }
        res['response']['text'] = 'Привет! Купи слона!'
        return

    if any([i in ['ладно', 'куплю', 'покупаю', 'хорошо']
            for i in req['request']['original_utterance'].lower().split()]):
        res['response']['text'] = targets[sessionStorage[
            user_id]['target']][0].capitalize()
        res['response']['text'] += ' можно найти на Яндекс.Маркете!'
        sessionStorage[user_id]['target'] += 1

        if sessionStorage[user_id]['target'] == 1:
            res['response']['text'] += ' А теперь купи кролика!'
        elif sessionStorage[user_id]['target'] == 2:
            res['response']['end_session'] = True
        return

    res['response']['text'] = offer_elephant(
        req['request']['original_utterance'],
        sessionStorage[user_id]['target'])


def offer_elephant(text, target):
    return f"Все говорят '{text}', а ты купи {targets[target][0]}!"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
