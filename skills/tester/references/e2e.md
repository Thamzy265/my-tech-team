# End-to-end tests

Checked: 2026-10-13. Check the current source when a rule decides an outcome.

Use the tool the project's Team setup names. The defaults are Playwright for web, Maestro for mobile apps, and Flutter `integration_test` inside a Flutter app's own tests. Items marked *(not checked)* come from general knowledge, not a fetched page.

## Where the files go

- Follow the project's convention if it has one. Otherwise:
  - Playwright: `e2e/<flow>.spec.ts` (Node) or `e2e/test_<flow>.py` (Python, `pytest-playwright`), with `playwright.config.ts` at the root;
  - Maestro: `.maestro/<flow>.yaml`;
  - Flutter: `integration_test/<flow>_test.dart`.
- The test runner itself (`npm i -D @playwright/test`, or `pytest-playwright` in the venv) is a dev-only dependency inside the project. Add it in its own commit (`test(e2e): add playwright`) with the lockfile, and name it in the report. If the project's rules forbid extra packages, it is a PM decision first (see the SKILL).
- Output folders (`test-results/`, `playwright-report/`, `qa-artifacts/`) are git-ignored. Never commit their contents.

## Playwright (web)

- **One test per user flow,** named after what the user does. One `describe` per page or feature.
- **Locators by role, label or text,** never by CSS class or position:

  ```ts
  import { test, expect } from '@playwright/test';

  test.describe('invoice list', () => {
    test('sends a draft invoice', async ({ page }) => {
      await page.goto('/invoices');
      await page.getByRole('button', { name: 'Send invoice: #1042' }).click();
      await expect(page.getByRole('status')).toHaveText('Invoice #1042 sent');
    });

    test('shows the empty state when there are no invoices', async ({ page }) => {
      await page.route('**/api/invoices', r => r.fulfill({ json: [] }));
      await page.goto('/invoices');
      await expect(page.getByText('No invoices yet')).toBeVisible();
    });
  });
  ```

- **States-matrix rows:** use `page.route()` to return empty, error or slow responses from the project's own API, so each state is reached on purpose *(not checked)*. Never call real third-party services.
- **Keyboard rows:** `page.keyboard.press('Tab')` and `expect(locator).toBeFocused()`.
- **The committed suite's evidence settings** (in `playwright.config.ts`):

  ```ts
  use: { screenshot: 'only-on-failure', video: 'retain-on-failure', trace: 'on-first-retry' }
  ```

  QA turns screenshots and video fully on for its own run; don't commit `'on'`.
- **Run:** `npx playwright test` (Python: `pytest e2e`). The browser install (`npx playwright install chromium`, about 281 MB, into `~/Library/Caches/ms-playwright` on macOS or `~/.cache/ms-playwright` on Linux) is asked once; `--with-deps` on Linux needs `sudo` and is asked separately.
- `npx playwright codegen <url>` can record a first draft; rewrite its locators to roles and labels.

## Maestro (mobile)

- One flow file per user flow. Select by `id:` (a Flutter `Semantics(identifier: …)`, an Android resource id or an iOS accessibility identifier) or by visible text:

  ```yaml
  appId: com.example.invoices
  ---
  - launchApp
  - tapOn:
      id: "invoice-1042-send"
  - assertVisible: "Invoice #1042 sent"
  ```

- Flutter `Key`s are not visible to Maestro. A widget with no `Semantics` identifier or label is a test-hook bug for the developer.
- Run with `maestro test .maestro/` and `MAESTRO_CLI_NO_ANALYTICS=1`. Never `maestro record` without `--local`.
- Maestro needs Java 17+ and, on macOS, Xcode. Installing it is asked once.

## Flutter `integration_test`

- `integration_test` comes with the Flutter SDK. If it isn't under `dev_dependencies` yet, ask the lead; adding it changes `pubspec.yaml`, which you don't edit. Call `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` at the top of each file.
- Find widgets with `find.bySemanticsLabel` or `find.byType`, tap with `tester.tap`, and settle with `tester.pumpAndSettle()`.
- Run with `flutter test integration_test` on a simulator or emulator. Never erase or reset a device to make a run pass: that is a host change and needs the PM.

## Fail first

- Run each new e2e test on the new code (pass), then against the old code: check out the old production files (as in the SKILL's Rules) or remove the feature's entry point, and confirm the test fails with a clear line (for example "locator getByRole('button', { name: 'Send invoice: #1042' }) not found"). Restore the new code and run `git status`.
- A test that can't run yet (tool not installed, waiting for the PM) is committed and reported as `pending install`; it shows fail-then-pass after the install.
