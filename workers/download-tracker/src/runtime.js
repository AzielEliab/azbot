/** AZBot hosted runtime. Skill markdown only. /v1 never touches DOWNLOADS KV. */

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

const SKILL = "---\nname: AZBot\ndescription: Use this when Grok, ChatGPT, Venice, or any assistant should call Aziel Eliab public engines via the aziel-runtime OpenAPI/MCP catalog.\n---\n\n# AZBot\n\nAZBot is a **skill**. It is not a new foundation model, not a kernel, not a VPN, not a paid-key proxy, and not Jeeves-as-sovereign.\n\nOne catalog for every public Aziel Eliab engine:\n\n- Catalog: https://aziel-runtime.vibelock.workers.dev/\n- OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json\n- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`\n\nAlways send a normal `User-Agent` (for example `Mozilla/5.0`). Cloudflare Workers may 403 empty agents.\n\n## Rules\n\n1. Call the catalog. Do not invent scores, overlays, receipts, or health.\n2. Repeat the product banner. Never claim forensic proof, a lab spectrometer, a real UV lamp, OCR truth, a kernel, a VPN, legal advice, lie detection, call intercept, or hosted AZAI spending paid keys.\n3. Lamb Lens order: Peace \u2192 Clarity \u2192 Service. Jeeves is not sovereign.\n4. AZ-CLCE Type D is a **label only**, not a finding of malice.\n5. SpectralLock overlays are advisory visualization. The human still reads the page.\n6. ForgeReceipts is not legal advice.\n7. Forks are welcome and always allowed. Apache-2.0.\n\n## How to call\n\n```bash\ncurl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/health\ncurl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/azclce/score \\\n  -H 'content-type: application/json' \\\n  -d '{\"r\":\"login button blue\",\"d\":\"login form submits\",\"p\":\"login button submits\"}'\n```\n\nMCP tools are named `{slug}_{op}` (example `azclce_score`, `spectrallock_overlay`, `azai_lamb_check`).\n\nGrok: import the OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.\n\n## Products (honest one-liners)\n\n| slug | name | do not claim |\n|------|------|----------------|\n| vibelock | VibeLock | courtroom audio proof |\n| veillock | VeilLock | FaceTime/Zoom intercept |\n| codelock | CodeLock | that meaning changed |\n| godlock | GodLock | a VPN or ghost net |\n| shadowlock | ShadowLock | OS hooks / process intercept |\n| temporallock | TemporalLock | legal chain of custody |\n| forgereceipts | ForgeReceipts | legal advice / court filing |\n| decisiongate | DecisionGATE | moral authority |\n| zsolver | ZionPattern Solver | a solved case; cap is 75% |\n| azos | AZ-OS | a kernel or remote shell |\n| glossafilter | Glossa Filter | that tools hold opinions |\n| miragegrid | MirageGrid | anonymity / VPN |\n| staticclock | StaticClock | a scheduler you set |\n| chronolock | ChronoLock | targeting or virality |\n| postking | Post-King Chess | that the goal is to win |\n| azclce | AZ-CLCE | intent or malice |\n| ark | The ARK | a kernel; hosted unlock |\n| azai | AZAI | a new model; hosted paid proxy |\n| spectrallock | SpectralLock | spectrometer / forensic ink |\n";

export async function handleRuntimeApi(request, url) {
  const path = url.pathname.replace(/\/+$/, "") || "/";
  if (path === "/v1/health" && request.method === "GET") {
    return json({
      ok: true,
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
