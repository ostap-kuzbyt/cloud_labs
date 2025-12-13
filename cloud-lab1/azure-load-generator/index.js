import express from "express";
import fetch from "node-fetch";

const app = express();
const port = process.env.PORT || 8080;

const url = process.env.API_URL || "https://zimbave.wonderfulsea-51d6acbd.polandcentral.azurecontainerapps.io/pizza";
const TOKEN = process.env.TOKEN || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";

const data = {
  id: 0,
  name: "string",
  description: "string",
  price: 0,
  size: "string",
  ingredients: ["string"]
};

async function sendRequest(i) {
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${TOKEN}`
      },
      body: JSON.stringify(data)
    });
    console.log(`Request ${i + 1}: ${res.status}`);
  } catch (err) {
    console.error(`Request ${i + 1} failed: ${err.message}`);
  }
}

async function runLoadTest(batchSize = 50, total = 1000, delay = 500) {
  console.log("🚀 Load test started...");
  for (let i = 0; i < total; i += batchSize) {
    const batch = [];
    for (let j = 0; j < batchSize && i + j < total; j++) {
      batch.push(sendRequest(i + j));
    }
    await Promise.all(batch);
    console.log(`Sent ${i + batchSize} requests`);
    await new Promise(r => setTimeout(r, delay));
  }
  console.log("✅ Load test finished.");
}

app.get("/", (req, res) => {
  res.send("Load generator is running. Use /start to trigger the load test.");
});

app.get("/start", async (req, res) => {
  res.send("Load test started! Check logs for progress.");
  runLoadTest();
});

app.listen(port, () => {
  console.log(`Server started on port ${port}`);
});
