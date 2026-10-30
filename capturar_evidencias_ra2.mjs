import { chromium } from './frontend/node_modules/playwright-core/index.mjs'
import fs from 'node:fs'

const chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
const out = 'output/ra2_captures'
fs.mkdirSync(out, { recursive: true })
const browser = await chromium.launch({ executablePath: chrome, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 950 }, deviceScaleFactor: 1 })
const consoleLines = []
page.on('console', message => consoleLines.push(message.text()))

await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle' })
await page.getByLabel('Correo electronico').fill('ra2captura@example.com')
await page.locator('input[name="password"]').fill('ClaveSegura123!')
await page.screenshot({ path: `${out}/01-login.png`, fullPage: true })
await page.getByRole('button', { name: 'Iniciar sesion' }).click()
await page.waitForURL('**/dashboard')
await page.waitForTimeout(1200)
await page.screenshot({ path: `${out}/02-dashboard.png`, fullPage: true })
await page.screenshot({ path: `${out}/03-api-terceros.png`, fullPage: true })

await page.getByLabel('Codigo ISO').fill('MX')
await page.getByRole('button', { name: 'Consultar' }).click()
await page.waitForTimeout(2500)
await page.screenshot({ path: `${out}/04-soap.png`, fullPage: true })
fs.writeFileSync(`${out}/console.txt`, consoleLines.join('\n'), 'utf8')
await browser.close()
console.log(out)
