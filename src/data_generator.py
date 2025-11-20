"""
dataset_generator.py

This script generates a small synthetic dataset of 200 unique customer comments.
The purpose is to create noisy, realistic user feedback containing:
- Positive / negative / neutral text
- Emojis
- HTML tags
- Contractions
- Additional descriptive phrases
- Special characters

The generated dataset is saved into:
    data/sample_comments.csv

This file is useful for testing and validating the cleaning pipeline.
"""

import pandas as pd
import random


# Predefined lists containing various types of text fragments to simulate realistic customer comments.

positive_phrases = [
    "I love this product", "Amazing quality", "Highly recommend", "Best purchase ever",
    "Fantastic experience", "Exceeded my expectations", "Worth every penny", 
    "Great value for money", "Super satisfied", "Will buy again", "Perfect gift",
    "Couldn't be happier", "Excellent choice", "Top-notch quality", "Very impressed",
    "Outstanding product", "Love everything about it", "Brilliant design", 
    "Works like a charm", "Awesome product"
]

negative_phrases = [
    "Worst experience", "Not worth the money", "Very disappointed", "Poor quality",
    "Didn't meet expectations", "Terrible product", "Waste of money", "Not satisfied",
    "Would not recommend", "Bad experience", "Horrible quality", "Not as advertised",
    "Defective item", "Cheap material", "Complete letdown", "Regret buying this",
    "Not impressed", "Failed after few uses", "Substandard product", "Avoid this"
]

neutral_phrases = [
    "It's okay", "Average product", "Could be better", "Nothing special",
    "Decent quality", "Acceptable", "Fair enough", "Not bad", "Moderate quality",
    "Standard product", "Meets basic needs", "Just as expected", "Regular quality",
    "Ordinary product", "Neither good nor bad", "Satisfactory", "Adequate",
    "Basic functionality", "Simple design", "Does the job"
]

# Emojis based on sentiment
emojis_positive = ["😊", "😍", "❤️", "🔥", "👍", "🌟", "🎉", "🤩", "💯", "✨", "🙌", "👌", "🎁", "💖", "⭐"]
emojis_negative = ["😡", "😤", "😞", "😒", "😠", "💔", "👎", "😐", "😕", "🙁", "😣", "😖", "😢", "😩", "🤬"]
emojis_neutral = ["🤔", "😌", "😶", "🙂", "😏", "🤷", "👀", "💭", "🤨", "😑"]

# HTML tags to randomly include
html_tags = [
    "<br>", "<div>", "</div>", "<p>", "</p>", "<span>", "</span>",
    "<a href='http://example.com'>", "</a>", "<strong>", "</strong>",
    "<em>", "</em>", "<b>", "</b>", "<i>", "</i>"
]

# Contractions to insert randomly
contractions = [
    "didn't", "don't", "can't", "won't", "shouldn't", "couldn't", "wouldn't",
    "isn't", "aren't", "was n't", "weren't", "haven't", "hasn't", "hadn't",
    "I'm", "I've", "I'll", "it's", "that's", "what's", "who's", "they're"
]

# Special characters for realism
special_chars = ["!!!", "...", "???", "!?", "###", "@@@", "$$$", "***", "---", "~~~"]

# Additional descriptive phrases
additional_phrases = [
    "but needs improvement", "with fast delivery", "however packaging was poor",
    "and great customer service", "but expensive", "with some issues",
    "arrived on time", "took too long to ship", "works perfectly",
    "has some defects", "better than similar products", "not as good as others",
    "would recommend with caution", "came damaged", "functions well",
    "broke after few days", "durable and strong", "flimsy construction",
    "loved by my family", "no one liked it", "good for the price",
    "overpriced for quality", "sleek design", "ugly appearance",
    "easy to use", "complicated setup", "user-friendly", "confusing instructions",
    "reliable brand", "unknown brand", "trusted seller", "sketchy vendor"
]

# Dataset generation logic

comments = [] # Final list of generated comments
used_combinations = set() # Keeps track of unique comments to avoid duplicates

# Continue until 200 unique comments are generated
while len(comments) < 200:
    
    # Randomly choose a sentiment type
    sentiment = random.choice(['positive', 'negative', 'neutral'])
    
    # Select base phrase + corresponding emoji pool
    if sentiment == 'positive':
        base = random.choice(positive_phrases)
        emoji_set = emojis_positive
    elif sentiment == 'negative':
        base = random.choice(negative_phrases)
        emoji_set = emojis_negative
    else:
        base = random.choice(neutral_phrases)
        emoji_set = emojis_neutral
    
    # Start building the comment
    comment_parts = [base]
    
    # Randomly add a contraction (50% chance)
    if random.random() > 0.5:
        comment_parts.append(random.choice(contractions))
    
    # Randomly add additional phrase (60% chance)
    if random.random() > 0.4:
        comment_parts.append(random.choice(additional_phrases))
    
    # Add emojis (1-3)
    num_emojis = random.randint(1, 3)
    emojis = ''.join(random.choices(emoji_set, k=num_emojis))
    
    # Randomly insert an HTML tag (40% chance)
    html = ""
    if random.random() > 0.6:
        html = random.choice(html_tags)
    
    # Randomly add special characters (50% chance)
    special = ""
    if random.random() > 0.5:
        special = random.choice(special_chars)
    
     # Construct final comment string
    comment = ' '.join(comment_parts) + ' ' + emojis + ' ' + html + special
    comment = comment.strip()
    
    # Ensure comment is unique before adding
    if comment not in used_combinations:
        used_combinations.add(comment)
        comments.append(comment)


# Create DataFrame and save to CSV

df = pd.DataFrame({'Comment': comments})

# Save to CSV
df.to_csv('data/sample_comments.csv', index=False)

# Final console output for verification

print("✓ Sample dataset with 200 unique comments created successfully!")
print("✓ File saved as: data/sample_comments.csv")
print(f"✓ Total comments: {len(df)}")
print(f"\nFirst 5 comments preview:")
print(df.head())
