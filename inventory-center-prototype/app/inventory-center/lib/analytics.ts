import dayjs from "dayjs";
import type {
  InventoryFilters,
  InventoryItem,
  InventoryStatus,
  InventoryMetric,
  SortConfig,
  StatusPoint,
  TrendPoint,
  WarehousePoint
} from "./types";

const numberFormatter = new Intl.NumberFormat("zh-CN");
const currencyFormatter = new Intl.NumberFormat("zh-CN", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0
});

const statusColors: Record<InventoryStatus, string> = {
  healthy: "#2E8B8F",
  low: "#D98B2B",
  out: "#B84A38",
  overstock: "#6A4C7B",
  inbound: "#4F7D46",
  stranded: "#6F6557"
};

const statusNames: Record<InventoryStatus, string> = {
  healthy: "健康",
  low: "低库存",
  out: "缺货",
  overstock: "积压",
  inbound: "在途",
  stranded: "搁置"
};

export function formatNumber(value: number): string {
  return numberFormatter.format(value);
}

export function formatCurrency(value: number): string {
  return currencyFormatter.format(value);
}

export function applyFilters(
  data: InventoryItem[],
  filters: InventoryFilters
): InventoryItem[] {
  const keyword = filters.keyword.trim().toLowerCase();

  return data.filter((item) => {
    const matchesMarketplace =
      filters.marketplace === "全部平台" || item.marketplace === filters.marketplace;
    const matchesWarehouse =
      filters.warehouse === "全部仓库" || item.warehouse === filters.warehouse;
    const matchesStatus = filters.status === "全部状态" || item.status === filters.status;
    const matchesCategory = filters.category === "全部品类" || item.category === filters.category;
    const matchesKeyword =
      keyword.length === 0 ||
      [item.sku, item.asin, item.productName, item.supplier]
        .join(" ")
        .toLowerCase()
        .includes(keyword);

    return (
      matchesMarketplace &&
      matchesWarehouse &&
      matchesStatus &&
      matchesCategory &&
      matchesKeyword
    );
  });
}

export function sortInventory(
  data: InventoryItem[],
  sortConfig: SortConfig
): InventoryItem[] {
  const multiplier = sortConfig.direction === "asc" ? 1 : -1;

  return [...data].sort((a, b) => {
    const left = a[sortConfig.key];
    const right = b[sortConfig.key];

    if (left === right) return 0;
    return left > right ? multiplier : -multiplier;
  });
}

export function getInventoryMetrics(data: InventoryItem[]): InventoryMetric[] {
  const totalSku = data.length;
  const available = data.reduce((sum, item) => sum + item.available, 0);
  const inbound = data.reduce((sum, item) => sum + item.inbound, 0);
  const value = data.reduce((sum, item) => sum + item.inventoryValue, 0);
  const riskSku = data.filter((item) => item.status === "low" || item.status === "out").length;
  const strandedValue = data
    .filter((item) => item.status === "stranded" || item.ageBucket === "90天以上")
    .reduce((sum, item) => sum + item.inventoryValue, 0);

  return [
    {
      label: "可售库存",
      value: formatNumber(available),
      helper: `${formatNumber(totalSku)} 个 SKU 覆盖筛选范围`,
      trend: "+6.8% vs 上周",
      tone: "harbor"
    },
    {
      label: "缺货/低库存 SKU",
      value: formatNumber(riskSku),
      helper: "建议优先处理补货单与调拨单",
      trend: riskSku > 18 ? "+3 个风险" : "-5 个风险",
      tone: "ember"
    },
    {
      label: "在途数量",
      value: formatNumber(inbound),
      helper: "包含采购在途、FBA 入仓、海外仓调拨",
      trend: "18 批 ETA < 7 天",
      tone: "moss"
    },
    {
      label: "库存金额",
      value: formatCurrency(value),
      helper: `呆滞/搁置金额 ${formatCurrency(strandedValue)}`,
      trend: "资金占用健康",
      tone: "plum"
    }
  ];
}

export function getTrendData(data: InventoryItem[]): TrendPoint[] {
  const available = data.reduce((sum, item) => sum + item.available, 0);
  const inbound = data.reduce((sum, item) => sum + item.inbound, 0);
  const riskSku = data.filter((item) => item.risk !== "低").length;

  return Array.from({ length: 14 }, (_, index) => {
    const wave = index % 4;
    return {
      date: dayjs("2026-05-16").add(index, "day").format("MM-DD"),
      available: Math.round(available * (0.9 + wave * 0.025) - index * 85),
      inbound: Math.round(inbound * (0.72 + (index % 5) * 0.05)),
      riskSku: Math.max(riskSku + (index % 6) - 3, 0)
    };
  });
}

export function getWarehouseData(data: InventoryItem[]): WarehousePoint[] {
  const grouped = data.reduce<Record<string, WarehousePoint>>((acc, item) => {
    const current = acc[item.warehouse] ?? {
      warehouse: item.warehouse,
      available: 0,
      inbound: 0,
      reserved: 0
    };

    return {
      ...acc,
      [item.warehouse]: {
        ...current,
        available: current.available + item.available,
        inbound: current.inbound + item.inbound,
        reserved: current.reserved + item.reserved
      }
    };
  }, {});

  return Object.values(grouped);
}

export function getStatusData(data: InventoryItem[]): StatusPoint[] {
  return Object.entries(statusNames).map(([status, name]) => ({
    name,
    value: data.filter((item) => item.status === status).length,
    color: statusColors[status as InventoryStatus]
  }));
}

export function getPageItems<T>(data: T[], page: number, pageSize: number): T[] {
  return data.slice((page - 1) * pageSize, page * pageSize);
}
