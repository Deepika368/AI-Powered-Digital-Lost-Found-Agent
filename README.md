# 🔎 AI-Powered Digital Lost & Found Agent

## 📌 Project Overview

The **AI-Powered Digital Lost & Found Agent** is an AI-assisted web application that helps users report lost and found items and automatically identify possible matches. It compares item descriptions, categories, colors, and locations to find similar reports.

The goal is to reduce the time spent searching for lost belongings using intelligent matching.

## 🎯 Objectives

* Make reporting lost and found items simple.
* Automatically identify possible matching reports.
* Reduce the time needed to locate missing belongings.
* Store and manage reports in a database.
* Provide a simple, user-friendly dashboard.

## ✨ Features

* 📝 Submit lost and found item reports.
* 🧠 AI-assisted description matching using TF-IDF and cosine similarity.
* 📍 Compare item locations and categories.
* 📊 Interactive dashboard with report statistics.
* 🗄️ Store reports using SQLite.
* 🔍 Rank possible matches by similarity score.
* 💻 Simple web interface built with Streamlit.

## 🛠️ Technologies Used

| Technology   | Purpose                      |
| ------------ | ---------------------------- |
| Python       | Application logic            |
| Streamlit    | Web interface                |
| SQLite       | Database management          |
| Scikit-learn | Text similarity and matching |
| Pandas       | Data processing              |

## 📂 Project Structure

```text
AI-Digital-Lost-Found-Agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── lost_found.db  # Generated automatically
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Digital-Lost-Found-Agent.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 2: Open the Project

```bash
cd AI-Digital-Lost-Found-Agent
```

Open this folder in VS Code.

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 🔄 How It Works

1. **Submit a Report:** Users enter the item name, category, color, location, and description.
2. **Store Information:** The application saves the report in an SQLite database.
3. **Analyze Descriptions:** TF-IDF converts report descriptions into numerical features.
4. **Calculate Similarity:** Cosine similarity compares a report against reports of the opposite type.
5. **Rank Matches:** Category and location agreement can increase the matching score.
6. **Display Results:** The application displays possible matches for users to review.

## 🧪 Example

**Lost Report**

* Item: Black leather wallet
* Category: Wallet
* Color: Black
* Location: College library

**Found Report**

* Item: Dark wallet
* Category: Wallet
* Color: Black
* Location: College library

The system compares both reports and ranks the found wallet as a potential match.

*Note: A similarity score is not a probability of ownership. Users must verify ownership before returning an item.*

## 🚀 Future Enhancements

* Semantic matching using sentence embeddings.
* Image-based matching of lost and found objects.
* Email or in-app notifications for potential matches.
* User authentication and role-based access.
* Duplicate report detection.
* Secure ownership verification.
* Multilingual support for English and Telugu.
* Deployment as a public web application.

## 🎓 Applications

* Colleges and universities.
* Offices and workplaces.
* Shopping malls.
* Railway stations and airports.
* Public events and community spaces.

## 🔐 Privacy and Security

Contact information should be handled securely and not exposed publicly. A production version should implement authentication, access controls, secure contact sharing, and a verified item-return process.

## 👨‍💻 Author

**Deepu**
B.Tech Computer Science and Engineering

## 📜 License

This project is intended for educational and demonstration purposes. Add an appropriate open-source license if you plan to distribute the code.

---

⭐ If you find this project useful, consider starring the repository!
