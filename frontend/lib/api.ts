export type IndexPoint = {
  ts: string;
  value: number;
};

export type IndexSeries = {
  name: string;
  points: IndexPoint[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8080/api/v1";

export async function fetchIndex(name: string): Promise<IndexSeries> {
  try {
    const response = await fetch(`${API_BASE}/indices/${name}`, { next: { revalidate: 3600 } });
    if (!response.ok) {
      throw new Error(`Failed to fetch index ${name}`);
    }
    const payload = await response.json();
    return { name: payload.name, points: payload.points };
  } catch (error) {
    const today = new Date();
    const fallback = Array.from({ length: 24 }).map((_, idx) => {
      const date = new Date(today);
      date.setMonth(today.getMonth() - (23 - idx));
      return {
        ts: date.toISOString(),
        value: 100 + Math.sin(idx / 3) * 5,
      };
    });
    return { name, points: fallback };
  }
}

export async function fetchLatestValues(names: string[]): Promise<Record<string, number>> {
  const entries = await Promise.all(
    names.map(async (name) => {
      try {
        const data = await fetchIndex(name);
        const latest = data.points[data.points.length - 1];
        return [name, latest.value] as const;
      } catch (error) {
        return [name, NaN] as const;
      }
    })
  );
  return Object.fromEntries(entries);
}
