import { Badge } from "@/components/ui/badge"
import type { DisasterCategory } from "@/lib/types"

interface CategoryBadgeProps {
  category: DisasterCategory
}

export default function CategoryBadge({ category }: CategoryBadgeProps) {
  // Map category names to colors
  const getCategoryColor = (name: string): string => {
    const colorMap: Record<string, string> = {
      earthquake: "bg-orange-100 text-orange-800 hover:bg-orange-100",
      flood: "bg-blue-100 text-blue-800 hover:bg-blue-100",
      fire: "bg-red-100 text-red-800 hover:bg-red-100",
      hurricane: "bg-purple-100 text-purple-800 hover:bg-purple-100",
      tornado: "bg-teal-100 text-teal-800 hover:bg-teal-100",
      tsunami: "bg-cyan-100 text-cyan-800 hover:bg-cyan-100",
      drought: "bg-amber-100 text-amber-800 hover:bg-amber-100",
      landslide: "bg-lime-100 text-lime-800 hover:bg-lime-100",
      medical: "bg-rose-100 text-rose-800 hover:bg-rose-100",
      food: "bg-green-100 text-green-800 hover:bg-green-100",
      water: "bg-sky-100 text-sky-800 hover:bg-sky-100",
      shelter: "bg-fuchsia-100 text-fuchsia-800 hover:bg-fuchsia-100",
      clothing: "bg-pink-100 text-pink-800 hover:bg-pink-100",
      money: "bg-emerald-100 text-emerald-800 hover:bg-emerald-100",
      missing_people: "bg-violet-100 text-violet-800 hover:bg-violet-100",
      refugees: "bg-indigo-100 text-indigo-800 hover:bg-indigo-100",
      death: "bg-gray-100 text-gray-800 hover:bg-gray-100",
      infrastructure: "bg-slate-100 text-slate-800 hover:bg-slate-100",
      weather: "bg-yellow-100 text-yellow-800 hover:bg-yellow-100",
    }

    return colorMap[name.toLowerCase()] || "bg-gray-100 text-gray-800 hover:bg-gray-100"
  }

  return (
    <Badge variant="outline" className={`${getCategoryColor(category.name)} border-0 font-medium`}>
      {category.name}
    </Badge>
  )
}
