import { useNavigate } from "react-router-dom";
import { FolderGit2, Home } from "lucide-react";

interface NavbarProps {
  repositoryName: string;
}

function Navbar({ repositoryName }: NavbarProps) {
  const navigate = useNavigate();

  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6 shadow-sm z-10">
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600">
          <FolderGit2 size={18} />
        </div>
        <div>
          <h2 className="text-sm font-bold text-slate-800 tracking-tight">
            {repositoryName}
          </h2>
          <p className="text-[10px] text-slate-400 font-medium tracking-wide uppercase">Active Workspace</p>
        </div>
      </div>

      <button
        onClick={() => navigate("/upload")}
        className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all shadow-sm cursor-pointer"
      >
        <Home size={14} />
        Exit Workspace
      </button>
    </header>
  );
}

export default Navbar;