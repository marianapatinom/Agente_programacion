import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import {
  FiAlertTriangle,
  FiCheckCircle,
  FiCode,
  FiDatabase,
  FiSend,
} from "react-icons/fi";

import { askStudyBot, checkBackendHealth } from "../services/api.js";
import Loader from "./Loader.jsx";
import MessageBubble from "./MessageBubble.jsx";

const initialMessages = [
  {
    id: "welcome",
    role: "assistant",
    text: "Hola. Soy StudyBot, tu asistente de programación. Pregúntame sobre errores, React, Python, APIs, SQL, algoritmos o buenas prácticas.",
    source: "programming-notes.txt",
  },
];

const suggestions = [
  "Explícame qué hace useEffect en React",
  "Hazme un ejemplo de API REST con FastAPI",
  "¿Qué es un JOIN en SQL?",
  "¿Cómo depuro un error en Python?",
];

export default function ChatBox() {
  const [messages, setMessages] = useState(initialMessages);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiStatus, setApiStatus] = useState("checking");
  const scrollRef = useRef(null);

  useEffect(() => {
    async function loadHealth() {
      try {
        await checkBackendHealth();
        setApiStatus("online");
      } catch {
        setApiStatus("offline");
      }
    }

    loadHealth();
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const cleanQuestion = question.trim();

    if (!cleanQuestion || loading) {
      return;
    }

    setError("");
    setQuestion("");
    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", text: cleanQuestion },
    ]);
    setLoading(true);

    try {
      const data = await askStudyBot(cleanQuestion);
      setApiStatus("online");
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: data.answer,
          source: data.source,
        },
      ]);
    } catch (requestError) {
      const detail =
        requestError.response?.data?.detail ||
        "No fue posible conectar con el agente. Inicia el backend en el puerto 8000.";
      setApiStatus("offline");
      setError(detail);
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: `No pude procesar la pregunta: ${detail}`,
          source: "api",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.section
      className="mx-auto max-w-7xl px-4 pb-16 sm:px-6 lg:px-8"
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.65, delay: 0.15, ease: "easeOut" }}
    >
      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        <aside className="hidden rounded-2xl border border-slate-800 bg-slate-950/55 p-4 lg:block">
          <p className="mb-4 text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
            Temas
          </p>
          {[
            ["Frontend", "React, HTML, CSS, estado, componentes", FiCode],
            ["Backend", "FastAPI, APIs REST, HTTP, JSON", FiSend],
            ["Datos", "SQL, joins, modelos y consultas", FiDatabase],
          ].map(([title, description, Icon]) => (
            <div
              key={title}
              className="mb-3 rounded-xl border border-slate-800 bg-slate-900/45 p-4"
            >
              <Icon className="mb-3 text-cyan-300" />
              <h4 className="text-sm font-semibold text-white">{title}</h4>
              <p className="mt-1 text-xs leading-5 text-slate-400">{description}</p>
            </div>
          ))}
        </aside>

        <div className="overflow-hidden rounded-2xl border border-slate-800 bg-[#0f172a] shadow-2xl shadow-black/20">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 px-5 py-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                Asistente técnico
              </p>
              <h3 className="text-xl font-semibold text-white">
                Tutor de programación
              </h3>
            </div>
            <div
              className={`inline-flex items-center gap-2 rounded-lg border px-3 py-2 text-sm ${
                apiStatus === "online"
                  ? "border-emerald-500/25 bg-emerald-500/10 text-emerald-200"
                  : "border-amber-500/25 bg-amber-500/10 text-amber-100"
              }`}
            >
              <FiCheckCircle />
              {apiStatus === "online" ? "Backend conectado" : "Backend pendiente"}
            </div>
          </div>

          <div
            ref={scrollRef}
            className="chat-scroll flex h-[520px] flex-col gap-6 overflow-y-auto bg-[#0b1120] px-5 py-6"
          >
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}

            {loading && (
              <div className="flex justify-start gap-3">
                <div className="mt-1 h-9 w-9 rounded-lg border border-slate-700 bg-slate-900" />
                <div className="rounded-lg border border-slate-800 bg-slate-900 px-4 py-3">
                  <Loader />
                </div>
              </div>
            )}
          </div>

          <form
            onSubmit={handleSubmit}
            className="border-t border-slate-800 bg-[#0f172a] p-4 sm:p-5"
          >
            {error && (
              <motion.div
                className="mb-3 flex items-start gap-2 rounded-lg border border-red-400/25 bg-red-500/10 px-3 py-2 text-sm text-red-100"
                initial={{ opacity: 0, y: -6 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <FiAlertTriangle className="mt-1 shrink-0" />
                <span>{error}</span>
              </motion.div>
            )}

            <div className="mb-3 flex flex-wrap gap-2">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => setQuestion(suggestion)}
                  className="rounded-full border border-slate-700 px-3 py-1.5 text-xs text-slate-300 transition hover:border-cyan-400/60 hover:text-white"
                >
                  {suggestion}
                </button>
              ))}
            </div>

            <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                maxLength={500}
                rows={3}
                className="min-h-24 flex-1 resize-none rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"
                placeholder="Pega un error, pide un ejemplo de código o pregunta un concepto..."
              />
              <motion.button
                type="submit"
                disabled={loading}
                className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-100 disabled:cursor-not-allowed disabled:opacity-60"
                whileHover={{ y: -1 }}
                whileTap={{ scale: 0.98 }}
              >
                <FiSend />
                Enviar
              </motion.button>
            </div>
          </form>
        </div>

      </div>
    </motion.section>
  );
}
