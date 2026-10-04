const colors = {
  cream: "#fbf7ea",
  orange: "#ed682d",
  blue: "#4d8995",
  violet: "#8a70a0",
  green: "#688064",
  gold: "#ba8433",
  deep: "#1b1c18"
};

const specimens = {
  shape: {
    number: "01",
    label: "SPECIMEN 01 · SHAPE PAIR",
    title: "Two pins, one genome packet",
    short: "flat ↔ nested",
    expression: "(a₁∧a₂)⌋(B₁∧B₂∧B₃)",
    genes: ["B₁", "B₂", "B₃"],
    pins: ["a₁", "a₂"],
    boundary: "The capsid shells are a deterministic tree diagram, not a claim that real phages place capsids inside capsids."
  },
  seam: {
    number: "02",
    label: "SPECIMEN 02 · CUTTABLE SEAM",
    title: "One shell, four ordered genes",
    short: "split + scalar debt",
    expression: "d⌋(A∧B∧C∧D)",
    genes: ["A", "B", "C", "D"],
    pins: ["d"],
    boundary: "A real restriction cut motivates the motion. The overlap scalar is algebraic bookkeeping, not literal chemical energy."
  },
  nested: {
    number: "03",
    label: "SPECIMEN 03 · NESTED TOWER",
    title: "A shell carrying another shell",
    short: "recursive grammar",
    expression: "d₁⌋(A∧d₂⌋(B∧C∧D))",
    genes: ["B", "C", "D"],
    outerGenes: ["A"],
    pins: ["d₁", "d₂"],
    boundary: "The nested body is an exact encoding of expression-tree depth, but it is a designed creature anatomy rather than normal bacteriophage biology."
  }
};

const operationCopy = {
  encode: {
    number: "READ 00",
    title: "Decode the body without guessing",
    text: "Direction gives wedge order, each bead gives a factor and every shell gate gives one contraction node."
  },
  swap: {
    number: "MOVE 01",
    title: "Swap two genes; attach the minus sign",
    text: "The selected factors exchange slots as one transposition. The body changes orientation locally and the coefficient ledger records −1."
  },
  shape: {
    number: "MOVE 02",
    title: "Move one pin into its own shell",
    text: "Two pins on one flat gate become two nested shell gates. The genome and coefficient remain unchanged."
  },
  cut: {
    number: "MOVE 03",
    title: "Cut through a selected seam",
    text: "The seam appears in both child packets. A κ-debt token records the overlap that must be restored when they recombine."
  },
  merge: {
    number: "MOVE 04",
    title: "Dock matching children",
    text: "Compatible shell lineage and sticky seam authorize a candidate. SandhiCanon supplies the scalar and residual germ."
  }
};

let currentSpecimen = "shape";
let currentOperation = "encode";

const stage = document.querySelector("#phageStage");
const exampleList = document.querySelector("#exampleList");

function frame(label, content) {
  return `<svg viewBox="0 0 780 405" aria-label="${label}">
    <text x="27" y="31" class="v-title">${label}</text>
    <text x="27" y="51" class="v-small">DIRECTED GENOME · EXPLICIT SHELLS · VISIBLE SCALARS</text>
    ${content}
  </svg>`;
}

