"use client";

import { useEffect, useMemo, useState } from "react";
import { Boxes, ClipboardList, Factory, LayoutDashboard, PackageSearch, RefreshCw } from "lucide-react";
import { motion } from "framer-motion";
import { FilterBar } from "./filter-bar";
import { InventoryCharts } from "./charts";
import { InventoryTable } from "./inventory-table";
import { StatCard } from "./stat-card";
import { DetailPanel } from "./detail-panel";
import {
  applyFilters,
  getInventoryMetrics,
  getPageItems,
  getStatusData,
  getTrendData,
  getWarehouseData,
  sortInventory
} from "../lib/analytics";
import { inventoryData } from "../lib/mock-data";
import type { InventoryFilters, InventoryItem, SortConfig } from "../lib/types";

const initialFilters: InventoryFilters = {
  marketplace: "全部平台",
  warehouse: "全部仓库",
  status: "全部状态",
  category: "全部品类",
  keyword: ""
};

const pageSize = 12;

const navItems = [
  { label: "库存总览", icon: LayoutDashboard, active: true },
  { label: "库存明细", icon: PackageSearch, active: false },
  { label: "补货计划", icon: ClipboardList, active: false },
  { label: "仓库调拨", icon: Boxes, active: false },
  { label: "供应商协同", icon: Factory, active: false }
];

export function InventoryCenterDashboard() {
  const [filters, setFilters] = useState<InventoryFilters>(initialFilters);
  const [sortConfig, setSortConfig] = useState<SortConfig>({
    key: "recommendedReplenishment",
    direction: "desc"
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedItem, setSelectedItem] = useState<InventoryItem | null>(null);

  const filteredData = useMemo(() => applyFilters(inventoryData, filters), [filters]);
  const sortedData = useMemo(
    () => sortInventory(filteredData, sortConfig),
    [filteredData, sortConfig]
  );
  const pageItems = useMemo(
    () => getPageItems(sortedData, currentPage, pageSize),
    [sortedData, currentPage]
  );
  const totalPages = Math.ceil(sortedData.length / pageSize);
  const metrics = useMemo(() => getInventoryMetrics(filteredData), [filteredData]);
  const trendData = useMemo(() => getTrendData(filteredData), [filteredData]);
  const warehouseData = useMemo(() => getWarehouseData(filteredData), [filteredData]);
  const statusData = useMemo(() => getStatusData(filteredData), [filteredData]);

  useEffect(() => {
    setCurrentPage(1);
  }, [filters]);

  const handleSort = (key: keyof InventoryItem) => {
    setSortConfig((current) => ({
      key,
      direction: current.key === key && current.direction === "desc" ? "asc" : "desc"
    }));
  };

  return (
    <main className="min-h-screen overflow-x-hidden text-ink">
      <div className="grid min-h-screen min-w-0 lg:grid-cols-[248px_1fr]">
        <aside className="min-w-0 border-b border-ink/10 bg-ink px-4 py-5 text-porcelain lg:border-b-0 lg:border-r">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-md bg-amber text-ink">
              <Boxes className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <p className="font-display text-lg font-semibold">Vibe ERP</p>
              <p className="text-xs text-porcelain/58">Cross-border Inventory</p>
            </div>
          </div>

          <nav className="mt-8 flex min-w-0 gap-2 overflow-x-auto lg:block lg:space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.label}
                  type="button"
                  className={`inline-flex h-10 shrink-0 items-center gap-2 rounded-md px-3 text-sm transition lg:w-full ${
                    item.active
                      ? "bg-porcelain text-ink"
                      : "text-porcelain/68 hover:bg-porcelain/10 hover:text-porcelain"
                  }`}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {item.label}
                </button>
              );
            })}
          </nav>

          <div className="mt-8 hidden rounded-lg border border-porcelain/12 bg-porcelain/6 p-4 lg:block">
            <p className="text-xs uppercase tracking-[0.16em] text-porcelain/46">Today focus</p>
            <p className="mt-3 text-sm leading-6 text-porcelain/78">
              优先处理缺货 SKU、FBA 到仓延迟和 90 天以上库龄库存，减少断货与资金占用。
            </p>
          </div>
        </aside>

        <section className="min-w-0 px-4 py-5 sm:px-6 lg:px-7">
          <motion.header
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-5 flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between"
          >
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.18em] text-harbor">
                ERP / 库存中心 / 2026-05-29
              </p>
              <h1 className="mt-2 font-display text-4xl font-semibold tracking-normal text-ink">
                跨境库存中心
              </h1>
              <p className="mt-2 max-w-3xl break-words text-sm leading-6 text-ink/62">
                统一管理多平台、多海外仓、FBA 与在途库存，帮助卖家快速发现断货、积压、搁置和补货风险。
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                className="inline-flex h-10 items-center gap-2 rounded-md border border-ink/12 bg-porcelain px-3 text-sm font-medium text-ink transition hover:border-harbor/30 hover:text-harbor"
                title="模拟同步库存"
              >
                <RefreshCw className="h-4 w-4" aria-hidden="true" />
                同步库存
              </button>
              <button
                type="button"
                onClick={() => setFilters({ ...initialFilters, status: "low" })}
                className="inline-flex h-10 items-center gap-2 rounded-md bg-ember px-3 text-sm font-medium text-porcelain transition hover:bg-ink"
              >
                查看低库存
              </button>
            </div>
          </motion.header>

          <div className="space-y-4">
            <FilterBar
              filters={filters}
              onChange={setFilters}
              onReset={() => setFilters(initialFilters)}
            />

            <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              {metrics.map((metric, index) => (
                <StatCard key={metric.label} metric={metric} index={index} />
              ))}
            </section>

            <InventoryCharts
              trendData={trendData}
              warehouseData={warehouseData}
              statusData={statusData}
            />

            <InventoryTable
              items={pageItems}
              totalCount={sortedData.length}
              currentPage={currentPage}
              totalPages={totalPages}
              sortConfig={sortConfig}
              onSort={handleSort}
              onPageChange={setCurrentPage}
              onSelectItem={setSelectedItem}
              exportRows={sortedData}
            />
          </div>
        </section>
      </div>

      {selectedItem && <div className="fixed inset-0 z-40 bg-ink/28" onClick={() => setSelectedItem(null)} />}
      <DetailPanel item={selectedItem} onClose={() => setSelectedItem(null)} />
    </main>
  );
}
