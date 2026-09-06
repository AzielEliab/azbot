/** AZBot hosted runtime. Skill markdown only. /v1 never touches DOWNLOADS KV.
 * `/v1/fraggate/*`, `/v1/runtime/*`, and `/v1/mesh/*` PROXY to aziel-runtime
 * via AZIEL_RUNTIME (or HTTPS fallback). Local ops are /v1/{health,skill,example}.
 * Author: Aziel Eliab only.
 */
import { SKILL } from "./skill-embed.js";
import { classifyV1Path, doorTargetUrl } from "./door.js";
import { isMeshPath, meshOpenApiPaths, meshPointer, runMeshProxy } from "./mesh.js";

const EXAMPLE_PAYLOAD = {};

const LIMITATION =
  "AZBot is a skill, not a foundation model, not a kernel, not a VPN, and not a paid-key proxy. Jeeves is not sovereign. Call aziel-runtime.";
const CATALOG = "https://aziel-runtime.vibelock.workers.dev";
const HOST = "https://azbot-download-tracker.vibelock.workers.dev";

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, HEAD, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, Authorization, X-Aziel-Runtime-Token, User-Agent",
  };
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders() },
  });
}

function html(body) {
  return new Response(body, {
    headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders() },
  });
}

function originOf(request) {
  try { return new URL(request.url).origin; } catch { return HOST; }
}

function runtimeFetcher(env) {
  if (env && env.AZIEL_RUNTIME && typeof env.AZIEL_RUNTIME.fetch === "function") return env.AZIEL_RUNTIME;
  return null;
}

async function proxyDoor(request, url, env) {
  const dest = doorTargetUrl(url.pathname, request.url, env);
  if (!dest) {
    return json({ ok: false, error: "not a door path", path: url.pathname, door: "fraggate" }, 404);
  }
  const headers = new Headers();
  const pass = ["content-type", "accept", "authorization", "user-agent", "x-aziel-runtime-token"];
  for (const name of pass) {
    const v = request.headers.get(name);
    if (v) headers.set(name, v);
  }
  if (!headers.has("User-Agent")) headers.set("User-Agent", "Mozilla/5.0 AZBot/0.2.0");
  let body = null;
  if (request.method !== "GET" && request.method !== "HEAD") {
    body = await request.arrayBuffer();
  }
  const initFor = () => {
    const init = { method: request.method, headers, redirect: "follow" };
    if (body) init.body = body;
    return init;
  };
  try {
    const fetcher = runtimeFetcher(env);
    let res = null;
    if (fetcher) {
      try {
        res = await fetcher.fetch(dest, initFor());
      } catch {
        res = null;
      }
    }
    if (!res || res.status === 503) {
      res = await fetch(dest, initFor());
    }
    const outHeaders = new Headers(res.headers);
    for (const [k, v] of Object.entries(corsHeaders())) outHeaders.set(k, v);
    outHeaders.set("X-Aziel-Door", "proxy");
    outHeaders.set("X-Aziel-Door-Origin", dest);
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers: outHeaders });
  } catch (exc) {
    return json({
      ok: false,
      error: "fraggate_proxy_failed",
      detail: String(exc).slice(0, 240),
      origin: dest,
      agent_path: CATALOG + "/v1/fraggate/call",
      door: "fraggate",
      slug: "azbot",
    }, 502);
  }
}

function mcpPointer() {
  return {
    ok: true,
    product: "azbot",
    pointer: true,
    identity: "Aziel Eliab only",
    author: "Aziel Eliab",
    catalog_mcp: CATALOG + "/mcp",
    catalog_openapi: CATALOG + "/openapi.json",
    worker_openapi: HOST + "/openapi.json",
    this_worker_mcp: HOST + "/mcp",
    agent_path: CATALOG + "/v1/fraggate/call",
    body: { slug: "azbot", op: "health", payload: {} },
    mesh: meshPointer(),
    mesh_body: { slug: "mesh", op: "status", payload: {} },
    note: "This Worker /mcp is a pointer, not a second MCP. Canonical catalog MCP is POST " + CATALOG + "/mcp (FragGate slug azbot). Catalog MCP mesh_* + FragGate slug=mesh. This Worker /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. QNM-BUILD-1.0 live|locked|isolated. No Node Gate. No auto-heal. Not anonymity. Author: Aziel Eliab only.",
    kv_increment: false,
  };
}

