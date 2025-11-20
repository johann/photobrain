export default function SystemPage() {
  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-semibold">System</h1>
      <p className="text-gray-700">
        This placeholder dashboard mirrors the health, disk usage, and job queue endpoints described for the backend API.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border rounded p-4">
          <div className="font-semibold">Health</div>
          <div>Status: ok</div>
        </div>
        <div className="border rounded p-4">
          <div className="font-semibold">Disk Usage</div>
          <div>Root: /Volumes/PhotoVault</div>
          <div>Used: 128 GB</div>
          <div>Free: 872 GB</div>
        </div>
        <div className="border rounded p-4">
          <div className="font-semibold">Jobs</div>
          <ul className="list-disc list-inside text-sm">
            <li>job-1 — completed</li>
            <li>job-2 — running</li>
          </ul>
        </div>
      </div>
    </main>
  );
}
