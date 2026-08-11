import { useOutletContext } from "react-router-dom";
import { Settings as SettingsIcon, Info, Database, FolderGit2 } from "lucide-react";

interface Repository {
  id: string;
  name: string;
  original_name: string;
  status: string;
  storage_path: string;
  created_at?: string;
}

function Settings() {
  const { repository } = useOutletContext<{ repository: Repository }>();

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return "N/A";
    return new Date(dateStr).toLocaleString("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Title Header */}
      <div className="border-b pb-4">
        <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight flex items-center gap-2.5">
          <SettingsIcon className="text-indigo-500 animate-spin-slow" size={28} />
          Workspace Settings
        </h1>
        <p className="text-slate-500 text-sm">
          Overview of database variables, local storage allocations, and parsing status flags.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl">
        {/* Workspace Metadata */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <Info size={16} className="text-indigo-500" />
            Workspace Metadata
          </h3>

          <div className="space-y-3.5 text-xs">
            <div>
              <span className="text-slate-400 font-medium">Workspace ID (UUID)</span>
              <p className="font-mono font-bold text-slate-700 mt-0.5 select-all">{repository?.id || "N/A"}</p>
            </div>
            <div>
              <span className="text-slate-400 font-medium">Repository Name</span>
              <p className="font-semibold text-slate-700 mt-0.5">{repository?.name || "N/A"}</p>
            </div>
            <div>
              <span className="text-slate-400 font-medium">Original File Name</span>
              <p className="font-semibold text-slate-700 mt-0.5">{repository?.original_name || "N/A"}</p>
            </div>
            <div>
              <span className="text-slate-400 font-medium">Initialization Date</span>
              <p className="font-semibold text-slate-700 mt-0.5">{formatDate(repository?.created_at)}</p>
            </div>
          </div>
        </div>

        {/* Directory & Indices */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <FolderGit2 size={16} className="text-emerald-500" />
            Storage & Processing
          </h3>

          <div className="space-y-3.5 text-xs">
            <div>
              <span className="text-slate-400 font-medium">Local Storage Path</span>
              <p className="font-mono text-slate-500 mt-0.5 select-all leading-normal break-all">
                {repository?.storage_path || "N/A"}
              </p>
            </div>
            <div>
              <span className="text-slate-400 font-medium">Analysis Status</span>
              <div className="mt-1">
                {repository?.status === "completed" ? (
                  <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    Completed
                  </span>
                ) : repository?.status === "failed" ? (
                  <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                    Failed
                  </span>
                ) : (
                  <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200 animate-pulse">
                    Indexing
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Vector Indexes */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4 md:col-span-2">
          <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <Database size={16} className="text-amber-500" />
            Chroma Vector Storage Info
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <span className="text-slate-400 font-medium">Local Vector Directory</span>
              <p className="font-mono text-slate-500 mt-0.5">storage/chroma</p>
            </div>
            <div>
              <span className="text-slate-400 font-medium">Collection Name</span>
              <p className="font-mono text-slate-500 mt-0.5">repositories</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;