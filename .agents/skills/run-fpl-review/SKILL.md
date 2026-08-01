---
name: run-fpl-review
description: Orchestrate one complete FPL Draft research iteration and publish it through a fresh branch, reviewed pull request, squash merge and branch deletion.
---

# Run an FPL review

Use this skill for a scheduled or manually requested full review.

## Inputs

- Official FPL API player and fixture data.
- Current board and watchlist from the latest `main`.
- Latest immutable review and changes record.
- New public evidence since the prior review.

## Branch setup

1. Establish the review timestamp in Australia/Melbourne.
2. Read the latest `main` and confirm there is no newer completed review than the one being used as baseline.
3. Create a new unique branch from current `main` named `codex/fpl-review-YYYYMMDD-HHmm-<short-slug>`.
4. Never reuse a prior run branch and never write review changes directly to `main`.

## Research and documentation procedure

1. Read `AGENTS.md` and the canonical current documents.
2. Run `sync-fpl-api` and record player-pool additions, removals and metadata changes.
3. Run `collect-public-evidence`, focusing on developments since the previous review.
4. Run `assess-preseason` when preseason evidence exists.
5. Run `assess-transfer-risk` for transfer and squad-competition developments.
6. Run `rank-draft-board` to produce the complete top-220 order and positional priorities.
7. Run `document-fpl-review` to create the immutable review and delta documents and update current state.
8. Run `maintain-obsidian-vault` to update entity notes, links and the wiki.
9. Validate that every material claim has a specific citation and every changed Markdown file appears in the document changelog.

## Publication procedure

1. Commit only the files belonging to this review branch.
2. Open one non-draft pull request to `main` summarising the review timestamp, material ranking changes, created review/change records and validation performed.
3. Inspect the complete PR diff and confirm:
   - all required documents exist;
   - citations point to specific posts, articles or API endpoints;
   - timestamps and paths are correct;
   - Obsidian links resolve consistently;
   - every changed Markdown file has a changelog row;
   - the PR is mergeable;
   - every configured check passes, or that no checks are configured.
4. Squash-merge the PR only after all completion conditions pass.
5. Verify the merge commit is on `main`.
6. Delete the merged head branch.
7. Report the PR number, merge commit and confirmation that the branch was deleted.

## Completion test

A run is incomplete unless it creates and publishes:

- one dated full review;
- one dated changes document;
- a reconciled current board;
- a reconciled current watchlist;
- updated affected entity notes;
- an updated wiki summary;
- a changelog entry for every changed Markdown document;
- one merged pull request based on a fresh branch;
- deletion of the merged head branch.

When there are no material changes, state that explicitly. Do not manufacture movement. If a PR cannot be safely merged or its branch cannot be deleted, report the incomplete lifecycle step rather than claiming success.
