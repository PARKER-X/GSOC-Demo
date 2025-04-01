import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.pyplot as plt

# Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('stopwords')

# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Sample list of crisis-related terms for detecting high-risk language (can be expanded)
crisis_terms = ['suicidal', 'die', 'end it', 'kill myself', 'not worth', 'depressed', 'overdose', 'hopeless']

# Function to clean the text
def clean_text(text):
    # Remove special characters and convert text to lowercase
    text = re.sub(r'[^A-Za-z0-9\s]', '', text.lower())
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Sentiment and Risk Classification
def classify_sentiment_and_risk(df):
    post_data = []
    
    # Process each post in the DataFrame
    for _, post in df.iterrows():
        post_id = post['Post ID']
        timestamp = post['Timestamp']
        content = post['Content']
        likes = post['Likes']
        comments = post['Comments']
        upvote_ratio = post['Upvote Ratio']

        # Clean the content
        cleaned_content = clean_text(content)
        
        # Sentiment Classification (using VADER for sentiment analysis)
        sentiment_score = sia.polarity_scores(cleaned_content)
        sentiment = 'Neutral'
        if sentiment_score['compound'] >= 0.05:
            sentiment = 'Positive'
        elif sentiment_score['compound'] <= -0.05:
            sentiment = 'Negative'
        
        # Detect Risk Level (Moderate and High Risk detection)
        risk_level = 'Low Concern'
        for term in crisis_terms:
            if term in cleaned_content:
                risk_level = 'High Risk'
                break
        if 'help' in cleaned_content or 'lost' in cleaned_content or 'struggle' in cleaned_content:
            risk_level = 'Moderate Concern'

        # Append the classified data
        post_data.append([post_id, timestamp, sentiment, risk_level, likes, comments, upvote_ratio])

    # Create DataFrame with the classified data
    classified_df = pd.DataFrame(post_data, columns=['Post ID', 'Timestamp', 'Sentiment', 'Risk Level', 'Likes', 'Comments', 'Upvote Ratio'])
    return classified_df

# Load the dataset (make sure to replace this with your actual file path)
df = pd.read_csv('mental_health_posts.csv')

# Classify the posts
classified_df = classify_sentiment_and_risk(df)

# Show the classified posts
print(classified_df)

# Save the classified data to a new CSV file
classified_df.to_csv('classified_mental_health_posts.csv', index=False)
print("Classification completed and saved to 'classified_mental_health_posts.csv'")

# Plot the distribution of Sentiment
plt.figure(figsize=(10, 6))
sns.countplot(data=classified_df, x='Sentiment', palette='Set1')
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Number of Posts')

# Save the Sentiment Distribution Plot as an image
plt.savefig('sentiment_distribution.png')
print("Sentiment Distribution plot saved as 'sentiment_distribution.png'")

# Plot the distribution of Risk Level
plt.figure(figsize=(10, 6))
sns.countplot(data=classified_df, x='Risk Level', palette='Set2')
plt.title('Risk Level Distribution')
plt.xlabel('Risk Level')
plt.ylabel('Number of Posts')

# Save the Risk Level Distribution Plot as an image
plt.savefig('risk_level_distribution.png')
print("Risk Level Distribution plot saved as 'risk_level_distribution.png'")

# Show the plots
plt.show()
