import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, flash ,url_for,session
from flask import request
import base64

from datetime import date
from flask import Flask, request, render_template



################  import tee client statifaction  ######################

from flask_mysqldb import MySQL
from markupsafe import Markup
import pickle
import pandas as pd
import xgboost as xg 
import pandas as pd
from flask import request
from flask import Response
import requests
from flask import send_file

from langdetect import detect
import os
from flask import Flask, render_template, request, session, redirect, url_for
from flask import send_file, request
import pandas as pd







################  import tee Logistique  ######################

import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, flash 
from markupsafe import Markup
import pickle
import pandas as pd
import xgboost as xg 
from math import radians, sin, cos, sqrt, atan2
from heapq import heappush, heappop
import heapq
from math import inf, sqrt
import os
import pdfplumber
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import ast
import cv2

# import face_recognition










####################  Configuration (see .env.example)  ####################
# All credentials are read from the environment. Copy .env.example to .env and
# fill it in. The MySQL settings keep their historical local-dev defaults; the
# third-party API keys have no default on purpose, so a missing key fails loudly
# instead of silently sending an invalid request.
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'oiloptima_pgs')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-only-insecure-key')
mysql = MySQL(app)









import math  
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('data', 'Faces')    # Dossier de téléchargement
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensions autorisées

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Configuration du dossier de téléchargement

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    



########################################################################################################################

from scipy.spatial.distance import cosine

from tensorflow.keras.applications import MobileNetV2

# Load the face detection scascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')




# # Route to handle capturing an image and performing face detection
# @app.route('/process_face_login', methods=['POST'])
# def process_face_login():

detected_face = None

model_embb = MobileNetV2(weights='imagenet', include_top=False, input_shape=(500, 500, 3))



def extract_embeddings(img_array):
    global model_embb
    img_array = np.expand_dims(img_array, axis=0)
    embeddings = model_embb.predict(img_array)
    return embeddings.flatten()

def face_compare(file):
    img = cv2.imread(file)
    img = cv2.resize(img, (500, 500))

    face_image1 = extract_embeddings(np.array(img))
    face_image2 = extract_embeddings(np.array(detected_face))
    similarity = 1 - cosine(face_image1, face_image2)
    
    return similarity




@app.route('/')
def login():
    global detected_face
    detected_face = None
    return render_template('Login.html')



@app.route('/', methods=['GET', 'POST'])
def login_with_face():
    global detected_face
    if detected_face is not None:
        for image in os.listdir(app.config['UPLOAD_FOLDER']):
            image_file_path = os.path.join(app.config['UPLOAD_FOLDER'],image)
            face_similarity = face_compare(image_file_path)
            if face_similarity > 0.5:
                return render_template('index.html',username=image[:-4])
            return render_template('Login.html', error='Uknown Face')
        return 
        
    else:
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['password']
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT username, password FROM users WHERE username = '{username}'")
            user = cur.fetchone()
            cur.close()
            if len (username) == 0:
            
                return render_template('login.html', error='Username Not Found')
            
            if len (pwd )== 0:
            
                return render_template('login.html', error='Password Not Found')

         
            
            if user and pwd == user[1]:
                session['username'] = user[0]
                return render_template('index.html',username=username) # Redirection vers la route 'index'
            else:
                return render_template('Login.html', error='The password you’ve entered is incorrect')
                
                
                    

    return render_template('Login.html')





"""@app.route('/', methods=['GET', 'POST'])
def loginafter():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT username, password FROM users WHERE username = '{username}'")
        user = cur.fetchone()
        cur.close()
        
        if user and pwd == user[1]:
            session['username'] = user[0]
            return render_template('index.html',username=username) # Redirection vers la route 'index'
        else:
            return render_template('Login.html', error='Invalid username or password ! ')
    return render_template('Login.html')"""


import time



def detect_faces(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(1, 1))
    
    
    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        face = frame[y:y+h, x:x+w]

        global detected_face
        detected_face = cv2.resize(face, (500, 500))
        
    return frame

def gen_frames():
    
    video_capture = cv2.VideoCapture(0) 
    

    while True:
        success, frame = video_capture.read()
        if not success:
            break
        
        # Perform face detection
        frame = detect_faces(frame)
        global detected_face
        if detected_face is not None:
            #cv2.imwrite(r"data\Faces\face.jpg", frame) 
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

@app.route('/video_feed')
def video_feed():
    # gen_frames()
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame', headers={'Access-Control-Allow-Origin': '*'}) 

