/* Reaction chamber — animates one sandhi merge at a time.
 *
 * Nothing here decides algebra. Panels, seams, overlap scalars and their signed
 * permutation expansions are read from chamber-data.json, which bake_chamber.py
 * produces by running SandhiCanon on each input expression.
 */

const el = {
  caseList: document.getElementById("caseList"),
  panels: document.getElementById("panels"),
  arcs: document.getElementById("arcLayer"),
  stage: document.getElementById("stage"),
  stamp: document.getElementById("stamp"),
  phase: document.getElementById("phaseLabel"),
  bloom: document.getElementById("bloom"),
  tally: document.getElementById("tally"),
  engine: document.getElementById("engineExpr"),
  note: document.getElementById("caseNote"),
  play: document.getElementById("playButton"),
  step: document.getElementById("stepButton"),
  reset: document.getElementById("resetButton"),
  speed: document.getElementById("speed"),
};

const PIN_COLORS = ["#4fa3b5", "#a98cc0", "#f2a541", "#7fb069", "#e2564a"];

const state = {
  cases: [],
  caseIndex: 0,
  stepIndex: 0,
  panels: [],
  scalars: [],
  busy: false,
  playing: false,
};

const current = () => state.cases[state.caseIndex];
const towerKey = (tower) => JSON.stringify(tower);
const pairKey = (a, b) => [a, b].sort().join("|");
const wait = (ms) => new Promise((r) => setTimeout(r, ms * (100 / Number(el.speed.value))));

/* ------------------------------------------------------------- rendering */

function pinColor(depth) {
  return PIN_COLORS[depth % PIN_COLORS.length];
}

function ladderMarkup(tower, index) {
  const rungs = tower
    .map((shell, depth) => {
      const slots = shell.nodes
        .map((n) => `<span class="slot" data-sym="${n}" data-panel="${index}">${n}</span>`)
        .join("");
      return `
        <div class="rung">
          <span class="rung-line"></span>
          <span class="pin" data-pin="${shell.pin}" data-panel="${index}"
                style="--pin:${pinColor(depth)}">${shell.pin}</span>
          <span class="slots">${slots}</span>
        </div>`;
    })
    .join("");

  return `<div class="ladder" data-panel="${index}">
      <div class="ladder-title">PANEL ${index + 1} · DEPTH ${tower.length}</div>
      ${rungs}
    </div>`;
}

function render(freshSymbols = []) {
  el.panels.innerHTML = state.panels.map(ladderMarkup).join("");
  freshSymbols.forEach((sym) => {
    el.panels
      .querySelectorAll(`.slot[data-sym="${sym}"]`)
      .forEach((node) => node.classList.add("fresh"));
  });
  clearArcs();
}

function renderTally() {
  el.tally.innerHTML = state.scalars.length
    ? state.scalars.map((s) => `<b>${s}</b>`).join("")
    : "<em>1</em>";
}

function renderCaseRail() {
  el.caseList.innerHTML = state.cases
    .map(
      (c, i) => `<button data-index="${i}" class="${i === state.caseIndex ? "active" : ""}">
        <b>${c.title}</b><span>${c.steps.length} MERGE${c.steps.length > 1 ? "S" : ""}</span>
      </button>`
    )
    .join("");
}

function setPhase(text) {
  el.phase.textContent = text;
}

/* ------------------------------------------------------------------ arcs */

function clearArcs() {
  el.arcs.innerHTML = "";
}

function drawArcs(pins, seams) {
  clearArcs();
  const stageBox = el.stage.getBoundingClientRect();
  const arcs = new Map();

  pins.forEach((pinNode) => {
    const p = pinNode.getBoundingClientRect();
    const px = p.left + p.width / 2 - stageBox.left;
    const py = p.top + p.height / 2 - stageBox.top;

    seams.forEach((slot) => {
      const s = slot.getBoundingClientRect();
      const sx = s.left + s.width / 2 - stageBox.left;
      const sy = s.top + s.height / 2 - stageBox.top;
      const lift = Math.max(30, Math.abs(sx - px) * 0.35);

      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", `M ${px} ${py} Q ${(px + sx) / 2} ${(py + sy) / 2 - lift} ${sx} ${sy}`);
      el.arcs.append(path);
      path.style.setProperty("--len", path.getTotalLength());
      path.classList.add("drawn");

      const key = pairKey(pinNode.dataset.pin, slot.dataset.sym);
      if (!arcs.has(key)) arcs.set(key, []);
      arcs.get(key).push(path);
    });
  });

  return arcs;
}

