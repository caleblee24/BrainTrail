export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <div className="max-w-2xl text-center space-y-4">
        <h1 className="text-4xl font-bold">BrainTrail — AI Knowledge Hub</h1>
        <p className="opacity-80">Personalized roadmaps, curated resources, adaptive quizzes.</p>
        <a href="/setup" className="px-4 py-2 rounded-xl bg-black text-white">Get Started</a>
      </div>
    </main>
  );
}
