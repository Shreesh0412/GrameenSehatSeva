from fastapi import FastAPI
from database import conn, cursor
from triage import (
    calculate_score, get_priority,
    get_similar_case, get_action,
    get_next_question, build_symptoms_from_answers,
    generate_summary
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ TRIAGE FLOW ------------------

@app.post("/triage/start")
def start_triage():
    return {"question": "Do you have chest pain?", "answers": {}}


@app.post("/triage/next")
def next_question(answers: dict):
    question = get_next_question(answers)

    if question:
        return {"question": question, "answers": answers}

    symptoms = build_symptoms_from_answers(answers)

    return {
        "message": "Triage complete",
        "symptoms": symptoms,
        "answers": answers
    }


@app.post("/triage/submit")
def submit_triage(name: str, age: int, answers: dict):
    # 1. Build symptoms string
    symptoms = build_symptoms_from_answers(answers)

    # 2. Safely insert patient into database (Fixes the near " " error)
    cursor.execute(
        "INSERT INTO patients (name, age, symptoms) VALUES (?, ?, ?)",
        (name, age, symptoms)
    )
    conn.commit()

    patient_id = cursor.lastrowid

    # 3. Calculate scores and priority
    score, reasons = calculate_score(symptoms, age)
    priority = get_priority(score)
    action = get_action(priority)
    similar_case = get_similar_case(symptoms, age)

    # 4. Safely insert into queue
    cursor.execute(
        "INSERT INTO queue (patient_id, score, priority) VALUES (?, ?, ?)",
        (patient_id, score, priority)
    )
    conn.commit()

    # 5. Generate summary
    summary = generate_summary(name, age, symptoms, score, priority, similar_case)

    return {
        "patient_id": patient_id,
        "score": score,
        "priority": priority,
        "action": action,
        "summary": summary,
        "reasons": reasons
    }


# ------------------ STATUS ------------------

@app.post("/complete/{patient_id}")
def complete_patient(patient_id: int):
    cursor.execute(
        "UPDATE queue SET status = 'done' WHERE patient_id = ?",
        (patient_id,)
    )
    conn.commit()

    return {"message": "Patient treated successfully"}


@app.get("/patient_status/{patient_id}")
def patient_status(patient_id: int):
    data = cursor.execute("""
        SELECT queue.status, queue.priority, queue.score
        FROM queue
        WHERE patient_id = ?
    """, (patient_id,)).fetchone()

    if not data:
        return {"error": "Patient not found"}

    return {
        "status": data[0],
        "priority": data[1],
        "score": data[2]
    }
