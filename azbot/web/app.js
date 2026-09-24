const OA = "https://aziel-runtime.vibelock.workers.dev/openapi.json";
const MCP = "https://aziel-runtime.vibelock.workers.dev/mcp";
const status = document.getElementById("status");
const skillEl = document.getElementById("skill");
const listEl = document.getElementById("skill-list");
const descEl = document.getElementById("skill-desc");
let selected = null;
let skills = [];

function say(message) {
  if (status) status.textContent = message;
}

async function load() {
  const response = await fetch("/api/skill");
  const text = await response.text();
  if (skillEl) skillEl.textContent = text;
  window._skill = text;
  await loadSkills();
}

async function loadSkills() {
  if (!listEl) return;
  skills = await fetch("/api/skills").then((r) => r.json());
  listEl.innerHTML = "";
  if (!skills.length) {
    if (descEl) descEl.textContent = "No skill files found yet. Choose a SKILL.md file, then Add skill.";
    return;
  }
  skills.forEach((s) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = s.name;
    button.dataset.name = s.name;
    button.addEventListener("click", () => selectSkill(s));
    li.appendChild(button);
    listEl.appendChild(li);
  });
  if (selected) {
    const still = skills.find((s) => s.name === selected.name);
    if (still) selectSkill(still);
  }
}

function selectSkill(s) {
  selected = s;
  listEl.querySelectorAll("button").forEach((button) => {
    const on = button.dataset.name === s.name;
    button.classList.toggle("active", on);
    button.setAttribute("aria-pressed", on ? "true" : "false");
  });
  if (descEl) descEl.textContent = s.description || "No description on this skill.";
}

function copy(text, label) {
  const done = () => say("Copied " + label + ".");
  const fail = () => say("Clipboard is blocked. Select the " + label + " link on this page and copy it.");
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done, fail);
  } else {
    fail();
  }
}

const copyOa = document.getElementById("copy-oa");
const copyMcp = document.getElementById("copy-mcp");
if (copyOa) copyOa.addEventListener("click", () => copy(OA, "OpenAPI"));
if (copyMcp) copyMcp.addEventListener("click", () => copy(MCP, "MCP"));

const exportBundled = document.getElementById("export");
if (exportBundled) {
  exportBundled.addEventListener("click", () => {
    const blob = new Blob([window._skill || ""], { type: "text/markdown" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "AZBot-SKILL.md";
    a.click();
    say("Exported AZBot-SKILL.md.");
  });
}

const importSkill = document.getElementById("import-skill");
if (importSkill) {
  importSkill.addEventListener("click", async () => {
    const input = document.getElementById("skill-file");
    if (!input || !input.files || !input.files[0]) {
      say("Choose a SKILL.md file, then Add skill.");
      return;
    }
    const fd = new FormData();
    fd.append("file", input.files[0], input.files[0].name);
    const res = await fetch("/api/skills/import", { method: "POST", body: fd });
    const body = await res.json();
    if (body.ok) {
      say("Added " + body.name + ".");
    } else {
      say((body.error || "Could not add that skill.") + " Next: use a SKILL.md file with name and description.");
    }
    await loadSkills();
  });
}

const exportSkill = document.getElementById("export-skill");
if (exportSkill) {
  exportSkill.addEventListener("click", () => {
    if (!selected) {
      say("Pick a skill, then Export skill.");
      return;
    }
    const a = document.createElement("a");
    a.href = "/api/skills/" + encodeURIComponent(selected.name) + "/export";
    a.download = (selected.slug || selected.name) + ".md";
    a.click();
    say("Exported " + selected.name + ".");
  });
}

(function () {
  const file = document.getElementById("aziel-import-json");
  const imp = document.getElementById("aziel-import-json-btn");
  const exp = document.getElementById("aziel-export-json-btn");
  const jsonStatus = document.getElementById("aziel-json-status");
  if (!file || !imp || !exp) return;
  function note(message) {
    if (jsonStatus) jsonStatus.textContent = message;
  }
  function collect() {
    const data = { product: document.title || "", exported_at: new Date().toISOString(), author: "Aziel Eliab" };
    document.querySelectorAll("input, select, textarea").forEach((el) => {
      if (!el.id || el.type === "file" || el.type === "password") return;
      data[el.id] = el.type === "checkbox" ? el.checked : el.value;
    });
    if (window.__azielLastJson && typeof window.__azielLastJson === "object") {
      data.last = window.__azielLastJson;
    }
    return data;
  }
  function apply(obj) {
    if (!obj || typeof obj !== "object") return;
    window.__azielLastJson = obj;
    Object.keys(obj).forEach((k) => {
      if (k === "last" || k === "product" || k === "exported_at" || k === "author") return;
      const el = document.getElementById(k);
      if (!el || el.type === "file" || el.type === "password") return;
      if (el.type === "checkbox") el.checked = !!obj[k];
      else if ("value" in el) el.value = obj[k];
    });
    const ta = document.querySelector("textarea");
    if (ta && obj && !obj[ta.id] && typeof obj === "object") {
      try { if (!ta.value) ta.value = JSON.stringify(obj, null, 2); } catch (e) { /* keep the page usable */ }
    }
  }
  imp.addEventListener("click", () => file.click());
  file.addEventListener("change", () => {
    const f = file.files && file.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        apply(JSON.parse(String(reader.result || "{}")));
        note("Imported " + f.name + ".");
      } catch (e) {
        note("That file is not JSON. Choose a .json file and try again.");
      }
    };
    reader.readAsText(f);
  });
  exp.addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(collect(), null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "session.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 800);
    note("Exported session.json.");
  });
})();

load().catch((err) => say(String(err)));
