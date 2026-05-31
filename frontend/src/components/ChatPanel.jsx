import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Sparkles } from 'lucide-react'
import { chat } from '../services/api'

const SUGGESTIONS = [
  'Why was this applicant declined?',
  'What would improve their score the most?',
  'Which factor has the biggest impact?',
  'Is this a borderline case?',
]

function TypingIndicator() {
  return (
    <div className="flex gap-2 items-start">
      <div className="w-7 h-7 rounded-full bg-accent/20 flex items-center justify-center flex-shrink-0">
        <Bot size={14} className="text-accent" />
      </div>
      <div className="bg-ink-800 rounded-2xl rounded-tl-sm px-4 py-3">
        <div className="typing flex gap-1.5 items-center h-4">
          <span className="w-1.5 h-1.5 bg-white/40 rounded-full block" />
          <span className="w-1.5 h-1.5 bg-white/40 rounded-full block" />
          <span className="w-1.5 h-1.5 bg-white/40 rounded-full block" />
        </div>
      </div>
    </div>
  )
}

function Message({ role, content }) {
  const isUser = role === 'user'
  return (
    <div className={`flex gap-2 items-start fade-up ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 ${
        isUser ? 'bg-accent/30' : 'bg-accent/20'
      }`}>
        {isUser ? <User size={14} className="text-accent" /> : <Bot size={14} className="text-accent" />}
      </div>
      <div className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
        isUser
          ? 'bg-accent/20 text-white rounded-tr-sm'
          : 'bg-ink-800 text-white/80 rounded-tl-sm'
      }`}>
        {content}
      </div>
    </div>
  )
}

export default function ChatPanel({ applicant, prediction }) {
  const [messages, setMessages]   = useState([])
  const [input, setInput]         = useState('')
  const [loading, setLoading]     = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    setMessages([])
  }, [prediction])

  const send = async (question) => {
    if (!question.trim() || loading || !prediction) return

    const userMsg = { role: 'user', content: question }
    const next = [...messages, userMsg]
    setMessages(next)
    setInput('')
    setLoading(true)

    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }))
      const res = await chat({ applicant, prediction, question, history })
      setMessages([...next, { role: 'assistant', content: res.answer }])
    } catch (err) {
      setMessages([...next, {
        role: 'assistant',
        content: 'Sorry, something went wrong. Check that your API key is set in the backend .env file.',
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(input) }
  }

  if (!prediction) {
    return (
      <div className="card flex flex-col items-center justify-center py-12 text-center space-y-2">
        <Sparkles size={28} className="text-accent/40" />
        <p className="text-sm text-white/30">Run an assessment first,<br />then ask the AI to explain it</p>
      </div>
    )
  }

  return (
    <div className="card flex flex-col h-[480px]">
      <div className="flex items-center gap-2 mb-4 pb-4 border-b border-ink-700">
        <Sparkles size={15} className="text-accent" />
        <h2 className="text-base font-medium text-white">Ask the AI analyst</h2>
      </div>

      {messages.length === 0 && (
        <div className="space-y-2 mb-4">
          <p className="text-xs text-white/30 uppercase tracking-wider">Suggested questions</p>
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map(s => (
              <button
                key={s}
                onClick={() => send(s)}
                className="text-xs bg-ink-800 hover:bg-ink-700 text-white/60 hover:text-white
                           px-3 py-1.5 rounded-lg transition-colors border border-ink-700"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {messages.map((m, i) => <Message key={i} role={m.role} content={m.content} />)}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2 mt-4 pt-4 border-t border-ink-700">
        <input
          className="input-field flex-1"
          placeholder="Ask about this prediction…"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading}
        />
        <button
          onClick={() => send(input)}
          disabled={!input.trim() || loading}
          className="btn-primary px-4 py-2.5"
          aria-label="Send"
        >
          <Send size={15} />
        </button>
      </div>
    </div>
  )
}
