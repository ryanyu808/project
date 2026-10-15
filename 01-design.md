## 2. Architecture Diagram

```text
                  RAW CPSC INJURY DATA
                           |
                           v
          +--------------------------------+
          | 02-data.md (Richard)                    |
          | DATA PREPARATION               |
          |                                |
          | - Filter ages 65–120           |
          | - Product code 3277            |
          | - Check Narrative_1            |
          | - Classify injury mechanisms   |
          | - Clean and validate records   |
          |                                |
          | Runs: Once ahead of time       |
          +--------------------------------+
                           |
                    Cleaned DataFrame
                           |
                           v
          +--------------------------------+
          | 03-loader.md (James)                  |
          | DATA LOADING & VALIDATION      |
          |                                |
          | - Load prepared data           |
          | - Validate required columns    |
          | - Check Weight and severity    |
          | - Precompute summary metrics   |
          |                                |
          | Runs: Ahead of time / startup  |
          +--------------------------------+
                           |
                   Loaded DataFrame
                           |
                           v
          +--------------------------------+
          | 04-filters.md (Parth)                 |
          | FILTERS                        |
          |                                |
          | - Filter by injury mechanism   |
          | - Filter by severity           |
          | - Apply user selections        |
          |                                |
          | Runs: On each filter change    |
          +--------------------------------+
                           |
                  Filtered DataFrame
                           |
                           v
          +--------------------------------+
          | 05-views.md (Ryan)                   |
          | DASHBOARD VISUALIZATIONS       |
          |                                |
          | - Estimated national ED visits |
          | - Severe outcome comparisons   |
          | - Injury mechanism charts      |
          | - Summary tables               |
          |                                |
          | Runs: On each interaction      |
          +--------------------------------+
                           ^
                           |
                    Dashboard settings
                           |
          +--------------------------------+
          | 06-setup.md (Colby)                   |
          | SETUP & CONFIGURATION          |
          |                                |
          | - Dashboard layout             |
          | - Default filter settings      |
          | - Available charts and views   |
          | - User interface configuration |
          |                                |
          | Runs: When dashboard starts    |
          +--------------------------------+
```

## 3. Design Decisions

**1. Clear Pieces:** We will divide the dashboard into five components so that data preparation, loading, filtering, visualization, and setup can be developed and tested independently.

**2. Simple Connections:** Components will exchange pandas DataFrames with clearly defined inputs and outputs. Each component will focus on its own responsibility without modifying unrelated components.

**3. Local Changes:** We will keep data preparation rules, filtering logic, visualizations, and dashboard settings separate. This allows us to update injury classifications or dashboard features without rewriting the entire application.

**4. Real-World Operation:** We will clean and classify the injury data once ahead of time, then load the prepared data when the dashboard starts. We will cache reusable calculations to avoid unnecessary processing during user interactions.