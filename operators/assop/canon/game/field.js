const SIZE = 6;
const UPPER_BLADES = ["∞", "α", "β", "Ω", "n"];
const LOWER_SYMBOLS = ["P", "Q", "R", "A", "B", "C", "u", "v", "w", "1", "2", "3"];

const state = {
  grid: [],
  tool: "move",
  score: 0,
  chain: 1,
  maxDepth: 0,
  nextId: 1,
  dragIndex: null,
  selectedIndex: null,
  busy: false
};

const gridElement = document.querySelector("#patternGrid");
const statusElement = document.querySelector("#fieldStatus");
const logElement = document.querySelector("#rewriteLog");

function randomItem(items) {
  return items[Math.floor(Math.random() * items.length)];
}

function leaf(up = randomItem(UPPER_BLADES)) {
  let first = randomItem(LOWER_SYMBOLS);
  let second = randomItem(LOWER_SYMBOLS);
  while (second === first) second = randomItem(LOWER_SYMBOLS);
  return {
    id: state.nextId++,
    up,
    nodes: [first, second],
    depth: 0,
    children: []
  };
}

function cloneTerm(term) {
  return {
    ...term,
    id: state.nextId++,
    nodes: [...term.nodes],
    children: term.children.map(cloneTerm)
  };
}

function initializeGrid() {
  state.grid = Array(SIZE * SIZE).fill(null);
  for (let index = 0; index < state.grid.length; index++) {
    let candidate = leaf();
    let attempts = 0;
    while (createsImmediateMatch(index, candidate.up) && attempts++ < 20) {
      candidate = leaf();
    }
    state.grid[index] = candidate;
  }
  render();
  updateStats();
}

function createsImmediateMatch(index, up) {
  const row = Math.floor(index / SIZE);
  const column = index % SIZE;
  const leftMatch = column >= 2
    && state.grid[index - 1]?.up === up
    && state.grid[index - 2]?.up === up;
  const upMatch = row >= 2
    && state.grid[index - SIZE]?.up === up
    && state.grid[index - SIZE * 2]?.up === up;
  return leftMatch || upMatch;
}

function render() {
  gridElement.innerHTML = "";
  state.grid.forEach((term, index) => {
    const tile = document.createElement("div");
    tile.className = "field-tile";
    if (state.selectedIndex === index) tile.classList.add("drop-target");
    if (term.depth) tile.classList.add("has-depth");
    tile.draggable = !state.busy;
    tile.dataset.index = index;
    tile.dataset.up = term.up;
    tile.innerHTML = `
      <span class="tile-grade">G${term.nodes.length}</span>
      ${renderTermGlyph(term)}
      ${term.depth ? `<span class="tile-depth">D${term.depth}</span>` : ""}
    `;

    tile.addEventListener("dragstart", handleDragStart);
    tile.addEventListener("dragend", handleDragEnd);
    tile.addEventListener("dragover", handleDragOver);
    tile.addEventListener("dragleave", handleDragLeave);
    tile.addEventListener("drop", handleDrop);
    tile.addEventListener("click", () => handleTileClick(index));
    tile.addEventListener("mouseenter", () => inspect(term));
    tile.addEventListener("focus", () => inspect(term));
    tile.tabIndex = 0;
    gridElement.appendChild(tile);
  });
}

function handleDragStart(event) {
  if (state.busy || state.tool === "split") {
    event.preventDefault();
    return;
  }
  state.dragIndex = Number(event.currentTarget.dataset.index);
  event.currentTarget.classList.add("dragging");
  event.dataTransfer.effectAllowed = "move";
  event.dataTransfer.setData("text/plain", String(state.dragIndex));
}

function handleDragEnd(event) {
  event.currentTarget.classList.remove("dragging");
  document.querySelectorAll(".drop-target").forEach((tile) => tile.classList.remove("drop-target"));
  state.dragIndex = null;
}

function handleDragOver(event) {
  event.preventDefault();
  event.currentTarget.classList.add("drop-target");
}

function handleDragLeave(event) {
  event.currentTarget.classList.remove("drop-target");
}

function handleDrop(event) {
  event.preventDefault();
  const targetIndex = Number(event.currentTarget.dataset.index);
  const sourceIndex = Number(event.dataTransfer.getData("text/plain"));
  event.currentTarget.classList.remove("drop-target");
  performAction(sourceIndex, targetIndex);
}

