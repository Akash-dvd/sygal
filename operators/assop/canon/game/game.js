const levels = [
  {
    title: "The Circumcenter",
    text: "Complete the triangle cycle by joining all three ∞ panels.",
    goal: "∞⌋(P₁ ∧ P₂ ∧ P₃ ∧ P₁) → 0",
    clears: 1,
    complete: "The three bisectors concur.",
    explanation: "The chain closes on P₁. In the full GA proof, exterior alternation makes the repeated point vanish.",
    panels: [
      ["∞", ["P₁", "P₂"]], ["∞", ["P₂", "P₃"]], ["∞", ["P₃", "P₁"]],
      ["a", ["Q₁", "Q₂"]]
    ]
  },
  {
    title: "The Four-Sided Loop",
    text: "Build one closed cycle from four matching panels.",
    goal: "n⌋(A ∧ B ∧ C ∧ D ∧ A) → 0",
    clears: 1,
    complete: "The quadrilateral chain closes.",
    explanation: "Four local relations have become one global invariant through repeated Sandhi.",
    panels: [
      ["n", ["A", "B"]], ["n", ["C", "D"]], ["n", ["B", "C"]],
      ["n", ["D", "A"]], ["m", ["A", "C"]]
    ]
  },
  {
    title: "Two Invariants",
    text: "Upper blades define separate worlds. Close one α cycle and one β cycle.",
    goal: "α-cycle → 0   and   β-cycle → 0",
    clears: 2,
    complete: "Two independent invariants revealed.",
    explanation: "Panels only fuse inside their own upper-blade context—the game analogue of a scoped algebraic rule.",
    panels: [
      ["α", ["U", "V"]], ["β", ["1", "2"]], ["α", ["W", "U"]],
      ["β", ["3", "1"]], ["α", ["V", "W"]], ["β", ["2", "3"]]
    ]
  },
  {
    title: "Viccheda",
    text: "Use splitting to reorganize a long chain, then close the cycle.",
    goal: "split → expose seam → fuse → 0",
    clears: 1,
    requires: "split",
    complete: "The hidden seam was exposed.",
    explanation: "Viccheda changes the presentation without changing the underlying chain, making a useful local match visible.",
    panels: [
      ["Ω", ["K", "L", "M", "N"]], ["Ω", ["N", "R"]],
      ["Ω", ["R", "K"]], ["x", ["L", "R"]]
    ]
  },
  {
    title: "Viccheda · Order Reversal",
    text: "Split the long plate, then reverse a piece so its seam faces the right way.",
    goal: "Ω⌋(A∧B∧C) = −Ω⌋(C∧B∧A) → close the cycle",
    clears: 1,
    requires: "reverse",
    complete: "Reversal accounted for.",
    explanation: "Reversing a k-blade multiplies it by (−1)^(k(k−1)/2): 2-blades and 3-blades flip sign, 4-blades do not. Sandhi has to carry that sign, so the closed cycle can vanish as −0 just as well as +0.",
    panels: [
      ["Ω", ["A", "B", "C", "D"]], ["Ω", ["D", "E"]],
      ["Ω", ["E", "A"]], ["w", ["B", "D"]]
    ]
  },
  {
    title: "The Pattern Field",
    text: "Ignore false matches, respect upper blades, and reveal both cycles.",
    goal: "choose the right context × 2",
    clears: 2,
    complete: "You found order inside the field.",
    explanation: "The difficult step was choosing compatible descriptions. Once the chart was right, inference became mechanical.",
    panels: [
      ["∞", ["P", "Q"]], ["e", ["a", "b"]], ["∞", ["R", "P"]],
      ["e", ["c", "d"]], ["∞", ["Q", "R"]], ["e", ["b", "c"]],
      ["z", ["P", "R"]], ["e", ["d", "a"]], ["z", ["a", "c"]]
    ]
  }
];

const state = {
  level: 0,
  panels: [],
  selected: [],
  mode: "sandhi",
  score: 0,
  moves: 0,
  cleared: 0,
  splitUsed: false,
  reverseUsed: false,
  nextId: 1
};

