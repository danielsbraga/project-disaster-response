"use client";

import type React from "react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle, CheckCircle2 } from "lucide-react";
import { classifyMessage } from "@/lib/classify-message";
import type { DisasterCategory } from "@/lib/types";
import { CategoryBadge } from "./category-badge";

// Color mapping for all possible tags - Professional Palette
const TAG_COLORS: Record<string, string> = {
  aid_related: "#0088FE",      // Blue
  weather_related: "#00C49F",  // Teal
  direct_report: "#FFBB28",    // Yellow
  request: "#FF8042",          // Orange
  other_aid: "#8884D8",        // Purple
  food: "#82CA9D",            // Green
  earthquake: "#FF6B6B",      // Red
  storm: "#6A7FDB",           // Indigo
  shelter: "#F7C59F",         // Peach
  floods: "#2D3047",          // Dark Blue
  medical_help: "#E6B89C",    // Light Orange
  infrastructure_related: "#9B9B9B", // Gray
  water: "#4ECDC4",           // Turquoise
  other_weather: "#45B7D1",   // Sky Blue
  buildings: "#96CEB4",       // Sage
  medical_products: "#FFEEAD", // Light Yellow
  transport: "#D4A5A5",       // Dusty Rose
  death: "#9B59B6",           // Purple
  other_infrastructure: "#3498DB", // Blue
  refugees: "#E67E22",        // Orange
  military: "#2C3E50",        // Dark Blue
  search_and_rescue: "#E74C3C", // Red
  money: "#27AE60",           // Green
  electricity: "#F1C40F",     // Yellow
  cold: "#3498DB",            // Blue
  security: "#8E44AD",        // Purple
  clothing: "#16A085",        // Teal
  aid_centers: "#D35400",     // Orange
  missing_people: "#C0392B",  // Red
  hospitals: "#2980B9",       // Blue
  fire: "#E74C3C",           // Red
  tools: "#7F8C8D",          // Gray
  shops: "#F39C12",          // Orange
  offer: "#1ABC9C",          // Turquoise
  child_alone: "#D35400"      // Orange
}

export default function DisasterResponseForm() {
  const [message, setMessage] = useState("");
  const [lastSubmittedMessage, setLastSubmittedMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<DisasterCategory[] | null>(null);
  const [isDisaster, setIsDisaster] = useState<boolean | null>(null);
  const [highlightedExample, setHighlightedExample] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    setIsLoading(true);
    try {
      const { categories, isDisasterRelated } = await classifyMessage(message);
      setLastSubmittedMessage(message);
      setResults(categories);
      setIsDisaster(isDisasterRelated);
      setMessage("");
    } catch (error) {
      console.error("Classification error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setMessage("");
    setLastSubmittedMessage("");
    setResults(null);
    setIsDisaster(null);
    setHighlightedExample(null);
  };

  const exampleMessages = [
    "Earthquake in the city center, buildings collapsed, need medical help and rescue teams.",
    "Flood has destroyed our crops, we need food and clean water urgently.",
    "Hurricane approaching our coast, evacuation routes are needed.",
  ];

  const exampleTags = [
    ["aid_related", "fire", "medical_help"],
    ["aid_related", "child_alone", "other_weather", "water"],
    ["aid_related"]
  ];

  const loadExample = (example: string, index: number) => {
    setMessage(example);
    setResults(null);
    setIsDisaster(null);
    setHighlightedExample(example);
  };

  return (
    <div className="space-y-6">
      {results && (
        <Card className="p-4 mt-6">
          <div className="flex items-center gap-2 mb-4">
            {isDisaster ? (
              <div className="flex items-center text-red-600 gap-2">
                <AlertCircle className="h-5 w-5" />
                <span className="font-medium">Disaster Related</span>
              </div>
            ) : (
              <div className="flex items-center text-green-600 gap-2">
                <CheckCircle2 className="h-5 w-5" />
                <span className="font-medium">Not Disaster Related</span>
              </div>
            )}
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-medium">Message:</h3>
            <p className="text-gray-700 bg-gray-50 p-3 rounded-md whitespace-pre-wrap">
              {lastSubmittedMessage}
            </p>

            <h3 className="text-sm font-medium mt-4">Categories:</h3>
            {results.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {results.map((category) => (
                  <CategoryBadge 
                    key={category.name} 
                    category={category} 
                    color={TAG_COLORS[category.name.replace(/ /g, '_')]}
                  />
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No specific disaster categories detected.</p>
            )}
          </div>
        </Card>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
            Enter a message to classify
          </label>
          <Textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message related to a disaster..."
            className="min-h-[120px]"
            required
          />
        </div>

        <div className="flex flex-wrap gap-2">
          <Button type="submit" disabled={isLoading || !message.trim()}>
            {isLoading ? "Classifying..." : "Classify Message"}
          </Button>
          <Button type="button" variant="outline" onClick={handleReset}>
            Reset
          </Button>
        </div>
      </form>

      <div className="space-y-2">
        <p className="text-sm font-medium text-gray-700">Example messages:</p>
        <div className="grid grid-cols-3 gap-4">
          {exampleMessages.map((example, index) => (
            <Card key={index} className="p-4">
              <p className="text-sm">{example}</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {exampleTags[index].map((tag) => (
                  <CategoryBadge 
                    key={tag} 
                    category={{ 
                      name: tag.replace(/_/g, ' '), 
                      confidence: 1 
                    }} 
                    color={TAG_COLORS[tag]}
                  />
                ))}
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}