import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { 
  Network, 
  Terminal, 
  Settings, 
  Database, 
  ShieldAlert, 
  Hammer, 
  GitBranch,
  Layers
} from "lucide-react";
import { getRepositoryArchitecture, getRepositoryDependencies } from "@/services/repositoryService";

interface ArchitectureData {
  project_type: string;
  backend_framework: string;
  frontend_framework: string;
  architecture_pattern: string;
  entry_points: string[];
  root_folders: string[];
  config_files: string[];
  databases: string[];
  orms: string[];
  authentication_methods: string[];
  api_styles: string[];
  devops_tools: string[];
  cicd_tools: string[];
  testing_frameworks: string[];
  code_quality_tools: string[];
  environment_files: string[];
  deployment_platforms: string[];
  repository_characteristics: string[];
}

interface Dependency {
  id: string;
  name: string;
  version: string | null;
  language: string;
  package_manager: string;
  dependency_type: string;
}

function Architecture() {
  const { repositoryId } = useParams<{ repositoryId: string }>();
  const [architecture, setArchitecture] = useState<ArchitectureData | null>(null);
  const [dependencies, setDependencies] = useState<Dependency[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState<"architecture" | "dependencies">("architecture");

  useEffect(() => {
    const fetchData = async () => {
      if (!repositoryId) return;
      try {
        setLoading(true);
        setError("");
        const [archRes, depRes] = await Promise.all([
          getRepositoryArchitecture(repositoryId),
          getRepositoryDependencies(repositoryId)
        ]);
        setArchitecture(archRes);
        setDependencies(depRes);
      } catch (err) {
        console.error("Error loading architecture metrics:", err);
        setError("Failed to fetch architecture metadata.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [repositoryId]);

  if (loading) {
    return (
      <div className="flex h-64 w-full flex-col items-center justify-center gap-2 text-slate-400">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        <p className="text-sm">Assembling architecture map...</p>
      </div>
    );
  }

  if (error || !architecture) {
    return (
      <div className="rounded-2xl border border-rose-100 bg-rose-50/50 p-6 text-center text-rose-800">
        <ShieldAlert className="mx-auto mb-2 text-rose-500" size={32} />
        <h3 className="font-bold text-sm">Failed to Load Architecture</h3>
        <p className="text-xs mt-1 text-rose-600">{error || "Ensure scan results are populated in Postgres."}</p>
      </div>
    );
  }

  const renderBadgeList = (items?: string[], fallback = "None detected") => {
    if (!items || items.length === 0) return <span className="text-xs text-slate-400 italic">{fallback}</span>;
    return (
      <div className="flex flex-wrap gap-1.5 mt-1.5">
        {items.map((item) => (
          <span
            key={item}
            className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-indigo-50 text-indigo-600 border border-indigo-100"
          >
            {item}
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Title Header */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between border-b pb-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight flex items-center gap-2.5">
            <Network className="text-indigo-500" size={28} />
            System Architecture
          </h1>
          <p className="text-slate-500 text-sm">
            Discovered project layers, modules, configuration paths, and package manifests.
          </p>
        </div>

        {/* Tab Toggle */}
        <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200">
          <button
            onClick={() => setActiveTab("architecture")}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
              activeTab === "architecture" ? "bg-white text-indigo-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Architecture Tiers
          </button>
          <button
            onClick={() => setActiveTab("dependencies")}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
              activeTab === "dependencies" ? "bg-white text-indigo-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Dependencies ({dependencies.length})
          </button>
        </div>
      </div>

      {activeTab === "architecture" ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Info Columns */}
          <div className="lg:col-span-2 space-y-6">
            {/* Core Blueprint Card */}
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-base font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Layers size={16} className="text-indigo-500" />
                Repository Blueprint
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="p-4 rounded-xl bg-slate-50/50 border border-slate-100">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Project Type</span>
                  <span className="text-sm font-semibold text-slate-800 block mt-1 capitalize">{architecture.project_type}</span>
                </div>

                <div className="p-4 rounded-xl bg-slate-50/50 border border-slate-100">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Architecture Pattern</span>
                  <span className="text-sm font-semibold text-slate-800 block mt-1 capitalize">{architecture.architecture_pattern || "Standard Layout"}</span>
                </div>

                <div className="p-4 rounded-xl bg-slate-50/50 border border-slate-100">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Backend Framework</span>
                  <span className="text-sm font-semibold text-slate-800 block mt-1">{architecture.backend_framework}</span>
                </div>

                <div className="p-4 rounded-xl bg-slate-50/50 border border-slate-100">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Frontend Framework</span>
                  <span className="text-sm font-semibold text-slate-800 block mt-1">{architecture.frontend_framework}</span>
                </div>
              </div>
            </div>

            {/* Grid Components */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Database & ORMs */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <Database size={16} className="text-emerald-500" />
                  Database Configuration
                </h4>
                <div className="space-y-3">
                  <div>
                    <span className="text-xs text-slate-400">Database Engine</span>
                    {renderBadgeList(architecture.databases, "No Database file detected")}
                  </div>
                  <div>
                    <span className="text-xs text-slate-400">Object Relational Mapper (ORM)</span>
                    {renderBadgeList(architecture.orms, "No ORM file detected")}
                  </div>
                </div>
              </div>

              {/* Devops & Deployments */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <Settings size={16} className="text-amber-500" />
                  DevOps & Deployments
                </h4>
                <div className="space-y-3">
                  <div>
                    <span className="text-xs text-slate-400">DevOps Tooling</span>
                    {renderBadgeList(architecture.devops_tools, "No docker/container file found")}
                  </div>
                  <div>
                    <span className="text-xs text-slate-400">CI/CD Platforms</span>
                    {renderBadgeList(architecture.cicd_tools, "No build manifest found")}
                  </div>
                </div>
              </div>

              {/* Entry Points */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <Terminal size={16} className="text-indigo-500" />
                  Discovered Entry Points
                </h4>
                <div className="space-y-1 max-h-40 overflow-y-auto pr-2">
                  {architecture.entry_points?.map((entry) => (
                    <div key={entry} className="text-xs font-mono py-1 border-b border-slate-50 text-slate-600 last:border-0 truncate">
                      {entry}
                    </div>
                  )) || <span className="text-xs text-slate-400 italic">No entry files detected</span>}
                </div>
              </div>

              {/* Testing & Code Quality */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <Hammer size={16} className="text-rose-500" />
                  Testing & Quality
                </h4>
                <div className="space-y-3">
                  <div>
                    <span className="text-xs text-slate-400">Testing Tools</span>
                    {renderBadgeList(architecture.testing_frameworks, "No tests detected")}
                  </div>
                  <div>
                    <span className="text-xs text-slate-400">Code Quality Tools</span>
                    {renderBadgeList(architecture.code_quality_tools, "No linters configured")}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column Layout */}
          <div className="space-y-6">
            {/* Configuration Files */}
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                <GitBranch size={14} />
                Global Configurations
              </h4>
              <div className="space-y-2">
                {architecture.config_files?.map((cfg) => (
                  <div key={cfg} className="flex items-center gap-2 p-2 rounded-lg bg-slate-50 text-xs font-semibold text-slate-600 border border-slate-100 truncate">
                    <span className="h-1.5 w-1.5 rounded-full bg-slate-400" />
                    {cfg}
                  </div>
                )) || <span className="text-xs text-slate-400 italic">No configuration found</span>}
              </div>
            </div>

            {/* Authentication and APIs */}
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
              <div>
                <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Authentication Layer</h5>
                {renderBadgeList(architecture.authentication_methods, "Standard authentication")}
              </div>
              <div>
                <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">API Design Pattern</h5>
                {renderBadgeList(architecture.api_styles, "Standard REST endpoints")}
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Dependencies Tab */
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden animate-fade-in">
          {dependencies.length === 0 ? (
            <div className="p-12 text-center text-slate-400">
              <p className="text-sm font-semibold">No external package dependencies detected.</p>
              <p className="text-xs mt-1">Make sure package.json or requirements.txt files exist.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 text-sm">
                <thead className="bg-slate-50">
                  <tr>
                    <th className="px-6 py-4 text-left font-bold text-slate-500 uppercase tracking-wider text-[11px]">Dependency</th>
                    <th className="px-6 py-4 text-left font-bold text-slate-500 uppercase tracking-wider text-[11px]">Version</th>
                    <th className="px-6 py-4 text-left font-bold text-slate-500 uppercase tracking-wider text-[11px]">Language</th>
                    <th className="px-6 py-4 text-left font-bold text-slate-500 uppercase tracking-wider text-[11px]">Package Manager</th>
                    <th className="px-6 py-4 text-left font-bold text-slate-500 uppercase tracking-wider text-[11px]">Type</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 bg-white">
                  {dependencies.map((dep) => (
                    <tr key={dep.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-3.5 font-bold text-slate-800 text-xs">{dep.name}</td>
                      <td className="px-6 py-3.5 text-slate-600 text-xs font-semibold">{dep.version || "-"}</td>
                      <td className="px-6 py-3.5 text-xs text-slate-500 font-medium">
                        <span className="px-2 py-0.5 rounded bg-slate-50 text-slate-600 border border-slate-100">
                          {dep.language}
                        </span>
                      </td>
                      <td className="px-6 py-3.5 text-xs text-slate-500 font-mono font-medium uppercase">{dep.package_manager}</td>
                      <td className="px-6 py-3.5 text-xs font-semibold">
                        <span className={`px-2 py-0.5 rounded-full text-[10px] ${
                          dep.dependency_type === "development" 
                            ? "bg-slate-100 text-slate-500" 
                            : "bg-indigo-50 text-indigo-600 border border-indigo-100"
                        }`}>
                          {dep.dependency_type}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Architecture;