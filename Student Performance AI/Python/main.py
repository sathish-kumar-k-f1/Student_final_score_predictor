from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel

model = joblib.load("student_model.pkl")

features = ["studytime","G2","absences","freetime","Dalc"]
app = FastAPI()
df = pd.read_csv("student-mat.csv", sep=";")
feature_mean = df[features].mean()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173",
                            "http://127.0.0.1:5173"],
        allow_credentials= True,
        allow_methods=["*"],
        allow_headers=["*"],
)

class StudentData(BaseModel):
    studytime: int
    G2: int
    absences: int
    freetime: int
    Dalc: int

@app.get("/")
def home():
    return{"message": "Student Performance API is running"}

@app.post("/predict")
def predict(data: StudentData):
    input_data = [[
        data.studytime,
        data.G2,
        data.absences,
        data.freetime,
        data.Dalc
    ]]

    prediction = model.predict(input_data)[0]
    score = round(prediction)

    if score >= 16:
        performance = "Excellent"

    elif score >= 13:
        performance = "Good"

    elif score >= 10:
        performance = "Average"

    else:
        performance = "Needs improvement"
    
    positive = []
    negative = []

    input_value= [
        data.studytime,
        data.G2,
        data.absences,
        data.freetime,
        data.Dalc
    ]

    for feature, coef, value in zip(features, model.coef_,input_value):

        avg = feature_mean[feature]

        contribution = coef * (value - avg)

        if contribution > 0:
            positive.append(feature)
            # positive.append(", ")
        else:
            negative.append(feature)
            # negative.append(", ")

    #----------------AI Suggestion System----------------------
    
    best_score = score

    test = {
        "studytime": [data.studytime + 1,data.G2, data.absences, data.freetime, data.Dalc],
        "reduce_absences": [data.studytime,data.G2,max(0,data.absences -1),data.freetime, data.Dalc],
        "reduce_freetime": [data.studytime,data.G2,data.absences,max(0,data.freetime -1), data.Dalc],
        "reduce_Dalc": [data.studytime,data.G2,data.absences,data.freetime, max(0,data.Dalc -1)]
    }

    best_suggestion = "No major improvement suggestion."
    for action, values in test.items():
        new_pred = model.predict([values])[0]
        new_score = round(new_pred)


        if new_score > best_score:
            best_score = new_score

            if action == "studytime":
                best_suggestion = f"If you study one more hour your predicted score could become {new_score}"
            
            elif action == "reduce_absences":
                best_suggestion = f"If you reduce absences your predicted score could become {new_score}"
            
            elif action == "reduce_freetime":
                best_suggestion = f"If you reduce free time  your predicted score could become {new_score}"
            
            elif action == "reduce_Dalc":
                best_suggestion = f"If you reduce alcohol consumption your predicted score could become {new_score}"

    # Retuen API Response

    return{
            "Prediction_score": score,
            "Performance": performance,
            "Positive_Factors": ", ".join(positive) if positive else "None",
            "Negative_Factors": ", ".join(negative) if negative else "None",
            "Suggestion" : best_suggestion,
    }

if __name__ == "__main__":
    prediction = predict(StudentData(studytime=2, G2=12, absences=3, freetime=3, Dalc=1))
    print(prediction)