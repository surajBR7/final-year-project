import os
import csv
import sqlite3
import matplotlib
import pandas as pd
import numpy as np

# IMPORTANT: set non-GUI backend before importing pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, render_template, flash, redirect, request, session, url_for
from forms import RegistrationForm, LoginForm
from get_tweets import TweetName
from front_end_gui import File_Pass

from chatterbot import ChatBot


# =========================================================
# CONFIG
# =========================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'stock_database.db')
CHATBOT_DB = 'sqlite:///database.sqlite3'
CONVERSATION_FOLDER = os.path.join(BASE_DIR, 'saved_conversations')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


# =========================================================
# SETUP HELPERS
# =========================================================
def ensure_directories():
    """Create required folders if they do not exist."""
    os.makedirs(CONVERSATION_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(STATIC_FOLDER, exist_ok=True)
    os.makedirs(TEMPLATES_FOLDER, exist_ok=True)


def init_db():
    """Create user table if it does not exist."""
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    cur.close()
    conn.close()


def get_db_connection():
    """Return sqlite connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_next_conversation_number():
    """Return next numeric conversation filename."""
    files = os.listdir(CONVERSATION_FOLDER)
    numbers = []

    for file_name in files:
        if file_name.isdigit():
            numbers.append(int(file_name))

    return (max(numbers) + 1) if numbers else 1


def create_conversation_file():
    """Create initial conversation file if needed for this app run."""
    file_number = get_next_conversation_number()
    file_path = os.path.join(CONVERSATION_FOLDER, str(file_number))

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(
            "bot : Hi There! I am a medical chatbot. "
            "You can begin conversation by typing in a message and pressing enter.\n"
        )

    return file_number


def save_chat_message(file_number, user_text, bot_response):
    """Append chatbot messages to conversation file."""
    file_path = os.path.join(CONVERSATION_FOLDER, str(file_number))

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"user : {user_text}\n")
        file.write(f"bot : {bot_response}\n")


# =========================================================
# INITIALIZE APP
# =========================================================
ensure_directories()
init_db()
filenumber = create_conversation_file()


# =========================================================
# CHATBOT SETUP
# NOTE:
# If ChatterBot still fails, install:
#   pip install chatterbot spacy
#   python3 -m spacy download en_core_web_sm
# =========================================================
english_bot = ChatBot(
    'Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Sorry, I do not understand. Please ask a banking-related question.',
            'maximum_similarity_threshold': 0.75
        }
    ]
)

# =========================================================
# ROUTES
# =========================================================
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/contactus")
def contactus():
    return render_template("contactus.html", title="Contact Us")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO user(name, email, password) VALUES (?, ?, ?)",
                (form.username.data, form.email.data, form.password.data)
            )
            conn.commit()
            flash(f"Registration successful for {form.username.data}!", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("This email is already registered.", "danger")

        finally:
            cur.close()
            conn.close()

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM user WHERE email = ? AND password = ?",
            (form.email.data, form.password.data)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session["logged_in"] = True
            session["user_email"] = form.email.data
            flash(f"{form.email.data} logged in successfully.", "success")
            return redirect(url_for("account"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/account")
def account():
    if not session.get("logged_in"):
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    return render_template("account.html", title="Account")


@app.route("/logout")
def logout():
    session["logged_in"] = False
    session.pop("user_email", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/onprediction", methods=["GET", "POST"])
def onprediction():
    return render_template("onprediction.html", title="Prediction")


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    csv_path = os.path.join(BASE_DIR, "data.csv")

    if not os.path.exists(csv_path):
        flash("data.csv file not found.", "danger")
        return render_template("prediction.html", title="Prediction")

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        flash(f"Error reading CSV file: {exc}", "danger")
        return render_template("prediction.html", title="Prediction")

    columns = list(df.columns)
    prediction_result = None
    chart_ready = False
    preview_data = []

    if request.method == "POST":
        selected_column = request.form.get("column_name", "").strip()

        if selected_column not in df.columns:
            flash("Please select a valid numeric column.", "warning")
            return render_template(
                "prediction.html",
                title="Prediction",
                columns=columns,
                preview_data=preview_data
            )

        try:
            series = pd.to_numeric(df[selected_column], errors="coerce").dropna()

            if len(series) < 5:
                flash("Not enough numeric data in selected column for prediction.", "warning")
                return render_template(
                    "prediction.html",
                    title="Prediction",
                    columns=columns,
                    preview_data=preview_data
                )

            # Use last 5 values to predict next value
            last_values = series.tail(5)
            next_prediction = round(last_values.mean(), 2)

            prediction_result = {
                "column": selected_column,
                "last_5_values": list(last_values.values),
                "predicted_next_value": next_prediction,
                "latest_actual_value": round(series.iloc[-1], 2)
            }

            preview_data = df.head(10).to_dict(orient="records")

            # Create chart
            plot_series = series.tail(20).reset_index(drop=True)
            x_actual = list(range(1, len(plot_series) + 1))
            y_actual = plot_series.tolist()

            x_pred = len(plot_series) + 1
            y_pred = next_prediction

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(x_actual, y_actual, marker='o', label="Actual Values")
            ax.plot(x_pred, y_pred, marker='o', markersize=10, label="Predicted Next Value")
            ax.set_title(f"Prediction for {selected_column}")
            ax.set_xlabel("Data Points")
            ax.set_ylabel(selected_column)
            ax.legend()
            ax.grid(True)

            plot_path = os.path.join(STATIC_FOLDER, "prediction_plot.png")
            fig.savefig(plot_path, bbox_inches="tight")
            plt.close(fig)

            chart_ready = True

        except Exception as exc:
            flash(f"Prediction failed: {exc}", "danger")

    else:
        preview_data = df.head(10).to_dict(orient="records")

    return render_template(
        "prediction.html",
        title="Prediction",
        columns=columns,
        prediction_result=prediction_result,
        chart_ready=chart_ready,
        preview_data=preview_data
    )


@app.route("/sentiment", methods=["GET", "POST"])
def sentiment():
    if request.method == "POST":
        company = request.form.get("company", "").strip()

        if company:
            try:
                getweet = TweetName(company)
                getweet.get_tweets()
                flash(f"Tweets fetched for {company}.", "success")
            except Exception as exc:
                flash(f"Error fetching tweets: {exc}", "danger")
        else:
            flash("Please enter a company name.", "warning")

    return render_template("sentiment.html", title="Sentiment")


@app.route("/onnifty50", methods=["GET", "POST"])
def onnifty50():
    csv_path = os.path.join(BASE_DIR, "data.csv")
    header = []
    data = []

    if os.path.exists(csv_path):
        with open(csv_path, newline="", encoding="utf-8") as file:
            result = csv.reader(file)
            header = next(result, [])
            data = [row for row in result]
    else:
        flash("data.csv file not found.", "danger")

    return render_template("onnifty50.html", title="Nifty50", header=header, data=data)


@app.route("/get")
def get_bot_response():
    user_text = request.args.get("msg", "").strip()

    if not user_text:
        return "Please type a message."

    try:
        response = str(english_bot.get_response(user_text))
    except Exception as exc:
        response = f"Chatbot error: {exc}"

    save_chat_message(filenumber, user_text, response)
    return response


@app.route("/analyse", methods=["GET", "POST"])
def analyse():
    if request.method == "POST":
        f = request.files.get("file")

        if not f or f.filename == "":
            flash("No file selected.", "danger")
            return redirect(url_for("onsentiment"))

        # Save uploaded file to uploads folder
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
        f.save(file_path)

        try:
            # Pass actual saved file path
            obj = File_Pass(file_path)
            data_out = obj.Analysiz_Text()

            # Validate and convert values
            positive = float(data_out[0])
            negative = float(data_out[1])
            neutral = float(data_out[2])

            sizes = [positive, negative, neutral]

            if any(value < 0 for value in sizes):
                flash(f"Invalid sentiment values: {sizes}", "danger")
                return redirect(url_for("onsentiment"))

            if sum(sizes) == 0:
                flash("Sentiment analysis returned all zeros. Chart cannot be created.", "warning")
                return redirect(url_for("onsentiment"))

            labels = ["Positive Sentiment", "Negative Sentiment", "Neutral Sentiment"]
            explode = (0.05, 0.05, 0.02)

            fig1, ax1 = plt.subplots(figsize=(6, 6))
            ax1.pie(
                sizes,
                explode=explode,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90
            )
            ax1.axis("equal")

            plot_path = os.path.join(STATIC_FOLDER, "my_plot.png")
            fig1.savefig(plot_path, bbox_inches="tight")
            plt.close(fig1)

            result_dict = {
                "Positive Sentiment": positive,
                "Negative Sentiment": negative,
                "Neutral Sentiment": neutral
            }

            return render_template("display.html", title="Result", result=result_dict)

        except Exception as exc:
            flash(f"Error during analysis: {exc}", "danger")
            return redirect(url_for("onsentiment"))

    return render_template("onsentiment.html", title="Analyse File")

@app.route("/onsentiment", methods=["GET", "POST"])
def onsentiment():
    return render_template("onsentiment.html", title="Analyse File")

@app.route("/chatbot")
def chatbot():
    return render_template("index.html", title="Chatbot")


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)