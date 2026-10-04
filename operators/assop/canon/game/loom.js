/* Thread Loom — a playable string-diagram skin over baked SandhiCanon steps.
 *
 * Algebra is never inferred here. chamber-data.json was produced by running
 * SandhiCanon one rewrite at a time. The game asks the player to discover the
 * same pair and seam; the baked step supplies the exact scalar and residual.
 *
 * Diagram convention: every panel is a chain of contraction nodes (the pins)
 * with one open leg per wedge factor. Two panels face each other across the
 * gutter; stitching bends the shared legs into a cup, and the closed loop that
 * forms is exactly the overlap scalar.
 */

const SVG_NS = "http://www.w3.org/2000/svg";
const THREAD_COLOURS = ["#58a6b4", "#9e80ad", "#efae45", "#73986a", "#d9584b"];
const GEO = { rowH: 34, shellDX: 96, legRun: 150, ringR: 17, gutter: 230, rowGap: 54, pad: 26 };

const OBJECTIVES = {
  flat: "Close one shared leg and weave the two diagrams into one.",
  chain: "Make two clean stitches. The first residual must feed the second.",
  rank2: "Find the two-leg seam and close it as one determinant loop.",
  deep: "Follow the nesting to depth three; stitch the complete inner seam.",
  bisector: "Weave all three diagrams. The final repeated leg must tear to zero.",
};

const state = {
  levels: [],
  levelIndex: 0,
  stepIndex: 0,
  panels: [],
  scalars: [],
  score: 0,
  moves: 0,
  busy: false,
  tool: "stitch",
  drag: null,
  selected: null,
  justDragged: false,
  ends: new Map(),
  completed: new Set(),
  unlocked: 0,
};

const el = {
  levelList: document.getElementById("levelList"),
  levelKicker: document.getElementById("levelKicker"),
  levelTitle: document.getElementById("levelTitle"),
  objective: document.getElementById("objective"),
  stage: document.getElementById("loomStage"),
  canvas: document.getElementById("loomCanvas"),
  bursts: document.getElementById("burstLayer"),
  zero: document.getElementById("zeroStamp"),
  tray: document.getElementById("scalarTray"),
  status: document.getElementById("statusLine"),
  score: document.getElementById("score"),
  moves: document.getElementById("moves"),
  levelHud: document.getElementById("levelHud"),
  progress: document.getElementById("progressBar"),
  grade: document.getElementById("grade"),
  gradeCopy: document.getElementById("gradeCopy"),
  engineInput: document.getElementById("engineInput"),
  engineTarget: document.getElementById("engineTarget"),
  tapeBody: document.getElementById("tapeBody"),
  tapeToggle: document.getElementById("tapeToggle"),
  hint: document.getElementById("hintButton"),
  reset: document.getElementById("resetButton"),
  complete: document.getElementById("complete"),
  completeTitle: document.getElementById("completeTitle"),
  completeCopy: document.getElementById("completeCopy"),
  endMoves: document.getElementById("endMoves"),
  endScalars: document.getElementById("endScalars"),
  endGrade: document.getElementById("endGrade"),
  next: document.getElementById("nextButton"),
};

const level = () => state.levels[state.levelIndex];
const currentStep = () => level().steps[state.stepIndex];
const towerKey = (tower) => JSON.stringify(tower);
const allSymbols = (tower) => tower.flatMap((shell) => shell.nodes);
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function loadProgress() {
  try {
    state.unlocked = Number(localStorage.getItem("threadLoomUnlocked") || 0);
    state.completed = new Set(JSON.parse(localStorage.getItem("threadLoomComplete") || "[]"));
  } catch {
    state.unlocked = 0;
    state.completed = new Set();
  }
}

function saveProgress() {
  try {
    localStorage.setItem("threadLoomUnlocked", String(state.unlocked));
    localStorage.setItem("threadLoomComplete", JSON.stringify([...state.completed]));
  } catch {
    // Storage is optional; the game remains playable without it.
  }
}

/* ---------------------------------------------------------------- model */

function consumedIndices(step) {
  const after = step.panelsAfter.map(towerKey);
  const used = new Set();
  const consumed = [];

  step.panelsBefore.forEach((tower, index) => {
    const key = towerKey(tower);
    const unchanged = after.findIndex((candidate, j) => candidate === key && !used.has(j));
    if (unchanged < 0) consumed.push(index);
    else used.add(unchanged);
  });

  return consumed.length >= 2 ? consumed.slice(0, 2) : step.panelsBefore.map((_, i) => i).slice(0, 2);
}

