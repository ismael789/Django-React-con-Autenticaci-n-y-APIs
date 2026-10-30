import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { AdminLayout, ClientLayout, CommonLayout } from '../layouts'
import { Dashboard, Home, Login, Register } from '../pages'

function Protected({ children }) { const { auth } = useAuth(); if (auth === undefined) return <div className="loading">Cargando sesion...</div>; return auth ? children : <Navigate to="/login" replace /> }
export function Navigation() {
  return <Routes>
    <Route element={<CommonLayout />}><Route path="/login" element={<Login />} /><Route path="/registro" element={<Register />} /></Route>
    <Route element={<ClientLayout />}><Route path="/" element={<Home />} /></Route>
    <Route element={<Protected><AdminLayout /></Protected>}><Route path="/dashboard" element={<Dashboard />} /></Route>
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
}
