import { timelapses } from "@/lib/mockData";

export default function TimelapsesPage() {
  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-semibold">Timelapses</h1>
      <ul className="space-y-2">
        {timelapses.map((tl) => (
          <li key={tl.id} className="border rounded p-4">
            <div className="font-bold">{tl.title}</div>
            <div className="text-sm text-gray-600">Frames: {tl.frameCount}</div>
          </li>
        ))}
      </ul>
    </main>
  );
}