export async function handleRuntimeApi(request, url, env) {
  const path = url.pathname.replace(/\/+$/, "") || "/";

  if (path === "/mcp") {
    return json(mcpPointer());
  }

  if (isMeshPath(path) || path === "/v1/mesh") {
    const out = await runMeshProxy(env, request, path + (url.search || ""));
    if (request.method === "HEAD") {
      return new Response(null, { status: out.status, headers: corsHeaders() });
    }
    return json(out.data, out.status);
  }

  const classified = classifyV1Path(url.pathname);
  if (classified.kind === "door") {
    return proxyDoor(request, url, env);
  }

  if (path === "/v1/health" && request.method === "GET") {
    return json({
      ok: true, author: "Aziel Eliab",
      product: "azbot",
      version: "0.2.0",
      runtime: true,
      kv_increment: false,
      is_skill: true,
      not_a_model: true,
      limitation: LIMITATION,
      catalog: CATALOG,
      mesh: meshPointer(),
      note: "Suite mesh /v1/mesh/* PROXY to aziel-runtime. Default OFF. QNM-BUILD-1.0 live|locked|isolated. No Node Gate. No auto-heal.",
    });
  }
  if ((path === "/v1/example" || path === "/v1/example/") && (request.method === "GET" || request.method === "HEAD")) {
    return json({
      ok: true,
      product: "azbot",
      author: "Aziel Eliab",
      example: EXAMPLE_PAYLOAD,
      note: "Sample payload only. Does not increment downloads.",
    });
  }

  if (path === "/v1/skill" && request.method === "GET") {
    return new Response(SKILL, {
      status: 200,
      headers: {
        "Content-Type": "text/markdown; charset=utf-8",
        "Cache-Control": "private, no-store",
        ...corsHeaders(),
      },
    });
  }
  if (path === "/openapi.json" && request.method === "GET") {
    const origin = originOf(request);
    return json({
      openapi: "3.1.0",
      info: {
        title: "AZBot",
        version: "0.2.0",
        description: LIMITATION + " Suite mesh /v1/mesh/* PROXY to aziel-runtime (AZIEL_RUNTIME). Default OFF. QNM-BUILD-1.0 live|locked|isolated. No Node Gate. No auto-heal. Not anonymity. Aziel Eliab only.",
      },
      paths: {
        "/v1/example": { get: { operationId: "azbotExample", summary: "Sample JSON payload. Does not increment downloads.", responses: { "200": { description: "OK" } } } },
        "/v1/health": { get: { operationId: "azbot_health", summary: "Liveness. Does not increment download KV." } },
        "/v1/skill": { get: { operationId: "azbot_skill", summary: "Return AZBot skill markdown. Does not increment download KV." } },
        "/mcp": { get: { operationId: "azbot_mcp_pointer", summary: "OpenAPI/MCP pointer (catalog MCP + FragGate slug=mesh). Not a second MCP." } },
        ...meshOpenApiPaths(),
      },
      servers: [{ url: origin }],
    });
  }
  if ((path === "/ai" || url.pathname === "/ai/") && request.method === "GET") {
    const origin = originOf(request);
    return html(`<!doctype html><meta charset=utf-8><title>AZBot AI</title>
<body style="font:16px/1.45 system-ui;max-width:44rem;margin:3rem auto;background:#0e1014;color:#e8eaef">
<h1>AZBot runtime</h1>
<p>${LIMITATION}</p>
<p>Suite mesh: <code>GET ${origin}/v1/mesh</code> PROXY to aziel-runtime. Default OFF. QNM-BUILD-1.0 live|locked|isolated. No Node Gate. No auto-heal. Not anonymity. Catalog MCP <code>mesh_*</code> + FragGate <code>slug=mesh</code>. Author: Aziel Eliab only.</p>
<p>OpenAPI: <a href="${origin}/openapi.json" style="color:#c9d4ff">${origin}/openapi.json</a></p>
<pre>curl -A Mozilla/5.0 ${origin}/v1/health
curl -A Mozilla/5.0 ${origin}/v1/skill
curl -A Mozilla/5.0 ${origin}/v1/mesh</pre>
<p>Catalog: <a href="${CATALOG}/" style="color:#c9d4ff">${CATALOG}</a> · MCP pointer: <a href="${origin}/mcp" style="color:#c9d4ff">${origin}/mcp</a></p>
</body>`);
  }
  if (path.startsWith("/v1/") || path === "/v1") {
    return json({
      error: "not found",
      hint: "GET /v1/health /v1/skill /v1/example GET /v1/mesh GET /v1/fraggate/list POST /mcp",
      limitation: LIMITATION,
      mesh: meshPointer(),
    }, 404);
  }
  return null;
}
