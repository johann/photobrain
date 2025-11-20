import { photos } from "@/lib/mockData";

export default function PhotosPage() {
  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-semibold">Photos</h1>
      <table className="min-w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 text-left">Filename</th>
            <th className="p-2 text-left">Shoot</th>
            <th className="p-2 text-left">Rating</th>
          </tr>
        </thead>
        <tbody>
          {photos.map((photo) => (
            <tr key={photo.id} className="border-t">
              <td className="p-2">{photo.filename}</td>
              <td className="p-2">{photo.shootId}</td>
              <td className="p-2">{photo.rating ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
