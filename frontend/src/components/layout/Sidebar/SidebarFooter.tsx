import { FolderGit2 } from "lucide-react";

function SidebarFooter() {
  return (
    <div className="border-t p-4">
      <div className="flex items-center gap-3 rounded-lg border p-3">
        <FolderGit2 className="h-5 w-5 text-slate-500" />

        <div>
          <p className="text-xs text-slate-500">
            Repository
          </p>

          <p className="font-medium">
            Demo Repository
          </p>
        </div>
      </div>
    </div>
  );
}

export default SidebarFooter;