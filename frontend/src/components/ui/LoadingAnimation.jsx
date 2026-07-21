import { Loader2 } from "lucide-react";

export default function LoadingAnimation({ stage = 0 }) {
  const stages = [
    "Reading Documents...",
    "Searching Chunks...",
    "Generating Response...",
    "Finalizing...",
  ];

  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12">
      <div className="relative w-16 h-16">
        <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-12 h-12 border-4 border-blue-200 dark:border-blue-800 rounded-full" />
        </div>
      </div>

      <div className="text-center">
        <p className="text-sm font-semibold text-blue-600 mb-2">
          {stages[Math.min(stage, stages.length - 1)]}
        </p>

        <div className="flex gap-1 justify-center">
          {stages.map((_, index) => (
            <div
              key={index}
              className={`h-2 w-2 rounded-full transition-all duration-300 ${
                index <= stage
                  ? "bg-blue-600 w-6"
                  : "bg-gray-300 dark:bg-gray-700"
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
