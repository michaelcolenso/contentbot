import requests
from bs4 import BeautifulSoup
from moviepy.editor import TextClip, ImageClip, concatenate_videoclips
from PIL import Image
import yaml

# Load configuration
def load_config():
    with open("config.yaml", 'r') as file:
        return yaml.safe_load(file)

# Fetch article content
def fetch_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n".join([para.get_text() for para in paragraphs])
        return content
    else:
        raise Exception(f"Failed to fetch content from {url}")

# Generate video from content
def generate_video(content, output_path):
    clips = []
    # Split content into lines and create text clips
    for line in content.split('\n')[:5]:  # Limit to first 5 lines for simplicity
        if line.strip():
            text_clip = TextClip(line, fontsize=24, color='white', size=(720, 1280)).set_duration(3)
            clips.append(text_clip)
    
    # Concatenate all text clips
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, fps=24)

if __name__ == "__main__":
    config = load_config()
    try:
        content = fetch_content(config['url'])
        generate_video(content, config['output_video'])
        print("Video generated successfully.")
    except Exception as e:
        print(f"Error: {e}")