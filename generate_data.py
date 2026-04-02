import random

questions = [
    "How can I open a bank account?",
    "How do I check my balance?",
    "I lost my debit card",
    "How can I apply for a loan?",
    "What are your branch timings?",
    "How do I reset my password?",
    "What should I do if my transaction fails?",
    "Do you provide credit cards?",
    "How do I transfer money?",
    "How can I close my account?",
    "What is the minimum balance?",
    "How can I activate my card?",
    "How do I update my KYC?",
    "What is mobile banking?",
    "How do I block my card?",
    "How can I change my PIN?",
    "What are the charges for ATM withdrawal?",
    "How do I check transaction history?",
    "What is internet banking?",
    "How do I contact customer support?"
]

answers = [
    "You can open a bank account online or by visiting your nearest branch.",
    "You can check your balance via mobile banking, ATM, or internet banking.",
    "Please block your debit card immediately using mobile banking or customer support.",
    "You can apply for a loan online or at your nearest branch.",
    "Our branches are open from 9 AM to 4 PM on working days.",
    "Use the 'forgot password' option on the login page to reset your password.",
    "If your transaction fails, wait for reversal or contact support.",
    "Yes, we provide multiple types of credit cards.",
    "You can transfer money using NEFT, RTGS, or IMPS.",
    "Visit the branch or submit an account closure request online.",
    "Minimum balance depends on the account type.",
    "You can activate your card via ATM or mobile banking.",
    "You can update your KYC online or at the branch.",
    "Mobile banking allows you to manage your account from your phone.",
    "You can block your card through mobile banking or customer care.",
    "You can change your PIN at an ATM or through banking apps.",
    "ATM withdrawal charges depend on your account type.",
    "Transaction history is available in your banking app.",
    "Internet banking allows you to access your account online.",
    "You can contact customer support via phone, email, or branch."
]

greetings = [
    "Hi", "Hello", "Hey", "Good morning", "Good evening"
]

responses = [
    "Hello! How can I help you today?",
    "Hi! What banking service do you need?",
    "Welcome to the banking chatbot."
]

with open("data/banking.txt", "w", encoding="utf-8") as f:

    # Greetings
    for _ in range(1000):
        q = random.choice(greetings)
        a = random.choice(responses)
        f.write(q + "\n")
        f.write(a + "\n")

    # Banking Q&A
    for _ in range(9000):
        q = random.choice(questions)
        a = random.choice(answers)
        f.write(q + "\n")
        f.write(a + "\n")

