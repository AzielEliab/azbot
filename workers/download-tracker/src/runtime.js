/** AZBot hosted runtime. Skill markdown only. /v1 never touches DOWNLOADS KV. */
import { SKILL } from "./skill-embed.js";

const EXAMPLE_PAYLOAD = {};

const LIMITATION =
  "AZBot is a skill, not a foundation model, not a kernel, not a VPN, and not a paid-key proxy. Jeeves is not sovereign. Call aziel-runtime.";
const CATALOG = "https://aziel-runtime.vibelock.workers.dev";

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
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
  try { return new URL(request.url).origin; } catch { return "https://azbot-download-tracker.vibelock.workers.dev"; }
}

export async function handleRuntimeApi(request, url) {
  const path = url.pathname.replace(/\/+$/, "") || "/";
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
      info: { title: "AZBot", version: "0.2.0", description: LIMITATION },
      paths: {
              "/v1/example": { get: { operationId: "azbotExample", summary: "Sample JSON payload. Does not increment downloads.", responses: { "200": { description: "OK" } } } },
      "/v1/health": { get: { operationId: "azbot_health", summary: "Liveness. Does not increment download KV." } },
        "/v1/skill": { get: { operationId: "azbot_skill", summary: "Return AZBot skill markdown. Does not increment download KV." } },
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
<p>OpenAPI: <a href="${origin}/openapi.json" style="color:#c9d4ff">${origin}/openapi.json</a></p>
<pre>curl -A Mozilla/5.0 ${origin}/v1/health
curl -A Mozilla/5.0 ${origin}/v1/skill</pre>
<p>Catalog: <a href="${CATALOG}/" style="color:#c9d4ff">${CATALOG}</a></p>
</body>`);
  }
  if (path.startsWith("/v1/") || path === "/v1") {
    return json({ error: "not found", hint: "GET /v1/health /v1/skill", limitation: LIMITATION }, 404);
  }
  return null;
}
