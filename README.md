# ATM GPT Reddit API review

This repository contains the Reddit-facing collector from ATM GPT, a local market briefing tool, with its timestamp conversion inlined for independent review. The host application schedules the collector about every five minutes. The public sample does not schedule requests or send them when imported.

The collector uses read-only OAuth through PRAW and requests up to 25 recent submissions per poll from each of r/wallstreetbets, r/stocks, r/options, r/investing, r/Forex, and r/Bitcoin. It counts discussion activity and cashtag mentions and matches outbound links to previously collected news. Briefings use aggregate counts. Post text and Reddit usernames are not included in briefings. The collector does not post, comment, vote, send messages, or place trades.

Reddit API access requires prior approval. The collector reads its client ID, client secret, and User-Agent from the local environment. This repository contains no credentials or collected data.
