/* Shared Operate chrome: health, nav, fetch, deep-link parse. */
(function (global) {
  const NAV = [
    { id: "clearance", href: "/", label: "Clearance" },
    { id: "policies", href: "/policies", label: "Policies" },
    { id: "metrics", href: "/metrics", label: "Metrics" },
    { id: "audit", href: "/audit", label: "Audit" },
    { id: "matrix", href: "/matrix", label: "Matrix" },
    { id: "architecture", href: "/architecture", label: "Architecture" },
    { id: "runbook", href: "/runbook", label: "Runbook" },
  ];

  const SCENARIOS = {
    refund: "refund",
    decision: "refund",
    "decision-support": "refund",
    support: "support",
    "customer-support": "support",
    copilot: "copilot",
    "internal-copilot": "copilot",
  };

  const Bay = {
    reduceMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    NAV,

    $(id) {
      return document.getElementById(id);
    },

    escape(value) {
      return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    },

    async json(url, opts) {
      const res = await fetch(url, opts);
      if (!res.ok) {
        const body = await res.text();
        throw new Error(body || `${res.status} ${url}`);
      }
      const type = res.headers.get("content-type") || "";
      if (type.includes("application/json")) return res.json();
      return res.text();
    },

    get(url) {
      return this.json(url);
    },

    post(url, body) {
      const opts = { method: "POST" };
      if (body !== undefined) {
        opts.headers = { "Content-Type": "application/json" };
        opts.body = JSON.stringify(body);
      }
      return this.json(url, opts);
    },

    parseDeepLink(search) {
      const q = new URLSearchParams(search || location.search);
      return {
        scenario: q.get("scenario") || "",
        mode: q.get("mode") || "",
        autorun: q.get("autorun") === "1",
        request: q.get("request") || "",
        cell: q.get("cell") || "",
      };
    },

    normalizeScenario(raw) {
      if (!raw) return "";
      return SCENARIOS[String(raw).toLowerCase().trim()] || "";
    },

    normalizeMode(raw) {
      const m = String(raw || "").toLowerCase().trim();
      if (m === "enforce" || m === "shadow") return m;
      return "";
    },

    navIdFromPath(path) {
      const p = (path || location.pathname).replace(/\/$/, "") || "/";
      if (p === "/" || p.endsWith("/index.html")) return "clearance";
      const hit = NAV.find((item) => p.endsWith(item.href.replace("/static/", "")));
      if (hit) return hit.id;
      if (p.includes("policies")) return "policies";
      if (p.includes("metrics")) return "metrics";
      if (p.includes("audit")) return "audit";
      if (p.includes("matrix")) return "matrix";
      if (p.includes("architecture")) return "architecture";
      if (p.includes("runbook")) return "runbook";
      return "clearance";
    },

    markNav() {
      const key = this.navIdFromPath();
      document.querySelectorAll("[data-nav]").forEach((a) => {
        const on = a.dataset.nav === key;
        a.classList.toggle("active", on);
        if (on) a.setAttribute("aria-current", "page");
        else a.removeAttribute("aria-current");
      });
    },

    async health() {
      const lamp = this.$("lamp");
      const text = this.$("healthText");
      if (!lamp || !text) return;
      try {
        const j = await this.get("/healthz");
        lamp.className = "lamp on";
        text.textContent = `lane 1 · ${j.uptime_s}s up`;
      } catch {
        lamp.className = "lamp bad";
        text.textContent = "bay offline";
      }
    },

    fmtFnr(value) {
      if (value == null) return "n/a";
      return `${(Number(value) * 100).toFixed(0)}%`;
    },

    fmtMs(value) {
      if (value == null || Number.isNaN(Number(value))) return "—";
      return Number(value).toFixed(2);
    },

    boot() {
      this.markNav();
      this.health();
      setInterval(() => this.health(), 15000);
    },
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => Bay.boot());
  } else {
    Bay.boot();
  }

  global.Bay = Bay;
})(window);
