"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getDisasterStats } from "@/lib/get-disaster-stats"
import type { DisasterStats as DisasterStatsType } from "@/lib/types"
import { HelpCircle } from "lucide-react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts"
import {
  Tooltip as UITooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

// Initial empty stats to prevent hydration mismatch
const initialStats: DisasterStatsType = {
  totalMessages: 0,
  disasterRelated: 0,
  nonDisasterRelated: 0,
  categoriesDistribution: [],
  genreDistribution: []
}

const tooltips = {
  totalMessages: "Displays the total number of messages in the original dataset.",
  disasterRelated: "Indicates how many messages are related to disasters, along with the percentage.",
  nonDisaster: "Indicates how many messages are not related to disasters, along with the percentage.",
  categoriesDistribution: "Bar chart showing how many messages are associated with each disaster-related category.",
  messageGenres: "Pie chart showing the proportion of messages by genre (e.g., news, direct, social)."
}

export default function DisasterStats() {
  const [mounted, setMounted] = useState(false)
  const [stats, setStats] = useState<DisasterStatsType>(initialStats)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Handle mounting state
  useEffect(() => {
    setMounted(true)
  }, [])

  // Fetch data only after component is mounted
  useEffect(() => {
    if (!mounted) return

    const fetchStats = async () => {
      try {
        setIsLoading(true)
        setError(null)
        const data = await getDisasterStats()
        // Sort categories by count in descending order
        data.categoriesDistribution.sort((a, b) => b.count - a.count)
        setStats(data)
      } catch (error) {
        console.error("Error fetching stats:", error)
        setError("Failed to load statistics. Please try again later.")
      } finally {
        setIsLoading(false)
      }
    }

    fetchStats()
  }, [mounted])

  const COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#8884D8",
    "#82CA9D",
    "#FF6B6B",
    "#6A7FDB",
    "#F7C59F",
    "#2D3047",
  ]

  // Don't render anything until mounted to prevent hydration mismatch
  if (!mounted) {
    return null
  }

  const TitleWithTooltip = ({ title, tooltip }: { title: string, tooltip: string }) => (
    <div className="flex items-center gap-2">
      <span>{title}</span>
      <TooltipProvider>
        <UITooltip>
          <TooltipTrigger asChild>
            <button 
              aria-label="Help" 
              className="text-gray-500 hover:text-gray-700 focus:outline-none"
            >
              <HelpCircle className="h-4 w-4" />
            </button>
          </TooltipTrigger>
          <TooltipContent className="max-w-xs">
            <p>{tooltip}</p>
          </TooltipContent>
        </UITooltip>
      </TooltipProvider>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">
              <TitleWithTooltip title="Total Messages" tooltip={tooltips.totalMessages} />
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-8 w-24 bg-gray-200 animate-pulse rounded" />
            ) : (
              <p className="text-3xl font-bold">{stats.totalMessages.toLocaleString()}</p>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">
              <TitleWithTooltip title="Disaster Related" tooltip={tooltips.disasterRelated} />
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-8 w-24 bg-gray-200 animate-pulse rounded" />
            ) : (
              <>
                <p className="text-3xl font-bold text-red-600">{stats.disasterRelated.toLocaleString()}</p>
                <p className="text-sm text-gray-500">
                  ({Math.round((stats.disasterRelated / stats.totalMessages) * 100)}%)
                </p>
              </>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">
              <TitleWithTooltip title="Non-Disaster" tooltip={tooltips.nonDisaster} />
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-8 w-24 bg-gray-200 animate-pulse rounded" />
            ) : (
              <>
                <p className="text-3xl font-bold text-green-600">{stats.nonDisasterRelated.toLocaleString()}</p>
                <p className="text-sm text-gray-500">
                  ({Math.round((stats.nonDisasterRelated / stats.totalMessages) * 100)}%)
                </p>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {error ? (
        <div className="text-center p-8">
          <div className="text-red-500">{error}</div>
        </div>
      ) : (
        <Tabs defaultValue="categories">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="categories">Categories Distribution</TabsTrigger>
            <TabsTrigger value="genres">Message Genres</TabsTrigger>
          </TabsList>

          <TabsContent value="categories" className="pt-4">
            <Card>
              <CardHeader>
                <CardTitle>
                  <TitleWithTooltip title="Disaster Categories Distribution" tooltip={tooltips.categoriesDistribution} />
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[400px]">
                  {isLoading ? (
                    <div className="h-full w-full bg-gray-200 animate-pulse rounded" />
                  ) : (
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={stats.categoriesDistribution} margin={{ top: 20, right: 30, left: 20, bottom: 70 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="name" 
                          angle={-45} 
                          textAnchor="end" 
                          height={70} 
                          tick={{ fontSize: 12 }}
                          interval={0}
                          label={{ value: 'Categories', position: 'insideBottom', offset: -40 }}
                        />
                        <YAxis 
                          label={{ value: 'Messages Count', angle: -90, position: 'insideLeft', offset: -10 }}
                        />
                        <Tooltip />
                        <Bar dataKey="count" fill="#8884d8">
                          {stats.categoriesDistribution.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="genres" className="pt-4">
            <Card>
              <CardHeader>
                <CardTitle>
                  <TitleWithTooltip title="Message Genres" tooltip={tooltips.messageGenres} />
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[400px]">
                  {isLoading ? (
                    <div className="h-full w-full bg-gray-200 animate-pulse rounded" />
                  ) : (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={stats.genreDistribution}
                          cx="50%"
                          cy="50%"
                          labelLine={true}
                          outerRadius={150}
                          fill="#8884d8"
                          dataKey="value"
                          label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                        >
                          {stats.genreDistribution.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  )
}
