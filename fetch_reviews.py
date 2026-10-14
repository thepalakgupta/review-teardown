import time
import pandas as pd
from google_play_scraper import app, reviews, Sort

APP_ID = "in.stage"
PER_LANGUAGE = 6000          # target reviews per language
OUTPUT = "data/reviews.csv"

# Basic app info (rating, installs) for context
info = app(APP_ID, lang="en", country="in")
print(f"App: {info['title']}  |  rating {info['score']:.2f}  |  installs {info['installs']}")

all_rows = []
for lang in ["en", "hi"]:    # many STAGE users write in Hindi / Hinglish
    token, fetched = None, 0
    while fetched < PER_LANGUAGE:
        batch, token = reviews(APP_ID, lang=lang, country="in",
                               sort=Sort.NEWEST, count=200,
                               continuation_token=token)
        if not batch:
            break
        for r in batch:
            r["lang_requested"] = lang
        all_rows.extend(batch)
        fetched += len(batch)
        print(f"  {lang}: {fetched} reviews")
        if token is None:
            break
        time.sleep(1)        # be polite to the servers

df = pd.DataFrame(all_rows).drop_duplicates(subset="reviewId")

# Privacy: drop reviewer names and profile pictures. We only analyse what was said.
df = df.drop(columns=["userName", "userImage"], errors="ignore")

import os
os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT, index=False)

print(f"\nSaved {len(df):,} unique reviews to {OUTPUT}")
print(f"Date range: {df['at'].min()}  ->  {df['at'].max()}")
print(df["score"].value_counts().sort_index())

