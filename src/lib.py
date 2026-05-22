import datetime
import json

def write_html(all_topics):
    html_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LLM YouTube Monitor</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="container">
            <h1>LLM YouTube Monitor</h1>

            <table>
                <thead>
                    <tr>
                        <th>Channel</th>
                        <th>Video</th>
                        <th>Topics</th>
                        <th>Key Quote</th>
                        <th>Summary</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for channel_name, channel_data in all_topics.items():
        for video_id, video_info in channel_data.items():
            analysis = video_info['analysis']
            topics_list = analysis.get('topics', [])
            key_quotes_list = analysis.get('key_quotes', [])
            summary_text = analysis.get('summary', '')
            
            topics_html = ''
            for topic in topics_list:
                topics_html += f'<span class="topic-tag">{topic}</span> '
            
            quotes_html = ''
            for quote in key_quotes_list[:2]:
                quotes_html += f'<div class="key-quote">"{quote}"</div>'
            
            html_str += f"""
            <tr>
                <td><span class="channel-name">{channel_name}</span></td>
                <td class="video-title">
                    <a href="{video_info['url']}" target="_blank">{video_info['title']}</a>
                    <div class="publish-date">{video_info['published_at'][:10]}</div>
                </td>
                <td>{topics_html}</td>
                <td>{quotes_html}</td>
                <td class="summary">{summary_text}</td>
            </tr>
            """
    
    html_str += f"""
                </tbody>
            </table>

            <div class="last-updated">
                Last updated: {str(datetime.datetime.now().replace(microsecond=0))} GMM+6
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("../docs/index.html", "w") as file:
        file.write(html_str)