function sharedSymbols(a, b) {
  const right = new Set(allSymbols(b));
  return [...new Set(allSymbols(a).filter((symbol) => right.has(symbol)))];
}

function expectedSeam(step) {
  const pair = consumedIndices(step);
  const common = sharedSymbols(step.panelsBefore[pair[0]], step.panelsBefore[pair[1]]);
  if (step.zero) return common;

  const baked = new Set([...step.seam.rows, ...step.seam.cols]);
  const seam = common.filter((symbol) => baked.has(symbol));
  return seam.length ? seam : common;
}

function availableSymbols() {
  const counts = new Map();
  state.panels.forEach((tower) => {
    new Set(allSymbols(tower)).forEach((symbol) => counts.set(symbol, (counts.get(symbol) || 0) + 1));
  });
  return new Set([...counts].filter(([, count]) => count > 1).map(([symbol]) => symbol));
}

function towerExpression(tower, depth = 0) {
  const shell = tower[depth];
  const inner = depth + 1 < tower.length
    ? [...shell.nodes, towerExpression(tower, depth + 1)]
    : shell.nodes;
  return `${shell.pin}⌋(${inner.join("∧")})`;
}

function gradeForMoves() {
  const ideal = Math.max(1, level().steps.length);
  if (state.moves <= ideal) return "S";
  if (state.moves <= ideal + 1) return "A";
  if (state.moves <= ideal + 3) return "B";
  return "C";
}

/* --------------------------------------------------------------- layout */

const colourFor = (depth) => THREAD_COLOURS[depth % THREAD_COLOURS.length];
const termEnds = (tower) => tower.reduce((total, shell) => total + shell.nodes.length, 0);
const termHeight = (tower) => Math.max(termEnds(tower) * GEO.rowH, 92);
const termReach = (tower) => (tower.length - 1) * GEO.shellDX + GEO.legRun;

function placeTerm(tower, index, dir, anchorX, centreY) {
  const height = termHeight(tower);
  const top = centreY - height / 2 + GEO.rowH / 2;
  const endX = anchorX + dir * ((tower.length - 1) * GEO.shellDX + GEO.legRun);
  let row = 0;

  const shells = tower.map((shell, depth) => {
    const ends = shell.nodes.map((sym) => ({ sym, x: endX, y: top + row++ * GEO.rowH }));
    const y = ends.reduce((sum, end) => sum + end.y, 0) / ends.length;
    return { pin: shell.pin, depth, x: anchorX + dir * depth * GEO.shellDX, y, ends };
  });

  return { index, tower, dir, anchorX, endX, centreY, height, shells };
}

const termBox = (term) => ({
  x0: Math.min(term.anchorX, term.endX) - GEO.ringR - 16,
  x1: Math.max(term.anchorX, term.endX) + GEO.ringR + 16,
});

/* Terms are laid out in content coordinates and the viewBox is fitted to the
 * result, so a two-leg diagram fills the stage just as a twelve-leg one does. */
function layoutScene(panels) {
  const rows = [];
  let y = 0;

  for (let i = 0; i < panels.length; i += 2) {
    const slots = [i, i + 1].filter((k) => k < panels.length);
    const rowHeight = Math.max(...slots.map((k) => termHeight(panels[k])));
    const leftReach = termReach(panels[slots[0]]);

    rows.push(slots.map((k, slot) => placeTerm(
      panels[k],
      k,
      slot === 0 ? 1 : -1,
      slot === 0 ? 0 : leftReach + GEO.gutter + termReach(panels[k]),
      y + rowHeight / 2,
    )));

    y += rowHeight + GEO.rowGap;
  }

  const spans = rows.map((row) => row.reduce((box, term) => {
    const own = termBox(term);
    return { x0: Math.min(box.x0, own.x0), x1: Math.max(box.x1, own.x1) };
  }, { x0: Infinity, x1: -Infinity }));

  const x0 = Math.min(...spans.map((span) => span.x0));
  const x1 = Math.max(...spans.map((span) => span.x1));
  const centre = (x0 + x1) / 2;

  const terms = rows.flatMap((row, index) => {
    const shift = centre - (spans[index].x0 + spans[index].x1) / 2;
    return shift ? row.map((term) => shiftTerm(term, shift)) : row;
  });

  const labelPad = 30;
  const captionPad = state.tool === "inspect" ? 38 : 18;
  const top = Math.min(...terms.map((term) => term.centreY - term.height / 2)) - labelPad;
  const bottom = Math.max(...terms.map((term) => term.centreY + term.height / 2)) + captionPad;

  // A floor on the view keeps the zoom steady: a lone residual must not balloon
  // to twice the size of the pair it came from.
  const view = fitView(x0 - GEO.pad, top - GEO.pad, x1 - x0 + GEO.pad * 2, bottom - top + GEO.pad * 2);
  return { terms, view, centre: { x: centre, y: (top + bottom) / 2 } };
}

