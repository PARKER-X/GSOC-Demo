Mental Health and Suicide Risk Analysis using Reddit Data!!
Overview
This project collects and analyzes posts from Reddit related to mental health and suicide risk, with the goal of identifying crisis language, sentiment, and geographic trends. The analysis provides insights into discussions about mental health and risk indicators. Data is fetched from specific subreddits and processed using natural language processing (NLP) and sentiment analysis.

Key Features:
Extracts posts related to mental health and crisis keywords from Reddit.

Cleans the extracted text (removes stopwords, emojis, special characters).

Classifies posts based on sentiment (positive, neutral, negative) using VADER sentiment analysis.

Detects posts with high risk or crisis-related language (e.g., suicidal thoughts, depression).

Geocodes extracted locations from the posts and visualizes global trends on a heatmap.

Setup Instructions
Prerequisites
Python 3.11 or higher

Install the required dependencies by running:

bash
Copy
pip install -r requirements.txt
Dependencies
pandas - For data manipulation and analysis.

nltk - For natural language processing, including sentiment analysis and stopword filtering.

emoji - To handle emoji removal in the text.

re - Regular expressions for text cleaning.

praw - Python Reddit API Wrapper, used to connect to Reddit and extract posts.

folium - For generating heatmaps to visualize geospatial data.

geopy - For geocoding extracted locations (convert place names to latitudes/longitudes).

spacy - For Named Entity Recognition (NER) to extract location data from posts.

matplotlib & seaborn - For plotting and visualizing sentiment and risk level distributions.

File Setup
keys.py: This file contains your Reddit API credentials (client_id, client_secret, user_agent).

Example:

python
Copy
client_id = "your_client_id"
client_secret = "your_client_secret"
user_agent = "your_user_agent"
Data Files:

mental_health_posts.csv: Stores the raw Reddit post data.

classified_mental_health_posts.csv: Contains classified posts with sentiment and risk levels.

reddit_mental_health_suicide_large_data.csv: Contains geocoded post data with extracted locations.

mental_health_suicide_large_heatmap.html: Displays a heatmap visualization of global trends in mental health discussions.

How to Use
Step 1: Extract Reddit Posts
Run the script to collect posts related to mental health and suicide from the subreddits specified in the code. This will store raw data in mental_health_posts.csv.

bash
Copy
python reddit.py
You can customize the subreddit_name and keywords in the code to collect posts from different subreddits or search for different keywords.

Step 2: Classify Sentiment and Risk
After collecting the posts, use the following script to classify the sentiment and detect high-risk language (e.g., suicidal thoughts or depression). This script outputs classified_mental_health_posts.csv with sentiment labels and risk levels (e.g., "Low Concern", "Moderate Concern", "High Risk").

bash
Copy
python sentiment.py
Step 3: Geocode Locations and Generate Heatmap
To visualize the geographic trends of mental health and suicide-related discussions, run the script to extract locations from the posts and generate a heatmap of geolocated posts. This will produce a file mental_health_suicide_large_heatmap.html that you can open in any browser.

bash
Copy
python geoo.py
This step uses spaCy to extract locations, geocodes them using geopy, and plots the heatmap using folium.

Output
mental_health_posts (CSV): Raw Reddit data collected from the chosen subreddits with information like post content, timestamp, upvotes, comments, etc.

classified_mental_health_posts (CSV): The posts are classified based on sentiment and risk level.

reddit_mental_health_suicide_large_data(CSV): Contains posts with locations and their corresponding latitudes and longitudes.

mental_health_suicide_large_heatmap (HTML): A geographical heatmap displaying the concentration of posts related to mental health and suicide, showing global trends.
