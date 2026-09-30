import feedparser, requests, os

PAGE_ID = os.environ.get("PAGE_ID")
PAGE_TOKEN = os.environ.get("PAGE_TOKEN")
RSS_URL = os.environ.get("RSS_URL")

def get_latest():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries: 
        print("No entries in RSS")
        return None
    posted_file = "posted.txt"
    posted = []
    if os.path.exists(posted_file):
        with open(posted_file) as f: posted = f.read().splitlines()
    for entry in feed.entries:
        if entry.link not in posted:
            return entry
    print("All posts already posted")
    return None

def post_to_fb(message):
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    r = requests.post(url, data={"message": message, "access_token": PAGE_TOKEN})
    print(r.text)
    return r.json()

entry = get_latest()
if entry:
    msg = f"{entry.title}\n\n{entry.description}\n\nRead more 👉 {entry.link}\n\n#Wellness #Motivation #Ghana"
    post_to_fb(msg)
    with open("posted.txt", "a") as f: f.write(entry.link + "\n")
