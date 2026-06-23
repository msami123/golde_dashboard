(function () {
  "use strict";

  function initLucide() {
    if (window.lucide) lucide.createIcons();
  }

  function initSidebar() {
    const sidebar = document.getElementById("sidebar");
    const toggle = document.getElementById("sidebar-toggle");
    const mobileBtn = document.getElementById("mobile-menu-btn");
    if (toggle && sidebar) {
      toggle.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
        initLucide();
      });
    }
    if (mobileBtn && sidebar) {
      mobileBtn.addEventListener("click", function () {
        sidebar.classList.toggle("open");
      });
    }
  }

  function initDeleteConfirm() {
    document.querySelectorAll("[data-confirm-delete]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        if (!window.confirm(form.getAttribute("data-confirm-delete"))) e.preventDefault();
      });
    });
  }

  function initParticipants() {
    const container = document.getElementById("participants-container");
    const addBtn = document.getElementById("add-participant-btn");
    if (!container || !addBtn) return;
    addBtn.addEventListener("click", function () {
      const row = document.createElement("div");
      row.className = "participant-row";
      row.style.cssText = "display:grid;grid-template-columns:3fr 1fr auto;gap:0.5rem;margin-bottom:0.5rem;align-items:end;";
      row.innerHTML =
        '<div class="form-group"><input type="text" name="participant_name" class="form-control"></div>' +
        '<div class="form-group"><input type="number" name="participant_pct" class="form-control" min="0" max="100" step="1" value="0"></div>' +
        '<button type="button" class="btn btn-secondary btn-sm remove-participant">×</button>';
      container.appendChild(row);
      bindRemove();
    });
    function bindRemove() {
      container.querySelectorAll(".remove-participant").forEach(function (btn) {
        btn.onclick = function () {
          if (container.querySelectorAll(".participant-row").length > 1)
            btn.closest(".participant-row").remove();
        };
      });
    }
    bindRemove();
  }

  function initSharedToggle() {
    const checkbox = document.getElementById("is_shared");
    const section = document.getElementById("participants-section");
    if (!checkbox || !section) return;
    function toggle() { section.style.display = checkbox.checked ? "block" : "none"; }
    checkbox.addEventListener("change", toggle);
    toggle();
  }

  function initCustomForecast() {
    const input = document.getElementById("custom-forecast-price");
    const result = document.getElementById("custom-forecast-result");
    if (!input || !result) return;
    const totalGrams = parseFloat(result.dataset.totalGrams || "0");
    const totalCost = parseFloat(result.dataset.totalCost || "0");
    const lang = document.body.getAttribute("dir") === "rtl" ? "ar" : "en";
    const currency = lang === "ar" ? "ر.س" : "SAR";
    function fmt(v, signed) {
      const n = Math.round(v * 10) / 10;
      const s = n.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
      return signed ? (n >= 0 ? "+" : "") + s + " " + currency : s + " " + currency;
    }
    function fmtPct(v) {
      const n = Math.round(v * 10) / 10;
      return (n >= 0 ? "+" : "") + n.toFixed(1) + "%";
    }
    function update() {
      const price = parseFloat(input.value);
      if (!price || price <= 0 || !totalGrams) { result.style.display = "none"; return; }
      const value = totalGrams * price;
      const profit = value - totalCost;
      const ret = totalCost ? (profit / totalCost) * 100 : 0;
      result.style.display = "block";
      const valEl = result.querySelector(".forecast-value");
      const profEl = result.querySelector(".forecast-profit");
      const retEl = result.querySelector(".forecast-return");
      if (valEl) valEl.textContent = fmt(value, false);
      if (profEl) { profEl.textContent = fmt(profit, true); profEl.className = "badge forecast-profit " + (profit >= 0 ? "badge-success" : "badge-danger"); }
      if (retEl) retEl.textContent = fmtPct(ret);
    }
    input.addEventListener("input", update);
  }

  function initTablePagination() {
    const table = document.getElementById("bars-table");
    if (!table) return;
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const perPage = 10;
    let page = 1;
    const searchInput = document.getElementById("table-search");
    const filterSelect = document.getElementById("table-filter");
    const pageInfo = document.getElementById("page-info");
    const prevBtn = document.getElementById("prev-page");
    const nextBtn = document.getElementById("next-page");

    function visibleRows() {
      const q = (searchInput?.value || "").toLowerCase();
      const ft = filterSelect?.value || "";
      return rows.filter(function (row) {
        const matchQ = !q || (row.dataset.search || "").includes(q);
        const matchT = !ft || ft === filterSelect.options[0].value || row.dataset.type === ft;
        row.style.display = matchQ && matchT ? "" : "none";
        return matchQ && matchT;
      });
    }

    function render() {
      const vis = visibleRows();
      const total = Math.max(1, Math.ceil(vis.length / perPage));
      if (page > total) page = total;
      vis.forEach(function (row, i) {
        const show = i >= (page - 1) * perPage && i < page * perPage;
        if (row.style.display !== "none") row.style.display = show ? "" : "none";
      });
      if (pageInfo) pageInfo.textContent = page + " / " + total + " (" + vis.length + " rows)";
    }

    if (searchInput) searchInput.addEventListener("input", function () { page = 1; render(); });
    if (filterSelect) filterSelect.addEventListener("change", function () { page = 1; render(); });
    if (prevBtn) prevBtn.addEventListener("click", function () { if (page > 1) { page--; render(); } });
    if (nextBtn) nextBtn.addEventListener("click", function () { page++; render(); });
    render();
  }

  function initAccordion() {
    document.querySelectorAll(".accordion-trigger").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = btn.closest(".accordion-item");
        if (item) item.classList.toggle("open");
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initLucide();
    initSidebar();
    initDeleteConfirm();
    initParticipants();
    initSharedToggle();
    initCustomForecast();
    initTablePagination();
    initAccordion();
  });
})();