/* ----------------------------------------------------------------- bloom */

function renderBloom(seam) {
  const { rows, cols } = seam;
  if (!rows.length || !cols.length) {
    el.bloom.innerHTML = '<p class="bloom-empty">This merge produced no overlap scalar.</p>';
    return new Map();
  }

  const cells = new Map();
  const head = ['<div class="cell head"></div>', ...cols.map((c) => `<div class="cell head">${c}</div>`)];
  const body = rows
    .map((r) => {
      const rowCells = cols.map((c) => `<div class="cell" data-key="${pairKey(r, c)}">${r}|${c}</div>`);
      return [`<div class="cell head">${r}</div>`, ...rowCells].join("");
    })
    .join("");

  const perms = seam.terms
    .map(
      (t, i) => `<div class="perm ${t.sign > 0 ? "plus" : "minus"}" data-term="${i}">
        <i>${t.sign > 0 ? "+" : "−"}</i>${t.factors.map((f) => `(${f})`).join(" ")}
      </div>`
    )
    .join("");

  el.bloom.innerHTML = `
    <div class="matrix" style="grid-template-columns: repeat(${cols.length + 1}, auto)">
      ${head.join("")}${body}
    </div>
    ${seam.terms.length ? `<div class="perms">${perms}</div>` : ""}`;

  el.bloom.querySelectorAll(".cell[data-key]").forEach((c) => cells.set(c.dataset.key, c));
  return cells;
}

async function playBloom(seam, cells, arcs) {
  for (let i = 0; i < seam.terms.length; i += 1) {
    const term = seam.terms[i];
    const row = el.bloom.querySelector(`.perm[data-term="${i}"]`);
    const keys = term.factors.map((f) => pairKey(...f.split("|")));

    row?.classList.add("lit");
    keys.forEach((k) => {
      cells.get(k)?.classList.add("lit");
      (arcs.get(k) || []).forEach((p) => p.classList.add("active"));
    });

    await wait(240);

    row?.classList.remove("lit");
    keys.forEach((k) => {
      cells.get(k)?.classList.remove("lit");
      (arcs.get(k) || []).forEach((p) => p.classList.remove("active"));
    });
    await wait(60);
  }
}

/* ------------------------------------------------------------------ step */

function consumedIndices(step) {
  const afterKeys = step.panelsAfter.map(towerKey);
  const used = new Set();
  const consumed = [];

  step.panelsBefore.forEach((tower, i) => {
    const key = towerKey(tower);
    const match = afterKeys.findIndex((k, j) => k === key && !used.has(j));
    if (match === -1) consumed.push(i);
    else used.add(match);
  });

  return consumed.length ? consumed : step.panelsBefore.map((_, i) => i);
}

function seamSymbols(step, consumed) {
  const symbols = new Set([...step.seam.rows, ...step.seam.cols]);
  const slotSets = consumed.map(
    (i) => new Set(step.panelsBefore[i].flatMap((shell) => shell.nodes))
  );
  return [...symbols].filter((s) => slotSets.every((set) => set.has(s)));
}

function freshSymbols(step, consumed) {
  const before = new Set(step.panelsBefore[consumed[0]].flatMap((s) => s.nodes));
  const after = step.panelsAfter.flatMap((t) => t.flatMap((s) => s.nodes));
  return [...new Set(after.filter((s) => !before.has(s)))];
}

