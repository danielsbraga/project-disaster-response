export interface DisasterCategory {
  name: string
  confidence: number
}

export interface ClassificationResult {
  categories: DisasterCategory[]
  isDisasterRelated: boolean
}

export interface DisasterStats {
  totalMessages: number
  disasterRelated: number
  nonDisasterRelated: number
  categoriesDistribution: Array<{
    name: string
    count: number
  }>
  genreDistribution: Array<{
    name: string
    value: number
  }>
}
