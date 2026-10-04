/* Construction page charts. All numbers come from data/construction.json,
   which scripts/export_data.py builds from the project spreadsheets. */

(function () {
  "use strict";

  var GW = window.GW;
  var c = GW.colors;
  var narrow = window.matchMedia("(max-width: 639px)").matches;
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  function monthLabel(ym) {
    var parts = ym.split("-");
    return MONTHS[Number(parts[1]) - 1] + " " + parts[0];
  }

  function diversionChart(monthly) {
    var months = monthly.months;
    GW.plot("chart-diversion", [
      {
        x: months.map(function (m) { return m.month + "-01"; }),
        y: months.map(function (m) { return m.rate; }),
        customdata: months.map(function (m) { return [monthLabel(m.month), m.diverted_tons, m.landfilled_tons, m.total_tons]; }),
        type: "scatter",
        mode: "lines+markers",
        connectgaps: false,
        line: { color: c.green, width: 2.5 },
        marker: { color: c.green, size: 6, line: { color: "#FFFFFF", width: 1.5 } },
        hovertemplate: "<b>%{customdata[0]}</b><br>Diversion: %{y:.1f}%<br>" +
          "Diverted: %{customdata[1]:,.1f} tons<br>Landfilled: %{customdata[2]:,.1f} tons<extra></extra>"
      }
    ], GW.baseLayout({
      height: 290,
      xaxis: { type: "date", fixedrange: true, showgrid: false, dtick: narrow ? "M12" : "M6", tickformat: "%b<br>%Y", tickfont: { color: c.muted } },
      yaxis: { range: [0, 105], tickvals: [0, 25, 50, 75, 90, 100], ticksuffix: "%", fixedrange: true,
               gridcolor: "rgba(94,104,120,0.15)", zeroline: false, tickfont: { color: c.muted } },
      shapes: [{ type: "line", xref: "paper", x0: 0, x1: 1, y0: 90, y1: 90, line: { color: c.ink, width: 1.5, dash: "dash" } }],
      annotations: [{
        xref: "paper", x: 0.01, y: 90, yanchor: "top", xanchor: "left", showarrow: false,
        text: "TRUE minimum (90%)", font: { size: 11, color: c.ink }, bgcolor: "rgba(255,255,255,0.85)"
      }]
    }));

    GW.table("table-diversion",
      [{ label: "Month" }, { label: "Diversion", num: true }, { label: "Diverted (tons)", num: true }, { label: "Landfilled (tons)", num: true }],
      months.filter(function (m) { return m.total_tons > 0; }).map(function (m) {
        return [monthLabel(m.month), m.rate.toFixed(1) + "%", GW.fmt(m.diverted_tons, 1), GW.fmt(m.landfilled_tons, 1)];
      }));
  }

  function materialsChart(materials) {
    var metal = materials.filter(function (m) { return m.material.toLowerCase() === "metal"; })[0];
    var major = materials.filter(function (m) { return m.tons >= metal.tons; })
      .sort(function (a, b) { return a.tons - b.tons; });
    var label = function (name) { return name.replace(" (ADC)", ""); };

    GW.plot("chart-materials", [{
      type: "bar", orientation: "h",
      x: major.map(function (m) { return m.tons; }),
      y: major.map(function (m) { return label(m.material); }),
      marker: { color: c.green },
      text: major.map(function (m) { return GW.fmt(m.tons); }),
      textposition: "outside", cliponaxis: false,
      textfont: { size: 11, color: c.ink },
      hovertemplate: "<b>%{y}</b><br>%{x:,.1f} tons<extra></extra>"
    }], GW.baseLayout({
      height: 270,
      margin: { l: 128, r: 44, t: 6, b: 30 },
      xaxis: { fixedrange: true, gridcolor: "rgba(94,104,120,0.15)", tickformat: ",.0f", range: [0, major[major.length - 1].tons * 1.2], tickfont: { color: c.muted } },
      yaxis: { fixedrange: true, showgrid: false, tickfont: { color: c.ink } },
      bargap: 0.35
    }));

    GW.table("table-materials",
      [{ label: "Material" }, { label: "Tons", num: true }],
      materials.slice().sort(function (a, b) { return b.tons - a.tons; }).map(function (m) {
        return [label(m.material), GW.fmt(m.tons, 2)];
      }));
  }

  function costChart(costs) {
    var withTrue = costs.with_true / 1e6;
    var without = costs.without_true / 1e6;
    var saved = (without - withTrue).toFixed(1);

    GW.plot("chart-costs", [{
      type: "bar",
      x: ["With source<br>separation", "Mixed bins<br>(estimate)"],
      y: [costs.with_true, costs.without_true],
      width: 0.45,
      marker: { color: [c.green, c.line], line: { color: [c.green, c.muted], width: 1 } },
      text: ["$" + withTrue.toFixed(1) + "M", "$" + without.toFixed(1) + "M"],
      textposition: "outside", cliponaxis: false, textfont: { size: 12, color: c.ink },
      hovertemplate: "<b>%{x}</b><br>$%{y:,.0f}<extra></extra>"
    }], GW.baseLayout({
      height: 260,
      margin: { l: 48, r: 16, t: 30, b: 44 },
      yaxis: { range: [0, costs.without_true * 1.22], tickvals: [0, 2e6, 4e6, 6e6, 8e6], ticktext: ["$0", "$2M", "$4M", "$6M", "$8M"],
               fixedrange: true, gridcolor: "rgba(94,104,120,0.15)", zeroline: false, tickfont: { color: c.muted } },
      annotations: [{
        x: 0.5, y: costs.without_true * 1.13, xref: "x", yref: "y", showarrow: false,
        text: "<b>~$" + saved + "M saved</b>", font: { size: 13, color: c.green }
      }]
    }));

    GW.table("table-costs",
      [{ label: "Scenario" }, { label: "Estimated hauling cost", num: true }],
      [["With source separation", "$" + GW.fmt(costs.with_true)], ["Mixed bins (estimate)", "$" + GW.fmt(costs.without_true)]]);
  }

  function carbonChart(rows) {
    var names = rows.map(function (r) { return r.material.replace(" ", "<br>"); });
    GW.plot("chart-carbon", [
      {
        type: "bar", name: "Embodied carbon remaining",
        x: names, y: rows.map(function (r) { return 100 - r.reduction_percent; }),
        marker: { color: c.green },
        hovertemplate: "<b>%{x}</b><br>%{y}% of the conventional baseline<extra></extra>"
      },
      {
        type: "bar", name: "Reduction",
        x: names, y: rows.map(function (r) { return r.reduction_percent; }),
        marker: { color: "#FFFFFF", line: { color: c.green, width: 1.5 }, pattern: { shape: "/", fgcolor: c.line, size: 6 } },
        text: rows.map(function (r) { return r.label; }), textposition: "inside", insidetextanchor: "middle", textangle: 0,
        textfont: { size: narrow ? 10 : 11, color: c.ink },
        hovertemplate: "<b>%{x}</b><br>%{y}% lower embodied carbon<extra></extra>"
      }
    ], GW.baseLayout({
      height: 260, barmode: "stack", bargap: 0.4,
      margin: { l: 44, r: 10, t: 14, b: 50 },
      yaxis: { range: [0, 100], tickvals: [0, 25, 50, 75, 100], ticksuffix: "%", fixedrange: true,
               gridcolor: "rgba(94,104,120,0.15)", zeroline: false, tickfont: { color: c.muted } }
    }));

    GW.table("table-carbon",
      [{ label: "Material" }, { label: "Lower embodied carbon than baseline", num: true }],
      rows.map(function (r) { return [r.material, r.label.replace(" lower", "")]; }));
  }

  GW.loadJSON("data/construction.json").then(function (data) {
    diversionChart(data.monthly);
    materialsChart(data.materials);
    costChart(data.hauling_costs);
    carbonChart(data.embodied_carbon);
  }).catch(function () {
    document.querySelectorAll(".chart").forEach(function (el) {
      el.innerHTML = '<p class="chart-fallback">This chart could not load right now. Please try refreshing the page.</p>';
    });
  });
})();
