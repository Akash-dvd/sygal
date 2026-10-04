/* Fermionic Foundry — factory reading of the sandhi rewrite.
 *
 * A packet is a nested contraction tower:
 *   d1⌋(a… ∧ d2⌋(c…))
 * The pin on each rung is what acts (Nr); the beads are what it acts on (Dr).
 * The reactor fuses two packets with the same pin lineage and a shared deep
 * bead: the shared beads contract out as the Capelli scalar (energy) and one
 * wider residual packet leaves the machine. The peel runs the same law
 * backwards and therefore costs energy.
 */

/* Wide outer pools keep accidental shell repeats (which force a zero) rare
 * enough that the reactor stays the main verb. */
const OUTER_A = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"];
const OUTER_B = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10"];

const LEVELS = [
  {
    label: "LINE 01",
    title: "Ship four grade-5 packets",
    quota: 4,
    contract: 5,
    lineages: [["d1", "d2"]],
    shellPools: [OUTER_A],
    corePool: ["c1", "c2", "c3", "c4", "c5"],
    coreSize: [2, 3],
  },
  {
    label: "LINE 02",
    title: "One shell deeper, grade 7",
    quota: 5,
    contract: 7,
    lineages: [["d1", "d2", "d3"]],
    shellPools: [OUTER_A, OUTER_B],
    corePool: ["c1", "c2", "c3", "c4", "c5", "c6"],
    coreSize: [2, 3],
  },
  {
    label: "LINE 03",
    title: "Two lineages on one belt",
    quota: 6,
    contract: 8,
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

/* The emitter only tops the belt up to FILL, so a peel always has a free slot
 * to put its second child in. CAPACITY is the hard jam limit. */
const FILL = 4;
const CAPACITY = 6;

/* Machined cartridge silhouette: chamfered corners, a socket on the left edge
 * and a matching plug on the right, so packets read as parts that snap
 * together rather than as buttons. Drawn in a 0–100 box and stretched. */
const CART_PATH =
  "M6 8 L14 1 L86 1 L94 8 L94 38 L100 44 L100 56 L94 62 L94 92 L86 99 L14 99 L6 92 L6 62 L0 56 L0 44 L6 38 Z";

const TOOL_PROMPTS = {
  reactor: "Reactor armed — click two packets that share a deep bead.",
  peel: "Peel armed — click a packet whose core holds three or more beads.",
  fuse: "Fuse armed — click two packets marked = 0.",
  ship: "Dock armed — click the packet at the belt head to ship it.",
};

const state = {
  levelIndex: 0,
  belt: [],
  tool: "reactor",
  selection: [],
  energy: 0,
  shownEnergy: 0,
  combo: 1,
  cycles: 0,
  shipped: 0,
  ledger: [],
  busy: false,
  nextId: 1,
  settled: new Set(),
};

const el = {
  panel: document.querySelector(".line-panel"),
  lane: document.getElementById("lane"),
  belt: document.querySelector(".belt"),
  sparks: document.getElementById("sparkLayer"),
  arcs: document.getElementById("arcLayer"),
  fx: document.getElementById("fxLayer"),
  flash: document.getElementById("flash"),
  toolrail: document.getElementById("toolrail"),
  energy: document.getElementById("energy"),
  energyBox: document.querySelector(".hud div"),
  combo: document.getElementById("combo"),
  comboBox: document.querySelector(".hud-combo"),
  cycles: document.getElementById("cycles"),
  status: document.getElementById("statusLine"),
  scalarCard: document.getElementById("scalarCard"),
  emitter: document.querySelector(".emitter"),
  emitterRecipe: document.getElementById("emitterRecipe"),
  dock: document.getElementById("dock"),
  dockGrade: document.getElementById("dockGrade"),
  sinkRow: document.getElementById("sinkRow"),
  sinkTotal: document.getElementById("sinkTotal"),
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

const calm = window.matchMedia("(prefers-reduced-motion: reduce)");
const reduced = () => calm.matches;

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

function makePacket() {
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

const coreOf = (packet) => packet.shells[packet.shells.length - 1].nodes;
const grade = (packet) => packet.shells.reduce((n, shell) => n + shell.nodes.length, 0);
const sharedCore = (a, b) => coreOf(a).filter((bead) => coreOf(b).includes(bead));
const sameSet = (a, b) => a.length === b.length && a.every((bead) => b.includes(bead));

const outerClash = (a, b) =>
  a.shells.slice(0, -1).some((shell, i) => shell.nodes.some((node) => b.shells[i].nodes.includes(node)));

function relation(a, b) {
  if (!a || !b || a.id === b.id) return "none";
  if (a.lineage !== b.lineage) return "none";
  if (!sharedCore(a, b).length) return "none";
  if (sameSet(coreOf(a), coreOf(b)) || outerClash(a, b)) return "zero";
  return "dock";
}

/* Sandhi: shared core beads contract out into the scalar; the survivors of
 * both packets wedge together into one residual packet. */
function fuse(a, b) {
  const overlap = sharedCore(a, b);
  const shells = a.shells.map((shell, i) => {
    const merged = [...new Set([...shell.nodes, ...b.shells[i].nodes])].sort();
    return { ...shell, nodes: shell.core ? merged.filter((bead) => !overlap.includes(bead)) : merged };
  });
  if (!shells[shells.length - 1].nodes.length) return null;
  return { id: state.nextId++, lineage: a.lineage, shells };
}

/* Vichcheda: cut the core into two children that overlap on one seam bead. */
function peelPair(packet) {
  const core = coreOf(packet);
  const mid = Math.floor(core.length / 2);
  const parts = [core.slice(0, mid + 1), core.slice(mid)];

  const children = parts.map((nodes) => ({
    id: state.nextId++,
    lineage: packet.lineage,
    shells: packet.shells.map((shell, i) =>
      i === packet.shells.length - 1 ? { ...shell, nodes: [...nodes] } : { ...shell, nodes: [...shell.nodes] }
    ),
  }));

  return { children, seam: core[mid] };
}

function hasDock() {
  for (let i = 0; i < state.belt.length; i += 1) {
    for (let j = i + 1; j < state.belt.length; j += 1) {
      if (relation(state.belt[i], state.belt[j]) === "dock") return true;
    }
  }
  return false;
}

/* The belt must always offer at least one reaction, otherwise the player can
 * only ship and scrap. */
function seedDock() {
  let guard = 0;
  while (!hasDock() && guard < 60 && state.belt.length > 1) {
    state.belt[state.belt.length - 1] = makePacket();
    guard += 1;
  }
  return guard > 0 && hasDock();
}

const pinsOf = (packet) => packet.shells.map((shell) => shell.pin).join("∧");
const scalarExpression = (packet, overlap) => `(${pinsOf(packet)}) | (${overlap.join("∧")})`;

/* ----------------------------------------------------------------- view */

function partnerKind(packet) {
  const anchor = state.selection[0];
  if (!anchor || anchor.id === packet.id) return "none";
  if (state.tool !== "reactor" && state.tool !== "fuse") return "none";
  return relation(anchor, packet);
}

const pinColor = (pin) => PIN_COLORS[pin] || "#4d8b98";

function rungMarkup(packet, shell, index, kind, overlap, anchor) {
  const mirror = anchor ? anchor.shells[index].nodes : [];
  const beads = shell.nodes
    .map((node) => {
      const marks = ["bead"];
      if (kind !== "none" && shell.core && overlap.includes(node)) marks.push("shared");
      if (kind !== "none" && !shell.core && mirror.includes(node)) marks.push("clash");
      return `<span class="${marks.join(" ")}" data-bead="${node}">${node}</span>`;
    })
    .join("");

  return `
    <div class="rung${shell.core ? " core" : ""}">
      <span class="rung-pin" style="--pin-color:${pinColor(shell.pin)}">${shell.pin}</span>
      <div class="beads">${beads}</div>
    </div>`;
}

function packetMarkup(packet, index) {
  const anchor = state.selection[0];
  const kind = partnerKind(packet);
  const overlap = anchor ? sharedCore(anchor, packet) : [];

  const rungs = packet.shells.map((shell, i) => rungMarkup(packet, shell, i, kind, overlap, anchor));

  const classes = ["cartridge"];
  if (state.settled.has(packet.id)) classes.push("settled");
  if (state.selection.some((p) => p.id === packet.id)) classes.push("selected");
  if (kind === "dock") classes.push("dockable");
  if (kind === "zero") classes.push("zeroable");
  if (index === 0) classes.push("next");

  const g = grade(packet);
  const target = level().contract;
  const head = `
    <div class="cart-head">
      <span>${packet.lineage}</span>
      <span class="cart-grade${g === target ? " match" : ""}">g${g}</span>
    </div>`;
  const meter = `<div class="cart-fill"><i style="width:${Math.min(100, (g / target) * 100)}%"></i></div>`;
  const badge = kind === "zero" ? '<span class="zero-badge">= 0</span>' : "";

  return `
    <div class="${classes.join(" ")}" data-id="${packet.id}" role="button" tabindex="0">
      ${badge}
      ${cartridgeBody(rungs, head, meter)}
    </div>`;
}

function cartridgeBody(rungs, head, meter) {
  const rivets = [[11, 5], [86.6, 5], [11, 92.4], [86.6, 92.4]]
    .map(([x, y]) => `<rect class="rivet" x="${x}" y="${y}" width="2.4" height="2.6" />`)
    .join("");

  return `
    <svg class="cart-shell" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <path class="cart-plate" d="${CART_PATH}" />
      ${rivets}
    </svg>
    <div class="cart-body">
      ${head}
      ${rungs.join("")}
      ${meter}
    </div>`;
}

/* Cartridges keep their identity across renders, so measure before the rebuild
 * and slide each survivor from where it used to be. */
function laneRects() {
  const map = new Map();
  el.lane.querySelectorAll(".cartridge").forEach((node) => map.set(node.dataset.id, node.getBoundingClientRect()));
  return map;
}

function slideLane(before) {
  if (reduced()) return;
  el.lane.querySelectorAll(".cartridge").forEach((node) => {
    const prev = before.get(node.dataset.id);
    if (!prev) return;
    const now = node.getBoundingClientRect();
    const dx = prev.left - now.left;
    const dy = prev.top - now.top;
    if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return;
    node.animate(
      [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: "none" }],
      { duration: 440, easing: "cubic-bezier(.22,.85,.28,1)" }
    );
  });
}

function renderSink() {
  el.sinkRow.innerHTML = state.ledger
    .slice(-9)
    .map((entry) => `<span class="crystal${entry.debt ? " debt" : ""}">${entry.label}</span>`)
    .join("");
}

function render() {
  const before = laneRects();

  el.lane.innerHTML = state.belt.length
    ? state.belt.map(packetMarkup).join("")
    : '<p class="lane-empty">Belt empty — the emitter is loading.</p>';
  state.belt.forEach((packet) => state.settled.add(packet.id));
  slideLane(before);

  el.combo.textContent = `×${state.combo}`;
  el.cycles.textContent = String(state.cycles);
  el.comboBox.classList.toggle("hot", state.combo > 1);
  paintEnergy();

  const cfg = level();
  el.levelLabel.textContent = cfg.label;
  el.goalTitle.textContent = cfg.title;
  el.goalBar.style.width = `${Math.min(100, (state.shipped / cfg.quota) * 100)}%`;
  el.goalText.textContent = `${Math.min(state.shipped, cfg.quota)} / ${cfg.quota}`;
  el.dockGrade.textContent = `GRADE ${cfg.contract}`;
  el.emitterRecipe.textContent = cfg.lineages.map((l) => l.join("·")).join(" / ");
  el.dock.classList.toggle("armed", state.tool === "ship");

  renderSink();
  el.toolrail.querySelectorAll(".tool").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.tool === state.tool));
  });

  drawArcs();
}

