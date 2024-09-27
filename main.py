import ollama
from flask import Flask, request, jsonify  
from flask_cors import CORS
import json
import requests


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

def get_flight_times(departure: str, arrival: str) -> str:

    flights = {
        'NYC-LAX': {'departure': '08:00 AM', 'arrival': '11:30 AM', 'duration': '5h 30m'},
        'LAX-NYC': {'departure': '02:00 PM', 'arrival': '10:30 PM', 'duration': '5h 30m'},
        'LHR-JFK': {'departure': '10:00 AM', 'arrival': '01:00 PM', 'duration': '8h 00m'},
        'JFK-LHR': {'departure': '09:00 PM', 'arrival': '09:00 AM', 'duration': '7h 00m'},
        'CDG-DXB': {'departure': '11:00 AM', 'arrival': '08:00 PM', 'duration': '6h 00m'},
        'DXB-CDG': {'departure': '03:00 AM', 'arrival': '07:30 AM', 'duration': '7h 30m'},
    }


    key = f'{departure}-{arrival}'.upper()

    return json.dumps(flights.get(key, {'error': 'Flight not found'}))

def get_weather(city: str) -> str:
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': '7612039fdd4e6f05c24099e2829519ef',
        'units': 'metric' 
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        #temperature = data['main']['temp']
        return json.dumps(data)
    else:
        print("Error:", response.status_code, response.json().get('message', ''))
        return json.dumps({'error': 'city not find'})



def newModel(modelName, actAs):
    mf = f'''
    FROM llama3.1
    SYSTEM {actAs}
    '''

    ollama.create(model=modelName, modelfile=mf)
    print('ok!')
    return

def prompt(model, user_input, messages, useContext):

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    if useContext:
        response = ollama.chat(
            model=model, 
            messages=messages,
            tools=[
                {
                    'type': 'function',
                    'function': {
                        'name': 'get_flight_times',
                        'description': 'Get the flight times between two cities',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'departure': {
                                    'type': 'string',
                                    'description': 'The departure city (airport code)',
                                },
                                'arrival': {
                                    'type': 'string',
                                    'description': 'The arrival city (airport code)',
                                },
                            },
                            'required': ['departure', 'arrival'],
                        },
                    },
                },
                {
                    'type': 'function',
                    'function': {
                        'name': 'get_weather',
                        'description': 'Get the current weather condition in a city',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'city': {
                                    'type': 'string',
                                    'description': 'The city to search the weather condition',
                                },
                            },
                            'required': ['city'],
                        },
                    },
                },
            ]
        )
    
    else:
        response = ollama.chat(
        model=model, 
        messages=messages)

    messages.append(response['message'])

    if not response['message'].get('tool_calls'):
        print("Resposta sem func: ")
        print(">>" + response['message']['content'])
        return response['message']['content']


    if response['message'].get('tool_calls'):
        available_functions = {
            'get_flight_times': get_flight_times,
            'get_weather': get_weather
        }
 
        for tool in response['message']['tool_calls']:
            function_to_call = available_functions[tool['function']['name']]
            print('>> FUNC: ' + str(function_to_call))
            function_args = tool['function']['arguments']
            function_response = function_to_call(**function_args)
            messages.append(
                {
                    'role': 'tool',
                    'content': function_response,
                }
            )

    final_response = ollama.chat(model=model, messages=messages)
    print(final_response['message']['content'])
    return final_response['message']['content']


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'oi :D'


@app.route('/api/readinput', methods=['GET', 'POST'])
def chat():
    content = request.json
    print('>>' + content['data'] + '<< REACT')
    print('pensando como ' + content['model'] + '...')
    print('CONTEXTO: ' + str(content['useContext']))
    return {'response': prompt(content['model'], content['data'], messages, content['useContext'])}

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
