import Link from "next/link";

const columns = ["Vintage", "Created", "Notes"];

export default function VintagesPage() {
  const rows = [
    { id: "sample", created: "2024-02-01", notes: "Initial dataset" },
    { id: "sample-2", created: "2024-03-01", notes: "Quarterly BIS update" },
  ];

  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <h2 className="text-xl font-semibold text-slate-100">Vintage History</h2>
        <p className="text-sm text-slate-400">Track revisions to the composite indices over time.</p>
      </header>
      <div className="overflow-hidden rounded-xl border border-slate-800">
        <table className="min-w-full divide-y divide-slate-800 text-sm">
          <thead className="bg-slate-900/80 text-left text-xs uppercase tracking-wider text-slate-400">
            <tr>
              {columns.map((column) => (
                <th key={column} className="px-4 py-3">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 bg-slate-900/40">
            {rows.map((row) => (
              <tr key={row.id} className="hover:bg-slate-800/40">
                <td className="px-4 py-3 font-medium text-slate-200">
                  <Link href={`?selected=${row.id}`} className="underline decoration-slate-600 hover:text-cyan-300">
                    {row.id}
                  </Link>
                </td>
                <td className="px-4 py-3 text-slate-300">{row.created}</td>
                <td className="px-4 py-3 text-slate-400">{row.notes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-slate-400">
        The production build will populate this table from the /api/v1/vintages endpoint and allow diffs between vintages.
      </p>
    </div>
  );
}
