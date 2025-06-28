from pydantic import BaseModel , EmailStr,AnyUrl,Field ,field_validator
from typing import List , Dict , Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies:Optional[List[str]]=None
    contact_details:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        
        valid_domains = ['wrc.edu.com.np','pul.edu.com.np']
        domain_name = value.split('@')[-1] # extracting the part after @ from email

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value 
    
    # to return the name in upper case
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)


def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)

patient_info = {'name':'Avishek Basyal'  ,'email':'pas078bct008@wrc.edu.com.np' ,'age':21 , 'weight':58.8 , 'married':True , 'contact_details':{'phone':'123456'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)