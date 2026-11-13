import streamlit as st
import json
from datetime import date, datetime

from pdf_extractor import extract_text_from_pdf
from notice_analyzer import analyze_notice

from database import (
    initialize_db,
    save_notice,
    get_all_notices,
    update_notice_status,
    save_multiple_tasks,
    get_all_tasks,
    update_task_status,
    update_task,
    get_task_summary,
    delete_task,
    delete_notice
)

from assistant import answer_question


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Notice2Action",
    page_icon="📘",
    layout="wide"
)

initialize_db()


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #172554;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

.hero {
    background: linear-gradient(120deg, #172554, #4338ca);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    color: white;
}

.hero p {
    font-size: 17px;
    color: #e0e7ff;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}

.card h3 {
    color: #1e293b;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    text-align: center;
}

.metric-number {
    font-size: 30px;
    font-weight: bold;
    color: #4338ca;
}

.metric-label {
    color: #64748b;
    font-size: 14px;
}

section[data-testid="stSidebar"] {
    background-color: #eef2ff;
}

.stButton button {
    border-radius: 9px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def safe_json(value):
    if isinstance(value, list):
        return value

    if not value:
        return []

    try:
        result = json.loads(value)
        return result if isinstance(result, list) else []
    except (ValueError, TypeError):
        return []


def format_date(value):
    if not value:
        return "Not specified"

    try:
        return date.fromisoformat(str(value)).strftime("%d %B %Y")
    except (ValueError, TypeError):
        return str(value)


def show_metric(label, number):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{number}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 📘 Notice2Action")
    st.caption("Your notices. Your tasks. One place.")

    st.divider()

    language = st.selectbox(
        "🌐 Language / भाषा",
        ["English", "हिंदी"]
    )

    if language == "English":
        pages = [
            "🏠 Home",
            "📤 Upload Notice",
            "📊 My Dashboard",
            "✅ My Tasks",
            "📁 Notice History",
            "🤖 Notice Assistant",
            "ℹ️ About Project"
        ]
    else:
        pages = [
            "🏠 Home",
            "📤 नोटिस अपलोड करें",
            "📊 मेरा डैशबोर्ड",
            "✅ मेरे कार्य",
            "📁 नोटिस हिस्ट्री",
            "🤖 नोटिस असिस्टेंट",
            "ℹ️ प्रोजेक्ट के बारे में"
        ]

    selected_page = st.radio(
        "Navigation",
        pages
    )

    st.divider()

    st.caption("Built with Python, Streamlit and SQLite")


# Normalize page names so both languages use same backend pages

page_mapping = {
    "🏠 Home": "Home",
    "📤 Upload Notice": "Upload",
    "📤 नोटिस अपलोड करें": "Upload",
    "📊 My Dashboard": "Dashboard",
    "📊 मेरा डैशबोर्ड": "Dashboard",
    "✅ My Tasks": "Tasks",
    "✅ मेरे कार्य": "Tasks",
    "📁 Notice History": "History",
    "📁 नोटिस हिस्ट्री": "History",
    "🤖 Notice Assistant": "Assistant",
    "🤖 नोटिस असिस्टेंट": "Assistant",
    "ℹ️ About Project": "About",
    "ℹ️ प्रोजेक्ट के बारे में": "About"
}

page = page_mapping[selected_page]


# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to Notice2Action 👋</h1>
        <p>
        Never miss an important college notice, deadline or task again.
        </p>
        <p>
        Upload notices, extract important information and manage
        your academic responsibilities in one place.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Everything you need, in one place")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>📄 Smart Notice Analysis</h3>
            <p>Extract important dates, fees and instructions from PDF notices.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>✅ Task Management</h3>
            <p>Convert notice information into tasks and track their progress.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🤖 Notice Assistant</h3>
            <p>Ask questions about your uploaded notice using our rule-based assistant.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## How it works")

    steps = st.columns(4)

    step_data = [
        ("01", "Upload", "Upload your college PDF notice."),
        ("02", "Analyze", "Extract important information."),
        ("03", "Organize", "Save notices and manage tasks."),
        ("04", "Act", "Track deadlines and complete tasks.")
    ]

    for col, item in zip(steps, step_data):
        with col:
            st.markdown(f"""
            <div class="card">
                <h2>{item[0]}</h2>
                <h3>{item[1]}</h3>
                <p>{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    if st.button("📤 Upload Your First Notice"):
        st.session_state["go_to_upload"] = True
        st.rerun()


# ==========================================
# UPLOAD NOTICE PAGE
# ==========================================

elif page == "Upload" or (
    page == "Home" and st.session_state.get("go_to_upload")
):

    st.markdown('<div class="main-title">📤 Upload Notice</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Upload a college PDF notice to extract important information.</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        key="notice_upload"
    )

    if uploaded_file:

        if (
            st.session_state.get("processed_filename")
            != uploaded_file.name
        ):
            st.session_state.pop("analysis", None)
            st.session_state.pop("extracted_text", None)
            st.session_state.pop("processed_filename", None)
            st.session_state.pop("saved_notice_id", None)

        if st.button("🔍 Analyze Notice", type="primary"):

            try:
                pdf_bytes = uploaded_file.getvalue()

                extracted_text = extract_text_from_pdf(pdf_bytes)

                if not extracted_text or not extracted_text.strip():
                    st.error(
                        "No readable text found in this PDF. "
                        "Scanned PDFs are not supported yet."
                    )

                else:
                    analysis = analyze_notice(extracted_text)

                    st.session_state["analysis"] = analysis
                    st.session_state["extracted_text"] = extracted_text
                    st.session_state["processed_filename"] = uploaded_file.name
                    st.session_state["filename"] = uploaded_file.name

                    st.success("Notice analyzed successfully!")

            except Exception:
                st.error(
                    "Unable to read this PDF. Please upload a valid PDF file."
                )

        if st.session_state.get("analysis"):

            analysis = st.session_state["analysis"]

            st.divider()
            st.subheader("📋 Extracted Information")

            dates = analysis.get("dates", [])
            fees = analysis.get("fees", [])
            instructions = analysis.get("instructions", [])
            tasks = analysis.get("tasks", [])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📅 Important Dates")

                if dates:
                    for item in dates:
                        st.write("•", item)
                else:
                    st.info("No dates found.")

            with col2:
                st.markdown("### 💰 Fees")

                if fees:
                    for item in fees:
                        st.write("•", item)
                else:
                    st.info("No fee information found.")

            st.markdown("### 📝 Instructions")

            if instructions:
                for item in instructions:
                    st.write("•", item)
            else:
                st.info("No instructions found.")

            st.markdown("### ✅ Suggested Tasks")

            if tasks:
                for index, task in enumerate(tasks, 1):
                    st.markdown(f"""
                    **{index}. {task.get('task_title', 'Task')}**

                    Deadline: {format_date(task.get('deadline'))}

                    Source: {task.get('source_text', 'Not available')}
                    """)
            else:
                st.info("No tasks identified in this notice.")

            with st.expander("📄 View Extracted Text"):
                st.text(st.session_state["extracted_text"])

            st.divider()

            st.markdown("### 💾 Save Notice")

            notice_title = st.text_input(
                "Enter a title for this notice",
                value=uploaded_file.name.replace(".pdf", "")
            )

            if st.button("💾 Save Notice and Tasks", type="primary"):

                try:
                    notice_id = save_notice(
                        notice_title,
                        st.session_state["filename"],
                        st.session_state["extracted_text"],
                        analysis
                    )

                    if notice_id is not None:

                        saved_tasks = save_multiple_tasks(
                            notice_id,
                            tasks
                        )

                        st.session_state["saved_notice_id"] = notice_id

                        st.success(
                            "Notice and its tasks have been saved successfully!"
                        )

                        st.info(
                            f"Tasks processed: {len(tasks)}"
                        )

                    else:
                        st.warning(
                            "This notice already exists in your database."
                        )

                except Exception as error:
                    st.error(f"Unable to save notice: {error}")


# ==========================================
# DASHBOARD PAGE
# ==========================================

elif page == "Dashboard":

    st.markdown('<div class="main-title">📊 My Dashboard</div>',
                unsafe_allow_html=True)

    notices = get_all_notices()
    summary = get_task_summary()

    st.markdown("### Your Task Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        show_metric("Total Tasks", summary.get("Total", 0))

    with col2:
        show_metric("Pending", summary.get("Pending", 0))

    with col3:
        show_metric("Completed", summary.get("Completed", 0))

    with col4:
        show_metric("Upcoming", summary.get("Upcoming", 0))

    with col5:
        show_metric("Overdue", summary.get("Overdue", 0))

    st.divider()

    st.markdown("### 📄 Saved Notices")

    if not notices:
        st.info("No notices saved yet. Upload your first notice!")

    else:

        for notice in notices:

            with st.expander(
                f"📘 {notice.get('title', 'Untitled Notice')}"
            ):

                st.write("**File:**", notice.get("filename", "N/A"))
                st.write("**Status:**", notice.get("status", "Pending"))

                st.markdown("#### Important Dates")

                for item in safe_json(notice.get("dates")):
                    st.write("•", item)

                st.markdown("#### Fees")

                for item in safe_json(notice.get("fees")):
                    st.write("•", item)

                st.markdown("#### Instructions")

                for item in safe_json(notice.get("instructions")):
                    st.write("•", item)

                current_status = notice.get("status", "Pending")

                new_status = st.selectbox(
                    "Notice Status",
                    ["Pending", "Completed"],
                    index=(
                        1 if current_status == "Completed" else 0
                    ),
                    key=f"notice_status_{notice['id']}"
                )

                if st.button(
                    "Update Notice Status",
                    key=f"update_notice_{notice['id']}"
                ):

                    update_notice_status(
                        notice["id"],
                        new_status
                    )

                    st.success("Notice status updated!")
                    st.rerun()


# ==========================================
# MY TASKS PAGE
# ==========================================

elif page == "Tasks":

    st.markdown('<div class="main-title">✅ My Tasks</div>',
                unsafe_allow_html=True)

    tasks = get_all_tasks()

    if not tasks:
        st.info("No tasks available. Upload a notice first.")

    else:

        filter_option = st.selectbox(
            "Filter Tasks",
            ["All", "Pending", "Completed", "Upcoming", "Overdue"]
        )

        today = date.today()

        for task in tasks:

            deadline = task.get("deadline")
            status = task.get("status", "Pending")

            overdue = False
            upcoming = False

            try:
                deadline_date = date.fromisoformat(str(deadline))

                overdue = (
                    deadline_date < today and status != "Completed"
                )

                upcoming = (
                    deadline_date >= today and status != "Completed"
                )

            except (ValueError, TypeError):
                pass

            if filter_option == "Pending" and status != "Pending":
                continue

            if filter_option == "Completed" and status != "Completed":
                continue

            if filter_option == "Upcoming" and not upcoming:
                continue

            if filter_option == "Overdue" and not overdue:
                continue

            with st.expander(
                f"📌 {task.get('task_title', 'Untitled Task')}"
            ):

                st.write("**Notice:**", task.get("notice_title", "N/A"))

                st.write(
                    "**Description:**",
                    task.get("description") or task.get("source_text", "N/A")
                )

                st.write(
                    "**Deadline:**",
                    format_date(deadline)
                )

                if overdue:
                    st.error("⚠️ Overdue")

                elif upcoming:
                    st.info("📅 Upcoming")

                else:
                    st.success("Completed")

                new_status = st.selectbox(
                    "Task Status",
                    ["Pending", "Completed"],
                    index=(
                        1 if status == "Completed" else 0
                    ),
                    key=f"task_status_{task['id']}"
                )

                if st.button(
                    "Update Status",
                    key=f"update_task_{task['id']}"
                ):

                    update_task_status(
                        task["id"],
                        new_status
                    )

                    st.success("Task status updated!")
                    st.rerun()

                st.divider()

                st.markdown("#### ✏️ Edit Task")

                edited_title = st.text_input(
                    "Task Title",
                    value=task.get("task_title", ""),
                    key=f"edit_title_{task['id']}"
                )

                edited_description = st.text_area(
                    "Description",
                    value=(
                        task.get("description")
                        or task.get("source_text", "")
                    ),
                    key=f"edit_description_{task['id']}"
                )

                edited_deadline = st.text_input(
                    "Deadline (YYYY-MM-DD)",
                    value=task.get("deadline") or "",
                    key=f"edit_deadline_{task['id']}"
                )

                if st.button(
                    "Save Changes",
                    key=f"save_edit_{task['id']}"
                ):

                    if edited_deadline:

                        try:
                            date.fromisoformat(edited_deadline)

                        except ValueError:
                            st.error(
                                "Please enter deadline in YYYY-MM-DD format."
                            )
                            st.stop()

                    update_task(
                        task["id"],
                        edited_title,
                        edited_description,
                        edited_deadline
                    )

                    st.success("Task updated successfully!")
                    st.rerun()

                if st.button(
                    "🗑️ Delete Task",
                    key=f"delete_task_{task['id']}"
                ):

                    delete_task(task["id"])

                    st.success("Task deleted successfully!")
                    st.rerun()


# ==========================================
# NOTICE HISTORY PAGE
# ==========================================

elif page == "History":

    st.markdown('<div class="main-title">📁 Notice History</div>',
                unsafe_allow_html=True)

    notices = get_all_notices()

    if not notices:
        st.info("No notice history available.")

    else:

        st.write(f"Total saved notices: {len(notices)}")

        for notice in notices:

            with st.expander(
                f"📄 {notice.get('title', 'Untitled Notice')}"
            ):

                st.write("**Filename:**", notice.get("filename", "N/A"))
                st.write("**Status:**", notice.get("status", "Pending"))

                st.markdown("**Important Dates**")

                for item in safe_json(notice.get("dates")):
                    st.write("•", item)

                st.markdown("**Fees**")

                for item in safe_json(notice.get("fees")):
                    st.write("•", item)

                if st.button(
                    "🗑️ Delete Notice",
                    key=f"delete_notice_{notice['id']}"
                ):

                    delete_notice(notice["id"])

                    st.success("Notice deleted successfully!")
                    st.rerun()


# ==========================================
# NOTICE ASSISTANT PAGE
# ==========================================

elif page == "Assistant":

    st.markdown('<div class="main-title">🤖 Notice Intelligence Assistant</div>',
                unsafe_allow_html=True)

    st.write(
        "Ask questions about the notice you have most recently analyzed."
    )

    notice_text = st.session_state.get("extracted_text", "")

    if not notice_text:

        st.info(
            "Please upload and analyze a notice first. "
            "The assistant currently uses the notice available in this session."
        )

    else:

        question = st.text_input(
            "Ask something about your notice",
            placeholder="Example: What is the last date for fee submission?"
        )

        if st.button("Ask Assistant", type="primary"):

            if question.strip():

                try:
                    response = answer_question(
                        question,
                        notice_text
                    )

                    st.markdown("### 💬 Answer")
                    st.info(response)

                except Exception as error:
                    st.error(f"Assistant error: {error}")

            else:
                st.warning("Please enter a question.")



# ==========================================
# ABOUT PROJECT PAGE
# ==========================================

elif page == "About":

    st.markdown(
        '<div class="main-title">ℹ️ About Notice2Action</div>',
        unsafe_allow_html=True
    )

    about_html = textwrap.dedent("""
        <div class="card">
            <h2>📘 Notice2Action</h2>

            <p>
                Notice2Action is a student-focused notice management
                platform designed to simplify academic responsibilities.
            </p>

            <h3>🎯 Our Mission</h3>

            <p>
                To help students understand college notices, identify
                important information and manage deadlines efficiently.
            </p>

            <h3>⚙️ Key Features</h3>

            <ul>
                <li>PDF notice text extraction</li>
                <li>Important date and fee detection</li>
                <li>Instruction and task identification</li>
                <li>Notice and task database management</li>
                <li>Task status tracking</li>
                <li>Notice Intelligence Assistant</li>
            </ul>

            <h3>🛠️ Technology Stack</h3>

            <ul>
                <li>Python</li>
                <li>Streamlit</li>
                <li>SQLite</li>
                <li>PyMuPDF</li>
                <li>Regular Expressions</li>
            </ul>

            <p>
                <b>Project:</b> Notice2Action
            </p>
        </div>
    """)

    st.markdown(about_html, unsafe_allow_html=True)

    st.caption("Notice2Action — From Notice to Action.")
