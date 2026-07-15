"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import type { StatusPoint, TrendPoint, WarehousePoint } from "../lib/types";
import { formatNumber } from "../lib/analytics";

interface InventoryChartsProps {
  trendData: TrendPoint[];
  warehouseData: WarehousePoint[];
  statusData: StatusPoint[];
}

const chartPanelClass = "rounded-lg border border-ink/10 bg-porcelain p-4 shadow-ledger";

export function InventoryCharts({
  trendData,
  warehouseData,
  statusData
}: InventoryChartsProps) {
  return (
    <section className="grid items-start gap-4 xl:grid-cols-[1.3fr_1fr]">
      <div className={chartPanelClass}>
        <div className="mb-4 flex items-baseline justify-between gap-3">
          <div>
            <h2 className="font-display text-xl font-semibold text-ink">库存水位与风险趋势</h2>
            <p className="mt-1 text-sm text-ink/56">近 14 天可售、在途与风险 SKU 联动观察</p>
          </div>
          <span className="rounded-full bg-harbor/10 px-3 py-1 text-xs font-medium text-harbor">
            日级
          </span>
        </div>
        <div className="h-[320px]">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={trendData} margin={{ top: 8, right: 12, bottom: 4, left: 0 }}>
              <CartesianGrid stroke="#1F2A2414" vertical={false} />
              <XAxis dataKey="date" tickLine={false} axisLine={false} tick={{ fill: "#1F2A2490" }} />
              <YAxis
                yAxisId="stock"
                tickFormatter={formatNumber}
                tickLine={false}
                axisLine={false}
                width={64}
                tick={{ fill: "#1F2A2490" }}
              />
              <YAxis
                yAxisId="risk"
                orientation="right"
                tickLine={false}
                axisLine={false}
                width={36}
                tick={{ fill: "#1F2A2490" }}
              />
              <Tooltip
                formatter={(value: number, name: string) => [formatNumber(value), name]}
                contentStyle={{ borderRadius: 8, borderColor: "#1F2A241A" }}
              />
              <Legend />
              <Bar
                yAxisId="stock"
                name="可售库存"
                dataKey="available"
                fill="#145C6D"
                radius={[4, 4, 0, 0]}
                isAnimationActive={false}
              />
              <Bar
                yAxisId="stock"
                name="在途数量"
                dataKey="inbound"
                fill="#4F7D46"
                radius={[4, 4, 0, 0]}
                isAnimationActive={false}
              />
              <Line
                yAxisId="risk"
                type="monotone"
                name="风险 SKU"
                dataKey="riskSku"
                stroke="#B84A38"
                strokeWidth={3}
                dot={{ r: 3 }}
                isAnimationActive={false}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2 xl:grid-cols-1">
        <div className={chartPanelClass}>
          <h2 className="font-display text-xl font-semibold text-ink">仓库库存分布</h2>
          <div className="mt-4 h-[210px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={warehouseData} layout="vertical" margin={{ top: 0, right: 12, bottom: 0, left: 28 }}>
                <CartesianGrid stroke="#1F2A2414" horizontal={false} />
                <XAxis type="number" tickFormatter={formatNumber} hide />
                <YAxis
                  dataKey="warehouse"
                  type="category"
                  tickLine={false}
                  axisLine={false}
                  width={84}
                  tick={{ fill: "#1F2A2490", fontSize: 12 }}
                />
                <Tooltip formatter={(value: number) => formatNumber(value)} />
                <Bar
                  dataKey="available"
                  name="可售"
                  fill="#2E8B8F"
                  radius={[0, 4, 4, 0]}
                  isAnimationActive={false}
                />
                <Bar
                  dataKey="inbound"
                  name="在途"
                  fill="#D98B2B"
                  radius={[0, 4, 4, 0]}
                  isAnimationActive={false}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className={chartPanelClass}>
          <h2 className="font-display text-xl font-semibold text-ink">库存状态占比</h2>
          <div className="mt-4 h-[210px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={statusData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={54}
                  outerRadius={82}
                  paddingAngle={2}
                  isAnimationActive={false}
                >
                  {statusData.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => `${value} SKU`} />
                <Legend iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </section>
  );
}
