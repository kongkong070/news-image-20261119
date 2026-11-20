# The World in One Day — Thursday 19 November 2026

A one-page newspaper front page summing up the world's news of
Thursday 19 November 2026, drawn offline with Pillow (`draw.py`) and
committed as `entry.png`. `main.ts` (Node 22, stdlib only) copies it to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).

## Stories

1. **Three leaders, one table** — Trump, Xi and Putin hold a historic
   trilateral summit in Shenzhen and issue a joint peace declaration.
2. **Genocide, the court rules** — the ICJ finds Myanmar committed
   genocide against the Rohingya, a first for a state.
3. **Bridge hit a third time** — Ukraine strikes the Crimea bridge
   again in a week; trains halted before the summit.
4. **$81bn debut** — Anthropic starts trading on Nasdaq after the
   biggest IPO on record; shares open near $111.
5. **A $190.4m Van Gogh** — "Chestnut Trees in Blossom" (1890) sets
   an auction record for the artist at Sotheby's.
6. **Dozens missing** — a migrant boat capsizes off Yenne, Senegal.

Sources: BBC, Reuters, AP, UN — see `SOURCES.md`.

## Run

```sh
python3 draw.py            # regenerate entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
