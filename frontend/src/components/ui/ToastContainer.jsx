import { useContext } from "react";
import { Check, AlertCircle, Info, X } from "lucide-react";
import { ToastContext } from "../../context/ToastContext";

export default function ToastContainer() {
  const { toasts, removeToast } = useContext(ToastContext);

  const getIcon = (type) => {
    switch (type) {
      case "success":
        return <Check size={18} className="text-green-600" />;
      case "error":
        return <AlertCircle size={18} className="text-red-600" />;
      case "info":
        return <Info size={18} className="text-blue-600" />;
      default:
        return null;
    }
  };

  const getStyles = (type) => {
    switch (type) {
      case "success":
        return "bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800 text-green-800 dark:text-green-300";
      case "error":
        return "bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800 text-red-800 dark:text-red-300";
      case "info":
        return "bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-300";
      default:
        return "bg-slate-50 dark:bg-slate-950/30 border-slate-200 dark:border-slate-800";
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`flex items-center gap-3 px-4 py-3 rounded-lg border backdrop-blur-sm ${getStyles(
            toast.type
          )} animate-in fade-in slide-in-from-right-4 duration-300`}
        >
          {getIcon(toast.type)}
          <span className="font-medium text-sm flex-1">{toast.message}</span>
          <button
            onClick={() => removeToast(toast.id)}
            className="text-muted-foreground hover:text-foreground transition"
          >
            <X size={16} />
          </button>
        </div>
      ))}
    </div>
  );
}
