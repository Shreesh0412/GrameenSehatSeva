import csv
import os

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.csv")

def calculate_score(symptoms, age):
    if not symptoms.strip():
        return 0, ["No symptoms provided"]

    score = 0
    reasons = []
    symptoms = symptoms.lower()

    if "chest pain" in symptoms:
        score += 40
        reasons.append("Chest pain (+40)")

    if "breathing" in symptoms:
        score += 30
        reasons.append("Breathing issue (+30)")

    if "unconscious" in symptoms:
        score += 50
        reasons.append("Unconscious (+50)")

    if "fever" in symptoms:
        score += 10
        reasons.append("Fever (+10)")

    if "headache" in symptoms:
        score += 5
        reasons.append("Headache (+5)")

    if age > 60:
        score += 20
        reasons.append("Age risk (+20)")

    return min(score, 100), reasons


def get_priority(score):
    if score >= 70:
        return "emergency"
    elif score >= 40:
        return "priority"
    else:
        return "basic"


def get_action(priority):
    if priority == "emergency":
        return "Immediate hospital visit / ambulance recommended"
    elif priority == "priority":
        return "Visit clinic soon"
    else:
        return "Basic teleconsultation is sufficient"


def get_similar_case(symptoms, age):
    try:
        with open(DATASET_PATH, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(word in symptoms for word in row["symptoms"].split()):
                    return row
    except Exception as e:
        print("Dataset error:", e)

    return None


def generate_summary(name, age, symptoms, score, priority, similar_case=None):
    summary = f"Patient {name} ({age} yrs). "
    summary += f"Symptoms: {symptoms}. "
    summary += f"Risk Score: {score}/100 ({priority}). "

    if priority == "emergency":
        summary += "Immediate medical attention required. "
    elif priority == "priority":
        summary += "Needs early consultation. "
    else:
        summary += "Condition stable. "

    if similar_case:
        summary += f"Similar case: {similar_case['symptoms']}."

    return summary


def get_next_question(answers):
    questions = [
        "Do you have chest pain?",
        "Do you have breathing issues?",
        "Do you have fever?",
        "Do you have headache?",
        "Are you unconscious?"
    ]

    for q in questions:
        if q not in answers:
            return q

    return None


# ✅ FIXED: supports Quick Add + normal flow
def build_symptoms_from_answers(answers):
    # 🔥 Quick Add support
    if "symptoms" in answers:
        return answers["symptoms"]

    symptoms = []

    if answers.get("Do you have chest pain?") == "yes":
        symptoms.append("chest pain")

    if answers.get("Do you have breathing issues?") == "yes":
        symptoms.append("breathing")

    if answers.get("Do you have fever?") == "yes":
        symptoms.append("fever")

    if answers.get("Do you have headache?") == "yes":
        symptoms.append("headache")

    if answers.get("Are you unconscious?") == "yes":
        symptoms.append("unconscious")

    return " ".join(symptoms)
