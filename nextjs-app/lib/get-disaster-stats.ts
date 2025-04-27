import type { DisasterStats } from "./types"

// This is a mock implementation that simulates fetching statistics
// In a real application, this would call an API endpoint that retrieves actual data
export async function getDisasterStats(): Promise<DisasterStats> {
  // Simulate API call delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Mock data for demonstration purposes
  const stats: DisasterStats = {
    totalMessages: 26386,
    disasterRelated: 9924,
    nonDisasterRelated: 16462,

    categoriesDistribution: [
      { name: "Weather Related", count: 2358 },
      { name: "Flood", count: 1789 },
      { name: "Earthquake", count: 1543 },
      { name: "Fire", count: 1259 },
      { name: "Medical Help", count: 1198 },
      { name: "Infrastructure", count: 1072 },
      { name: "Water", count: 986 },
      { name: "Food", count: 952 },
      { name: "Shelter", count: 873 },
      { name: "Missing People", count: 586 },
      { name: "Death", count: 412 },
      { name: "Refugees", count: 389 },
      { name: "Clothing", count: 247 },
      { name: "Money", count: 186 },
    ],

    genreDistribution: [
      { name: "News", value: 12872 },
      { name: "Direct", value: 8976 },
      { name: "Social", value: 4538 },
    ],
  }

  return stats
}
