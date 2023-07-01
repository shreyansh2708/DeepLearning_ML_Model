from flask import Flask,request,redirect,session,jsonify
from pymongo import MongoClient
from flask_cors import CORS
from crack import dent
import numpy as np
from PIL import Image
import io
import base64
from Measure import ms
from main_photo import measure

app=Flask(__name__)
mongo=MongoClient("mongodb+srv://chandraniroysk:babairoy123@cluster0.arzzosh.mongodb.net/?retryWrites=true&w=majority")
db=mongo.get_database('users')
CORS(app)


@app.route('/create',methods=["POST"])
def dbase():
    body=request.json
    id=body.id
    db[id].insert_one({'Name':body.name})


@app.route('/crack',methods=['POST','GET'])
def crk():
    if request.method=='POST':
        img=request.files['image']
        name=img.filename
        path='E:/hack/images/'+name
        img.save(path)
        print(path)
        return redirect('http://localhost:3000/results')
    if request.method=='GET':
        image_np=dent()
        image = Image.fromarray(image_np)
        image_data = io.BytesIO()
        image.save(image_data, format='PNG')
        image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    
        return jsonify({
            "Image":image_base64
        })
    
pth=None
@app.route('/object',methods=['POST','GET'])
def meas():
    global pth
    if(request.method=='POST'):
        img=request.files['image']
        name=img.filename
        pth='E:/hack/object/'+name
        img.save(pth)
        print(pth)
        return redirect('http://localhost:3000/object')
    if(request.method=='GET'):
        image_np=ms(pth)
        image = Image.fromarray(image_np)
        image_data = io.BytesIO()
        image.save(image_data, format='PNG')
        image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    
        return jsonify({
            "Image":image_base64
        })

@app.route('/live',methods=['GET'])
def scan():
    measure()
    return redirect('http://localhost:3000/object')

if __name__=='__main__':
    app.debug=True
    app.run()
