from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# Paths to your Python scripts
ADD_FACES_PATH = "C:\\Users\\LENOVO\\Downloads\\face_recognition_project-main1\\face_recognition_project-main\\add_faces.py"
TEST_PATH = "C:\\Users\\LENOVO\\Downloads\\face_recognition_project-main1\\face_recognition_project-main\\test.py"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_faces', methods=['POST'])
def add_faces():
    # Call the add_faces.py script
    subprocess.Popen(['python', ADD_FACES_PATH])
    return redirect(url_for('home'))

@app.route('/test', methods=['POST'])
def test():
    # Call the test.py script
    subprocess.Popen(['python', TEST_PATH])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
