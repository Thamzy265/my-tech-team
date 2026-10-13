# Research: automated testing, evidence and host safety

Checked 13 Oct 2026. Items marked *(not checked)* come from general knowledge, not a fetched page.

## Playwright (web)

- Latest version: 1.64 (https://playwright.dev/docs/release-notes).
- Run with `npx playwright test`. It is headless by default; add `--headed` to see the browser. `npx playwright codegen <url>` records a test. The HTML report goes to `playwright-report/`, and artifacts go to `test-results/`.
- Evidence settings (https://playwright.dev/docs/test-use-options, https://playwright.dev/docs/videos):
  - `use: { screenshot: 'only-on-failure' | 'on', video: 'retain-on-failure' | 'on', trace: 'on-first-retry' }`
  - The `video` setting can also set the size and draw action overlays.
- Screenshot from a test or script: `await page.screenshot({ path, fullPage: true })` *(not checked)*.
- Browsers (https://playwright.dev/docs/browsers):
  - Install with `npx playwright install chromium`. Chromium is about 281 MB.
  - The cache lives in `~/Library/Caches/ms-playwright` (macOS), `~/.cache/ms-playwright` (Linux) or `%USERPROFILE%\AppData\Local\ms-playwright` (Windows). `PLAYWRIGHT_BROWSERS_PATH` changes it.
  - On Linux, `--with-deps` installs OS packages and needs sudo.
- Python (https://playwright.dev/python/docs/test-runners): `pip install pytest-playwright && playwright install`, then `pytest --screenshot only-on-failure --video retain-on-failure --tracing retain-on-failure --output test-results`.
- Playwright MCP (https://github.com/microsoft/playwright-mcp):
  - Install with `claude mcp add playwright npx @playwright/mcp@latest`.
  - It runs headed unless you pass `--headless`. `browser_take_screenshot` takes screenshots.
  - Video and tracing need `--caps=devtools`. `--output-dir` sets where files go.

## Maestro (mobile)

- Install (https://docs.maestro.dev/maestro-cli/how-to-install-maestro-cli): `curl -fsSL "https://get.maestro.mobile.dev" | bash` or `brew install mobile-dev-inc/tap/maestro`. It needs Java 17+ and `JAVA_HOME`. On macOS it also needs Xcode and the Command Line Tools. `MAESTRO_VERSION` pins a version.
- Run with `maestro test flow.yaml`. `--test-output-dir` sets the output folder.
- Evidence:
  - `- takeScreenshot: name` saves a PNG.
  - `- startRecording: name` … `- stopRecording` saves an MP4 next to the flow file (https://docs.maestro.dev/reference/commands-available/startrecording).
  - **`maestro record` without `--local` uploads the capture to mobile.dev's servers.** Always use `maestro record --local`.
- Flutter (https://docs.maestro.dev/platform-support/flutter): target widgets with `Semantics(identifier: …)` (`id:` selector) or `semanticLabel`. Flutter `Key`s are not visible to Maestro. Flutter Web needs `SemanticsBinding.instance.ensureSemantics()`.
- Platforms: Android emulators and iOS simulators.
- Maestro MCP (https://docs.maestro.dev/get-started/maestro-mcp): run as `maestro mcp`. Local tools need no account; only the cloud tools do.
- Telemetry: set `MAESTRO_CLI_NO_ANALYTICS=1` to turn analytics off. This was checked in the source code, not in the docs.

## Fallbacks that need no extra install

- iOS Simulator: `xcrun simctl io booted screenshot shot.png`. For video, `xcrun simctl io booted recordVideo --codec=h264 out.mp4`, stopped with Ctrl+C or SIGINT.
- Android (https://developer.android.com/tools/adb): `adb exec-out screencap -p > shot.png`. For video, `adb shell screenrecord --time-limit 180 /sdcard/x.mp4` then `adb pull`. The limit is 180 s and there is no audio.
- macOS: `screencapture -x shot.png`, or `screencapture -v` for video. The terminal needs Screen Recording permission *(not checked)*.

## Flutter's own tools

- `flutter test integration_test` (https://docs.flutter.dev/testing/integration-tests).
- Screenshots use `binding.takeScreenshot('name')` together with `integrationDriver(onScreenshot: …)` under `flutter drive`. On Android, call `convertFlutterSurfaceToImage()` first.
- Patrol 4.x (https://patrol.leancode.co/documentation) adds native interactions. Its screenshots-on-failure work on Android only, and video is not documented.

## Claude Code only

- iOS Simulator pane (https://code.claude.com/docs/en/desktop-ios-simulator): beta, Desktop on macOS, needs Xcode. The user allows each device once. The user can press Cmd+S for a screenshot and Cmd+R to record.
- Browser pane (https://code.claude.com/docs/en/desktop): previews dev servers from `.claude/launch.json`.
- Claude in Chrome (https://code.claude.com/docs/en/chrome): uses the user's real browser and logged-in state. It can record GIFs and save screenshots.

## Safety hook (Claude Code)

Sources: https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/plugins-reference, https://code.claude.com/docs/en/plugins/security

- A plugin can ship `hooks/hooks.json` with a top-level `"hooks"` wrapper: a `PreToolUse` entry with `matcher: "Bash"` running `"${CLAUDE_PLUGIN_ROOT}"/scripts/<guard>`.
- To make Claude Code ask, the hook exits 0 and prints `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"…"}}`.
  - The other values are `allow`, `deny` and `defer`. Precedence is deny > defer > ask > allow.
  - Since v2.1.211, `ask` also prompts in auto mode.
  - Exit code 2 blocks the call. Other errors and timeouts don't block, unless `"onFailure":"block"` is set.
- Plugin hooks run with the user's full privileges once the plugin is installed. There is no separate per-hook approval.
- The docs call hooks a backstop and recommend permission deny rules for hard blocks.
