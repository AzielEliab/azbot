import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import worker from "../src/index.js";

const origFetch = globalThis.fetch;
before(() => {
  globalThis.fetch = async (input, init) => {
    const url = String(input?.url || input);
    if (url.includes("api.github.com")) {
      return new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } });
    }
    return origFetch(input, init);
  };
});
after(() => {
  globalThis.fetch = origFetch;
});

function mockKv(init = {}) {
  const store = new Map(Object.entries(init));
  return {
    async get(key) {
      return store.has(key) ? store.get(key) : null;
    },
    async put(key, val) {
      store.set(key, String(val));
    },
    async list() {
      return {
        keys: [...store.keys()].map((name) => ({ name })),
        list_complete: true,
      };
    },
  };
}

function mockAssets() {
  return {
    async fetch() {
      return new Response("gzip-bytes", {
        status: 200,
        headers: { "Content-Length": "10" },
      });
    },
  };
}

function env() {
  return { DOWNLOADS: mockKv(), ASSETS: mockAssets() };
}

async function fetchPath(bindings, path, method = "GET") {
  return worker.fetch(new Request("https://azbot-download-tracker.vibelock.workers.dev" + path, { method }), bindings);
}

test("GET / increments views; GET /download increments downloads; GET /count returns all three", async () => {
  const bindings = env();

  const before = JSON.parse(await (await fetchPath(bindings, "/count")).text());
  assert.deepEqual(before, { project: "azbot", views: 0, downloads: 0, total: 0 });

  const home = await fetchPath(bindings, "/");
  assert.equal(home.status, 200);
  assert.match(home.headers.get("content-type") || "", /text\/html/);

  const afterView = JSON.parse(await (await fetchPath(bindings, "/count")).text());
  assert.equal(afterView.project, "azbot");
  assert.equal(afterView.views, 1);
  assert.equal(afterView.downloads, 0);
  assert.equal(afterView.total, 0);

  const dl = await fetchPath(bindings, "/download?asset=azbot-0.2.0.tar.gz");
  assert.equal(dl.status, 200);

  const afterDl = JSON.parse(await (await fetchPath(bindings, "/count")).text());
  assert.deepEqual(Object.keys(afterDl), ["project", "views", "downloads", "total"]);
  assert.equal(afterDl.project, "azbot");
  assert.equal(afterDl.views, 1);
  assert.equal(afterDl.downloads, 1);
  assert.equal(afterDl.total, 1);

  const again = JSON.parse(await (await fetchPath(bindings, "/count")).text());
  assert.deepEqual(again, afterDl);
});

test("GET /v1/health does not increment views or downloads", async () => {
  const bindings = env();
  const health = await fetchPath(bindings, "/v1/health");
  assert.equal(health.status, 200);
  const count = JSON.parse(await (await fetchPath(bindings, "/count")).text());
  assert.deepEqual(count, { project: "azbot", views: 0, downloads: 0, total: 0 });
});
