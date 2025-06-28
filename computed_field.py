from pydantic import BaseModel , EmailStr,AnyUrl,computed_field
from typing import List , Dict , Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float # in kg
    height:float # in meters
    married:bool


    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height ** 2),2)
        return bmi
    

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print('BMI',patient.bmi) # we have not defined bmi , we are calculating bmi from the weight and height which is called computed field , and the name 'bmi' should be same as the function name

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)

patient_info = {'name':'Avishek Basyal'  ,'email':'pas078bct008@wrc.edu.com.np' ,'age':61 , 'weight':65 , 'height':1.67, 'married':True }

patient1 = Patient(**patient_info)

insert_patient_data(patient1)