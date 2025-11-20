import nltk
import os

# Ensure required NLTK resources are installed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

import re
import emoji
import html
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import contractions

# -------------------------------------------------------
# LOAD STOPWORDS AND PROTECT IMPORTANT NEGATION WORDS
# -------------------------------------------------------
stop_words = set(stopwords.words("english"))

# Negation words that MUST be preserved (never removed)
negation_words = {
    "not", "no", "never", "none",
    "did", "did not",
    "was", "was not",
    "were", "were not",
    "cannot",
    "cant", "can't",
    "should not", "shouldn't",
    "could not", "couldn't",
    "would not", "wouldn't"
}

# Remove negation words from stopwords so they are preserved
stop_words = stop_words - negation_words

# -------------------------------------------------------
# REMOVE HTML TAGS (BUT KEEP TEXT INSIDE TAGS)
# -------------------------------------------------------
def remove_html_tags(text):
    """Remove HTML tags but keep the text inside them."""
    text = html.unescape(text)
    return re.sub(r"<.*?>", " ", text)

# -------------------------------------------------------
# REMOVE EMOJIS
# -------------------------------------------------------
def remove_emojis(text):
    """Remove emojis from text safely."""
    return emoji.replace_emoji(text, replace=" ")

# -------------------------------------------------------
# EXPAND CONTRACTIONS SAFELY
# -------------------------------------------------------
def expand_contractions_text(text):
    """Expand contractions such as didn't → did not."""
    expanded = contractions.fix(text)
    
    # contractions library does: "can not" → we correct it:
    expanded = expanded.replace("can not", "cannot")
    
    return expanded

# -------------------------------------------------------
# NORMALIZE REPEATED CHARACTERS
# -------------------------------------------------------
def normalize_repeated_characters(text):
    """Normalize repeated characters: goooood → good."""
    return re.sub(r"(.)\1{2,}", r"\1\1", text)

# -------------------------------------------------------
# REMOVE SYMBOLS BUT KEEP WORDS
# -------------------------------------------------------
def remove_symbols(text):
    """Remove punctuation and symbols but keep readable text."""
    return re.sub(r"[^a-zA-Z\s]", " ", text)

# -------------------------------------------------------
# LOWERCASE TEXT
# -------------------------------------------------------
def lowercase_text(text):
    return text.lower()

# -------------------------------------------------------
# REMOVE STOPWORDS (NEGATION-SAFE)
# -------------------------------------------------------
def remove_stopwords(text):
    """Remove standard stopwords but keep negation words."""
    words = word_tokenize(text)
    cleaned = []
    
    for w in words:
        if w in negation_words:
            cleaned.append(w)
        elif w not in stop_words:
            cleaned.append(w)
    
    return " ".join(cleaned)

# -------------------------------------------------------
# COUNT WORDS
# -------------------------------------------------------
def count_words(text):
    return len(text.split())

# -------------------------------------------------------
# MASTER CLEANING PIPELINE
# -------------------------------------------------------
def clean_comment(text):
    """
    Balanced cleaning pipeline:
     - Expand contractions
     - Remove HTML tags but keep content
     - Remove emojis
     - Normalize repeated characters
     - Lowercase
     - Remove symbols
     - Remove stopwords (negation-safe)
    """
    words_before = count_words(text)

    cleaned = expand_contractions_text(text)
    cleaned = remove_html_tags(cleaned)
    cleaned = remove_emojis(cleaned)
    cleaned = normalize_repeated_characters(cleaned)
    cleaned = lowercase_text(cleaned)
    cleaned = remove_symbols(cleaned)
    cleaned = remove_stopwords(cleaned)

    # remove extra spaces
    cleaned = " ".join(cleaned.split())

    words_after = count_words(cleaned)

    return cleaned, words_before, words_after

# -------------------------------------------------------
# SUCCESS FLAG
# -------------------------------------------------------
def flag_cleaning_success(original_text, cleaned_text):
    return "Success" if cleaned_text.strip() else "Failed"

# -------------------------------------------------------
# TEST (OPTIONAL)
# -------------------------------------------------------
if __name__ == "__main__":
    test_comment = "Didn't meet expectations weren't 😡😡 <div>Gooood quality though</div>"
    print("Original:", test_comment)
    cleaned, b, a = clean_comment(test_comment)
    print("Cleaned:", cleaned)
    print("Words:", b, "->", a)
