# AI-Driven Inventory Demand Forecasting

This project provides a Streamlit-based web application for predicting inventory demand using a pre-trained deep learning model. Users can upload their data in CSV format to generate demand forecasts, which are displayed in the app and can be downloaded as a CSV file.

---

## Features

1. **CSV File Upload**:
   - Upload a CSV file with features matching the training dataset.
2. **Data Validation**:
   - Checks for missing or extra columns in the uploaded data.
   - Reorders columns to match the trained model's requirements.
3. **Data Scaling**:
   - Scales input data using a pre-fitted `StandardScaler`.
4. **Demand Prediction**:
   - Generates predictions using a pre-trained Keras deep learning model.
5. **Results Display**:
   - Shows predicted weekly sales (demand) in a tabular format.
6. **Downloadable Predictions**:
   - Allows users to download predictions as a CSV file.

---

## Requirements

Ensure you have the following installed:

- Python 3.8+
- Required libraries:
  - `streamlit`
  - `pandas`
  - `joblib`
  - `tensorflow`

---

## File Structure

```
project/
|— app.py                # Streamlit application script
|— data/
   |— scaler.joblib      # Pre-fitted StandardScaler
   |— demand_forecasting_model.h5 # Pre-trained Keras model
|— X_test.csv            # Example input data
|— y_test.csv            # Example output data
|— README.md            # Project documentation
```

---

## How to Run the App

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd project
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the App**:
   ```bash
   streamlit run app.py
   ```

4. **Access the App**:
   - Open the link provided in the terminal (e.g., `http://localhost:8501`) in your browser.

---

## Using the App

1. **Upload a CSV File**:
   - Prepare your data with the same features as used during training. Exclude the target column (`Weekly_Sales`).
   - Example CSV columns:
     ```csv
     Store,Dept,IsHoliday,Temperature,Fuel_Price,CPI,Unemployment,Size,WeekOfYear,Year,Type_B,Type_C,MarkDown1,MarkDown2,MarkDown3,MarkDown4,MarkDown5
     ```

2. **Review Results**:
   - The app will validate your data and display warnings or errors for missing/extra columns.
   - Predictions will be displayed in a table.

3. **Download Predictions**:
   - Click the "Download Predictions" button to save the results as a CSV file.

---

## Troubleshooting

- **Error: Missing Columns**:
  - Ensure your uploaded CSV includes all required features.
- **Error: Extra Columns**:
  - Extra columns will be ignored, but ensure the required columns are present.
- **Error: Feature Names Mismatch**:
  - Ensure the feature names in your CSV match the training data exactly (case-sensitive).

---

## Future Improvements

1. Add support for additional input formats (e.g., Excel files).
2. Provide visualizations of predictions and insights.
3. Include a log of processed inputs for tracking.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

