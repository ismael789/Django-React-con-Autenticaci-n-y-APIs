import { createContext, useEffect, useState } from 'react'
import { getMeApi, getToken, loginApi, removeToken, saveToken } from '../api/auth'

export const AuthContext = createContext(null)
export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined)
  useEffect(() => { const token = getToken(); token ? getMeApi(token).then(user => setAuth({ token, user })).catch(() => { removeToken(); setAuth(null) }) : setAuth(null) }, [])
  const login = async (values) => { const data = await loginApi(values); saveToken(data.access); console.log('Token JWT obtenido:', data.access); const user = await getMeApi(data.access); setAuth({ token: data.access, user }); return data }
  const logout = () => { removeToken(); setAuth(null) }
  return <AuthContext.Provider value={{ auth, login, logout }}>{children}</AuthContext.Provider>
}
