// Repository guards on the TypeScript side: the package manifest the workspace grows from.
// Runs in CI (`bun test`) on every develop push and pull request, until code brings its own tests.
import { describe, expect, test } from "bun:test";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = join(import.meta.dir, "..");
const manifest = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));

describe("package.json", () => {
  test("is private: Parti is not published to npm from the root", () => {
    expect(manifest.private).toBe(true);
  });

  test("declares the project's licence, GPL-3.0-only (D20)", () => {
    expect(manifest.license).toBe("GPL-3.0-only");
  });

  test("is an ES module package", () => {
    expect(manifest.type).toBe("module");
  });
});

describe("lockfile", () => {
  test("bun.lock is committed, so CI installs with --frozen-lockfile", () => {
    expect(existsSync(join(root, "bun.lock"))).toBe(true);
  });
});
