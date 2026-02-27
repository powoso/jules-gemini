from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Optional
import asyncio
import concurrent.futures

from app.models import SocialMediaPost
from app.services.reddit import scrape_subreddit
from app.services.twitter import scrape_twitter_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/api/feed")
async def get_feed(source: str = "all", subreddit: str = "technology", username: str = "elonmusk"):

    # Run scrapers in threadpool executor to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    tasks = []

    if source == "all" or source == "reddit":
        tasks.append(loop.run_in_executor(executor, scrape_subreddit, subreddit))

    if source == "all" or source == "twitter":
        tasks.append(loop.run_in_executor(executor, scrape_twitter_user, username))

    results = await asyncio.gather(*tasks)

    all_posts = []
    for res in results:
        if isinstance(res, list):
            all_posts.extend(res)

    # Simple sort attempt
    # We can try to standardize timestamps or just return
    return all_posts

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")
