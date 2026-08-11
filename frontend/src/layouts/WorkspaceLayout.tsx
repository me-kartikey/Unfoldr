import { useState, useEffect } from "react";
import { Outlet, useParams, useNavigate } from "react-router-dom";
import { Loader2, ShieldAlert } from "lucide-react";
import Navbar from "@/components/layout/Navbar/Navbar";
import Sidebar from "@/components/layout/Sidebar/Sidebar";
import { getRepository } from "@/services/repositoryService";

// Edited on 2026-08-11: Added status polling loop and repository analysis progress layouts to WorkspaceLayout.

interface Repository {
  id: string;
  name: string;
  original_name: string;
  status: string;
  created_at?: string;
}

function WorkspaceLayout() {
  const { repositoryId } = useParams<{ repositoryId: string }>();
  const navigate = useNavigate();
  const [repository, setRepository] = useState<Repository | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [secondsElapsed, setSecondsElapsed] = useState(0);

  useEffect(() => {
    let intervalId: any;
    let timerId: any;

    const fetchRepo = async (showLoading: boolean) => {
      if (!repositoryId) return;
      try {
        if (showLoading) setIsLoading(true);
        const data = await getRepository(repositoryId);
        setRepository(data);
        if (showLoading) setIsLoading(false);

        if (data.status === "pending" || data.status === "indexing") {
          // Start timer for progress message changes if not already running
          if (!timerId) {
            timerId = setInterval(() => {
              setSecondsElapsed((prev) => prev + 1);
            }, 1000);
          }

          // Set up polling interval
          if (!intervalId) {
            intervalId = setInterval(async () => {
              try {
                const updatedData = await getRepository(repositoryId);
                setRepository(updatedData);
                if (updatedData.status === "completed" || updatedData.status === "failed") {
                  clearInterval(intervalId);
                  clearInterval(timerId);
                  intervalId = undefined;
                  timerId = undefined;
                }
              } catch (err) {
                console.error("Failed to poll repository status:", err);
              }
            }, 3000);
          }
        }
      } catch (err) {
        console.error("Failed to fetch repository in workspace:", err);
        navigate("/upload");
      }
    };

    fetchRepo(true);

    return () => {
      if (intervalId) clearInterval(intervalId);
      if (timerId) clearInterval(timerId);
    };
  }, [repositoryId, navigate]);

  const getProgressMessage = () => {
    if (secondsElapsed < 8) return "Preparing repository archive & workspace...";
    if (secondsElapsed < 25) return "Running static code analyzers & framework detectors...";
    if (secondsElapsed < 45) return "Analyzing package manager dependencies...";
    if (secondsElapsed < 75) return "Generating automated architectural mappings & documentation...";
    return "Creating AI vector store indexes & finalized references...";
  };

  const isProcessing = repository?.status === "pending" || repository?.status === "indexing";
  const isFailed = repository?.status === "failed";

  return (
    <div className="flex h-screen flex-col bg-slate-50 selection:bg-indigo-500 selection:text-white">
      <Navbar repositoryName={repository?.name || "Loading Workspace..."} />

      <div className="flex flex-1 overflow-hidden">
        {/* Render sidebar only when not processing or failed */}
        {!isProcessing && !isFailed && <Sidebar />}

        <main className="flex-1 overflow-y-auto p-8">
          {isLoading ? (
            <div className="flex h-full w-full flex-col items-center justify-center gap-3 text-slate-400">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
              <p className="text-sm font-medium">Initializing workspace views...</p>
            </div>
          ) : isProcessing ? (
            <div className="flex h-full w-full flex-col items-center justify-center gap-6 p-8 text-center bg-white rounded-2xl border border-slate-200 shadow-sm max-w-2xl mx-auto my-12">
              <div className="h-16 w-16 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-500 mb-2">
                <Loader2 className="animate-spin" size={32} />
              </div>
              <h2 className="text-2xl font-extrabold text-slate-800 tracking-tight">
                Analyzing Repository & Creating Workspace
              </h2>
              <div className="text-sm text-slate-500 max-w-md leading-relaxed">
                <p>We are running our static code analysis, library detection, mapping entry points, and building your AI assistant index. This may take a moment depending on the size of your repository.</p>
              </div>
              <div className="w-full max-w-md bg-slate-100 rounded-full h-2 mt-4 overflow-hidden border">
                <div className="bg-indigo-600 h-2 rounded-full transition-all duration-500 animate-pulse" style={{ width: `${Math.min(10 + secondsElapsed * 1.5, 95)}%` }}></div>
              </div>
              <p className="text-xs text-indigo-600 font-semibold uppercase tracking-wider mt-2 animate-pulse">
                {getProgressMessage()}
              </p>
            </div>
          ) : isFailed ? (
            <div className="flex h-full w-full flex-col items-center justify-center gap-6 p-8 text-center bg-white rounded-2xl border border-rose-100 shadow-sm max-w-2xl mx-auto my-12">
              <div className="h-16 w-16 rounded-2xl bg-rose-50 flex items-center justify-center text-rose-500 mb-2">
                <ShieldAlert size={32} />
              </div>
              <h2 className="text-2xl font-extrabold text-slate-800 tracking-tight text-rose-900">
                Workspace Analysis Failed
              </h2>
              <p className="text-sm text-slate-500 max-w-md leading-relaxed">
                An error occurred during repository extraction or static analyzer processing. Please verify the uploaded archive is a valid ZIP and contains inspectable code.
              </p>
              <button
                onClick={() => navigate("/upload")}
                className="mt-4 px-5 py-2.5 bg-rose-600 text-white rounded-xl text-xs font-semibold hover:bg-rose-700 transition shadow-sm cursor-pointer"
              >
                Back to Upload
              </button>
            </div>
          ) : (
            <Outlet context={{ repository, setRepository }} />
          )}
        </main>
      </div>
    </div>
  );
}

export default WorkspaceLayout;