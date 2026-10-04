/* Candy merge — nested sandhi from test1.py
 *
 * t1 =
 *   (d1 < (a1∧a2 ∧ (d2 < (b1∧b2 ∧ (d3 < (c1∧c2∧c3))))))
 *   ∧
 *   (d1 < (a3∧a4 ∧ (d2 < (b3∧b4 ∧ (d3 < (c1∧c2∧c3∧c4))))))
 *
 * t1_1 =
 *   ((d1∧d2∧d3)|(c1∧c2∧c3))
 *   ·
 *   (d1 < (a1∧a2∧a3∧a4 ∧ (d2 < (b1∧b2∧b3∧b4 ∧ (d3 < (c1∧c2∧c3∧c4))))))
 */

const COLS = 12;
const ROWS = 10;
const stride = () =>
  parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--stride")) || 43;

const SHELLS_L = [
  { wrap: "d1", candy: ["a1", "a2"] },
  { wrap: "d2", candy: ["b1", "b2"] },
  { wrap: "d3", candy: ["c1", "c2", "c3"] },
];
const SHELLS_R = [
  { wrap: "d1", candy: ["a3", "a4"] },
  { wrap: "d2", candy: ["b3", "b4"] },
  { wrap: "d3", candy: ["c1", "c2", "c3", "c4"] },
];

const state = {
  cards: [],
  selected: null,
  nextId: 1,
  kappa: null,
};

const el = {
  table: document.getElementById("table"),
  yard: document.getElementById("yard"),
  hand: document.getElementById("hand"),
  signL: document.getElementById("signL"),
  signR: document.getElementById("signR"),
  rungCount: document.getElementById("rungCount"),
  status: document.getElementById("statusLine"),
  exprL: document.getElementById("exprL"),
  exprR: document.getElementById("exprR"),
  metaL: document.getElementById("metaL"),
  metaR: document.getElementById("metaR"),
  kappa: document.getElementById("kappaExpr"),
  kappaMeta: document.getElementById("kappaMeta"),
  reset: document.getElementById("resetButton"),
  peel: document.getElementById("reshapeButton"),
  join: document.getElementById("rotateButton"),
  candy: document.getElementById("candyButton"),
};

