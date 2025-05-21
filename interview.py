import os
'''from dotenv import load_dotenv'''
from openai import OpenAI

'''load_dotenv()'''

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions(role, difficulty="Intermediate"):
    prompt = f"Generate 6 {difficulty}-level interview questions for a {role} position. Ask them naturally like in a conversation. DO NOT number them."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ OpenAI ERROR (generate_questions):", str(e))
        return "Error generating questions."

def evaluate_answers(question, user_answer):
    prompt = f"""
    You are a warm, conversational, and thoughtful AI interviewer. You're conducting a casual but insightful mock interview. Your goal is to respond to the user's answers in a way that feels like a real person — friendly, curious, and responsive.

    Guidelines:
    - Acknowledge the user’s answer in a friendly tone.
    - If they mentioned a project or detail, react to it.
    - Offer helpful or encouraging feedback if needed.
    - Then, smoothly transition to the next question.
    - Don’t number anything or sound robotic.

    Current Question: {question}
    Candidate’s Answer: {user_answer}

    Respond naturally:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ OpenAI ERROR (evaluate_answers):", str(e))
        return "Error evaluating answer."
