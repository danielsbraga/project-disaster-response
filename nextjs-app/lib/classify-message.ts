import type { ClassificationResult, DisasterCategory } from "./types"

// This is a mock implementation that simulates the classification process
// In a real application, this would call an API endpoint that uses the ML model
export async function classifyMessage(message: string): Promise<ClassificationResult> {
  // Simulate API call delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  const lowerCaseMessage = message.toLowerCase()

  // Define keywords for each category
  const categoryKeywords: Record<string, string[]> = {
    earthquake: ["earthquake", "quake", "tremor", "seismic"],
    flood: ["flood", "flooding", "water level", "submerged"],
    fire: ["fire", "burning", "flames", "smoke"],
    hurricane: ["hurricane", "cyclone", "typhoon", "storm"],
    tornado: ["tornado", "twister", "windstorm"],
    tsunami: ["tsunami", "tidal wave", "sea level"],
    drought: ["drought", "dry", "water shortage"],
    landslide: ["landslide", "mudslide", "rockfall"],
    medical: ["medical", "medicine", "doctor", "hospital", "injured", "wound"],
    food: ["food", "hungry", "starving", "meal", "nutrition"],
    water: ["water", "thirsty", "drinking water", "clean water"],
    shelter: ["shelter", "housing", "homeless", "roof"],
    clothing: ["clothing", "clothes", "blankets"],
    money: ["money", "cash", "financial", "donation"],
    missing_people: ["missing", "lost", "disappeared", "find"],
    refugees: ["refugee", "displaced", "evacuation"],
    death: ["death", "dead", "killed", "fatalities"],
    infrastructure: ["infrastructure", "road", "bridge", "building", "collapsed"],
    weather: ["weather", "storm", "rain", "wind", "snow", "temperature"],
  }

  // Check for disaster-related keywords
  const disasterKeywords = [
    "disaster",
    "emergency",
    "crisis",
    "catastrophe",
    "calamity",
    "earthquake",
    "flood",
    "hurricane",
    "tornado",
    "tsunami",
    "drought",
    "fire",
    "landslide",
    "avalanche",
    "volcanic",
    "epidemic",
    "pandemic",
    "outbreak",
    "famine",
    "war",
    "explosion",
    "collapse",
    "crash",
    "accident",
    "attack",
    "rescue",
    "evacuate",
    "evacuating",
    "evacuation",
    "help",
    "victim",
    "survivor",
    "trapped",
    "stranded",
    "injured",
    "damage",
    "destroyed",
    "devastated",
    "devastation",
    "rubble",
    "urgent",
    "immediately",
    "emergency",
    "critical",
    "severe",
    "death",
    "dead",
    "dying",
    "casualty",
    "casualties",
  ]

  // Determine if the message is disaster-related
  const isDisasterRelated = disasterKeywords.some((keyword) => lowerCaseMessage.includes(keyword))

  // Identify categories
  const categories: DisasterCategory[] = []

  Object.entries(categoryKeywords).forEach(([category, keywords]) => {
    const matchedKeywords = keywords.filter((keyword) => lowerCaseMessage.includes(keyword))

    if (matchedKeywords.length > 0) {
      // Calculate a mock confidence score based on the number of matched keywords
      const confidence = Math.min(0.5 + matchedKeywords.length * 0.1, 0.99)

      categories.push({
        name: category,
        confidence: Number.parseFloat(confidence.toFixed(2)),
      })
    }
  })

  // Sort categories by confidence (highest first)
  categories.sort((a, b) => b.confidence - a.confidence)

  return {
    categories,
    isDisasterRelated,
  }
}
