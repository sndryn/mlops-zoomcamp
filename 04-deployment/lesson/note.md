# 03 - ML Pipelines/Workflow Orchestration

Types of deployment:
1. Batch/offline: run the model regularly
2. Online: up and running all the time
    - Web service
    - Streaming

### Using pipenv
1. Install pipenv
```
pip install pipenv
```
2. Install virtual environment and dependencies
```
pip install scikit-learn==1.0.2 flask --python 3.9
```
3. Install for dev environment
```
pip install --dev requests 
```
4. Enter virtual env
```
pipenv shell
```

## Web service

### Using Flask example
```
app = Flask("duration-prediction")

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_features(ride)
    pred = predict(features)

    result = {
        "duration": pred
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
```

### Using gunicorn
1. Install gunicorn
2. Call using gunicorn
```
gunicorn --bind=0.0.0.0:9696 predict:app
```

### Using Docker
```
docker build -t ride-duration-prediction-service:v1 .
```
```
docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1
``````

