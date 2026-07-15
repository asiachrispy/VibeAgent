# 跨境电商 ERP 库存中心原型

这是一个可运行的数据报表原型，用于展示跨境电商卖家 ERP 中的库存中心管理体验。

## 技术栈

- Next.js 14 App Router
- TypeScript
- Tailwind CSS
- Recharts
- lucide-react
- dayjs
- papaparse
- framer-motion

## 功能范围

- 多平台、多仓库、多库存状态筛选
- SKU / ASIN / 商品 / 供应商关键词搜索
- 可售库存、低库存风险、在途数量、库存金额指标卡
- 库存水位与风险趋势图
- 仓库库存分布图
- 库存状态占比图
- SKU 明细表格排序、分页、CSV 导出
- SKU 详情侧栏，展示补货、调拨、风险和商品档案

## 运行

```bash
cd inventory-center-prototype
npm install
npm run dev
```

访问：

```text
http://localhost:3000/inventory-center
```

## 核心文件

- `app/inventory-center/page.tsx`：库存中心页面入口
- `app/inventory-center/components/inventory-center-dashboard.tsx`：页面状态与布局
- `app/inventory-center/components/filter-bar.tsx`：筛选控制台
- `app/inventory-center/components/charts.tsx`：库存图表
- `app/inventory-center/components/inventory-table.tsx`：明细表格与导出
- `app/inventory-center/components/detail-panel.tsx`：SKU 详情侧栏
- `app/inventory-center/lib/mock-data.ts`：模拟数据
- `app/inventory-center/lib/analytics.ts`：筛选、排序、指标和图表数据计算
- `app/inventory-center/lib/types.ts`：类型定义

## 后续接 API 建议

- `GET /api/inventory/items`：库存明细，参数包含 `marketplace`、`warehouse`、`status`、`category`、`keyword`、`page`、`pageSize`
- `GET /api/inventory/summary`：库存指标与图表聚合数据
- `POST /api/inventory/export`：按当前筛选条件生成导出文件
- `GET /api/inventory/items/:sku`：SKU 详情、补货建议和调拨建议

当前原型不依赖后端，所有数据来自本地确定性模拟数据。
