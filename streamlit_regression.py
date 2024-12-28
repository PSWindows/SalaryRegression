import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle

# Load the trained model
model = tf.keras.models.load_model('regression_model.h5')

# Load the encoders and scaler
with open('label_encoder_gender.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('onehot_encoder_geo.pkl', 'rb') as file:
    onehot_encoder_geo = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

## streamlit app

st.title('Estimated Salary Prediction')

# User input
geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', ['Male', 'Female'])  # Display Male/Female instead of 0/1
# Encode the gender for the model input
gender_numeric = label_encoder_gender.transform([gender])[0]  # Transform to 0 or 1

age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
exited = st.selectbox('Exited', [0, 1])
credit_score = st.number_input('Credit Score')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1]) 

# Prepare the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'gender': [gender_numeric],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'Exited': [exited]
})


# Encoding the 'Gender' column
input_data['Gender'] = label_encoder_gender.transform([gender])

# One-hot encode 'Geography'

geo_encoded = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

# Combine one-hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# Ensure input_data columns match the training data columns that were used to fit the scaler
input_data = input_data[scaler.feature_names_in_]

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Predict the estimated salary
prediction = model.predict(input_data_scaled)
prediction_salary = prediction[0][0]

st.write(f'Predicted Estimated Salary: {prediction_salary:.2f}')
