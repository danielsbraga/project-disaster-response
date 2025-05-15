import type { DisasterStats } from "./types"

// This is a mock implementation that simulates fetching statistics
// In a real application, this would call an API endpoint that retrieves actual data
export async function getDisasterStats(): Promise<DisasterStats> {
  try {
    const res = await fetch("http://localhost:5000/api/stats")
    if (!res.ok) {
      throw new Error("Failed to fetch stats")
    }
    const data = await res.json()
    
    // Transform the data to match our expected format
    return {
      totalMessages: data.totalMessages,
      disasterRelated: data.disasterRelated,
      nonDisasterRelated: data.nonDisasterRelated,
      categoriesDistribution: data.categoriesDistribution.map((item: any) => ({
        name: item.name.replace(/_/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase()),
        count: item.count
      })),
      genreDistribution: data.genreDistribution
    }
  } catch (error) {
    console.error("Error fetching disaster stats:", error)
    throw error
  }
}