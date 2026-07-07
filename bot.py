"""
Z Agent — Autonomous Solana KOL Reply Bot
Main entry point. Monitors Twitter mentions and generates AI-powered replies.
"""

import os
import time
import random
import datetime
from datetime import timezone

from core.twitter import TwitterClient
from core.ai import AIEngine
from core.dedup import DedupStore
from core.context import ContextBuilder
from config import Config


def main():
    print(f"Z Agent v1.0.0 starting...")
    print(f"Monitoring @{Config.BOT_USERNAME}")
    print(f"Model: {Config.XAI_MODEL}")
    print(f"Poll interval: {Config.POLL_INTERVAL}s")
    print("=" * 50)

    twitter = TwitterClient()
    ai = AIEngine()
    dedup = DedupStore()
    context_builder = ContextBuilder(twitter)

    bearer = twitter.get_bearer_token()
    print("Bearer token OK")

    replied_ids = dedup.load()
    print(f"Loaded {len(replied_ids)} replied IDs from disk.")

    last_checked = datetime.datetime.now(timezone.utc) - datetime.timedelta(minutes=15)

    while True:
        try:
            mentions = twitter.fetch_mentions(bearer, Config.BOT_USERNAME, last_checked)

            for mention in mentions:
                tweet_id = mention["id"]
                text = mention["text"]
                author = mention["author"]

                if tweet_id in replied_ids:
                    continue

                print(f"\nNew mention from @{author}: {text}")

                parent_context = context_builder.get_parent_context(bearer, mention)
                if parent_context:
                    print(f"  Context: {parent_context[:80]}...")

                reply = ai.generate_response(text, author, parent_context)
                print(f"  → {reply}")

                success = twitter.reply(tweet_id, reply)
                if success:
                    replied_ids.add(tweet_id)
                    dedup.save(replied_ids)

            last_checked = datetime.datetime.now(timezone.utc)
            jitter = random.uniform(-5, 5)
            time.sleep(Config.POLL_INTERVAL + jitter)

        except KeyboardInterrupt:
            print("\nShutdown requested. Saving state...")
            dedup.save(replied_ids)
            break
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
