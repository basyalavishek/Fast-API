from fastapi import FastAPI , Path , HTTPException, Query# Path  is used to enhance the readibility of the endpoints 
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated , Literal,Optional
import json


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

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f) # writing the dictionary (which is data) into json file

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


class Patient(BaseModel):
    id:Annotated[str , Field(...,description='Id of the patient',examples=['P001'])]
    name:Annotated[str , Field(...,description='Name of the patient',examples=['Avishek Basyal'])]
    city:Annotated[str , Field(...,description='City where the patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['Male','Female','Others'],Field(...,description='Gender of the patient')]
    height:Annotated[float,Field(...,gt=0 , description='Height of the patient in meters')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the patient in Kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight / (self.height ** 2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if(self.bmi<18.5):
            return 'Underweight'
        elif(self.bmi<25):
            return 'Normal'
        elif(self.bmi<30):
            return 'Normal'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

        
@app.post('/create')

def create_patient(patient:Patient):

    # load existing data
    data = load_data()

    # check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400 , detail='Patieint already exists')

    # add new patient detail
    data[patient.id]=patient.model_dump(exclude=['id']) # it is in dictionary format

    # save into json
    save_data(data)

    return JSONResponse(status_code=201 , content={'message':'Patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail='Patient not found')

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_onset = True)

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

        existing_patient_info['id'] = patient_id
        patient_pydantic_obj = Patient(**existing_patient_info)

        # Pydantic obj -> dict
        existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

        # add this dict to data
        data[patient_id] = existing_patient_info

        # save data
        save_data(data)

        return JSONResponse(status_code=200 , content={'message':'Patieint Updated'})
    
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})