const requirementCopy = {
  split: {
    hint: "Hint: switch to VICCHEDA and select the long Ω panel.",
    refusal: "This theorem asks for Viccheda first. Split the long Ω chain."
  },
  reverse: {
    hint: "Hint: split the long Ω plate, then use PARIVṚTTI on one piece.",
    refusal: "This theorem asks for a reversal first. Flip one plate with PARIVṚTTI."
  }
};

// Reversing a k-blade costs (−1)^(k(k−1)/2).
function reversalSign(length) {
  return (length * (length - 1) / 2) % 2 === 0 ? 1 : -1;
}

function requirementMet(level) {
  if (level.requires === "split") return state.splitUsed;
  if (level.requires === "reverse") return state.reverseUsed;
  return true;
}

function signPrefix(sign) {
  return sign < 0 ? "−" : "";
}

const $ = (selector) => document.querySelector(selector);
const board = $("#board");
const message = $("#message");

function makePanel([up, nodes, sign = 1]) {
  return { id: state.nextId++, up, nodes: [...nodes], sign };
}

function loadLevel(index) {
  state.level = index;
  state.panels = levels[index].panels.map(makePanel);
  state.selected = [];
  state.mode = "sandhi";
  state.cleared = 0;
  state.splitUsed = false;
  state.reverseUsed = false;

  const data = levels[index];
  $("#missionNumber").textContent = String(index + 1).padStart(2, "0");
  $("#missionTitle").textContent = data.title;
  $("#missionText").textContent = data.text;
  $("#goalExpression").textContent = data.goal;
  $("#completeTitle").textContent = data.complete;
  $("#completeExplanation").textContent = data.explanation;
  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.classList.toggle("active", button.dataset.mode === "sandhi");
  });
  setMessage(requirementCopy[data.requires]
    ? requirementCopy[data.requires].hint
    : "Same upper blade + shared lower symbol = a legal Sandhi.");
  updateStatus();
  render();
}

function render() {
  board.innerHTML = "";
  state.panels.forEach((panel, index) => {
    const button = document.createElement("button");
    button.className = `panel${state.selected.includes(panel.id) ? " selected" : ""}`;
    button.style.animationDelay = `${index * 35}ms`;
    button.dataset.id = panel.id;
    button.dataset.up = panel.up;
    button.innerHTML = `
      <span class="panel-index">${String(index + 1).padStart(2, "0")}</span>
      <span class="panel-up">PIN · ${panel.up}  ⊥  plate</span>
      <span class="panel-expression">
        <span class="panel-glyph">${panelGlyph(panel)}</span>
        <span>${signPrefix(panel.sign)}${panel.up}<span class="operator">⌋</span>(${panel.nodes.join("∧")})</span>
      </span>
      <span class="panel-meta">GRADE ${panel.nodes.length} · ⊥ TO ${panel.up}</span>
    `;
    button.addEventListener("click", () => selectPanel(panel.id));
    board.appendChild(button);
  });
}

function panelGlyph(panel) {
  const slotsByCount = {
    1: [[50, 40]],
    2: [[12, 40], [88, 40]],
    3: [[12, 40], [88, 40], [50, 94]],
    4: [[12, 36], [88, 36], [24, 94], [76, 94]]
  };
  const shown = panel.nodes.slice(0, 4);
  const slots = slotsByCount[shown.length] || slotsByCount[4];
  const labels = shown.map((node, index) => {
    const [x, y] = slots[index];
    const text = index === 3 && panel.nodes.length > 4
      ? `${node}…`
      : node;
    return `<text x="${x}" y="${y}" class="glyph-label">${text}</text>`;
  }).join("");

  const cut = panel.nodes.length >= 3
    ? `<polyline points="26,58 50,46 74,58" fill="none" stroke="var(--tile-color)"
         stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`
    : `<line x1="26" y1="58" x2="74" y2="58" stroke="var(--tile-color)"
         stroke-width="7" stroke-linecap="round"/>`;

  return `
    <svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      <polygon points="14,58 50,34 86,58 50,82"
        fill="var(--tile-color)" fill-opacity=".16"
        stroke="var(--tile-color)" stroke-opacity=".75" stroke-width="2.5"/>
      <line x1="50" y1="8" x2="50" y2="52" class="glyph-pin-line"/>
      <circle cx="50" cy="9" r="7" class="glyph-pin-head"/>
      <text x="50" y="13" class="glyph-pin">${panel.up}</text>
      ${cut}
      ${labels}
    </svg>
  `;
}