async function runStep() {
  const c = current();
  if (state.busy || state.stepIndex >= c.steps.length) return;

  state.busy = true;
  syncControls();

  const step = c.steps[state.stepIndex];
  state.panels = step.panelsBefore;
  render();

  const consumed = consumedIndices(step);
  const seams = seamSymbols(step, consumed);
  const ladders = consumed.map((i) => el.panels.querySelector(`.ladder[data-panel="${i}"]`));

  setPhase("DOCKING");
  ladders.forEach((l, i) => l?.classList.add("docking", i === 0 ? "dock-left" : "dock-right"));
  el.engine.textContent = step.after;
  await wait(480);

  setPhase("SEAM LOCK");
  const seamNodes = [];
  consumed.forEach((i) => {
    seams.forEach((sym) => {
      el.panels
        .querySelectorAll(`.slot[data-panel="${i}"][data-sym="${sym}"]`)
        .forEach((n) => {
          n.classList.add("seam", "pulsing");
          seamNodes.push(n);
        });
    });
  });
  await wait(420);

  let arcs = new Map();
  let cells = new Map();

  if (!step.zero) {
    setPhase("PAIRING");
    consumed.forEach((i) =>
      el.panels.querySelectorAll(`.pin[data-panel="${i}"]`).forEach((p) => p.classList.add("paired"))
    );
    // Both ladders carry the same pin lineage, so one set of anchors is enough.
    const pinNodes = [...el.panels.querySelectorAll(`.pin[data-panel="${consumed[0]}"]`)];
    arcs = drawArcs(pinNodes, seamNodes);
    await wait(420);

    setPhase("DETERMINANT");
    cells = renderBloom(step.seam);
    await playBloom(step.seam, cells, arcs);

    el.bloom.insertAdjacentHTML("beforeend", `<div class="bloom-total">${step.coeff}</div>`);
    state.scalars.push(step.coeff);
    renderTally();
    el.stage.classList.add("flash");
    setTimeout(() => el.stage.classList.remove("flash"), 500);
    await wait(360);
  }

  if (step.zero) {
    setPhase("ANNIHILATION");
    el.bloom.innerHTML =
      '<p class="bloom-empty">A symbol repeats inside the wedge. The whole product is zero — no scalar survives.</p>';
    el.stage.classList.add("zero");
    el.panels.querySelectorAll(".ladder").forEach((l) => l.classList.add("shatter"));
    el.stamp.hidden = false;
    el.stamp.textContent = "= 0";
    state.scalars = ["0"];
    renderTally();
    await wait(620);
    el.stage.classList.remove("zero");
    state.panels = [];
    state.stepIndex += 1;
    state.busy = false;
    syncControls();
    setPhase("ZERO");
    return;
  }

  setPhase("FUSING");
  clearArcs();
  ladders.forEach((l) => l?.classList.add("consumed"));
  await wait(360);

  state.panels = step.panelsAfter;
  state.stepIndex += 1;
  render(freshSymbols(step, consumed));
  el.panels.querySelectorAll(".ladder").forEach((l) => l.classList.add("arriving"));
  await wait(520);

  setPhase(state.stepIndex >= c.steps.length ? "NORMAL FORM" : "READY");
  if (state.stepIndex >= c.steps.length) el.engine.textContent = c.result.expr;

  state.busy = false;
  syncControls();
}

async function runAll() {
  if (state.playing) return;
  state.playing = true;
  syncControls();
  while (state.stepIndex < current().steps.length) {
    await runStep();
    await wait(280);
  }
  state.playing = false;
  syncControls();
}

/* --------------------------------------------------------------- control */

function syncControls() {
  const done = state.stepIndex >= current().steps.length;
  el.step.disabled = state.busy || state.playing || done;
  el.play.disabled = state.busy || state.playing || done;
}

function loadCase(index) {
  state.caseIndex = index;
  state.stepIndex = 0;
  state.scalars = [];
  state.panels = current().input.panels;
  state.playing = false;
  state.busy = false;

  el.stamp.hidden = true;
  el.bloom.innerHTML = '<p class="bloom-empty">The pairing matrix appears when a seam locks.</p>';
  el.engine.textContent = current().input.expr;
  el.note.textContent = current().note;
  setPhase("READY");

  renderCaseRail();
  renderTally();
  render();
  syncControls();
}

el.caseList.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (button && !state.busy && !state.playing) loadCase(Number(button.dataset.index));
});
el.step.addEventListener("click", runStep);
el.play.addEventListener("click", runAll);
el.reset.addEventListener("click", () => {
  if (!state.busy) loadCase(state.caseIndex);
});

window.chamber = { state, loadCase, runStep, runAll };

fetch("chamber-data.json")
  .then((r) => r.json())
  .then((data) => {
    state.cases = data;
    loadCase(0);
  })
  .catch(() => {
    el.panels.innerHTML =
      '<p style="color:#f1ede0;font:12px monospace">chamber-data.json missing — run bake_chamber.py</p>';
  });
