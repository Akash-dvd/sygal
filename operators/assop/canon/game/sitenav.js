/* Renders the same page list in the same order everywhere and marks the
 * current page with aria-current="page". */

const SITE_PAGES = [
  { href: "index.html", label: "Theorem game" },
  { href: "field.html", label: "Pattern field" },
  { href: "cascade.html", label: "Orbital cascade" },
  { href: "foundry.html", label: "Fermionic foundry" },
  { href: "packets.html", label: "Candy merge" },
  { href: "germ.html", label: "Germ culture" },
  { href: "chamber.html", label: "Reaction chamber" },
  { href: "loom.html", label: "Thread loom" },
  { href: "themes.html", label: "Visual languages" },
  { href: "docs/visual/index.html", label: "Mutation worlds" },
  { href: "docs/visual/phage.html", label: "Seam phage" },
];

function gameRootPrefix() {
  const path = window.location.pathname.replace(/\\/g, "/");
  if (path.includes("/docs/visual/")) return "../../";
  if (path.includes("/docs/")) return "../";
  return "";
}

function currentPageKey() {
  const path = window.location.pathname.replace(/\\/g, "/");
  if (path.includes("/docs/visual/")) {
    const file = path.split("/").pop() || "index.html";
    return `docs/visual/${file}`;
  }
  const file = path.split("/").pop();
  return file === "" ? "index.html" : file;
}

function renderSiteNav() {
  const here = currentPageKey();
  const prefix = gameRootPrefix();

  document.querySelectorAll("[data-site-nav]").forEach((host) => {
    host.setAttribute("aria-label", "Pages");
    host.innerHTML = SITE_PAGES.map((page) => {
      const active = page.href === here;
      return `<a href="${prefix}${page.href}"${active ? ' aria-current="page"' : ""}>${page.label}</a>`;
    }).join("");

    // Keep the highlighted page visible when the strip has to scroll.
    const active = host.querySelector('[aria-current="page"]');
    if (active) {
      const centered = active.offsetLeft - (host.clientWidth - active.offsetWidth) / 2;
      host.scrollLeft = Math.max(0, centered);
    }
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", renderSiteNav);
} else {
  renderSiteNav();
}
