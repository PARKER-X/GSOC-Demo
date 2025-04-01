import praw
import pandas as pd
import spacy
from geopy.geocoders import Nominatim
from collections import Counter
import folium
from folium.plugins import HeatMap
import time
from keys import *

# Step 1: Set up Reddit API credentials (replace with your own)
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

# Step 2: Load spaCy for NLP-based place recognition
nlp = spacy.load("en_core_web_sm")

# Step 3: Initialize geocoder with timeout
geolocator = Nominatim(user_agent="mental_health_suicide_large_heatmap", timeout=10)

# Step 4: Function to extract multiple locations using NLP
def extract_locations(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    return locations if locations else [None]

# Step 5: Function to geocode a location with retry logic
def geocode_location(location):
    if not location:
        return None, None
    for attempt in range(3):  # Retry up to 3 times
        try:
            geo = geolocator.geocode(location)
            if geo:
                return geo.latitude, geo.longitude
            return None, None
        except:
            time.sleep(1)  # Wait before retrying
    return None, None

# Step 6: Retrieve large dataset from multiple subreddits and sources
subreddits = "mentalhealth+suicidewatch+depression+anxiety"  # Expand as needed
keywords = ["suicide", "mental health", "depression", "help", "crisis", "anxiety"]
posts = []

for subreddit_name in subreddits.split("+"):
    subreddit = reddit.subreddit(subreddit_name)
    for method in [subreddit.new, subreddit.hot, subreddit.top]:  # Multiple streams
        try:
            for submission in method(limit=1000):  # Max per stream
                text = (submission.title + " " + submission.selftext).lower()
                if any(keyword in text for keyword in keywords):
                    posts.append({
                        "title": submission.title,
                        "selftext": submission.selftext,
                        "subreddit": subreddit_name,
                        "geotag": None  # Reddit doesn’t provide geotags
                    })
        except Exception as e:
            print(f"Error fetching from {subreddit_name}: {e}")
        time.sleep(2)  # Respect rate limits

# Step 7: Create DataFrame and extract locations
df = pd.DataFrame(posts)
df["extracted_locations"] = (df["title"] + " " + df["selftext"]).apply(extract_locations)

# Explode to handle multiple locations per post
df_exploded = df.explode("extracted_locations").rename(columns={"extracted_locations": "extracted_location"})
df_exploded["lat"], df_exploded["lon"] = zip(*df_exploded["extracted_location"].apply(geocode_location))

# Step 8: Drop rows where geocoding failed
df_clean = df_exploded.dropna(subset=["lat", "lon"])

# Step 9: Display top 5 locations
location_counts = Counter(df_clean["extracted_location"].fillna("Unknown"))
top_5_locations = location_counts.most_common(5)
print("Top 5 locations with the highest mental health/suicide discussions:")
for loc, count in top_5_locations:
    print(f"{loc}: {count} posts")

# Step 10: Generate Folium heatmap
m = folium.Map(location=[0, 0], zoom_start=2)  # Global view
heat_data = [[row["lat"], row["lon"]] for _, row in df_clean.iterrows()]
HeatMap(heat_data, radius=15, blur=20).add_to(m)  # Adjusted for visibility
m.save("mental_health_suicide_large_heatmap.html")
print("Heatmap saved as 'mental_health_suicide_large_heatmap.html'. Open it in a browser to view.")

# Step 11: Save data to CSV
df_clean.to_csv("reddit_mental_health_suicide_large_data.csv", index=False)
print(f"Saved {len(df_clean)} geocoded posts to 'reddit_mental_health_suicide_large_data.csv'.")
print("\nSample Geocoded Data:")
print(df_clean[["title", "extracted_location", "lat", "lon"]].head())