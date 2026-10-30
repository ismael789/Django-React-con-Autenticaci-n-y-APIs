import { API_ROOT, TOKEN_URL, request } from './client'

const storageKey = import.meta.env.VITE_TOKEN_STORAGE_KEY || 'mercado_local_access_token'
export const getToken = () => localStorage.getItem(storageKey)
export const saveToken = (token) => localStorage.setItem(storageKey, token)
export const removeToken = () => localStorage.removeItem(storageKey)
export const loginApi = (values) => request(TOKEN_URL, { method: 'POST', body: JSON.stringify({ email: values.email, password: values.password }) })
export const registerApi = (values) => request(`${API_ROOT}/auth/register/`, { method: 'POST', body: JSON.stringify(values) })
export const getMeApi = (token) => request(`${API_ROOT}/auth/me/`, { headers: { Authorization: `Bearer ${token}` } })
