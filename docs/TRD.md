# Notice2Action
## Technical Requirements Document (TRD)

**Project Name:** Notice2Action  
**Team Name:** Nextrio 
**Version:** Initial Prototype

### 1. Technical Overview
Notice2Action is a Python-based web application that processes college notice PDFs, extracts readable text, identifies important information, and stores analyzed notices for student access.

The system uses a modular architecture to separate PDF processing, notice analysis, database operations, and user interface functionality.

### 2. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend Framework | Streamlit |
| PDF Processing | PyMuPDF |
| Database | SQLite |
| Data Handling | Pandas |
| Version Control | Git and GitHub |
| Cloud Deployment | Render (planned) |

### 3. System Architecture

The application follows a modular processing workflow:

**User Interface → PDF Upload → PDF Text Extraction → Notice Analysis → Database Storage → Student Dashboard**

The proposed AI Assistant will be an additional application module.

### 4. Module Description

**4.1 Application Module (app.py)**
- Provides the Streamlit application interface.
- Handles user interaction and PDF uploads.
- Displays analyzed information and saved notices.
- Connects the interface with backend modules.

**4.2 PDF Extraction Module (pdf_extractor.py)**
- Uses PyMuPDF to open PDF documents.
- Extracts readable text page by page.
- Handles empty and unreadable documents.
- Returns extracted text for further processing.

**4.3 Notice Analysis Module (notice_analyzer.py)**
- Processes extracted notice text.
- Identifies dates, fees, and instructions.
- Uses predefined text-processing and pattern-matching rules.
- Produces structured analysis output.

**4.4 Database Module (database.py)**
- Uses SQLite for persistent data storage.
- Creates and initializes required database tables.
- Stores notice details and extracted information.
- Supports retrieval, status updates, and deletion.
- Includes content-hash-based duplicate detection.

**4.5 Task Management Module (Planned/Under Integration)**
- Stores individual tasks associated with notices.
- Supports task descriptions, deadlines, and status.
- Allows students to organize actionable responsibilities.

**4.6 AI Assistant Module (Planned)**
- Intended to provide notice-related question answering.
- Will use available notice content as context.
- Will explain instructions in simpler language.
- May use an external AI service if successfully integrated.

### 5. Database Design

**Notices Table**

| Field | Description |
|---|---|
| id | Primary key |
| title | Notice title |
| filename | Uploaded PDF filename |
| extracted_text | Extracted notice content |
| dates | Identified dates |
| fees | Identified fees |
| instructions | Identified instructions |
| status | Pending or Completed |
| created_at | Record creation time |
| extracted_text_hash | Duplicate detection hash |

**Tasks Table (Added to backend schema)**

| Field | Description |
|---|---|
| id | Primary key |
| notice_id | Related notice ID |
| task_title | Task title |
| description | Task description |
| deadline | Task deadline |
| source_text | Original supporting text |
| status | Task status |
| created_at | Creation timestamp |

### 6. Processing Workflow

1. The user uploads a PDF through the application.
2. PyMuPDF opens the uploaded document.
3. Readable text is extracted from its pages.
4. The notice analyzer processes the extracted content.
5. Important dates, fees, and instructions are identified.
6. A SHA-256 hash is generated for duplicate detection.
7. The notice is stored in SQLite if it is not a duplicate.
8. Saved records are displayed through the dashboard.

### 7. Error Handling
The system should handle:
- Empty PDF uploads.
- Invalid or corrupted PDF documents.
- PDFs containing no readable text.
- Duplicate notice uploads.
- Invalid status values.
- Database operation errors.

### 8. Security and Data Management
- Database files should not be committed to public GitHub repositories.
- Sensitive credentials should be stored using environment variables.
- Uploaded files should be processed safely.
- Database persistence must be configured appropriately for cloud deployment.

### 9. Deployment Requirements
The planned deployment environment is Render.

Required deployment components:
- GitHub repository.
- Python runtime.
- requirements.txt.
- Streamlit startup command.
- Configured persistent storage for SQLite data, or another suitable persistent database solution.

### 10. Current Technical Limitations
- Current PDF extraction focuses on text-based PDFs.
- OCR is not included in the existing extraction implementation.
- Notice analysis uses predefined rules and patterns rather than a fully trained AI model.
- AI Assistant integration is not considered complete until implemented and tested.
- Cloud deployment and persistent storage configuration remain to be completed.

### 11. Future Technical Improvements
- OCR integration.
- Improved natural-language processing.
- Context-aware AI question answering.
- Automated deadline notifications.
- Enhanced database architecture.
- Cloud database integration if required.

### 12. Conclusion
Notice2Action uses a modular Python architecture to simplify the processing and management of college notices. Its technical design supports future improvements in AI-based understanding, task management, and cloud deployment.