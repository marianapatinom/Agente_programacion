import { motion } from "framer-motion";
import { FiBookOpen, FiGithub, FiShield } from "react-icons/fi";

export default function Navbar() {
  return (
    <motion.header
      className="sticky top-0 z-40 border-b border-slate-800 bg-[#0b1020]/90 backdrop-blur"
      initial={{ opacity: 0, y: -16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-lg border border-slate-700 bg-slate-900">
            <FiBookOpen className="text-xl text-cyan-300" />
          </div>
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
              Programming assistant
            </p>
            <h1 className="text-xl font-semibold text-white">
              StudyBot
            </h1>
          </div>
        </div>

        <div className="hidden items-center gap-3 md:flex">
          <span className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300">
            <FiShield className="text-emerald-300" />
            Validación activa
          </span>
          <span className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300">
            <FiGithub className="text-cyan-300" />
            API lista
          </span>
        </div>
      </nav>
    </motion.header>
  );
}
