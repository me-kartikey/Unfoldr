import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { 
  Folder, 
  FileCode, 
  ChevronRight, 
  FolderOpen, 
  Copy, 
  Check, 
  ShieldAlert, 
  Code,
  Loader2,
  Sparkles
} from "lucide-react";
import { getRepositoryFiles, getFileContent } from "@/services/repositoryService";

// Created on 13-08-2026: RepositoryFiles workspace view with draggable resizable sidebar, custom mouse listeners, and clean text truncation.

// Simple client-side memory cache for file trees by repository ID
const fileTreeCache: Record<string, FileItem> = {};

interface FileItem {
  name: string;
  path: string;
  type: "file" | "dir";
  children?: FileItem[];
}

interface FileNodeProps {
  node: FileItem;
  onFileSelect: (path: string) => void;
  selectedPath: string;
}

function FileNode({ node, onFileSelect, selectedPath }: FileNodeProps) {
  const [isOpen, setIsOpen] = useState(false);
  const isSelected = selectedPath === node.path;

  if (node.type === "file") {
    return (
      <div
        onClick={() => onFileSelect(node.path)}
        className={`flex items-center gap-2 px-2 py-1.5 rounded-lg text-xs cursor-pointer select-none transition-colors min-w-0 ${
          isSelected 
            ? "bg-indigo-50 text-indigo-600 font-semibold border border-indigo-100" 
            : "text-slate-600 hover:bg-slate-100 hover:text-slate-900 border border-transparent"
        }`}
      >
        <FileCode size={14} className={isSelected ? "text-indigo-500" : "text-slate-400"} />
        <span className="truncate">{node.name}</span>
      </div>
    );
  }

  return (
    <div className="space-y-0.5 min-w-0">
      <div
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between px-2 py-1.5 rounded-lg text-xs text-slate-700 hover:bg-slate-50 cursor-pointer select-none font-medium transition-colors min-w-0"
      >
        <div className="flex items-center gap-2 truncate pr-2">
          {isOpen ? (
            <FolderOpen size={14} className="text-indigo-500" />
          ) : (
            <Folder size={14} className="text-slate-400" />
          )}
          <span className="truncate">{node.name}</span>
        </div>
        <ChevronRight size={12} className={`text-slate-400 transition-transform duration-150 shrink-0 ${isOpen ? "rotate-90" : ""}`} />
      </div>

      {isOpen && node.children && (
        <div className="pl-3.5 border-l border-slate-100 ml-3.5 space-y-0.5 min-w-0">
          {node.children.map((child) => (
            <FileNode
              key={child.path}
              node={child}
              onFileSelect={onFileSelect}
              selectedPath={selectedPath}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function RepositoryFiles() {
  const { repositoryId } = useParams<{ repositoryId: string }>();
  const navigate = useNavigate();
  const [fileTree, setFileTree] = useState<FileItem | null>(null);
  const [selectedPath, setSelectedPath] = useState("");
  const [fileContent, setFileContent] = useState("");
  const [loadingTree, setLoadingTree] = useState(true);
  const [loadingContent, setLoadingContent] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");

  // Resizable sidebar states
  const [sidebarWidth, setSidebarWidth] = useState(320);
  const [isResizing, setIsResizing] = useState(false);

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return;
      // Draggable width bounds between 180px and 650px
      setSidebarWidth((prev) => {
        const nextWidth = prev + e.movementX;
        return Math.max(180, Math.min(650, nextWidth));
      });
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    if (isResizing) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
    }

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isResizing]);

  useEffect(() => {
    const fetchTree = async () => {
      if (!repositoryId) return;

      // Edited on 14-08-2026: Cache the file tree inside local client memory to eliminate API latency during tab switching
      if (fileTreeCache[repositoryId]) {
        setFileTree(fileTreeCache[repositoryId]);
        setLoadingTree(false);
        return;
      }

      try {
        setLoadingTree(true);
        setError("");
        const res = await getRepositoryFiles(repositoryId);
        // Save to client cache
        fileTreeCache[repositoryId] = res;
        setFileTree(res);
      } catch (err) {
        console.error("Failed to load file tree:", err);
        setError("Could not read directory structure. Run 'python create_tables.py' and verify ZIP extracts correctly.");
      } finally {
        setLoadingTree(false);
      }
    };
    fetchTree();
  }, [repositoryId]);

  const handleFileSelect = async (path: string) => {
    if (!repositoryId) return;
    try {
      setSelectedPath(path);
      setLoadingContent(true);
      setCopied(false);
      const res = await getFileContent(repositoryId, path);
      setFileContent(res.content);
    } catch (err) {
      console.error("Failed to fetch file content:", err);
      setFileContent("// Failed to read file content from workspace storage.");
    } finally {
      setLoadingContent(false);
    }
  };

  const handleAskAI = () => {
    if (!selectedPath || !repositoryId) return;
    navigate(`/workspace/${repositoryId}/assistant`, {
      state: { initialQuery: `Explain this file completely: ${selectedPath}` }
    });
  };

  const handleCopy = () => {
    if (!fileContent) return;
    navigator.clipboard.writeText(fileContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Split content into rows with line numbers
  const renderCodeLines = () => {
    if (!fileContent) return null;
    const lines = fileContent.split("\n");
    return (
      <div className="flex font-mono text-[11px] leading-relaxed select-text overflow-x-auto w-full">
        {/* Line Numbers Column */}
        <div className="text-right select-none text-slate-300 pr-4 pl-2 bg-slate-50/50 border-r border-slate-100 shrink-0 sticky left-0 z-10">
          {lines.map((_, idx) => (
            <div key={idx}>{idx + 1}</div>
          ))}
        </div>
        {/* Code Content Column */}
        <pre className="pl-4 text-slate-700 whitespace-pre">
          {lines.map((line, idx) => (
            <div key={idx}>{line || " "}</div>
          ))}
        </pre>
      </div>
    );
  };

  if (loadingTree) {
    return (
      <div className="flex h-64 w-full flex-col items-center justify-center gap-2 text-slate-400">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        <p className="text-sm">Reading repository file system...</p>
      </div>
    );
  }

  if (error || !fileTree) {
    return (
      <div className="rounded-2xl border border-rose-100 bg-rose-50/50 p-6 text-center text-rose-800">
        <ShieldAlert className="mx-auto mb-2 text-rose-500" size={32} />
        <h3 className="font-bold text-sm">Failed to Load Repository Files</h3>
        <p className="text-xs mt-1 text-rose-600">{error || "Data is missing or incomplete."}</p>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-140px)] flex bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden animate-fade-in select-none">
      {/* Left Pane - File Explorer Tree with Resizable Width */}
      <div 
        className="shrink-0 flex flex-col border-r border-slate-200" 
        style={{ width: `${sidebarWidth}px` }}
      >
        <div className="px-4 py-3 border-b bg-slate-50/50 shrink-0">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-2">
            <Code size={14} className="text-indigo-500" />
            File Explorer
          </h3>
        </div>
        <div className="flex-1 overflow-y-auto overflow-x-hidden p-4 space-y-1">
          {fileTree.children && fileTree.children.map((child) => (
            <FileNode
              key={child.path}
              node={child}
              onFileSelect={handleFileSelect}
              selectedPath={selectedPath}
            />
          ))}
        </div>
      </div>

      {/* Draggable Divider resizer handle bar */}
      <div 
        onMouseDown={handleMouseDown}
        className={`w-1 hover:w-1.5 active:w-1.5 bg-slate-100 hover:bg-indigo-500 active:bg-indigo-600 transition-all cursor-col-resize h-full shrink-0 relative z-20 ${
          isResizing ? "bg-indigo-500 w-1.5" : ""
        }`}
      />

      {/* Right Pane - Code Viewer */}
      <div className="flex-1 flex flex-col min-w-0 bg-slate-50/20">
        {selectedPath ? (
          <div className="h-full flex flex-col">
            {/* Header controls */}
            <div className="px-6 py-3 border-b bg-white flex items-center justify-between shadow-sm z-10">
              <div className="min-w-0 pr-4">
                <span className="text-[10px] font-bold text-indigo-500 uppercase tracking-wide">Inspecting File</span>
                <h4 className="text-xs font-mono font-bold text-slate-800 truncate mt-0.5">{selectedPath}</h4>
              </div>
              
              <div className="flex items-center gap-2">
                <button
                  onClick={handleAskAI}
                  disabled={loadingContent}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-indigo-200 bg-indigo-50 hover:bg-indigo-100 text-[10px] font-bold text-indigo-600 transition cursor-pointer shrink-0"
                >
                  <Sparkles size={12} className="animate-pulse" />
                  <span>Ask AI</span>
                </button>
                <button
                  onClick={handleCopy}
                  disabled={loadingContent}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-[10px] font-bold text-slate-600 hover:text-slate-900 transition cursor-pointer shrink-0"
                >
                {copied ? (
                  <>
                    <Check size={12} className="text-emerald-500" />
                    <span className="text-emerald-600">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy size={12} />
                    <span>Copy Code</span>
                  </>
                )}
              </button>
              </div>
            </div>

            {/* Code Content */}
            <div className="flex-1 overflow-y-auto p-6 bg-slate-50/30 select-text">
              {loadingContent ? (
                <div className="flex h-full w-full flex-col items-center justify-center gap-2 text-slate-400">
                  <Loader2 className="animate-spin text-indigo-500" size={24} />
                  <p className="text-xs font-semibold">Reading storage block...</p>
                </div>
              ) : (
                <div className="bg-white rounded-xl border border-slate-200/60 p-4 shadow-sm h-full overflow-y-auto max-w-none">
                  {renderCodeLines()}
                </div>
              )}
            </div>
          </div>
        ) : (
          /* Empty placeholder */
          <div className="h-full flex flex-col items-center justify-center text-center p-8 select-none">
            <div className="h-16 w-16 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-500 mb-4 shadow-sm border border-indigo-100">
              <Code size={28} />
            </div>
            <h3 className="text-sm font-bold text-slate-800">Preview Source Code</h3>
            <p className="text-xs text-slate-400 mt-1 max-w-xs leading-relaxed">
              Navigate through the file structure on the left side pane and select a file to view its content and code line mapping.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default RepositoryFiles;
