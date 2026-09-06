import streamlit as st
import pandas as pd
import os

# Set page configuration for mobile-friendliness
st.set_page_config(page_title="Student Result Portal", page_icon="🎓", layout="centered")

# CHANGE THIS: Type the exact name of your Excel file present in GitHub
EXCEL_FILE_NAME = "iaresults.xlsx" 

# --- HELPER FUNCTION TO READ EXCEL ---
@st.cache_data(ttl=60)  # Caches data for 1 hour so the app loads instantly for students
def load_data():
    if os.path.exists(EXCEL_FILE_NAME):
        try:
            # Read the Excel file
            df = pd.read_excel(EXCEL_FILE_NAME)
            # Clean column names (remove hidden spaces)
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")
            return None
    return None

# --- APP UI ---
st.title("🎓 Student Result Portal")
st.write("Welcome! Enter your Register Number below to view your test results.")

# Load the permanent data
df_results = load_data()

if df_results is None:
    st.error(f"⚠️ System Error: Could not find the file named '{EXCEL_FILE_NAME}' in the system folder.")
    st.info("Please ensure your Excel file is uploaded to GitHub and its name matches exactly.")
else:
    # Input field for students
    reg_number = st.text_input("🔑 Enter your Register Number:", placeholder="e.g., 2026001")
    
    if st.button("Check Result"):
        if reg_number.strip() == "":
            st.warning("Please enter a valid Register Number.")
        else:
            # Check if the column exists
            if "Register Number" in df_results.columns:
                # Convert column and input to string to prevent numbers vs text mismatch errors
                df_results["Register Number"] = df_results["Register Number"].astype(str)
                student_record = df_results[df_results["Register Number"] == reg_number.strip()]
                
                if not student_record.empty:
                    st.success(f"🎉 Result found!")
                    
                    # Convert the student row to a dictionary for a beautiful vertical card layout
                    record_dict = student_record.iloc[0].to_dict()
                    
                    # Display results row by row cleanly
                    st.markdown("### 📊 Your Report Card")
                    for key, val in record_dict.items():
                        st.markdown(f"**{key}:** {val}")
                else:
                    st.error("❌ Register number not found. Please verify your number and try again.")
            else:
                st.error("⚠️ System Error: The uploaded sheet is missing a 'Register Number' column.")
