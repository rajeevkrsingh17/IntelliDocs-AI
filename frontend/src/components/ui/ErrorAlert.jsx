import { AlertCircle, X } from "lucide-react";

export default function ErrorAlert({ message, onClose, details = null }) {
  return (
    <div className="mt-8 rounded-3xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30 p-6">
      <div className="flex gap-4">
        <div className="flex-shrink-0">
          <AlertCircle size={24} className="text-red-600 dark:text-red-400" />
        </div>

        <div className="flex-1">
          <h3 className="font-semibold text-red-900 dark:text-red-200 mb-1">
            AI Service Unavailable
          </h3>

          <p className="text-sm text-red-800 dark:text-red-300 mb-2">
            {message}
          </p>

          {details && (
            <details className="mt-3 cursor-pointer">
              <summary className="text-xs text-red-700 dark:text-red-400 font-medium hover:text-red-900 dark:hover:text-red-200">
                Show details
              </summary>
              <pre className="mt-2 p-3 bg-red-100 dark:bg-red-900/20 rounded text-xs overflow-auto text-red-900 dark:text-red-200 border border-red-200 dark:border-red-800">
                {details}
              </pre>
            </details>
          )}

          <p className="text-xs text-red-700 dark:text-red-400 mt-3">
            💡 Try again in a few moments or check your API quota.
          </p>
        </div>

        {onClose && (
          <button
            onClick={onClose}
            className="flex-shrink-0 text-red-400 hover:text-red-600 transition"
          >
            <X size={20} />
          </button>
        )}
      </div>
    </div>
  );
}
