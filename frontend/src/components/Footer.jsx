import { FiGithub, FiLayers } from "react-icons/fi";

export default function Footer() {
  return (
    <footer className="border-t border-line bg-ink/80">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-6 text-sm text-slate-400 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8">
        <span className="inline-flex items-center gap-2">
          <FiLayers className="text-cyanline" />
          StudyBot Agent Full Stack
        </span>
        <span className="inline-flex items-center gap-2">
          <FiGithub className="text-emeraldline" />
          DevSecOps academic project
        </span>
      </div>
    </footer>
  );
}
