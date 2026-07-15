import dayjs from "dayjs";
import type {
  InventoryItem,
  InventoryStatus,
  Marketplace,
  Warehouse
} from "./types";

export const marketplaces: Marketplace[] = [
  "Amazon US",
  "Amazon UK",
  "Amazon DE",
  "Walmart",
  "Shopify",
  "TikTok Shop"
];

export const warehouses: Warehouse[] = [
  "美西自营仓",
  "美东 3PL",
  "FBA US",
  "FBA EU",
  "英国海外仓",
  "华南集货仓"
];

export const statuses: InventoryStatus[] = [
  "healthy",
  "low",
  "out",
  "overstock",
  "inbound",
  "stranded"
];

export const statusLabels: Record<InventoryStatus, string> = {
  healthy: "健康",
  low: "低库存",
  out: "缺货",
  overstock: "滞销积压",
  inbound: "在途补货",
  stranded: "不可售/搁置"
};

export const categories = [
  "家居收纳",
  "宠物用品",
  "户外运动",
  "厨房小电",
  "消费电子",
  "汽摩配件",
  "美妆工具"
];

const productSeeds = [
  "折叠收纳箱",
  "宠物饮水机滤芯",
  "露营灯串",
  "便携咖啡磨豆机",
  "磁吸充电支架",
  "车载应急启动电源",
  "LED 化妆镜",
  "真空保鲜盒",
  "猫砂垫",
  "防水运动腰包",
  "桌面理线器",
  "硅胶烘焙垫",
  "蓝牙寻物器",
  "汽车后备箱整理箱"
];

const suppliers = ["宁波合创", "深圳野火", "义乌千帆", "东莞星航", "厦门沐森"];
const owners = ["Mia", "Leo", "Ava", "Noah", "Ivy"];

function pick<T>(items: T[], index: number): T {
  return items[index % items.length];
}

function bounded(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function getStatus(
  available: number,
  inbound: number,
  daysOfCover: number,
  index: number
): InventoryStatus {
  if (available === 0) return "out";
  if (index % 17 === 0) return "stranded";
  if (daysOfCover > 115) return "overstock";
  if (daysOfCover < 16) return "low";
  if (inbound > available * 0.8) return "inbound";
  return "healthy";
}

function getAgeBucket(index: number, daysOfCover: number): InventoryItem["ageBucket"] {
  if (daysOfCover > 120 || index % 19 === 0) return "90天以上";
  if (daysOfCover > 75) return "61-90天";
  if (daysOfCover > 38) return "31-60天";
  return "0-30天";
}

function getRisk(status: InventoryStatus): InventoryItem["risk"] {
  if (status === "out" || status === "low") return "高";
  if (status === "inbound") return "中";
  return "低";
}

function createInventoryItem(index: number): InventoryItem {
  const marketplace = pick(marketplaces, index);
  const warehouse = pick(warehouses, index * 2 + 1);
  const category = pick(categories, index * 3);
  const productName = `${pick(productSeeds, index)} ${index % 4 === 0 ? "升级款" : "标准款"}`;
  const dailySales = bounded(Math.round(((index * 7) % 43) + 2 + (index % 5)), 1, 58);
  const availableBase = ((index * 137) % 980) + (index % 9) * 34;
  const available = index % 29 === 0 ? 0 : availableBase;
  const inbound = index % 6 === 0 ? ((index * 61) % 620) + 80 : (index * 23) % 220;
  const reserved = Math.round(available * (((index % 7) + 3) / 100));
  const transferPending = index % 8 === 0 ? ((index * 11) % 160) + 12 : (index * 5) % 55;
  const thirtyDaySales = dailySales * 30 + ((index * 31) % 180);
  const sevenDaySales = dailySales * 7 + ((index * 13) % 45);
  const daysOfCover = available === 0 ? 0 : Math.round(available / dailySales);
  const reorderPoint = Math.round(dailySales * (index % 3 === 0 ? 28 : 21));
  const recommendedReplenishment = Math.max(reorderPoint + dailySales * 35 - available - inbound, 0);
  const unitCost = Number((5.6 + ((index * 37) % 190) / 10).toFixed(2));
  const status = getStatus(available, inbound, daysOfCover, index);

  return {
    id: `INV-${String(index + 1).padStart(4, "0")}`,
    sku: `VA-${category.slice(0, 2).toUpperCase()}-${String(1000 + index)}`,
    asin: `B0${String(8_400_000 + index * 137).slice(0, 8)}`,
    productName,
    category,
    marketplace,
    warehouse,
    status,
    available,
    reserved,
    inbound,
    transferPending,
    dailySales,
    sevenDaySales,
    thirtyDaySales,
    sellThroughRate: Number(bounded(thirtyDaySales / (available + thirtyDaySales + 1), 0.03, 0.96).toFixed(2)),
    daysOfCover,
    reorderPoint,
    recommendedReplenishment,
    unitCost,
    inventoryValue: Number((available * unitCost).toFixed(2)),
    ageBucket: getAgeBucket(index, daysOfCover),
    supplier: pick(suppliers, index * 5 + 2),
    owner: pick(owners, index * 7 + 1),
    lastSyncAt: dayjs("2026-05-29T09:00:00+08:00")
      .subtract(index % 11, "minute")
      .format("YYYY-MM-DD HH:mm"),
    nextInboundEta: dayjs("2026-05-29")
      .add((index % 18) + 2, "day")
      .format("YYYY-MM-DD"),
    risk: getRisk(status)
  };
}

export const inventoryData = Array.from({ length: 126 }, (_, index) =>
  createInventoryItem(index)
);