function selectPanel(id) {
  if (state.mode === "split") {
    splitPanel(id);
    return;
  }

  if (state.mode === "reverse") {
    reversePanel(id);
    return;
  }

  const index = state.selected.indexOf(id);
  if (index >= 0) {
    state.selected.splice(index, 1);
  } else {
    state.selected.push(id);
  }

  if (state.selected.length === 2) {
    const [first, second] = state.selected.map((panelId) =>
      state.panels.find((panel) => panel.id === panelId)
    );
    state.selected = [];
    combine(first, second);
  }
  render();
}

function combine(a, b) {
  state.moves++;

  const level = levels[state.level];
  if (!requirementMet(level)) {
    setMessage(requirementCopy[level.requires].refusal, "error");
    updateStatus();
    return;
  }

  if (a.up !== b.up) {
    setMessage(`No Sandhi: upper blades ${a.up} and ${b.up} belong to different contexts.`, "error");
    updateStatus();
    return;
  }

  const shared = a.nodes.filter((node) => b.nodes.includes(node));
  if (!shared.length) {
    setMessage("No seam found. The lower chains need a shared symbol.", "error");
    updateStatus();
    return;
  }

  const join = joinChains(a.nodes, b.nodes);
  const sign = a.sign * b.sign * join.sign;
  const closed = formsCycle(a.nodes, b.nodes, join.nodes);
  const signNote = join.sign < 0 ? " Re-ordering the seam flipped the sign." : "";
  removePanels(a.id, b.id);

  if (closed) {
    state.cleared++;
    state.score += 500 + Math.max(0, 100 - state.moves * 5);
    setMessage(`Cycle closed at ${shared.join(", ")}. Alternation → ${signPrefix(sign)}0.${signNote}`, "success");
  } else {
    state.panels.push({ id: state.nextId++, up: a.up, nodes: join.nodes, sign });
    state.score += 100 + shared.length * 25;
    setMessage(`Sandhi at ${shared.join(", ")}: two panels became ${signPrefix(sign)}one.${signNote}`, "success");
  }

  updateStatus();
  render();
  if (state.cleared >= levels[state.level].clears) {
    window.setTimeout(() => { $("#levelComplete").hidden = false; }, 450);
  }
}

function formsCycle(a, b, merged) {
  const aEndsInB = b.includes(a[0]) && b.includes(a[a.length - 1]);
  const bEndsInA = a.includes(b[0]) && a.includes(b[b.length - 1]);
  const unionSize = new Set([...a, ...b]).size;
  return unionSize >= 3 && (aEndsInB || bEndsInA || merged[0] === merged[merged.length - 1]);
}

function joinChains(aInput, bInput) {
  const flipA = reversalSign(aInput.length);
  const flipB = reversalSign(bInput.length);
  const orientations = [
    { a: [...aInput], b: [...bInput], sign: 1 },
    { a: [...aInput].reverse(), b: [...bInput], sign: flipA },
    { a: [...aInput], b: [...bInput].reverse(), sign: flipB },
    { a: [...aInput].reverse(), b: [...bInput].reverse(), sign: flipA * flipB }
  ];

  for (const { a, b, sign } of orientations) {
    if (a[a.length - 1] === b[0]) return { nodes: [...a, ...b.slice(1)], sign };
  }

  const nodes = [...aInput];
  bInput.forEach((node) => {
    if (!nodes.includes(node)) nodes.push(node);
  });
  return { nodes, sign: 1 };
}

