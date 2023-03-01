from flask import Flask, jsonify, request, render_template
import pickle
import logging


app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='app.log', level= logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


# Load model

try:
    with open('Affair.pkl','rb') as f:
        model = pickle.load(f)
except Exception as e:
    logging.error(f'failed to load model : {e}')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Get the input value from the form
        try:
            rate_marriage = float(request.form['rate_marriage'])
            age = float(request.form['age'])
            yrs_married = float(request.form['yrs_married'])
            children = float(request.form['children'])
            religious = float(request.form['religious'])
            educ = float(request.form['educ'])
            occupation = float(request.form['occupation'])
            occupation_husb = float(request.form['occupation_husb'])
        except ValueError as e:
            logging.error(f'Failed to parse input values: {e}')
            return jsonify({'error':'Invalid input values'})




        # Make a prediction using the model
        try:
            prediction = model.predict([[rate_marriage,age,yrs_married,children,religious,educ,occupation,occupation_husb]])
        except Exception as e:
            logging.error(f'Failed to make prediction: {e}')
            return jsonify({'error':'Failed to make prediction'})


        # Return the prediction to the user

        logging.info(f'Prediction : {prediction[0]}')
        return render_template('index.html', prediction = prediction[0])

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,port=5000)