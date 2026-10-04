const themes = {
  geometry: {
    domain: "GEOMETRIC ALGEBRA",
    title: "The pin cuts a subspace plate",
    exact: true,
    build: "A and B span an oriented plane",
    read: "o selects a vector inside that plane",
    wedge: "oriented subspace",
    contractor: "orthogonal probe",
    result: "in-plane vector",
    explanation: "For a vector o and a simple bivector A∧B, contraction produces (o·A)B − (o·B)A. The answer is therefore a linear combination of A and B, and its inner product with o vanishes.",
    caveat: "<b>Literal statement:</b> this picture directly represents the algebraic subspace and orthogonality relations.",
    visual: () => `
      <svg viewBox="0 0 700 350">
        <defs><linearGradient id="plate" x1="0" x2="1"><stop stop-color="#376f7c" stop-opacity=".35"/><stop offset="1" stop-color="#ed682d" stop-opacity=".2"/></linearGradient></defs>
        <text x="35" y="38" class="svg-title">SUBSPACE PLATE  A ∧ B</text>
        <polygon points="105,240 340,95 605,215 350,310" fill="url(#plate)" stroke="#6da0a8" stroke-width="2"/>
        <line x1="125" y1="247" x2="330" y2="118" class="svg-blue" stroke-width="5"/><text x="102" y="270" class="svg-label">A</text>
        <line x1="340" y1="287" x2="575" y2="222" class="svg-orange" stroke-width="5"/><text x="594" y="230" class="svg-label">B</text>
        <g class="probe"><line x1="350" y1="25" x2="350" y2="202" stroke="#fbf7ea" stroke-width="5"/><circle cx="350" cy="25" r="18" fill="#ed682d"/><text x="350" y="31" text-anchor="middle" class="svg-title">o</text><path d="M350 202 l18 -4 l-4 18" fill="none" stroke="#fbf7ea" stroke-width="3"/></g>
        <line class="result pulse" x1="215" y1="240" x2="500" y2="169" stroke="#ed682d" stroke-width="12" stroke-linecap="round"/>
        <text x="430" y="270" class="svg-label">result stays in A∧B</text>
      </svg>`
  },
  fock: {
    domain: "FERMIONIC FOCK SPACE · QUANTUM CHEMISTRY",
    title: "Creation builds; annihilation contracts",
    exact: true,
    build: "a†A a†B |0⟩ creates a two-fermion state",
    read: "ao removes the o-component",
    wedge: "antisymmetric Slater state",
    contractor: "annihilation operator",
    result: "one-fermion state",
    explanation: "The exterior algebra is a model of fermionic Fock space. Creation acts by wedge: a†(φ)Ψ = φ∧Ψ. With an inner product, annihilation is interior contraction: a(φ)Ψ = φ⌋Ψ.",
    caveat: "<b>Physically exact correspondence:</b> this is the canonical creation/annihilation algebra behind Slater determinants and electronic-structure theory.",
    visual: () => `
      <svg viewBox="0 0 700 350">
        <text x="35" y="38" class="svg-title">FERMIONIC OCCUPATION</text>
        <g transform="translate(70 78)">
          <line x1="0" y1="55" x2="500" y2="55" class="svg-muted" stroke-width="2"/>
          <line x1="0" y1="145" x2="500" y2="145" class="svg-muted" stroke-width="2"/>
          <text x="520" y="61" class="svg-label">orbital A</text><text x="520" y="151" class="svg-label">orbital B</text>
          <circle cx="125" cy="55" r="25" fill="#56a0ad"/><text x="125" y="61" text-anchor="middle" class="svg-title">A</text>
          <circle cx="270" cy="145" r="25" fill="#a987b8"/><text x="270" y="151" text-anchor="middle" class="svg-title">B</text>
          <path d="M125 55 C180 15 220 185 270 145" fill="none" stroke="#ed682d" stroke-width="5"/>
          <text x="155" y="215" class="svg-label">|A ∧ B⟩  antisymmetric 2-particle state</text>
          <g class="probe"><path d="M400 -35 v105" stroke="#fbf7ea" stroke-width="5"/><path d="M387 52 l13 18 l13 -18" fill="none" stroke="#fbf7ea" stroke-width="5"/><text x="400" y="-48" text-anchor="middle" class="svg-title">a(o)</text></g>
          <circle class="result pulse" cx="400" cy="55" r="33" fill="none" stroke="#ed682d" stroke-width="8"/>
        </g>
      </svg>`
  },
  field: {
    domain: "SPACETIME ALGEBRA · ELECTRODYNAMICS",
    title: "An observer contracts the field bivector",
    exact: true,
    build: "F is the electromagnetic bivector",
    read: "Eᵤ = F·u is spatial relative to u",
    wedge: "simple field plane (shown)",
    contractor: "observer velocity u",
    result: "measured electric field Eᵤ",
    explanation: "In spacetime algebra, an observer with unit timelike velocity u extracts the relative electric field by contracting the electromagnetic bivector F. The measured Eᵤ is orthogonal to u.",
    caveat: "<b>Exact with a qualification:</b> a general electromagnetic bivector need not be simple, so it may not be one literal plane. The observer-orthogonality statement remains exact.",
    visual: () => `
      <svg viewBox="0 0 700 350">
        <text x="35" y="38" class="svg-title">FIELD SEEN BY AN OBSERVER</text>
        <ellipse cx="355" cy="195" rx="245" ry="100" fill="#376f7c" fill-opacity=".18" stroke="#56a0ad" stroke-width="2"/>
        <path d="M135 225 C235 90 450 310 575 150" fill="none" stroke="#a987b8" stroke-width="8"/>
        <path d="M125 180 C270 285 425 85 590 210" fill="none" stroke="#56a0ad" stroke-width="8"/>
        <text x="565" y="130" class="svg-label">F</text>
        <g class="probe"><line x1="350" y1="300" x2="350" y2="55" stroke="#fbf7ea" stroke-width="6"/><path d="M338 75 l12 -20 l12 20" fill="none" stroke="#fbf7ea" stroke-width="5"/><text x="370" y="75" class="svg-title">u</text></g>
        <line class="result pulse" x1="350" y1="195" x2="545" y2="195" stroke="#ed682d" stroke-width="12"/><path d="M525 183 l20 12 l-20 12" fill="none" stroke="#ed682d" stroke-width="6"/>
        <text x="450" y="230" class="svg-label">Eᵤ = F·u,  Eᵤ·u = 0</text>
      </svg>`
  },
  threads: {
    domain: "STRING DIAGRAMS · HOPF / TENSOR CALCULUS",
    title: "A cap pulls one wire from a bundle",
    exact: true,
    build: "wires A and B enter an antisymmetric bundle",
    read: "the o-cap pairs, leaving a residual wire",
    wedge: "antisymmetric wire bundle",
    contractor: "evaluation cap / pairing",
    result: "unpaired output wire",
    explanation: "Exterior products and contractions admit a diagrammatic reading: wires tensor together, antisymmetrization supplies signs, and an evaluation cap pairs a dual input with one branch.",
    caveat: "<b>Exact algebraic diagrammatics:</b> the threads are morphism wires, not material strings. This is likely the clearest skin for recursive Sandhi and Viccheda.",
    visual: () => `
      <svg viewBox="0 0 700 350">
        <text x="35" y="38" class="svg-title">SPLIT · PAIR · COLLECT</text>
        <path d="M160 300 C160 230 255 225 255 155 S350 85 350 45" fill="none" stroke="#56a0ad" stroke-width="9"/>
        <path d="M430 300 C430 220 335 220 335 155 S245 90 245 45" fill="none" stroke="#a987b8" stroke-width="9"/>
        <text x="140" y="325" class="svg-label">A</text><text x="420" y="325" class="svg-label">B</text>
        <circle cx="295" cy="155" r="28" fill="#ed682d"/><text x="295" y="161" text-anchor="middle" class="svg-title">∧</text>
        <g class="probe"><path d="M545 45 v92 C545 180 490 180 490 137 v-25" fill="none" stroke="#fbf7ea" stroke-width="7"/><text x="565" y="55" class="svg-title">o*</text></g>
        <path class="result pulse" d="M350 45 C385 95 445 105 490 112" fill="none" stroke="#ed682d" stroke-width="11"/>
        <text x="425" y="225" class="svg-label">cap = contraction</text>
      </svg>`
  },
  dna: {
    domain: "BIOMOLECULAR VISUAL METAPHOR",
    title: "Matching bases unzip and recombine",
    exact: false,
    build: "two strands encode compatible patterns",
    read: "a matching probe selects and releases a segment",
    wedge: "paired strand",
    contractor: "matching enzyme/probe",
    result: "selected sequence",
    explanation: "DNA supplies strong game language: complementary matching, zipping, cutting, repair, mutation, and nested motifs. These motions can make Sandhi memorable.",
    caveat: "<b>Metaphor only:</b> molecular DNA operations are not exterior contraction, and the orthogonality relation has no direct biochemical meaning.",
    visual: () => {
      const rungs = Array.from({length:8},(_,i) => {
        const y=55+i*33, x1=270+Math.sin(i*.9)*70, x2=430-Math.sin(i*.9)*70;
        return `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${i===4?"#ed682d":"rgba(251,247,234,.4)"}" stroke-width="${i===4?9:4}"/><circle cx="${x1}" cy="${y}" r="7" fill="#56a0ad"/><circle cx="${x2}" cy="${y}" r="7" fill="#a987b8"/>`;
      }).join("");
      return `<svg viewBox="0 0 700 350"><text x="35" y="38" class="svg-title">MATCH · ZIP · CUT</text>
        <path d="M270 55 C350 105 190 155 270 205 S350 285 270 320" fill="none" stroke="#56a0ad" stroke-width="7"/>
        <path d="M430 55 C350 105 510 155 430 205 S350 285 430 320" fill="none" stroke="#a987b8" stroke-width="7"/>
        ${rungs}<g class="probe"><path d="M560 80 v105 l-25 25 m25-25 l25 25" stroke="#fbf7ea" fill="none" stroke-width="7"/><text x="585" y="92" class="svg-title">probe o</text></g>
        <line class="result pulse" x1="310" y1="187" x2="390" y2="187" stroke="#ed682d" stroke-width="12"/><text x="485" y="270" class="svg-label">visual skin, not physics</text></svg>`;
    }
  }
};

