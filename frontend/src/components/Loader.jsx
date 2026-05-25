import { motion } from "framer-motion";

export default function Loader() {
  return (
    <div className="flex items-center gap-2 px-1 py-2">
      {[0, 1, 2].map((index) => (
        <motion.span
          key={index}
          className="h-2 w-2 rounded-full bg-cyanline"
          animate={{ opacity: [0.25, 1, 0.25], y: [0, -5, 0] }}
          transition={{
            duration: 0.9,
            repeat: Infinity,
            delay: index * 0.14,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  );
}
