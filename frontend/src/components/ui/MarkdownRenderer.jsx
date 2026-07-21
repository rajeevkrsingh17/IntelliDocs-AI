import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Check, Copy } from "lucide-react";

function CodeBlock({ children, className }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const text = String(children).replace(/\n$/, "");
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group my-4 rounded-xl border border-border bg-slate-900 text-slate-100 overflow-hidden shadow-sm">
      <div className="flex items-center justify-between px-4 py-2 bg-slate-800/80 border-b border-slate-700/60 text-xs font-mono text-slate-400">
        <span>{className?.replace("language-", "") || "code"}</span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-700/60 hover:bg-slate-700 text-slate-300 transition"
          title="Copy code"
        >
          {copied ? (
            <>
              <Check size={13} className="text-green-400" />
              <span className="text-green-400 font-sans text-xs">Copied</span>
            </>
          ) : (
            <>
              <Copy size={13} />
              <span className="font-sans text-xs">Copy</span>
            </>
          )}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto font-mono text-sm leading-relaxed">
        <code>{children}</code>
      </pre>
    </div>
  );
}

/**
 * Pre-processes text to clean up raw LaTeX math expressions like $p(y|x)$ or $$...$$
 * and strips any bracketed citation tags to ensure text flows 100% cleanly.
 */
