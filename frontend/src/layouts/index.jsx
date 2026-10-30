import { Link, Outlet } from 'react-router-dom'
export function CommonLayout() { return <div className="app-shell"><Outlet /></div> }
export function ClientLayout() { return <div className="app-shell"><nav className="topbar"><Link className="brand" to="/">Mercado Local</Link><div><Link to="/login">Iniciar sesion</Link><Link className="button-link" to="/registro">Crear cuenta</Link></div></nav><Outlet /></div> }
export function AdminLayout() { return <div className="app-shell"><nav className="topbar"><Link className="brand" to="/dashboard">Mercado Local</Link><Link to="/">Catalogo publico</Link></nav><Outlet /></div> }