function esc(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const keyOf = (x, y) => `${x},${y}`;
const cloneShells = (shells) => shells.map((shell) => ({ wrap: shell.wrap, candy: [...shell.candy] }));
const signMark = (sign) => (sign < 0 ? "−" : "+");

function wedgeExpr(row) {
  if (!row.length) return "∅";
  if (row.length === 1) return row[0];
  return `(${row.join("∧")})`;
}

function expr(piece) {
  let acc = "";
  for (let i = piece.shells.length - 1; i >= 0; i -= 1) {
    const shell = piece.shells[i];
    let inner;
    if (!acc) inner = wedgeExpr(shell.candy);
    else if (shell.candy.length) inner = `${wedgeExpr(shell.candy)}∧(${acc})`;
    else inner = acc;
    acc = inner.includes("<") ? `${shell.wrap}<(${inner})` : `${shell.wrap}<${inner}`;
  }
  return `${signMark(piece.sign)} ${acc}`;
}

function wrapLine(piece) {
  return piece.shells.map((shell) => shell.wrap).join("∧");
}

function innerCandy(piece) {
  return piece.shells[piece.shells.length - 1].candy;
}

function residualGrade(piece) {
  return innerCandy(piece).length - piece.shells.length;
}

function gradeLabel(n) {
  if (n > 0) return `+${n}`;
  if (n === 0) return "0";
  return `−${-n}`;
}

function gradeLine(piece) {
  const inner = innerCandy(piece);
  return `d-tower g${piece.shells.length} · inner Dr g${inner.length} · ${gradeLabel(residualGrade(piece))}`;
}

function layoutCells(piece) {
  const width = Math.max(1, ...piece.shells.map((shell) => Math.max(1, shell.candy.length)));
  const cells = [];
  let y = 0;
  piece.shells.forEach((shell, i) => {
    const wrapShift = width - 1;
    cells.push({
      bead: shell.wrap, role: "pin", rung: `w${i}`, index: 0,
      x: wrapShift, y, shell: i, kind: "wrap", inner: true, outer: true,
    });
    y += 1;
    if (!shell.candy.length) return;
    const candyShift = width - shell.candy.length;
    shell.candy.forEach((bead, j) => {
      cells.push({
        bead, role: "body", rung: `c${i}`, index: j,
        x: candyShift + j, y, shell: i, kind: "candy",
      });
    });
    y += 1;
  });
  return cells;
}

function worldCells(piece) {
  return piece.cells.map((cell) => ({
    ...cell,
    x: cell.x + piece.origin.x,
    y: cell.y + piece.origin.y,
  }));
}

function treePairs(cells) {
  const byRung = new Map();
  cells.forEach((cell) => {
    const list = byRung.get(cell.rung) || [];
    list.push(cell);
    byRung.set(cell.rung, list);
  });
  const pairs = [];
  const shells = new Set(cells.map((cell) => cell.shell));
  shells.forEach((i) => {
    const wrap = (byRung.get(`w${i}`) || [])[0];
    const candy = (byRung.get(`c${i}`) || []).sort((a, b) => a.index - b.index);
    const nextWrap = (byRung.get(`w${i + 1}`) || [])[0];
    candy.forEach((cell, j) => {
      if (j < candy.length - 1) pairs.push([cell, candy[j + 1]]);
    });
    if (wrap && candy.length) {
      const mid = {
        x: (candy[0].x + candy[candy.length - 1].x) / 2,
        y: candy[0].y,
        shell: wrap.shell,
      };
      pairs.push([wrap, mid]);
    }
    if (wrap && nextWrap) pairs.push([wrap, nextWrap]);
  });
  return pairs;
}

function edgeMarkup(from, to) {
  const step = stride();
  const x1 = (from.x + 0.5) * step;
  const y1 = (from.y + 0.5) * step;
  const x2 = (to.x + 0.5) * step;
  const y2 = (to.y + 0.5) * step;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.hypot(dx, dy);
  const ang = Math.atan2(dy, dx) * (180 / Math.PI);
  const a = from.shell ?? 0;
  const b = to.shell ?? 0;
  const shell = Math.max(a, b);
  return `<i class="edge" data-shell="${shell}" data-angle="${ang}" style="left:${x1}px;top:${y1}px;width:${len}px;transform:rotate(${ang}deg)"></i>`;
}

function occupyExcept(id) {
  const map = new Map();
  state.cards.forEach((piece) => {
    if (piece.id === id) return;
    worldCells(piece).forEach((cell) => map.set(keyOf(cell.x, cell.y), true));
  });
  return map;
}

function blocked(piece) {
  const taken = occupyExcept(piece.id);
  return worldCells(piece).some((cell) => {
    if (cell.x < 0 || cell.y < 0 || cell.x >= COLS || cell.y >= ROWS) return true;
    return taken.has(keyOf(cell.x, cell.y));
  });
}

function nudgeIntoPlace(piece) {
  if (!blocked(piece)) return true;
  const saved = { ...piece.origin };
  for (let radius = 1; radius <= 8; radius += 1) {
    for (let dx = -radius; dx <= radius; dx += 1) {
      for (let dy = -radius; dy <= radius; dy += 1) {
        if (Math.max(Math.abs(dx), Math.abs(dy)) !== radius) continue;
        piece.origin = { x: saved.x + dx, y: saved.y + dy };
        if (!blocked(piece)) return true;
      }
    }
  }
  piece.origin = saved;
  return false;
}

function relayout(piece) {
  piece.cells = layoutCells(piece);
  nudgeIntoPlace(piece);
  retargetFocus(piece);
}

function retargetFocus(piece) {
  if (!piece.focus) return;
  const cell = piece.cells.find((item) => item.bead === piece.focus.bead && item.role === piece.focus.role);
  if (cell) {
    piece.focus = {
      rung: cell.rung, index: cell.index, role: cell.role, bead: cell.bead,
      shell: cell.shell, kind: cell.kind,
    };
  }
}

function makePiece(shells, origin) {
  const piece = {
    id: state.nextId++,
    sign: 1,
    shells: cloneShells(shells),
    origin: { ...origin },
    cells: [],
    focus: null,
  };
  relayout(piece);
  return piece;
}

function rowOf(piece, node) {
  if (!node || node.kind !== "candy") return null;
  return piece.shells[node.shell] ? piece.shells[node.shell].candy : null;
}

function swapAdjacent(piece, node, dir) {
  const row = rowOf(piece, node);
  if (!row) return false;
  const other = node.index + dir;
  if (other < 0 || other >= row.length) return false;
  [row[node.index], row[other]] = [row[other], row[node.index]];
  piece.sign *= -1;
  return true;
}

function unionCandy(left, right) {
  const pool = [];
  left.forEach((candy) => {
    if (!pool.includes(candy)) pool.push(candy);
  });
  right.forEach((candy) => {
    if (!pool.includes(candy)) pool.push(candy);
  });
  return pool;
}

function wrapsMatch(left, right) {
  if (left.shells.length !== right.shells.length) return false;
  return left.shells.every((shell, i) => shell.wrap === right.shells[i].wrap);
}

function candyReady() {
  if (state.cards.length !== 2) return null;
  const [left, right] = state.cards;
  if (!wrapsMatch(left, right)) return null;
  const last = left.shells.length - 1;
  const seam = [...new Set(left.shells[last].candy.filter((candy) => right.shells[last].candy.includes(candy)))];
  if (!seam.length) return null;
  const shells = left.shells.map((shell, i) => ({
    wrap: shell.wrap,
    candy: unionCandy(shell.candy, right.shells[i].candy),
  }));
  const kappa = `(${wrapLine(left)})|(${seam.join("∧")})`;
  return { left, right, seam, shells, kappa };
}

function setStatus(text) {
  el.status.textContent = text;
}

function pieceMarkup(piece, side) {
  const selected = state.selected && state.selected.id === piece.id;
  const worlds = worldCells(piece);
  const tag = worlds[0] || { x: piece.origin.x, y: piece.origin.y };
  const ready = candyReady();
  const classes = ["piece"];
  if (selected) classes.push("selected");
  if (piece.sign < 0) classes.push("neg");
  if (ready) classes.push("dockable");
  if (residualGrade(piece) < 0) classes.push("zeroable");

  const tiles = worlds.map((cell) => {
    const marks = ["cell", cell.role === "pin" ? "pin" : "body"];
    if (cell.inner) marks.push("edge-inner");
    if (piece.focus && piece.focus.bead === cell.bead && piece.focus.role === cell.role) marks.push("focus");
    if (cell.kind === "candy" && ready && cell.shell === piece.shells.length - 1 && ready.seam.includes(cell.bead)) {
      marks.push("seam");
    }
    return `<button class="${marks.join(" ")}" data-bead="${cell.bead}" data-rung="${cell.rung}" data-index="${cell.index}" data-shell="${cell.shell}" data-kind="${cell.kind}" type="button"
      style="left:calc(${cell.x} * var(--stride));top:calc(${cell.y} * var(--stride))">${cell.bead}</button>`;
  }).join("");

  const edges = treePairs(worlds).map(([from, to]) => edgeMarkup(from, to)).join("");
  const neg = piece.sign < 0 ? " neg" : "";

  return `
    <div class="${classes.join(" ")}" data-id="${piece.id}" data-side="${side}">
      <span class="sign-badge${neg}" style="left:calc(${tag.x} * var(--stride) - 8px);top:calc(${tag.y} * var(--stride) - 26px)">${signMark(piece.sign)}</span>
      <span class="piece-tag" style="left:calc(${tag.x} * var(--stride));top:calc(${tag.y} * var(--stride))">${esc(expr(piece))}</span>
      ${edges}
      ${tiles}
    </div>`;
}

function paintYard() {
  el.yard.style.setProperty("--cols", COLS);
  el.yard.style.setProperty("--rows", ROWS);
  el.yard.innerHTML = Array.from({ length: COLS * ROWS }, () => '<i class="slot"></i>').join("");
}

function render() {
  el.hand.innerHTML = state.cards.map((piece, i) => pieceMarkup(piece, i === 0 ? "L" : "R")).join("");
  const [left, right] = state.cards;
  el.signL.textContent = left ? signMark(left.sign) : "+";
  el.signR.textContent = right ? signMark(right.sign) : "+";
  el.signL.style.color = left && left.sign < 0 ? "var(--orange)" : "";
  el.signR.style.color = right && right.sign < 0 ? "var(--orange)" : "";
  const selected = state.selected || left;
  const grade = selected ? residualGrade(selected) : 0;
  el.rungCount.textContent = selected ? gradeLabel(grade) : "0";
  el.rungCount.style.color = grade < 0 ? "var(--orange)" : "";
  if (el.exprL) el.exprL.textContent = left ? expr(left) : "—";
  if (el.exprR) el.exprR.textContent = right ? expr(right) : "—";
  if (el.metaL) el.metaL.textContent = left ? gradeLine(left) : "";
  if (el.metaR) el.metaR.textContent = right ? gradeLine(right) : "pooled";
  if (el.kappa) el.kappa.textContent = state.kappa || "—";
  if (el.kappaMeta) el.kappaMeta.textContent = state.kappa ? "Capelli scalar" : "waiting for sandhi";
  if (el.candy) el.candy.classList.toggle("ready", Boolean(candyReady()));
}

const nodeFor = (id) => el.hand.querySelector(`[data-id="${id}"]`);

function select(piece) {
  state.selected = piece;
  setStatus(`Selected. ${expr(piece)}. Matching d-towers candy-merge on the inner c-seam.`);
  render();
}

function moveSelected(dx, dy) {
  const piece = state.selected;
  if (!piece) return;
  const snapshot = { ...piece.origin };
  piece.origin = { x: piece.origin.x + dx, y: piece.origin.y + dy };
  if (blocked(piece)) piece.origin = snapshot;
  else render();
}

function peelSelected() {
  const piece = state.selected;
  if (!piece) {
    setStatus("Select a wrap, then peel leftover candy into a nested wrap.");
    return;
  }
  const node = peelTarget(piece);
  const ok = applyReshape(
    piece,
    () => peelCandy(piece, node),
    () => `Peeled into a nested wrap. ${expr(piece)}`,
    "Nothing to peel. Grab leftover candy and peel, or drag it up.",
  );
  if (ok) render();
}

function joinSelected() {
  const piece = state.selected;
  if (!piece) {
    setStatus("Select a nested wrap, then fold it back into the wedge.");
    return;
  }
  const focus = piece.focus;
  const foldAt = focus && Number.isInteger(focus.shell) ? focus.shell : 0;
  const ok = applyReshape(
    piece,
    () => foldShell(piece, foldAt),
    () => `Folded back into the wedge. ${expr(piece)}`,
    "Nothing to fold. Peel leftover candy first, then fold that wrap.",
  );
  if (ok) render();
}

function startLab() {
  state.nextId = 1;
  state.selected = null;
  state.kappa = null;
  state.cards = [
    makePiece(SHELLS_L, { x: 1, y: 0 }),
    makePiece(SHELLS_R, { x: 7, y: 0 }),
  ];
  if (blocked(state.cards[1])) {
    state.cards[1].origin = { x: 6, y: 0 };
    relayout(state.cards[1]);
  }
  setStatus("test1 nested sandhi. Same d1,d2,d3 foil; inner c-candy is the seam. Candy merge.");
  render();
}

function candyMerge() {
  if (state.cards.length < 2) {
    setStatus("Need two nested wraps to merge.");
    return;
  }
  const [left, right] = state.cards;
  if (!wrapsMatch(left, right)) {
    setStatus("d-towers don't match. Sandhi needs the same nested annihilators.");
    return;
  }
  const ready = candyReady();
  if (!ready) {
    setStatus("No shared inner candy. The d-tower has no seam to eat.");
    return;
  }
  const merged = makePiece(ready.shells, { ...left.origin });
  merged.sign = left.sign * right.sign;
  if (blocked(merged)) nudgeIntoPlace(merged);
  state.cards = [merged];
  state.selected = merged;
  state.kappa = ready.kappa;
  setStatus(`Candy merge. κ = ${ready.kappa}. Pool grew. ${expr(merged)}`);
  render();
}

const drag = {
  id: null,
  pointer: null,
  startX: 0,
  startY: 0,
  origin: null,
  node: null,
  moved: false,
  live: null,
  pieceNode: null,
  liftTargets: [],
};

function restTransform(target) {
  const ang = target.dataset.angle;
  if (ang != null && ang !== "") return `rotate(${ang}deg)`;
  if (target.classList.contains("piece-tag")) return "translate(24px, -20px)";
  return "";
}

function liftTransform(target, px, py) {
  const rest = restTransform(target);
  return rest ? `translate(${px}px, ${py}px) ${rest}` : `translate(${px}px, ${py}px)`;
}

function gatherLiftTargets(pieceNode, node) {
  if (!pieceNode) return [];
  if (node && node.kind === "wrap") {
    const shell = node.shell;
    const targets = [];
    pieceNode.querySelectorAll(".cell").forEach((el) => {
      if (Number(el.dataset.shell) >= shell) targets.push(el);
    });
    pieceNode.querySelectorAll(".edge").forEach((el) => {
      if (Number(el.dataset.shell) >= shell) targets.push(el);
    });
    if (shell === 0) {
      pieceNode.querySelectorAll(".piece-tag, .sign-badge").forEach((el) => targets.push(el));
    }
    return targets;
  }
  if (drag.live) return [drag.live];
  return drag.pieceNode ? [drag.pieceNode] : [];
}

function pieceFromEvent(event) {
  const node = event.target.closest(".piece");
  if (!node) return null;
  return state.cards.find((item) => item.id === Number(node.dataset.id)) || null;
}

function applyLift(px, py) {
  if (!drag.liftTargets.length) {
    drag.liftTargets = gatherLiftTargets(drag.pieceNode || nodeFor(drag.id), drag.node);
  }
  drag.liftTargets.forEach((target) => {
    target.classList.add("lifting");
    target.style.transition = "none";
    target.style.transform = liftTransform(target, px, py);
    target.style.zIndex = target.classList.contains("edge") ? "8" : "9";
  });
}

function clearLiftStyles(targets) {
  (targets || []).forEach((target) => {
    if (!target) return;
    target.classList.remove("lifting", "returning");
    target.style.transform = restTransform(target);
    target.style.zIndex = "";
    target.style.transition = "";
  });
}

function snapBack(targets, done) {
  const list = (targets || []).filter(Boolean);
  if (!list.length) {
    done();
    return;
  }
  list.forEach((target) => {
    target.classList.add("returning");
    target.style.transition = "transform .18s ease";
    const rest = restTransform(target);
    target.style.transform = rest ? `translate(0px, 0px) ${rest}` : "translate(0px, 0px)";
  });
  let finished = false;
  const finish = () => {
    if (finished) return;
    finished = true;
    list[0].removeEventListener("transitionend", finish);
    clearLiftStyles(list);
    done();
  };
  list[0].addEventListener("transitionend", finish);
  window.setTimeout(finish, 220);
}

function restoreSnapshot(piece, snapshot) {
  piece.sign = snapshot.sign;
  piece.shells = cloneShells(snapshot.shells);
  piece.origin = { ...snapshot.origin };
  piece.focus = snapshot.focus ? { ...snapshot.focus } : null;
  relayout(piece);
  retargetFocus(piece);
}

function snapshotOf(piece) {
  return {
    sign: piece.sign,
    shells: cloneShells(piece.shells),
    origin: { ...piece.origin },
    focus: piece.focus ? { ...piece.focus } : null,
  };
}

function peelTarget(piece) {
  const focus = piece.focus;
  if (focus && focus.kind === "candy") return focus;
  const start = focus && Number.isInteger(focus.shell) ? focus.shell : 0;
  for (let i = start; i < piece.shells.length; i += 1) {
    const candy = piece.shells[i].candy;
    if (candy.length) {
      return { kind: "candy", shell: i, index: 0, bead: candy[0], role: "body" };
    }
  }
  return null;
}

function peelCandy(piece, node) {
  if (!node || node.kind !== "candy") return false;
  const shell = piece.shells[node.shell];
  if (!shell || node.index < 0 || node.index >= shell.candy.length) return false;
  const taken = shell.candy[node.index];
  const rest = shell.candy.slice(node.index + 1);
  shell.candy = shell.candy.slice(0, node.index);
  piece.shells.splice(node.shell + 1, 0, { wrap: taken, candy: rest });
  piece.focus = {
    bead: taken, role: "pin", kind: "wrap", shell: node.shell + 1,
    index: 0, rung: `w${node.shell + 1}`,
  };
  return true;
}

function foldShell(piece, shellIndex) {
  if (shellIndex <= 0 || shellIndex >= piece.shells.length) return false;
  const child = piece.shells[shellIndex];
  if (/^d\d+$/.test(child.wrap)) return false;
  const parent = piece.shells[shellIndex - 1];
  const wrapIndex = parent.candy.length;
  parent.candy.push(child.wrap, ...child.candy);
  piece.shells.splice(shellIndex, 1);
  piece.focus = {
    bead: child.wrap, role: "body", kind: "candy", shell: shellIndex - 1,
    index: wrapIndex, rung: `c${shellIndex - 1}`,
  };
  return true;
}

function applyReshape(piece, mutate, okText, failText) {
  const snapshot = snapshotOf(piece);
  if (!mutate()) {
    restoreSnapshot(piece, snapshot);
    setStatus(failText);
    return false;
  }
  relayout(piece);
  retargetFocus(piece);
  if (blocked(piece)) {
    restoreSnapshot(piece, snapshot);
    setStatus("No room for that nest. Move the tree first.");
    return false;
  }
  setStatus(typeof okText === "function" ? okText() : okText);
  return true;
}

function gridSteps(raw, step) {
  const t = raw / step;
  if (Math.abs(t) < 0.35) return 0;
  return Math.sign(t) * Math.max(1, Math.round(Math.abs(t)));
}

function commitCellDrop(piece, node, dx, dy) {
  if (!dx && !dy) {
    setStatus("Returned to the original slot.");
    return false;
  }
  const horizontal = Math.abs(dx) > Math.abs(dy);
  if (!horizontal && node.kind === "candy" && dy < 0) {
    return applyReshape(
      piece,
      () => peelCandy(piece, node),
      () => `Peeled into a nested wrap. ${expr(piece)}`,
      "That sweet cannot nest there.",
    );
  }
  if (!horizontal && node.kind === "candy" && dy > 0) {
    return applyReshape(
      piece,
      () => foldShell(piece, node.shell),
      () => `Folded back into the wedge. ${expr(piece)}`,
      "Fold the nested wrap, not the outer foil. Peel leftover candy first.",
    );
  }
  if (!horizontal) {
    setStatus("Drag leftover candy up to nest it, or twist it sideways.");
    return false;
  }
  if (node.kind !== "candy") {
    setStatus("Foil stays nested. Peel leftover candy, or candy merge.");
    return false;
  }
  return applyReshape(
    piece,
    () => swapAdjacent(piece, node, dx > 0 ? 1 : -1),
    () => `Wrapper twisted. ${expr(piece)}`,
    "No neighbour on that side.",
  );
}

function finishDrag(event) {
  if (drag.id == null || event.pointerId !== drag.pointer) return;
  const piece = state.cards.find((item) => item.id === drag.id);
  const moved = drag.moved;
  const rawX = event.clientX - drag.startX;
  const rawY = event.clientY - drag.startY;
  const liftTargets = drag.liftTargets.slice();
  const node = drag.node;
  const origin = drag.origin;
  drag.id = null;
  drag.pointer = null;
  drag.live = null;
  drag.pieceNode = null;
  drag.node = null;
  drag.moved = false;
  drag.liftTargets = [];
  if (!piece) return;

  if (!moved) {
    clearLiftStyles(liftTargets);
    select(piece);
    return;
  }

  const step = stride();
  const dx = gridSteps(rawX, step);
  const dy = gridSteps(rawY, step);

  if (node && node.kind === "wrap") {
    piece.origin = { x: origin.x + dx, y: origin.y + dy };
    if (blocked(piece) || (!dx && !dy)) {
      piece.origin = { ...origin };
      setStatus("Nested wrap stays attached. Drop on empty grid to move the packet.");
      snapBack(liftTargets, () => render());
      return;
    }
    setStatus(`Moved the nested wrap. Outer foil stays attached. ${expr(piece)}`);
    render();
    return;
  }

  if (node) {
    const ok = commitCellDrop(piece, node, dx, dy);
    if (!ok) {
      snapBack(liftTargets, () => render());
      return;
    }
    render();
    return;
  }

  piece.origin = { x: origin.x + dx, y: origin.y + dy };
  if (blocked(piece) || (!dx && !dy)) {
    piece.origin = { ...origin };
    setStatus("Returned to the original slot.");
    snapBack(liftTargets, () => render());
    return;
  }
  render();
}

el.hand.addEventListener("pointerdown", (event) => {
  const piece = pieceFromEvent(event);
  if (!piece) return;
  event.preventDefault();
  const cell = event.target.closest(".cell");
  const pieceNode = event.target.closest(".piece");
  drag.id = piece.id;
  drag.pointer = event.pointerId;
  drag.startX = event.clientX;
  drag.startY = event.clientY;
  drag.origin = { ...piece.origin };
  drag.moved = false;
  drag.live = cell;
  drag.pieceNode = pieceNode;
  drag.liftTargets = [];
  drag.node = cell
    ? {
      rung: cell.dataset.rung,
      index: Number(cell.dataset.index),
      role: cell.classList.contains("body") ? "body" : "pin",
      bead: cell.dataset.bead,
      shell: Number(cell.dataset.shell),
      kind: cell.dataset.kind,
    }
    : null;
  if (drag.node) piece.focus = { ...drag.node };
  state.selected = piece;
  el.hand.querySelectorAll(".piece.selected").forEach((item) => item.classList.remove("selected"));
  el.hand.querySelectorAll(".cell.focus").forEach((item) => item.classList.remove("focus"));
  const livePiece = nodeFor(piece.id);
  if (livePiece) livePiece.classList.add("selected");
  if (cell) cell.classList.add("focus");
  try {
    (cell || pieceNode).setPointerCapture(event.pointerId);
  } catch (err) {
    /* capture is optional */
  }
});

window.addEventListener("pointermove", (event) => {
  if (drag.id == null || event.pointerId !== drag.pointer) return;
  const px = event.clientX - drag.startX;
  const py = event.clientY - drag.startY;
  if (Math.hypot(px, py) < 3) return;
  drag.moved = true;
  applyLift(px, py);
});

window.addEventListener("pointerup", finishDrag);
window.addEventListener("pointercancel", finishDrag);

el.peel.addEventListener("click", peelSelected);
el.join.addEventListener("click", joinSelected);
if (el.candy) el.candy.addEventListener("click", candyMerge);

document.querySelectorAll("[data-move]").forEach((button) => {
  button.addEventListener("click", () => {
    const [dx, dy] = button.dataset.move.split(",").map(Number);
    moveSelected(dx, dy);
  });
});

window.addEventListener("keydown", (event) => {
  if (!state.selected) return;
  const keys = {
    ArrowUp: [0, -1],
    ArrowDown: [0, 1],
    ArrowLeft: [-1, 0],
    ArrowRight: [1, 0],
  };
  if (keys[event.key]) {
    event.preventDefault();
    moveSelected(...keys[event.key]);
  }
  if (event.key === "c" || event.key === "C" || event.key === "m" || event.key === "M") {
    event.preventDefault();
    candyMerge();
  }
});

el.reset.addEventListener("click", startLab);

try {
  paintYard();
  startLab();
} catch (err) {
  console.error(err);
  if (el.status) el.status.textContent = err.message;
}
