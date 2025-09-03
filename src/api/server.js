const express = require("express");
const cors = require("cors");
const { createClient } = require("@supabase/supabase-js");

const app = express();

// 🔹 Configurações Express
app.use(cors());
app.use(express.json());

// 🔹 Supabase
const SUPABASE_URL = "https://hvbvembchrfhrmoasokm.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2YnZlbWJjaHJmaHJtb2Fzb2ttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYzMTc4MTUsImV4cCI6MjA3MTg5MzgxNX0.4ADUxmO7hM24CCWDYnYhmptPvI25P9XRgN5H7xg8SGc";
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

const NOME_TABELA_TEXTOS = "Textos";
const NOME_TABELA_USUARIOS = "Usuarios"; // case sensitive

// 🔹 GET: todos os textos
app.get("/text", async (req, res) => {
  try {
    const { data, error } = await supabase
      .from(NOME_TABELA_TEXTOS)
      .select("texto")
      .order("id", { ascending: true });

    if (error) throw error;

    const textos = data.map(item => item.texto);
    res.json({ status: "ok", textos });
  } catch (err) {
    console.error(err);
    res.status(500).json({ status: "erro", mensagem: "Falha ao buscar textos" });
  }
});

// 🔹 GET: todos os usuários (mesma lógica de /text)
app.get("/usuarios", async (req, res) => {
  try {
    const { data, error } = await supabase
      .from("Usuarios") // Use exatamente o case correto
      .select("*")
      .order("id", { ascending: true });

    if (error) throw error;
    res.json({ status: "ok", usuarios: data });
  } catch (err) {
    console.error(err);
    res.status(500).json({ status: "erro", mensagem: "Falha ao buscar usuários" });
  }
});


// 🔹 Inicia servidor
app.listen(3000, () => {
  console.log("✅ Servidor rodando em: http://localhost:3000");
  console.log("👉 Endpoints disponíveis:");
  console.log("   - GET  /text");
  console.log("   - GET  /usuarios");
});
