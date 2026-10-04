const operations = {
  swap: {
    number: "MUTATION 01",
    title: "Exchange order; carry parity",
    text: "Two selected factors trade places. Orientation must remain visible because an odd transposition changes the germ's sign."
  },
  shape: {
    number: "MUTATION 02",
    title: "Same germ, new topology",
    text: "The object moves between flat and nested presentations without changing its underlying algebraic value."
  },
  cut: {
    number: "MUTATION 03",
    title: "Dissect; retain the seam",
    text: "The selected section becomes two overlapping children. A visible token remembers the borrowed overlap scalar."
  },
  merge: {
    number: "MUTATION 04",
    title: "Recognize; fuse; cascade",
    text: "Compatible children lock at their seam, release the scalar token and leave one residual germ that can react again."
  }
};

const themes = {
  phage: {
    icon: "φ",
    name: "Seam phage",
    subtitle: "Living puzzle creature",
    domain: "BACTERIOPHAGE · GENOME PACKING",
    title: "A virus that cuts, inverts, packs and seals",
    truth: "BIOLOGY-INSPIRED",
    scores: { "Four-move fit": 96, "Visual clarity": 91, "Biological honesty": 76, "Arcade energy": 94 },
    map: { Germ: "packaged genome", Swap: "segment inversion", Shape: "linear ↔ capsid-packed", Viccheda: "cos-site cut", Sandhi: "sticky-end ligation", Scalar: "cohesive-end charge" },
    verdict: "Best complete game world. One recognizable creature supports all four motions and naturally produces offspring for cascades.",
    visual: phageVisual
  },
  dna: {
    icon: "⌬",
    name: "Sticky-end lab",
    subtitle: "Restriction + ligase",
    domain: "MOLECULAR TOOLKIT · DNA ASSEMBLY",
    title: "Cut at a site; orient the ends; zip the match",
    truth: "CLOSE METAPHOR",
    scores: { "Four-move fit": 93, "Visual clarity": 96, "Biological honesty": 86, "Arcade energy": 72 },
    map: { Germ: "DNA construct", Swap: "fragment inversion", Shape: "linear ↔ plasmid", Viccheda: "restriction cut", Sandhi: "ligase join", Scalar: "sticky-end compatibility" },
    verdict: "Clearest teaching skin. Excellent seams and cuts, though it feels more like a laboratory assembly puzzle than a creature game.",
    visual: dnaVisual
  },
  flu: {
    icon: "8",
    name: "Segmented virus",
    subtitle: "Reassortment swarm",
    domain: "INFLUENZA-LIKE · SEGMENT REASSORTMENT",
    title: "Trade genome cards between compatible shells",
    truth: "PARTIAL MATCH",
    scores: { "Four-move fit": 68, "Visual clarity": 83, "Biological honesty": 79, "Arcade energy": 90 },
    map: { Germ: "viral segment", Swap: "reassortment", Shape: "pack ↔ unpack", Viccheda: "segment release", Sandhi: "compatible packaging", Scalar: "packaging signal" },
    verdict: "Strong swarm and cascade fantasy. Swap is excellent; arbitrary sectional cutting and nested contraction are less natural.",
    visual: fluVisual
  },
  recombination: {
    icon: "X",
    name: "Recombination",
    subtitle: "Chromosome crossing",
    domain: "HOMOLOGOUS RECOMBINATION",
    title: "Align shared regions and exchange the residual arms",
    truth: "CLOSE METAPHOR",
    scores: { "Four-move fit": 84, "Visual clarity": 78, "Biological honesty": 90, "Arcade energy": 67 },
    map: { Germ: "chromosome arm", Swap: "crossing over", Shape: "loop ↔ extended chromatin", Viccheda: "strand break", Sandhi: "homology repair", Scalar: "homology score" },
    verdict: "Most faithful shared-seam story after DNA assembly. Visually elegant, but less immediate for fast arcade play.",
    visual: recombinationVisual
  },
  prion: {
    icon: "β",
    name: "Fold creature",
    subtitle: "Prion-like templating",
    domain: "PROTEIN FOLDING · CONFORMATION",
    title: "One sequence mutates between shallow and deep folds",
    truth: "LOOSE METAPHOR",
    scores: { "Four-move fit": 55, "Visual clarity": 81, "Biological honesty": 62, "Arcade energy": 77 },
    map: { Germ: "protein chain", Swap: "residue permutation", Shape: "helix ↔ sheet", Viccheda: "proteolytic cut", Sandhi: "templated aggregation", Scalar: "binding energy" },
    verdict: "The strongest shape-change image, but swap and exact Sandhi accounting feel imposed rather than native.",
    visual: prionVisual
  },
  transposon: {
    icon: "⇥",
    name: "Jumping gene",
    subtitle: "Cut · flip · insert",
    domain: "TRANSPOSON · MOBILE GENETIC ELEMENT",
    title: "Excise a cassette and dock it into a matching site",
    truth: "CLOSE METAPHOR",
    scores: { "Four-move fit": 87, "Visual clarity": 89, "Biological honesty": 82, "Arcade energy": 86 },
    map: { Germ: "mobile cassette", Swap: "orientation flip", Shape: "looped synapse", Viccheda: "excision", Sandhi: "target insertion", Scalar: "site duplication token" },
    verdict: "Excellent action vocabulary and strong orientation play. Slightly weaker than phage for nested towers and chain reactions.",
    visual: transposonVisual
  }
};