const nodeFor = (id) => el.lane.querySelector(`[data-id="${id}"]`);
const panelRect = () => el.panel.getBoundingClientRect();

function local(rect) {
  const panel = panelRect();
  return { x: rect.left + rect.width / 2 - panel.left, y: rect.top + rect.height / 2 - panel.top };
}

/* Amber threads between the beads that are about to pair off — the Gram matrix
 * of the seam, drawn before it collapses. */
function drawArcs() {
  el.arcs.innerHTML = "";
  const anchor = state.selection[0];
  if (!anchor || (state.tool !== "reactor" && state.tool !== "fuse")) return;

  const anchorNode = nodeFor(anchor.id);
  if (!anchorNode) return;

  const panel = panelRect();
  el.arcs.setAttribute("viewBox", `0 0 ${panel.width} ${panel.height}`);

  /* Only live pairings get a thread; dead pairs already read as dashed blue
   * cartridges with a = 0 badge, and arcs on them would just add noise. */
  const paths = [];
  state.belt.forEach((packet) => {
    if (relation(anchor, packet) !== "dock") return;
    const node = nodeFor(packet.id);
    if (!node) return;

    sharedCore(anchor, packet).forEach((bead) => {
      const from = anchorNode.querySelector(`.rung.core [data-bead="${bead}"]`);
      const to = node.querySelector(`.rung.core [data-bead="${bead}"]`);
      if (!from || !to) return;
      from.classList.remove("clash");
      from.classList.add("shared");

      const p1 = local(from.getBoundingClientRect());
      const p2 = local(to.getBoundingClientRect());
      const lift = Math.max(30, Math.abs(p2.x - p1.x) * 0.3);
      paths.push(
        `<path class="arc" d="M${p1.x} ${p1.y} Q${(p1.x + p2.x) / 2} ${
          Math.min(p1.y, p2.y) - lift
        } ${p2.x} ${p2.y}" />`
      );
    });
  });

  el.arcs.innerHTML = paths.join("");
}

