const OA = "https://aziel-runtime.vibelock.workers.dev/openapi.json";
const MCP = "https://aziel-runtime.vibelock.workers.dev/mcp";
const status = document.getElementById("status");
const skillEl = document.getElementById("skill");
async function load() {
  const t = await fetch("/api/skill").then((r) => r.text());
  skillEl.textContent = t;
  window._skill = t;
}
function copy(text, label) {
  navigator.clipboard.writeText(text).then(() => { status.textContent = "Copied " + label; });
}
document.getElementById("copy-oa").onclick = () => copy(OA, "OpenAPI");
document.getElementById("copy-mcp").onclick = () => copy(MCP, "MCP");
document.getElementById("export").onclick = () => {
  const blob = new Blob([window._skill || ""], { type: "text/markdown" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "AZBot-SKILL.md";
  a.click();
  status.textContent = "Exported AZBot-SKILL.md";
};
load();
