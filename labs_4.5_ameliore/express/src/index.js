const express = require("express")

const app = express()
const port = process.env.PORT || 3000
const FLASK_URL = process.env.FLASK_URL || "http://localhost:5000"
const SPRING_URL = process.env.SPRING_URL || "http://localhost:8080"

// Appelle une URL et renvoie son contenu (JSON si possible, sinon texte)
async function call(url) {
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(5000) })
    const text = await response.text()
    try {
      return JSON.parse(text)
    } catch {
      return text
    }
  } catch (error) {
    return `ERREUR (${url}) : ${error.message}`
  }
}

// Point d'entrée de l'application polyglotte :
// Express interroge Flask (qui interroge lui-même Spring Boot, PostgreSQL et Redis) et Spring Boot
app.get("/", async (req, res) => {
  const [flask, spring] = await Promise.all([call(FLASK_URL), call(SPRING_URL)])
  res.json({
    express: "Hello, Express!",
    flask,
    spring,
  })
})

app.listen(port, () => console.log(`Express écoute sur le port ${port}`))