/* --------------------------------------------------------------- effects */

function paintEnergy() {
  el.energy.textContent = String(state.shownEnergy).padStart(6, "0");
  el.sinkTotal.textContent = `${state.shownEnergy} ◇`;
}

let energyFrame = 0;
function tweenEnergy() {
  const target = Math.max(0, state.energy);
  if (reduced()) {
    state.shownEnergy = target;
    paintEnergy();
    return;
  }
  cancelAnimationFrame(energyFrame);
  const from = state.shownEnergy;
  const start = performance.now();
  const step = (now) => {
    const k = Math.min(1, (now - start) / 520);
    state.shownEnergy = Math.round(from + (target - from) * (1 - (1 - k) ** 3));
    paintEnergy();
    if (k < 1) energyFrame = requestAnimationFrame(step);
  };
  energyFrame = requestAnimationFrame(step);
}

function flash(cold) {
  el.flash.className = `flash show${cold ? " cold" : ""}`;
  setTimeout(() => { el.flash.className = "flash"; }, 420);
}

function runMachine(tool, cold) {
  el.panel.classList.add("reacting");
  const button = el.toolrail.querySelector(`[data-tool="${tool}"]`);
  button?.classList.add("firing");
  flash(cold);
  setTimeout(() => {
    el.panel.classList.remove("reacting");
    button?.classList.remove("firing");
  }, 620);
}

