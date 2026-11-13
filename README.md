# 📘 Notice2Action

### From Notice to Action

Notice2Action is a student-focused notice management platform that helps students understand college notices, identify important information, and manage academic tasks efficiently.

Instead of manually reading lengthy college notices, students can upload PDF documents and extract important dates, fees, instructions, and suggested tasks in one place.

🌐 **Live Demo:** [https://notice2action-svv7.onrender.com]

📂 **GitHub Repository:** [https://github.com/yadavsakshi43435-creator/Notice2Action]

---

## 🚩 Problem Statement

College students regularly receive notices regarding examinations, fee submissions, assignments, registrations, events, and other academic activities.

Important information can easily be missed when students have to read multiple lengthy notices manually.

This can lead to missed deadlines, incomplete tasks, and confusion.

## 💡 Our Solution

Notice2Action simplifies notice management by converting PDF notices into organized and actionable information.

Students can upload notices, automatically extract relevant details, save notices, manage tasks, and ask questions about notice content using the Notice Intelligence Assistant.

---

## ✨ Key Features

### 1. PDF Notice Upload

- Upload college notices in PDF format.
- Extract readable text using PyMuPDF.
- Display extracted notice content.

### 2. Smart Notice Analysis

- Detect important dates.
- Identify fee-related information.
- Extract important instructions.
- Generate suggested tasks from notice content.

### 3. Notice Management

- Save analyzed notices in the database.
- Prevent duplicate notice entries.
- View previously saved notices.
- Track notice status.

### 4. Task Management

- Automatically save suggested tasks.
- View all saved tasks.
- Filter pending, completed, upcoming, and overdue tasks.
- Edit task details.
- Update task status.
- Delete individual tasks.

### 5. Dashboard

- View saved notices.
- Monitor total tasks.
- Track pending and completed tasks.
- View upcoming and overdue tasks.

### 6. Notice Intelligence Assistant

- Ask questions about analyzed notice content.
- Find relevant information using rule-based text matching.
- Receive answers based on extracted notice text.

**Note:** The current assistant uses rule-based matching and is not powered by a generative AI model.

---

## ⚙️ Technology Stack

| Technology          | Purpose                      |
| ------------------- | ---------------------------- |
| Python              | Core programming language    |
| Streamlit           | Frontend and web application |
| SQLite              | Database management          |
| PyMuPDF             | PDF text extraction          |
| Regular Expressions | Information detection        |
| Python difflib      | Text similarity matching     |
| Git & GitHub        | Version control              |
| Render              | Cloud deployment             |

---

## 🔄 How It Works

1. Student uploads a college notice PDF.
2. PyMuPDF extracts readable text.
3. Notice Analyzer processes the extracted text.
4. Important dates, fees, and instructions are identified.
5. Suggested tasks are generated.
6. Notice and tasks are saved in SQLite.
7. Students manage their tasks through the dashboard.
8. Notice Intelligence Assistant helps answer questions about the analyzed notice.

---

## 🏗️ Project Structure

```text
Notice2Action/
│
├── app.py
├── assistant.py
├── database.py
├── notice_analyzer.py
├── pdf_extractor.py
├── requirements.txt
├── README.md
│
├── docs/
│   ├── PRD.md
│   └── TRD.md
│
└── .gitignore
```

---

## 🚀 Installation and Setup

### Prerequisites

- Python 3.11 or later
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yadavsakshi43435-creator/Notice2Action.git
```

### Step 2: Navigate to the Project Folder

```bash
cd Notice2Action/Notice2Action
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

---

## ⚠️ Current Limitations

- Currently supports text-based PDF notices only.
- Scanned PDFs and image-based notices are not supported because OCR is not implemented.
- Notice information extraction is primarily rule-based and may not identify every notice format accurately.
- The Notice Intelligence Assistant uses rule-based text matching and may not always provide contextually accurate answers.
- Automatic notifications and external calendar integration are not currently available.
- SQLite is used for data storage; persistent cloud database integration is a future improvement.

---

## 🔮 Future Scope

- OCR support for scanned and image-based notices.
- AI-powered notice summarization and information extraction.
- Improved contextual understanding through advanced AI models.
- Automatic task and reminder notifications.
- Calendar integration for important deadlines.
- Improved multilingual notice understanding.
- Cloud-based database and reliable data persistence.
- Mobile-friendly access for students.

---

## 🎯 Project Objective

Our objective is to reduce the effort required to understand and manage college notices by transforming important academic information into organized and actionable tasks.

**Notice2Action — Never Miss an Important Notice Again!**

---

## 👥 Project Documentation

- [Product Requirements Document (PRD)](docs/PRD.md)
- [Technical Requirements Document (TRD)](docs/TRD.md)

---

## 📜 License

This project was developed as an academic project for IDEATHON 2026.



