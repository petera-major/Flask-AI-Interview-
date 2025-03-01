import openai
import os
from dotenv import load_dotenv
import random

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions(role, difficulty="Intermediate"):
    prompt = f"Generate 6 {difficulty}-level interview questions for a {role} position. Ask them naturally like in a conversation. DO NOT number them (no 'Q1', '1.', etc.)."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def evaluate_answers(question, user_answer):
    prompt= f"""

    You are a **friendly, engaging AI interviewer**.
    Your goal is to **evaluate the candidate’s response in a casual, human-like way**—without using "AI Response:" or robotic feedback.

    **Instructions:**
    - DO NOT ask a new question immediately. First, acknowledge the user's answer.
    - Provide a warm, conversational response. If needed, gently correct mistakes.
    - Wait for the user before moving to the next question.
    - DO NOT number questions (no "1.", "Q1:", etc.).
    - Ask only **one** question at a time.

    **Example Conversation:**
    User: "I think my biggest strength is problem-solving."
    AI: "Oh, that’s a fantastic skill! Problem-solving is so important in software development. Can you give me an example of a time you solved a tough problem?"

    Now, evaluate the following:
    
    **Question:** {question}
    **Candidate's Answer:** {user_answer}

    **AI’s response:**

    """

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