function fitView(x, y, width, height) {
  const minWidth = 640;
  const minHeight = 220;
  if (width < minWidth) {
    x -= (minWidth - width) / 2;
    width = minWidth;
  }
  if (height < minHeight) {
    y -= (minHeight - height) / 2;
    height = minHeight;
  }
  return [x, y, width, height];
}

function shiftTerm(term, dx) {
  return {
    ...term,
    anchorX: term.anchorX + dx,
    endX: term.endX + dx,
    shells: term.shells.map((shell) => ({
      ...shell,
      x: shell.x + dx,
      ends: shell.ends.map((end) => ({ ...end, x: end.x + dx })),
    })),
  };
}

/* --------------------------------------------------------------- render */

function trunkPath(term) {
  return term.shells.map((shell, i) => {
    if (!i) return `M ${shell.x} ${shell.y}`;
    const prev = term.shells[i - 1];
    return `C ${prev.x + term.dir * 48} ${prev.y}, ${shell.x - term.dir * 48} ${shell.y}, ${shell.x} ${shell.y}`;
  }).join(" ");
}

function legPath(term, shell, end) {
  const sx = shell.x + term.dir * GEO.ringR;
  return `M ${sx} ${shell.y} C ${sx + term.dir * 74} ${shell.y}, ${end.x - term.dir * 74} ${end.y}, ${end.x} ${end.y}`;
}

function termMarkup(term, available, arrived) {
  const legs = [];
  const rings = [];
  const dots = [];

  term.shells.forEach((shell) => {
    const colour = colourFor(shell.depth);

    shell.ends.forEach((end) => {
      const seamReady = available.has(end.sym);
      legs.push(`<path class="leg${seamReady ? " seam-ready" : ""}" style="--thread:${colour}"
        data-wire="${term.index}:${end.sym}" d="${legPath(term, shell, end)}"/>`);

      const dotClass = ["end-dot"];
      if (seamReady) dotClass.push("available", "pulsing");
      if (arrived.has(end.sym)) dotClass.push("fresh");

      dots.push(`<g class="end-group" data-panel="${term.index}" data-symbol="${end.sym}"
        style="--thread:${colour}" role="button" tabindex="0" aria-label="Leg ${end.sym}, diagram ${term.index + 1}">
        <circle class="end-halo" cx="${end.x}" cy="${end.y}" r="14"/>
        <circle class="${dotClass.join(" ")}" cx="${end.x}" cy="${end.y}" r="6.5"/>
        <text class="end-label" x="${end.x}" y="${end.y - 17}" text-anchor="middle">${end.sym}</text>
        <circle class="end-hit" cx="${end.x}" cy="${end.y}" r="18"/>
      </g>`);
    });

    rings.push(`<g style="--thread:${colour}">
      <circle class="node-ring" cx="${shell.x}" cy="${shell.y}" r="${GEO.ringR}"/>
      <text class="node-label" x="${shell.x}" y="${shell.y}">${shell.pin}</text>
    </g>`);
  });

  const caption = state.tool === "inspect"
    ? `<text class="term-caption" x="${(term.anchorX + term.endX) / 2}"
        y="${term.centreY + term.height / 2 + 28}">${towerExpression(term.tower)}</text>`
    : "";

  return `<g class="term entering" data-panel="${term.index}">
    <path class="trunk" d="${trunkPath(term)}"/>
    ${legs.join("")}${rings.join("")}${dots.join("")}${caption}
  </g>`;
}

