from pydantic import BaseModel

class Address(BaseModel):
    province:str
    district:str
    city:str
    pincode:str

class Patient(BaseModel):
    name:str
    gender:str
    somke:bool=True
    address:Address

address_dict = {'province':'Lumbini','district':'Arghakhanchi','city':'Sandhikharka','pincode':'1004'}

address1 = Address(**address_dict)

patient_dict = {'name':'Avishek Basyal','gender':'male','address':address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump() # exporting the patient1 in dictionary format
print(temp)

temp1 = patient1.model_dump(include='name') # only export the model with name field in dictionary 
print(temp1)

temp2 = patient1.model_dump(exclude_unset=True) # only export the field that are set while creating object , like smoke is not set so it will not be shown
print(temp2)

temp3 = patient1.model_dump(exclude=['address'])
print(temp3)

tempp = patient1.model_dump_json() # to export in json


