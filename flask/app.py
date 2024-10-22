from flask import Flask, request, render_template
import pandas as pd
<<<<<<< HEAD
import pickle
=======
import pickle  # Importing pickle for saving/loading models
>>>>>>> fbba354bc328479f0481a93d9283da2ada040537

app = Flask(__name__)

# Load the model
<<<<<<< HEAD
model_path = 'model/visraf.pkl'  # Adjusted the model path
with open(model_path, 'rb') as model_file:
=======
model_file_path = 'C:/Visa_Approval_Prediction/model/visraf.pkl'  # Update this path

# Open the model file
with open(model_file_path, 'rb') as model_file:
>>>>>>> fbba354bc328479f0481a93d9283da2ada040537
    loaded_model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('visaapproval.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
<<<<<<< HEAD
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    prev_visa = request.form['prev_visa']
    education = request.form['education']
=======
>>>>>>> fbba354bc328479f0481a93d9283da2ada040537
    full_time_position = request.form['full_time_position']
    prevailing_wage = float(request.form['prevailing_wage'])
    year = int(request.form['year'])
    soc_name = request.form['soc_name']

<<<<<<< HEAD
    # Business logic for job description
    if education == 'none':
        return render_template('resultVA.html', prediction_text='Visa Denied: Education qualification is None.')

    # Adjusted prevailing wage range to 30,000 - 3,000,000
    if not (30000 <= prevailing_wage <= 3000000):
        return render_template('resultVA.html', prediction_text='Visa Denied: Prevailing wage must be between 30,000 and 3,000,000.')

    if not (18 <= age <= 47):
        return render_template('resultVA.html', prediction_text='Visa Denied: Age should be between 18 to 47.')

    if full_time_position != 'Y':
        return render_template('resultVA.html', prediction_text='Visa Denied: Full-time position required.')

    # Preprocessing the input data
    full_time_position = 1 if full_time_position == 'Y' else 0
    soc_n = 0 if soc_name.lower() == 'it' else 1
=======
    # Preprocessing the input data
    full_time_position = 1 if full_time_position == 'Y' else 0
    soc_n = 0 if soc_name.lower() == 'it' else 1  # Adjust according to your mapping
>>>>>>> fbba354bc328479f0481a93d9283da2ada040537

    # Prepare the feature array for prediction
    input_data = pd.DataFrame([[full_time_position, prevailing_wage, year, soc_n]],
                              columns=["FULL_TIME_POSITION", "PREVAILING_WAGE", "YEAR", "SOC_N"])

    # Make prediction
    prediction = loaded_model.predict(input_data)
<<<<<<< HEAD
    prediction_result = 'Approved' if prediction[0] == 1 else 'Denied'

    if prediction_result == 'Denied':
        return render_template('resultVA.html', prediction_text=f'The visa is {prediction_result}.')
    else:
        # Navigate to a new page to ask for further questions
        return render_template('next_questions.html', name=name)

@app.route('/next', methods=['POST'])
def next_step():
    # Get responses from the new page
    foreign_languages = request.form['foreign_languages']
    native_language = request.form['native_language']
    english_fluency = request.form['english_fluency']
    reason = request.form['reason']
    work_experience = request.form['work_experience']
    country = request.form['country']
    percentage = float(request.form['percentage'])
    night_shifts = request.form['night_shifts']

    # Business logic based on the provided answers
    if english_fluency.lower() == 'beginner':
        return render_template('resultVA.html', prediction_text='Visa Denied: English fluency cannot be Beginner.')

    if 'employment' not in reason.lower():
        return render_template('resultVA.html', prediction_text='Visa Denied: The reason must relate to employment in the US.')

    if country.lower() == 'us':
        return render_template('resultVA.html', prediction_text='Visa Denied: Applicant cannot be from the US.')

    if not (70 <= percentage <= 100):
        return render_template('resultVA.html', prediction_text='Visa Denied: Percentage must be between 70% and 100%.')

    # If all conditions are met
    return render_template('resultVA.html', prediction_text='The visa is Approved.')
=======
    prediction_result = 'Approved' if prediction[0] == 1 else 'Denied' if prediction[0] == 2 else 'Unknown'

    return render_template('resultVA.html', prediction_text=f'The visa is {prediction_result}.')
>>>>>>> fbba354bc328479f0481a93d9283da2ada040537

if __name__ == "__main__":
    app.run(debug=True)