function burst(point, cold) {
  if (reduced()) return;

  const ring = document.createElement("div");
  ring.className = `ring${cold ? " cold" : ""}`;
  ring.style.left = `${point.x}px`;
  ring.style.top = `${point.y}px`;
  el.fx.append(ring);
  setTimeout(() => ring.remove(), 720);

  for (let i = 0; i < 14; i += 1) {
    const mote = document.createElement("i");
    const angle = (Math.PI * 2 * i) / 14 + Math.random() * 0.5;
    const reach = 38 + Math.random() * 74;
    mote.className = `mote${cold ? " cold" : ""}`;
    mote.style.left = `${point.x}px`;
    mote.style.top = `${point.y}px`;
    mote.style.setProperty("--dx", `${Math.cos(angle) * reach}px`);
    mote.style.setProperty("--dy", `${Math.sin(angle) * reach}px`);
    mote.style.animationDelay = `${Math.random() * 90}ms`;
    el.fx.append(mote);
    setTimeout(() => mote.remove(), 900);
  }
}

function pulseSink() {
  el.sinkRow.parentElement.classList.add("charged");
  setTimeout(() => el.sinkRow.parentElement.classList.remove("charged"), 480);
}

/* The scalar is worth an object on screen: it leaves the seam and lands in the
 * sink as a crystal. */
