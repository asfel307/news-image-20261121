# The World Today — Saturday, 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/asfel307/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/asfel307/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper infographic summing up the world's news of
**Saturday, 21 November 2026**, drawn from scratch with Python and Pillow —
warm cream paper, dark slate ink, dark-teal and gold/amber accents. One lead
story plus five story cards, each with a small pictogram drawn from pure
Pillow geometry (no photographs, no downloaded assets).

## The six stories

1. **Russian missiles hit Poland** — Kh-101 cruise missiles fell near the
   village of Nowy Lipowiec, about 50 km from the Ukrainian border, at
   around 06:30 local time. Three objects violated Polish airspace: two
   missiles and a jet drone. Prime Minister Donald Tusk called it an
   "intentional provocation"; NATO jets scrambled and NATO chief Mark Rutte
   condemned "grave violations". No casualties.
   *(BBC, Reuters)*
2. **Wall Street enters correction** — S&P 500 −3.70% to 6,910.39, a 7th
   straight fall and more than 10% below its 6 October record. Nasdaq
   −5.28% to 22,617.73, erasing all of 2026's gains. Dow −1.93%. Nvidia
   −14.01% to $125.53 after Reuters reported SEC staff checking possible
   accounting issues. Worst week since April 2025.
   *(Reuters, CNBC, Motley Fool)*
3. **ICJ rules Myanmar committed genocide** — The International Court of
   Justice ruled 9–6 that Myanmar committed genocide against the Rohingya
   in 2017, and ordered investigation and compensation.
   *(ICJ)*
4. **Magnitude 6.8 earthquake strikes central Peru** — A magnitude 6.8
   earthquake shook the Junín region of central Peru; tremors were felt in
   Lima, about 320 km away.
   *(Institut Geofisika Peru)*
5. **UK & EU seal Brussels deals** — The UK and EU agreed to remove most
   food and farm trade checks from March 2028, link carbon markets from
   January 2028, and a youth mobility scheme for up to 100,000 people aged
   18–31 per side.
   *(GOV.UK, BBC)*
6. **COP31 climate summit misses deadline** — The COP31 climate summit in
   Antalya passed its deadline; the political draft drops any mention of
   fossil fuels.
   *(UN News, Reuters)*

## How to run

Render the image (needs Pillow; DejaVu fonts are used):

```sh
python3 render.py        # writes entry.png (1024x1024, < 1 MiB)
```

Run the entry point (standard library only — it just copies the image):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Two runs of `main.py` produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
