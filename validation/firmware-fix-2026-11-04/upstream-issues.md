# QIDI GitHub issue check — 2026-11-04

Read-only GitHub API checks covered the MAX4 issue list (all states), releases,
recent commits, and QIDITECH-wide issue searches for refill and extrude_state.
No issue or published fix for the exact observed logical-tool/physical-slot
confusion was found. This is a search result, not proof no report exists elsewhere.

- [MAX4 issues](https://github.com/QIDITECH/QIDI_MAX4/issues): only issue1 was
  returned, requesting generic materials. No GitHub releases were returned.
  Latest source commit was 47fc14cefe064dbd30b90582429fe650883ae900,
  dated2026-08-06.
- [Q2 issue32](https://github.com/QIDITECH/QIDI_Q2/issues/32), open, filed2026-11-03:
  reports failed refill in a four-Box multicolor job and an AttributeError for
  loaded_stepper during a later tool change. Its reported failure differs from
  this MAX4's successful replacement selection followed by wrong-slot resume.
- [Q2 issue24](https://github.com/QIDITECH/QIDI_Q2/issues/24): reports unexpected
  saved tool/slot assignments after an update. It does not establish this refill
  handler's root cause.
- [Plus4 issue112](https://github.com/QIDITECH/QIDI_PLUS4/issues/112): reports
  wrong-slot selection when starting from the printer screen; a comment describes
  correcting a missing preparation-extruder parameter. Different start paths can
  matter, but neither observation proves why Dan's memory-start refill works.

Dan's memory-start observation remains user-reported, with no matched local-start
trace yet. The installed correction is based on the recorded failure and isolated
execution of his exact vendor modules, not on adopting a suggested issue workaround.
No issue/comment was posted and no firmware update was installed from these links.
