import "../styles/globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "Global Liquidity Indices",
  description: "Dashboard for tracking global liquidity conditions",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen">
        <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
          <header className="flex items-center justify-between">
            <h1 className="text-2xl font-semibold">Global Liquidity Indices</h1>
            <span className="text-sm text-slate-400">Auto-refreshing macro liquidity monitor</span>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
