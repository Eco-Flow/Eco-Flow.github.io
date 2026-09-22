// Render ```mermaid code blocks in lessons as diagrams.
//
// Kramdown renders them as <pre><code class="language-mermaid">, which Mermaid
// does not pick up on its own, so convert those blocks first. The library is
// only fetched on pages that actually contain a diagram, and the blocks are
// only replaced once it has loaded, so a failed load leaves the original code
// block on the page rather than an empty gap.

const blocks = document.querySelectorAll("pre > code.language-mermaid");

if (blocks.length) {
  const { default: mermaid } = await import(
    "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"
  );

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "neutral",
    fontFamily: "inherit",
  });

  blocks.forEach((code) => {
    const diagram = document.createElement("div");
    diagram.className = "mermaid";
    diagram.style.overflowX = "auto";
    diagram.textContent = code.textContent;
    code.parentElement.replaceWith(diagram);
  });

  await mermaid.run({ nodes: document.querySelectorAll("div.mermaid") });
}
