from src.pipeline.test_pipe import test_pipe
from src.logging.logger import my_logger

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)  # ✅ Corrected Flask app name

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/predict.html', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Step 1: Collect data
            data = request.form.to_dict()
            my_logger.info(f"Form Data Received: {data}")
            print(f"[DEBUG] Received form data: {data}")

            # Step 2: Convert to DataFrame
            df = pd.DataFrame([data])  # ✅ Wrap data in a list
            df['Price'] = 0
            print(f"[DEBUG] Converted to DataFrame:\n{df}")
            my_logger.info(f"DataFrame created for prediction:\n{df}")

            # Step 3: Load model and predict
            obj = test_pipe()
            prediction = obj.load_model(df)
            print(f"[DEBUG] Prediction: {prediction}")
            my_logger.info(f"Prediction result: {prediction}")

            # Step 4: Show result
            return render_template('predict.html', prediction=prediction)

        except Exception as e:
            print(f"[ERROR] Exception during prediction: {e}")
            my_logger.error(f"Prediction failed due to: {str(e)}")
            return render_template('predict.html', prediction="Error occurred")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port= 5000, host='0.0.0.0')
