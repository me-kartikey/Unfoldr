import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles, ArrowLeft, Loader2 } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import {
    RecentUploads,
    UploadButton,
    UploadDropzone,
} from "./components";

import { uploadRepository, getRepositories } from "@/services/repositoryService";

// Edited on 13-08-2026: Add user session greeting and logout triggers in header of the Upload view

interface Repository {
  id: string;
  name: string;
  original_name: string;
  status: string;
  created_at?: string;
}

function Upload() {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [statusMessage, setStatusMessage] = useState("");
    const [repositories, setRepositories] = useState<Repository[]>([]);
    const [isLoadingRepos, setIsLoadingRepos] = useState(true);

    const loadRepositories = async () => {
        try {
            setIsLoadingRepos(true);
            const data = await getRepositories();
            setRepositories(data);
        } catch (error) {
            console.error("Failed to load repositories:", error);
        } finally {
            setIsLoadingRepos(false);
        }
    };

    useEffect(() => {
        loadRepositories();
    }, []);

    const handleAnalyzeRepository = async () => {
        if (!selectedFile) return;

        try {
            setIsUploading(true);
            setStatusMessage("Uploading repository ZIP...");
            
            // Artificial intervals to show progress details since backend runs synchronously
            const timer1 = setTimeout(() => setStatusMessage("Extracting files & folders..."), 2000);
            const timer2 = setTimeout(() => setStatusMessage("Running static analysis & technological detection..."), 5000);
            const timer3 = setTimeout(() => setStatusMessage("Mapping entry points & directory structures..."), 8000);
            const timer4 = setTimeout(() => setStatusMessage("Generating automated documentation & AI vector indexes..."), 12000);

            const repository = await uploadRepository(selectedFile);

            clearTimeout(timer1);
            clearTimeout(timer2);
            clearTimeout(timer3);
            clearTimeout(timer4);

            setStatusMessage("Finalizing analysis...");
            
            // Navigate to overview of the new workspace
            navigate(`/workspace/${repository.id}`);

        } catch (error) {
            console.error("Upload Failed:", error);
            setStatusMessage("Analysis failed. Please make sure the ZIP is valid.");
            setTimeout(() => {
                setIsUploading(false);
                setStatusMessage("");
            }, 3000);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 text-slate-900 pb-16 selection:bg-indigo-500 selection:text-white">
            {/* Header */}
            <header className="border-b bg-white px-6 lg:px-16 py-4 flex items-center justify-between shadow-sm">
                <button
                    onClick={() => navigate("/")}
                    className="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
                >
                    <ArrowLeft size={16} />
                    Back to Home
                </button>
                <div className="flex items-center gap-2">
                    <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center font-bold text-white shadow-md shadow-indigo-500/10">
                        U
                    </div>
                    <span className="text-lg font-bold tracking-tight text-slate-800">
                        Unfoldr
                    </span>
                </div>
                <div className="flex items-center gap-4">
                    {user && (
                        <div className="flex items-center gap-2">
                            <div className="h-7 w-7 rounded-full bg-indigo-50 flex items-center justify-center font-bold text-xs text-indigo-600 border border-indigo-100">
                                {user.username.slice(0, 2).toUpperCase()}
                            </div>
                            <span className="text-xs font-semibold text-slate-500 hidden sm:inline-block">
                                Hello, {user.username}
                            </span>
                        </div>
                    )}
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

            <div className="mx-auto max-w-4xl px-6 mt-12 space-y-10 relative">
                {/* Main Card */}
                <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
                    <div className="mb-8">
                        <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight flex items-center gap-2">
                            <Sparkles className="text-indigo-500" size={24} />
                            Create New Workspace
                        </h1>
                        <p className="mt-2 text-slate-500 text-sm">
                            Upload a compressed ZIP archive of your repository. Unfoldr will scan code layers, detect libraries, extract configuration patterns, and build an AI Q&A assistant index.
                        </p>
                    </div>

                    {isUploading ? (
                        <div className="flex flex-col items-center justify-center py-16 px-4 bg-slate-50 rounded-xl border border-slate-100 animate-pulse text-center">
                            <div className="h-12 w-12 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-500 mb-6">
                                <Loader2 className="animate-spin" size={28} />
                            </div>
                            <h3 className="text-lg font-bold text-slate-800">Analyzing Repository</h3>
                            <p className="text-sm text-slate-500 mt-2 max-w-md">{statusMessage}</p>
                            <div className="mt-8 flex gap-1 justify-center w-32">
                                <div className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: "0ms" }} />
                                <div className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: "150ms" }} />
                                <div className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: "300ms" }} />
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            <UploadDropzone
                                selectedFile={selectedFile}
                                setSelectedFile={setSelectedFile}
                            />

                            <UploadButton
                                disabled={!selectedFile}
                                onClick={handleAnalyzeRepository}
                            />
                        </div>
                    )}
                </div>

                {/* Recent Uploads Section */}
                <RecentUploads 
                    repositories={repositories} 
                    isLoading={isLoadingRepos}
                />
            </div>
        </div>
    );
}

export default Upload;