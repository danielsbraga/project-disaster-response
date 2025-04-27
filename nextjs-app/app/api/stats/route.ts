import { type NextRequest, NextResponse } from "next/server"
import { getDisasterStats } from "@/lib/get-disaster-stats"

export async function GET(request: NextRequest) {
  try {
    const stats = await getDisasterStats()
    return NextResponse.json(stats)
  } catch (error) {
    console.error("Error fetching stats:", error)
    return NextResponse.json({ error: "An error occurred while fetching statistics" }, { status: 500 })
  }
}
