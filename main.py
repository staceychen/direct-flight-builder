from flask import Flask, request, render_template, send_file, redirect
#from flask.ext.uploads import UploadSet, configure_uploads, DOCUMENTS
import DirectFlightBuilder

app = Flask(__name__)
#input = UploadSet('input', DOCUMENTS)
history = []

#app.config['UPLOADED_PHOTO_DEST'] = 'static/inputs'
#configure_uploads(app, input)

#@app.route('/upload', methods=['GET', 'POST'])
#def upload():
    

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods =['POST'])
def call_builder():
    global history
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
        history.append(a + " <--> " + b)
        
        reversed_history = history[::-1]
        
        history_string = "<h3>History</h3><br>"
        for i in reversed_history:
            history_string += "<h6>" + i + "<h6>"
            
            
        return render_template("index.html",
                               history = history_string)
        
        
    elif "download" in request.form:
        return redirect("/download")
    
    elif "clear" in request.form:
        DirectFlightBuilder.new_file()
        history = []
        
        return render_template("index.html")
    
    elif "load" in request.form:
        DirectFlightBuilder.pre_processing()
        return render_template("index.html")
        
        
@app.route('/download')
def downloadFile ():
    path = "outputs/flights.csv"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug = True)

