import { Hono } from "hono"
import { env } from "hono/adapter"
import { cors } from "hono/cors"
import axios from "axios"

const app = new Hono().basePath("/api")
app.use('/*', cors())

app.get("/submissions/:submission_id", async (ctx) => {
  try {
    const { submission_id } = ctx.req.param()

    const { data } = await axios.get('http://localhost:3000/submissions/' + submission_id)

    return ctx.json({
      data
    })
  } catch (err) {
    console.error(err)
    return ctx.json({
      results: [],
      message: 'Not found'
    }, { status: 404 })
  }

})


export default app
