import React from "react";
import { Suspense } from "react"
import DisasterResponseForm from "@/components/disaster-response-form"
import DisasterStats from "@/components/disaster-stats"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Disaster Response Classification</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            This application uses machine learning to classify messages related to humanitarian disasters, helping NGOs
            and institutions provide quick and accurate responses during crises.
          </p>
        </header>

        <Tabs defaultValue="classify" className="max-w-4xl mx-auto">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="classify">Classify Message</TabsTrigger>
            <TabsTrigger value="stats">Disaster Statistics</TabsTrigger>
          </TabsList>

          <TabsContent value="classify" className="p-4 bg-white rounded-lg shadow-md">
            <DisasterResponseForm />
          </TabsContent>

          <TabsContent value="stats" className="p-4 bg-white rounded-lg shadow-md">
            <Suspense fallback={<div>Loading statistics...</div>}>
              <DisasterStats />
            </Suspense>
          </TabsContent>
        </Tabs>
      </div>
    </main>
  )
}