const colors = {
  cream: "#fbf7ea",
  orange: "#ed682d",
  blue: "#4d8995",
  violet: "#8a70a0",
  green: "#688064",
  gold: "#ba8433",
  deep: "#1b1c18"
};

function frame(label, content) {
  return `<svg viewBox="0 0 760 390" aria-label="${label}">
    <text x="28" y="32" class="v-title">${label}</text>
    <text x="28" y="52" class="v-small">SAME ALGEBRA · DIFFERENT BIOLOGICAL MOTION</text>
    ${content}
  </svg>`;
}

function arrow(x1, y1, x2, y2) {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${colors.orange}" stroke-width="3"/>
    <path d="M${x2 - 10} ${y2 - 7} L${x2} ${y2} L${x2 - 10} ${y2 + 7}" fill="none" stroke="${colors.orange}" stroke-width="3"/>`;
}

function token(x, y, label = "overlap") {
  return `<g class="pulse"><polygon points="${x},${y - 18} ${x + 18},${y} ${x},${y + 18} ${x - 18},${y}" fill="${colors.orange}"/>
    <text x="${x}" y="${y + 4}" text-anchor="middle" fill="${colors.cream}" font-size="10">κ</text>
    <text x="${x}" y="${y + 36}" text-anchor="middle" class="v-small">${label}</text></g>`;
}

function beads(nodes, x, y, gap = 58, reverse = false) {
  const list = reverse ? [...nodes].reverse() : nodes;
  return list.map((node, i) => {
    const cx = x + i * gap;
    const fill = i === Math.floor(list.length / 2) ? colors.orange : colors.blue;
    return `${i ? `<line x1="${cx - gap + 15}" y1="${y}" x2="${cx - 15}" y2="${y}" class="v-line"/>` : ""}
      <circle cx="${cx}" cy="${y}" r="15" fill="${fill}"/>
      <text x="${cx}" y="${y + 5}" text-anchor="middle" class="v-title">${node}</text>`;
  }).join("");
}

function phage(x, y, scale = 1, accent = colors.blue) {
  return `<g transform="translate(${x} ${y}) scale(${scale})">
    <polygon points="0,-40 35,-20 35,20 0,40 -35,20 -35,-20" fill="none" stroke="${accent}" stroke-width="6"/>
    <circle cx="0" cy="0" r="13" fill="${colors.orange}"/>
    <path d="M0 40 V92 M-16 92 H16 M-16 92 L-34 120 M16 92 L34 120 M0 92 V124" fill="none" stroke="${colors.cream}" stroke-width="5" stroke-linecap="round"/>
  </g>`;
}

function phageVisual(step) {
  if (step === "swap") return frame("SEAM PHAGE · SEGMENT INVERSION", `
    ${phage(135, 190, .85)}
    ${beads(["A","B","C"], 250, 190)}
    ${arrow(455,190,545,190)}
    ${beads(["C","B","A"], 580,190,52)}
    <text x="615" y="238" text-anchor="middle" class="v-label">orientation flips · sign −</text>`);
  if (step === "shape") return frame("SEAM PHAGE · PACKING TOPOLOGY", `
    ${beads(["A","B","C","D"], 80,195,55)}
    <text x="165" y="250" text-anchor="middle" class="v-label">linear genome</text>
    ${arrow(290,195,370,195)}
    ${phage(565,195,1.5)}
    <path d="M505 175 C535 115 610 125 620 190 C630 250 540 270 520 210 C505 165 580 150 600 190" class="v-orange"/>
    <text x="565" y="335" text-anchor="middle" class="v-label">same genome · nested in capsid</text>`);
  if (step === "cut") return frame("SEAM PHAGE · COHESIVE-END CUT", `
    ${beads(["A","B","C","D"], 100,155,70)}
    <path d="M303 108 l-22 30 m22 -30 l22 30" class="v-orange"/>
    <line x1="100" y1="255" x2="300" y2="255" class="v-blue"/>
    <line x1="365" y1="255" x2="565" y2="255" class="v-violet"/>
    <path d="M285 255 h55 v20" class="v-orange"/><path d="M365 255 h-25 v-20" class="v-orange"/>
    <text x="312" y="306" class="v-label">shared sticky end B</text>${token(655,255,"cohesive charge")}`);
  return frame("SEAM PHAGE · LIGATE AND REPLICATE", `
    ${phage(105,185,.8,colors.blue)}${phage(245,185,.8,colors.violet)}
    <path d="M145 185 C175 145 205 145 220 185" class="v-orange"/>
    ${token(340,185,"released κ")}${arrow(385,185,455,185)}
    ${phage(585,185,1.35,colors.orange)}
    <circle cx="675" cy="120" r="8" fill="${colors.orange}"/><circle cx="700" cy="155" r="6" fill="${colors.blue}"/>
    <text x="585" y="330" text-anchor="middle" class="v-label">residual phage can dock again</text>`);
}

function dnaStrands(x, y, width = 280, cutAt = -1) {
  const rungs = Array.from({ length: 7 }, (_, i) => {
    const px = x + i * width / 6;
    const hot = i === cutAt;
    return `<line x1="${px}" y1="${y - 18}" x2="${px}" y2="${y + 18}" stroke="${hot ? colors.orange : "rgba(251,247,234,.35)"}" stroke-width="${hot ? 7 : 3}"/>`;
  }).join("");
  return `<path d="M${x} ${y-18} C${x+width*.3} ${y-48},${x+width*.7} ${y+12},${x+width} ${y-18}" class="v-blue"/>
    <path d="M${x} ${y+18} C${x+width*.3} ${y+48},${x+width*.7} ${y-12},${x+width} ${y+18}" class="v-violet"/>${rungs}`;
}

function dnaVisual(step) {
  if (step === "swap") return frame("STICKY-END LAB · FLIP THE INSERT", `
    ${dnaStrands(55,150,250)}${arrow(335,150,410,150)}
    <g transform="rotate(180 565 150)">${dnaStrands(440,150,250)}</g>
    <text x="180" y="235" text-anchor="middle" class="v-label">A—B—C</text>
    <text x="565" y="235" text-anchor="middle" class="v-label">C—B—A · orientation −</text>`);
  if (step === "shape") return frame("STICKY-END LAB · LINEAR OR PLASMID", `
    ${dnaStrands(55,180,260)}${arrow(345,180,420,180)}
    <circle cx="565" cy="185" r="105" fill="none" stroke="${colors.blue}" stroke-width="9"/>
    <circle cx="565" cy="185" r="82" fill="none" stroke="${colors.violet}" stroke-width="7" stroke-dasharray="28 13"/>
    <text x="565" y="335" text-anchor="middle" class="v-label">same construct · closed shape</text>`);
  if (step === "cut") return frame("STICKY-END LAB · RESTRICTION CUT", `
    ${dnaStrands(65,140,610,3)}
    <path d="M370 78 l-25 35 m25 -35 l25 35" class="v-orange"/>
    <path d="M80 260 H335 v22 h38" class="v-blue"/>
    <path d="M680 260 H410 v-22 h-37" class="v-violet"/>
    ${token(373,320,"sticky-end debt")}`);
  return frame("STICKY-END LAB · LIGASE ZIP", `
    <path d="M65 175 H295 v22 h45" class="v-blue"/>
    <path d="M420 175 H650 v-22 h-80" class="v-violet"/>
    <g class="arrive"><path d="M340 197 C365 150 395 150 420 175" class="v-orange"/>
    <text x="380" y="130" text-anchor="middle" class="v-label">ligase</text></g>
    ${arrow(330,280,430,280)}${token(510,280,"match paid")}
    <text x="380" y="345" text-anchor="middle" class="v-label">one longer construct remains</text>`);
}

function virion(x, y, accent, segmentOrder = [0,1,2,3]) {
  return `<g transform="translate(${x} ${y})">
    <circle r="92" fill="none" stroke="${accent}" stroke-width="5"/>
    ${segmentOrder.map((n,i) => `<line x1="${-42+i*28}" y1="-45" x2="${-30+i*25}" y2="45" stroke="${[colors.blue,colors.orange,colors.violet,colors.green][n]}" stroke-width="9" stroke-linecap="round"/>`).join("")}
    ${Array.from({length:12},(_,i)=>{const a=i*Math.PI/6;return `<line x1="${Math.cos(a)*92}" y1="${Math.sin(a)*92}" x2="${Math.cos(a)*106}" y2="${Math.sin(a)*106}" stroke="${accent}" stroke-width="3"/>`;}).join("")}
  </g>`;
}

function fluVisual(step) {
  if (step === "swap") return frame("SEGMENTED VIRUS · REASSORT", `
    ${virion(170,195,colors.blue,[0,1,2,3])}${virion(570,195,colors.violet,[3,2,1,0])}
    <path d="M255 155 C350 85 405 85 485 155 M485 235 C400 305 345 305 255 235" class="v-orange"/>
    <text x="370" y="195" text-anchor="middle" class="v-label">trade selected segments</text>`);
  if (step === "shape") return frame("SEGMENTED VIRUS · PACK / UNPACK", `
    ${[0,1,2,3].map((n,i)=>`<line x1="70" y1="${115+i*50}" x2="270" y2="${115+i*50}" stroke="${[colors.blue,colors.orange,colors.violet,colors.green][n]}" stroke-width="10"/>`).join("")}
    ${arrow(320,195,405,195)}${virion(580,195,colors.orange)}
    <text x="170" y="340" text-anchor="middle" class="v-label">flat inventory</text><text x="580" y="340" text-anchor="middle" class="v-label">packed shell</text>`);
  if (step === "cut") return frame("SEGMENTED VIRUS · RELEASE A SEGMENT", `
    ${virion(190,190,colors.blue)}${arrow(305,190,410,190)}
    <line x1="450" y1="190" x2="610" y2="190" class="v-orange"/>
    <circle cx="450" cy="190" r="14" fill="${colors.orange}"/>
    ${token(660,190,"packaging signal")}
    <text x="525" y="235" text-anchor="middle" class="v-label">whole segment, not arbitrary cut</text>`);
  return frame("SEGMENTED VIRUS · PACKAGE A NEW SHELL", `
    <line x1="80" y1="130" x2="260" y2="130" class="v-blue"/><line x1="80" y1="190" x2="260" y2="190" class="v-orange"/>
    <line x1="80" y1="250" x2="260" y2="250" class="v-violet"/>
    ${token(350,190,"signals")}${arrow(390,190,460,190)}${virion(600,190,colors.orange,[0,1,2,3])}`);
}

function chromosome(x, y, color, flip = false) {
  const s = flip ? -1 : 1;
  return `<g transform="translate(${x} ${y}) scale(${s} 1)">
    <path d="M-55 -100 C20 -60,-20 -20,55 0 C-20 20,20 60,-55 100" fill="none" stroke="${color}" stroke-width="12" stroke-linecap="round"/>
    <path d="M55 -100 C-20 -60,20 -20,-55 0 C20 20,-20 60,55 100" fill="none" stroke="${color}" stroke-width="12" stroke-linecap="round"/>
  </g>`;
}

function recombinationVisual(step) {
  if (step === "swap") return frame("RECOMBINATION · CROSS OVER", `
    ${chromosome(180,195,colors.blue)}${chromosome(570,195,colors.violet,true)}
    <path d="M250 195 C330 120 410 270 495 195" class="v-orange"/>
    <text x="375" y="105" text-anchor="middle" class="v-label">exchange homologous arms</text>`);
  if (step === "shape") return frame("RECOMBINATION · CHROMATIN LOOP", `
    <path d="M55 190 C130 95 210 285 285 190" class="v-blue"/>
    ${arrow(325,190,405,190)}
    <path d="M445 190 C445 75 680 75 680 190 C680 305 445 305 445 190 C445 125 615 125 615 190" class="v-blue"/>
    <text x="565" y="340" text-anchor="middle" class="v-label">same locus · nested loop</text>`);
  if (step === "cut") return frame("RECOMBINATION · DOUBLE-STRAND BREAK", `
    <line x1="60" y1="150" x2="330" y2="150" class="v-blue"/><line x1="60" y1="225" x2="330" y2="225" class="v-blue"/>
    <line x1="425" y1="150" x2="700" y2="150" class="v-violet"/><line x1="425" y1="225" x2="700" y2="225" class="v-violet"/>
    <path d="M355 105 l-22 30 m22 -30 l22 30" class="v-orange"/>
    ${token(378,282,"homology debt")}`);
  return frame("RECOMBINATION · HOMOLOGY REPAIR", `
    <path d="M65 140 H290 C345 140 345 240 400 240 H690" class="v-blue"/>
    <path d="M65 240 H290 C345 240 345 140 400 140 H690" class="v-violet"/>
    <circle cx="345" cy="190" r="24" fill="${colors.orange}" class="pulse"/>
    <text x="345" y="195" text-anchor="middle" class="v-title">κ</text>
    <text x="380" y="320" text-anchor="middle" class="v-label">shared sequence resolves the junction</text>`);
}

function protein(x, y, folded = false, color = colors.blue) {
  if (!folded) return `<path d="M${x} ${y} C${x+45} ${y-70},${x+90} ${y+70},${x+135} ${y} S${x+225} ${y-70},${x+270} ${y}" fill="none" stroke="${color}" stroke-width="11" stroke-linecap="round"/>`;
  return `<g transform="translate(${x} ${y})">
    <path d="M0 0 C20 -75,80 -75,95 0 C110 75,165 75,180 0 C195 -75,250 -75,270 0" fill="none" stroke="${color}" stroke-width="11"/>
    <path d="M40 45 H230 M55 65 H215" class="v-orange"/>
  </g>`;
}

function prionVisual(step) {
  if (step === "swap") return frame("FOLD CREATURE · RESIDUE ORDER", `
    ${beads(["A","B","C"],75,180,65)}${arrow(300,180,390,180)}${beads(["C","B","A"],455,180,65)}
    <text x="555" y="245" text-anchor="middle" class="v-label">sequence changed · not ordinary folding</text>`);
  if (step === "shape") return frame("FOLD CREATURE · CONFORMATION", `
    ${protein(45,190,false,colors.blue)}${arrow(345,190,425,190)}${protein(445,190,true,colors.violet)}
    <text x="180" y="300" text-anchor="middle" class="v-label">extended</text><text x="580" y="300" text-anchor="middle" class="v-label">deep fold</text>`);
  if (step === "cut") return frame("FOLD CREATURE · PROTEOLYSIS", `
    ${protein(55,155,false,colors.blue)}
    <path d="M330 90 l-23 32 m23 -32 l23 32" class="v-orange"/>
    <path d="M80 275 C145 220 205 330 275 275" class="v-blue"/>
    <path d="M430 275 C495 220 555 330 625 275" class="v-violet"/>
    ${token(355,275,"binding energy")}`);
  return frame("FOLD CREATURE · TEMPLATED AGGREGATION", `
    ${protein(35,135,true,colors.violet)}${protein(35,245,true,colors.violet)}
    ${arrow(350,190,430,190)}${protein(455,190,true,colors.orange)}
    <text x="585" y="320" text-anchor="middle" class="v-label">one larger aggregate · weak Sandhi analogy</text>`);
}

function cassette(x, y, reversed = false) {
  const labels = reversed ? ["R","B","A","L"] : ["L","A","B","R"];
  return `<g transform="translate(${x} ${y})">
    <rect x="0" y="-34" width="250" height="68" rx="6" fill="none" stroke="${colors.orange}" stroke-width="4"/>
    ${labels.map((v,i)=>`<rect x="${15+i*58}" y="-20" width="45" height="40" fill="${i===0||i===3?colors.gold:colors.blue}" opacity=".85"/><text x="${37+i*58}" y="5" text-anchor="middle" class="v-title">${v}</text>`).join("")}
  </g>`;
}

function transposonVisual(step) {
  if (step === "swap") return frame("JUMPING GENE · ORIENTATION FLIP", `
    ${cassette(45,170)}${arrow(325,170,405,170)}${cassette(450,170,true)}
    <text x="575" y="255" text-anchor="middle" class="v-label">terminal repeats now face inward</text>`);
  if (step === "shape") return frame("JUMPING GENE · SYNAPTIC LOOP", `
    ${cassette(45,175)}${arrow(330,175,410,175)}
    <path d="M460 220 C430 65 700 65 665 220 C640 305 485 305 460 220" class="v-orange"/>
    <circle cx="460" cy="220" r="13" fill="${colors.gold}"/><circle cx="665" cy="220" r="13" fill="${colors.gold}"/>
    <text x="563" y="335" text-anchor="middle" class="v-label">ends meet inside one loop</text>`);
  if (step === "cut") return frame("JUMPING GENE · EXCISION", `
    <line x1="45" y1="150" x2="705" y2="150" class="v-blue"/>
    ${cassette(250,150)}
    <path d="M250 80 l-20 30 m20 -30 l20 30 M500 80 l-20 30 m20 -30 l20 30" class="v-orange"/>
    <path d="M250 270 C300 210 450 210 500 270" class="v-orange"/>
    ${token(600,270,"site duplication")}`);
  return frame("JUMPING GENE · TARGET INSERTION", `
    <line x1="50" y1="260" x2="700" y2="260" class="v-blue"/>
    <path d="M330 260 l35 -25 l35 25" class="v-orange"/>
    <g class="arrive">${cassette(250,125)}</g>
    ${arrow(375,180,375,225)}${token(645,155,"target paid")}
    <text x="375" y="325" text-anchor="middle" class="v-label">residual genome can receive another cassette</text>`);
}

const worldList = document.querySelector("#worldList");
const stage = document.querySelector("#visualStage");
let currentTheme = "phage";
let currentStep = "swap";

function renderWorldList() {
  worldList.innerHTML = Object.entries(themes).map(([key, theme]) => `
    <button class="world-button${key === currentTheme ? " active" : ""}" data-theme="${key}">
      <i>${theme.icon}</i>
      <span><b>${theme.name}</b><small>${theme.subtitle}</small></span>
    </button>
  `).join("");

  worldList.querySelectorAll("[data-theme]").forEach(button => {
    button.addEventListener("click", () => {
      currentTheme = button.dataset.theme;
      render();
    });
  });
}

function renderScores(theme) {
  document.querySelector("#scores").innerHTML = Object.entries(theme.scores).map(([label, value]) => `
    <div class="score">
      <div class="score-label"><b>${label}</b><span>${value} / 100</span></div>
      <div class="score-track"><i style="width:${value}%"></i></div>
    </div>
  `).join("");
}

function renderMapping(theme) {
  document.querySelector("#mapping").innerHTML = Object.entries(theme.map).map(([key, value]) => `
    <div><dt>${key.toUpperCase()}</dt><dd>${value}</dd></div>
  `).join("");
}

function render() {
  const theme = themes[currentTheme];
  const operation = operations[currentStep];
  renderWorldList();

  document.querySelector("#domain").textContent = theme.domain;
  document.querySelector("#title").textContent = theme.title;
  document.querySelector("#truthBadge").textContent = theme.truth;
  document.querySelector("#truthBadge").className =
    `truth-badge${theme.truth.includes("METAPHOR") || theme.truth.includes("PARTIAL") ? " metaphor" : ""}`;
  stage.innerHTML = theme.visual(currentStep);
  document.querySelector("#operationName").textContent = operation.number;
  document.querySelector("#operationTitle").textContent = operation.title;
  document.querySelector("#operationText").textContent = operation.text;
  document.querySelector("#verdict").textContent = theme.verdict;
  renderScores(theme);
  renderMapping(theme);

  document.querySelectorAll("[data-step]").forEach(button => {
    button.classList.toggle("active", button.dataset.step === currentStep);
  });
}

document.querySelectorAll("[data-step]").forEach(button => {
  button.addEventListener("click", () => {
    currentStep = button.dataset.step;
    render();
  });
});

render();
