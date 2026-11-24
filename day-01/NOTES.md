# Day 1 Notes

## My version vs Claude Code's version

I wrote the record cleaner myself first, then asked Claude Code to do the same task and compared.

Both handle the basics the same way: trimming fields, rejecting a missing or blank id, and converting the dates to ISO.

But Claude's version handled some cases mine doesn't. If the record has no `signup_date` key, or the date is `None` or a number, my code just crashes with a KeyError/TypeError instead of rejecting the record properly. All my tests used nicely shaped records with strings, so I never thought about the wrong shape of data, only wrong values. Fixed it later test-first, now all three are rejected with a ValueError.

What I didn't take from it: it added extra date formats and an extra parameter nobody asked for, and it was written in one go, not test by test.

## DORA metrics

- **Deployment frequency** - how often we push changes to prod
- **Lead time for changes** - how long from commit to running in prod
- **Change failure rate** - how many of those deployments break something
- **Time to restore** - how fast we recover when something breaks

For a data pipeline, a deployment is when a change to the pipeline goes live (new transformation, query change, schema change). The daily scheduled run is not a deployment.

A change failure isn't only the job crashing. The worse case is when the job runs fine but the data is wrong (duplicates, missing rows, wrong totals) and nobody notices. Restoring then means fixing the code and also fixing the bad data that already got loaded.

## Claude Code, BEE and Learn

Claude Code is like a pair programmer in the terminal, but I'm still responsible for what gets committed. The rules for the repo go in `CLAUDE.md` (one test at a time, minimal code, refactor separately), so it works the way we work.

BEE follows the Incubyte way: spec first, then tests, then code in small slices, then review. Learn is more for learning: it guides you through the task instead of just giving the answer.

## Reflection: which value will stretch me most

Work-in-Public. I usually work quietly and only show things once they feel done. You can see it in my commits: on Day 1 and Day 3 I worked for hours but committed everything at the end, so the history doesn't show how the work actually went. The playbook says to keep work and progress visible and to be open about mistakes. I'm trying to commit as I go now, and Day 4 is already better.

## Reflection: what does test-first change

It makes me think about bad input before writing the code: what happens with an empty id, a weird date, a date that doesn't exist. Without tests I would write the happy path and find these problems later in the data. It also keeps the functions small.

But tests only cover what I think of. The comparison with Claude showed that, since I missed the missing-key and None cases. With data I need to test the wrong shape of the record too, not just wrong values.
