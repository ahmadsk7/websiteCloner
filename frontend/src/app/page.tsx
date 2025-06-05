'use client'

import { useState } from 'react'
import InputBox from '@/components/InputBox'

export default function Home() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [cloneResult, setCloneResult] = useState<string | null>(null)

  const handleSubmit = async (inputUrl: string) => {
    setUrl(inputUrl)
    setLoading(true)
    setCloneResult(null)
    // Placeholder for API call
    setTimeout(() => {
      setCloneResult('<h1>Dummy HTML for ' + inputUrl + '</h1>')
      setLoading(false)
    }, 1000)
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center space-y-8">
          <h1 className="text-5xl font-bold text-gray-900">
            Website Cloner
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform any website into a clone using AI. Just paste the URL and let our technology do the rest.
          </p>
          <div className="mt-12">
            <InputBox onSubmit={handleSubmit} isLoading={loading} />
          </div>
          {cloneResult && (
            <div className="mt-12 p-6 bg-white rounded-lg shadow">
              <div dangerouslySetInnerHTML={{ __html: cloneResult }} />
            </div>
          )}
        </div>
      </div>
    </main>
  )
} 