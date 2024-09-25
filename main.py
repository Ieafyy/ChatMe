import ollama
from flask import Flask, request, jsonify  
from flask_cors import CORS

#llama3.1

modelfile = '''
FROM llama3.1

SYSTEM Você se chama jarvis. É meu assistente pessoal e sempre está pronto pra me ajudar
'''

app = Flask(__name__)
CORS(app)
ollama.create(model='Leafy', modelfile=modelfile)
ollama.embeddings(model='Leafy', prompt='Estudamos na usp, eu curso filosofia')
messages = []
models = ['Leafy']

def newModel(modelName, actAs):
    mf = f'''
    FROM llama3.1
    SYSTEM {actAs}
    '''

    ollama.create(model=modelName, modelfile=mf)
    print('ok!')
    return

def prompt(model, user_input, messages):

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    response = ollama.chat(
        model=model, 
        messages=messages,
    )

    messages.append(response['message'])
    print(response['message']['content'])
    return response['message']['content']


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'oi :D'


@app.route('/api/readinput', methods=['GET', 'POST'])
def chat():
    content = request.json
    print('>>' + content['data'] + '<< REACT')
    print('pensando como ' + content['model'] + '...')
    return {'response': prompt(content['model'], content['data'], messages)}

@app.route('/api/newmodel', methods=['GET', 'POST'])
def newmodel():
    content = request.json
    print('>> Name: ' + content['name'] + ' << REACT')
    print('>> ActAs: ' + content['act_as'] + ' << REACT')
    if content['name'] in models:
        print('Modelo Ja existente :(')
        return {'error': 'Modelo ja existe'}
    models.append(content['name'])
    print('# Novo modelo adicionado #')
    print(models)
    return {'response': newModel(content['name'], content['act_as'])}


@app.route('/api/deleteData', methods=['GET', 'POST'])
def deleteData():
    print('Apagando data...')
    global messages
    messages.clear()
    print(messages)
    print('Apagado!')
    return {'Apagado': messages}


@app.route('/api/getModels', methods=['GET'])
def getModels():
    print('enviando dados...')
    return {'models': models}




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')


# while True:
#     user_input = input('> ')
#     prompt("Leafy", user_input, messages)
#