function renderPanels(arrivedSymbols = []) {
  const arrived = new Set(arrivedSymbols);
  const available = availableSymbols();
  if (!state.panels.length) {
    el.canvas.innerHTML = `<g id="overlay"></g>`;
    state.ends = new Map();
    return;
  }

  const scene = layoutScene(state.panels);
  state.scene = scene;
  state.ends = new Map();
  scene.terms.forEach((term) => term.shells.forEach((shell) => shell.ends.forEach((end) => {
    state.ends.set(`${term.index}:${end.sym}`, { x: end.x, y: end.y, dir: term.dir });
  })));

  el.canvas.setAttribute("viewBox", scene.view.join(" "));
  el.canvas.setAttribute("preserveAspectRatio", "xMidYMid meet");
  el.canvas.innerHTML = scene.terms.map((term) => termMarkup(term, available, arrived)).join("")
    + `<g id="overlay"></g>`;
}

function renderLevels() {
  el.levelList.innerHTML = state.levels.map((item, index) => {
    const locked = index > state.unlocked;
    const classes = [
      index === state.levelIndex ? "active" : "",
      state.completed.has(item.id) ? "complete-level" : "",
    ].filter(Boolean).join(" ");
    return `<button data-level="${index}" class="${classes}" ${locked ? "disabled" : ""}>
      <span class="level-number">${state.completed.has(item.id) ? "✓" : index + 1}</span>
      <span class="level-name">${item.title}</span>
      <span class="level-lock">${locked ? "LOCK" : `${item.steps.length}×`}</span>
    </button>`;
  }).join("");
}

function renderHud() {
  el.score.textContent = String(Math.max(0, state.score)).padStart(4, "0");
  el.moves.textContent = String(state.moves).padStart(2, "0");
  el.levelHud.textContent = `${state.levelIndex + 1} / ${state.levels.length}`;
  el.levelKicker.textContent = `PATTERN ${String(state.levelIndex + 1).padStart(2, "0")}`;
  el.levelTitle.textContent = level().title;
  el.objective.textContent = OBJECTIVES[level().id] || level().note;
  el.engineInput.textContent = level().input.expr;
  el.engineTarget.textContent = level().result.expr;
  el.progress.style.width = `${(state.stepIndex / level().steps.length) * 100}%`;

  const liveGrade = gradeForMoves();
  el.grade.textContent = liveGrade === "S" ? "MASTER WEAVE" : liveGrade === "A" ? "CLEAN WEAVE" : "FRAYED WEAVE";
  el.gradeCopy.textContent = `${level().steps.length} ideal stitch${level().steps.length === 1 ? "" : "es"} · currently ${state.moves}.`;
}

function renderTray() {
  el.tray.innerHTML = state.scalars.length
    ? state.scalars.map((scalar) => `<b>${scalar}</b>`).join("")
    : "<em>empty</em>";
}

function renderAll(arrived = []) {
  renderPanels(arrived);
  renderLevels();
  renderHud();
  renderTray();
}

/* ---------------------------------------------------------- svg helpers */

const overlay = () => el.canvas.querySelector("#overlay");
const endGroup = (panel, symbol) => el.canvas.querySelector(`.end-group[data-panel="${panel}"][data-symbol="${symbol}"]`);
const endPoint = (panel, symbol) => state.ends.get(`${panel}:${symbol}`);

function svgPoint(clientX, clientY) {
  const point = el.canvas.createSVGPoint();
  point.x = clientX;
  point.y = clientY;
  return point.matrixTransform(el.canvas.getScreenCTM().inverse());
}

function stagePixel(x, y) {
  const point = el.canvas.createSVGPoint();
  point.x = x;
  point.y = y;
  const screen = point.matrixTransform(el.canvas.getScreenCTM());
  const box = el.stage.getBoundingClientRect();
  return { x: screen.x - box.left, y: screen.y - box.top };
}

function cupPath(a, b) {
  const reach = Math.max(70, Math.abs(b.x - a.x) * .42);
  return `M ${a.x} ${a.y} C ${a.x + a.dir * reach} ${a.y}, ${b.x + b.dir * reach} ${b.y}, ${b.x} ${b.y}`;
}

