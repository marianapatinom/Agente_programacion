import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { FiTerminal, FiUser } from "react-icons/fi";

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";
  const Icon = isUser ? FiUser : FiTerminal;

  return (
    <motion.div
      className={`flex gap-4 ${isUser ? "justify-end" : "justify-start"}`}
      initial={{ opacity: 0, y: 14, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
    >
      {!isUser && (
        <div className="mt-1 grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-slate-800 bg-slate-950 text-emerald-300">
          <Icon />
        </div>
      )}

      <article
        className={`max-w-[88%] rounded-xl border px-5 py-4 text-sm leading-7 sm:max-w-[78%] ${
          isUser
            ? "border-blue-500/20 bg-blue-600/90 text-white"
            : "border-slate-800 bg-[#0d1424] text-slate-100"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.text}</p>
        ) : (
          <ReactMarkdown
            components={{
              code({ inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || "");
                if (!inline && match) {
                  return (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                      customStyle={{
                        borderRadius: "10px",
                        margin: "14px 0",
                        fontSize: "13px",
                      }}
                      {...props}
                    >
                      {String(children).replace(/\n$/, "")}
                    </SyntaxHighlighter>
                  );
                }
                return (
                  <code
                    className="rounded-md bg-slate-950 px-1.5 py-0.5 text-cyan-200"
                    {...props}
                  >
                    {children}
                  </code>
                );
              },
              h2({ children }) {
                return (
                  <h2 className="mb-3 text-lg font-semibold text-white">
                    {children}
                  </h2>
                );
              },
              h3({ children }) {
                return (
                  <h3 className="mb-2 mt-4 text-sm font-semibold text-cyan-200">
                    {children}
                  </h3>
                );
              },
              ul({ children }) {
                return <ul className="my-3 list-disc space-y-1 pl-5">{children}</ul>;
              },
              ol({ children }) {
                return (
                  <ol className="my-3 list-decimal space-y-1 pl-5">{children}</ol>
                );
              },
              table({ children }) {
                return (
                  <div className="my-4 overflow-x-auto">
                    <table className="min-w-full border-collapse text-left text-sm">
                      {children}
                    </table>
                  </div>
                );
              },
              th({ children }) {
                return (
                  <th className="border border-slate-700 bg-slate-950 px-3 py-2">
                    {children}
                  </th>
                );
              },
              td({ children }) {
                return <td className="border border-slate-800 px-3 py-2">{children}</td>;
              },
            }}
          >
            {message.text}
          </ReactMarkdown>
        )}
        {message.source && (
          <p className="mt-4 border-t border-slate-800 pt-2 text-xs text-slate-500">
            Fuente: {message.source}
          </p>
        )}
      </article>

      {isUser && (
        <div className="mt-1 grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-blue-500/20 bg-blue-950 text-cyan-200">
          <Icon />
        </div>
      )}
    </motion.div>
  );
}
