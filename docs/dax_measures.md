# DAX Measures Catalog & Python Semantic Layer Reconciliation

This document catalogs every DAX measure implemented in **Power BI** and maps it to its source definition in the **Python Metric Framework / Production Semantic Layer** (Olist E-Commerce Platform).

---

## 1. Core Metrics & Cross-Platform Reconciliation

| Business Metric | Metric Tier | Power BI (DAX Measure) | Display Folder | Python Metric Layer Reference | Reconciliation Status |
|---|---|---|---|---|---|
| **Good Orders** | **North Star** | `[Good Orders]` | `1 North Star` | `monthly_kpis['good_orders']` | ✅ Exact Match (All 20 Months) |
| **Valid Orders** | Input | `[Valid Orders]` | `2 Inputs` | `monthly_kpis['orders']` | ✅ Exact Match (All 20 Months) |
| **Delivered** | Input | `[Delivered]` | `2 Inputs` | `monthly_kpis['delivered']` | ✅ Exact Match (All 20 Months) |
| **On Time** | Input | `[On Time]` | `2 Inputs` | `monthly_kpis['on_time']` | ✅ Exact Match (All 20 Months) |
| **Delivered Rate** | Input | `[Delivered Rate]` | `2 Inputs` | `monthly_kpis['delivered_rate']` | ✅ Exact Match |
| **On-Time Rate** | Input | `[On-Time Rate]` | `2 Inputs` | `monthly_kpis['on_time_rate']` | ✅ Exact Match |
| **Good Review Rate** | Input | `[Good Review Rate]` | `2 Inputs` | `monthly_kpis['good_review_rate']` | ✅ Exact Match |
| **GMV** | Guardrail | `[GMV]` | `3 Guardrails` | `monthly_kpis['gmv']` | ✅ Exact Match (Rounded 2 Dec) |
| **Avg Promised Days** | Guardrail | `[Avg Promised Days]` | `3 Guardrails` | `monthly_kpis['promised_days']` | ✅ Exact Match |
| **Cancellation Rate** | Guardrail | `[Cancellation Rate]` | `3 Guardrails` | `monthly_kpis['cancellation_rate']` | ✅ Exact Match |
| **Freight Share** | Guardrail | `[Freight Share]` | `3 Guardrails` | `monthly_kpis['freight_share']` | ✅ Exact Match |
| **New Customers** | Input | `[New Customers]` | `2 Inputs` | `monthly_kpis['new_customers']` | ✅ Exact Match (All 20 Months) |
| **Repeat Rate (Window)** | Diagnostic | `[Repeat Rate Within Window]` | `4 Diagnostics` | `customer_repeat_mart` | ✅ Exact Match |
| **Buyer M3 Retention** | Diagnostic | `[Buyer M3 Retention]` | `4 Diagnostics` | `buyer_cohort_matrix` | ✅ Exact Match (~0.25%) |
| **Seller M3 Retention** | Diagnostic | `[Seller M3 Retention]` | `4 Diagnostics` | `seller_cohort_matrix` | ✅ Exact Match (~53.2%) |

---

## 2. North Star Decomposition (Waterfall) Measures

These measures power the log-decomposition waterfall chart explaining month-over-month movement in Good Orders:

$$\Delta \ln(\text{Good Orders}) = \Delta \ln(\text{Orders}) + \Delta \ln(\text{Delivered Rate}) + \Delta \ln(\text{On-Time Rate}) + \Delta \ln(\text{Good Review Rate})$$

- **`[Component Value]`**: Dynamic switch returning the metric corresponding to the selected row in `NS Components`.
- **`[Log Contribution]`**: Calculates $\ln(\text{Value}_{t}) - \ln(\text{Value}_{t-1})$ inside modified filter context using `DATEADD(dim_date[Date], -1, MONTH)`.
- **`[Δ ln Good Orders]`**: Total target change $\ln(\text{Good Orders}_t) - \ln(\text{Good Orders}_{t-1})$.

---

## 3. Reconciliation Verification (QA) Measures

Measures evaluated on the **Reconciliation** page against expected targets exported from the Python semantic model (`expected_monthly_kpis.csv`):

- `[Δ Orders vs Target] = [Valid Orders] - SUM(expected_monthly_kpis[orders])` $\rightarrow$ **0 across all months**
- `[Δ Good Orders vs Target] = [Good Orders] - SUM(expected_monthly_kpis[good_orders])` $\rightarrow$ **0 across all months**
- `[Δ GMV vs Target] = ROUND([GMV] - SUM(expected_monthly_kpis[gmv]), 2)` $\rightarrow$ **0 across all months**
