# Notice2Action

### From College Notices to Clear Student Actions

Notice2Action is a College Notice Intelligence and Student Action Management System designed to help students understand lengthy college notices and keep track of important information.

## Problem Statement

Colleges regularly share notices containing important deadlines, examination details, fee information, events, and instructions.

Students may find it difficult to identify important information from lengthy notices and keep track of the actions they need to complete.

## Our Solution

Notice2Action simplifies this process by allowing students to upload college notice PDFs, extract their text, identify important information, and save notices for easy tracking.

It aims to make college communication more accessible, organized, and student-friendly.

## Key Features

- **PDF Notice Upload:** Upload college notices in PDF format.
- **Automatic Text Extraction:** Extract readable text from PDF documents.
- **Deadline Detection:** Identify important dates mentioned in notices.
- **Fee Detection:** Find fee-related amounts and information.
- **Instruction Identification:** Extract important instructions and action-related information.
- **Notice Management:** Save analyzed notices for future reference.
- **Student Dashboard:** View saved notices in one place.
- **Status Tracking:** Mark notices as Pending or Completed.
- **Duplicate Prevention:** Prevent saving the same notice multiple times.

## Technology Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core programming language |
| Streamlit  | User interface            |
| PyMuPDF    | PDF text extraction       |
| SQLite     | Database management       |
| Pandas     | Data handling             |

## How It Works

1. Student uploads a college notice PDF.
2. Notice2Action extracts readable text from the document.
3. The system identifies dates, fees, and instructions.
4. Student reviews the extracted information.
5. The notice can be saved to the database.
6. Student tracks saved notices through the dashboard.

## Project Structure

```text
Notice2Action/
│
├── app.py
├── database.py
├── notice_analyzer.py
├── pdf_extractor.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yadavsakshi43435-creator/Notice2Action.git
```

### 2. Open the Project Folder

```bash
cd Notice2Action
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## Current Limitations

- Currently supports text-based PDFs.
- Scanned PDFs and image-based notices are not supported yet because OCR is not implemented.
- Information detection is rule-based and may not identify every notice format correctly.
- AI-based analysis and Gemini API integration are potential future enhancements.

## Future Scope

- OCR support for scanned notices.
- AI-powered notice summarization.
- Automatic task and reminder generation.
- Calendar integration for important deadlines.
- Improved multilingual notice understanding.
- Cloud-based access for students.

## Team – Nextrio

| Team Member      | Responsibility                        |
| ---------------- | ------------------------------------- |
| Sakshi Yadav     | Team Leader – Backend and Integration |
| Rajni Singh      | Frontend and UI                       |
| Rimjhim Kushwaha | Database and Testing                  |

## Project Information

**Event:** IDEATHON 2026
**Project Name:** Notice2Action
**Status:** Under Development

---

*Making college notices easier to understand and student actions easier to manage.*


