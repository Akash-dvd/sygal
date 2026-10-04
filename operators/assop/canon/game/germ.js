/* Germ Culture — biological reading of the sandhi rewrite.
 *
 * The rules are byte-for-byte the ones the foundry runs: a phage is a nested
 * contraction tower d1⌋(a… ∧ d2⌋(c…)), two phages of one lineage sharing a
 * deep gene inject and leave one residual, a repeated symbol is zero, and a
 * cut runs the law backwards at a cost. Only the staging is different — a
 * round dish, drifting creatures, and actions that hang off the creature the
 * player primed instead of a rail of machines.
 */

const OUTER_A = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"];
const OUTER_B = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10"];

const PLATES = [
  {
    label: "PLATE 01",
    title: "Infect the host four times",
    quota: 4,
    receptor: 5,
    lineages: [["d1", "d2"]],
    shellPools: [OUTER_A],
    corePool: ["c1", "c2", "c3", "c4", "c5"],
    coreSize: [2, 3],
  },
  {
    label: "PLATE 02",
    title: "A deeper strain, receptor 7",
    quota: 5,
    receptor: 7,
    lineages: [["d1", "d2", "d3"]],
    shellPools: [OUTER_A, OUTER_B],
    corePool: ["c1", "c2", "c3", "c4", "c5", "c6"],
    coreSize: [2, 3],
  },
  {
    label: "PLATE 03",
    title: "Two strains on one plate",
    quota: 6,
    receptor: 8,
    lineages: [["d1", "d2", "d3"], ["e1", "e2", "e3"]],
    shellPools: [OUTER_A, OUTER_B],
    corePool: ["c1", "c2", "c3", "c4", "c5", "c6", "c7"],
    coreSize: [3, 4],
  },
];

const PIN_COLORS = {
  d1: "#86c26b", d2: "#5fa8a0", d3: "#ffd166",
  e1: "#b58ad1", e2: "#e08f6a", e3: "#ffd166",
};

/* The plate refills to FILL, so a cut always has room for its second child. */
const FILL = 4;
const CAPACITY = 6;

/* Creatures sit on a ring around the host, clear of the cell in the middle. */
const SLOTS = [-90, -30, 30, 90, 150, 210].map((deg) => {
  const rad = (deg * Math.PI) / 180;
  return { x: 50 + 35 * Math.cos(rad), y: 50 + 35 * Math.sin(rad) };
});

const state = {
  plateIndex: 0,
  colony: [],
  slots: new Map(),
  primed: null,
  biomass: 0,
  shownBiomass: 0,
  virulence: 1,
  generations: 0,
  infections: 0,
  busy: false,
  nextId: 1,
};

