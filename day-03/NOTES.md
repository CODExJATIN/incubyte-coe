# Day 3 Notes

## My cleaner vs Claude Code's

I built the order cleaner test-first myself, then asked Claude Code to go through the same task and throw edge cases at my script that my tests don't cover.

What my tests already cover: trimming fields, dropping blank ids, removing duplicate ids, converting dates to ISO, dropping rows with dates that can't be read, and loading the clean file into DuckDB to check the counts.

Edge cases Claude found that mine doesn't handle:

- **A short row in the CSV** (like `2003,Meera` with no date or amount): csv gives `None` for the missing columns and my code crashes on `.strip()`, so one bad row kills the whole file
- **Amount that isn't a number** (`abc`): mine keeps it in the clean file and it only fails later when DuckDB tries to load it as DECIMAL
- **Negative amount** (`-50`): mine keeps it. Not sure this is wrong though, could be a refund, so it's a business question not a cleaning one

All three are about the amount column or the shape of the row, my tests only looked at ids and dates. Same lesson as Day 1, I test wrong values but not wrong shapes.

## Reading JSON

Added `read_orders_json` so the same cleaner works on a JSON file too. JSON gives numbers and `null` instead of strings, so they get turned into strings first (null becomes empty), then the same cleaning runs.

## Reflection

The hardest case was dates like `03/04/2025`, it's hard to tell if it's 3rd April or 4th March, and the parser never fails since it's a valid date in both dd/mm/yyyy and mm/dd/yyyy. I went with dd/mm/yyyy, but the file itself can't tell you which one is right.

The other one was duplicate ids. When two orders have the same id, which one wins? Currently the first one wins, but in real data it's not guaranteed the first (or the last) one is the correct one. You would need something like an updated-at time to decide.
