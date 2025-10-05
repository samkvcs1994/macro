import { IndexCard } from "@/components/IndexCard";
import { TimeSeriesChart } from "@/components/TimeSeriesChart";
import { fetchIndex, fetchLatestValues } from "@/lib/api";

const INDICES = ["GLI_Composite", "GLI_G4_CB", "GLI_Credit"];

export default async function OverviewPage() {
  const [composite, latest] = await Promise.all([fetchIndex("GLI_Composite"), fetchLatestValues(INDICES)]);
  const chartData = composite.points.slice(-12).map((point) => ({
    ts: point.ts,
    value: point.value,
  }));

  return (
    <div className="space-y-8">
      <section className="grid gap-4 md:grid-cols-3">
        {INDICES.map((name) => (
          <IndexCard key={name} name={name} value={latest[name] ?? 0} change1m={0.0} change3m={0.0} />
        ))}
      </section>
      <section>
        <h2 className="text-lg font-semibold text-slate-100">Composite Liquidity Index</h2>
        <TimeSeriesChart data={chartData} label="GLI Composite" />
      </section>
    </div>
  );
}
