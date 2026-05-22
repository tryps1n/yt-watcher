from openai import OpenAI
import json
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import time
import lib
from google.genai.errors import ClientError

GROQ_API_KEY = "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"
YT_API_KEY = "AIzaSyAcnJUalBErwLO8gM-yxF0gfnCn6SInNjA"

CHANNEL_IDS = {
    "AndrejKarpathy" : "UCXUPKJO5MZQN11PqgIvyuvQ",
    "DwarkeshPatel" : "UCXl4i9dYBrFOabk0xGmbkRA",
    "WesRoth" : "UCqcbQf6yw5KzRoDDcZ_wBSw",
    "AIExplained" : "UCNJ1Ymd5yFuUPtn21xtRbbw",
    "KrishNaik" : "UCNU_lfiiWBdtULKOw6X0Dig",
    "SebastianRaschka" : "UC_CzsS7UTjcxJ-xXp1ftxtA"
}

youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

ytt_api = YouTubeTranscriptApi()

def get_uploads_playlist_id(channel_id):
    request = youtube.channels().list(
        part='contentDetails', 
        id=channel_id
    ) 
    response = request.execute()
    uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    return uploads_id

def get_recent_videos(uploads_playlist_id, limit=3):
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=limit
    )
    response = request.execute()
    
    videos = []
    for item in response['items']:
        videos.append({
            'video_id': item['contentDetails']['videoId'],
            'title': item['snippet']['title'],
            'published_at': item['snippet']['publishedAt'],
            'url': f"https://youtube.com/watch?v={item['contentDetails']['videoId']}"
        })
    return videos

def get_video_topic(channel_id, max_retries=3):
    topics = {}
    uploads_id = get_uploads_playlist_id(channel_id)
    recent_videos = get_recent_videos(uploads_id)

    for video in recent_videos:
        transcript = ytt_api.fetch(video['video_id'])
        raw_text = ""
        for snippet in transcript:
            raw_text += snippet.text

        prompt = f"""
        Analyze this YouTube video titled "{video['title']}".
        
        Extract:
        1. Topics: 2-4 main LLM/AI topics covered
        2. Key quotes: 2 actual quotes from the speaker
        3. Summary: One sentence summary
        
        Return ONLY valid JSON: {{"topics": ["t1", "t2"], "key_quotes": ["q1", "q2"], "summary": "..."}}
        
        Transcript: {raw_text[:200]}
        """
        
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        topics[video['video_id']] = {
            'title': video['title'],
            'url': video['url'],
            'published_at': video['published_at'],
            'analysis': json.loads(response.choices[0].message.content)
        }
        
        time.sleep(3)
    
    return topics

all_topics = {}

for channel_name, channel_id in CHANNEL_IDS.items():
    all_topics[channel_name] = get_video_topic(channel_id)

lib.write_html(all_topics)

with open('docs/videos_data.json', 'w') as f:
    json.dump(all_topics, f, indent=2)