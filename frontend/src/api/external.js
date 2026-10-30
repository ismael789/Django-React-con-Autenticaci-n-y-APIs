export async function getAdvice() {
  const response = await fetch('https://api.adviceslip.com/advice?t=' + Date.now())
  if (!response.ok) throw new Error('No se pudo consultar Advice Slip')
  return response.json()
}
