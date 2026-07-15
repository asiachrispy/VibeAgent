"use client";

import clsx from "clsx";
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronsUpDown,
  Download,
  Eye
} from "lucide-react";
import Papa from "papaparse";
import { formatCurrency, formatNumber } from "../lib/analytics";
import { statusLabels } from "../lib/mock-data";
import type { InventoryItem, SortConfig } from "../lib/types";

interface InventoryTableProps {
  items: InventoryItem[];
  totalCount: number;
  currentPage: number;
  totalPages: number;
  sortConfig: SortConfig;
  onSort: (key: keyof InventoryItem) => void;
  onPageChange: (page: number) => void;
  onSelectItem: (item: InventoryItem) => void;
  exportRows: InventoryItem[];
}

interface CsvExportRow {
  SKU: string;
  ASIN: string;
  商品: string;
  平台: string;
  仓库: string;
  状态: string;
  可售: number;
  预留: number;
  在途: number;
  日均销量: number;
  覆盖天数: number;
  建议补货: number;
  库存金额: number;
  负责人: string;
}

const statusClass: Record<InventoryItem["status"], string> = {
  healthy: "bg-sea/10 text-sea",
  low: "bg-amber/12 text-amber",
  out: "bg-ember/12 text-ember",
  overstock: "bg-plum/12 text-plum",
  inbound: "bg-moss/12 text-moss",
  stranded: "bg-ink/10 text-ink/70"
};

const columns: Array<{ key: keyof InventoryItem; label: string; align?: "right" }> = [
  { key: "sku", label: "SKU" },
  { key: "marketplace", label: "平台" },
  { key: "warehouse", label: "仓库" },
  { key: "available", label: "可售", align: "right" },
  { key: "inbound", label: "在途", align: "right" },
  { key: "daysOfCover", label: "覆盖天数", align: "right" },
  { key: "recommendedReplenishment", label: "建议补货", align: "right" },
  { key: "inventoryValue", label: "金额", align: "right" }
];

function getDaysOfCoverClass(daysOfCover: number): string {
  if (daysOfCover < 16) return "bg-ember/12 text-ember";
  if (daysOfCover <= 90) return "bg-sea/10 text-sea";
  return "bg-plum/12 text-plum";
}

function getExportRows(items: InventoryItem[]): CsvExportRow[] {
  return items.map((item) => ({
    SKU: item.sku,
    ASIN: item.asin,
    商品: item.productName,
    平台: item.marketplace,
    仓库: item.warehouse,
    状态: statusLabels[item.status],
    可售: item.available,
    预留: item.reserved,
    在途: item.inbound,
    日均销量: item.dailySales,
    覆盖天数: item.daysOfCover,
    建议补货: item.recommendedReplenishment,
    库存金额: item.inventoryValue,
    负责人: item.owner
  }));
}

