# Gateway Sustainability Systems

**Live site: https://ucberkeleyzerowaste.github.io/gateway-dashboard/**

How UC Berkeley's Barbara and Gerson Bakar Gateway runs on zero waste. Gateway is the first building in the world pursuing TRUE Zero Waste certification for both construction and operations.

## At a glance

| | |
|---|---|
| **TRUE Platinum** | Construction, awarded August 2026 |
| **99.01%** | Construction waste diverted from landfill |
| **66,751 tons** | Kept out of landfill during construction |
| **~$1.8M** | Saved through source separation |

## What's on the site

- **Construction:** how Gateway earned TRUE Platinum before it opened
- **01 Building Systems:** what goes in must come out
- **02 Reuse Systems:** making reuse the easiest option every day
- **03 Circular Purchasing:** reuse and refill first, then buy smart
- **04 Recovery Systems:** compost, e-waste, and batteries kept out of landfill
- **Resource Library:** sorting guide, kitchen, catering, event, and café guides, and the Approved Products Catalog
- **[TRUE Facility Case Study (PDF)](docs/assets/Gateway_TRUE_Case_Study.pdf)**

## How it's built

A static site: plain HTML, CSS, and JavaScript in [`/docs`](docs), with charts drawn by Plotly from JSON exported from the project's spreadsheets (`scripts/export_data.py`). GitHub Pages serves it straight from the `static-site` branch, with no build step.

The earlier Streamlit dashboard is preserved on `main` and at the `streamlit-final` tag.

## Credits

Site designed and built by **Audrey Pollack**, Project Coordinator.

The systems it describes are carried out by the Cal Zero Waste Gateway team, part of UC Berkeley Facilities Services, with funding from The Green Initiative Fund (TGIF):

- Sam Bunke, PhD, Zero Waste Specialist
- Audrey Pollack, Project Coordinator
- Tiana Elgidi, Data and Analytics Staff Associate
- Maia Berges Voorhis, Education and Outreach Staff Associate
- Luisa Cervantes Nualart, Research and Documentation Staff Associate
