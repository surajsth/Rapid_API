from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

# from GET_ import load_data

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the patient", examples=['p01'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City of the patient')]
    age: Annotated[int, Field(...,gt=0, lt=120,description='Age of the patient')]
    gender: Annotated[Literal['male', 'female','others'], Field(..., description='Gender of the patient')]
    height:Annotated[float, Field(..., gt=0, description='Height of the patient in meter')]
    weight: Annotated[float, Field(..., gt=0,description='Weight of the patientin kg')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi <25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdated(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('Patients.json', 'r') as f:
        data = json.load(f)

    return data


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/view")
def view():
    data = load_data()

    return data

@app.put('/edit/{patient_id}')
def updated_patient(patient_id:str, patient_update: PatientUpdated):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not Found")

    existing_patient_info = data[patient_id]

    # conveting into dictonary
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

    # existing_patient_info -> pydantic obj -> upadted bmi + verdict
    existing_patient_info['id'] = patient_id
    patinet_pydnatic_object = Patient(**existing_patient_info)

    # pydantic object -> dict
    existing_patient_info = patinet_pydnatic_object.model_dump(exclude='id')
    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200,  content={'message': "Patient Updated sucessfully"})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})