function arrow(x1, y1, x2, y2, label = "") {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${colors.orange}" stroke-width="3"/>
    <path d="M${x2 - 10} ${y2 - 7} L${x2} ${y2} L${x2 - 10} ${y2 + 7}" fill="none" stroke="${colors.orange}" stroke-width="3"/>
    ${label ? `<text x="${(x1+x2)/2}" y="${y1-12}" text-anchor="middle" class="v-small">${label}</text>` : ""}`;
}

function genes(nodes, x, y, gap = 58, selected = []) {
  return nodes.map((node, index) => {
    const cx = x + index * gap;
    const hot = selected.includes(index);
    return `${index ? `<line x1="${cx-gap+14}" y1="${y}" x2="${cx-14}" y2="${y}" class="v-muted"/>` : ""}
      <circle cx="${cx}" cy="${y}" r="15" fill="${hot ? colors.orange : colors.blue}"/>
      <text x="${cx}" y="${y+5}" text-anchor="middle" class="v-title">${node}</text>`;
  }).join("");
}

function direction(x1, x2, y) {
  return `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${colors.orange}" stroke-width="2"/>
    <path d="M${x2-8} ${y-5} L${x2} ${y} L${x2-8} ${y+5}" fill="none" stroke="${colors.orange}" stroke-width="2"/>`;
}

function shell(x, y, width, height, pin, inner, color = colors.violet) {
  return `<g>
    <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="34" fill="none" stroke="${color}" stroke-width="5"/>
    <rect x="${x+18}" y="${y-11}" width="42" height="22" rx="11" fill="${color}"/>
    <text x="${x+39}" y="${y+4}" text-anchor="middle" class="v-title">${pin}</text>
    ${inner}
  </g>`;
}

function token(x, y, text) {
  return `<g class="pulse">
    <polygon points="${x},${y-20} ${x+20},${y} ${x},${y+20} ${x-20},${y}" fill="${colors.orange}"/>
    <text x="${x}" y="${y+5}" text-anchor="middle" class="v-title">κ</text>
    <text x="${x}" y="${y+40}" text-anchor="middle" class="v-small">${text}</text>
  </g>`;
}

function splitParts(nodes) {
  if (nodes.length === 3) {
    return {
      left: nodes.slice(0,2),
      right: nodes.slice(1),
      seam: nodes.slice(1,2)
    };
  }
  return {
    left: nodes.slice(0,Math.ceil(nodes.length / 2) + 1),
    right: nodes.slice(Math.floor(nodes.length / 2) - 1),
    seam: nodes.slice(Math.floor(nodes.length / 2) - 1,Math.ceil(nodes.length / 2) + 1)
  };
}

function packedBody(specimen, x = 205, y = 115, width = 370) {
  if (specimen.outerGenes) {
    const inner = shell(
      x + 105, y + 72, width - 145, 135, specimen.pins[1],
      `${genes(specimen.genes, x+150, y+140, 55)}${direction(x+135,x+315,y+178)}`,
      colors.blue
    );
    return shell(
      x, y, width, 260, specimen.pins[0],
      `${genes(specimen.outerGenes,x+62,y+82)}${inner}`,
      colors.violet
    );
  }

  const pin = specimen.pins.join("∧");
  return shell(
    x, y, width, 190, pin,
    `${genes(specimen.genes,x+62,y+92,Math.min(70,(width-120)/Math.max(1,specimen.genes.length-1)))}
     ${direction(x+47,x+width-45,y+132)}`,
    colors.violet
  );
}

function encodeVisual(specimen) {
  return frame("ANATOMY · EXPRESSION TO BODY", `
    <g transform="translate(45 90)">
      <rect width="250" height="220" rx="5" fill="rgba(251,247,234,.05)" stroke="rgba(251,247,234,.16)"/>
      <text x="20" y="30" class="v-small">EXPRESSION TREE</text>
      <text x="20" y="72" class="v-label">${specimen.expression}</text>
      <line x1="20" y1="105" x2="225" y2="105" class="v-muted"/>
      <text x="20" y="135" class="v-small">pins: ${specimen.pins.join(", ")}</text>
      <text x="20" y="158" class="v-small">genes: ${specimen.genes.join(" → ")}</text>
      <text x="20" y="181" class="v-small">sign: +1</text>
    </g>
    ${arrow(320,200,390,200,"encode")}
    ${packedBody(specimen,420,100,315)}
  `);
}

function swapVisual(specimen) {
  const before = [...specimen.genes];
  const after = [...specimen.genes];
  if (after.length > 1) [after[0], after[after.length-1]] = [after[after.length-1], after[0]];
  const gap = Math.min(64,210/Math.max(1,before.length-1));
  return frame("SWAP · ONE TRANSPOSITION", `
    <text x="145" y="92" text-anchor="middle" class="v-small">BEFORE · SIGN +</text>
    ${genes(before,55,165,gap,[0,before.length-1])}${direction(42,270,205)}
    ${arrow(310,170,445,170,"swap selected genes")}
    <text x="610" y="92" text-anchor="middle" class="v-small">AFTER · SIGN −</text>
    ${genes(after,505,165,gap,[0,after.length-1])}${direction(492,720,205)}
    <rect x="524" y="258" width="170" height="52" rx="4" fill="rgba(237,104,45,.12)" stroke="${colors.orange}"/>
    <text x="609" y="280" text-anchor="middle" class="v-label">coefficient × −1</text>
    <text x="609" y="299" text-anchor="middle" class="v-small">sign is not genome material</text>
  `);
}

function shapeVisual(specimen) {
  const pins = specimen.pins.length > 1 ? specimen.pins : ["a₁","a₂"];
  const geneNodes = specimen.genes.slice(0,3);
  return frame("SHAPE · FLAT GATE TO NESTED GATES", `
    <text x="155" y="82" text-anchor="middle" class="v-small">FLAT · (${pins.join("∧")})⌋B</text>
    ${shell(35,115,275,185,pins.join("∧"),`${genes(geneNodes,85,205,72)}${direction(70,275,242)}`)}
    ${arrow(335,205,430,205,"same value")}
    <text x="595" y="82" text-anchor="middle" class="v-small">DEEP · ${pins[0]}⌋(${pins[1]}⌋B)</text>
    ${shell(455,105,285,235,pins[0],shell(505,155,185,135,pins[1],`${genes(geneNodes,535,220,55)}${direction(520,665,255)}`,colors.blue))}
    <text x="390" y="375" text-anchor="middle" class="v-label">no scalar created · sign unchanged</text>
  `);
}

function cutVisual(specimen) {
  const nodes = specimen.genes;
  const { left, right, seam } = splitParts(nodes);
  return frame("VICCHEDA · OVERLAPPING CHILD PACKETS", `
    ${shell(165,80,450,105,specimen.pins.at(-1),`${genes(nodes,225,135,80,[1,2])}${direction(210,570,168)}`)}
    <path d="M390 202 l-23 32 m23 -32 l23 32" class="v-orange"/>
    <text x="390" y="260" text-anchor="middle" class="v-small">cut selected seam ${seam.join("∧")}</text>
    ${shell(35,280,300,90,specimen.pins.at(-1),genes(left,92,325,82,[1,2]),colors.blue)}
    ${shell(445,280,300,90,specimen.pins.at(-1),genes(right,502,325,82,[0,1]),colors.violet)}
    ${token(390,323,"overlap debt")}
  `);
}

function mergeVisual(specimen) {
  const nodes = specimen.genes;
  const { left, right } = splitParts(nodes);
  return frame("SANDHI · MATCH, PAY, KEEP RESIDUAL", `
    ${shell(25,92,280,100,specimen.pins.at(-1),genes(left,78,143,72,[1,2]),colors.blue)}
    ${shell(25,235,280,100,specimen.pins.at(-1),genes(right,78,286,72,[0,1]),colors.violet)}
    <path d="M305 142 C365 142 365 286 305 286" class="v-orange"/>
    ${token(382,214,"scalar released")}
    ${arrow(420,214,485,214)}
    <g class="arrive">${shell(500,105,250,220,specimen.pins.at(-1),`${genes(nodes,535,210,55)}${direction(522,715,248)}`,colors.orange)}</g>
    <text x="625" y="365" text-anchor="middle" class="v-label">one residual germ · cascade-ready</text>
  `);
}

function operationState(specimen, operation) {
  const lastPin = specimen.pins.at(-1);
  const nodes = specimen.genes;
  if (operation === "swap") {
    const swapped = [...nodes];
    if (swapped.length > 1) [swapped[0],swapped[swapped.length-1]] = [swapped[swapped.length-1],swapped[0]];
    return {
      expression: `−${lastPin}⌋(${swapped.join("∧")})`,
      body: "same shell; first and last gene beads exchanged",
      orientation: "directed packet retained; coefficient is now −1",
      scalar: "−1 parity token attached",
      legal: "both selected objects are factors in the same wedge",
      sign: -1
    };
  }
  if (operation === "shape") {
    const pins = specimen.pins.length > 1 ? specimen.pins : ["a₁","a₂"];
    return {
      expression: `${pins[0]}⌋(${pins[1]}⌋(${nodes.join("∧")}))`,
      body: "one flat two-pin gate becomes two nested shell gates",
      orientation: "gene order unchanged",
      scalar: "none created or consumed",
      legal: "selected subtree matches the left-contraction reshape rule",
      sign: 1
    };
  }
  if (operation === "cut") {
    const { left: leftNodes, right: rightNodes, seam } = splitParts(nodes);
    const left = `${lastPin}⌋(${leftNodes.join("∧")})`;
    const right = `${lastPin}⌋(${rightNodes.join("∧")})`;
    return {
      expression: `[${left}] ∧ [${right}]`,
      body: `two child packets share ${seam.join("∧")}`,
      orientation: "both children inherit directed order",
      scalar: `debt: overlap(${lastPin}, ${seam.join("∧")})`,
      legal: "engine validates both children and computes the debt",
      sign: 1
    };
  }
  if (operation === "merge") {
    const { seam } = splitParts(nodes);
    return {
      expression: `overlap(${lastPin},${seam.join("∧")}) · ${lastPin}⌋(${nodes.join("∧")})`,
      body: "matching children consumed; one wider shell packet remains",
      orientation: "residual order supplied by SandhiCanon",
      scalar: "overlap token released; matching debt consumed",
      legal: "pin lineage, tree shape, grade gate and seam all match",
      sign: 1
    };
  }
  return {
    expression: specimen.expression,
    body: specimen.outerGenes ? "outer shell containing genes and one inner shell" : "one directed packet inside its pin shell",
    orientation: `left-to-right: ${nodes.join(" → ")}`,
    scalar: "coefficient +1; no debt",
    legal: "every visible symbol decodes uniquely",
    sign: 1
  };
}

function renderExampleList() {
  exampleList.innerHTML = Object.entries(specimens).map(([key,specimen]) => `
    <button class="specimen${key === currentSpecimen ? " active" : ""}" data-specimen="${key}">
      <span>${specimen.number}</span>
      <div><b>${specimen.title}</b><small>${specimen.short}</small></div>
    </button>
  `).join("");
  exampleList.querySelectorAll("[data-specimen]").forEach(button => {
    button.addEventListener("click", () => {
      currentSpecimen = button.dataset.specimen;
      render();
    });
  });
}

function render() {
  const specimen = specimens[currentSpecimen];
  const copy = operationCopy[currentOperation];
  const state = operationState(specimen,currentOperation);
  renderExampleList();

  document.querySelector("#specimenLabel").textContent = specimen.label;
  document.querySelector("#specimenTitle").textContent = specimen.title;
  document.querySelector("#stepNumber").textContent = copy.number;
  document.querySelector("#stepTitle").textContent = copy.title;
  document.querySelector("#stepText").textContent = copy.text;
  document.querySelector("#algebraExpression").textContent = state.expression;
  document.querySelector("#bodyReading").textContent = state.body;
  document.querySelector("#orientationReading").textContent = state.orientation;
  document.querySelector("#scalarReading").textContent = state.scalar;
  document.querySelector("#legalReading").textContent = state.legal;
  document.querySelector("#boundaryText").textContent = specimen.boundary;
  const signBadge = document.querySelector("#signBadge");
  signBadge.textContent = `SIGN ${state.sign < 0 ? "−" : "+"}`;
  signBadge.className = `sign-badge${state.sign < 0 ? " negative" : ""}`;

  const visuals = { encode: encodeVisual, swap: swapVisual, shape: shapeVisual, cut: cutVisual, merge: mergeVisual };
  stage.innerHTML = visuals[currentOperation](specimen);
  document.querySelectorAll("[data-operation]").forEach(button => {
    button.classList.toggle("active",button.dataset.operation === currentOperation);
  });
}

document.querySelectorAll("[data-operation]").forEach(button => {
  button.addEventListener("click", () => {
    currentOperation = button.dataset.operation;
    render();
  });
});

render();
