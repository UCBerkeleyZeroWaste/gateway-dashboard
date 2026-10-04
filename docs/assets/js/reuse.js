/* Reuse page chart. Numbers come from data/reuse.json, which
   scripts/export_data.py builds from Data/starter_kit_2026.csv. */

(function () {
  "use strict";

  var GW = window.GW;
  var c = GW.colors;

  GW.loadJSON("data/reuse.json").then(function (data) {
    var rows = data.plastic.cumulative;
    GW.plot("chart-plastic", [{
      type: "bar",
      x: rows.map(function (r) { return String(r.year); }),
      y: rows.map(function (r) { return r.kg; }),
      width: 0.5,
      marker: { color: c.green },
      text: rows.map(function (r) { return r.kg.toFixed(2) + " kg"; }),
      textposition: "outside", cliponaxis: false, textfont: { size: 12, color: c.ink },
      hovertemplate: "<b>%{x}</b><br>%{y:.2f} kg prevented (running total)<extra></extra>"
    }], GW.baseLayout({
      height: 240,
      margin: { l: 44, r: 12, t: 16, b: 30 },
      xaxis: { type: "category", fixedrange: true, showgrid: false, tickfont: { color: c.ink } },
      yaxis: { range: [0, rows[rows.length - 1].kg * 1.25], ticksuffix: " kg", fixedrange: true,
               gridcolor: "rgba(94,104,120,0.15)", zeroline: false, tickfont: { color: c.muted } }
    }));

    GW.table("table-plastic",
      [{ label: "Year" }, { label: "Plastic prevented, running total", num: true }],
      rows.map(function (r) { return [String(r.year), r.kg.toFixed(2) + " kg"]; }));
  }).catch(function () {
    document.getElementById("chart-plastic").innerHTML =
      '<p class="chart-fallback">This chart could not load right now. Please try refreshing the page.</p>';
  });
})();
