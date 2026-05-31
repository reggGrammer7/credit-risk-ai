import { useState } from 'react'
import { ChevronRight, Loader2 } from 'lucide-react'

const DEFAULTS = {
  age: 35,
  income: 65000,
  loan_amount: 15000,
  loan_term: 36,
  credit_score: 680,
  employment_years: 4,
  debt_to_income: 0.28,
  num_credit_lines: 5,
  num_delinquencies: 0,
  home_ownership: 'RENT',
}

const fields = [
  { key: 'age',               label: 'Age',                  type: 'number', min: 18,  max: 100,  step: 1     },
  { key: 'income',            label: 'Annual income ($)',     type: 'number', min: 0,   max: null, step: 1000  },
  { key: 'loan_amount',       label: 'Loan amount ($)',       type: 'number', min: 0,   max: null, step: 500   },
  { key: 'loan_term',         label: 'Loan term (months)',    type: 'number', min: 1,   max: 360,  step: 1     },
  { key: 'credit_score',      label: 'Credit score',          type: 'number', min: 300, max: 850,  step: 1     },
  { key: 'employment_years',  label: 'Employment years',      type: 'number', min: 0,   max: 50,   step: 0.5   },
  { key: 'debt_to_income',    label: 'Debt-to-income (0–1)',  type: 'number', min: 0,   max: 1,    step: 0.01  },
  { key: 'num_credit_lines',  label: 'Open credit lines',     type: 'number', min: 0,   max: 50,   step: 1     },
  { key: 'num_delinquencies', label: 'Past delinquencies',    type: 'number', min: 0,   max: 20,   step: 1     },
]

export default function InputForm({ onSubmit, loading }) {
  const [form, setForm] = useState(DEFAULTS)

  const set = (key, val) => setForm(prev => ({ ...prev, [key]: val }))

  const handleSubmit = (e) => {
    e.preventDefault()
    const parsed = { ...form }
    fields.forEach(f => { parsed[f.key] = parseFloat(form[f.key]) })
    parsed.num_credit_lines   = parseInt(form.num_credit_lines)
    parsed.num_delinquencies  = parseInt(form.num_delinquencies)
    parsed.loan_term          = parseInt(form.loan_term)
    parsed.age                = parseInt(form.age)
    onSubmit(parsed)
  }

  return (
    <form onSubmit={handleSubmit} className="card space-y-5">
      <div>
        <h2 className="text-base font-medium text-white">Applicant details</h2>
        <p className="text-xs text-white/40 mt-0.5">Fill in all fields and run the assessment</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {fields.map(f => (
          <div key={f.key}>
            <label className="label">{f.label}</label>
            <input
              className="input-field"
              type={f.type}
              min={f.min}
              max={f.max}
              step={f.step}
              value={form[f.key]}
              onChange={e => set(f.key, e.target.value)}
              required
            />
          </div>
        ))}

        <div>
          <label className="label">Home ownership</label>
          <select
            className="input-field"
            value={form.home_ownership}
            onChange={e => set('home_ownership', e.target.value)}
          >
            <option value="RENT">Rent</option>
            <option value="OWN">Own</option>
            <option value="MORTGAGE">Mortgage</option>
          </select>
        </div>
      </div>

      <button type="submit" disabled={loading} className="btn-primary w-full">
        {loading
          ? <><Loader2 size={16} className="animate-spin" /> Analysing…</>
          : <><ChevronRight size={16} /> Run risk assessment</>
        }
      </button>
    </form>
  )
}