function handleTileClick(index) {
  if (state.busy) return;
  inspect(state.grid[index]);

  if (state.tool === "split") {
    splitTerm(index);
    return;
  }

  if (state.selectedIndex === null) {
    state.selectedIndex = index;
    toast("Now choose an adjacent term");
    render();
    return;
  }

  const source = state.selectedIndex;
  state.selectedIndex = null;
  if (source === index) {
    render();
    return;
  }
  performAction(source, index);
}

async function performAction(sourceIndex, targetIndex) {
  if (state.busy) return;
  if (!areAdjacent(sourceIndex, targetIndex)) {
    toast("Terms must be adjacent");
    render();
    return;
  }

  if (state.tool === "move") {
    [state.grid[sourceIndex], state.grid[targetIndex]] =
      [state.grid[targetIndex], state.grid[sourceIndex]];
    addLog(`Swap cells ${sourceIndex + 1} and ${targetIndex + 1}.`);
    render();
    const matched = await resolveMatches();
    if (!matched) {
      state.chain = 1;
      statusElement.textContent = "No match · try another neighboring swap";
      updateStats();
    }
    return;
  }

  mergeTerms(sourceIndex, targetIndex);
}

function mergeTerms(sourceIndex, targetIndex) {
  const source = state.grid[sourceIndex];
  const target = state.grid[targetIndex];
  const shared = source.nodes.filter((node) => target.nodes.includes(node));

  if (source.up !== target.up && shared.length === 0) {
    toast("No Sandhi: match an upper blade or lower seam");
    return;
  }

  const up = source.up === target.up ? source.up : target.up;
  const nodes = [...new Set([...source.nodes, ...target.nodes])];
  const merged = {
    id: state.nextId++,
    up,
    nodes,
    depth: Math.max(source.depth, target.depth) + 1,
    children: [source, target]
  };

  state.grid[targetIndex] = merged;
  state.grid[sourceIndex] = leaf();
  state.score += 180 * merged.depth;
  state.maxDepth = Math.max(state.maxDepth, merged.depth);
  addLog(`Sandhi: ${formatTerm(source)} + ${formatTerm(target)} → depth ${merged.depth}.`);
  statusElement.textContent = `Merged at ${shared.join(", ") || `upper blade ${up}`} · hierarchy preserved`;
  floatScore(`+${180 * merged.depth}`);
  inspect(merged);
  updateStats();
  render();
}

function splitTerm(index) {
  const term = state.grid[index];
  if (!term.children.length) {
    toast("This is already an atomic term");
    return;
  }

  const destinations = [index, ...neighborIndexes(index)];
  const children = term.children.map(cloneTerm);
  children.forEach((child, childIndex) => {
    state.grid[destinations[childIndex]] = child;
  });
  state.score = Math.max(0, state.score - 40);
  addLog(`Viccheda: depth ${term.depth} term split into ${children.length} children.`);
  statusElement.textContent = "Viccheda complete · immediate children returned to the field";
  floatScore("−40");
  updateStats();
  render();
}

function areAdjacent(a, b) {
  const rowA = Math.floor(a / SIZE);
  const rowB = Math.floor(b / SIZE);
  const columnA = a % SIZE;
  const columnB = b % SIZE;
  return Math.abs(rowA - rowB) + Math.abs(columnA - columnB) === 1;
}

function neighborIndexes(index) {
  const candidates = [index - 1, index + 1, index - SIZE, index + SIZE];
  return candidates.filter((candidate) =>
    candidate >= 0 && candidate < state.grid.length && areAdjacent(index, candidate)
  );
}

function findMatchGroups() {
  const runs = [];

  for (let row = 0; row < SIZE; row++) {
    let start = 0;
    for (let column = 1; column <= SIZE; column++) {
      const current = column < SIZE ? state.grid[row * SIZE + column]?.up : null;
      const first = state.grid[row * SIZE + start]?.up;
      if (current !== first) {
        if (column - start >= 3) {
          runs.push(Array.from({ length: column - start }, (_, offset) => row * SIZE + start + offset));
        }
        start = column;
      }
    }
  }

  for (let column = 0; column < SIZE; column++) {
    let start = 0;
    for (let row = 1; row <= SIZE; row++) {
      const current = row < SIZE ? state.grid[row * SIZE + column]?.up : null;
      const first = state.grid[start * SIZE + column]?.up;
      if (current !== first) {
        if (row - start >= 3) {
          runs.push(Array.from({ length: row - start }, (_, offset) => (start + offset) * SIZE + column));
        }
        start = row;
      }
    }
  }

  return mergeOverlappingRuns(runs);
}