@app.route('/close_popup')
def close_popup():
    global detected_face
    if detected_face is not None:
       
        return Response("stop")
    else:
    
        return Response("don't stop")
    

@app.route('/signup')
def signupfirst():
    global detected_face
    detected_face = None
    return render_template('logup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        email = request.form['email']
        join_date = date.today().strftime('%Y-%m-%d')  # Date d'inscription automatique
        
        # Vérification si l'utilisateur existe déjà
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if password != password2:
            return render_template('logup.html', error='Different Password', username=username, email=email)
        if existing_user:
            cur.close()
            return render_template('logup.html', error='Username already exists!', username=username, email=email)
        
        # Vérification si l'email est déjà utilisé
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_email = cur.fetchone()
        if existing_email:
            cur.close()
            return render_template('logup.html', error='Email address already in use!', username=username, email=email)
        
        # Vérification des contraintes
        if not (username.isalpha() and len(username) >= 8):
            cur.close()
            return render_template('logup.html', error='Username must be at least 8 characters long and contain only alphabetic characters.', username=username, email=email)
        
        if not ('@' in email and email.endswith('pgs.tn')):
            cur.close()
            return render_template('logup.html', error='Please enter a valid email address ending with "pgs.tn".', username=username, email=email)
        
        if not (len(password) >= 8 and not any(c in password for c in '!@#$%^&*()_+-={}[]|:;"\'<>,.?/')):
            cur.close()
            return render_template('logup.html', error='Password must be at least 8 characters long and not contain special characters.', username=username, email=email)
        
        global detected_face
        if detected_face is not None:
            #file = os.path.join(app.config['UPLOAD_FOLDER'], 'face')
            new_filename = f"{username}"
            new_file = os.path.join(app.config['UPLOAD_FOLDER'], new_filename+'.jpg')
            # os.rename(file+'.jpg', new_file)
            cv2.imwrite(new_file, detected_face) 
            cur.execute("INSERT INTO users (username, password, email, join_date, image) VALUES (%s, %s, %s, %s, %s)",
                    (username, password, email, join_date, new_file))

        else: 
        # Insertion de l'utilisateur dans la base de données
            cur.execute("INSERT INTO users (username, password, email, join_date) VALUES (%s, %s, %s, %s)",
                        (username, password, email, join_date))
        mysql.connection.commit()
        cur.close()
        return redirect('/')  # Rediriger vers la page d'accueil ou une autre page après inscription
    
    return render_template('logup.html')



######################################################################################################################################################

# Définition de la route pour la page d'accueil
@app.route('/index')
def index():
    # Code pour la page d'accueil
    return render_template('index.html')



@app.route('/visitor')
def visitor():
    # Code pour la page d'accueil
    return render_template('Visitor.html')




@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/analysis')
def analysis():
    return render_template('Dashboard.html')


@app.route('/Stock_out_Prediction')
def Stock_out_Prediction():
    return render_template('Stock_out Prediction.html')

@app.route('/Tank_Behaviour_Prediction')
def Tank_Behaviour_Prediction():
    return render_template('Tank_Behaviour_Prediction.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



############################################################Tank behaviour################################################################################


@app.route('/Tank_Behaviour_Prediction', methods=['POST'])
def Tank_Behaviour_Prediction_form():
    data = request.form.to_dict()
    CONTAINER_CODE = float(data['CONTAINER_CODE'])
    Product_NAME = float(data['Product_NAME'])
    gross_quantity = float(data['GROSS_QUANTITY'])
    NET_QUANTITY = float(data['NET_QUANTITY'])
    TEMPERATURE = float(data['TEMPERATURE'])
    DENSITY = float(data['DENSITY'])
    WEIGHT = float(data['WEIGHT'])
    TO_SUPPLIER_NUMBER = float(data['TO_SUPPLIER_NUMBER'])


    input_data = pd.DataFrame([Product_NAME, CONTAINER_CODE, gross_quantity, NET_QUANTITY,
                            DENSITY, TEMPERATURE, WEIGHT, TO_SUPPLIER_NUMBER]).T
    
    input_data.columns= ['TERMINAL_PRODUCT_NUMBER', 'GROSS_QUANTITY', 'NET_QUANTITY', 'DENSITY',
       'TEMPERATURE', 'WEIGHT', 'TO_SUPPLIER_NUMBER',
       'CONTAINER_CODE_encoded']
    
    loaded_model = xg.Booster()
    loaded_model.load_model("tank_behavior_model.json")


    pred =  loaded_model.predict(xg.DMatrix(input_data))[0]
    # lstm_scaled_tb_predictions = (model.predict(xg.DMatrix(input_data)))>0.5).astype('int32')


    safe = "Anomaly" if pred > 0.5 else "Not Anomaly"
    return render_template('Tank_Behaviour_Prediction.html', safe=safe)





@app.route('/Injector_failure_Prediction', methods=['POST'])
def Injector_failure_Prediction_form():
    data = request.form.to_dict()
    Product_NAME = float(data['Product_NAME'])
    TOTALIZER = float(data['TOTALIZER'])
    THRUPUT = float(data['THRUPUT'])
    UNACCOUNTED = float(data['UNACCOUNTED'])
    PRODUCT_THRUPUT = float(data['PRODUCT_THRUPUT'])
    ACTUAL_THRUPUT = float(data['ACTUAL_THRUPUT'])
    INJECTOR_CODE_encoded = float(data['INJECTOR_CODE_encoded'])



    input_data = [[TOTALIZER, Product_NAME, THRUPUT, UNACCOUNTED,
                            PRODUCT_THRUPUT, ACTUAL_THRUPUT, INJECTOR_CODE_encoded]]
    
    with open("injector_failure_model.pkl", "rb") as f:
        injector_model = pickle.load(f)
    
    safe2 = injector_model.predict(input_data)
    
    return render_template('Tank_Behaviour_Prediction.html', safe2=safe2[0])
############################################################demand_forecasting_ala####################################################################

from flask import Flask, request, render_template
import matplotlib.pyplot as plt

@app.route('/Stock_out_Prediction', methods=['POST', 'GET'])
def uploader():
    if request.method == 'POST':
        model = pickle.load(open('demand_forecasting.pkl', 'rb'))
        model_fit = model.fit()
  
        nb_forecast = request.form['nb_forecast']
        nb_forecast = int(nb_forecast)
        
        prediction_results = model_fit.forecast(nb_forecast)
        prediction_results_list = prediction_results.tolist()  # Convert NumPy array to Python list

        # Create a simple line plot of the forecasted values
        plt.figure(figsize=(10, 6))
        plt.plot(prediction_results_list)
        plt.xlabel('Day')
        plt.ylabel('Demand')
        plt.title('Demand Forecasting')
        plt.grid(True)
        plt.savefig('static/forecast_plot.png')  # Save the plot as a static image
        
        return render_template('Stock_out Prediction.html', safety_stock_prediction=prediction_results_list)
    else:
        return render_template('Stock_out Prediction.html')
















############################################################demand_forecasting_SALMA ####################################################################


import numpy as np

from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model  # Modifier l'importation ici


model = load_model('modelNN_safety_stock.h5', compile=False)

@app.route('/Safety_stock', methods=['POST'])
def Safety_stock():
    data = request.form.to_dict()
    tank_code = int(data['TANK_CODE_encoded'])
    name = int(data['NAME_encoded'])
    net_quantity = float(data['NET_QUANTITY'])
    gross_quantity = float(data['GROSS_QUANTITY'])
    rt_net_quantity = float(data['RT_NET_QUANTITY'])
    rt_gross_quantity = float(data['RT_GROSS_QUANTITY'])
    shell_capacity = float(data['SHELL_CAPACITY'])
    rt_temperature = float(data['RT_TEMPERATURE'])
    rt_density = float(data['RT_DENSITY'])
    status_date_year = int(data['STATUS_DATE_YEAR'])
    status_date_month = int(data['STATUS_DATE_MONTH'])
    status_date_day = int(data['STATUS_DATE_DAY'])
    status_date_hour = int(data['STATUS_DATE_HOUR'])
    status_date_minute = int(data['STATUS_DATE_MINUTE'])
    status_date_second = int(data['STATUS_DATE_SECOND'])

    # Préparation des données pour la prédiction
    input_data = np.array([[tank_code, name, net_quantity, gross_quantity, rt_net_quantity,
                            rt_gross_quantity, shell_capacity, rt_temperature, rt_density,
                            status_date_year, status_date_month, status_date_day,
                            status_date_hour, status_date_minute, status_date_second]])

    # Faire la prédiction
    prediction = model.predict(input_data)
    predicted_class = int(prediction[0][0])
    result = "Safe" if predicted_class == 1 else "Not Safe"

    # Retourner le résultat au format JSON
    return render_template('Stock_out Prediction.html', safe=result)





























########################################################################### Partie feedback  #####################################################################################################################################



from textblob import TextBlob



#############################################Partie Textblob
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer

# # Assurez-vous d'avoir téléchargé les données nécessaires pour NLTK
# nltk.download('vader_lexicon')

# # Initialiser l'analyseur de sentiment Vader
# sia = SentimentIntensityAnalyzer()

# def analyze_sentiment(text):
#     # Obtenir la polarité du sentiment pour le texte
#     sentiment_scores = sia.polarity_scores(text)
#     compound_score = sentiment_scores['compound']

#     # Déterminer le sentiment en fonction du score composite
#     if compound_score >= 0.05:
#         return "Positive"
#     elif compound_score <= -0.05:
#         return "Negative"
#     else:
#         return "Neutral"







def analyze_sentiment(word):
    analysis = TextBlob(word)
    if analysis.sentiment.polarity > 0.1:
        return "Positive"
    elif analysis.sentiment.polarity <0.1:
        return "Negative"
    else:
        return "Neutral"


    




@app.route('/Clients_Feedback')
def Clients_Feedback():

    sheet_id = '1cZBpGsvTsJ9x0irMaimTqDjuKq4aOCkg5OoX1Qcxdcg'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

    print(df)

  

    # Renommer les colonnes
    df = df.rename(columns={
        'Horodateur': 'date',
        '1-  Please choose Your oil group :': 'Partner',
        '2-  Please choose the Government :': 'Governement',
        '4-Please write your Feedback Here : ': 'Reclamation',
        '3- Your Feedback is about :':'Topic',
        '5-  On a scale of 1 to 5, how would you rate your experience :':'Rate'
    })



    ######################################  Cleaning mtee 1-5 scale     #######################
    # Convertir la colonne 'Rate' de chaîne de caractères à entier

    df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')
    df = df.dropna(subset=['Rate'])
    df['Rate'] = df['Rate'].astype(int)

    # Sélectionner les lignes avec des valeurs en dehors de l'intervalle 1-5
    invalid_rate_index = df.loc[~df['Rate'].isin([1, 2, 3, 4, 5])].index

    # Supprimer les lignes avec des valeurs de 'Rate' invalides
    df = df.drop(index=invalid_rate_index)

    # Réinitialiser les index après suppression des lignes
    df = df.reset_index(drop=True)

    # Supprimer la dernière colonne
    df = df.drop(columns=['Score'])




    ######################################  Cleaning mtee 1-5 scale #######################

   
    # Ajouter une colonne pour la langue de la réclamation
    df['Reclamation_Language'] = df['Reclamation']

    # Filtrer les lignes avec des réclamations en anglais ou en français
    #df = df[df['Reclamation_Language'].isin(['en'])]

    # Supprimer la colonne de langue intermédiaire
    df = df.drop(columns=['Reclamation_Language'])

    # Afficher le DataFrame nettoyé

    # Analyser le sentiment pour chaque réclamation
    result_list = []

    for index, row in df.iterrows():
        reclamation_text = row['Reclamation']
        
        sentiment = analyze_sentiment(reclamation_text)
        result_list.append(sentiment)
        
    df['Prediction'] = result_list
    

    # Convert DataFrame to a list of dictionaries
    result_list = df.to_dict(orient='records')
    # Convertir DataFrame en un fichier Excel
    # Créer le chemin complet du fichier Excel
    excel_path = os.path.join( 'static','database', 'clients_feedback.xlsx')

    # Convertir DataFrame en un fichier Excel
    df.to_excel(excel_path, index=False)    # Passez le résultat d'analyse de sentiment à votre modèle ou template
    return render_template('Clients_Feedback.html', result_list=result_list)









@app.route('/download_excel', methods=['POST'])
def download_excel():
    # Charger les données à partir de Google Sheets
    sheet_id = '1cZBpGsvTsJ9x0irMaimTqDjuKq4aOCkg5OoX1Qcxdcg'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    
    # Renommer les colonnes
    df = df.rename(columns={
        'Horodateur': 'date',
        '1-  Please choose Your oil group :': 'Partner',
        '2-  Please choose the Government :': 'Governement',
        '4-Please write your Feedback Here : ': 'Reclamation',
        '3- Your Feedback is about :':'Topic',
        '5-  On a scale of 1 to 5, how would you rate your experience :':'Rate'
    })
    
    # Supprimer la colonne 'Score' si nécessaire
    if 'Score' in df.columns:
        df = df.drop(columns=['Score'])
    
    # Convertir DataFrame en un fichier Excel
    excel_path = os.path.join('static', 'database', 'clients_feedback.xlsx')
    df.to_excel(excel_path, index=False)
    
    # Renvoyer le fichier Excel comme réponse
    message = "The Excel file has been generated successfully!"
    
    # Renvoyer le template avec le message
    return render_template('Clients_Feedback.html', message=message)














































########################################################################### Logistique #####################################################################################################################################



read_graph = np.load('graph (1).npy',allow_pickle='TRUE').item()

def parse_input(input_dict):
    graph = {}
    for coord, neighbors in input_dict.items():
        coord_tuple = tuple(map(float, coord.strip('[]').split(', ')))
        neighbor_list = [(tuple(map(float, n.strip('[]').split(', '))), d) for n, d in neighbors.items()]
        graph[coord_tuple] = neighbor_list
    return graph

def dijkstra_with_heuristic(graph, start, goal):
    """
    Dijkstra's algorithm with heuristic estimates for geographical locations.

    Args:
    - graph: A dictionary representing the graph, where keys are nodes and values are lists of tuples (neighbor, distance).
    - start: The starting node.
    - goal: The goal node.

    Returns:
    - path: A list representing the shortest path from start to goal.
    - total_distance: The total distance of the shortest path.
    """
    # Heuristic function (Euclidean distance)
    def heuristic(node):
        x1, y1 = node[1:-1].split(',')
        x2, y2 = goal[1:-1].split(',')
        return haversine_distance(float(x1), float(y1), float(x2), float(y2))

    # Priority queue for frontier nodes
    frontier = [(0, start)]  # (distance, node)
    # Dictionary to store the shortest distances from start to each node
    shortest_distances = {node: inf for node in graph}
    shortest_distances[start] = 0
    # Dictionary to store the previous node in the shortest path
    previous_node = {node: None for node in graph}

    while frontier:
        # Pop node from the frontier with the smallest distance
        current_distance, current_node = heapq.heappop(frontier)

        # Check if we reached the goal
        if current_node == goal:
            # Reconstruct the path from start to goal
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = previous_node[current_node]
            return path, shortest_distances[goal]

        # Explore neighbors of the current node
        for neighbor, distance in graph[current_node].items():
            # Calculate the total distance to the neighbor
            total_distance = current_distance + distance
            # Update the shortest distance if we found a shorter path
            if total_distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = total_distance
                # Update the previous node in the shortest path
                previous_node[neighbor] = current_node
                # Add the neighbor to the frontier with priority based on heuristic estimate
                heapq.heappush(frontier, (total_distance + heuristic(neighbor), neighbor))

    # If no path is found
    return [], inf

def dijkstra(graph, start, end):
    # Initialize distances to infinity for all nodes except the start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Priority queue to store nodes with their current shortest distance
    priority_queue = {start: 0}  # Dictionary {node: distance}
    
    # Dictionary to store the previous node in the shortest path
    previous = {node: None for node in graph}
    
    while priority_queue:
        current_node = min(priority_queue, key=priority_queue.get)
        del priority_queue[current_node]
        
        # If current node is the end node, reconstruct and return the shortest path
        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = previous[current_node]
            return path[::-1]  # Reverse the path to get it in the correct order
        
        # Otherwise, explore neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                priority_queue[neighbor] = distance
    
    # If no path is found
    return None

client_df = pd.read_csv('data/client_list.csv')
if 'Unnamed: 0' in client_df.columns:
    client_df.drop(['Unnamed: 0'],axis=1, inplace=True)


pgs_megrin = [36.77151858775371, 9.938279939704579]
pgs_bezert = [37.25320085241904, 9.778379857893148]
pgs_sfax = [34.30501189276116, 10.064632038873942]

all_terminals = [pgs_megrin, pgs_bezert, pgs_sfax]



def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    # Radius of earth in kilometers. Use 3956 for miles
    radius = 6371 
    distance = radius * c

    return distance

def get_weather_by_coordinates(latitude, longitude):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    # API endpoint URL
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'

    # Send HTTP request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant weather information
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Print the weather information
        return temperature, humidity
    else:
        # Print an error message if the request was unsuccessful
        print("Error fetching weather data.")


def average_hum_temp(poses):
  temps = []
  humis = []

  for pos in poses:
    la = float(pos.split(',')[0][1:])
    longi = float(pos.split(',')[1][:-1])

    temp, hum = get_weather_by_coordinates(la, longi)
    temps.append(temp)
    humis.append(hum)
  return sum(temps)/len(temps)+ sum(humis)/len(humis)



@app.route('/Logisitics')
def Logisitics():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stations")
    client_list = cur.fetchall()

  
    return render_template('Logisitics.html', columns=['id','name','cords'], rows=client_list)





@app.route('/add_station')
def add_station_page():
    return render_template('add_station.html')






@app.route('/add_station', methods=['POST'])
def add_station():
    if request.method == 'POST':
        station_name = request.form['name']
        station_location = request.form['location']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stations (station_name, coordination) VALUES (%s, %s)", (station_name, station_location))
        mysql.connection.commit()
        cur.execute("SELECT * FROM stations")
        client_list = cur.fetchall()



        return render_template('Logisitics.html',  columns=['id','name','cords'], rows=client_list)
    








@app.route('/delete_row/<int:index>')
def delete_row(index):

    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM stations where station_id={str(index)}")
    mysql.connection.commit()
    cur.execute("SELECT * FROM stations")
    client_list = cur.fetchall()



    return render_template('Logisitics.html',  columns=['id','name','cords'], rows=client_list)












@app.route('/update_row/<int:index>')
def update_station_page(index):

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM stations where station_id={str(index)}")
    client_list = cur.fetchone()
    return render_template('update_station.html', id=int(client_list[0]), name=client_list[1], x=client_list[2].split(',')[0][1:], y = client_list[2].split(',')[1][:-1])













@app.route('/update_row/<int:index>', methods=['POST'])
def update_row(index):

    if request.method == 'POST':
        station_name = request.form['name']
        station_location = request.form['location']

        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE stations SET station_name = %s, coordination = %s WHERE station_id = %s", (station_name, station_location, index))
        mysql.connection.commit()
        cur.execute("SELECT * FROM stations")
        client_list = cur.fetchall()



        return render_template('Logisitics.html',  columns=['id','name','cords'], rows=client_list)













@app.route('/selected_row/<int:index>')
def get_selected_row(index):


    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM stations where station_id={str(index)}")
    client_list = cur.fetchone()
    


    one_row = client_list[1:]

    x = one_row[1].split(',')[0][1:]
    y = one_row[1].split(',')[1][:-1]

    tmp = float('inf')
    clostest_x = 0
    clostest_y = 0

    for terminal in all_terminals:
        if haversine_distance(float(y), float(x), terminal[1], terminal[0]) < tmp:
            tmp = haversine_distance(float(y), float(x), terminal[1], terminal[0])
            clostest_x = terminal[0]
            clostest_y = terminal[1]

   
    #print(read_dictionary['[11.3349, 32.3727]']) # displays "world"

    return render_template('Logisitics.html', cols = ['name','cords'], one_row = [list(one_row)], x=x, y=y, clostest_x=clostest_x, clostest_y=clostest_y)













@app.route('/createpath/<float:long1>/<float:lat1>/<float:long2>/<float:lat2>/')
def createpath(long1, lat1, long2, lat2):
    # print(long1, lat1, long2, lat2)
    start_node = '['+str(long1)+', '+str(lat1)+']'
    end_node = '['+str(long2)+', '+str(lat2)+']'  

    
    if lat1< lat2:

        lat_diff_third =  lat1 + (lat2 - lat1) / 3
        lon_diff_third = long1 + (long2 - long1) / 3
        lat_diff_two_thirds = lat1 + (lat2 - lat1) * 2 / 3
        lon_diff_two_thirds = long1 + (long2 - long1) * 2 / 3

    else:
        lat_diff_third =  lat1 - (lat2 - lat1) / 3
        lon_diff_third = long1 - (long2 - long1) / 3
        lat_diff_two_thirds = lat1 - (lat2 - lat1) * 2 / 3
        lon_diff_two_thirds = long1 - (long2 - long1) * 2 / 3


    #######################
    reference_point = (long1, lat1) 

    # Calculate distances from the reference point to each position
    distances = [(haversine_distance(float(reference_point[0]), float(reference_point[1]), float(pos[1:-1].split(',')[1]), float(pos[1:-1].split(',')[0])), pos) for pos in list(read_graph.keys())]

    # Sort the positions based on distances
    sorted_positions = sorted(distances, key=lambda x: x[0])

    sorted_nodes= []
    for node in sorted_positions:
        sorted_nodes.append(node[1])

    start_node = sorted_nodes[0]
    ###################################
    reference_point = (long2, lat2) 

    # Calculate distances from the reference point to each position
    distances = [(haversine_distance(float(reference_point[0]), float(reference_point[1]), float(pos[1:-1].split(',')[1]), float(pos[1:-1].split(',')[0])), pos) for pos in list(read_graph.keys())]

    # Sort the positions based on distances
    sorted_positions = sorted(distances, key=lambda x: x[0])

    sorted_nodes= []
    for node in sorted_positions:
        sorted_nodes.append(node[1])
    
    end_node = sorted_nodes[0]

    ###################################
    reference_point = (lon_diff_third, lat_diff_third) 

    # Calculate distances from the reference point to each position
    distances = [(haversine_distance(float(reference_point[0]), float(reference_point[1]), float(pos[1:-1].split(',')[1]), float(pos[1:-1].split(',')[0])), pos) for pos in list(read_graph.keys())]

    # Sort the positions based on distances
    sorted_positions = sorted(distances, key=lambda x: x[0])

    sorted_nodes= []
    for node in sorted_positions:
        sorted_nodes.append(node[1])
    
    midel_node = sorted_nodes[0]

    ###################################
    reference_point = (lon_diff_two_thirds, lat_diff_two_thirds) 

    # Calculate distances from the reference point to each position
    distances = [(haversine_distance(float(reference_point[0]), float(reference_point[1]), float(pos[1:-1].split(',')[1]), float(pos[1:-1].split(',')[0])), pos) for pos in list(read_graph.keys())]

    # Sort the positions based on distances
    sorted_positions = sorted(distances, key=lambda x: x[0])

    sorted_nodes= []
    for node in sorted_positions:
        sorted_nodes.append(node[1])
    
    second_midel_node = sorted_nodes[0]
    ###############################
   
    paths = dijkstra(read_graph, start_node, end_node)
    paths1 = dijkstra(read_graph, start_node, midel_node) + dijkstra(read_graph, midel_node, end_node)
    paths2 = dijkstra(read_graph, start_node, second_midel_node) + dijkstra(read_graph, second_midel_node, end_node)

    all_paths = [paths, paths1, paths2]
    
    score = float('inf')
    best_paths = None

    for p in all_paths:
        new_score = average_hum_temp(p)
        
        if  new_score < score:
            score = new_score
            best_paths= p

    # print(paths)
    return render_template('createpath.html', paths=best_paths)









@app.route('/resume/<string:path>', methods=['POST'])
def resume(path):
    
    description = [str(x) for x in request.form.values()]
    vectorizer = CountVectorizer()
    vectorizer.fit(description)
    final_results = []
    best_score = 0
    best_driver = ""
    for file in os.listdir(r"static/pdfs"):
        image_path = r'static/pdfs/'+ file
        if image_path[-3:] == 'pdf':
            extracted_text = ''
            with pdfplumber.open(image_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    extracted_text += text
            text = [description[0], extracted_text]
            
            X = vectorizer.transform(text)
            if round(cosine_similarity(X)[0][1]*100,2) > best_score:
                best_score = round(cosine_similarity(X)[0][1]*100,2)
                best_driver = file
    return render_template('resume.html',resume=best_driver, paths= ast.literal_eval(path))


@app.route('/trailer_forecast', methods=['POST'])
def trailer_forecast_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Read the Excel file
            df = pd.read_excel(file)
            if 'Unnamed: 0' in df.columns:
                df.drop(['Unnamed: 0'],axis=1, inplace=True)

            
            if  not 'ENTER_TERMINAL' in df.columns or not 'USABLE_CAPACITY' in df.columns or not 'LAST_MODIFIED' in df.columns:
                return render_template('trailer_forecast.html', safetly_stock_prediction=f"Wrong type of Data")


            to_drop = []

            for col in df.columns:
                if df[col].isnull().sum() / df.shape[0] > .9:
                    to_drop.append(col)

            for col in df.columns:
                if df[col].nunique() == 1:
                    to_drop.append(col)
            df.drop(to_drop, axis=1,inplace=True)

            df = df.filter([ 'ENTER_TERMINAL', 'USABLE_CAPACITY', 'LAST_MODIFIED'])
            df.dropna(inplace=True)

            df['LAST_MODIFIED'] = df['LAST_MODIFIED'].dt.strftime('%y-%m-%d')
            df.sort_values(by=['LAST_MODIFIED'], inplace=True)


            df1 = df[df['ENTER_TERMINAL'] == 1]
            df2 = df[df['ENTER_TERMINAL'] == 2]

            df1 = df1.groupby(["LAST_MODIFIED"]).mean()
            df1 = df1.reset_index()

            window = 5
            X = []
            Y = []

            for i in range(len(df1)-window-1):
                x = df1.loc[i:i+window-1, 'USABLE_CAPACITY'].values
                y = df1.loc[i+window, 'USABLE_CAPACITY']
                X.append(x)
                Y.append(y)
            loaded_model = xg.Booster()
            loaded_model.load_model("terminal1_model.json")

            pred1 = loaded_model.predict(xg.DMatrix([X[-1]]))[0]


            df2 = df2.groupby(["LAST_MODIFIED"]).mean()
            df2 = df2.reset_index() 

            window = 5
            X = []
            Y = []

            for i in range(len(df2)-window-1):
                x = df2.loc[i:i+window-1, 'USABLE_CAPACITY'].values
                y = df2.loc[i+window, 'USABLE_CAPACITY']
                X.append(x)
                Y.append(y)
                
            loaded_model = xg.Booster()
            loaded_model.load_model("terminal2_model.json")

            pred2 = loaded_model.predict(xg.DMatrix([X[-1]]))[0]


           
    return render_template('trailer_forecast.html', pred1=pred1, pred2= pred2)

@app.route('/trailer_forecast')
def trailer_forecast():
    return render_template('trailer_forecast.html')

@app.route('/tractor_forecast', methods=['POST'])
def tractor_forecast_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            df_tractor = pd.read_excel(file)

            columns_with_missing_values =  [col for col in df_tractor.columns
                                if df_tractor[col].isnull().any()]

            columns_to_drop = [col for col in columns_with_missing_values if col != "LICENSE"]

            df_tractor = df_tractor.drop(columns=columns_to_drop)

            columns_to_drop = ["LOCKOUT_ENTRY", "RT_CURRENTLY_LOADING", "UNLADEN_WEIGHT"]
            df_tractor = df_tractor.drop(columns=columns_to_drop)

            numerical_features = [col for col in df_tractor.columns if df_tractor[col].dtype in ['int64', 'float64']]
            df_numerical = df_tractor[numerical_features]

            df_tractor['QUANTITY_TRACTOR'] = 1

            df_tractor['LAST_MODIFIED'] = pd.to_datetime(df_tractor['LAST_MODIFIED'])

            df_tractor['LAST_MODIFIED'] = df_tractor['LAST_MODIFIED'].dt.strftime('%y-%m-%d')

            df_tractor = df_tractor.filter([ 'QUANTITY_TRACTOR', 'LAST_MODIFIED'])
            df_tractor = df_tractor.groupby(["LAST_MODIFIED"]).sum()
            df_tractor = df_tractor.reset_index()

            window = 5
            X = []
            Y = []

            for i in range(len(df_tractor)-window-1):
                x = df_tractor.loc[i:i+window-1, 'QUANTITY_TRACTOR'].values
                y = df_tractor.loc[i+window, 'QUANTITY_TRACTOR']
                X.append(x)
                Y.append(y)

            loaded_model = xg.Booster()
            loaded_model.load_model("tractor_model.json")

            preds = loaded_model.predict(xg.DMatrix([X[-1]]))[0]

    return render_template('tractor_forecast.html',preds=math.ceil(preds))



@app.route('/tractor_forecast')
def tractor_forecast():
    return render_template('tractor_forecast.html')


########################################################chatbot########################################################################################
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

chat_model = genai.GenerativeModel('gemini-pro')

extracted_text = ''
for file in os.listdir(r"data/brocher/"):
  if '.pdf' in file:
    image_path = r"data/brocher/"+file

    with pdfplumber.open(image_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            extracted_text += text


infos = extracted_text
messages = [
    {'role':'user',
     'parts': [f"as a server you will answer the questions based on these informations: {infos} if related"]},
    {'role':'model',
     'parts': ["""okay and if the user asked me a defferent quetion i will answer him with out the given inforamtion"""]}
]
@app.route("/chatbot")
def chatpage():
    global messages
    infos = extracted_text
    messages = [
        {'role':'user',
        'parts': [f"as a server you will answer the questions based on these informations: {infos} if related"]},
        {'role':'model',
        'parts': ["""okay and if the user asked me a defferent quetion i will answer him with out the given inforamtion"""]}
    ]
    return render_template('chat.html')


@app.route("/chatbot", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
 
    messages.append({'role':'user',
                 'parts':[input]})

    answer = chat_model.generate_content(messages)
    messages.append({'role':'model',
                 'parts':answer.parts})

   
    return answer.parts[0].text




































































if __name__ == "__main__":
    app.run(debug=True)