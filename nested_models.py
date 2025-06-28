from pydantic import BaseModel

class Address(BaseModel):
    province:str
    district:str
    city:str
    pincode:str

class Patient(BaseModel):
    name:str
    gender:str
    address:Address

address_dict = {'province':'Lumbini','district':'Arghakhanchi','city':'Sandhikharka','pincode':'1004'}

address1 = Address(**address_dict)

patient_dict = {'name':'Avishek Basyal','gender':'male','address':address1}

patient1 = Patient(**patient_dict)

print(patient1.address.city)


