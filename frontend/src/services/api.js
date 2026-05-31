// import axios from 'axios'

// // const api = axios.create({
// //   baseURL: '/api',
// //   headers: { 'Content-Type': 'application/json' },
// // })
// const api = axios.create({
//   baseURL: 'http://localhost:8000',
//   headers: { 'Content-Type': 'application/json' },
// })

// export async function predict(applicant) {
//   const { data } = await api.post('/predict', applicant)
//   return data
// }

// export async function chat({ applicant, prediction, question, history = [] }) {
//   const { data } = await api.post('/chat', { applicant, prediction, question, history })
//   return data
// }

// export async function healthCheck() {
//   const { data } = await api.get('/health')
//   return data
// }





import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

export async function predict(applicant, modelName = 'xgboost') {
  const { data } = await api.post(`/predict?model=${modelName}`, applicant)
  return data
}

export async function chat({ applicant, prediction, question, history = [] }) {
  const { data } = await api.post('/chat', { applicant, prediction, question, history })
  return data
}

export async function healthCheck() {
  const { data } = await api.get('/health')
  return data
}