import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import worker from "../src/index.js";
import { meshPointer, runMeshProxy } from "../src/mesh.js";

const origFetch = globalThis.fetch;
const seen = [];

function meshOk() {
  return {
    ok: true,
    code: "MESH-OK",
    enabled: false,
    radios: "off",
    mesh_default: "off",
    spec: "QNM-BUILD-1.0",
    rollup: { live: 0, locked: 0, isolated: 0 },
    live_nodes: 0,
    author: "Aziel Eliab",
  };
}

function jsonRes(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

const azielRuntime = {
  async fetch(input, init) {
    const req = input instanceof Request ? input : new Request(input, init);
    const url = new URL(req.url);
    seen.push({ method: req.method, href: url.href, path: url.pathname });
    if ((url.pathname === "/v1/mesh" || url.pathname === "/v1/mesh/status") && req.method === "GET") {
      return jsonRes(meshOk());
    }
    if (url.pathname === "/v1/mesh/enable" && req.method === "POST") {
      const body = await req.json();
      if (!body.bearer) return jsonRes({ ok: false, code: "MESH-NEED-BEARER", enabled: false }, 400);
      return jsonRes({ ok: true, code: "MESH-OK", enabled: true, radios: "on", bearers: [body.bearer] });
    }
    if (url.pathname === "/v1/mesh/join" && req.method === "POST") {
      return jsonRes({ ok: false, code: "MESH-OFF", enabled: false }, 409);
    }
    return jsonRes({ error: "not found" }, 404);
  },
};

before(() => {
  seen.length = 0;
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

function env() {
  return { DOWNLOADS: mockKv(), ASSETS: { async fetch() { return new Response("x"); } }, AZIEL_RUNTIME: azielRuntime };
}

async function fetchPath(bindings, path, method = "GET", body) {
  const init = { method, headers: { "User-Agent": "Mozilla/5.0" } };
  if (body !== undefined) {
    init.headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }
  return worker.fetch(new Request("https://azbot-download-tracker.vibelock.workers.dev" + path, init), bindings);
}

test("mesh pointer stays default OFF", () => {
  const p = meshPointer();
  assert.equal(p.enabled_default, false);
  assert.equal(p.node_gate, false);
  assert.equal(p.rollup, "live|locked|isolated");
  assert.equal(p.anon_broadcast_publish_path, false);
});

test("GET /v1/mesh/status returns MESH-OK enabled:false", async () => {
  const bindings = env();
  const res = await fetchPath(bindings, "/v1/mesh/status");
  assert.equal(res.status, 200);
  const data = JSON.parse(await res.text());
  assert.equal(data.ok, true);
  assert.equal(data.code, "MESH-OK");
  assert.equal(data.enabled, false);
  assert.deepEqual(data.rollup, { live: 0, locked: 0, isolated: 0 });
});

test("GET /v1/mesh never enables", async () => {
  const bindings = env();
  const res = await fetchPath(bindings, "/v1/mesh");
  const data = JSON.parse(await res.text());
  assert.equal(data.enabled, false);
  assert.equal(data.code, "MESH-OK");
});

test("POST /v1/mesh/enable without bearer stays OFF", async () => {
  const bindings = env();
  const res = await fetchPath(bindings, "/v1/mesh/enable", "POST", {});
  assert.equal(res.status, 400);
  const data = JSON.parse(await res.text());
  assert.equal(data.code, "MESH-NEED-BEARER");
  assert.notEqual(data.enabled, true);
});

test("POST /v1/mesh/join while OFF stays OFF", async () => {
  const bindings = env();
  const res = await fetchPath(bindings, "/v1/mesh/join", "POST", { product: "azbot" });
  const data = JSON.parse(await res.text());
  assert.equal(data.code, "MESH-OFF");
  assert.notEqual(data.enabled, true);
});

test("unknown mesh path is MESH-UNKNOWN", async () => {
  const bindings = env();
  const res = await fetchPath(bindings, "/v1/mesh/gate");
  assert.equal(res.status, 404);
  const data = JSON.parse(await res.text());
  assert.equal(data.code, "MESH-UNKNOWN");
});

test("GET /v1/mesh/status does not increment views", async () => {
  const bindings = env();
  await fetchPath(bindings, "/v1/mesh/status");
  const count = JSON.parse(await (await fetchPath(bindings, "/count")).text());
  assert.deepEqual(count, { project: "azbot", views: 0, downloads: 0, total: 0 });
});

test("homepage HTML has Live Nodes strip and no Node Gate", async () => {
  const bindings = env();
  const home = await fetchPath(bindings, "/");
  const html = await home.text();
  assert.match(html, /id="meshStrip"/);
  assert.match(html, /Live Nodes/);
  assert.match(html, /QNM-BUILD-1.0/);
  assert.match(html, /No Node Gate/);
  assert.doesNotMatch(html, /id="node-gate"/);
});

test("runMeshProxy uses AZIEL_RUNTIME binding", async () => {
  seen.length = 0;
  const out = await runMeshProxy(env(), new Request("https://azbot-download-tracker.vibelock.workers.dev/v1/mesh"), "/v1/mesh");
  assert.equal(out.status, 200);
  assert.equal(out.data.code, "MESH-OK");
  assert.equal(out.data.enabled, false);
  assert.ok(seen.some((s) => s.method === "GET" && s.path === "/v1/mesh"));
});

test("GET /mcp and /openapi.json point at suite mesh", async () => {
  const bindings = env();
  const mcp = JSON.parse(await (await fetchPath(bindings, "/mcp")).text());
  assert.equal(mcp.mesh.enabled_default, false);
  assert.equal(mcp.mesh.fraggate_slug, "mesh");
  const spec = JSON.parse(await (await fetchPath(bindings, "/openapi.json")).text());
  assert.ok(spec.paths["/v1/mesh"]);
  assert.ok(spec.paths["/v1/mesh/status"]);
});