function splitPanel(id) {
  const panel = state.panels.find((item) => item.id === id);
  if (panel.nodes.length < 3) {
    setMessage("Viccheda needs a chain with at least three lower symbols.", "error");
    return;
  }

  state.moves++;
  state.splitUsed = true;
  const cut = Math.floor(panel.nodes.length / 2);
  const left = panel.nodes.slice(0, cut + 1);
  const right = panel.nodes.slice(cut);
  state.panels = state.panels.filter((item) => item.id !== id);
  state.panels.push(
    { id: state.nextId++, up: panel.up, nodes: left, sign: panel.sign },
    { id: state.nextId++, up: panel.up, nodes: right, sign: 1 }
  );
  state.score = Math.max(0, state.score - 20);
  setMessage(`Viccheda at ${panel.nodes[cut]}: one chain became two overlapping panels.`, "success");
  updateStatus();
  render();
}

function reversePanel(id) {
  const panel = state.panels.find((item) => item.id === id);
  const grade = panel.nodes.length;
  const flip = reversalSign(grade);
  const before = `${signPrefix(panel.sign)}${panel.up}⌋(${panel.nodes.join("∧")})`;

  state.moves++;
  state.reverseUsed = true;
  panel.nodes.reverse();
  panel.sign *= flip;
  state.score = Math.max(0, state.score - 10);

  const after = `${signPrefix(panel.sign)}${panel.up}⌋(${panel.nodes.join("∧")})`;
  setMessage(
    flip < 0
      ? `Parivṛtti: ${before} = ${after}. Grade ${grade} reverses with a sign.`
      : `Parivṛtti: ${before} = ${after}. Grade ${grade} reverses with no sign.`,
    "success"
  );
  updateStatus();
  render();
}

function removePanels(...ids) {
  state.panels = state.panels.filter((panel) => !ids.includes(panel.id));
}

function setMessage(text, type = "") {
  message.textContent = text;
  message.className = `message${type ? ` ${type}` : ""}`;
}

function updateStatus() {
  $("#score").textContent = String(state.score).padStart(4, "0");
  $("#moves").textContent = String(state.moves).padStart(2, "0");
  $("#level").textContent = `${state.level + 1} / ${levels.length}`;
  $("#progressText").textContent = `${state.cleared} / ${levels[state.level].clears}`;
  $("#progressBar").style.width = `${Math.min(100, state.cleared / levels[state.level].clears * 100)}%`;
}

document.querySelectorAll("[data-mode]").forEach((button) => {
  button.addEventListener("click", () => {
    state.mode = button.dataset.mode;
    state.selected = [];
    document.querySelectorAll("[data-mode]").forEach((item) =>
      item.classList.toggle("active", item === button)
    );
    const instructions = {
      sandhi: "Select two panels to combine",
      split: "Select one long panel to split",
      reverse: "Select one panel to reverse"
    };
    const guidance = {
      sandhi: "Same upper blade + shared lower symbol = a legal Sandhi.",
      split: "Choose a chain of grade 3 or higher. The middle symbol becomes the shared seam.",
      reverse: "Reversal turns a∧b∧c into c∧b∧a and carries (−1)^(k(k−1)/2)."
    };
    $("#instruction").textContent = instructions[state.mode];
    setMessage(guidance[state.mode]);
    render();
  });
});

$("#restartButton").addEventListener("click", () => loadLevel(state.level));
$("#nextButton").addEventListener("click", () => {
  $("#levelComplete").hidden = true;
  if (state.level < levels.length - 1) {
    loadLevel(state.level + 1);
  } else {
    state.score += 1000;
    state.moves = 0;
    loadLevel(0);
    setMessage("All theorems complete. A new cycle begins.", "success");
  }
});

const helpDialog = $("#helpDialog");
$("#helpButton").addEventListener("click", () => helpDialog.showModal());
$("#closeHelp").addEventListener("click", () => helpDialog.close());
helpDialog.addEventListener("click", (event) => {
  if (event.target === helpDialog) helpDialog.close();
});

loadLevel(0);
