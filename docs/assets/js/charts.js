/* Shared chart helpers. Loaded only on pages with charts, after plotly.js
   and site.js. Every chart also gets a plain data table for screen readers
   and anyone who prefers numbers to shapes. */

(function () {
  "use strict";

  var GW = window.GW;
  var c = GW.colors;

  GW.baseLayout = function (extra) {
    var layout = {
      font: { family: GW.font, size: 12, color: c.ink },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      margin: { l: 48, r: 16, t: 10, b: 40 },
      showlegend: false,
      hoverlabel: { bgcolor: "#FFFFFF", bordercolor: c.line, font: { family: GW.font, size: 12, color: c.ink } },
      xaxis: { fixedrange: true, showgrid: false, tickfont: { color: c.muted } },
      yaxis: { fixedrange: true, gridcolor: "rgba(94,104,120,0.15)", zeroline: false, tickfont: { color: c.muted } }
    };
    return Object.assign(layout, extra || {});
  };

  GW.plot = function (id, traces, layout) {
    var el = document.getElementById(id);
    if (!el) return;
    if (!window.Plotly) {
      el.innerHTML = '<p class="chart-fallback">The chart could not load. The data table below has the same numbers.</p>';
      return;
    }
    el.innerHTML = "";
    window.Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true, scrollZoom: false });
  };

  /* Fill a <details class="table-fold"> with a data table. */
  GW.table = function (id, headers, rows) {
    var holder = document.getElementById(id);
    if (!holder) return;
    var head = headers.map(function (h) {
      return '<th scope="col"' + (h.num ? ' class="num"' : "") + ">" + h.label + "</th>";
    }).join("");
    var body = rows.map(function (row) {
      return "<tr>" + row.map(function (cell, i) {
        return "<td" + (headers[i].num ? ' class="num"' : "") + ">" + cell + "</td>";
      }).join("") + "</tr>";
    }).join("");
    holder.innerHTML = '<div class="table-scroll"><table class="data-table"><thead><tr>' + head +
      "</tr></thead><tbody>" + body + "</tbody></table></div>";
  };

  GW.fmt = function (value, digits) {
    return Number(value).toLocaleString("en-US", { minimumFractionDigits: digits || 0, maximumFractionDigits: digits || 0 });
  };
})();