const el = {
  dish: document.getElementById("dish"),
  colony: document.getElementById("colony"),
  filaments: document.getElementById("filaments"),
  fx: document.getElementById("fxLayer"),
  host: document.getElementById("host"),
  hostDemand: document.getElementById("hostDemand"),
  hint: document.getElementById("hintLine"),
  biomass: document.getElementById("biomass"),
  biomassBox: document.querySelector(".hud div"),
  virulence: document.getElementById("virulence"),
  virulenceBox: document.querySelector(".hud-virulence"),
  generations: document.getElementById("generations"),
  eventCard: document.getElementById("eventCard"),
  plateLabel: document.getElementById("plateLabel"),
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

const plate = () => PLATES[state.plateIndex];
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

function makePhage() {
  const cfg = plate();
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

const coreOf = (phage) => phage.shells[phage.shells.length - 1].nodes;
const genomeSize = (phage) => phage.shells.reduce((n, shell) => n + shell.nodes.length, 0);
const sharedCore = (a, b) => coreOf(a).filter((gene) => coreOf(b).includes(gene));
const sameSet = (a, b) => a.length === b.length && a.every((gene) => b.includes(gene));

const outerClash = (a, b) =>
  a.shells.slice(0, -1).some((shell, i) => shell.nodes.some((node) => b.shells[i].nodes.includes(node)));

function relation(a, b) {
  if (!a || !b || a.id === b.id) return "none";
  if (a.lineage !== b.lineage) return "none";
  if (!sharedCore(a, b).length) return "none";
  if (sameSet(coreOf(a), coreOf(b)) || outerClash(a, b)) return "zero";
  return "dock";
}

/* Sandhi: the shared genes pair off into the scalar; everything else in both
 * creatures wedges together into the survivor. */
function inject(a, b) {
  const overlap = sharedCore(a, b);
  const shells = a.shells.map((shell, i) => {
    const merged = [...new Set([...shell.nodes, ...b.shells[i].nodes])].sort();
    return { ...shell, nodes: shell.core ? merged.filter((gene) => !overlap.includes(gene)) : merged };
  });
  if (!shells[shells.length - 1].nodes.length) return null;
  return { id: state.nextId++, lineage: a.lineage, shells };
}

/* Vichcheda: cut the genome into two daughters overlapping on one gene. */
function cutPair(phage) {
  const core = coreOf(phage);
  const mid = Math.floor(core.length / 2);
  const parts = [core.slice(0, mid + 1), core.slice(mid)];

  const children = parts.map((nodes) => ({
    id: state.nextId++,
    lineage: phage.lineage,
    shells: phage.shells.map((shell, i) =>
      i === phage.shells.length - 1 ? { ...shell, nodes: [...nodes] } : { ...shell, nodes: [...shell.nodes] }
    ),
  }));

  return { children, seam: core[mid] };
}

function hasPair() {
  for (let i = 0; i < state.colony.length; i += 1) {
    for (let j = i + 1; j < state.colony.length; j += 1) {
      if (relation(state.colony[i], state.colony[j]) === "dock") return true;
    }
  }
  return false;
}

/* The plate must always offer at least one injection. */
function seedPair() {
  let guard = 0;
  while (!hasPair() && guard < 60 && state.colony.length > 1) {
    const last = state.colony[state.colony.length - 1];
    state.slots.delete(last.id);
    state.colony[state.colony.length - 1] = makePhage();
    guard += 1;
  }
  return guard > 0 && hasPair();
}

const pinsOf = (phage) => phage.shells.map((shell) => shell.pin).join("∧");
const scalarExpression = (phage, overlap) => `(${pinsOf(phage)}) | (${overlap.join("∧")})`;
const pinColor = (pin) => PIN_COLORS[pin] || "#86c26b";

/* ----------------------------------------------------------------- view */

function partnerKind(phage) {
  if (!state.primed) return "none";
  if (state.primed.id === phage.id) return "self";
  return relation(state.primed, phage);
}

function slotFor(id) {
  if (state.slots.has(id)) return state.slots.get(id);
  const taken = new Set(state.slots.values());
  const free = SLOTS.findIndex((_, i) => !taken.has(i));
  const index = free === -1 ? state.slots.size % SLOTS.length : free;
  state.slots.set(id, index);
  return index;
}

/* Genes the primed creature can pair off with anyone on the plate, so its own
 * seam lights up too and the filaments visibly start somewhere. */
function primedSeam() {
  if (!state.primed) return [];
  const seam = new Set();
  state.colony.forEach((other) => {
    if (relation(state.primed, other) !== "dock") return;
    sharedCore(state.primed, other).forEach((gene) => seam.add(gene));
  });
  return [...seam];
}

function phageMarkup(phage) {
  const kind = partnerKind(phage);
  const overlap = kind === "self" ? primedSeam() : state.primed ? sharedCore(state.primed, phage) : [];
  const core = phage.shells[phage.shells.length - 1];
  const outer = phage.shells.slice(0, -1);

  const collars = outer
    .map((shell, i) => {
      const mirror = state.primed ? state.primed.shells[i].nodes : [];
      const genes = shell.nodes
        .map((node) => {
          const dead = kind !== "none" && kind !== "self" && mirror.includes(node);
          return `<span class="gene${dead ? " lethal" : ""}" data-gene="${node}">${node}</span>`;
        })
        .join("");
      return `
        <div class="collar">
          <span class="collar-pin" style="--pin:${pinColor(shell.pin)}">${shell.pin}</span>
          ${genes}
        </div>`;
    })
    .join("");

  /* Only a live pairing lights amber. A lethal pair keeps its dashed rim and
   * the = 0 badge, so the two readings never fight over one gene. */
  const genes = core.nodes
    .map((node) => {
      const shared = (kind === "dock" || kind === "self") && overlap.includes(node);
      const dead = kind === "zero" && overlap.includes(node);
      return `<span class="gene${shared ? " shared" : ""}${dead ? " lethal" : ""}" data-gene="${node}">${node}</span>`;
    })
    .join("");

  const size = genomeSize(phage);
  const receptor = plate().receptor;

  const classes = ["phage"];
  if (kind === "self") classes.push("primed");
  if (kind === "dock") classes.push("compatible");
  if (kind === "zero") classes.push("lethal-pair");

  const slot = SLOTS[slotFor(phage.id)];
  const canCut = coreOf(phage).length >= 3 && state.colony.length < CAPACITY;

  const chips =
    kind === "self"
      ? `
      <span class="chips">
        <span class="chip" data-act="cut"${canCut ? "" : " disabled"}>CUT</span>
        <span class="chip" data-act="send">SEND TO HOST</span>
      </span>`
      : "";

  return `
    <button class="${classes.join(" ")}" data-id="${phage.id}" style="--x:${slot.x}%; --y:${slot.y}%"
      aria-label="Phage ${phage.lineage}, ${size} genes">
      ${kind === "zero" ? '<span class="dead-mark">= 0</span>' : ""}
      <span class="phage-body">
        <span class="gene-count">
          <span>${phage.lineage}</span>
          <b class="${size === receptor ? "match" : ""}">g${size}</b>
        </span>
        <svg class="capsid" viewBox="0 0 66 60" style="--capsid:${pinColor(phage.shells[0].pin)}" aria-hidden="true">
          <polygon class="capsid-shell" points="33,0 66,15.6 66,44.4 33,60 0,44.4 0,15.6" />
          <path class="capsid-facet" d="M0 15.6 L33 30 L66 15.6 M33 30 L33 60" />
          <circle class="capsid-core" cx="33" cy="30" r="6.5" />
        </svg>
        <span class="collars">${collars}</span>
        <span class="sheath" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        <span class="baseplate" style="--plate:${pinColor(core.pin)}">
          <svg class="plate-shell" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
            <path d="M6 1 L94 1 L99 99 L1 99 Z" />
          </svg>
          <span class="genome">
            <span class="collar-pin" style="--pin:${pinColor(core.pin)}">${core.pin}</span>
            ${genes}
          </span>
        </span>
        <span class="fibers" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>
      </span>
      ${chips}
    </button>`;
}

function render() {
  el.colony.innerHTML = state.colony.map(phageMarkup).join("");

  const cfg = plate();
  el.plateLabel.textContent = cfg.label;
  el.goalTitle.textContent = cfg.title;
  el.hostDemand.textContent = String(cfg.receptor);
  el.goalBar.style.width = `${Math.min(100, (state.infections / cfg.quota) * 100)}%`;
  el.goalText.textContent = `${Math.min(state.infections, cfg.quota)} / ${cfg.quota}`;
  el.virulence.textContent = `×${state.virulence}`;
  el.virulenceBox.classList.toggle("hot", state.virulence > 1);
  el.generations.textContent = String(state.generations);
  el.host.classList.toggle("ready", Boolean(state.primed));
  paintBiomass();

  drawFilaments();
}

const nodeFor = (id) => el.colony.querySelector(`[data-id="${id}"]`);
const dishRect = () => el.dish.getBoundingClientRect();

function local(rect) {
  const dish = dishRect();
  return { x: rect.left + rect.width / 2 - dish.left, y: rect.top + rect.height / 2 - dish.top };
}

const centreOf = (id) => {
  const node = nodeFor(id);
  return node ? local(node.getBoundingClientRect()) : null;
};

/* A filament runs from every shared gene of the primed creature to the same
 * gene on a compatible neighbour — the seam, drawn on the plate. */
function drawFilaments() {
  el.filaments.innerHTML = "";
  el.filaments.classList.remove("taut");
  if (!state.primed) return;

  const dish = dishRect();
  el.filaments.setAttribute("viewBox", `0 0 ${dish.width} ${dish.height}`);
  const anchor = nodeFor(state.primed.id);
  if (!anchor) return;

  state.colony.forEach((phage) => {
    if (relation(state.primed, phage) !== "dock") return;
    const partner = nodeFor(phage.id);
    if (!partner) return;

    sharedCore(state.primed, phage).forEach((gene) => {
      const from = anchor.querySelector(`.genome [data-gene="${gene}"]`);
      const to = partner.querySelector(`.genome [data-gene="${gene}"]`);
      if (!from || !to) return;

      const a = local(from.getBoundingClientRect());
      const b = local(to.getBoundingClientRect());
      const bend = 0.18 * Math.hypot(b.x - a.x, b.y - a.y);
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2 + bend;

      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("class", "filament");
      path.setAttribute("d", `M${a.x} ${a.y} Q${mx} ${my} ${b.x} ${b.y}`);
      el.filaments.append(path);
    });
  });
}

/* --------------------------------------------------------------- effects */

function paintBiomass() {
  el.biomass.textContent = String(Math.round(state.shownBiomass)).padStart(6, "0");
}

function tweenBiomass() {
  const from = state.shownBiomass;
  const to = state.biomass;
  if (reduced() || from === to) {
    state.shownBiomass = to;
    paintBiomass();
    return;
  }
  const started = performance.now();
  const step = (now) => {
    const t = Math.min(1, (now - started) / 520);
    state.shownBiomass = from + (to - from) * (1 - Math.pow(1 - t, 3));
    paintBiomass();
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

function credit(amount, cold) {
  state.biomass = Math.max(0, state.biomass + amount);
  tweenBiomass();
  el.biomassBox.classList.add("tick");
  setTimeout(() => el.biomassBox.classList.remove("tick"), 420);
  if (cold) el.biomassBox.classList.remove("tick");
}

function burst(point, cold) {
  if (reduced() || !point) return;

  const ring = document.createElement("div");
  ring.className = `ring${cold ? " cold" : ""}`;
  ring.style.left = `${point.x}px`;
  ring.style.top = `${point.y}px`;
  el.fx.append(ring);
  setTimeout(() => ring.remove(), 640);

  for (let i = 0; i < 12; i += 1) {
    const angle = (Math.PI * 2 * i) / 12 + Math.random();
    const reach = 40 + Math.random() * 55;
    const mote = document.createElement("div");
    mote.className = `mote${cold ? " cold" : ""}`;
    mote.style.left = `${point.x}px`;
    mote.style.top = `${point.y}px`;
    mote.style.setProperty("--dx", `${Math.cos(angle) * reach}px`);
    mote.style.setProperty("--dy", `${Math.sin(angle) * reach}px`);
    el.fx.append(mote);
    setTimeout(() => mote.remove(), 720);
  }
}

function readout(point, value, text, cold) {
  if (!point) return;
  const node = document.createElement("div");
  node.className = `readout${cold ? " cold" : ""}`;
  node.style.left = `${point.x}px`;
  node.style.top = `${point.y}px`;
  node.innerHTML = `<b>${value >= 0 ? "+" : "−"}${Math.abs(value)}</b>${text}`;
  el.fx.append(node);
  setTimeout(() => node.remove(), 1120);
}

function shake() {
  if (reduced()) return;
  document.body.classList.add("shake");
  setTimeout(() => document.body.classList.remove("shake"), 320);
}

function setHint(text) {
  el.hint.textContent = text;
}

function showEvent({ expr, meta, gain, cold }) {
  el.eventCard.className = "event-card fired";
  el.eventCard.innerHTML = `
    <div class="event-expr">${expr}</div>
    <div class="event-meta">
      <span>${meta}</span><b class="${cold ? "cold" : ""}">${gain >= 0 ? "+" : "−"}${Math.abs(gain)}</b>
    </div>`;
}

/* The genes that pair off crawl down the filament into the contact point. */
function drainGenes(nodes, point) {
  if (reduced()) return 0;
  const genes = nodes.flatMap((node) => (node ? [...node.querySelectorAll(".genome .gene.shared")] : []));
  genes.forEach((gene, i) => {
    const here = local(gene.getBoundingClientRect());
    gene.animate(
      [
        { transform: "none", opacity: 1 },
        { offset: 0.7, transform: `translate(${point.x - here.x}px, ${point.y - here.y}px) scale(.9)`, opacity: 1 },
        { transform: `translate(${point.x - here.x}px, ${point.y - here.y}px) scale(0)`, opacity: 0 },
      ],
      { duration: 440, delay: i * 50, easing: "cubic-bezier(.4,.1,.5,1)", fill: "forwards" }
    );
  });
  return 400 + genes.length * 50;
}

/* ---------------------------------------------------------------- verbs */

async function runInject(a, b) {
  state.busy = true;
  const overlap = sharedCore(a, b);
  const depth = a.shells.length;
  const gain = 40 * depth * overlap.length * state.virulence;

  const from = centreOf(a.id);
  const to = centreOf(b.id);
  const point = { x: (from.x + to.x) / 2, y: (from.y + to.y) / 2 };

  setHint(`Fibers locked on ${overlap.join("∧")} — the sheath is contracting.`);

  /* Both creatures crawl together on the plate, then the tail punches. */
  const nodes = [nodeFor(a.id), nodeFor(b.id)];
  const dish = dishRect();
  nodes.forEach((node) => {
    if (!node) return;
    node.style.setProperty("--x", `${(point.x / dish.width) * 100}%`);
    node.style.setProperty("--y", `${(point.y / dish.height) * 100}%`);
  });
  el.filaments.classList.add("taut");
  await wait(reduced() ? 0 : 380);

  nodes.forEach((node) => node?.classList.add("injecting"));
  await wait(drainGenes(nodes, point));

  burst(point);
  readout(point, gain, `virulence ×${state.virulence} · gene ${overlap.join(" ")}`);
  showEvent({
    expr: scalarExpression(a, overlap),
    meta: `rank ${overlap.length} · depth ${depth}`,
    gain,
  });
  credit(gain);
  state.virulence += 1;
  shake();
  setHint(`Gene ${overlap.join("∧")} paired off as biomass. One survivor carries the rest.`);

  nodes.forEach((node) => node?.classList.add("leaving"));
  await wait(reduced() ? 0 : 300);

  const survivor = inject(a, b);
  const freed = [a.id, b.id];
  const slot = state.slots.get(a.id);
  freed.forEach((id) => state.slots.delete(id));
  state.colony = state.colony.filter((p) => !freed.includes(p.id));

  if (survivor) {
    state.slots.set(survivor.id, slot);
    state.colony.push(survivor);
  } else {
    credit(150);
    readout(point, 150, "whole genome paired off");
    setHint("The whole genome paired off — the creature dissolved into pure biomass. +150");
  }

  state.primed = null;
  render();
  if (survivor) pop(nodeFor(survivor.id));

  await wait(240);
  state.busy = false;
  endGeneration();
}

async function runLysis(a, b) {
  state.busy = true;
  const repeat = sharedCore(a, b);
  const reason = sameSet(coreOf(a), coreOf(b)) ? repeat.join("∧") : "a repeated outer gene";
  const gain = 60;

  const from = centreOf(a.id);
  const to = centreOf(b.id);
  const point = { x: (from.x + to.x) / 2, y: (from.y + to.y) / 2 };

  [a, b].forEach((p) => nodeFor(p.id)?.classList.add("bursting"));
  burst(point, true);
  readout(point, gain, `${reason} → 0`, true);
  showEvent({
    expr: `${reason} repeated in one wedge = 0`,
    meta: "lysis · scrap refund",
    gain,
    cold: true,
  });
  credit(gain, true);
  state.virulence = 1;
  setHint(`A gene repeats (${reason}) — the pair is dead. Both capsids burst.`);

  await wait(reduced() ? 0 : 440);
  [a.id, b.id].forEach((id) => state.slots.delete(id));
  state.colony = state.colony.filter((p) => p.id !== a.id && p.id !== b.id);
  state.primed = null;
  render();

  await wait(200);
  state.busy = false;
  endGeneration();
}

async function runCut(phage) {
  state.busy = true;
  const depth = phage.shells.length;
  const cost = 25 * depth;
  const { children, seam } = cutPair(phage);
  const point = centreOf(phage.id);

  nodeFor(phage.id)?.classList.add("leaving");
  burst(point, true);
  readout(point, -cost, `borrowed gene ${seam}`, true);
  showEvent({
    expr: `${phage.lineage} ⌋(…) → two daughters sharing ${seam}`,
    meta: `vichcheda · depth ${depth}`,
    gain: -cost,
    cold: true,
  });
  credit(-cost, true);
  setHint(`Genome cut at ${seam}. Two daughters bud off, and ${cost} biomass is owed.`);

  await wait(reduced() ? 0 : 320);
  const slot = state.slots.get(phage.id);
  state.slots.delete(phage.id);
  state.colony = state.colony.filter((p) => p.id !== phage.id);

  state.slots.set(children[0].id, slot);
  state.colony.push(...children);
  state.primed = null;
  render();
  children.forEach((child, i) => bud(nodeFor(child.id), i === 0 ? -1 : 1));

  await wait(260);
  state.busy = false;
  endGeneration();
}

async function runInfect(phage) {
  state.busy = true;
  const cfg = plate();
  const size = genomeSize(phage);
  const ok = size === cfg.receptor;
  const gain = ok ? 120 + 20 * size : -80;

  const node = nodeFor(phage.id);
  const dish = dishRect();
  setHint(ok ? "Docking on the receptor…" : "Approaching the host…");

  node?.classList.add("primed");
  node?.style.setProperty("--x", "50%");
  node?.style.setProperty("--y", "50%");
  await wait(reduced() ? 0 : 520);

  const point = { x: dish.width / 2, y: dish.height / 2 };
  el.host.classList.add(ok ? "hit" : "reject");
  node?.classList.add(ok ? "leaving" : "bursting");
  burst(point, !ok);
  readout(point, gain, ok ? `receptor ${size} matched` : `receptor wants ${cfg.receptor}`, !ok);
  showEvent({
    expr: ok
      ? `infected with ${phage.lineage} ⌋(…) at ${size} genes`
      : `rejected ${phage.lineage} ⌋(…) — ${size} genes, receptor ${cfg.receptor}`,
    meta: ok ? "host · infection counted" : "host · rejected",
    gain,
    cold: !ok,
  });
  credit(gain, !ok);
  if (ok) state.infections += 1;
  else state.virulence = 1;
  setHint(
    ok
      ? `The host accepted a ${size}-gene genome. Infection counted.`
      : `The host rejected a ${size}-gene genome — it needs exactly ${cfg.receptor}.`
  );

  await wait(reduced() ? 0 : 420);
  el.host.classList.remove("hit", "reject");
  state.slots.delete(phage.id);
  state.colony = state.colony.filter((p) => p.id !== phage.id);
  state.primed = null;
  render();

  await wait(200);
  state.busy = false;
  endGeneration();
}

function pop(node) {
  if (!node || reduced()) return;
  node.animate(
    [
      { transform: "translate(-50%, -50%) scale(.6)", opacity: 0 },
      { offset: 0.6, transform: "translate(-50%, -50%) scale(1.08)", opacity: 1 },
      { transform: "translate(-50%, -50%) scale(1)", opacity: 1 },
    ],
    { duration: 480, easing: "cubic-bezier(.2,.9,.3,1.2)" }
  );
}

function bud(node, side) {
  if (!node || reduced()) return;
  node.animate(
    [
      { transform: `translate(calc(-50% + ${side * 18}px), -50%) scale(.6)`, opacity: 0 },
      { offset: 0.6, transform: "translate(-50%, -50%) scale(1.06)", opacity: 1 },
      { transform: "translate(-50%, -50%) scale(1)", opacity: 1 },
    ],
    { duration: 540, easing: "cubic-bezier(.2,.9,.3,1.25)" }
  );
}

/* -------------------------------------------------------------- cycling */

function endGeneration() {
  state.generations += 1;

  while (state.colony.length < FILL) {
    const born = makePhage();
    state.colony.push(born);
  }

  if (!hasPair() && seedPair()) {
    setHint("No injection left on the plate — a fresh strain drifted in.");
  }

  render();

  if (state.infections >= plate().quota) finishPlate();
}

function finishPlate() {
  const last = state.plateIndex === PLATES.length - 1;
  el.banner.hidden = false;
  el.bannerMark.textContent = last ? "✦" : "◇";
  el.bannerKicker.textContent = last ? "CULTURE CLEARED" : "PLATE CLEARED";
  el.bannerTitle.textContent = last ? "The whole culture fell." : "The colony fell.";
  el.bannerText.textContent = last
    ? `Every plate infected. Final biomass ${state.biomass}.`
    : "Every infection matched the receptor.";
  el.bannerButton.textContent = last ? "Start over" : "Next plate";
}

function startPlate(index) {
  state.plateIndex = index;
  state.colony = [];
  state.slots = new Map();
  state.primed = null;
  state.virulence = 1;
  state.generations = 0;
  state.infections = 0;
  state.busy = false;
  while (state.colony.length < FILL) state.colony.push(makePhage());
  seedPair();

  el.eventCard.className = "event-card empty";
  el.eventCard.innerHTML =
    "<span>φ</span><p>Nothing has happened yet. Prime a phage and find one that shares a gene.</p>";
  setHint("Click a phage to prime it.");
  tweenBiomass();
  render();
}

/* ------------------------------------------------------------- dispatch */

function handlePhage(phage) {
  if (state.busy) return;

  if (!state.primed) {
    state.primed = phage;
    setHint("Primed. Amber filaments run to every phage that shares a gene.");
    render();
    return;
  }

  if (state.primed.id === phage.id) {
    state.primed = null;
    setHint("Click a phage to prime it.");
    render();
    return;
  }

  const kind = relation(state.primed, phage);
  if (kind === "dock") { runInject(state.primed, phage); return; }
  if (kind === "zero") { runLysis(state.primed, phage); return; }

  state.primed = phage;
  setHint(
    state.primed.lineage === phage.lineage
      ? "No gene in common down in the genome — nothing to inject."
      : "Different strain. These two cannot pair."
  );
  render();
}

el.colony.addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  const node = event.target.closest(".phage");
  if (!node || state.busy) return;

  const phage = state.colony.find((p) => p.id === Number(node.dataset.id));
  if (!phage) return;

  if (chip) {
    if (chip.hasAttribute("disabled")) return;
    if (chip.dataset.act === "cut") runCut(phage);
    if (chip.dataset.act === "send") runInfect(phage);
    return;
  }

  handlePhage(phage);
});

el.host.addEventListener("click", () => {
  if (state.busy) return;
  if (!state.primed) {
    setHint("Prime a phage first, then send it into the host.");
    return;
  }
  runInfect(state.primed);
});

el.reset.addEventListener("click", () => {
  el.banner.hidden = true;
  state.biomass = 0;
  state.shownBiomass = 0;
  startPlate(state.plateIndex);
});

el.bannerButton.addEventListener("click", () => {
  el.banner.hidden = true;
  const last = state.plateIndex === PLATES.length - 1;
  if (last) {
    state.biomass = 0;
    state.shownBiomass = 0;
    startPlate(0);
  } else {
    startPlate(state.plateIndex + 1);
  }
});

document.addEventListener("keydown", (event) => {
  if (state.busy) return;
  const key = event.key.toLowerCase();
  if (key === "escape" && state.primed) {
    state.primed = null;
    setHint("Click a phage to prime it.");
    render();
  }
  if (key === "c" && state.primed && coreOf(state.primed).length >= 3 && state.colony.length < CAPACITY) {
    runCut(state.primed);
  }
  if (key === "h" && state.primed) runInfect(state.primed);
});

window.addEventListener("resize", drawFilaments);

startPlate(0);
