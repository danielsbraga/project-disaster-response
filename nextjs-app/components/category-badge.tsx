import { Badge } from "@/components/ui/badge"
import type { DisasterCategory } from "@/lib/types"

interface CategoryBadgeProps {
  category: {
    name: string
    confidence: number
  }
  color: string
}

export function CategoryBadge({ category, color }: CategoryBadgeProps) {
  return (
    <Badge 
      variant="outline" 
      className="border-0 font-medium"
      style={{ 
        backgroundColor: `${color}20`,
        color: color,
        borderColor: `${color}40`
      }}
    >
      {category.name}
    </Badge>
  )
}
