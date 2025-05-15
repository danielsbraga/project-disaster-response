import type { DisasterStats } from "./types"

// This is a mock implementation that simulates fetching statistics
// In a real application, this would call an API endpoint that retrieves actual data
export async function getDisasterStats(): Promise<DisasterStats> {
  const res = await fetch("/api/stats")
  if (!res.ok) throw new Error("Failed to fetch stats")
  return res.json()
}
