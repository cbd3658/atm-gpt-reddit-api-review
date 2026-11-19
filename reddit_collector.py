"""Read-only Reddit access. Post content is kept in memory only."""
import os
import re

from datetime import datetime, timezone

COMMUNITIES = ("wallstreetbets", "stocks", "options", "investing", "Forex", "Bitcoin")
MIN_INTERVAL = 300
ENV = ("ATM_REDDIT_CLIENT_ID", "ATM_REDDIT_CLIENT_SECRET", "ATM_REDDIT_USER_AGENT")


def fetch(client=None):
    if client is None:
        settings = [os.environ.get(key) for key in ENV]
        if not all(settings):
            return "missing_credentials", []
        try:
            import praw
        except ImportError:
            return "missing_praw", []
        client = praw.Reddit(client_id=settings[0], client_secret=settings[1],
                             user_agent=settings[2], timeout=8, ratelimit_seconds=0)
        client.read_only = True
    posts = []
    for community in COMMUNITIES:
        for post in client.subreddit(community).new(limit=25):
            if getattr(post, "removed_by_category", None) or not post.author:
                continue
            symbols = sorted(set(re.findall(r"(?<!\w)\$([A-Z][A-Z0-9]{0,5})\b", getattr(post, "title", ""))))
            posts.append(dict(source="reddit", kind="sentiment", id=post.id, community=community,
                              time=datetime.fromtimestamp(post.created_utc, timezone.utc).isoformat(), symbols=symbols,
                              link="" if post.is_self else post.url))
    return "ok", posts
