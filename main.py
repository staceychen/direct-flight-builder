from flask import Flask, request, render_template, send_file, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, DATA
import DirectFlightBuilder

app = Flask(__name__)
inputquery = UploadSet('inputquery', DATA)

app.config['UPLOADS_DEFAULT_DEST'] = 'inputs'
configure_uploads(app, inputquery)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST" and 'inputquery' in request.files:
        inputquery.save(request.files['inputquery'])
        return "UPLOAD COMPLETE"
    return "UPLOAD FAILED"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods =['POST'])
def call_builder():
    if "add" in request.form:
        a = request.form['a']
        b = request.form['b']
        a_radius = int(request.form['a_radius'])
        b_radius = int(request.form['b_radius'])
        a_lat = float(request.form['a_lat'])
        a_lng = float(request.form['a_lng'])
        b_lat = float(request.form['b_lat'])
        b_lng = float(request.form['b_lng'])
    
        DirectFlightBuilder.direct_flight_builder(a, (a_lat, a_lng), a_radius, b, 
                                                  (b_lat, b_lng), b_radius)
            
            
        return render_template("index.html")
        
        
    elif "download" in request.form:
        return redirect("/download")
    
    elif "clear" in request.form:
        DirectFlightBuilder.new_file()
        
        return render_template("index.html")
    
    
    elif "upload" in request.form:
        print("here")
        print(str(request.files))
        if 'inputquery' in request.files:
            inputquery.save(request.files['inputquery'])
            print("im here")
            return "UPLOAD COMPLETE"
        
        return render_template('index.html')
    
    
    elif "load" in request.form:
        DirectFlightBuilder.pre_processing()
        return render_template("index.html")
        
        
@app.route('/download')
def downloadFile ():
    path = "outputs/flights.csv"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug = True)

