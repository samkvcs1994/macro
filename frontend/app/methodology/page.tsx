const sections = [
  {
    title: "Overview",
    content:
      "The Global Liquidity Indices track the evolution of balance sheet liquidity across major central banks and the availability of cross-border credit.",
  },
  {
    title: "Central Bank Liquidity",
    content:
      "GLI_G4_CB aggregates the balance sheets of the Federal Reserve, European Central Bank, Bank of Japan, and Bank of England. Optional toggles allow for Fed netting (subtracting ON RRP and the Treasury General Account).",
  },
  {
    title: "Credit Availability",
    content:
      "GLI_Credit draws on BIS data covering foreign-currency credit extended to non-resident non-banks across USD, EUR, and JPY denominations.",
  },
  {
    title: "Composite Methodology",
    content:
      "Each component is standardised using a configurable rolling z-score. The composite index linearly combines the components with transparent weights and rescales the output to a base of 100.",
  },
];

export default function MethodologyPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-slate-100">Methodology</h2>
      <div className="space-y-4 text-sm text-slate-300">
        {sections.map((section) => (
          <section key={section.title} className="space-y-2">
            <h3 className="text-base font-semibold text-slate-100">{section.title}</h3>
            <p>{section.content}</p>
          </section>
        ))}
      </div>
    </div>
  );
}
