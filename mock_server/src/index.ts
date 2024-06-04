import { Hono } from "hono"
import { env } from "hono/adapter"
import { cors } from "hono/cors"
import axios from "axios"

const app = new Hono().basePath('/api');
app.use('/*', cors());

const JSON_SERVER_URL = 'http://127.0.0.1:3000';

app.get('/submissions/:submission_id', async (ctx) => {
  try {
    const { submission_id } = ctx.req.param();
    console.log(`Fetching submission ID: ${submission_id}`);

    const { data } = await axios.get(`${JSON_SERVER_URL}/submissions/${submission_id}`);
    console.log('Data fetched:', data);

    return ctx.json({ data });
  } catch (err) {
    console.error('Error fetching submission:', err);
    return ctx.json({ results: [], message: 'Not found' }, { status: 404 });
  }
});

export default app;
