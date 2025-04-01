import praw
import pandas as pd
import nltk
import emoji
import re
from nltk.corpus import stopwords
from datetime import datetime
from keys import *

# Download stopwords
nltk.download('stopwords')

# Define the list of keywords for filtering relevant posts
keywords = ['depressed', 'addiction help', 'overwhelmed', 'suicidal', 'mental health', 'substance abuse', 
            'addiction', 'therapy', 'anxiety', 'depression', 'suicide prevention']



# Initialize the Reddit API client
reddit = praw.Reddit(client_id=client_id, 
                     client_secret=client_secret, 
                     user_agent=user_agent)

# Function to clean text by removing stopwords, emojis, and special characters
def clean_text(text):
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')

    # Remove special characters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)

    # Convert text to lowercase
    text = text.lower()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])

    return text

# Function to extract posts from Reddit
def extract_posts(subreddit_name, keywords, limit=1000):
    # Initialize list to store post data
    post_data = []

    # Get the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Search for posts containing the keywords
    for submission in subreddit.search(' '.join(keywords), sort='relevance', time_filter='all', limit=limit):
        try:
            # Collect relevant data
            post_id = submission.id
            timestamp = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            content = submission.title + ' ' + submission.selftext
            likes = submission.score  # karma (upvotes - downvotes)
            comments = submission.num_comments
            upvote_ratio = submission.upvote_ratio  # Proportion of upvotes to total votes

            # Clean the content text
            cleaned_content = clean_text(content)

            # Append post data
            post_data.append([post_id, timestamp, cleaned_content, likes, comments, upvote_ratio])

        except Exception as e:
            print(f"Error processing post {submission.id}: {e}")

    return post_data

# Function to save data to CSV
def save_to_csv(post_data, file_name='mental_health_posts.csv'):
    # Convert list of post data to DataFrame
    df = pd.DataFrame(post_data, columns=['Post ID', 'Timestamp', 'Content', 'Likes', 'Comments', 'Upvote Ratio'])
    
    # Save DataFrame to CSV
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

# Main function
def main():
    # Extract posts from the subreddit of your choice (e.g., r/mentalhealth, r/depression)
    subreddit_name = 'mentalhealth'  # Change to any subreddit related to mental health
    post_data = extract_posts(subreddit_name, keywords, limit=100000)  # Set limit as needed

    # Save the data to CSV
    save_to_csv(post_data)

# Run the script
if __name__ == '__main__':
    main()
