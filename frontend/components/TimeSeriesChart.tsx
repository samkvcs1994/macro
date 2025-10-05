"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export type ChartPoint = {
  ts: string;
  value: number;
};

export type TimeSeriesChartProps = {
  data: ChartPoint[];
  label: string;
};

export function TimeSeriesChart({ data, label }: TimeSeriesChartProps) {
  return (
    <div className="h-80 w-full rounded-xl border border-slate-800 bg-slate-900/60 p-4">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="colorIndex" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#22d3ee" stopOpacity={0.1} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="ts"
            stroke="#94a3b8"
            tickFormatter={(val) => new Date(val).toLocaleDateString(undefined, { month: "short", year: "2-digit" })}
          />
          <YAxis stroke="#94a3b8" width={60} domain={["auto", "auto"]} />
          <Tooltip
            contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b" }}
            labelFormatter={(val) => new Date(val).toLocaleDateString()}
          />
          <Area type="monotone" dataKey="value" stroke="#22d3ee" fillOpacity={1} fill="url(#colorIndex)" name={label} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
