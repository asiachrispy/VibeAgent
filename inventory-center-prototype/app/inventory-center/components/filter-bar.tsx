"use client";

import { RotateCcw, Search, SlidersHorizontal } from "lucide-react";
import type { InventoryFilters, InventoryStatus, Marketplace, Warehouse } from "../lib/types";
import { categories, marketplaces, statusLabels, statuses, warehouses } from "../lib/mock-data";

interface FilterBarProps {
  filters: InventoryFilters;
  onChange: (filters: InventoryFilters) => void;
  onReset: () => void;
}

const selectClass =
  "h-10 w-full rounded-md border border-ink/12 bg-porcelain px-3 text-sm text-ink shadow-sm transition hover:border-harbor/40";

export function FilterBar({ filters, onChange, onReset }: FilterBarProps) {
  const updateFilter = <K extends keyof InventoryFilters>(
    key: K,
    value: InventoryFilters[K]
  ) => onChange({ ...filters, [key]: value });

  return (
    <section className="rounded-lg border border-ink/10 bg-porcelain p-3 shadow-ledger">
      <div className="flex items-center gap-2 border-b border-ink/8 pb-3">
        <SlidersHorizontal className="h-4 w-4 text-harbor" aria-hidden="true" />
        <h2 className="text-sm font-semibold text-ink">库存筛选控制台</h2>
        <button
          type="button"
          onClick={onReset}
          className="ml-auto inline-flex h-8 items-center gap-1 rounded-md border border-ink/10 px-2 text-xs text-ink/70 transition hover:border-harbor/30 hover:text-harbor"
          title="重置筛选条件"
        >
          <RotateCcw className="h-3.5 w-3.5" aria-hidden="true" />
          重置
        </button>
      </div>
      <div className="mt-3 grid gap-3 md:grid-cols-2 xl:grid-cols-[1.2fr_1fr_1fr_1fr_1fr]">
        <label className="relative block">
          <span className="sr-only">搜索 SKU、ASIN、商品或供应商</span>
          <Search className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-ink/38" />
          <input
            value={filters.keyword}
            onChange={(event) => updateFilter("keyword", event.target.value)}
            placeholder="搜索 SKU / ASIN / 商品 / 供应商"
            className="h-10 w-full rounded-md border border-ink/12 bg-porcelain pl-9 pr-3 text-sm text-ink shadow-sm transition placeholder:text-ink/36 hover:border-harbor/40"
          />
        </label>
        <select
          aria-label="平台筛选"
          value={filters.marketplace}
          onChange={(event) =>
            updateFilter("marketplace", event.target.value as Marketplace | "全部平台")
          }
          className={selectClass}
        >
          <option>全部平台</option>
          {marketplaces.map((marketplace) => (
            <option key={marketplace}>{marketplace}</option>
          ))}
        </select>
        <select
          aria-label="仓库筛选"
          value={filters.warehouse}
          onChange={(event) =>
            updateFilter("warehouse", event.target.value as Warehouse | "全部仓库")
          }
          className={selectClass}
        >
          <option>全部仓库</option>
          {warehouses.map((warehouse) => (
            <option key={warehouse}>{warehouse}</option>
          ))}
        </select>
        <select
          aria-label="库存状态筛选"
          value={filters.status}
          onChange={(event) =>
            updateFilter("status", event.target.value as InventoryStatus | "全部状态")
          }
          className={selectClass}
        >
          <option value="全部状态">全部状态</option>
          {statuses.map((status) => (
            <option key={status} value={status}>
              {statusLabels[status]}
            </option>
          ))}
        </select>
        <select
          aria-label="品类筛选"
          value={filters.category}
          onChange={(event) => updateFilter("category", event.target.value)}
          className={selectClass}
        >
          <option>全部品类</option>
          {categories.map((category) => (
            <option key={category}>{category}</option>
          ))}
        </select>
      </div>
    </section>
  );
}
