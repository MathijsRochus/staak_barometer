# 📊 The Strike Barometer (De Staak Barometer)

The **Strike Barometer** is an interactive web application designed to gauge public opinion regarding strike events. It aims to capture the "silent majority" view by allowing citizens to vote on their stance regarding specific strikes.

The application features secure authentication, real-time data visualization, and a multilingual interface (Dutch, French, English).

## ✨ Key Features

* **Secure Authentication:** User Login, Registration, and Password Reset powered by Supabase Auth.
* **Multilingual Support:** Fully translated interface in NL, FR, and EN.
* **Voting System:**
    * Users can vote once per event.
    * Options include current work status (Striking vs. Working) and opinion (Agree vs. Disagree).
* **Live Analytics:** Interactive charts display real-time voting results (charts are hidden until the user votes).
* **Admin Dashboard:** A secured interface for administrators to create new strike events.
* **Privacy Focused:** Row Level Security (RLS) ensures users can only see their own voting history, while aggregated data is fetched anonymously.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend & Database:** [Supabase](https://supabase.com/) (PostgreSQL)
* **Language:** Python 3.x
* **Data Processing:** Pandas

## 📂 Project Structure

The project follows a modular MVC-style architecture:

```text
/staak-barometer
├── .streamlit/
│   └── secrets.toml       # API keys (Excluded from Git)
├── src/
│   ├── backend/           # Database & Auth logic
│   │   ├── client.py      # Supabase client initialization
│   │   └── service.py     # Core functions (login, vote, fetch_data)
│   ├── views/             # UI Components (Pages)
│   │   ├── login.py       # Login/Register tabs
│   │   ├── home.py        # Event feed
│   │   ├── detail.py      # Voting & Charts
│   │   └── admin.py       # Event creation tool
│   └── utils/             # Helpers
│       └── text.py        # Translation dictionaries
├── main.py                # Main Entry Point & Router
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
