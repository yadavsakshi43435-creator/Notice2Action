# Notice2Action

## Product Requirements Document (PRD)

**Project Name:** Notice2Action  
**Team Name:** Nextrio&#32;  
**Project Type:** Student Productivity \& Notice Management System

### 1\. Introduction

Notice2Action is a student-focused platform designed to simplify college notices by converting lengthy PDF notices into structured and actionable information.

It helps students understand important announcements, identify deadlines, track responsibilities, and avoid missing important college activities.

### 2\. Problem Statement

Students frequently receive lengthy college notices containing examination schedules, fee deadlines, registration instructions, event announcements, and other important information.

Manually reading and tracking every notice can be time-consuming. Important dates and instructions may be overlooked, resulting in missed deadlines and incomplete tasks.

### 3\. Proposed Solution

Notice2Action provides a centralized platform where students can upload college notice PDFs and extract relevant information.

The platform organizes the extracted information into understandable sections and helps students track their pending and completed activities.

### 4\. Target Users

- College and university students.
- Students managing multiple academic announcements.
- Educational institutions looking to simplify notice management.

### 5\. Product Objectives

- Simplify lengthy college notices.
- Extract important dates, fees, and instructions.
- Help students organize their responsibilities.
- Reduce the chances of missing deadlines.
- Provide a centralized notice management dashboard.

### 6\. Core Functional Requirements

**FR-01: PDF Upload**
Students should be able to upload college notice PDFs.

**FR-02: Text Extraction**
The system should extract readable text from uploaded PDFs.

**FR-03: Notice Analysis**
The system should identify relevant dates, fees, and instructions using text-processing rules.

**FR-04: Notice Storage**
Analyzed notices should be saved in a database.

**FR-05: Duplicate Detection**
The system should identify duplicate notices using content hashing.

**FR-06: Student Dashboard**
Students should be able to view their saved notices.

**FR-07: Status Management**
Students should be able to mark notices as Pending or Completed.

**FR-08: Task Management**
The system is designed to support individual actionable tasks extracted from notices, including task status and deadlines.

**FR-09: Delete Functionality**
Students should be able to delete unwanted saved records.

**FR-10: AI Assistant (Planned)**
A notice-based assistant is proposed to answer questions about uploaded notices and explain important instructions in simple language.

### 7\. Non-Functional Requirements

- Simple and user-friendly interface.
- Reliable PDF processing.
- Consistent database storage.
- Appropriate error handling.
- Maintainable and modular code.
- Accessible through a web browser after deployment.

### 8\. User Workflow

1. Student opens Notice2Action.
2. Student uploads a college notice PDF.
3. The system extracts readable text.
4. The analyzer identifies important information.
5. The student reviews the extracted information.
6. The notice is saved.
7. The student accesses saved notices through the dashboard.
8. The student tracks relevant activities and their completion status.

### 9\. Scope and Limitations

- Initial version focuses on text-based PDF notices.
- Scanned/image-only PDFs are not supported in the current extraction implementation.
- Extracted information may require manual verification.
- AI Assistant and advanced task extraction are subject to implementation and testing.

### 10\. Future Enhancements

- OCR support for scanned notices.
- Advanced AI-based notice understanding.
- Automated reminders for deadlines.
- Multilingual notice explanation.
- Personalized student notifications.
- Integration with institutional portals.

### 11\. Expected Outcome

Notice2Action aims to make college communication easier to understand and manage by transforming unstructured notices into organized student actions.