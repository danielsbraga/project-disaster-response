import type { ClassificationResult, DisasterCategory } from "./types"

// This is a mock implementation that simulates the classification process
// In a real application, this would call an API endpoint that uses the ML model
export async function classifyMessage(message: string): Promise<ClassificationResult> {
  try {
    const res = await fetch("/api/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    })

    if (!res.ok) {
      throw new Error("Failed to classify message")
    }

    const data = await res.json()
    
    // Transform the API response to match the expected ClassificationResult type
    const categories: DisasterCategory[] = Object.entries(data.categories)
      .filter(([name, value]) => value === 1 && name !== 'request') // Filter out 'request' tag
      .map(([name, _]) => ({
        name: name.replace(/_/g, ' '), // Convert snake_case to spaces
        confidence: 1 // ML model returns binary values, so confidence is 1
      }))

    return {
      categories,
      isDisasterRelated: data.isRelated
    }
  } catch (error) {
    console.error("Error classifying message:", error)
    throw error
  }
}
