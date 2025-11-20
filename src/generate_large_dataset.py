"""
dataset_generator_large.py

This script generates a large synthetic dataset containing 1500 unique
customer comments. The goal is to simulate real-world noisy user feedback 
that includes multiple elements such as:
- Positive, negative, and neutral sentiment phrases
- Emojis
- HTML tags
- Contractions
- Additional descriptive phrases
- Special characters

This dataset is used to test the performance and accuracy of the
Customer Input Data Cleaning Pipeline.
"""

import pandas as pd
import random

# FUNCTION: generate_large_dataset()
def generate_large_dataset(num_comments=1500):  
    """
    Generate a large dataset with unique and noisy customer comments.
    
    Parameters:
    num_comments (int): Number of unique comments to generate (default: 1500)
    
    Returns:
    pd.DataFrame: DataFrame with generated comments
    """

    # Predefined phrase lists to build realistic text samples

    positive_phrases = [
        "I love this product", "Amazing quality", "Highly recommend", "Best purchase ever",
        "Fantastic experience", "Exceeded my expectations", "Worth every penny", 
        "Great value for money", "Super satisfied", "Will buy again", "Perfect gift",
        "Couldn't be happier", "Excellent choice", "Top-notch quality", "Very impressed",
        "Outstanding product", "Love everything about it", "Brilliant design", 
        "Works like a charm", "Awesome product", "Fantastic deal", "Great investment",
        "Absolutely brilliant", "Highly delighted", "Perfect purchase", "Super happy"
    ]
    
    negative_phrases = [
        "Worst experience", "Not worth the money", "Very disappointed", "Poor quality",
        "Didn't meet expectations", "Terrible product", "Waste of money", "Not satisfied",
        "Would not recommend", "Bad experience", "Horrible quality", "Not as advertised",
        "Defective item", "Cheap material", "Complete letdown", "Regret buying this",
        "Not impressed", "Failed after few uses", "Substandard product", "Avoid this",
        "Terrible quality", "Very poor", "Completely useless", "Total disaster"
    ]
    
    neutral_phrases = [
        "It's okay", "Average product", "Could be better", "Nothing special",
        "Decent quality", "Acceptable", "Fair enough", "Not bad", "Moderate quality",
        "Standard product", "Meets basic needs", "Just as expected", "Regular quality",
        "Ordinary product", "Neither good nor bad", "Satisfactory", "Adequate",
        "Basic functionality", "Simple design", "Does the job", "Passable",
        "Mediocre", "So-so", "Unremarkable", "Plain"
    ]

    # Emoji collections
    emojis_positive = ["😊", "😍", "❤️", "🔥", "👍", "🌟", "🎉", "🤩", "💯", "✨", "🙌"]
    emojis_negative = ["😡", "😤", "😞", "😒", "😠", "💔", "👎", "😐", "😕", "🙁", "😣"]
    emojis_neutral = ["🤔", "😌", "😶", "🙂", "😏", "🤷", "👀", "💭", "🤨"]
    
    # Random HTML tags
    html_tags = [
        "<br>", "<div>", "</div>", "<p>", "</p>", "<span>", "</span>",
        "<a href='http://example.com'>", "</a>", "<strong>", "</strong>",
        "<em>", "</em>", "<b>", "</b>", "<i>", "</i>", "<h1>", "</h1>"
    ]
    
    # Contractions for extra variability
    contractions = [
        "didn't", "don't", "can't", "won't", "shouldn't", "couldn't", "wouldn't",
        "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't",
        "I'm", "I've", "I'll", "it's", "that's", "what's", "who's", "they're",
        "he's", "she's", "we're", "you're", "let's"
    ]
    
    # Noise characters
    special_chars = ["!!!", "...", "???", "!?", "###", "@@@", "$$$", "***", "---", "~~~", "+++"]

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
        "reliable brand", "unknown brand", "trusted seller", "sketchy vendor",
        "amazing packaging", "horrible packaging", "nice presentation", "poor presentation"
    ]
    
    # Internal variables to track generated data
    comments = []  # List of final comments
    used_combinations = set() # Ensure uniqueness
    
    counter = 0 # Count of successfully generated comments
    max_attempts = num_comments * 10 # Safety limit to avoid infinite loops
    attempts = 0
    
    print(f"Generating {num_comments} unique comments...")
    
     # Main Comment Generation Loop
    while counter < num_comments and attempts < max_attempts:
        attempts += 1
        
        # Pick sentiment type for this comment
        sentiment = random.choice(['positive', 'negative', 'neutral'])
        
        # Choose base phrase + matching emoji set
        if sentiment == 'positive':
            base = random.choice(positive_phrases)
            emoji_set = emojis_positive
        elif sentiment == 'negative':
            base = random.choice(negative_phrases)
            emoji_set = emojis_negative
        else:
            base = random.choice(neutral_phrases)
            emoji_set = emojis_neutral
        
        # Build comment with various elements
        comment_parts = [base]
        
         # Randomly add contraction (50% chance)
        if random.random() > 0.5:
            comment_parts.append(random.choice(contractions))
        
        # Randomly add an extra descriptive phrase (60% chance)
        if random.random() > 0.4:
            comment_parts.append(random.choice(additional_phrases))
        
        # Add emojis (1-3)
        num_emojis = random.randint(1, 3)
        emojis = ''.join(random.choices(emoji_set, k=num_emojis))
        
        # Random HTML insert (40% chance)
        html = ""
        if random.random() > 0.6:
            html = random.choice(html_tags)
        
        # Random special characters (50% chance)
        special = ""
        if random.random() > 0.5:
            special = random.choice(special_chars)
        
        # Build the final comment text
        comment = ' '.join(comment_parts) + ' ' + emojis + ' ' + html + special
        comment = comment.strip()
        
        # Add only unique comments
        if comment not in used_combinations:
            used_combinations.add(comment)
            comments.append(comment)
            counter += 1
            
             # Print progress for every 150 comments generated
            if counter % 150 == 0:
                print(f"  Generated {counter} comments...")

    # Convert list to DataFrame and return
    df = pd.DataFrame({'Comment': comments})
    return df

# Main Execution
if __name__ == "__main__":
    print("\n" + "="*80)
    print("LARGE DATASET GENERATOR (1500+ COMMENTS)")
    print("="*80 + "\n")
    
    # Generate 1500 unique comments (1000+)
    df = generate_large_dataset(1500)
    
    # Save to CSV
    df.to_csv('data/sample_comments.csv', index=False)
    
    #Summary output
    print(f"\n Successfully generated {len(df)} unique comments")
    print(f" Saved to: data/sample_comments.csv")
    print(f" This exceeds the 1000+ requirement by {len(df) - 1000} comments")
    print("\n" + "="*80)
