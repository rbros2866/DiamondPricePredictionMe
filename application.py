from flask import Flask, request, render_template, redirect, url_for
from src.pipelines.prediction_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        data = CustomData(
            carat=float(request.form.get('carat')),
            depth=float(request.form.get('depth')),
            table=float(request.form.get('table')),
            x=float(request.form.get('x')),
            y=float(request.form.get('y')),
            z=float(request.form.get('z')),
            cut=request.form.get('cut'),
            color=request.form.get('color'),
            clarity=request.form.get('clarity')
        )
        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)
        prediction_result = round(pred[0], 2)
        
        # Redirect to the result route with the predicted value
        return redirect(url_for('result', prediction_result=prediction_result))

@app.route('/result')
def result():
    # Retrieve the predicted value from the URL parameter
    prediction_result = request.args.get('prediction_result')
    
    # Render the result template with the predicted value
    return render_template('result.html', prediction_result=prediction_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
