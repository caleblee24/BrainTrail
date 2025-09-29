"use client";
import { useState } from "react";

export default function Learn({ params }: { params: { moduleId: string } }) {
  const [q, setQ] = useState("");
  const [hits, setHits] = useState<any[]>([]);
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE || "http://localhost/api"}/tutor/ask/contexts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal_id: 0, question: q })
    });
    const data = await res.json();
    setHits(data.contexts || []);
  };

  const askStream = async () => {
    setAnswer("");
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE || "http://localhost/api"}/tutor/ask/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal_id: 0, question: q })
    });
    const reader = res.body!.getReader();
    const decoder = new TextDecoder();
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      chunk.split("\n\n").forEach(line => {
        if (line.startsWith("data: ")) setAnswer(prev => prev + line.slice(6));
      });
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <h2 className="text-2xl font-bold">Module {params.moduleId}</h2>
      <div className="flex gap-2">
        <input className="flex-1 border p-2 rounded" placeholder="Ask the AI tutor..." value={q} onChange={e=>setQ(e.target.value)} />
        <button onClick={ask} className="px-4 py-2 bg-black text-white rounded">Search</button>
        <button onClick={askStream} className="px-4 py-2 bg-gray-900 text-white rounded">Answer</button>
      </div>
      <div className="space-y-2">
        {hits.map((h,i) => (
          <div key={i} className="border p-3 rounded">
            <div className="font-semibold">{h.title}</div>
            <a className="text-sm underline" href={h.url} target="_blank">Open</a>
            <p className="text-sm mt-2 opacity-80">{(h.content_text||"").slice(0,300)}...</p>
          </div>
        ))}
      </div>
      {answer && (
        <div className="border p-3 rounded whitespace-pre-wrap"><strong>Answer:</strong> {answer}</div>
      )}
    </div>
  );
}
