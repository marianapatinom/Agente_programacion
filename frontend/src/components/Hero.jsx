import { motion } from "framer-motion";
import { FiCode, FiCpu, FiTerminal } from "react-icons/fi";

const metrics = [
  { icon: FiCode, label: "Lenguajes", value: "Python, JS, SQL" },
  { icon: FiTerminal, label: "Soporte", value: "Errores y código" },
  { icon: FiCpu, label: "Conceptos", value: "Algoritmos y web" },
];

export default function Hero() {
  return (
    <section className="mx-auto max-w-7xl px-4 pb-6 pt-10 sm:px-6 lg:px-8 lg:pt-14">
      <motion.div
        className="max-w-4xl"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <div className="mb-5 inline-flex w-fit items-center gap-2 rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-300">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          Asistente técnico para estudiantes
        </div>

        <h2 className="max-w-3xl bg-gradient-to-r from-blue-400 via-cyan-300 to-emerald-300 bg-clip-text text-4xl font-bold leading-tight text-transparent sm:text-5xl">
          Aprende programación con respuestas claras y ejemplos de código
        </h2>

        <p className="mt-5 max-w-2xl text-base leading-8 text-slate-300">
          StudyBot ayuda a entender conceptos, depurar errores y construir
          ejemplos en Python, JavaScript, SQL, HTML, CSS y desarrollo web.
        </p>

        <div className="mt-8 grid gap-3 sm:grid-cols-3">
          {metrics.map((item) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={item.label}
                className="rounded-lg border border-slate-800 bg-slate-900/75 p-4"
                whileHover={{ y: -3 }}
                transition={{ type: "spring", stiffness: 320, damping: 22 }}
              >
                <Icon className="mb-4 text-2xl text-cyan-300" />
                <p className="text-sm text-slate-500">{item.label}</p>
                <p className="mt-1 font-semibold text-white">{item.value}</p>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    </section>
  );
}
