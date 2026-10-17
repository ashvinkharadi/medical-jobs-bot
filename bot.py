import os
import requests
import feedparser

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=Medical+Recruitment+2026&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=Nursing+Officer+Vacancy&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=AIIMS+Recruitment&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=Pharmacist+Government+Jobs&hl=en-IN&gl=IN&ceid=IN:en"
]

SEEN_FILE = "seen_posts.txt"

def load_seen_posts():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_seen_post(post_id):
    with open(SEEN_FILE, "a") as f:
        f.write(post_id + "\n")

def send_telegram_message(title, link):
    message = (
        f"🩺 **Medical Job Alert!** 🩺\n\n"
        f"📌 {title}\n\n"
        f"🔗 **Details & Apply:** {link}\n\n"
        f"📢 Join: {CHAT_ID}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

def main():
    seen_posts = load_seen_posts()
    
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            post_id = entry.link
            if post_id not in seen_posts:
                send_telegram_message(entry.title, entry.link)
                save_seen_post(post_id)
                seen_posts.add(post_id)

if __name__ == "__main__":
    main()
  
