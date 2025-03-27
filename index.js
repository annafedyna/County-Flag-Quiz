import express from "express";
import bodyParser from "body-parser";
import "dotenv/config";
import pg from "pg";

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));
let quiz = [];

const db = new pg.Client({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_DATABASE,
  password: process.env.DB_PASSWORD,
  port: parseInt(process.env.DB_PORT),
});

const fetchData = async () => {
  try {
    await db.connect();
    const res = await db.query("SELECT * FROM flags");
    return res.rows;
  } catch (err) {
    console.error("Error executing query", err.stack);
    return [];
  }
};

fetchData().then((res) => {
  quiz = res;
});

function getNextRandomQuestion(quiz) {
  return quiz[Math.floor(Math.random() * quiz.length)];
}

let totalCorrect = 0;
let bestScore = 0;
let currentQuestion = {};

app.get("/", (req, res) => {
  bestScore = 0;
  res.render("index.ejs");
});

app.get("/play", async (req, res) => {
  currentQuestion = await getNextRandomQuestion(quiz);
  res.render("game.ejs", { question: currentQuestion });
});

app.post("/submit", async (req, res) => {
  const answer = req.body.answer.trim();
  if (answer.toLowerCase() === currentQuestion.name.toLowerCase()) {
    totalCorrect += 1;
    currentQuestion = await getNextRandomQuestion(quiz);
    res.render("game.ejs", {
      question: currentQuestion,
      totalCorrect: totalCorrect,
    });
  } else {
    bestScore = Math.max(totalCorrect, bestScore);
    totalCorrect = 0;
    currentQuestion = await getNextRandomQuestion(quiz);
    res.render("index.ejs", {
      bestScore: bestScore,
    });
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
