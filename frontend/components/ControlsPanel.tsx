"use client";

import { ChangeEvent } from "react";

export type Controls = {
  zWindow: number;
  setZWindow: (n: number) => void;
  useFedNet: boolean;
  setUseFedNet: (value: boolean) => void;
  stepHoldGli: boolean;
  setStepHoldGli: (value: boolean) => void;
  weights: { credit: number; g4: number };
  setWeights: (value: { credit: number; g4: number }) => void;
  rebaseDate?: string;
  setRebaseDate: (value: string) => void;
};

export function ControlsPanel({
  zWindow,
  setZWindow,
  useFedNet,
  setUseFedNet,
  stepHoldGli,
  setStepHoldGli,
  weights,
  setWeights,
  rebaseDate,
  setRebaseDate,
}: Controls) {
  const handleWeightChange = (event: ChangeEvent<HTMLInputElement>, key: "credit" | "g4") => {
    const value = parseFloat(event.target.value);
    const nextWeights = { ...weights, [key]: value };
    setWeights(nextWeights);
  };

  return (
    <section className="grid gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-4 md:grid-cols-2">
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">Z-Score Window (months)</label>
        <select
          value={zWindow}
          onChange={(event) => setZWindow(Number(event.target.value))}
          className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus:outline-none"
        >
          {[60, 120, 180].map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">Rebase Date</label>
        <input
          type="month"
          value={rebaseDate}
          onChange={(event) => setRebaseDate(event.target.value)}
          className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus:outline-none"
        />
      </div>
      <div className="space-y-2">
        <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
          <input type="checkbox" checked={useFedNet} onChange={(event) => setUseFedNet(event.target.checked)} />
          Use Fed Net Liquidity
        </label>
      </div>
      <div className="space-y-2">
        <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
          <input type="checkbox" checked={stepHoldGli} onChange={(event) => setStepHoldGli(event.target.checked)} />
          Step-Hold BIS GLI
        </label>
      </div>
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">Weight: GLI Credit</label>
        <input
          type="range"
          min={0}
          max={1}
          step={0.1}
          value={weights.credit}
          onChange={(event) => handleWeightChange(event, "credit")}
          className="w-full"
        />
        <p className="text-xs text-slate-400">{weights.credit.toFixed(2)}</p>
      </div>
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">Weight: G4 Central Banks</label>
        <input
          type="range"
          min={0}
          max={1}
          step={0.1}
          value={weights.g4}
          onChange={(event) => handleWeightChange(event, "g4")}
          className="w-full"
        />
        <p className="text-xs text-slate-400">{weights.g4.toFixed(2)}</p>
      </div>
    </section>
  );
}
