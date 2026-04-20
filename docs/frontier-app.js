(function () {
  const data = window.PM_FRONTIER_MODEL_DATA;
  if (!data || !Array.isArray(data.rows)) {
    console.error("Missing frontier model site data.");
    return;
  }

  const state = {
    query: "",
    provider: "all",
    minCoverage: 0,
    sortKey: "realized_occupation_exposure_100",
    sortDirection: "desc",
  };

  const elements = {
    snapshot: document.getElementById("metric-snapshot"),
    models: document.getElementById("metric-models"),
    topScore: document.getElementById("metric-top-score"),
    topModel: document.getElementById("metric-top-model"),
    median: document.getElementById("metric-median"),
    baselineDae: document.getElementById("baseline-dae"),
    baselineSe: document.getElementById("baseline-se"),
    baselineOc: document.getElementById("baseline-oc"),
    baselineIc: document.getElementById("baseline-ic"),
    baselineTasks: document.getElementById("baseline-tasks"),
    searchInput: document.getElementById("search-input"),
    providerFilter: document.getElementById("provider-filter"),
    coverageFilter: document.getElementById("coverage-filter"),
    coverageOutput: document.getElementById("coverage-output"),
    sortSelect: document.getElementById("sort-select"),
    sortDirection: document.getElementById("sort-direction"),
    resetFilters: document.getElementById("reset-filters"),
    resultCount: document.getElementById("result-count"),
    coverageSummary: document.getElementById("coverage-summary"),
    comparisonBody: document.getElementById("comparison-body"),
  };

  function formatScore(value) {
    return Number(value).toFixed(2);
  }

  function formatCoverage(value) {
    return `${Math.round(Number(value) * 100)}%`;
  }

  function buildProviderOptions() {
    const providers = Array.from(
      new Set(data.rows.map((row) => row.provider || "Unknown"))
    ).sort((left, right) => left.localeCompare(right));

    const defaultOption = document.createElement("option");
    defaultOption.value = "all";
    defaultOption.textContent = "All providers";
    elements.providerFilter.appendChild(defaultOption);

    providers.forEach((provider) => {
      const option = document.createElement("option");
      option.value = provider;
      option.textContent = provider;
      elements.providerFilter.appendChild(option);
    });
  }

  function renderSummary() {
    elements.snapshot.textContent = data.snapshot_month;
    elements.models.textContent = String(data.summary.tracked_model_count);
    elements.topScore.textContent = formatScore(
      data.summary.top_model.realized_occupation_exposure_100
    );
    elements.topModel.textContent = `${data.summary.top_model.display_name} (${data.summary.top_model.provider})`;
    elements.median.textContent = formatScore(
      data.summary.median_realized_occupation_exposure_100
    );

    elements.baselineDae.textContent = formatScore(data.occupation.weighted_dae_100);
    elements.baselineSe.textContent = formatScore(data.occupation.weighted_se_100);
    elements.baselineOc.textContent = formatScore(data.occupation.weighted_oc_100);
    elements.baselineIc.textContent = formatScore(data.occupation.weighted_ic_100);
    elements.baselineTasks.textContent = String(data.occupation.included_task_count);
  }

  function matchesQuery(row, query) {
    if (!query) {
      return true;
    }
    const haystack = [
      row.display_name,
      row.frontier_model_id,
      row.provider,
      ...(row.benchmarks || []),
      ...(row.selected_systems || []),
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(query);
  }

  function sortRows(rows) {
    const sorted = rows.slice().sort((left, right) => {
      const leftValue = left[state.sortKey];
      const rightValue = right[state.sortKey];

      if (typeof leftValue === "string" || typeof rightValue === "string") {
        const stringCompare = String(leftValue).localeCompare(String(rightValue));
        return state.sortDirection === "asc" ? stringCompare : -stringCompare;
      }

      const numericCompare = Number(leftValue) - Number(rightValue);
      return state.sortDirection === "asc" ? numericCompare : -numericCompare;
    });

    return sorted;
  }

  function filteredRows() {
    const query = state.query.toLowerCase();
    return data.rows.filter((row) => {
      if (!matchesQuery(row, query)) {
        return false;
      }
      if (state.provider !== "all" && row.provider !== state.provider) {
        return false;
      }
      if (Number(row.benchmark_coverage_ratio) < state.minCoverage) {
        return false;
      }
      return true;
    });
  }

  function clearTable() {
    while (elements.comparisonBody.firstChild) {
      elements.comparisonBody.removeChild(elements.comparisonBody.firstChild);
    }
  }

  function createCell(content, className) {
    const cell = document.createElement("td");
    if (className) {
      cell.className = className;
    }
    if (content instanceof Node) {
      cell.appendChild(content);
    } else {
      cell.textContent = content;
    }
    return cell;
  }

  function renderRows() {
    const rows = sortRows(filteredRows());
    clearTable();

    elements.resultCount.textContent = `${rows.length} frontier families shown`;
    elements.coverageSummary.textContent = `Matched public systems in full snapshot: ${data.summary.matched_source_system_count}`;

    rows.forEach((row) => {
      const tr = document.createElement("tr");

      const rank = document.createElement("span");
      rank.className = "rank-pill";
      rank.textContent = String(row.rank);
      tr.appendChild(createCell(rank));

      const familyCell = document.createElement("td");
      const familyName = document.createElement("span");
      familyName.className = "system-name";
      familyName.textContent = row.display_name;
      const familyId = document.createElement("span");
      familyId.className = "system-id";
      familyId.textContent = row.frontier_model_id;
      familyCell.appendChild(familyName);
      familyCell.appendChild(familyId);
      tr.appendChild(familyCell);

      tr.appendChild(createCell(row.provider));

      const scoreCell = document.createElement("td");
      const scoreStrong = document.createElement("span");
      scoreStrong.className = "score-strong";
      scoreStrong.textContent = formatScore(row.realized_occupation_exposure_100);
      scoreCell.appendChild(scoreStrong);
      tr.appendChild(scoreCell);

      const coverageCell = document.createElement("td");
      const coverageStrong = document.createElement("span");
      coverageStrong.className = "coverage-strong";
      coverageStrong.textContent = formatCoverage(row.benchmark_coverage_ratio);
      const coverageMeta = document.createElement("span");
      coverageMeta.className = "system-id";
      coverageMeta.textContent = `${row.benchmark_count} benchmarks`;
      coverageCell.appendChild(coverageStrong);
      coverageCell.appendChild(coverageMeta);
      tr.appendChild(coverageCell);

      const benchmarkCell = document.createElement("td");
      const benchmarkList = document.createElement("div");
      benchmarkList.className = "benchmark-list";
      (row.benchmarks || []).forEach((benchmark) => {
        const chip = document.createElement("span");
        chip.className = "benchmark-chip";
        chip.textContent = benchmark;
        benchmarkList.appendChild(chip);
      });
      benchmarkCell.appendChild(benchmarkList);
      tr.appendChild(benchmarkCell);

      const systemCell = document.createElement("td");
      const selectedList = document.createElement("div");
      selectedList.className = "selected-system-list";
      (row.selected_systems || []).forEach((entry) => {
        const item = document.createElement("div");
        item.className = "selected-system-item";
        item.textContent = entry;
        selectedList.appendChild(item);
      });
      const systemMeta = document.createElement("span");
      systemMeta.className = "system-id";
      systemMeta.textContent = `${row.source_system_count} matched public systems, ${row.selected_system_count} selected`;
      systemCell.appendChild(selectedList);
      systemCell.appendChild(systemMeta);
      tr.appendChild(systemCell);

      elements.comparisonBody.appendChild(tr);
    });
  }

  function resetControls() {
    state.query = "";
    state.provider = "all";
    state.minCoverage = 0;
    state.sortKey = "realized_occupation_exposure_100";
    state.sortDirection = "desc";

    elements.searchInput.value = "";
    elements.providerFilter.value = "all";
    elements.coverageFilter.value = "0";
    elements.coverageOutput.value = "0%";
    elements.sortSelect.value = "realized_occupation_exposure_100";
    elements.sortDirection.textContent = "Descending";
    renderRows();
  }

  function bindEvents() {
    elements.searchInput.addEventListener("input", (event) => {
      state.query = event.target.value.trim();
      renderRows();
    });

    elements.providerFilter.addEventListener("change", (event) => {
      state.provider = event.target.value;
      renderRows();
    });

    elements.coverageFilter.addEventListener("input", (event) => {
      state.minCoverage = Number(event.target.value) / 100;
      elements.coverageOutput.value = `${event.target.value}%`;
      renderRows();
    });

    elements.sortSelect.addEventListener("change", (event) => {
      state.sortKey = event.target.value;
      renderRows();
    });

    elements.sortDirection.addEventListener("click", () => {
      state.sortDirection = state.sortDirection === "desc" ? "asc" : "desc";
      elements.sortDirection.textContent =
        state.sortDirection === "desc" ? "Descending" : "Ascending";
      renderRows();
    });

    elements.resetFilters.addEventListener("click", resetControls);
  }

  buildProviderOptions();
  renderSummary();
  bindEvents();
  resetControls();
})();