function flyCrystal(point, label, debt) {
  const sink = local(el.sinkRow.getBoundingClientRect());
  const slot = Math.min(8, state.ledger.length) * 32;
  const target = { x: sink.x - el.sinkRow.clientWidth / 2 + slot + 16, y: sink.y };

  const node = document.createElement("div");
  node.className = `flying-crystal${debt ? " debt" : ""}`;
  node.textContent = label;
  node.style.left = `${point.x}px`;
  node.style.top = `${point.y}px`;
  el.fx.append(node);

  const at = (dx, dy, scale, spin) =>
    `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) scale(${scale}) rotate(${spin}deg)`;

  const midX = (target.x - point.x) * 0.45;
  const arc = node.animate(
    [
      { transform: at(0, 0, 0.4, 0), opacity: 0 },
      { offset: 0.2, transform: at(0, -18, 1.3, 25), opacity: 1 },
      { offset: 0.6, transform: at(midX, -62, 1, 200), opacity: 1 },
      { transform: at(target.x - point.x, target.y - point.y, 0.65, 340), opacity: 0.1 },
    ],
    { duration: 920, easing: "cubic-bezier(.32,.68,.4,1)" }
  );

  arc.onfinish = () => {
    node.remove();
    state.ledger.push({ label, debt: Boolean(debt) });
    renderSink();
    pulseSink();
  };
}

function credit(amount, label, debt, point) {
  state.energy = Math.max(0, state.energy + amount);
  tweenEnergy();
  el.energyBox.classList.add("tick");
  setTimeout(() => el.energyBox.classList.remove("tick"), 420);

  if (point && !reduced()) {
    flyCrystal(point, label, debt);
    return;
  }
  state.ledger.push({ label, debt: Boolean(debt) });
  renderSink();
}

function spark(point, text, value, cold) {
  const node = document.createElement("div");
  node.className = `spark${cold ? " cold" : ""}`;
  node.style.left = `${point.x}px`;
  node.style.top = `${point.y}px`;
  node.innerHTML = `<b>${value >= 0 ? "+" : "−"}${Math.abs(value)}</b>${text}`;
  el.sparks.append(node);
  setTimeout(() => node.remove(), 1100);
}

/* Pull the two cartridges into each other before they collapse. */
function converge(nodes, point) {
  nodes.forEach((node) => {
    if (!node) return;
    if (reduced()) {
      node.classList.add("merging");
      return;
    }
    const here = local(node.getBoundingClientRect());
    node.animate(
      [
        { transform: "none", opacity: 1 },
        { offset: 0.45, transform: `translate(${(point.x - here.x) * 0.5}px, 0) scale(1.04)`, opacity: 1 },
        { transform: `translate(${point.x - here.x}px, 0) scale(.6)`, opacity: 0 },
      ],
      { duration: 440, easing: "cubic-bezier(.42,.05,.6,1)", fill: "forwards" }
    );
  });
}

/* The occupations that pair off slide down the seam into the contact point
 * before the two cartridges collapse — the Wick pairing, made literal. */
async function pairOff(nodes, point) {
  if (reduced()) return;

  nodes.forEach((node) => {
    node?.querySelector(".cart-plate")?.animate(
      [{ strokeWidth: 1.4 }, { strokeWidth: 3.2 }, { strokeWidth: 1.4 }],
      { duration: 420, easing: "ease-in-out" }
    );
  });

  const beads = nodes.flatMap((node) => (node ? [...node.querySelectorAll(".rung.core .bead.shared")] : []));
  beads.forEach((bead, i) => {
    const here = local(bead.getBoundingClientRect());
    bead.animate(
      [
        { transform: "none", opacity: 1 },
        { offset: 0.7, transform: `translate(${point.x - here.x}px, ${point.y - here.y}px) scale(.9)`, opacity: 1 },
        { transform: `translate(${point.x - here.x}px, ${point.y - here.y}px) scale(0)`, opacity: 0 },
      ],
      { duration: 420, delay: i * 45, easing: "cubic-bezier(.4,.1,.5,1)", fill: "forwards" }
    );
  });

  await wait(360 + beads.length * 45);
}

function pop(node) {
  if (!node) return;
  if (reduced()) return;
  node.animate(
    [
      { transform: "scale(.7)", opacity: 0, filter: "brightness(2.2)" },
      { offset: 0.55, transform: "scale(1.08)", opacity: 1, filter: "brightness(1.3)" },
      { transform: "none", opacity: 1, filter: "none" },
    ],
    { duration: 460, easing: "cubic-bezier(.2,.9,.3,1.25)" }
  );
}

