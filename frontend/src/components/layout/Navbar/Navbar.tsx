import { useNavigate } from "react-router-dom";
import { FolderGit2, Home } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

// Edited on 13-08-2026: Include AuthContext to add user sign-out options and user initials badge inside active Workspace Navbar.

interface NavbarProps {
  repositoryName: string;
}

function Navbar({ repositoryName }: NavbarProps) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

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

      <div className="flex items-center gap-3">
        {user && (
          <div className="flex items-center gap-2 border-r pr-3 border-slate-100">
            <div className="h-7 w-7 rounded-full bg-indigo-50 flex items-center justify-center font-bold text-xs text-indigo-600 border border-indigo-100">
              {user.username.slice(0, 2).toUpperCase()}
            </div>
            <span className="text-xs font-semibold text-slate-500 hidden sm:inline-block">
              {user.username}
            </span>
          </div>
        )}
        <button
          onClick={() => navigate("/upload")}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all shadow-sm cursor-pointer"
        >
          <Home size={14} />
          Exit Workspace
        </button>
        <button
          onClick={async () => {
            await logout();
            navigate("/login");
          }}
          className="px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-red-600 hover:bg-red-50 hover:border-red-100 transition-colors cursor-pointer"
        >
          Sign Out
        </button>
      </div>
    </header>
  );
}

export default Navbar;