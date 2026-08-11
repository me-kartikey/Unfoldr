import { useNavigate } from "react-router-dom";
import { FolderGit2, Calendar, CheckCircle2, Clock } from "lucide-react";

interface Repository {
  id: string;
  name: string;
  original_name: string;
  status: string;
  created_at?: string;
}

interface RecentUploadsProps {
  repositories: Repository[];
  isLoading: boolean;
}

function RecentUploads({ repositories, isLoading }: RecentUploadsProps) {
  const navigate = useNavigate();

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return "Unknown date";
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    } catch {
      return "Unknown date";
    }
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-6 text-xl font-bold text-slate-800 flex items-center gap-2">
        <FolderGit2 className="text-indigo-500" size={22} />
        Recent Workspaces
      </h2>

      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-12 gap-3 text-slate-400">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
          <p className="text-sm">Loading workspaces...</p>
        </div>
      ) : repositories.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center text-slate-400 border-2 border-dashed border-slate-100 rounded-xl">
          <FolderGit2 className="mb-3 text-slate-300" size={40} />
          <p className="text-sm font-medium">No repositories analyzed yet.</p>
          <p className="text-xs mt-1 text-slate-400">Upload a project ZIP above to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {repositories.map((repo) => (
            <div
              key={repo.id}
              onClick={() => navigate(`/workspace/${repo.id}`)}
              className="group cursor-pointer rounded-xl border border-slate-100 bg-slate-50/50 p-4 transition-all hover:bg-white hover:border-slate-300 hover:shadow-md hover:shadow-slate-100 flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-500 group-hover:bg-indigo-500 group-hover:text-white transition-colors">
                  <FolderGit2 size={20} />
                </div>
                <div>
                  <h4 className="font-semibold text-slate-800 text-sm group-hover:text-indigo-600 transition-colors">
                    {repo.name}
                  </h4>
                  <div className="flex items-center gap-2 mt-1 text-xs text-slate-400">
                    <Calendar size={12} />
                    <span>{formatDate(repo.created_at)}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2">
                {repo.status === "completed" ? (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <CheckCircle2 size={12} />
                    Ready
                  </span>
                ) : repo.status === "failed" ? (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200">
                    Failed
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200 animate-pulse">
                    <Clock size={12} />
                    Analyzing
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RecentUploads;