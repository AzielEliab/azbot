const OA = "https://aziel-runtime.vibelock.workers.dev/openapi.json";
const MCP = "https://aziel-runtime.vibelock.workers.dev/mcp";
const status = document.getElementById("status");
const skillEl = document.getElementById("skill");
const listEl = document.getElementById("skill-list");
const descEl = document.getElementById("skill-desc");
let selected = null;
let skills = [];

async function load() {
  const t = await fetch("/api/skill").then((r) => r.text());
  skillEl.textContent = t;
  window._skill = t;
  await loadSkills();
}

async function loadSkills() {
  skills = await fetch("/api/skills").then((r) => r.json());
  listEl.innerHTML = "";
  skills.forEach((s) => {
    const li = document.createElement("li");
    li.textContent = s.name;
    li.title = s.description;
    li.dataset.name = s.name;
    li.onclick = () => selectSkill(s);
    listEl.appendChild(li);
  });
  if (selected) {
    const still = skills.find((s) => s.name === selected.name);
    if (still) selectSkill(still);
  }
}

function selectSkill(s) {
  selected = s;
  [...listEl.children].forEach((li) => {
    li.classList.toggle("active", li.dataset.name === s.name);
  });
  descEl.textContent = s.description || "No description.";
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
document.getElementById("import-skill").onclick = async () => {
  const input = document.getElementById("skill-file");
  if (!input.files || !input.files[0]) {
    status.textContent = "Choose a SKILL.md file first.";
    return;
  }
  const fd = new FormData();
  fd.append("file", input.files[0], input.files[0].name);
  const res = await fetch("/api/skills/import", { method: "POST", body: fd });
  const body = await res.json();
  status.textContent = body.ok ? "Added skill " + body.name : (body.error || "Add skill failed");
  await loadSkills();
};
document.getElementById("export-skill").onclick = () => {
  if (!selected) {
    status.textContent = "Pick a skill, then Export skill.";
    return;
  }
  const a = document.createElement("a");
  a.href = "/api/skills/" + encodeURIComponent(selected.name) + "/export";
  a.download = (selected.slug || selected.name) + ".md";
  a.click();
  status.textContent = "Exported " + selected.name;
};
load();
