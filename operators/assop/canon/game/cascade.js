/* Orbital Cascade — a playable reading of nested sandhi.
 *
 * A tower is a nested contraction tower:
 *   d1⌋(a… ∧ d2⌋(b… ∧ d3⌋(c…)))
 * Two towers with the same pin lineage and a shared deep core fuse: the shared
 * core contracts out as a scalar (the Capelli overlap) and the survivors merge
 * into one wider tower, which may immediately fuse again — the cascade.
 */

const OUTER_A = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"];
const OUTER_B = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9"];

const LEVELS = [
  {
    label: "SHELL 01",
    title: "Collapse six shared cores",
    goal: 6,
    lineages: [["d1", "d2"]],
    shellPools: [OUTER_A],
    corePool: ["c1", "c2", "c3", "c4", "c5"],
    coreSize: [2, 3],
  },
  {
    label: "SHELL 02",
    title: "Go one shell deeper",
    goal: 8,
    lineages: [["d1", "d2", "d3"]],
    shellPools: [OUTER_A, OUTER_B],
    corePool: ["c1", "c2", "c3", "c4", "c5", "c6"],
    coreSize: [2, 3],
  },
  {
    label: "SHELL 03",
    title: "Two lineages, one cascade",
    goal: 10,
    lineages: [["d1", "d2", "d3"], ["e1", "e2", "e3"]],
    shellPools: [OUTER_A, OUTER_B],
    corePool: ["c1", "c2", "c3", "c4", "c5", "c6", "c7"],
    coreSize: [3, 4],
  },
];

const PIN_COLORS = {
  d1: "#4d8b98", d2: "#9a7fb0", d3: "#f2a541",
  e1: "#6f9068", e2: "#c9788c", e3: "#f2a541",
};

const SLOTS = 6;

const state = {
  levelIndex: 0,
  towers: [],
  selected: null,
  score: 0,
  chain: 1,
  collapses: 0,
  busy: false,
  nextId: 1,
};

const el = {
  board: document.getElementById("board"),
  sparks: document.getElementById("sparkLayer"),
  score: document.getElementById("score"),
  chain: document.getElementById("chain"),
  chainBox: document.querySelector(".hud-chain"),
  depth: document.getElementById("depth"),
  status: document.getElementById("statusLine"),
  scalarCard: document.getElementById("scalarCard"),
  levelLabel: document.getElementById("levelLabel"),
  goalTitle: document.getElementById("goalTitle"),
  goalBar: document.getElementById("goalBar"),
  goalText: document.getElementById("goalText"),
  reset: document.getElementById("resetButton"),
  banner: document.getElementById("banner"),
  bannerMark: document.getElementById("bannerMark"),
  bannerKicker: document.getElementById("bannerKicker"),
  bannerTitle: document.getElementById("bannerTitle"),
  bannerText: document.getElementById("bannerText"),
  bannerButton: document.getElementById("bannerButton"),
};

/* ---------------------------------------------------------------- model */

const level = () => LEVELS[state.levelIndex];
const pick = (list) => list[Math.floor(Math.random() * list.length)];
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function sample(pool, count) {
  const copy = [...pool];
  const out = [];
  while (out.length < count && copy.length) {
    out.push(copy.splice(Math.floor(Math.random() * copy.length), 1)[0]);
  }
  return out.sort();
}

function makeTower() {
  const cfg = level();
  const lineage = pick(cfg.lineages);
  const [minCore, maxCore] = cfg.coreSize;
  const coreCount = minCore + Math.floor(Math.random() * (maxCore - minCore + 1));

  const shells = lineage.slice(0, -1).map((pin, i) => ({
    pin,
    nodes: sample(cfg.shellPools[i] || cfg.shellPools[0], 2),
  }));

  shells.push({ pin: lineage[lineage.length - 1], nodes: sample(cfg.corePool, coreCount), core: true });
  return { id: state.nextId++, lineage: lineage.join("·"), shells };
}

