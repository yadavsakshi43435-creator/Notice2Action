import streamlit as st
import json

from pdf_extractor import extract_text_from_pdf
from notice_analyzer import analyze_notice
from database import (
    initialize_db,
    save_notice,
    get_all_notices,
    update_notice_status
)

# Page configuration
st.set_page_config(
    page_title="Notice2Action",
    page_icon="📢",
    layout="wide"
)

# Initialize database
initialize_db()

# Header
st.title("📢 Notice2Action")
st.subheader("Turn College Notices into Student Actions")

st.write(
    "Upload your college notice and never miss "
    "an important deadline again."
)

st.divider()

# Sidebar
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "My Dashboard"]
)

# HOME PAGE
if menu == "Home":

    st.header("📄 Upload College Notice")

    uploaded_file = st.file_uploader(
        "Choose a PDF notice",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button("Analyze Notice"):

            with st.spinner("Analyzing your notice..."):

                try:
                    pdf_bytes = uploaded_file.getvalue()

                    extracted_text = extract_text_from_pdf(
                        pdf_bytes
                    )

                    if not extracted_text.strip():
                        st.warning(
                            "No readable text found in this PDF. "
                            "Scanned PDFs are not supported yet."
                        )

                    else:
                        analysis = analyze_notice(
                            extracted_text
                        )

                        st.session_state["analysis"] = analysis
                        st.session_state["extracted_text"] = extracted_text
                        st.session_state["filename"] = uploaded_file.name

                except Exception as e:
                    st.error(f"Error: {e}")

    # Show analysis
    if "analysis" in st.session_state:

        analysis = st.session_state["analysis"]

        st.divider()
        st.header("🔍 Notice Analysis")

        st.subheader("📅 Important Dates")

        if analysis["dates"]:
            for date in analysis["dates"]:
                st.write("•", date)
        else:
            st.info("No dates detected.")

        st.subheader("💰 Fees and Payments")

        if analysis["fees"]:
            for fee in analysis["fees"]:
                st.write("•", fee)
        else:
            st.info("No fee information detected.")

        st.subheader("📌 Important Instructions")

        if analysis["instructions"]:
            for instruction in analysis["instructions"]:
                st.write("•", instruction)
        else:
            st.info("No instructions detected.")

        with st.expander("View Extracted PDF Text"):
            st.text(st.session_state["extracted_text"])

        title = st.text_input(
            "Notice Title",
            value=st.session_state["filename"]
        )

        if st.button("💾 Save Notice"):

            if title.strip():

                save_notice(
                    title,
                    st.session_state["filename"],
                    st.session_state["extracted_text"],
                    analysis
                )

                st.success("Notice saved successfully!")

                del st.session_state["analysis"]
                del st.session_state["extracted_text"]
                del st.session_state["filename"]

            else:
                st.warning("Please enter a notice title.")


# DASHBOARD PAGE
elif menu == "My Dashboard":

    st.header("📊 Student Dashboard")

    notices = get_all_notices()

    total = len(notices)

    pending = sum(
        1 for n in notices if n["status"] == "Pending"
    )

    completed = sum(
        1 for n in notices if n["status"] == "Completed"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Notices", total)
    col2.metric("Pending", pending)
    col3.metric("Completed", completed)

    st.divider()

    st.subheader("📋 Saved Notices")

    if notices:

        for notice in notices:

            with st.expander(notice["title"]):

                st.write("File:", notice["filename"])
                st.write("Status:", notice["status"])

                dates = json.loads(notice["dates"])
                fees = json.loads(notice["fees"])
                instructions = json.loads(
                    notice["instructions"]
                )

                st.write("**Important Dates:**")
                st.write(dates if dates else "None")

                st.write("**Fees:**")
                st.write(fees if fees else "None")

                st.write("**Instructions:**")
                st.write(
                    instructions if instructions else "None"
                )

                status = st.selectbox(
                    "Update Status",
                    ["Pending", "Completed"],
                    index=(
                        0 if notice["status"] == "Pending" else 1
                    ),
                    key=f"status_{notice['id']}"
                )

                if st.button(
                    "Update",
                    key=f"update_{notice['id']}"
                ):

                    update_notice_status(
                        notice["id"],
                        status
                    )

                    st.success("Status updated!")
                    st.rerun()

    else:
        st.info(
            "No notices saved yet. Upload your first notice!"
        )