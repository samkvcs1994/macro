import { ChartView } from "@/components/ChartView";
import { fetchIndex } from "@/lib/api";

export default async function ChartPage() {
  const composite = await fetchIndex("GLI_Composite");
  const chartData = composite.points.map((point) => ({ ts: point.ts, value: point.value }));

  return (
    <div className="space-y-8">
      <header className="space-y-2">
        <h2 className="text-xl font-semibold text-slate-100">Interactive Chart</h2>
        <p className="text-sm text-slate-400">Explore index behaviour with configurable parameters.</p>
      </header>
      <ChartView initialData={chartData} />
    </div>
  );
}
