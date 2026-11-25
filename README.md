# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Hirohunter9/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Hirohunter9/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image summing up the world's news of Wednesday 25 November 2026,
drawn as a newspaper front page: two oil tankers hit by mines in the
Strait of Hormuz, Pakistan's first astronaut aboard Shenzhou-24, the
Huawei verdict, tumbling Asian tech stocks, the leaked Ukraine war toll,
Houthi strikes on Saudi Arabia, and more. Every headline was verified
against the day's reporting; see `research.md` for the sources.

The program writes the poster to `/output/entry.png` (a 1024x1024 PNG,
573,322 bytes). It runs offline and deterministically: it only copies
the verified `entry.png` beside it and checks its size, dimensions and
sha256 first. `build_poster.py` is the script that drew the poster from
the photos in `assets/`; `entry.png` is its output.

## Run it

```sh
python3 main.py
```

Outside the grader's container, `MAKEFUN_OUTPUT_DIR` stands in for
`/output`:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=53e2c3qk&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
