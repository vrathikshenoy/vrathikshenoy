#!/usr/bin/env python3
import re
import datetime
import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
README_PATH = os.path.join(REPO_DIR, "README.md")

QUOTES = [
    "\"The question is not whether machines think but whether men do.\" — B.F. Skinner",
    "\"The analytical engine weaves algebraic patterns just as the Jacquard loom weaves flowers.\" — Ada Lovelace",
    "\"A computer would deserve to be called intelligent if it could deceive a human into believing that it was human.\" — Alan Turing",
    "\"An intelligence is a mechanism that makes decisions in the face of uncertainty.\" — Unknown Neural Net",
    "\"Hardware is what makes a machine fast. Software is what makes a machine slow. AI is what makes it think.\"",
    "\"Gradient descent is the ultimate programmer. It writes programs we could never conceive.\"",
    "\"while(alive) { learn(); build(); share(); repeat(); }\""
]

def update_readme():
    if not os.path.exists(README_PATH):
        print(f"README.md not found at {README_PATH}")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Sync Time
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sync_text = f"System Sync: {now_utc} (Active)"
    
    content = re.sub(
        r"<!-- SYNC_TIME_START -->.*?<!-- SYNC_TIME_END -->",
        f"<!-- SYNC_TIME_START -->{sync_text}<!-- SYNC_TIME_END -->",
        content,
        flags=re.DOTALL
    )

    # 2. Update Random Quote
    random_quote = random.choice(QUOTES)
    quote_text = f"\n```\n{random_quote}\n```\n"
    
    content = re.sub(
        r"<!-- QUOTE_START -->.*?<!-- QUOTE_END -->",
        f"<!-- QUOTE_START -->{quote_text}<!-- QUOTE_END -->",
        content,
        flags=re.DOTALL
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully updated README.md with live sync time and random quote!")

if __name__ == "__main__":
    update_readme()
