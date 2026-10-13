# Automation tools and evidence capture

Checked: 2026-10-13. Check the current source when a rule decides an outcome.

Use the tool the project's Team setup names. These are the defaults. Items marked *(not checked)* come from general knowledge, not a fetched page.

| Product | Tool | Evidence |
|---|---|---|
| Web UI | Playwright (`npx playwright test`; Python: `pytest-playwright`) | `screenshot`, `video`, `trace` settings; `page.screenshot()` |
| Mobile app (Flutter, iOS, Android) | Maestro (`maestro test flow.yaml`) | `takeScreenshot`, `startRecording` / `stopRecording`; `maestro record --local` only |
| Flutter, inside the app's own tests | `flutter test integration_test` | `binding.takeScreenshot()` |
| API, CLI or daemon | the project's test runner plus real requests (curl or an HTTP client) | captured request and response, masked |
| No tool installed yet | `xcrun simctl io`, `adb`, `screencapture` | PNG / MP4 |

Installing a tool or a browser changes the PM's machine. Ask once per tool, with the exact command, the size and where it goes on disk (see the SKILL's "Asking the PM before a host change"). After a yes, the lead records it under "Approved tools" in Team setup; don't ask again for that tool.

## Playwright (web)

- **Run:** `npx playwright test` (headless by default; `--headed` to watch). Put QA output in the git-ignored folder: `npx playwright test --output=qa-artifacts/<milestone>`. The HTML report goes to `playwright-report/`; keep it out of git.
- **Evidence settings** for a QA run (in `playwright.config.ts`, or a QA-only config passed with `--config`):

  ```ts
  use: { screenshot: 'on', video: 'on', trace: 'on-first-retry' }
  ```

  The committed suite usually keeps `screenshot: 'only-on-failure'` and `video: 'retain-on-failure'`; turn them on only for the QA run. One test per user flow gives one video per flow.
- **Named screenshots** of a key state, viewport only:

  ```ts
  await page.screenshot({ path: 'docs/qa/M3/screens/1-full.png' });
  await page.getByRole('button', { name: 'Book' }).screenshot({ path: 'docs/qa/M3/screens/1-book-focus.png' });
  ```

  Add `fullPage: true` only when the whole page matters.
- **Checks people hand over by mistake** *(not checked)*:
  - keyboard and focus: `await page.keyboard.press('Tab')`, then `await expect(page.getByRole('button', { name: 'Book' })).toBeFocused()` and screenshot the focused element;
  - roles and announcements: `await expect(page.getByRole('alert')).toHaveText('…')`, or `await expect(page.locator('main')).toMatchAriaSnapshot(…)` for the accessibility tree;
  - 320 px: `await page.setViewportSize({ width: 320, height: 640 })`, then screenshot.
- **Where QA's own scripts live:** reuse the tester's specs first. A capture-only script goes in `qa-artifacts/scripts/` (not committed). If a check should stay in the suite, ask the tester through the lead to add it.
- **Python:** `pip install pytest-playwright` (inside the project's venv), then `pytest --screenshot on --video on --tracing retain-on-failure --output qa-artifacts/<milestone>`.
- **Browsers:** `npx playwright install chromium`, about 281 MB, into `~/Library/Caches/ms-playwright` (macOS), `~/.cache/ms-playwright` (Linux) or `%USERPROFILE%\AppData\Local\ms-playwright` (Windows). This is an install: ask once. On Linux, `--with-deps` also needs `sudo`: ask for that separately.

## Maestro (mobile)

- **Run:** `maestro test flow.yaml --test-output-dir qa-artifacts/<milestone>`. Set `MAESTRO_CLI_NO_ANALYTICS=1` to turn analytics off.
- **Evidence in the flow:**

  ```yaml
  - startRecording: checkout-flow
  - tapOn:
      id: "pay-button"
  - takeScreenshot: 2-receipt
  - stopRecording
  ```

  The recording is saved next to the flow file; move it to `qa-artifacts/`. Copy the key-state PNGs to `docs/qa/<milestone>/screens/`.
- **`maestro record` uploads the capture to mobile.dev's servers unless you add `--local`.** Always run `maestro record --local flow.yaml`.
- **Flutter:** target widgets with `Semantics(identifier: …)` (the `id:` selector) or a semantic label. Flutter `Key`s are not visible to Maestro; a widget without either is a test-hook gap for the developer, through the lead. Flutter Web also needs `SemanticsBinding.instance.ensureSemantics()`.
- **Needs:** Java 17+ with `JAVA_HOME` set; on macOS, Xcode and the Command Line Tools. Installing Maestro (`brew install mobile-dev-inc/tap/maestro`) is an install: ask once. Never use the `curl … | bash` installer without the PM's yes.

## Flutter integration tests

- Run with `flutter test integration_test`.
- Screenshots: `binding.takeScreenshot('2-receipt')` with `integrationDriver(onScreenshot: …)` under `flutter drive`. On Android, call `convertFlutterSurfaceToImage()` first.
- Patrol adds native interactions; its screenshots-on-failure work on Android only and it has no documented video, so record with the fallbacks below.

## API, CLI and daemon evidence

- Capture the exact request and the response (status, headers that matter, body) against the local server: `curl -sS -i http://localhost:<port>/<path>`.
- Mask tokens, cookies and personal data before pasting (`Bearer ****abcd`).
- For a CLI, paste the command and its output; for a daemon, the log lines with IDs, not personal data.

## Fallbacks that need no extra install

- **iOS Simulator:** `xcrun simctl io booted screenshot shot.png`; video with `xcrun simctl io booted recordVideo --codec=h264 qa-artifacts/<name>.mp4`, stopped with Ctrl+C. (`simctl erase` and `delete` are host changes: ask first.)
- **Android:** `adb exec-out screencap -p > shot.png`; video with `adb shell screenrecord --time-limit 180 /sdcard/x.mp4`, then `adb pull /sdcard/x.mp4 qa-artifacts/`. The limit is 180 s, with no audio.
- **macOS:** `screencapture -x shot.png`, or `screencapture -v` for video. The terminal needs the Screen Recording permission, which is a system permission dialog: the PM grants it, you don't *(not checked)*.

## *On Claude Code*

- **Browser pane:** previews the project's dev server from `.claude/launch.json`. Use it to drive the flow, read the accessibility tree, the console and network requests, and look at each state. Save a PNG of every key state; if the pane can't write a file, capture the window with a fallback above, and say which in the evidence file.
- **iOS Simulator tools** (Desktop on macOS, beta, needs Xcode): drive the app, take screenshots and record. The PM allows each device once.
- **Claude in Chrome** uses the PM's real, logged-in browser. Ask the PM's OK **each time** before using it, and never capture the PM's own accounts or data.
