"use client";

import { useEffect, useState } from "react";
import { ControlsPanel } from "./ControlsPanel";
import { TimeSeriesChart } from "./TimeSeriesChart";
import type { ChartPoint } from "./TimeSeriesChart";

export type ChartViewProps = {
  initialData: ChartPoint[];
};

export function ChartView({ initialData }: ChartViewProps) {
  const [zWindow, setZWindow] = useState(120);
  const [useFedNet, setUseFedNet] = useState(true);
  const [stepHoldGli, setStepHoldGli] = useState(true);
  const [weights, setWeights] = useState({ credit: 0.5, g4: 0.5 });
  const [rebaseDate, setRebaseDate] = useState<string>("2015-01");
  const [data, setData] = useState(initialData);

  useEffect(() => {
    setData(initialData);
  }, [initialData]);

  return (
    <div className="space-y-6">
      <ControlsPanel
        zWindow={zWindow}
        setZWindow={setZWindow}
        useFedNet={useFedNet}
        setUseFedNet={setUseFedNet}
        stepHoldGli={stepHoldGli}
        setStepHoldGli={setStepHoldGli}
        weights={weights}
        setWeights={setWeights}
        rebaseDate={rebaseDate}
        setRebaseDate={setRebaseDate}
      />
      <TimeSeriesChart data={data} label="GLI Composite" />
      <p className="text-xs text-slate-400">
        Adjust the controls to explore different configurations. In the production build these controls will trigger API calls to
        refresh data with the requested parameters.
      </p>
    </div>
  );
}
