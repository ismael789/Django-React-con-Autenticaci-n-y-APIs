const API_URL = import.meta.env.VITE_BASE_API_URL || 'http://127.0.0.1:8000'
export const API_ROOT = `${API_URL}/api/v1`
export const TOKEN_URL = `${API_URL}/api/token/`

export async function request(url, options = {}) {
  const response = await fetch(url, { headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || 'No se pudo completar la solicitud')
  return data
}
