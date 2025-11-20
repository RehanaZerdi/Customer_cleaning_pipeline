📄 Customer Data Cleaning Pipeline

A fully automated text-cleaning system designed to preprocess raw customer feedback at scale.
This project removes noise such as emojis, HTML tags, repeated characters, special symbols, contractions, and unnecessary stopwords — while correctly preserving negation meaning (e.g., “didn’t” → “did not”).

The project includes:

✔️ A complete Python cleaning pipeline
✔️ A dataset generator for large-scale testing
✔️ A Streamlit web application for uploading & cleaning CSV files
✔️ Before/after comparison for all comments
✔️ Downloadable cleaned dataset

📌 Features

Clean customer comments in bulk (1000+ comments supported)

Remove emojis, HTML tags (but keep text), noise & repeated characters

Expand contractions correctly (didn’t → did not, we’re → we are)

Intelligent stopword removal while preserving negation words

Before/After comparison table for every comment

Summary metrics (word count reduction, total words removed, etc.)

Download the cleaned dataset as CSV

Dataset generator for creating synthetic comments

🧠 Why This Pipeline?

Raw customer comments typically contain noise that disrupts NLP workflows:

Emojis, tags, special characters

Broken grammar, contractions, and repeated letters

Inconsistent casing

Words inside HTML tags

Unnecessary filler text

Manual cleaning is time-consuming and inconsistent.
This pipeline ensures clean, reliable, NLP-ready text with zero manual effort.

🚀 Project Structure
Customer_cleaning_pipeline/
│
├── app/
│   └── streamlit_app.py           # User-facing web interface
│
├── src/
│   ├── cleaning_functions.py      # Core cleaning pipeline logic
│   ├── main_pipeline.py           # CLI cleaning script
│   ├── data_generator.py          # Creates sample dataset
│   └── generate_large_dataset.py  # Generates 1500+ synthetic comments
│
├── data/
│   ├── sample_comments.csv        # Input dataset example
│   └── cleaned_output.csv         # Output (created after cleaning)
│
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # Project documentation

🧩 Tech Stack

Python 3.10+

NLTK (tokenization, stopwords)

contractions (expanding contractions)

emoji (emoji removal)

Streamlit (web UI)

Pandas

⚙️ How to Run the Project
1️⃣ Clone the repository
git clone https://github.com/RehanaZerdi/Customer_cleaning_pipeline.git
cd Customer_cleaning_pipeline

2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run app/streamlit_app.py

5️⃣ Run the cleaning pipeline (CLI)
python src/main_pipeline.py

🧼 Cleaning Steps (Behind the Scenes)

The comment cleaning pipeline performs:

Expand contractions

Remove HTML tags (keep text inside)

Remove emojis

Normalize repeated characters

Convert to lowercase

Strip special characters

Stopword removal with negation protection

Final whitespace cleanup

📊 Output Examples

Before:

Didn't meet expectations weren't 😡😡 <div>Gooood quality though</div>


After:

did not meet expectations were not goood quality

📥 Web App Screenshot

You can add your screenshot here later:

![Streamlit UI](path_to_screenshot)

📎 Download Options

Download fully cleaned CSV

View before/after results

Review statistics summary

📜 License

This project is published under the MIT License.

🙌 Acknowledgements

Special thanks to the guidance provided during the internship project at Newton AI Technologies.