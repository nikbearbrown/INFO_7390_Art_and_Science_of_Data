# This Python script uses **Streamlit** to create a web-based application for predicting inventory demand (weekly sales) based on user-uploaded CSV data. The main functionalities include:

# 1. **User Input**: Allows users to upload a CSV file containing the features required for demand prediction.
# 2. **Data Validation**: Ensures that the uploaded data has the required features for the machine learning model by checking for missing or extra columns.
# 3. **Data Preprocessing**: Applies the same scaling used during model training to the uploaded data.
# 4. **Prediction**: Uses a pre-trained deep learning model to predict weekly sales.
# 5. **Result Display**: Presents predictions in a tabular format and allows users to download the results as a CSV file.

import streamlit as st
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
import os

# Path to data and model
DATA_DIR = 'data'
SCALER_PATH = os.path.join(DATA_DIR, 'scaler.joblib')
MODEL_PATH = os.path.join(DATA_DIR, 'demand_forecasting_model.h5')

st.title("AI-Driven Inventory Demand Forecasting")

st.write("Upload a CSV file with the same features as X_test.csv (excluding Weekly_Sales).")

uploaded_file = st.file_uploader("Upload your CSV", type="csv")

if uploaded_file is not None:
    # Load uploaded data
    data = pd.read_csv(uploaded_file)

    # Load scaler and model
    scaler = joblib.load(SCALER_PATH)
    model = load_model(MODEL_PATH)

    # Get required feature names from scaler
    required_columns = list(scaler.feature_names_in_)  # Features expected by the scaler

    # Validate uploaded data
    missing_columns = [col for col in required_columns if col not in data.columns]
    extra_columns = [col for col in data.columns if col not in required_columns]

    if missing_columns:
        st.error(f"Error: Missing required columns: {missing_columns}")
    elif extra_columns:
        st.warning(f"Warning: Extra columns found. These will be ignored: {extra_columns}")
        data = data[required_columns]  # Select only required columns
    else:
        st.success("Uploaded data matches the required features.")

    # Reorder columns to match the scaler's training order
    data = data[required_columns]

    # Scale data
    data_scaled = scaler.transform(data)

    # Predict
    predictions = model.predict(data_scaled)

    # Display predictions
    st.subheader("Predicted Weekly Sales (Demand):")
    predictions_df = pd.DataFrame(predictions, columns=["Predicted Weekly Sales"])
    st.dataframe(predictions_df)

    # Download option
    predictions_file = "predicted_sales.csv"
    predictions_df.to_csv(predictions_file, index=False)
    st.download_button(
        label="Download Predictions",
        data=open(predictions_file, "rb"),
        file_name=predictions_file,
        mime="text/csv",
    )