function slash(node) {
  if (!node || reduced()) return;
  const core = node.querySelector(".rung.core") || node;
  const point = local(core.getBoundingClientRect());
  const cut = document.createElement("div");
  cut.className = "cut";
  cut.style.left = `${point.x}px`;
  cut.style.top = `${point.y}px`;
  el.fx.append(cut);
  setTimeout(() => cut.remove(), 520);
}

function bump() {
  if (reduced()) return;
  document.body.classList.add("shake");
  setTimeout(() => document.body.classList.remove("shake"), 300);
}

/* ----------------------------------------------------------------- play */

function emit() {
  if (state.belt.length < FILL) state.belt.push(makePacket());
  el.emitter.classList.add("firing");
  setTimeout(() => el.emitter.classList.remove("firing"), 520);
}

function endCycle() {
  state.cycles += 1;
  state.selection = [];
  emit();
  if (state.belt.length >= FILL && seedDock()) {
    setStatus("No reaction left on the belt — the emitter reloaded the tail.");
  }
  render();
  if (state.shipped >= level().quota) finishLevel();
}

const setStatus = (text) => { el.status.textContent = text; };

async function runReactor(a, b) {
  state.busy = true;
  const overlap = sharedCore(a, b);
  const depth = a.shells.length;
  const gain = 40 * depth * overlap.length * state.combo;

  const nodes = [nodeFor(a.id), nodeFor(b.id)];
  const points = nodes.filter(Boolean).map((n) => local(n.getBoundingClientRect()));
  const point = {
    x: points.reduce((s, p) => s + p.x, 0) / points.length,
    y: points.reduce((s, p) => s + p.y, 0) / points.length,
  };

  setStatus(`Seam ${overlap.join("∧")} clamped — pairing off the shared occupation.`);
  await pairOff(nodes, point);

  el.arcs.classList.add("firing");
  converge(nodes, point);
  runMachine("reactor");
  burst(point);
  spark(point, `combo ×${state.combo} · seam ${overlap.join(" ")}`, gain);
  showReaction({
    expr: scalarExpression(a, overlap),
    meta: `rank ${overlap.length} · depth ${depth}`,
    gain,
  });
  setStatus(`Seam ${overlap.join("∧")} contracted out as energy. One residual packet leaves the reactor.`);
  bump();

  credit(gain, `+${gain}`, false, point);
  state.combo += 1;
  await wait(440);
  el.arcs.classList.remove("firing");

  const merged = fuse(a, b);
  const index = state.belt.findIndex((p) => p.id === a.id);
  state.belt = state.belt.filter((p) => p.id !== a.id && p.id !== b.id);

  if (merged) {
    state.belt.splice(Math.max(0, index), 0, merged);
    render();
    pop(nodeFor(merged.id));
  } else {
    credit(150, "+150", false, point);
    setStatus("The whole core contracted away — the packet discharged as pure energy. +150");
    render();
  }

  await wait(300);
  state.busy = false;
  endCycle();
}

async function runPeel(packet) {
  state.busy = true;
  const depth = packet.shells.length;
  const cost = 25 * depth;
  const { children, seam } = peelPair(packet);

  const node = nodeFor(packet.id);
  const point = node ? local(node.getBoundingClientRect()) : { x: 0, y: 0 };

  slash(node);
  node?.classList.add("cutting");
  runMachine("peel", true);
  spark(point, `borrowed seam ${seam}`, -cost, true);
  showReaction({
    expr: `${packet.lineage} ⌋(…) → two children sharing ${seam}`,
    meta: `vichcheda · depth ${depth}`,
    gain: -cost,
    cold: true,
  });
  setStatus(`Cut on ${seam}. Two overlapping children on the belt, and a debt of ${cost} in the sink.`);

  credit(-cost, `−${cost}`, true, point);
  state.combo = 1;
  await wait(400);

  const index = state.belt.findIndex((p) => p.id === packet.id);
  state.belt.splice(index, 1, ...children);
  if (state.belt.length > CAPACITY) state.belt.length = CAPACITY;
  render();
  children.forEach((child) => pop(nodeFor(child.id)));

  await wait(240);
  state.busy = false;
  state.cycles += 1;
  state.selection = [];
  render();
}