function mergeOverlappingRuns(runs) {
  const groups = [];
  runs.forEach((run) => {
    const overlaps = groups.filter((group) => run.some((index) => group.has(index)));
    if (!overlaps.length) {
      groups.push(new Set(run));
      return;
    }
    const merged = overlaps[0];
    run.forEach((index) => merged.add(index));
    overlaps.slice(1).forEach((group) => {
      group.forEach((index) => merged.add(index));
      groups.splice(groups.indexOf(group), 1);
    });
  });
  return groups.map((group) => [...group]);
}

async function resolveMatches() {
  let groups = findMatchGroups();
  if (!groups.length) return false;

  state.busy = true;
  state.chain = 1;
  while (groups.length) {
    const matchedIndexes = groups.flat();
    document.querySelectorAll(".field-tile").forEach((tile, index) => {
      if (matchedIndexes.includes(index)) tile.classList.add("matched");
    });
    await wait(360);

    let turnPoints = 0;
    groups.forEach((indexes) => {
      const terms = indexes.map((index) => state.grid[index]).filter(Boolean);
      const anchor = Math.max(...indexes);
      const up = terms[0].up;
      const merged = {
        id: state.nextId++,
        up,
        nodes: [...new Set(terms.flatMap((term) => term.nodes))],
        depth: Math.max(...terms.map((term) => term.depth)) + 1,
        children: terms
      };
      indexes.forEach((index) => { state.grid[index] = null; });
      state.grid[anchor] = merged;
      state.maxDepth = Math.max(state.maxDepth, merged.depth);
      turnPoints += indexes.length * 100 * state.chain;
      addLog(`Match ×${indexes.length}: ${up} panels → hierarchical depth ${merged.depth}.`);
    });

    state.score += turnPoints;
    floatScore(`+${turnPoints}`);
    collapseAndFill();
    updateStats();
    render();
    await wait(260);
    state.chain++;
    groups = findMatchGroups();
  }

  state.chain = Math.max(1, state.chain - 1);
  state.busy = false;
  statusElement.textContent = `Cascade complete · chain ×${state.chain}`;
  updateStats();
  render();
  return true;
}

function collapseAndFill() {
  for (let column = 0; column < SIZE; column++) {
    const terms = [];
    for (let row = SIZE - 1; row >= 0; row--) {
      const term = state.grid[row * SIZE + column];
      if (term) terms.push(term);
    }
    for (let row = SIZE - 1; row >= 0; row--) {
      state.grid[row * SIZE + column] = terms[SIZE - 1 - row] || leaf();
    }
  }
}

function inspect(term) {
  document.querySelector("#emptyInspector").hidden = true;
  document.querySelector("#termInspector").hidden = false;
  document.querySelector("#inspectorGlyph").innerHTML = renderTermGlyph(term);
  document.querySelector("#inspectorExpression").textContent = formatTerm(term);
  document.querySelector("#geometryReading").textContent = geometryReading(term);
  document.querySelector("#inspectorUp").textContent = term.up;
  document.querySelector("#inspectorPlate").textContent = term.nodes.join(" ∧ ");
  document.querySelector("#inspectorGrade").textContent = term.nodes.length;
  document.querySelector("#inspectorDepth").textContent = term.depth;
  document.querySelector("#termTree").innerHTML = renderTree(term);
}

function geometryReading(term) {
  const plate = term.nodes.join(" ∧ ");
  if (term.nodes.length === 2) {
    return `Pin ${term.up} is orthogonal to the result; the result lives in the plate of ${plate}.`;
  }
  return `Pin ${term.up} cuts the higher plate ${plate}; the result stays inside that subspace.`;
}

function renderTree(term) {
  const children = term.children.length
    ? `<div>${term.children.map(renderTree).join("")}</div>`
    : "";
  return `<div class="tree-node"><span>${formatTerm(term)}</span>${children}</div>`;
}

function formatTerm(term) {
  return `${term.up}⌋(${term.nodes.join("∧")})`;
}