function overlayPath(className, d) {
  const path = document.createElementNS(SVG_NS, "path");
  path.setAttribute("class", className);
  path.setAttribute("d", d);
  overlay().append(path);
  return path;
}

function clearOverlay() {
  const layer = overlay();
  if (layer) layer.innerHTML = "";
}

function closeCups(panelA, panelB, symbols) {
  clearOverlay();
  const centres = [];

  symbols.forEach((symbol) => {
    const a = endPoint(panelA, symbol);
    const b = endPoint(panelB, symbol);
    if (!a || !b) return;

    const path = overlayPath("cup closing", cupPath(a, b));
    path.style.setProperty("--length", path.getTotalLength());
    centres.push({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 });

    [`${panelA}:${symbol}`, `${panelB}:${symbol}`].forEach((key) => {
      el.canvas.querySelector(`.leg[data-wire="${key}"]`)?.classList.add("live");
    });
  });

  if (!centres.length) return state.scene?.centre || { x: 0, y: 0 };
  return {
    x: centres.reduce((sum, p) => sum + p.x, 0) / centres.length,
    y: centres.reduce((sum, p) => sum + p.y, 0) / centres.length,
  };
}

/* ------------------------------------------------------------ feedback */

function setStatus(text) {
  el.status.textContent = text;
}

function fray(message) {
  state.moves += 2;
  state.score = Math.max(0, state.score - 30);
  el.stage.classList.add("fray");
  setTimeout(() => el.stage.classList.remove("fray"), 390);
  setStatus(message);
  renderHud();
}

function releaseBead(at, scalar) {
  const spot = stagePixel(at.x, at.y);

  const bead = document.createElement("span");
  bead.className = "scalar-bead";
  bead.style.left = `${spot.x}px`;
  bead.style.top = `${spot.y}px`;
  bead.textContent = scalar;
  el.bursts.append(bead);

  const sparks = document.createElement("span");
  sparks.className = "thread-sparks";
  sparks.style.left = `${spot.x}px`;
  sparks.style.top = `${spot.y}px`;
  sparks.innerHTML = Array.from({ length: 12 }, (_, i) => `<i style="--a:${i * 30}deg"></i>`).join("");
  el.bursts.append(sparks);

  setTimeout(() => {
    bead.remove();
    sparks.remove();
  }, 1050);
}

function arrivedSymbols(step, pair) {
  if (!step.panelsAfter.length) return [];
  const original = new Set(allSymbols(step.panelsBefore[pair[0]]));
  const after = new Set(step.panelsAfter.flatMap(allSymbols));
  return [...after].filter((symbol) => !original.has(symbol));
}

/* ---------------------------------------------------------- selection */

function clearSelection() {
  state.selected = null;
  el.canvas.querySelectorAll(".end-group.target, .end-group.picked").forEach((node) => {
    node.classList.remove("target", "picked");
  });
}

function markTwins(panel, symbol) {
  el.canvas.querySelectorAll(`.end-group[data-symbol="${symbol}"]`).forEach((node) => {
    if (Number(node.dataset.panel) !== panel) node.classList.add("target");
  });
}

function selectEnd(node) {
  if (state.busy || state.tool !== "stitch" || state.justDragged) return;
  const panel = Number(node.dataset.panel);
  const symbol = node.dataset.symbol;

  if (!state.selected) {
    state.selected = { panel, symbol, node };
    node.classList.add("picked");
    markTwins(panel, symbol);
    setStatus(`Leg ${symbol} picked up. Choose its twin across the gutter.`);
    return;
  }

  const selected = state.selected;
  if (selected.node === node) {
    clearSelection();
    setStatus("Leg released.");
    return;
  }

  if (selected.symbol === symbol && selected.panel !== panel) {
    clearSelection();
    attemptStitch(selected.panel, panel, symbol);
    return;
  }

  clearSelection();
  selectEnd(node);
}

/* --------------------------------------------------------------- play */

