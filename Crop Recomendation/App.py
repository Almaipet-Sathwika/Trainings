from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Home route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Login route
@app.route('/login')
def login():
    return render_template('login.html')

# Register route
@app.route('/register')
def register():
    return render_template('registration.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if file and file.filename.endswith('.csv'):
        try:
            data = pd.read_csv(file)

            if 'label' not in data.columns:
                return "<h3>Error: 'label' column missing in uploaded file.</h3><a href='/'>Back to Home</a>"

            X = data.drop('label', axis=1)
            y = data['label']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            model = LogisticRegression(max_iter=200)
            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            return f"<h2>Prediction Successful</h2><p>Sample Predictions: {predictions[:5].tolist()}</p><a href='/'>Back to Home</a>"

        except Exception as e:
            return f"<h3>Error processing file: {e}</h3><a href='/'>Back to Home</a>"
    else:
        return "<h3>Invalid file format. Please upload a CSV file.</h3><a href='/'>Back to Home</a>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4500, debug=True)
