from flask import Flask,render_template,jsonify,request
import requests
from flask_cors import CORS,cross_origin

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/temperature',methods=['POST','GET'])
def metho():
    code=request.form['Zip']
    r=requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+code+',in&appid=9a44ae6b82fe9ea41c971492d642c923')

    jsonobj=r.json()
    tempInK=float(jsonobj['main']['temp'])
    tempMinK=float(jsonobj['main']['temp_min'])
    tempMaxK=float(jsonobj['main']['temp_max'])
    press=float(jsonobj['main']['pressure'])
    hum=float(jsonobj['main']['humidity'])

    mininc=tempMinK-273.15
    maxinc=tempMaxK-273.15
    temp=tempInK -273.15
    string=str(temp)+','+str(mininc)+','+str(maxinc)+','+str(press)+','+str(hum)
    file=open("res.txt","w")
    file.write(string)
    file.close()
    #return render_template('temp.html',temp_k=temp,temp_mn=mininc,temp_mx=maxinc,pressure=press,humi=hum)
    return 'ok'

@app.route('/temperature/index',methods=['GET','POST'])
@cross_origin()
def report():
    fileob=open('res.txt','r').read()
    dicto={'d1':fileob}
    return jsonify(dicto)
        
if __name__=='__main__':
    app.run(debug=True,port=5000,host='127.0.0.1')