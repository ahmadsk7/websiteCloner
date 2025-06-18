'use client'

import { useState } from 'react'
import axios from 'axios'
import InputBox from '@/components/InputBox'

interface CloneResponse {
  html: string;
  design_context: {
    url: string;
    html: string;
    title: string;
    meta: {
      description: string;
    };
    styles: Record<string, {
      color: string;
      backgroundColor: string;
      fontSize: string;
    }>;
    assets: {
      images: Array<{
        src: string;
        alt: string;
        width: number;
        height: number;
      }>;
    };
  };
}

type LoadingState = 'idle' | 'scraping' | 'processing' | 'generating' | 'complete';

export default function Home() {
  const [url, setUrl] = useState('')
  const [loadingState, setLoadingState] = useState<LoadingState>('idle')
  const [cloneResult, setCloneResult] = useState<CloneResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (inputUrl: string) => {
    console.log('Starting submission with URL:', inputUrl);
    setUrl(inputUrl)
    setLoadingState('scraping')
    setCloneResult(null)
    setError(null)
    try {
      // Ensure URL is properly formatted
      const formattedUrl = inputUrl.startsWith('http') ? inputUrl : `https://${inputUrl}`;
      console.log('Sending request to backend...', { url: formattedUrl });
      const res = await axios.post<CloneResponse>('http://127.0.0.1:9000/api/clone', { 
        url: formattedUrl 
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        withCredentials: false
      });
      console.log('Received response:', res.data);
      setCloneResult(res.data);
      setLoadingState('complete');
      console.log('State updated, loading complete');
    } catch (err: any) {
      console.error('Error details:', err);
      console.error('Error response:', err.response);
      console.error('Error message:', err.message);
      setError(err.response?.data?.detail || err.message || 'Failed to clone website. Please try again.');
      setLoadingState('idle');
      console.log('Error state set, loading idle');
    }
  }

  const getLoadingMessage = () => {
    switch (loadingState) {
      case 'scraping':
        return 'Scraping website content...';
      case 'processing':
        return 'Processing design elements...';
      case 'generating':
        return 'Generating clone with AI...';
      default:
        return 'Loading...';
    }
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
            <InputBox onSubmit={handleSubmit} isLoading={loadingState !== 'idle'} />
          </div>
          {loadingState !== 'idle' && loadingState !== 'complete' && (
            <div className="mt-6">
              <div className="flex items-center justify-center space-x-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-900"></div>
                <p className="text-gray-600">{getLoadingMessage()}</p>
              </div>
            </div>
          )}
          {error && (
            <div className="mt-6 text-red-500">{error}</div>
          )}
          {cloneResult && (
            <div className="mt-12 space-y-8">
              <div className="p-6 bg-white rounded-lg shadow">
                <h2 className="text-2xl font-semibold mb-4">Generated Clone</h2>
                <div className="text-left mb-4">
                  <h3 className="text-lg font-medium">Title: {cloneResult.design_context.title}</h3>
                  <p className="text-gray-600">Description: {cloneResult.design_context.meta.description}</p>
                </div>
                <div dangerouslySetInnerHTML={{ __html: cloneResult.html }} />
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  )
} 