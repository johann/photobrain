import Link from "next/link";

const links = [
  { href: "/shoots", label: "Shoots" },
  { href: "/photos", label: "Photos" },
  { href: "/timelapses", label: "Timelapses" },
  { href: "/system", label: "System" }
];

export default function HomePage() {
  return (
    <main className="p-8 space-y-4">
      <h1 className="text-3xl font-bold">PhotoBrain</h1>
      <p className="text-gray-700">
        Lightweight Next.js shell that links to the major areas described in the specification.
      </p>
      <nav className="flex gap-4">
        {links.map((link) => (
          <Link key={link.href} href={link.href} className="text-blue-600 underline">
            {link.label}
          </Link>
        ))}
      </nav>
    </main>
  );
}
