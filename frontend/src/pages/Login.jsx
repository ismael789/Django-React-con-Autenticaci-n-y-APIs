import { useFormik } from 'formik'
import * as Yup from 'yup'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import { useAuth } from '../hooks/useAuth'

export default function Login() { const { login } = useAuth(); const navigate = useNavigate(); const formik = useFormik({ initialValues: { email: '', password: '' }, validationSchema: Yup.object({ email: Yup.string().email('Correo no valido').required('Requerido'), password: Yup.string().required('Requerido') }), onSubmit: async (values, actions) => { try { await login(values); toast.success('Sesion iniciada'); navigate('/dashboard') } catch (e) { toast.error(e.message); actions.setSubmitting(false) } } }); return <main className="auth-page"><section className="auth-card"><span className="eyebrow">MERCADO LOCAL</span><h1>Bienvenido de vuelta</h1><p>Inicia sesion para acceder a tu dashboard.</p><form onSubmit={formik.handleSubmit}><label>Correo electronico<input name="email" type="email" {...formik.getFieldProps('email')} /></label><label>Contraseña<input name="password" type="password" {...formik.getFieldProps('password')} /></label><button className="primary-button wide" type="submit" disabled={formik.isSubmitting}>Iniciar sesion</button></form><p className="form-footer">¿No tienes cuenta? <Link to="/registro">Registrate</Link></p></section></main> }
