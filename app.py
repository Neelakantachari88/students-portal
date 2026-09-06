import streamlit as st
import pandas as pd
import os

# Set page configuration for mobile-friendliness
st.set_page_config(page_title="Student Result Portal", page_icon="🎓", layout="centered")

DATA_FILE = "student_results.csv"

# --- HELPER FUNCTIONS ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return None

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- APP UI ---
st.title("🎓 GPT KUDLIGI - 1ST IA RESULTS")
st.write("Welcome! Enter your REGISTER NUMBER IN CAPITALS below to view IA-1  performance.")

# Create Sidebar for Admin/Teacher Upload
with st.sidebar:
    st.header("⚙️ Admin Panel")
    admin_password = st.text_input("Enter Admin Password", type="password")
    
    # Change "admin123" to your preferred secure password
    if admin_password == "admin123":
        st.success("Authenticated!")
        uploaded_file = st.file_uploader("Upload Student Results (Excel or CSV)", type=["xlsx", "csv"])
        
        if uploaded_file is not None:
            try:
                # Read Excel or CSV based on file type
                if uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)
                
                # Clean column names (remove hidden spaces)
                df.columns = df.columns.str.strip()
                
                # Save data locally
                save_data(df)
                st.sidebar.success("✅ Results updated successfully!")
            except Exception as e:
                st.sidebar.error(f"Error processing file: {e}")
    elif admin_password:
        st.error("Incorrect Password")

# --- STUDENT PORTAL ---
df_results = load_data()

if df_results is None:
    st.info("📢 The portal hasn't been updated with latest results yet. Please check back later.")
else:
    # Input field for students
    reg_number = st.text_input("🔑 Enter your Register Number:", placeholder="e.g., 2026001")
    
    if st.button("Check Result"):
        if reg_number.strip() == "":
            st.warning("Please enter a valid Register Number.")
        else:
            # Match the input. We convert column and input to string to avoid mismatch errors
            # Assumes your Excel column is named exactly "Register Number"
            if "Register Number" in df_results.columns:
                df_results["Register Number"] = df_results["Register Number"].astype(str)
                student_record = df_results[df_results["Register Number"] == reg_number.strip()]
                
                if not student_record.empty:
                    st.success(f"🎉 Result found for Register Number: {reg_number}")
                    
                    # Convert the row into a clean, easy-to-read vertical format
                    record_dict = student_record.iloc[0].to_dict()
                    
                    # Display results beautifully
                    for key, val in record_dict.items():
                        st.markdown(f"**{key}:** {val}")
                else:
                    st.error("❌ Register number not found. Please check and try again.")
            else:
                st.error("⚠️ System Error: The uploaded sheet is missing a 'Register Number' column.")
