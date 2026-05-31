import { useState } from 'react'
import { predict } from './services/api'
import InputForm   from './components/InputForm'
import ResultsCard from './components/ResultsCard'
import ShapChart   from './components/ShapChart'
import ChatPanel   from './components/ChatPanel'
import { Activity } from 'lucide-react'

export default function App() {
  const [applicant,   setApplicant]   = useState(null)
  const [prediction,  setPrediction]  = useState(null)
  const [loading,     setLoading]     = useState(false)
  const [error,       setError]       = useState(null)

  const handleSubmit = async (data) => {
    setLoading(true)
    setError(null)
    try {
      const result = await predict(data)
      setApplicant(data)
      setPrediction(result)
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to connect to backend. Is it running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-ink-950 font-sans">
      {/* Header */}
      <header className="border-b border-ink-800 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center gap-3">
          <div className="w-8 h-8 bg-accent/20 rounded-lg flex items-center justify-center">
            <Activity size={16} className="text-accent" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white tracking-tight">CreditAI</h1>
            <p className="text-xs text-white/30">Risk assessment platform</p>
          </div>
        </div>
      </header>

      {/* Body */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {error && (
          <div className="mb-6 bg-risk-high/10 border border-risk-high/30 text-risk-high
                          text-sm rounded-xl px-4 py-3">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-[380px_1fr] gap-6">
          {/* Left column */}
          <div className="space-y-6">
            <InputForm onSubmit={handleSubmit} loading={loading} />
          </div>

          {/* Right column */}
          <div className="space-y-6">
            {prediction ? (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <ResultsCard prediction={prediction} />
                  <ShapChart   prediction={prediction} />
                </div>
                <ChatPanel applicant={applicant} prediction={prediction} />
              </>
            ) : (
              <div className="card flex flex-col items-center justify-center h-64 text-center space-y-3">
                <Activity size={32} className="text-accent/30" />
                <p className="text-sm text-white/30">
                  Fill in the applicant details and run<br />an assessment to see results here
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