async function runFuse(a, b) {
  state.busy = true;
  const gain = 60;
  const reason = outerClash(a, b) ? "repeated shell bead" : "repeated core";

  const nodes = [nodeFor(a.id), nodeFor(b.id)];
  const points = nodes.filter(Boolean).map((n) => local(n.getBoundingClientRect()));
  const point = {
    x: points.reduce((s, p) => s + p.x, 0) / points.length,
    y: points.reduce((s, p) => s + p.y, 0) / points.length,
  };

  nodes.forEach((n) => n?.classList.add("scrapped"));
  runMachine("fuse", true);
  burst(point, true);
  spark(point, `${reason} → 0`, gain, true);
  showReaction({
    expr: `${reason} inside one wedge = 0`,
    meta: "pauli fuse · scrap refund",
    gain,
    cold: true,
  });
  setStatus(`A bead repeats (${reason}), so the term is zero. Both packets scrapped for a small refund.`);
  bump();

  credit(gain, `+${gain}`, false, point);
  state.combo = 1;
  await wait(440);

  state.belt = state.belt.filter((p) => p.id !== a.id && p.id !== b.id);
  render();
  await wait(140);
  state.busy = false;
  endCycle();
}

async function runShip(packet) {
  state.busy = true;
  const cfg = level();
  const g = grade(packet);
  const ok = g === cfg.contract;
  const gain = ok ? 120 + 20 * g : -80;

  const node = nodeFor(packet.id);
  const point = node ? local(node.getBoundingClientRect()) : { x: 0, y: 0 };
  const target = local(el.dock.getBoundingClientRect());

  if (node && !reduced()) {
    node.animate(
      [
        { transform: "none", opacity: 1 },
        { offset: 0.7, transform: `translate(${(target.x - point.x) * 0.8}px, 0) scale(.9)`, opacity: 1 },
        { transform: `translate(${target.x - point.x}px, 0) scale(.6)`, opacity: 0 },
      ],
      { duration: 480, easing: "cubic-bezier(.5,.05,.6,1)", fill: "forwards" }
    );
  } else {
    node?.classList.add("shipping");
  }

  runMachine("ship", !ok);
  el.dock.classList.add(ok ? "hit" : "reject");
  spark(point, ok ? `contract grade ${g}` : `off-spec grade ${g}`, gain, !ok);
  showReaction({
    expr: ok
      ? `shipped ${packet.lineage} ⌋(…) at grade ${g}`
      : `rejected ${packet.lineage} ⌋(…) — grade ${g}, contract ${cfg.contract}`,
    meta: ok ? "output dock · accepted" : "output dock · scrapped",
    gain,
    cold: !ok,
  });
  setStatus(
    ok
      ? `Grade ${g} matches the contract. Quota advanced.`
      : `Grade ${g} misses the contract of ${cfg.contract}. Scrapped at a penalty — merge or peel to hit it exactly.`
  );

  await wait(360);
  burst(target, !ok);
  credit(gain, `${gain >= 0 ? "+" : "−"}${Math.abs(gain)}`, !ok, target);
  if (ok) state.shipped += 1;
  else state.combo = 1;

  await wait(220);
  el.dock.classList.remove("hit", "reject");
  state.belt = state.belt.filter((p) => p.id !== packet.id);
  render();
  state.busy = false;
  endCycle();
}

function showReaction({ expr, meta, gain, cold }) {
  el.scalarCard.className = "scalar-card fired";
  el.scalarCard.innerHTML = `
    <div class="scalar-expr">${expr}</div>
    <div class="scalar-meta">
      <span>${meta}</span><b class="${cold ? "cold" : ""}">${gain >= 0 ? "+" : "−"}${Math.abs(gain)}</b>
    </div>`;
  setTimeout(() => el.scalarCard.classList.remove("fired"), 500);
}

/* ------------------------------------------------------------- dispatch */

function chooseTool(tool) {
  if (state.busy || !TOOL_PROMPTS[tool]) return;
  state.tool = tool;
  state.selection = [];
  setStatus(TOOL_PROMPTS[tool]);
  render();
}

