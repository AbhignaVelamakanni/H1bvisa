from flask import Flask, request, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model (ensure model path is correct)
model_file_path = 'C:/Visa_Approval_Prediction/model/visraf.pkl'  # Update this path
with open(model_file_path, 'rb') as model_file:
    loaded_model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('visaapproval.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    prev_visa = request.form['prev_visa_status']
    education = request.form['education']
    full_time_position = request.form['full_time_position']
    prevailing_wage = float(request.form['prevailing_wage'])
    year = int(request.form['year'])
    soc_name = request.form['soc_name']  # Capture SOC Name

    # Example encoding of soc_name (you may want to adjust this based on your model's requirements)
    soc_mapping = {'1110': 1, '1130': 2, '1010': 3, 'none': 0}  # Adjust according to your mapping
    soc_encoded = soc_mapping.get(soc_name, 0)  # Default to 0 if not found

    # Visa denial based on form inputs
    if education == 'none':
        return render_template('resultVA.html', prediction_text='Visa Denied: Education qualification is None.')

    if not (30000 <= prevailing_wage <= 3000000):
        return render_template('resultVA.html', prediction_text='Visa Denied: Prevailing wage must be between 30,000 and 3,000,000.')

    if not (18 <= age <= 50):
        return render_template('resultVA.html', prediction_text='Visa Denied: Age should be between 18 and 50.')

    if full_time_position != 'Y':
        return render_template('resultVA.html', prediction_text='Visa Denied: Full-time position required.')

    # Preprocess data for model
    full_time_position = 1 if full_time_position == 'Y' else 0

    # Prepare input for prediction
    input_data = pd.DataFrame([[full_time_position, prevailing_wage, year, soc_encoded]], 
                               columns=["FULL_TIME_POSITION", "PREVAILING_WAGE", "YEAR", "SOC_N"])

    # Make prediction using the loaded model
    prediction = loaded_model.predict(input_data)
    prediction_result = 'Approved' if prediction[0] == 1 else 'Denied'

    # Redirect to next questions if initial conditions pass
    if prediction_result == 'Approved':
        return render_template('next_questions.html', name=name)

    return render_template('resultVA.html', prediction_text=f'The visa is {prediction_result}.')

@app.route('/next', methods=['POST'])
def next_step():
    # Get responses from next_questions.html form
    native_language = request.form['native_language']
    foreign_languages = request.form['foreign_languages']
    english_fluency = request.form['english_fluency']
    reason = request.form['reason']
    work_experience = request.form['work_experience']
    country = request.form['country']
    previous_visa_status = request.form['previous_visa_status']

    # Business logic for additional questions
    if native_language.lower() == foreign_languages.lower():
        return render_template('resultVA.html', prediction_text='Visa Denied: Foreign language must be different from native language.')

    if english_fluency.lower() == 'beginner':
        return render_template('resultVA.html', prediction_text='Visa Denied: English fluency cannot be Beginner.')

    if 'employment' not in reason.lower():
        return render_template('resultVA.html', prediction_text='Visa Denied: The reason must relate to employment in the US.')

    if country.lower() == 'us':
        return render_template('resultVA.html', prediction_text='Visa Denied: Applicant cannot be from the US.')

    return render_template('resultVA.html', prediction_text='The visa is Approved.')

if __name__ == "__main__":
    app.run(debug=True)
