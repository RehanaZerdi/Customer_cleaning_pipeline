"""
streamlit_app.py

This Streamlit web application provides an interactive interface to upload,
clean, preview, and download customer comments. It uses the same cleaning
pipeline functions used in the main Python scripts (HTML removal, emoji
removal, stopword removal, contractions expansion, etc.).

Key Features:
- Upload a CSV file containing a 'Comment' column
- Clean all comments instantly using the clean_comment() function
- View before/after results with word statistics
- Download the full cleaned dataset as CSV
- Modern UI styling using custom CSS
"""

import streamlit as st
import pandas as pd
import io
import sys
from pathlib import Path

# Add src directory to Python path so cleaning_functions can be imported
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Import the cleaning function
from cleaning_functions import clean_comment

st.set_page_config(page_title="Data Cleaning Pipeline", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
body {background: #f8f9fa;}
h1 {color: #1a237e !important; font-weight: bold;}
h2 {color: #1a237e !important;}
section[tabindex] {
    background: #ffffffcc !important;
    border-radius: 12px;
    box-shadow: 0 4px 24px rgba(60,67,110,0.08);
    padding: 2rem !important;
}
.stTable {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
}
thead th {
    background: #f0f3ff !important;
    font-size: 0.95rem !important;
}
tbody tr:hover {
    background: #f5f7ff !important;
}
.stDownloadButton>button {
    background-color: #3f51b5 !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 6px !important;
    padding: 0.6em 1.6em !important;
    border: none !important;
}
.stDownloadButton>button:hover {
    background-color: #283593 !important;
}
.metric-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# App Title and Description
st.title(" Customer Data Cleaning Pipeline")
st.markdown("Upload CSV, clean all comments, preview everything, download results.")

# Sidebar Information
st.sidebar.header("About")
st.sidebar.info(
    "Upload a CSV file with customer feedback. The app will clean ALL records "
    "(remove emojis, HTML, contractions, special chars, stopwords), show full before/after comparison, "
    "and let you download the complete cleaned dataset."
)

st.sidebar.header("Features")
st.sidebar.markdown("""
- Upload CSV (with 'Comment' column)
- Clean ALL comments instantly
- View before/after for every record
- Download full cleaned dataset
- Performance metrics & statistics
""")

# File Upload Section
uploaded_file = st.file_uploader("Upload your CSV file *", type="csv")

# Main Processing Logic
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8", encoding_errors="ignore")

        
        # Check if the required column exists
        if 'Comment' not in df.columns:
            st.error("❌ Your file must have a column named 'Comment'.")
        else:
            st.success(f"✅ File uploaded! {len(df)} comments found.")
            
            # Clean all comments with loading spinner
            with st.spinner("Processing all comments..."):
                results = df['Comment'].apply(lambda x: clean_comment(x))

                # Extract cleaned data and word counts
                df['Cleaned_Comment'] = results.apply(lambda x: x[0])
                df['Words_Before'] = results.apply(lambda x: x[1])
                df['Words_After'] = results.apply(lambda x: x[2])
                df['Words_Removed'] = df['Words_Before'] - df['Words_After']
            
            # Display Metrics Section
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Comments", len(df))
            with col2:
                st.metric("Avg Words Before", f"{df['Words_Before'].mean():.1f}")
            with col3:
                st.metric("Avg Words After", f"{df['Words_After'].mean():.1f}")
            with col4:
                st.metric("Total Removed", int(df['Words_Removed'].sum()))
            
            # Display Before/After Table
            st.subheader(f"All {len(df)} Comments - Before & After")
            
            # Prepare table for display
            display_df = df[['Comment', 'Cleaned_Comment', 'Words_Before', 'Words_After', 'Words_Removed']].copy()
            display_df.columns = ['Original Comment', 'Cleaned Comment', 'Before', 'After', 'Removed']
            
            # Use Streamlit's data editor for scrollable, interactive table
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # Download Cleaned Results
            st.subheader("Download Full Results")
            buf = io.StringIO()
            df.to_csv(buf, index=False)
            st.download_button(
                label="📥 Download Cleaned Data (CSV)",
                data=buf.getvalue(),
                file_name="cleaned_comments_full.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    # Show sample format if file not yet uploaded
    st.info("👆 Upload a CSV file to begin. Example format:")
    sample = pd.DataFrame({
        "Comment": [
            "I love this! 😍 <br> Amazing",
            "Terrible product!!! 😡",
            "It's okay... wasn't expecting much"
        ]
    })
    st.table(sample)

# Footer Section
st.markdown("---")
st.caption("Fast, professional text cleaning. Powered by Streamlit & Python.")
