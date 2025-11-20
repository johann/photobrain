import { shoots } from "@/lib/mockData";

export default function ShootsPage() {
  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-semibold">Shoots</h1>
      <ul className="space-y-2">
        {shoots.map((shoot) => (
          <li key={shoot.id} className="border rounded p-4">
            <div className="font-bold">{shoot.name}</div>
            <div className="text-sm text-gray-600">{shoot.location}</div>
            <div className="text-xs text-gray-500">Captured: {shoot.capturedAt}</div>
            <div className="text-xs text-gray-500">Tags: {shoot.tags.join(", ")}</div>
          </li>
        ))}
      </ul>
    </main>
  );
}