const stage = document.querySelector(".theme-visual");
let current = "geometry";

function selectTheme(name) {
  current = name;
  const theme = themes[name];
  document.querySelectorAll("[data-theme]").forEach(button =>
    button.classList.toggle("active", button.dataset.theme === name)
  );
  document.querySelector("#themeDomain").textContent = theme.domain;
  document.querySelector("#themeTitle").textContent = theme.title;
  document.querySelector("#buildText").textContent = theme.build;
  document.querySelector("#readText").textContent = theme.read;
  document.querySelector("#wedgeMeaning").textContent = theme.wedge;
  document.querySelector("#contractorMeaning").textContent = theme.contractor;
  document.querySelector("#resultMeaning").textContent = theme.result;
  document.querySelector("#themeExplanation").textContent = theme.explanation;
  document.querySelector("#caveat").innerHTML = theme.caveat;
  const badge = document.querySelector("#truthBadge");
  badge.textContent = theme.exact ? "EXACT REALIZATION" : "VISUAL METAPHOR";
  badge.className = `truth-badge ${theme.exact ? "exact" : "metaphor"}`;
  stage.classList.remove("playing");
  stage.innerHTML = theme.visual();
}

document.querySelectorAll("[data-theme]").forEach(button =>
  button.addEventListener("click", () => selectTheme(button.dataset.theme))
);

document.querySelector("#playButton").addEventListener("click", () => {
  stage.classList.remove("playing");
  void stage.offsetWidth;
  stage.classList.add("playing");
});

selectTheme(current);
