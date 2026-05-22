# yt-watcher

## Problem Statement

Write a python script to analyse videos of select few AI channels and summarise their content to display on a live webpage

### Key challenges addressed:**
- How to automatically extract what creators *actually say* (not just titles)
- How to categorize content by topics across multiple channels
- How to keep information current as new videos are published
- How to do this without expensive API subscriptions

### Data Collection
 
Data is collected from the following channels: 

- Andrej Karpathy 
- Dwarkesh Patel 
- Wes Roth 
- AI Explained 
- Krish Naik
- Sebastian Raschka

-----------------------------------------------------------------------------------------


## Methodology

- uses YouTube API for calling information on select few channels
- uses yt-transcript API for obtaining transcripts from videos, merges all of the captions to get raw transcripts
- passes the transcript to OpenAI API for analysis and obtaining a summary
- receives the summary and writes an HTML file with the information 
- HTML page displayed on GitHub pages

--- 

