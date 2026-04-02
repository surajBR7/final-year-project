# Banking Chatbot and Stock Analysis System

## How the Project Works

### 1. User Registration and Login

Users can register using the registration form and log in using their email and password.

#### Code Flow
- `forms.py` defines `RegistrationForm` and `LoginForm`
- `main2.py` handles:
  - `/register`
  - `/login`
  - `/logout`
  - `/account`

The data is stored in SQLite in the `user` table.

---

### 2. Banking Chatbot

The chatbot is created using ChatterBot and trained using data from `data/banking.txt`.

#### Training Flow
- `train.py` reads each line from `data/banking.txt`
- The bot learns question-answer patterns
- Training data is stored in `database.sqlite3`

#### Runtime Flow
- `/chatbot` loads the chatbot UI
- `/get` receives the user message using query parameter `msg`
- `english_bot.get_response(user_text)` generates a reply
- Conversation is saved into `saved_conversations/`

---

### 3. Sentiment Analysis

The sentiment module allows a user to upload a file and analyse the emotional tone of the text.

#### Flow
- `/onsentiment` loads the upload page
- `/analyse` accepts the uploaded file
- The file is saved to `uploads/`
- `File_Pass(file_path).Analysiz_Text()` processes the file
- The result returns counts of positive, negative, and neutral sentiment
- A pie chart is generated using Matplotlib and saved in `static/my_plot.png`
- The result is shown in `display.html`

---

### 4. Stock Data Table

The `/onnifty50` route reads `data.csv` and renders its contents into a responsive HTML table.

#### Flow
- File is read using Python `csv`
- Headers are extracted
- Rows are passed to `onnifty50.html`
- The page displays the data in a Bootstrap table

---

### 5. Prediction Module

The prediction module is used to extend the project into forecasting.

Currently it can be used as:
- A placeholder dashboard
- A simple predictive interface
- A foundation for ML integration

This page can later be upgraded using:
- Moving average
- Linear regression
- LSTM / RNN
- Stock trend visualization

---

## Main Files Explained

### `main2.py`

This is the main Flask application file.

It handles:
- App configuration
- Database initialization
- Chatbot configuration
- Routing
- File upload handling
- Sentiment chart generation
- Session management

#### Important Sections in `main2.py`

**App Configuration**
```python
app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)
app.config['SECRET_KEY'] = 'your_secret_key'
```

**Database Setup**

Creates the SQLite database for storing registered users.

**Chatbot Setup**
```python
english_bot = ChatBot(
    'Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)
```

**Routes**
- `/home`
- `/register`
- `/login`
- `/account`
- `/chatbot`
- `/get`
- `/onsentiment`
- `/analyse`
- `/onnifty50`
- `/prediction`

---

### `forms.py`

Contains form classes for registration and login.

**RegistrationForm**

Fields:
- `username`
- `email`
- `password`
- `confirm_password`

**LoginForm**

Fields:
- `email`
- `password`
- `remember`

---

### `train.py`

This script trains the chatbot.

#### Flow
- Deletes old chatbot DB if it exists
- Creates a new chatbot instance
- Reads training files from `data/`
- Uses `ListTrainer` to train the bot
- Saves training into `database.sqlite3`

**Run:**
```bash
python3 train.py
```

---

### `data/banking.txt`

This file contains chatbot training conversations.

**Example:**
```
Hi
Hello! Welcome to the banking chatbot.

How can I open a bank account?
You can open a bank account online or by visiting the nearest branch.
```

The chatbot learns by matching one line as input and the next line as response.

---

### `templates/`

Contains all HTML files used by Flask with Jinja templating.

#### `base.html`
Master layout for all pages. Includes:
- Navbar
- Footer
- Bootstrap
- Flashed messages

All other templates extend this file.

#### `home.html`
Landing page with feature cards and navigation.

#### `register.html` / `login.html`
Forms for user authentication using Bootstrap styling.

#### `index.html`
Chatbot interface page.

#### `onsentiment.html`
File upload page for sentiment analysis.

#### `display.html`
Displays sentiment results and pie chart.

#### `onnifty50.html`
Displays stock data table.

#### `prediction.html`
Prediction module page.

---

### `static/css/style.css`

Custom CSS for:
- Cards
- Chat bubbles
- Responsive design
- Tables
- Visual layout

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/final-year-project.git
cd final-year-project
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask flask-wtf wtforms email_validator matplotlib pandas numpy chatterbot spacy
python3 -m spacy download en_core_web_sm
```

### 4. Create Required Folders
```bash
mkdir -p data uploads saved_conversations static/css templates
```

### 5. Train Chatbot
```bash
python3 train.py
```

### 6. Run the Application
```bash
python3 main2.py
```

### 7. Open in Browser
```
http://127.0.0.1:5000
```

---

## How to Use

### Banking Chatbot
1. Open the chatbot page
2. Type a banking-related question
3. Receive a chatbot response

**Examples:**
- Hi
- How do I check my balance?
- I lost my debit card
- How can I apply for a loan?

### Sentiment Analysis
1. Go to **Analyse File** page
2. Upload a text file
3. View sentiment counts and chart

### Stock Table
1. Open the **Nifty50** page
2. View data from `data.csv`

### Prediction
1. Open **Prediction** page
2. Use it as a forecasting dashboard base
3. Extend later with ML models

---

## Challenges Faced

During development, several issues were encountered and resolved:

- Missing `saved_conversations` folder
- Missing `templates` folder
- ChatterBot database mismatch
- Missing spaCy model
- Flask-WTF 403/CSRF issues
- Missing `email_validator`
- Matplotlib MacOS backend error
- Invalid pie chart data issues
- Route endpoint mismatches
- GitHub authentication issues

These were fixed through:
- Proper directory setup
- Backend corrections
- Dependency installation
- Route updates
- Safer file handling
- Non-interactive Matplotlib backend

---

## Future Enhancements

This project can be improved further by adding:

- Password hashing using `werkzeug.security`
- Flask-Login for secure authentication
- Real stock prediction using ML models
- Live banking APIs
- Fraud detection module
- Account dashboard charts
- Chatbot intent classification
- FAQ quick buttons
- Export chat history
- Admin panel
- Deployment to cloud platforms

---

## Learning Outcomes

This project helped in understanding:

- Full-stack Flask development
- Template inheritance using Jinja2
- Session-based login systems
- SQLite integration
- Chatbot training and response generation
- Sentiment analysis workflow
- File uploads and server-side processing
- Responsive UI design
- Debugging real-world Python/Flask issues

---

## Screens / Modules

- Home page
- About page
- Contact page
- Register page
- Login page
- Account dashboard
- Banking chatbot
- File sentiment analysis
- Stock table page
- Prediction module

---

## Author

**Suraj Rajolad**  
*Final Year Project – Banking Chatbot and Stock Analysis System*