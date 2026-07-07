# Task: Build Complete Professional Frontend

Build the full UI for the 4D Ecosystem Simulator using modern best practices. 

**Tech Stack:** Streamlit (UI), Shapely (2D spatial geometry), PyVista (3D rendering), Plotly (charts).

**Strict Rules:**
1. **Clean Architecture:** UI only renders data. Keep all Shapely math/logic in the domain layer.
2. **VM Safe (CRITICAL):** Set `pyvista.OFF_SCREEN = True`. Export 3D renders as static images or HTML to display in Streamlit. Do not open native windows.
3. **Modern UI:** Use Streamlit tabs, columns, and custom CSS for a professional, fast dashboard experience.

**Execution Steps:**

1. Build a modular UI with 4 main tabs: 
   - **Dashboard:** High-level metrics.
   - **2D Layout:** Interactive Shapely polygon visualization of A/C rows.
   - **3D Strata:** PyVista 3D rendering of tree heights/canopy.
   - **Metabolism:** Plotly charts for biomass flows.
2. Generate mock data to make the UI fully functional and visually impressive.


Execute autonomously. Do not ask for permission.
