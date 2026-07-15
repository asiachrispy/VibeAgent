export type Marketplace =
  | "Amazon US"
  | "Amazon UK"
  | "Amazon DE"
  | "Walmart"
  | "Shopify"
  | "TikTok Shop";

export type Warehouse =
  | "美西自营仓"
  | "美东 3PL"
  | "FBA US"
  | "FBA EU"
  | "英国海外仓"
  | "华南集货仓";

export type InventoryStatus =
  | "healthy"
  | "low"
  | "out"
  | "overstock"
  | "inbound"
  | "stranded";

export type InventoryRisk = "低" | "中" | "高";

export interface InventoryItem {
  id: string;
  sku: string;
  asin: string;
  productName: string;
  category: string;
  marketplace: Marketplace;
  warehouse: Warehouse;
  status: InventoryStatus;
  available: number;
  reserved: number;
  inbound: number;
  transferPending: number;
  dailySales: number;
  sevenDaySales: number;
  thirtyDaySales: number;
  sellThroughRate: number;
  daysOfCover: number;
  reorderPoint: number;
  recommendedReplenishment: number;
  unitCost: number;
  inventoryValue: number;
  ageBucket: "0-30天" | "31-60天" | "61-90天" | "90天以上";
  supplier: string;
  owner: string;
  lastSyncAt: string;
  nextInboundEta: string;
  risk: InventoryRisk;
}

export interface InventoryFilters {
  marketplace: Marketplace | "全部平台";
  warehouse: Warehouse | "全部仓库";
  status: InventoryStatus | "全部状态";
  category: string;
  keyword: string;
}

export interface InventoryMetric {
  label: string;
  value: string;
  helper: string;
  trend: string;
  tone: "harbor" | "moss" | "amber" | "ember" | "plum";
}

export interface TrendPoint {
  date: string;
  available: number;
  inbound: number;
  riskSku: number;
}

export interface WarehousePoint {
  warehouse: Warehouse;
  available: number;
  inbound: number;
  reserved: number;
}

export interface StatusPoint {
  name: string;
  value: number;
  color: string;
}

export interface SortConfig {
  key: keyof InventoryItem;
  direction: "asc" | "desc";
}
