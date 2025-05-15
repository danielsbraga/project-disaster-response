import { type NextRequest, NextResponse } from "next/server"
import type { DisasterStats } from "@/lib/types"

export async function GET(request: NextRequest) {
  try {
    // Mock stats for now - in a real app, this would come from a database
    const stats: DisasterStats = {
      totalMessages: 1000,
      disasterRelated: 750,
      nonDisasterRelated: 250,
      categoriesDistribution: [
        { name: "aid_related", count: 450 },
        { name: "weather_related", count: 300 },
        { name: "direct_report", count: 250 },
        { name: "request", count: 200 },
        { name: "other_aid", count: 150 },
        { name: "food", count: 100 },
        { name: "earthquake", count: 80 },
        { name: "storm", count: 70 },
        { name: "shelter", count: 60 },
        { name: "floods", count: 50 }
      ],
      genreDistribution: [
        { name: "direct", value: 600 },
        { name: "news", value: 250 },
        { name: "social", value: 150 }
      ]
    }
    
    return NextResponse.json(stats)
  } catch (error) {
    console.error("Error fetching stats:", error)
    return NextResponse.json({ error: "An error occurred while fetching statistics" }, { status: 500 })
  }
}
