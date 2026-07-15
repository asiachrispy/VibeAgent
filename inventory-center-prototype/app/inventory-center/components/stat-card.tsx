"use client";

import clsx from "clsx";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";
import { motion } from "framer-motion";
import type { InventoryMetric } from "../lib/types";

const toneClass: Record<InventoryMetric["tone"], string> = {
  harbor: "border-harbor/25 bg-harbor/8 text-harbor",
  moss: "border-moss/25 bg-moss/10 text-moss",
  amber: "border-amber/30 bg-amber/12 text-amber",
  ember: "border-ember/25 bg-ember/10 text-ember",
  plum: "border-plum/25 bg-plum/10 text-plum"
};

interface StatCardProps {
  metric: InventoryMetric;
  index: number;
}

export function StatCard({ metric, index }: StatCardProps) {
  const isPositive = metric.trend.startsWith("+") || metric.trend.includes("健康");
  const TrendIcon = isPositive ? ArrowUpRight : ArrowDownRight;

  return (
    <motion.article
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.06, duration: 0.28 }}
      className="min-h-[148px] rounded-lg border border-ink/10 bg-porcelain p-4 shadow-ledger"
    >
      <div className="flex flex-col items-start justify-between gap-2 sm:flex-row sm:gap-3">
        <p className="text-sm font-medium text-ink/64">{metric.label}</p>
        <span
          className={clsx(
            "shrink-0 rounded-full border px-2 py-1 text-xs",
            toneClass[metric.tone]
          )}
        >
          <TrendIcon className="mr-1 inline h-3.5 w-3.5" aria-hidden="true" />
          {metric.trend}
        </span>
      </div>
      <strong className="mt-4 block font-display text-3xl font-semibold tracking-normal text-ink">
        {metric.value}
      </strong>
      <p className="mt-3 text-sm leading-5 text-ink/58">{metric.helper}</p>
    </motion.article>
  );
}