function cleanMathSyntax(text) {
  if (!text) return "";

  let cleaned = text;

  // Completely strip bracketed citations [DocName, Page X...] for 100% clean text
  cleaned = cleaned.replace(
    /\[([^\n\]]+?),\s*Page\s*(\d+)(?::\s*["“'`\s]*(.*?)["”'`\s]*)?\]/gi,
    ""
  );

  // Clean block math $$...$$ -> inline code (not fenced code blocks)
  cleaned = cleaned.replace(/\$\$(.*?)\$\$/gs, (match, equation) => {
    const trimmed = equation.trim();
    // Skip if it looks like a filename or is very short
    if (!trimmed || /\.\w{2,5}$/.test(trimmed) || trimmed.length < 3) {
      return trimmed;
    }
    return `\`${trimmed}\``;
  });

  // Clean inline math $...$ -> `...`
  cleaned = cleaned.replace(/\$([^\$\n]+?)\$/g, (match, equation) => {
    const trimmed = equation.trim();
    // Skip if it looks like a filename or a dollar amount
    if (!trimmed || /\.\w{2,5}$/.test(trimmed)) {
      return trimmed;
    }
    return `\`${trimmed}\``;
  });

  return cleaned;
}

export default function MarkdownRenderer({ content }) {
  if (!content) return null;

  const formattedContent = cleanMathSyntax(content);

  return (
    <div className="prose dark:prose-invert max-w-none text-foreground leading-relaxed">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Headings
          h1: ({ node, ...props }) => (
            <h1
              className="text-2xl font-bold text-foreground mt-6 mb-3 scroll-m-20 border-b border-border pb-2 tracking-tight"
              {...props}
            />
          ),
          h2: ({ node, ...props }) => (
            <h2
              className="text-xl font-bold text-foreground mt-6 mb-3 scroll-m-20 tracking-tight flex items-center gap-2"
              {...props}
            />
          ),
          h3: ({ node, ...props }) => (
            <h3
              className="text-lg font-semibold text-foreground mt-4 mb-2 scroll-m-20"
              {...props}
            />
          ),
          h4: ({ node, ...props }) => (
            <h4
              className="font-semibold text-foreground mt-3 mb-1.5"
              {...props}
            />
          ),

          // Paragraphs
          p: ({ node, ...props }) => (
            <p className="text-foreground leading-7 mb-4 text-base" {...props} />
          ),

          // Lists
          ul: ({ node, ...props }) => (
            <ul
              className="list-disc space-y-2 mb-4 text-foreground pl-6"
              {...props}
            />
          ),
          ol: ({ node, ...props }) => (
            <ol
              className="list-decimal space-y-2 mb-4 text-foreground pl-6"
              {...props}
            />
          ),
          li: ({ node, ...props }) => (
            <li className="text-foreground leading-relaxed pl-1" {...props} />
          ),

          // Code blocks & inline code
          code: ({ node, inline, className, children, ...props }) => {
            const text = String(children).replace(/\n$/, "");
            const isMultiLine = text.includes("\n");
            const isShort = text.length < 80;

            // Render as inline-style for: inline code, short single-line blocks, or blocks without a language
            if (inline || (!isMultiLine && isShort && !className)) {
              return (
                <code
                  className="bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 px-2 py-0.5 rounded-md text-sm font-mono border border-blue-200/80 dark:border-blue-900/80 font-medium"
                  {...props}
                >
                  {children}
                </code>
              );
            }
            return <CodeBlock className={className}>{children}</CodeBlock>;
          },
          pre: ({ node, children }) => <>{children}</>,

          // Blockquotes / Highlights — with callout detection
          blockquote: ({ node, children, ...props }) => {
            // Extract text content from children to detect callout patterns
            const textContent = String(
              children?.props?.children || children || ""
            );

            // 📌 Key Takeaway callout
            if (textContent.includes("📌") || textContent.includes("Key Takeaway")) {
              return (
                <div
                  className="border-l-4 border-emerald-500 bg-emerald-50/70 dark:bg-emerald-950/30 px-4 py-3 my-4 rounded-r-xl shadow-sm"
                  {...props}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-emerald-600 dark:text-emerald-400 text-lg mt-0.5 shrink-0">📌</span>
                    <div className="text-emerald-900 dark:text-emerald-100 font-medium text-sm leading-relaxed [&>p]:mb-0 [&>strong]:text-emerald-800 dark:[&>strong]:text-emerald-200">
                      {children}
                    </div>
                  </div>
                </div>
              );
            }

            // ⚠️ Warning/Note callout
            if (textContent.includes("⚠️") || textContent.includes("Note:")) {
              return (
                <div
                  className="border-l-4 border-amber-500 bg-amber-50/70 dark:bg-amber-950/30 px-4 py-3 my-4 rounded-r-xl shadow-sm"
                  {...props}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-amber-600 dark:text-amber-400 text-lg mt-0.5 shrink-0">⚠️</span>
                    <div className="text-amber-900 dark:text-amber-100 font-medium text-sm leading-relaxed [&>p]:mb-0 [&>strong]:text-amber-800 dark:[&>strong]:text-amber-200">
                      {children}
                    </div>
                  </div>
                </div>
              );
            }

            // 💡 Tip callout
            if (textContent.includes("💡") || textContent.includes("Tip:")) {
              return (
                <div
                  className="border-l-4 border-sky-500 bg-sky-50/70 dark:bg-sky-950/30 px-4 py-3 my-4 rounded-r-xl shadow-sm"
                  {...props}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-sky-600 dark:text-sky-400 text-lg mt-0.5 shrink-0">💡</span>
                    <div className="text-sky-900 dark:text-sky-100 font-medium text-sm leading-relaxed [&>p]:mb-0 [&>strong]:text-sky-800 dark:[&>strong]:text-sky-200">
                      {children}
                    </div>
                  </div>
                </div>
              );
            }

            // Default blockquote styling
            return (
              <blockquote
                className="border-l-4 border-blue-600 bg-blue-50/70 dark:bg-blue-950/30 px-4 py-3 my-4 italic text-foreground rounded-r-xl shadow-xs"
                {...props}
              >
                {children}
              </blockquote>
            );
          },

          // Premium Table Styling
          table: ({ node, ...props }) => (
            <div className="overflow-x-auto my-6 rounded-2xl border border-border shadow-xs bg-card">
              <table
                className="w-full border-collapse text-left text-sm text-foreground"
                {...props}
              />
            </div>
          ),
          thead: ({ node, ...props }) => (
            <thead
              className="bg-slate-100 dark:bg-slate-800/90 text-foreground font-semibold border-b border-border"
              {...props}
            />
          ),
          tbody: ({ node, ...props }) => (
            <tbody
              className="divide-y divide-border text-foreground bg-card"
              {...props}
            />
          ),
          tr: ({ node, ...props }) => (
            <tr
              className="hover:bg-blue-50/40 dark:hover:bg-blue-950/20 transition-colors"
              {...props}
            />
          ),
          th: ({ node, ...props }) => (
            <th
              className="px-5 py-3.5 font-bold text-foreground border-r border-border/50 last:border-r-0 uppercase text-xs tracking-wider"
              {...props}
            />
          ),
          td: ({ node, ...props }) => (
            <td
              className="px-5 py-3.5 text-foreground leading-relaxed border-r border-border/40 last:border-r-0 align-top"
              {...props}
            />
          ),

          // Links
          a: ({ node, ...props }) => (
            <a
              className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
              target="_blank"
              rel="noopener noreferrer"
              {...props}
            />
          ),

          // Horizontal rule
          hr: ({ node, ...props }) => (
            <hr className="my-6 border-border" {...props} />
          ),

          // Strong and emphasis
          strong: ({ node, ...props }) => (
            <strong className="font-bold text-foreground bg-amber-500/10 dark:bg-amber-400/10 px-1 py-0.5 rounded text-blue-900 dark:text-blue-100" {...props} />
          ),
          em: ({ node, ...props }) => (
            <em className="italic text-foreground" {...props} />
          ),
        }}
      >
        {formattedContent}
      </ReactMarkdown>
    </div>
  );
}
