import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'BrainTrail - AI Knowledge Hub',
  description: 'Personalized learning roadmaps powered by AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
