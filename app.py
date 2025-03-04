from flask import Flask, render_template, session, redirect, request, url_for
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import openai
from interview import generate_questions, evaluate_answers

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = "supersecretkey"
socketio = SocketIO(app)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/index", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        job_role = request.form["job_role"]
        difficulty = request.form["difficulty"]
        session["questions"] = generate_questions(job_role, difficulty).split("\n")
        session["current_question_index"] = 0
        session["answers"] = []

        return redirect(url_for("chatroom"))  

    return render_template("index.html")  

@app.route("/chat")
def chatroom():
    if "questions" not in session or not session["questions"]:
        return redirect(url_for("home"))  
    
    return render_template("chat.html")  

@app.route("/test-openai")
def test_openai():
    import openai
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say hello"}]
        )
        return response.choices[0].message["content"]
    except openai.error.APIConnectionError:
        return "🚨 Error: Unable to connect to OpenAI. Railway may be blocking API requests.", 500
    except openai.error.OpenAIError as e:
        return f"🚨 OpenAI Error: {str(e)}", 500

@app.route("/test")
def test():
    return "🚀 Flask is running!"


@socketio.on("connect")
def handle_connect():
    emit("receive_message", {"message": "👋 Hi there! Welcome to your AI interview."})
    emit("receive_message", {"message": "Can you tell me a bit about yourself before we start the questions?"})

@socketio.on("send_message")
def handle_message(data):

    user_answer = data["message"]
    current_index = session["current_question_index"]
    questions = session["questions"]

    emit("show_typing", {"status": True})

    if current_index >= len(questions):
        emit("receive_message", {"message": "🎉 You're all set. Hope this helped! Interview completed!"})
        session.clear()
        emit("redirect", {"url": "/landing"})  
        return

    session["answers"].append(user_answer)
    feedback = evaluate_answers(questions[current_index], user_answer)

    session["current_question_index"] += 1
    next_question = questions[session["current_question_index"]] if session["current_question_index"] < len(questions) else None

    emit("receive_message", {"message": feedback})  
    if next_question:
        emit("receive_message", {"message": next_question})  

    emit("show_typing", {"status": False})

if __name__ == "__main__":
    if "RAILWAY_ENVIRONMENT" in os.environ: 
        socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), allow_unsafe_werkzeug=True)
    else:
        socketio.run(app, debug=True)