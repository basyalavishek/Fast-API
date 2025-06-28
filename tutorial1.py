from fastapi import FastAPI , Path , HTTPException , Query
# Path  is used to enhance the readibility of the endpoints 

import json

app = FastAPI()

@app.get('/')
def hello():
    return{'message':'Hello World'}

@app.get('/about')
def about():
    return{'message':'Hello My name is Avishek Basyal'}

# To load all  the data from json file
def load_data():
    with open('patients.json','r') as  f:
        data = json.load(f)
    return data

@app.get('/view')
def view():
    data  = load_data()
    return data

# To view specific  patient detail  using Path parameter and exception 
@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(...,description='ID  of the patient in DB', example='P001')) : # defining patient id  should string , '... means 'patient_id' is required

    # load all the data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise (HTTPException(status_code=404 , detail='Patient not foud'))

# Using Query parameter
@app.get('/sort')
def sort_patients(sort_by:str = Query(description='sort on the basis of height,weight,bmi'),order:str = Query('asc',description='sort in asc or desc order')): # by default order is in ascending
   
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise (HTTPException(status_code=400 , detail=f'invalid field selected from {valid_fields}'))

    if order not in ['asc' , 'desc']:
        raise(HTTPException(status_code=400 , detail='invalid order selected from asc and desc'))

    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data
# http://127.0.0.1:8000/sort?sort_by=height&order=desc --> url to show the sorted list in descending order on the basis of height (you can also go to url without order since it is optional)