export function InventoryTable({
  items,
  totalCount,
  currentPage,
  totalPages,
  sortConfig,
  onSort,
  onPageChange,
  onSelectItem,
  exportRows
}: InventoryTableProps): JSX.Element {
  const exportCsv = () => {
    const csv = Papa.unparse(getExportRows(exportRows));
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "inventory-center-export.csv";
    anchor.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="rounded-lg border border-ink/10 bg-porcelain shadow-ledger">
      <div className="flex flex-col gap-3 border-b border-ink/10 p-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="font-display text-xl font-semibold text-ink">SKU 库存明细</h2>
          <p className="mt-1 text-sm text-ink/56">共 {formatNumber(totalCount)} 条，支持排序、分页、详情下钻和 CSV 导出</p>
        </div>
        <button
          type="button"
          onClick={exportCsv}
          className="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-ink px-3 text-sm font-medium text-porcelain transition hover:bg-harbor"
          title="导出当前筛选结果"
        >
          <Download className="h-4 w-4" aria-hidden="true" />
          导出 CSV
        </button>
      </div>

      <div className="scrollbar-thin overflow-x-auto">
        <table className="w-full min-w-[1120px] border-collapse text-left text-sm">
          <thead className="bg-paper/80 text-xs uppercase tracking-[0.08em] text-ink/52">
            <tr>
              <th className="w-[260px] px-4 py-3 font-semibold">商品</th>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={clsx("px-3 py-3 font-semibold", column.align === "right" && "text-right")}
                >
                  <button
                    type="button"
                    onClick={() => onSort(column.key)}
                    className={clsx(
                      "inline-flex items-center gap-1 rounded-sm text-inherit transition hover:text-harbor",
                      column.align === "right" && "justify-end"
                    )}
                  >
                    {column.label}
                    {sortConfig.key === column.key ? (
                      <ChevronDown
                        className={clsx(
                          "h-3.5 w-3.5 transition",
                          sortConfig.direction === "asc" && "rotate-180"
                        )}
                        aria-hidden="true"
                      />
                    ) : (
                      <ChevronsUpDown className="h-3.5 w-3.5" aria-hidden="true" />
                    )}
                  </button>
                </th>
              ))}
              <th className="px-3 py-3 font-semibold">状态</th>
              <th className="px-4 py-3 text-right font-semibold">操作</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} className="border-t border-ink/8 transition hover:bg-paper/70">
                <td className="px-4 py-3">
                  <div className="max-w-[250px]">
                    <p className="truncate font-medium text-ink">{item.productName}</p>
                    <p className="mt-1 font-mono text-xs text-ink/48">
                      {item.asin} · {item.category}
                    </p>
                  </div>
                </td>
                <td className="px-3 py-3 font-mono text-xs text-ink">{item.sku}</td>
                <td className="px-3 py-3 text-ink/70">{item.marketplace}</td>
                <td className="px-3 py-3 text-ink/70">{item.warehouse}</td>
                <td className="px-3 py-3 text-right font-medium">{formatNumber(item.available)}</td>
                <td className="px-3 py-3 text-right text-ink/70">{formatNumber(item.inbound)}</td>
                <td className="px-3 py-3 text-right">
                  <span
                    className={clsx(
                      "rounded-full px-2 py-1 text-xs font-medium",
                      getDaysOfCoverClass(item.daysOfCover)
                    )}
                  >
                    {item.daysOfCover} 天
                  </span>
                </td>
                <td className="px-3 py-3 text-right font-medium text-amber">
                  {formatNumber(item.recommendedReplenishment)}
                </td>
                <td className="px-3 py-3 text-right">{formatCurrency(item.inventoryValue)}</td>
                <td className="px-3 py-3">
                  <span className={clsx("rounded-full px-2 py-1 text-xs", statusClass[item.status])}>
                    {statusLabels[item.status]}
                  </span>
                </td>
                <td className="px-4 py-3 text-right">
                  <button
                    type="button"
                    onClick={() => onSelectItem(item)}
                    className="inline-grid h-8 w-8 place-items-center rounded-md border border-ink/10 text-ink/60 transition hover:border-harbor/30 hover:text-harbor"
                    title="查看 SKU 详情"
                  >
                    <Eye className="h-4 w-4" aria-hidden="true" />
                  </button>
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td colSpan={11} className="px-4 py-12 text-center text-sm text-ink/56">
                  当前筛选条件下暂无库存数据
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex flex-col gap-3 border-t border-ink/10 p-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-ink/56">
          第 {currentPage} / {Math.max(totalPages, 1)} 页
        </p>
        <div className="flex items-center gap-2">
          <button
            type="button"
            disabled={currentPage <= 1}
            onClick={() => onPageChange(currentPage - 1)}
            className="inline-flex h-9 items-center gap-1 rounded-md border border-ink/10 px-3 text-sm text-ink/70 transition hover:border-harbor/30 hover:text-harbor disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronLeft className="h-4 w-4" aria-hidden="true" />
            上一页
          </button>
          <button
            type="button"
            disabled={currentPage >= totalPages}
            onClick={() => onPageChange(currentPage + 1)}
            className="inline-flex h-9 items-center gap-1 rounded-md border border-ink/10 px-3 text-sm text-ink/70 transition hover:border-harbor/30 hover:text-harbor disabled:cursor-not-allowed disabled:opacity-40"
          >
            下一页
            <ChevronRight className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      </div>
    </section>
  );
}
