import openai
import os
from dotenv import load_dotenv
import random

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_questions(role, difficulty="Intermediate"):
    prompt = f"Generate 6 {difficulty}-level interview questions for a {role} position. Ask them naturally like in a conversation. DO NOT number them (no 'Q1', '1.', etc.)."

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def evaluate_answers(question, user_answer):
    prompt = f"""
    You are a warm, conversational, and thoughtful AI interviewer. You're conducting a casual but insightful mock interview. Your goal is to respond to the user's answers in a way that feels like a real person — friendly, curious, and responsive.

    **Guidelines:**
    - Start by briefly acknowledging or reacting to the user's answer in a natural tone.
    - If the user shared a personal project or experience, comment on it thoughtfully.
    - Offer encouragement, gentle clarification, or corrections only if needed.
    - If the answer was unclear or weak, kindly ask a follow-up or suggest improvements.
    - Then, smoothly transition to the next interview question.
    - DO NOT number questions (no "1.", "Q1:", etc.).
    - Keep the tone supportive, relaxed, and professional.

    **Example:**
    User: "One project I built was a meal planner app that used React and Firebase."
    AI: "That sounds really useful — a meal planner with React and Firebase is a great way to show both front-end and back-end skills. How did you approach the database design for storing user preferences?"

    Now, continue the interview:

    **Current Question:** {question}
    **Candidate’s Answer:** {user_answer}

    Respond in a natural tone:
    """


    response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

    return response.choices[0].message.content
