"use client";
import { useState } from "react";
import { api, setToken } from "@/lib/api";

export default function Setup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("password");
  const [topic, setTopic] = useState("Learn React");
  const [level, setLevel] = useState("Beginner");
  const [days, setDays] = useState(30);

  const registerAndCreate = async () => {
    const { data: tok } = await api.post("/auth/register", { email, password });
    setToken(tok.access_token);
    const { data: goal } = await api.post("/goals/", { topic, level, timeline_days: days });
    window.location.href = `/roadmap/${goal.id}`;
  };

  return (
    <div className="max-w-xl mx-auto p-6 space-y-4">
      <h2 className="text-2xl font-bold">Goal Setup Wizard</h2>
      <input className="w-full border p-2 rounded" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="w-full border p-2 rounded" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
      <input className="w-full border p-2 rounded" placeholder="Topic" value={topic} onChange={e=>setTopic(e.target.value)} />
      <div className="grid grid-cols-2 gap-3">
        <input className="border p-2 rounded" placeholder="Level" value={level} onChange={e=>setLevel(e.target.value)} />
        <input className="border p-2 rounded" type="number" value={days} onChange={e=>setDays(parseInt(e.target.value))} />
      </div>
      <button onClick={registerAndCreate} className="px-4 py-2 bg-black text-white rounded">Create Roadmap</button>
    </div>
  );
}
