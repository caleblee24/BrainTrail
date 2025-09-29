"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function Roadmap({ params }: { params: { id: string } }) {
  const [modules, setModules] = useState<any[]>([]);
  useEffect(() => {
    api.get(`/goals/${params.id}`).then(r => setModules(r.data.modules || []));
  }, [params.id]);
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Your Roadmap</h2>
      <ul className="space-y-2">
        {modules.map(m => (
          <li key={m.id} className="p-3 border rounded flex items-center justify-between">
            <div>
              <div className="font-semibold">{m.title}</div>
              <div className="text-sm opacity-70">~{m.est_minutes} min</div>
            </div>
            <a className="px-3 py-1 bg-black text-white rounded" href={`/learn/${m.id}`}>Open</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
