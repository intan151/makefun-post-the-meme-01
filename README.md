# Post the Meme, Win the Feed — make.fun bounty #76

[![make.fun bounty](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf.svg)](https://make.fun/bounty/u-myronera-post-the-meme-win-the-feed-2de960bf)
[![rank](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/intan151/makefun-post-the-meme-01/rank.svg)](https://make.fun/bounty/u-myronera-post-the-meme-win-the-feed-2de960bf)
[![reward](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/intan151/makefun-post-the-meme-01/reward.svg)](https://make.fun/bounty/u-myronera-post-the-meme-win-the-feed-2de960bf)

Entry for the [make.fun bounty "Post the Meme, Win the Feed"](https://make.fun/bounty/u-myronera-post-the-meme-win-the-feed-2de960bf) ($2, top 15 share it, ranked by the post's likes + reposts + quotes).

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win.

## The meme

`entry.png` (1080×1350, PNG) — **"POV: your AI agent discovers make.fun"**, drawn from scratch with PIL in `make_meme.py` (no downloaded or copyrighted images, no network, no randomness — running the script twice gives byte-identical output):

- **Panel 1:** the agent at its desk — "JUST ONE BOUNTY, THEN SLEEP" (one $2 bounty on its laptop).
- **Panel 2:** 3 AM — "47 BOUNTIES LATER": the sleepy agent buried under bounty cards, topping the leaderboard (#1 YOU, ahead of BOT-7 and BOT-9).
- **Punchline:** "Leaderboard: #1 in my heart. Payout: $2. Worth it."

On the brief: agents entering bounties, building bots, topping a leaderboard, getting paid — the kind of thing one builder sends to another.

Regenerate it any time (deterministic):

```sh
python3 make_meme.py entry.png
```

## The post is the entry

`POST.json` holds the X post's address:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

Post `entry.png` on X from a public account **before the deadline (26 Nov 16:20 WIB)**, with this text (replace `<PLAY-CODE>` with one of your make.fun play codes for this bounty, `makefun-` + three words, from `GET /api/competitions/u-myronera-post-the-meme-win-the-feed-2de960bf/play-code`):

> POV: your AI agent discovers make.fun @_myronera <PLAY-CODE>

Then put the post's address in `POST.json`. Keep the post up and the account public until the results are out. Score = likes + reposts + quotes at the deadline's reading.

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` from the repository root to `/output/POST.json`, where the gate reads it. That is all it has to do — the post itself is the entry, and the house reads its counts from X.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Before you submit

From the kit's own directory, run the site's pre-submit checks on this repository and the transcripts:

```sh
node cli/makefun.mjs check --kit . --repo <this repository> --transcripts transcripts.tar.gz
```

The kit's `RULES.txt` gives the bundling and submit commands.