async function attemptStitch(panelA, panelB, symbol) {
  if (state.busy || panelA === panelB) return;

  const step = currentStep();
  const pair = consumedIndices(step);
  const chosen = [panelA, panelB].sort((a, b) => a - b);
  const expected = [...pair].sort((a, b) => a - b);
  const seam = expectedSeam(step);

  state.moves += 1;

  const rightPair = chosen[0] === expected[0] && chosen[1] === expected[1];
  const rightSymbol = seam.includes(symbol);
  if (!rightPair || !rightSymbol) {
    // attemptStitch already charged one move; fray charges one additional move.
    state.moves -= 1;
    fray(rightPair
      ? `${symbol} is shared, but it is not the seam selected by the grade gate.`
      : "Those diagrams share a leg, but cupping them now will not reach normal form.");
    return;
  }

  state.busy = true;
  state.score += 100 + seam.length * 75 + step.panelsBefore[pair[0]].length * 25;
  renderHud();
  setStatus(`Seam ${seam.join(" · ")} locked. Bending the legs into a cup…`);

  const centre = closeCups(pair[0], pair[1], seam);
  await wait(560);

  if (step.zero) {
    state.scalars.push("0");
    renderTray();
    el.zero.hidden = false;
    el.stage.classList.add("fray");
    el.canvas.querySelectorAll(".leg").forEach((leg) => leg.classList.add("tear"));
    setStatus("A leg repeats inside the bundle. Antisymmetry tears the diagram to zero.");
    await wait(800);
    el.canvas.querySelectorAll(".term").forEach((term) => term.classList.add("consuming"));
    state.panels = [];
    state.stepIndex += 1;
    renderHud();
    state.busy = false;
    finishPattern(true);
    return;
  }

  releaseBead(centre, step.coeff);
  state.scalars.push(step.coeff);
  renderTray();
  el.stage.classList.add("finish");
  setTimeout(() => el.stage.classList.remove("finish"), 650);
  setStatus(`The loop closed into ${step.coeff}. Open legs are being rewoven.`);

  pair.forEach((index) => {
    el.canvas.querySelector(`.term[data-panel="${index}"]`)?.classList.add("consuming");
  });
  await wait(540);

  const arrived = arrivedSymbols(step, pair);
  state.panels = step.panelsAfter;
  state.stepIndex += 1;
  renderAll(arrived);
  await wait(420);

  state.busy = false;
  if (state.stepIndex >= level().steps.length) {
    finishPattern(false);
  } else {
    setStatus("The residual still has a twin. Find the next seam.");
  }
}

function finishPattern(zero) {
  state.completed.add(level().id);
  state.unlocked = Math.max(state.unlocked, Math.min(state.levelIndex + 1, state.levels.length - 1));
  saveProgress();
  renderLevels();
  el.progress.style.width = "100%";

  const grade = gradeForMoves();
  el.endMoves.textContent = state.moves;
  el.endScalars.textContent = state.scalars.length;
  el.endGrade.textContent = grade;
  el.completeTitle.textContent = zero ? "The weave vanished." : "One open bundle remains.";
  el.completeCopy.textContent = zero
    ? "The final stitch repeated a leg. Antisymmetry erased the whole diagram exactly as the engine predicted."
    : "Every closed cup became a scalar bead; the open legs survived in the residual normal form.";
  el.next.textContent = state.levelIndex === state.levels.length - 1 ? "Weave again ↺" : "Next pattern →";

  setTimeout(() => { el.complete.hidden = false; }, 500);
}

function hint() {
  if (state.busy || state.stepIndex >= level().steps.length) return;
  const step = currentStep();
  const pair = consumedIndices(step);
  const seam = expectedSeam(step);

  pair.forEach((index) => seam.forEach((symbol) => {
    endGroup(index, symbol)?.classList.add("target");
    el.canvas.querySelector(`.leg[data-wire="${index}:${symbol}"]`)?.classList.add("hint-leg");
  }));

  setStatus(`Hint: the seam is ${seam.join(" · ")}.`);
  state.score = Math.max(0, state.score - 20);
  renderHud();
  setTimeout(() => {
    el.canvas.querySelectorAll(".hint-leg").forEach((node) => node.classList.remove("hint-leg"));
    el.canvas.querySelectorAll(".end-group.target").forEach((node) => node.classList.remove("target"));
  }, 1500);
}

/* --------------------------------------------------------------- drag */

