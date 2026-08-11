import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { BookOpen, List, ShieldAlert } from "lucide-react";
import { getRepositoryDocumentation } from "@/services/repositoryService";

interface DocHeader {
  id: string;
  text: string;
}

function KnowledgeBase() {
  const { repositoryId } = useParams<{ repositoryId: string }>();
  const [documentation, setDocumentation] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [headers, setHeaders] = useState<DocHeader[]>([]);

  useEffect(() => {
    const fetchDoc = async () => {
      if (!repositoryId) return;
      try {
        setLoading(true);
        setError("");
        const res = await getRepositoryDocumentation(repositoryId);
        setDocumentation(res.documentation);
        
        // Extract headers for table of contents
        const extractedHeaders: DocHeader[] = [];
        res.documentation.split("\n").forEach((line: string) => {
          const trimmed = line.trim();
          if (trimmed.startsWith("## ")) {
            const text = trimmed.replace("## ", "");
            const id = text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
            extractedHeaders.push({ id, text });
          }
        });
        setHeaders(extractedHeaders);
      } catch (err) {
        console.error("Error loading documentation:", err);
        setError("Repository documentation has not been generated or cannot be read.");
      } finally {
        setLoading(false);
      }
    };
    fetchDoc();
  }, [repositoryId]);

  const slugify = (text: string) => {
    return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  };

  const parseMarkdown = (md: string) => {
    const lines = md.split("\n");
    const parsed: React.ReactNode[] = [];
    
    let key = 0;
    let inTable = false;
    let tableHeaders: string[] = [];
    let tableRows: string[][] = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      // Handle Table parsing
      if (line.startsWith("|")) {
        inTable = true;
        const cells = line.split("|").map(c => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
        
        // Skip alignment line like |---|---|
        if (line.includes("---")) {
          continue;
        }
        
        if (tableHeaders.length === 0) {
          tableHeaders = cells;
        } else {
          tableRows.push(cells);
        }
        continue;
      } else {
        // If table ended, render table
        if (inTable && tableHeaders.length > 0) {
          parsed.push(
            <div key={`table-${key++}`} className="my-6 overflow-x-auto rounded-xl border border-slate-200 shadow-sm">
              <table className="min-w-full divide-y divide-slate-200 text-sm">
                <thead className="bg-slate-50">
                  <tr>
                    {tableHeaders.map((h, idx) => (
                      <th key={idx} className="px-4 py-3 text-left font-bold text-slate-700 tracking-wider uppercase text-[11px]">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 bg-white">
                  {tableRows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-slate-50 transition-colors">
                      {row.map((cell, cIdx) => (
                        <td key={cIdx} className="px-4 py-2.5 text-slate-600 font-medium">{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
          inTable = false;
          tableHeaders = [];
          tableRows = [];
        }
      }

      if (line === "") continue;

      if (line.startsWith("# ")) {
        parsed.push(
          <h1 key={key++} className="text-3xl font-extrabold tracking-tight text-slate-800 border-b pb-2 mb-6 mt-4">
            {line.replace("# ", "")}
          </h1>
        );
      } else if (line.startsWith("## ")) {
        const text = line.replace("## ", "");
        const id = slugify(text);
        parsed.push(
          <h2 key={key++} id={id} className="scroll-mt-6 text-xl font-bold text-slate-800 tracking-tight mt-8 mb-4 border-l-4 border-indigo-500 pl-3">
            {text}
          </h2>
        );
      } else if (line.startsWith("- ")) {
        parsed.push(
          <div key={key++} className="flex items-start gap-2.5 my-1 text-slate-600 text-sm pl-2">
            <span className="h-1.5 w-1.5 rounded-full bg-slate-400 mt-2 shrink-0" />
            <span>{line.replace("- ", "")}</span>
          </div>
        );
      } else {
        parsed.push(
          <p key={key++} className="text-sm text-slate-600 leading-relaxed my-3">
            {line}
          </p>
        );
      }
    }

    if (inTable && tableHeaders.length > 0) {
      parsed.push(
        <div key={`table-${key++}`} className="my-6 overflow-x-auto rounded-xl border border-slate-200 shadow-sm">
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-50">
              <tr>
                {tableHeaders.map((h, idx) => (
                  <th key={idx} className="px-4 py-3 text-left font-bold text-slate-700 tracking-wider uppercase text-[11px]">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              {tableRows.map((row, rIdx) => (
                <tr key={rIdx} className="hover:bg-slate-50 transition-colors">
                  {row.map((cell, cIdx) => (
                    <td key={cIdx} className="px-4 py-2.5 text-slate-600 font-medium">{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    return parsed;
  };

  if (loading) {
    return (
      <div className="flex h-64 w-full flex-col items-center justify-center gap-2 text-slate-400">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        <p className="text-sm">Generating knowledge base...</p>
      </div>
    );
  }

  if (error || !documentation) {
    return (
      <div className="rounded-2xl border border-rose-100 bg-rose-50/50 p-6 text-center text-rose-800">
        <ShieldAlert className="mx-auto mb-2 text-rose-500" size={32} />
        <h3 className="font-bold text-sm">Failed to Load Knowledge Base</h3>
        <p className="text-xs mt-1 text-rose-600">{error || "Ensure backend extraction completed successfully."}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in h-[calc(100vh-140px)] flex gap-8">
      {/* Documentation Main Content */}
      <div className="flex-1 overflow-y-auto pr-4 bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
        <div className="flex items-center gap-2.5 border-b pb-4 mb-6">
          <BookOpen className="text-indigo-500" size={24} />
          <h2 className="text-xl font-bold text-slate-800">Project Documentation</h2>
        </div>
        
        <div className="prose max-w-none">
          {parseMarkdown(documentation)}
        </div>
      </div>

      {/* Side Navigation Table of Contents */}
      {headers.length > 0 && (
        <div className="w-64 shrink-0 hidden xl:flex flex-col bg-white rounded-2xl border border-slate-200 p-6 shadow-sm self-start max-h-full overflow-y-auto">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
            <List size={14} />
            On this page
          </h3>
          <nav className="flex flex-col gap-2.5">
            {headers.map((h) => (
              <a
                key={h.id}
                href={`#${h.id}`}
                className="text-xs font-medium text-slate-500 hover:text-indigo-600 hover:underline transition-colors leading-relaxed block"
                onClick={(e) => {
                  e.preventDefault();
                  document.getElementById(h.id)?.scrollIntoView({ behavior: "smooth" });
                }}
              >
                {h.text}
              </a>
            ))}
          </nav>
        </div>
      )}
    </div>
  );
}

export default KnowledgeBase;