const coreOf = (tower) => tower.shells[tower.shells.length - 1].nodes;
const power = (tower) => tower.shells.reduce((n, s) => n + s.nodes.length, 0);
const shared = (a, b) => coreOf(a).filter((s) => coreOf(b).includes(s));
const sameSet = (a, b) => a.length === b.length && a.every((s) => b.includes(s));

const outerClash = (a, b) =>
  a.shells.slice(0, -1).some((shell, i) => shell.nodes.some((n) => b.shells[i].nodes.includes(n)));

function relation(a, b) {
  if (!a || !b || a.id === b.id) return "none";
  if (a.lineage !== b.lineage) return "none";
  if (!shared(a, b).length) return "none";
  if (sameSet(coreOf(a), coreOf(b)) || outerClash(a, b)) return "pauli";
  return "dock";
}

/* Sandhi: the shared core symbols contract out into the scalar, the surviving
 * symbols of both towers wedge together into one residual tower. */
function fuse(a, b) {
  const overlap = shared(a, b);
  const shells = a.shells.map((shell, i) => {
    const merged = [...new Set([...shell.nodes, ...b.shells[i].nodes])].sort();
    return { ...shell, nodes: shell.core ? merged.filter((s) => !overlap.includes(s)) : merged };
  });
  if (!shells[shells.length - 1].nodes.length) return null;
  return { id: state.nextId++, lineage: a.lineage, shells };
}

function zeroReason(a, b) {
  return outerClash(a, b) ? "repeated shell symbol" : "repeated core";
}

function scalarExpression(a, b, overlap) {
  const pins = a.shells.map((s) => s.pin).join("∧");
  return `(${pins}) | (${overlap.join("∧")})`;
}

function hasMove() {
  for (let i = 0; i < state.towers.length; i += 1) {
    for (let j = i + 1; j < state.towers.length; j += 1) {
      if (relation(state.towers[i], state.towers[j]) === "dock") return true;
    }
  }
  return false;
}

/* ----------------------------------------------------------------- view */

function towerMarkup(tower) {
  const partner = state.selected && state.selected.id !== tower.id
    ? relation(state.selected, tower)
    : "none";
  const overlap = state.selected ? shared(state.selected, tower) : [];

  const shells = tower.shells
    .map((shell, i) => {
      const mirror = state.selected ? state.selected.shells[i].nodes : [];
      const chips = shell.nodes
        .map((node) => {
          if (partner === "none") return `<span class="chip">${node}</span>`;
          if (shell.core && overlap.includes(node)) return `<span class="chip shared">${node}</span>`;
          if (!shell.core && mirror.includes(node)) return `<span class="chip clash">${node}</span>`;
          return `<span class="chip">${node}</span>`;
        })
        .join("");
      return `
        <div class="shell${shell.core ? " core" : ""}">
          <span class="shell-pin" style="--pin-color:${PIN_COLORS[shell.pin] || "#4d8b98"}">${shell.pin}</span>
          <div class="chips">${chips}</div>
        </div>`;
    })
    .join("");

  const classes = ["tower"];
  if (state.selected && state.selected.id === tower.id) classes.push("selected");
  if (partner === "dock") classes.push("dockable");
  if (partner === "pauli") classes.push("zeroable");

  const badge = partner === "pauli" ? '<span class="zero-badge">= 0</span>' : "";

  return `
    <div class="${classes.join(" ")}" data-id="${tower.id}" role="button" tabindex="0">
      ${badge}
      <div class="tower-head">
        <span>${tower.lineage}</span>
        <span class="tower-power">${power(tower)}◇</span>
      </div>
      ${shells}
    </div>`;
}

function render() {
  el.board.innerHTML = state.towers.map(towerMarkup).join("");
  el.score.textContent = String(state.score).padStart(6, "0");
  el.chain.textContent = `×${state.chain}`;
  el.depth.textContent = level().lineages[0].length;
  el.chainBox.classList.toggle("hot", state.chain > 1);

  const goal = level().goal;
  el.goalBar.style.width = `${Math.min(100, (state.collapses / goal) * 100)}%`;
  el.goalText.textContent = `${Math.min(state.collapses, goal)} / ${goal}`;
  el.levelLabel.textContent = level().label;
  el.goalTitle.textContent = level().title;
}

