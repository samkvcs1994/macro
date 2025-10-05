"use client";

import { ArrowLongUpIcon, ArrowLongDownIcon } from "@heroicons/react/24/outline";
import clsx from "clsx";

export type IndexCardProps = {
  name: string;
  value: number;
  change1m: number;
  change3m: number;
};

const format = (value: number) => value.toFixed(2);

export function IndexCard({ name, value, change1m, change3m }: IndexCardProps) {
  const trendIcon = (delta: number) => {
    if (delta >= 0) {
      return <ArrowLongUpIcon className="w-5 h-5 text-emerald-400" aria-hidden />;
    }
    return <ArrowLongDownIcon className="w-5 h-5 text-rose-400" aria-hidden />;
  };

  const changeBadge = (delta: number) => (
    <span
      className={clsx(
        "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium",
        delta >= 0 ? "bg-emerald-500/10 text-emerald-300" : "bg-rose-500/10 text-rose-300"
      )}
    >
      {trendIcon(delta)}
      {format(delta)} σ
    </span>
  );

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/50">
      <div className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100">{name}</h2>
        <span className="text-3xl font-bold text-slate-50">{format(value)}</span>
      </div>
      <div className="mt-4 flex items-center gap-4">
        <div className="flex flex-col gap-2">
          <span className="text-xs uppercase tracking-wide text-slate-400">1m</span>
          {changeBadge(change1m)}
        </div>
        <div className="flex flex-col gap-2">
          <span className="text-xs uppercase tracking-wide text-slate-400">3m</span>
          {changeBadge(change3m)}
        </div>
      </div>
    </div>
  );
}
