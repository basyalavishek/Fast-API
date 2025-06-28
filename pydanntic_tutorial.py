from pydantic import BaseModel , EmailStr,AnyUrl,Field
from typing import List , Dict , Optional,Annotated

    # creating a data model (like a schema) 
    # defining a class 'Patient' that inherits from BaseModel, which is provided by Pydantic.
class Patient(BaseModel):
    # by default these are required
    name:Annotated[str,Field(max_length=20 , title='Enter the name of the patient',description='Name of the patient should be less than 20 characters',examples=['Avishek Basyal','Ashok Shrestha'])]

    linkedin_URL : AnyUrl # should be valid url

    email:EmailStr

    age:int = Field(gt=0 , lt=60) # age should be greater than 0 and less than 60

    weight:Annotated[float,Field(gt=0 , strict=True)] # should strictly be float 

    smoker:Annotated[bool , Field(default=None , description='Is the patient Smoker or not')]

    married:Optional[bool] = None # making it optional default value is set tonone

    allergies:Annotated[Optional[List[str]],Field(default=None , max_length=5) ]# list where all items are string and isoptional
    
    contact_details:Dict[str , str] # dictionary where the keys and values bothare string

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.smoker)
    print(patient.allergies)

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)

patient_info = {'name':'Avishek Basyal' ,'linkedin_URL':'https://abc.com' ,'email':'abc@abc.com' ,'age':21 , 'weight':58.8 , 'married':True , 'contact_details':{'phone':'123456'}}

patient1 = Patient(**patient_info) # '**' means unpacking the dictionary

insert_patient_data(patient1)