/**
 * Glyph for o ⌋ (A ∧ B ∧ …) drawn on a fixed 100×100 canvas:
 * - stacked diamonds  = the subspace plate (extra layers show recursion depth)
 * - vertical pin      = the contracting blade o, orthogonal to the plate
 * - bright bar inside = the contracted result, lying in the plate
 */
function renderTermGlyph(term) {
  const depth = Math.min(term.depth, 3);
  const plates = [];

  for (let layer = depth; layer >= 1; layer--) {
    const lift = layer * 9;
    plates.push(`
      <polygon points="14,${58 - lift} 50,${34 - lift} 86,${58 - lift} 50,${82 - lift}"
        fill="none" stroke="var(--tile-color)" stroke-opacity="${0.5 - layer * 0.09}"
        stroke-width="2" stroke-dasharray="5 4"/>
    `);
  }

  const labels = term.nodes.slice(0, 3).map((node, index) => {
    const slots = [[12, 40], [88, 40], [50, 97]];
    const [x, y] = slots[index];
    return `<text x="${x}" y="${y}" class="glyph-label">${node}</text>`;
  }).join("");

  const cut = term.nodes.length >= 3
    ? `<polyline points="26,58 50,46 74,58" fill="none" stroke="var(--tile-color)"
         stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`
    : `<line x1="26" y1="58" x2="74" y2="58" stroke="var(--tile-color)"
         stroke-width="7" stroke-linecap="round"/>`;

  return `
    <svg class="term-glyph" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      ${plates.join("")}
      <polygon points="14,58 50,34 86,58 50,82"
        fill="var(--tile-color)" fill-opacity=".16"
        stroke="var(--tile-color)" stroke-opacity=".75" stroke-width="2.5"/>
      <line x1="50" y1="8" x2="50" y2="52" class="glyph-pin-line"/>
      <circle cx="50" cy="9" r="7" class="glyph-pin-head"/>
      <text x="50" y="13" class="glyph-pin">${term.up}</text>
      ${cut}
      ${labels}
    </svg>
  `;
}

function addLog(text) {
  const item = document.createElement("li");
  item.textContent = text;
  logElement.prepend(item);
  while (logElement.children.length > 8) logElement.lastElementChild.remove();
}

function updateStats() {
  document.querySelector("#fieldScore").textContent = String(state.score).padStart(6, "0");
  document.querySelector("#fieldChain").textContent = `×${state.chain}`;
  document.querySelector("#fieldDepth").textContent = state.maxDepth;
}

function floatScore(text) {
  const element = document.querySelector("#floatingScore");
  element.textContent = text;
  element.hidden = false;
  element.style.animation = "none";
  void element.offsetWidth;
  element.style.animation = "";
  window.setTimeout(() => { element.hidden = true; }, 900);
}

let toastTimer;
function toast(text) {
  const element = document.querySelector("#toast");
  element.textContent = text;
  element.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => element.classList.remove("show"), 1500);
}

function wait(milliseconds) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}

const toolCopy = {
  move: [
    "Drag a tile onto an adjacent cell to swap. Lines of three matching upper blades collapse into a nested term.",
    "MOVE mode · create a row or column of 3"
  ],
  merge: [
    "Drag one term onto an adjacent compatible term. Matching upper blades or a shared lower symbol permit Sandhi.",
    "SANDHI mode · drag a compatible term onto its neighbor"
  ],
  split: [
    "Click a hierarchical term. Its immediate children return to neighboring cells.",
    "VICCHEDA mode · click a term with depth ≥ 1"
  ]
};

document.querySelectorAll("[data-tool]").forEach((button) => {
  button.addEventListener("click", () => {
    state.tool = button.dataset.tool;
    state.selectedIndex = null;
    document.querySelectorAll("[data-tool]").forEach((item) =>
      item.classList.toggle("active", item === button)
    );
    document.querySelector("#modeHelp").textContent = toolCopy[state.tool][0];
    statusElement.textContent = toolCopy[state.tool][1];
    render();
  });
});

document.querySelector("#shuffleButton").addEventListener("click", () => {
  if (state.busy) return;
  for (let index = state.grid.length - 1; index > 0; index--) {
    const other = Math.floor(Math.random() * (index + 1));
    [state.grid[index], state.grid[other]] = [state.grid[other], state.grid[index]];
  }
  state.score = Math.max(0, state.score - 100);
  state.chain = 1;
  addLog("Field shuffled (−100). Hierarchies preserved.");
  updateStats();
  render();
});

initializeGrid();
