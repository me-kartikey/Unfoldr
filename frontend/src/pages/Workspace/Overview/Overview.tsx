import { useState, useEffect } from "react";
import { useParams, useNavigate, useOutletContext } from "react-router-dom";
import { 
  FileCode2, 
  Code2, 
  Database, 
  BookOpen, 
  Cpu, 
  ArrowRight, 
  Clock, 
  ShieldAlert,
  HardDrive
} from "lucide-react";
import { getRepositoryAnalysis, getRepositoryArchitecture } from "@/services/repositoryService";

interface Repository {
  id: string;
  name: string;
  original_name: string;
  status: string;
  created_at?: string;
}

interface AnalysisData {
  total_files: number;
  languages: string[];
  frameworks: string[];
  libraries: string[];
  extensions: string[];
}

interface ArchitectureData {
  project_type: string;
  backend_framework: string;
  frontend_framework: string;
  architecture_pattern: string;
  databases: string[];
  orms: string[];
  entry_points: string[];
}

function Overview() {
  const { repositoryId } = useParams<{ repositoryId: string }>();
  const navigate = useNavigate();
  const { repository } = useOutletContext<{ repository: Repository }>();

  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [architecture, setArchitecture] = useState<ArchitectureData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchOverviewData = async () => {
      if (!repositoryId) return;
      try {
        setLoading(true);
        setError("");
        const [analysisRes, archRes] = await Promise.all([
          getRepositoryAnalysis(repositoryId),
          getRepositoryArchitecture(repositoryId)
        ]);
        setAnalysis(analysisRes);
        setArchitecture(archRes);
      } catch (err) {
        console.error("Error fetching overview metrics:", err);
        setError("Failed to load repository metrics. Run 'python create_tables.py' and verify scans completed.");
      } finally {
        setLoading(false);
      }
    };

    fetchOverviewData();
  }, [repositoryId]);

  if (loading) {
    return (
      <div className="flex h-64 w-full flex-col items-center justify-center gap-2 text-slate-400">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        <p className="text-sm">Fetching metrics and stats...</p>
      </div>
    );
  }

  if (error || !analysis || !architecture) {
    return (
      <div className="rounded-2xl border border-rose-100 bg-rose-50/50 p-6 text-center text-rose-800">
        <ShieldAlert className="mx-auto mb-2 text-rose-500" size={32} />
        <h3 className="font-bold text-sm">Failed to Load Dashboard</h3>
        <p className="text-xs mt-1 max-w-md mx-auto text-rose-600">{error || "Data is missing or incomplete."}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-rose-600 text-white rounded-lg text-xs font-semibold hover:bg-rose-700 transition shadow-sm cursor-pointer"
        >
          Retry
        </button>
      </div>
    );
  }

  // Format creation timestamp
  const formatDate = (dateStr?: string) => {
    if (!dateStr) return "Just now";
    return new Date(dateStr).toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Title Header */}
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">
            Repository Overview
          </h1>
          <p className="text-slate-500 text-sm">
            Analysis insights for <span className="font-semibold text-slate-700">{repository?.original_name}</span>.
          </p>
        </div>

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl border border-indigo-100 bg-indigo-50/30 text-indigo-700 text-xs font-semibold shadow-sm shadow-indigo-100/10">
          <Clock size={14} />
          <span>Analyzed on {formatDate(repository?.created_at)}</span>
        </div>
      </div>

      {/* Stats Cards Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {/* Primary Language */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-center gap-4">
          <div className="h-12 w-12 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-500">
            <Code2 size={24} />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Primary Language</p>
            <p className="text-xl font-bold text-slate-800 mt-0.5">
              {(() => {
                const langs = analysis.languages || [];
                const codeLangs = langs.filter(
                  l => !["Markdown", "JSON", "YAML", "HTML", "CSS", "XML"].includes(l)
                );
                return codeLangs[0] || langs[0] || "Unknown";
              })()}
            </p>
          </div>
        </div>

        {/* Framework */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-center gap-4">
          <div className="h-12 w-12 rounded-xl bg-violet-50 flex items-center justify-center text-violet-500">
            <Cpu size={24} />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Framework</p>
            <p className="text-xl font-bold text-slate-800 mt-0.5">
              {architecture.backend_framework || architecture.frontend_framework || "Vanilla"}
            </p>
          </div>
        </div>

        {/* Total Files */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-center gap-4">
          <div className="h-12 w-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-500">
            <FileCode2 size={24} />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Files</p>
            <p className="text-xl font-bold text-slate-800 mt-0.5">
              {analysis.total_files}
            </p>
          </div>
        </div>

        {/* Databases */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-center gap-4">
          <div className="h-12 w-12 rounded-xl bg-amber-50 flex items-center justify-center text-amber-500">
            <Database size={24} />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Database</p>
            <p className="text-xl font-bold text-slate-800 mt-0.5">
              {architecture.databases?.[0] || "None"}
            </p>
          </div>
        </div>
      </div>

      {/* Info Details Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Workspace Info */}
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
              <HardDrive size={18} className="text-indigo-500" />
              Technology Stack
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-sm">
              <div className="space-y-3">
                <div>
                  <span className="text-slate-400 font-medium">Project Type</span>
                  <p className="font-semibold text-slate-700 mt-0.5 capitalize">{architecture.project_type}</p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Architecture Pattern</span>
                  <p className="font-semibold text-slate-700 mt-0.5">{architecture.architecture_pattern || "N/A"}</p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Detected Languages</span>
                  <div className="flex flex-wrap gap-1.5 mt-1.5">
                    {analysis.languages?.map((lang) => (
                      <span key={lang} className="px-2 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
                        {lang}
                      </span>
                    )) || <span className="text-xs text-slate-400">None</span>}
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <span className="text-slate-400 font-medium">Backend Server</span>
                  <p className="font-semibold text-slate-700 mt-0.5">{architecture.backend_framework || "N/A"}</p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Frontend Framework</span>
                  <p className="font-semibold text-slate-700 mt-0.5">{architecture.frontend_framework || "N/A"}</p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Frameworks Detected</span>
                  <div className="flex flex-wrap gap-1.5 mt-1.5">
                    {analysis.frameworks?.map((fw) => (
                      <span key={fw} className="px-2 py-0.5 rounded-md text-xs font-medium bg-violet-50 text-violet-600 border border-violet-100">
                        {fw}
                      </span>
                    )) || <span className="text-xs text-slate-400">None</span>}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Info Summary */}
          <div className="rounded-2xl border border-indigo-100 bg-indigo-50/10 p-6">
            <h4 className="text-sm font-bold text-indigo-900 uppercase tracking-wider mb-2">Automated Codebase Description</h4>
            <p className="text-slate-600 text-sm leading-relaxed">
              This repository represents a {architecture.project_type} application utilizing {analysis.languages?.join(", ")}. 
              The codebase leverages {architecture.backend_framework || "native standard models"} as the primary architecture engine 
              and depends on {analysis.libraries?.slice(0, 5).join(", ") || "various helper components"} to handle modules and operational dependencies.
            </p>
          </div>
        </div>

        {/* Quick Navigation Panel */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
            <BookOpen size={18} className="text-indigo-500" />
            Quick Actions
          </h3>
          <p className="text-xs text-slate-400">Jump directly to workspace pages to understand code structures.</p>
          
          <div className="space-y-2 mt-4">
            <button
              onClick={() => navigate(`/workspace/${repositoryId}/knowledge-base`)}
              className="w-full flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50 hover:bg-indigo-50/30 hover:border-indigo-100 group transition text-left cursor-pointer"
            >
              <div>
                <p className="text-xs font-bold text-slate-700 group-hover:text-indigo-600 transition-colors">Knowledge Base</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Read auto-generated manuals</p>
              </div>
              <ArrowRight size={14} className="text-slate-400 group-hover:text-indigo-500 transition" />
            </button>

            <button
              onClick={() => navigate(`/workspace/${repositoryId}/architecture`)}
              className="w-full flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50 hover:bg-indigo-50/30 hover:border-indigo-100 group transition text-left cursor-pointer"
            >
              <div>
                <p className="text-xs font-bold text-slate-700 group-hover:text-indigo-600 transition-colors">Architecture</p>
                <p className="text-[10px] text-slate-400 mt-0.5">View database systems & ORMs</p>
              </div>
              <ArrowRight size={14} className="text-slate-400 group-hover:text-indigo-500 transition animate-pulse" />
            </button>

            <button
              onClick={() => navigate(`/workspace/${repositoryId}/assistant`)}
              className="w-full flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50 hover:bg-indigo-50/30 hover:border-indigo-100 group transition text-left cursor-pointer"
            >
              <div>
                <p className="text-xs font-bold text-slate-700 group-hover:text-indigo-600 transition-colors">Developer Assistant</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Chat with Gemini AI about code</p>
              </div>
              <ArrowRight size={14} className="text-slate-400 group-hover:text-indigo-500 transition" />
            </button>

            <button
              onClick={() => navigate(`/workspace/${repositoryId}/files`)}
              className="w-full flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50 hover:bg-indigo-50/30 hover:border-indigo-100 group transition text-left cursor-pointer"
            >
              <div>
                <p className="text-xs font-bold text-slate-700 group-hover:text-indigo-600 transition-colors">Repository Files</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Explore structure & read files</p>
              </div>
              <ArrowRight size={14} className="text-slate-400 group-hover:text-indigo-500 transition" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Overview;