"use client";

import { AlertTriangle, ArrowRightLeft, PackageCheck, Truck, X } from "lucide-react";
import clsx from "clsx";
import type { ReactNode } from "react";
import { formatCurrency, formatNumber } from "../lib/analytics";
import { statusLabels } from "../lib/mock-data";
import type { InventoryItem } from "../lib/types";

interface DetailPanelProps {
  item: InventoryItem | null;
  onClose: () => void;
}

interface ActionRowProps {
  icon: ReactNode;
  label: string;
  value: string;
  tone: ActionTone;
}

interface InfoRowProps {
  label: string;
  value: string;
}

type ActionTone = "normal" | "medium" | "high";

const insightClass = "rounded-md border border-ink/10 bg-paper/70 p-3";

function getRiskTone(risk: InventoryItem["risk"]): ActionTone {
  if (risk === "高") return "high";
  if (risk === "中") return "medium";
  return "normal";
}

export function DetailPanel({ item, onClose }: DetailPanelProps): JSX.Element | null {
  if (!item) return null;

  const replenishmentText =
    item.recommendedReplenishment > 0
      ? `建议补货 ${formatNumber(item.recommendedReplenishment)} 件`
      : "当前无需补货";

  return (
    <aside
      className="fixed inset-y-0 right-0 z-50 w-full max-w-[460px] border-l border-ink/12 bg-porcelain shadow-2xl"
      aria-label="库存详情侧栏"
    >
      <div className="flex h-full flex-col">
        <header className="border-b border-ink/10 p-5">
          <div className="flex items-start gap-3">
            <div className="grid h-11 w-11 shrink-0 place-items-center rounded-md bg-harbor text-porcelain">
              <PackageCheck className="h-5 w-5" aria-hidden="true" />
            </div>
            <div className="min-w-0">
              <p className="font-mono text-xs uppercase tracking-[0.14em] text-ink/50">{item.sku}</p>
              <h2 className="mt-1 truncate font-display text-2xl font-semibold text-ink">
                {item.productName}
              </h2>
            </div>
            <button
              type="button"
              onClick={onClose}
              className="ml-auto grid h-9 w-9 shrink-0 place-items-center rounded-md border border-ink/10 text-ink/60 transition hover:text-ember"
              title="关闭详情"
            >
              <X className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
          <div className="mt-4 flex flex-wrap gap-2 text-xs">
            <span className="rounded-full bg-harbor/10 px-2.5 py-1 text-harbor">{item.marketplace}</span>
            <span className="rounded-full bg-moss/10 px-2.5 py-1 text-moss">{item.warehouse}</span>
            <span className="rounded-full bg-amber/12 px-2.5 py-1 text-amber">
              {statusLabels[item.status]}
            </span>
          </div>
        </header>

        <div className="scrollbar-thin flex-1 overflow-y-auto p-5">
          <section className="grid grid-cols-2 gap-3">
            <div className={insightClass}>
              <p className="text-xs text-ink/52">可售库存</p>
              <strong className="mt-2 block text-2xl text-ink">{formatNumber(item.available)}</strong>
            </div>
            <div className={insightClass}>
              <p className="text-xs text-ink/52">库存金额</p>
              <strong className="mt-2 block text-2xl text-ink">{formatCurrency(item.inventoryValue)}</strong>
            </div>
            <div className={insightClass}>
              <p className="text-xs text-ink/52">日均销量</p>
              <strong className="mt-2 block text-2xl text-ink">{formatNumber(item.dailySales)}</strong>
            </div>
            <div className={insightClass}>
              <p className="text-xs text-ink/52">覆盖天数</p>
              <strong className="mt-2 block text-2xl text-ink">{item.daysOfCover} 天</strong>
            </div>
          </section>

          <section className="mt-5 rounded-lg border border-ink/10 bg-paper/80 p-4">
            <h3 className="text-sm font-semibold text-ink">补货与调拨建议</h3>
            <div className="mt-4 space-y-3">
              <ActionRow
                icon={<Truck className="h-4 w-4" />}
                label="采购补货"
                value={replenishmentText}
                tone={item.recommendedReplenishment > 0 ? "high" : "normal"}
              />
              <ActionRow
                icon={<ArrowRightLeft className="h-4 w-4" />}
                label="仓间调拨"
                value={`待调拨 ${formatNumber(item.transferPending)} 件`}
                tone={item.transferPending > 80 ? "medium" : "normal"}
              />
              <ActionRow
                icon={<AlertTriangle className="h-4 w-4" />}
                label="风险等级"
                value={`${item.risk}风险，安全库存点 ${formatNumber(item.reorderPoint)}`}
                tone={getRiskTone(item.risk)}
              />
            </div>
          </section>

          <section className="mt-5 rounded-lg border border-ink/10 bg-porcelain p-4">
            <h3 className="text-sm font-semibold text-ink">商品档案</h3>
            <dl className="mt-4 grid gap-3 text-sm">
              <InfoRow label="ASIN" value={item.asin} />
              <InfoRow label="品类" value={item.category} />
              <InfoRow label="供应商" value={item.supplier} />
              <InfoRow label="负责人" value={item.owner} />
              <InfoRow label="库龄" value={item.ageBucket} />
              <InfoRow label="预计到仓" value={item.nextInboundEta} />
              <InfoRow label="最近同步" value={item.lastSyncAt} />
            </dl>
          </section>
        </div>
      </div>
    </aside>
  );
}

function ActionRow({
  icon,
  label,
  value,
  tone
}: ActionRowProps): JSX.Element {
  return (
    <div className="flex items-center gap-3 rounded-md bg-porcelain p-3">
      <span
        className={clsx(
          "grid h-8 w-8 place-items-center rounded-md",
          tone === "high" && "bg-ember/12 text-ember",
          tone === "medium" && "bg-amber/12 text-amber",
          tone === "normal" && "bg-harbor/10 text-harbor"
        )}
      >
        {icon}
      </span>
      <div>
        <p className="text-xs text-ink/50">{label}</p>
        <p className="text-sm font-medium text-ink">{value}</p>
      </div>
    </div>
  );
}

function InfoRow({ label, value }: InfoRowProps): JSX.Element {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-ink/8 pb-2 last:border-0">
      <dt className="text-ink/52">{label}</dt>
      <dd className="text-right font-medium text-ink">{value}</dd>
    </div>
  );
}
