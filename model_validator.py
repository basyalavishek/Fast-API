from pydantic import BaseModel , EmailStr,AnyUrl,model_validator
from typing import List , Dict , Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies:Optional[List[str]]=None
    contact_details:Dict[str,str]

    @model_validator(mode='after') # after means after the type coersion
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patient older than 60 must have emergency contact')
        return model

    

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)


def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)

patient_info = {'name':'Avishek Basyal'  ,'email':'pas078bct008@wrc.edu.com.np' ,'age':61 , 'weight':58.8 , 'married':True , 'contact_details':{'phone':'123456','emergency':'9866'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)