function nodeFor(id) {
  return el.board.querySelector(`[data-id="${id}"]`);
}

function spark(ids, text, value) {
  const panel = el.sparks.getBoundingClientRect();
  const boxes = ids.map(nodeFor).filter(Boolean).map((n) => n.getBoundingClientRect());
  if (!boxes.length) return;

  const x = boxes.reduce((sum, b) => sum + b.left + b.width / 2, 0) / boxes.length - panel.left;
  const y = boxes.reduce((sum, b) => sum + b.top + b.height / 2, 0) / boxes.length - panel.top;

  const node = document.createElement("div");
  node.className = "spark";
  node.style.left = `${x}px`;
  node.style.top = `${y}px`;
  node.innerHTML = `<b>+${value}</b>${text}`;
  el.sparks.append(node);
  setTimeout(() => node.remove(), 1100);
}

function showScalar({ expr, overlap, depth, gain, kind }) {
  if (kind === "pauli") {
    el.scalarCard.className = "scalar-card";
    el.scalarCard.innerHTML = `
      <div class="scalar-expr">${expr} = 0</div>
      <div class="scalar-meta"><span>repeated core</span><b>alternation</b></div>`;
    return;
  }
  el.scalarCard.className = "scalar-card";
  el.scalarCard.innerHTML = `
    <div class="scalar-expr">${expr}</div>
    <div class="scalar-meta">
      <span>rank ${overlap.length} · depth ${depth}</span><b>+${gain}</b>
    </div>`;
}

function setStatus(text) {
  el.status.textContent = text;
}

function bump() {
  document.body.classList.add("shake");
  setTimeout(() => document.body.classList.remove("shake"), 320);
}

/* ----------------------------------------------------------------- play */

async function pauli(a, b) {
  state.busy = true;
  const reason = zeroReason(a, b);
  const gain = 120;

  [a, b].forEach((t) => nodeFor(t.id)?.classList.add("pauli"));
  spark([a.id, b.id], `${reason} → 0`, gain);
  showScalar({ expr: `${reason} in the wedge`, kind: "pauli" });
  setStatus(`A symbol repeats (${reason}). The wedge alternates to zero — chain broken.`);
  bump();

  state.score += gain;
  state.chain = 1;
  await wait(430);

  state.towers = state.towers.filter((t) => t.id !== a.id && t.id !== b.id);
  render();
  await wait(140);
  refill();
  state.busy = false;
  afterTurn();
}

async function dock(a, b) {
  state.busy = true;
  const overlap = shared(a, b);
  const depth = a.shells.length;
  const gain = 60 * depth * overlap.length * state.chain;

  [a, b].forEach((t) => nodeFor(t.id)?.classList.add("collapsing"));
  spark([a.id, b.id], `chain ×${state.chain} · seam ${overlap.join(" ")}`, gain);
  showScalar({ expr: scalarExpression(a, b, overlap), overlap, depth, gain, kind: "dock" });
  setStatus(`Shared core ${overlap.join("∧")} contracted out. One residual tower survives.`);
  bump();

  state.score += gain;
  state.collapses += 1;
  await wait(400);

  const merged = fuse(a, b);
  const index = state.towers.findIndex((t) => t.id === a.id);
  state.towers = state.towers.filter((t) => t.id !== a.id && t.id !== b.id);
  state.selected = null;

  if (!merged) {
    state.score += 200;
    state.chain = 1;
    setStatus("The whole core contracted away — the tower discharged as a pure scalar. +200");
    render();
    refill();
    state.busy = false;
    afterTurn();
    return undefined;
  }

  state.towers.splice(Math.max(0, index), 0, merged);
  render();
  nodeFor(merged.id)?.classList.add("resonant");
  await wait(320);

  const follow = state.towers.find((t) => relation(merged, t) === "dock");
  if (follow) {
    state.chain += 1;
    render();
    setStatus(`Cascade ×${state.chain} — the residual tower still shares a core.`);
    await wait(420);
    state.busy = false;
    return dock(merged, follow);
  }

  state.chain = 1;
  refill();
  state.busy = false;
  afterTurn();
  return undefined;
}

