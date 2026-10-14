# 🔍 Review Teardown

**An AI agent that reads thousands of app reviews, in English, Hinglish and Hindi, and turns them into product decisions.**

Point it at any Play Store app. It pulls public reviews, profiles them, groups complaints into themes, ranks what matters most, and writes a report a product team can act on. You don't script the analysis steps; the agent decides what to investigate next.

📄 **[Read the sample teardown: STAGE →](https://thepalakgupta.github.io/review-teardown/examples/report.html)** · Built with the [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview)

---

## What it found: STAGE (regional-dialect OTT app)

Run on 7,467 public Play Store reviews, with a focus on the last 12 months:

- **The rating drop wasn't what it looked like.** The average fell from 4.4 to 3.2, mostly because short "good" / "nice" 5★ reviews dried up, not because complaints surged. But reviews with real content did turn more negative.
- **68% of substantive complaints are about money,** and most trace back to one journey: a ₹1 trial that becomes a ₹199 autopay that users didn't expect and found hard to stop.
- **"I paid and still can't watch" jumped to 33% of complaints in May–Jul 2026,** with one recurring mechanism: turning off autopay ended the trial users had already paid for.
- **Users love the content.** Only 5% of complaints are about the library. Praise centres on regional culture, emotional stories and specific titles.

It ends with six ranked, testable recommendations, each with a metric to watch.

## How it works

| Stage | What the agent does | Output |
|---|---|---|
| 1. Profile | Volume, ratings, language mix, trends, app versions, developer replies | `profile.md` |
| 2. Themes | Builds a complaint taxonomy, tags every review with multilingual rules, validates by sampling | `themes.md` |
| 3. Diagnosis | Ranks themes by volume × severity × agreement × trend, digs into the top issues | `recommendations.md` |
| 4. Report | Builds a single-page HTML report for the product team | `report.html` |

At each stage, Claude writes its own Python, runs it, reads the results and decides what to dig into next. The analyst method is encoded in the system prompt in `review_doctor.py`.

## Run it on any app

**Requirements:** Python 3.10+, a Claude account (Pro or higher), and [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) logged in.

```bash
git clone https://github.com/thepalakgupta/review-teardown.git
cd review-teardown
python -m venv .venv
.venv\Scripts\activate        # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

1. Set `APP_ID` in `fetch_reviews.py` to the app's Play Store ID (the part after `id=` in its store URL) and run `python fetch_reviews.py`.
2. Set `APP_NAME` in `review_doctor.py`, then run `python review_doctor.py` for all four stages, or `python review_doctor.py 1` to run one stage at a time.
3. Open `output/report.html`.

## Design choices

- **Multilingual by default.** Indian app reviews are often in Hinglish or Devanagari. Here, 58% of substantive feedback was in Hindi or Hinglish. Dropping them would miss most of the signal.
- **Substance over volume.** One-word reviews ("good", "nice") are counted but not themed. Insights come from reviews with real content.
- **Validated tagging.** Theme rules are checked by reading random samples and refined until precision is high.
- **Fair by design.** Reviewer names are dropped at download. Unproven suspicions are framed as questions for the company, never as claims.

## Limitations

- Reviewers aren't all users: very happy and very angry people post more. The report shows what reviewers raise, not how many users are affected.
- Keyword tagging can miss sarcasm and unusual spellings.
- App version is tied to calendar time, so version gaps are leads to check, not proof.

---

*Independent analysis of public reviews. Not affiliated with or endorsed by STAGE.*

Built by [Palak Gupta](https://github.com/thepalakgupta), an analyst working at the intersection of AI and product analytics.