function beginDrag(event, node) {
  if (state.busy || state.tool !== "stitch") return;
  // A picked end means the player is using click-to-stitch; let the click
  // handler choose the destination without replacing the selection.
  if (state.selected) return;
  event.preventDefault();

  const panel = Number(node.dataset.panel);
  const symbol = node.dataset.symbol;
  const start = endPoint(panel, symbol);
  const path = overlayPath("drag-line", cupPath(start, { ...start, dir: -start.dir }));

  state.drag = { panel, symbol, start, path, node };
  node.classList.add("picked");
  markTwins(panel, symbol);
  el.canvas.setPointerCapture?.(event.pointerId);
}

function moveDrag(event) {
  if (!state.drag) return;
  const point = svgPoint(event.clientX, event.clientY);
  const { start } = state.drag;
  const reach = Math.max(50, Math.abs(point.x - start.x) * .4);
  state.drag.path.setAttribute(
    "d",
    `M ${start.x} ${start.y} C ${start.x + start.dir * reach} ${start.y}, ${point.x - start.dir * reach} ${point.y}, ${point.x} ${point.y}`,
  );
}

function endDrag(event) {
  if (!state.drag) return;
  const drag = state.drag;
  const target = document.elementFromPoint(event.clientX, event.clientY)?.closest?.(".end-group");

  drag.node.classList.remove("picked");
  el.canvas.querySelectorAll(".end-group.target").forEach((node) => node.classList.remove("target"));
  state.drag = null;
  state.justDragged = true;
  setTimeout(() => { state.justDragged = false; }, 80);
  clearOverlay();

  if (target === drag.node) {
    state.justDragged = false;
    selectEnd(target);
    state.justDragged = true;
    return;
  }

  if (!target || target.dataset.symbol !== drag.symbol || Number(target.dataset.panel) === drag.panel) {
    fray("The loose leg missed its twin. Two moves lost to the fray.");
    return;
  }

  attemptStitch(drag.panel, Number(target.dataset.panel), drag.symbol);
}

/* ------------------------------------------------------------- control */

function loadLevel(index) {
  if (index > state.unlocked || state.busy) return;

  state.levelIndex = index;
  state.stepIndex = 0;
  state.panels = level().input.panels;
  state.scalars = [];
  state.moves = 0;
  state.busy = false;
  state.drag = null;
  state.selected = null;

  el.zero.hidden = true;
  el.complete.hidden = true;
  el.bursts.innerHTML = "";
  setStatus("Pick up a gold leg end and cup it against its twin.");
  renderAll();
}

el.canvas.addEventListener("pointerdown", (event) => {
  const node = event.target.closest?.(".end-group");
  if (node) beginDrag(event, node);
});
el.canvas.addEventListener("click", (event) => {
  const node = event.target.closest?.(".end-group");
  if (node) selectEnd(node);
});
window.addEventListener("pointermove", moveDrag);
window.addEventListener("pointerup", endDrag);

el.levelList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-level]");
  if (button) loadLevel(Number(button.dataset.level));
});

document.querySelectorAll(".tool").forEach((button) => {
  button.addEventListener("click", () => {
    state.tool = button.dataset.tool;
    document.querySelectorAll(".tool").forEach((node) => node.classList.toggle("active", node === button));
    el.tapeBody.hidden = state.tool !== "inspect";
    el.tapeToggle.textContent = el.tapeBody.hidden ? "+" : "−";
    renderPanels();
    setStatus(state.tool === "inspect"
      ? "Scientist tape exposed: each diagram is captioned with its contraction."
      : "Pick up a gold leg end and cup it against its twin.");
  });
});

el.tapeToggle.addEventListener("click", () => {
  el.tapeBody.hidden = !el.tapeBody.hidden;
  el.tapeToggle.textContent = el.tapeBody.hidden ? "+" : "−";
});
el.hint.addEventListener("click", hint);
el.reset.addEventListener("click", () => loadLevel(state.levelIndex));
el.next.addEventListener("click", () => {
  el.complete.hidden = true;
  loadLevel(state.levelIndex === state.levels.length - 1 ? 0 : state.levelIndex + 1);
});

fetch("chamber-data.json")
  .then((response) => {
    if (!response.ok) throw new Error("chamber-data.json unavailable");
    return response.json();
  })
  .then((levels) => {
    state.levels = levels;
    loadProgress();
    loadLevel(0);
  })
  .catch((error) => {
    setStatus(`${error.message}. Run bake_chamber.py to rebuild the baked steps.`);
  });

window.threadLoom = { state, loadLevel, attemptStitch, hint };