function refill() {
  while (state.towers.length < SLOTS) state.towers.push(makeTower());
  render();
}

function afterTurn() {
  render();
  if (state.collapses >= level().goal) return finishLevel();

  let guard = 0;
  while (!hasMove() && guard < 40) {
    state.towers = state.towers.map(() => makeTower());
    guard += 1;
  }
  if (guard > 0) {
    setStatus("No shared cores left — the shell re-seeded.");
    render();
  }
  return undefined;
}

function finishLevel() {
  const last = state.levelIndex === LEVELS.length - 1;
  el.banner.hidden = false;
  el.bannerMark.textContent = last ? "✦" : "◇";
  el.bannerKicker.textContent = last ? "CASCADE COMPLETE" : "SHELL COMPLETE";
  el.bannerTitle.textContent = last ? "Every shell collapsed." : "The cascade closed.";
  el.bannerText.textContent = last
    ? `Final score ${state.score}. Each collapse you fired is one application of the sandhi rule: shared deep symbols contract to a scalar, survivors fuse into a single wider tower.`
    : "The shared cores are gone. The next shell nests one level deeper.";
  el.bannerButton.textContent = last ? "Play again ↻" : "Next shell →";
}

function select(tower) {
  if (state.busy) return;

  if (!state.selected) {
    state.selected = tower;
    state.chain = 1;
    setStatus(`Selected ${tower.lineage}. Glowing towers share a deep core.`);
    render();
    return;
  }

  if (state.selected.id === tower.id) {
    state.selected = null;
    setStatus("Selection cleared.");
    render();
    return;
  }

  const kind = relation(state.selected, tower);
  const a = state.selected;
  state.selected = null;

  if (kind === "dock") { render(); dock(a, tower); return; }
  if (kind === "pauli") { render(); pauli(a, tower); return; }

  state.selected = tower;
  setStatus(
    a.lineage === tower.lineage
      ? "No shared core symbol — nothing to contract. Try a glowing tower."
      : "Different pin lineage — these towers cannot dock."
  );
  render();
}

function startLevel(index) {
  state.levelIndex = index;
  state.towers = [];
  state.selected = null;
  state.chain = 1;
  state.collapses = 0;
  state.busy = false;
  refill();
  let guard = 0;
  while (!hasMove() && guard < 40) { state.towers = state.towers.map(() => makeTower()); guard += 1; }
  el.scalarCard.className = "scalar-card empty";
  el.scalarCard.innerHTML = "<span>◇</span><p>No collapse yet. Dock two towers sharing a deep core.</p>";
  setStatus("Select a tower, then dock it into a glowing partner.");
  render();
}

/* ------------------------------------------------------------- bindings */

el.board.addEventListener("click", (event) => {
  const node = event.target.closest(".tower");
  if (!node) return;
  const tower = state.towers.find((t) => t.id === Number(node.dataset.id));
  if (tower) select(tower);
});

el.board.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" && event.key !== " ") return;
  const node = event.target.closest(".tower");
  if (!node) return;
  event.preventDefault();
  const tower = state.towers.find((t) => t.id === Number(node.dataset.id));
  if (tower) select(tower);
});

el.reset.addEventListener("click", () => startLevel(state.levelIndex));

el.bannerButton.addEventListener("click", () => {
  el.banner.hidden = true;
  if (state.levelIndex === LEVELS.length - 1) {
    state.score = 0;
    startLevel(0);
  } else {
    startLevel(state.levelIndex + 1);
  }
});

startLevel(0);
