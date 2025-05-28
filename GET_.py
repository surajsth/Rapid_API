from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('Patients.json', 'r') as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage the patient"}


@app.get("/view")
def view():
    data = load_data()

    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    else:
        return {'error': 'patient not found'}
    
# for selective details from id  --> HTTpException
@app.get('/patients/{patient_id}')
def view_patients(patient_id: str = Path(..., description="ID of the pateinet in DB", example="p01")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    else:
        return HTTPException(status_code=404, details="patient not found")


# Query Parameter -> pass additional information eg height, age...
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"),
                  order: str = Query('asc', description="Sort in Ascending or descending")):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid fields select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid Order select between asc or desc')

    data = load_data()
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
