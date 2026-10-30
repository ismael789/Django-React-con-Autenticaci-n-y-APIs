import { API_ROOT, request } from './client'
export const getCountryInfo = (code, token) => request(`${API_ROOT}/soap/country/?code=${encodeURIComponent(code)}`, { headers: { Authorization: `Bearer ${token}` } })