function handlePacket(packet) {
  if (state.busy) return;

  if (state.tool === "ship") {
    if (state.belt[0].id !== packet.id) {
      setStatus("Only the packet at the head of the belt reaches the dock.");
      return;
    }
    runShip(packet);
    return;
  }

  if (state.tool === "peel") {
    if (coreOf(packet).length < 3) {
      setStatus("This core is too small to cut — a peel needs three or more beads.");
      return;
    }
    if (state.belt.length >= CAPACITY) {
      setStatus("The belt is full. Ship or fuse something before cutting a packet in two.");
      return;
    }
    runPeel(packet);
    return;
  }

  const anchor = state.selection[0];
  if (!anchor) {
    state.selection = [packet];
    setStatus(
      state.tool === "reactor"
        ? "Selected. Amber threads show the beads that will pair off and leave."
        : "Selected. Click a dashed blue partner to scrap the pair."
    );
    render();
    return;
  }

  if (anchor.id === packet.id) {
    state.selection = [];
    setStatus(TOOL_PROMPTS[state.tool]);
    render();
    return;
  }

  const kind = relation(anchor, packet);

  /* Actions keep the selection alive so the seam threads and paired beads are
   * still on screen for the reaction to animate; endCycle clears it after. */
  if (state.tool === "reactor") {
    if (kind === "dock") { runReactor(anchor, packet); return; }
    state.selection = [packet];
    setStatus(
      kind === "zero"
        ? "That pair annihilates. Switch to the Pauli fuse to scrap it."
        : anchor.lineage === packet.lineage
          ? "No shared bead in the deep core — nothing for the reactor to contract."
          : "Different pin lineage. These packets cannot dock."
    );
    render();
    return;
  }

  if (kind === "zero") { runFuse(anchor, packet); return; }
  state.selection = [packet];
  setStatus("Nothing annihilates here. The fuse only scraps pairs marked = 0.");
  render();
}

function finishLevel() {
  const last = state.levelIndex === LEVELS.length - 1;
  el.banner.hidden = false;
  el.bannerMark.textContent = last ? "✦" : "◇";
  el.bannerKicker.textContent = last ? "FOUNDRY CLEARED" : "CONTRACT FILLED";
  el.bannerTitle.textContent = last ? "Every line ran." : "The line ran clean.";
  el.bannerText.textContent = last
    ? `Final energy ${state.energy} over ${state.cycles} cycles. Every reaction you fired was one application of the sandhi rule: shared deep beads contract to a scalar, survivors fuse into one wider packet.`
    : `Quota met in ${state.cycles} cycles. The next line runs deeper packets and a tighter contract.`;
  el.bannerButton.textContent = last ? "Run again ↻" : "Next line →";
}

function startLevel(index) {
  state.levelIndex = index;
  state.belt = [];
  state.selection = [];
  state.combo = 1;
  state.cycles = 0;
  state.shipped = 0;
  state.ledger = [];
  state.settled = new Set();
  state.busy = false;
  while (state.belt.length < FILL) state.belt.push(makePacket());
  seedDock();

  el.scalarCard.className = "scalar-card empty";
  el.scalarCard.innerHTML =
    "<span>◇</span><p>Nothing has fired yet. Dock two packets that share a deep occupation.</p>";
  setStatus(TOOL_PROMPTS[state.tool]);
  tweenEnergy();
  render();
}

/* ------------------------------------------------------------- bindings */

el.toolrail.addEventListener("click", (event) => {
  const button = event.target.closest(".tool");
  if (button) chooseTool(button.dataset.tool);
});

el.lane.addEventListener("click", (event) => {
  const node = event.target.closest(".cartridge");
  if (!node) return;
  const packet = state.belt.find((p) => p.id === Number(node.dataset.id));
  if (packet) handlePacket(packet);
});

el.lane.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" && event.key !== " ") return;
  const node = event.target.closest(".cartridge");
  if (!node) return;
  event.preventDefault();
  const packet = state.belt.find((p) => p.id === Number(node.dataset.id));
  if (packet) handlePacket(packet);
});

document.addEventListener("keydown", (event) => {
  const keys = { r: "reactor", v: "peel", f: "fuse", s: "ship" };
  const tool = keys[event.key.toLowerCase()];
  if (tool) chooseTool(tool);
});

window.addEventListener("resize", () => drawArcs());

el.reset.addEventListener("click", () => startLevel(state.levelIndex));

el.bannerButton.addEventListener("click", () => {
  el.banner.hidden = true;
  if (state.levelIndex === LEVELS.length - 1) {
    state.energy = 0;
    state.shownEnergy = 0;
    startLevel(0);
  } else {
    startLevel(state.levelIndex + 1);
  }
});

startLevel(0);
