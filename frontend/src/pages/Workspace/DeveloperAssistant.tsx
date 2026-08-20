import { useState, useRef, useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import { Bot, Send, User, Sparkles, Loader2, BookOpen, AlertCircle, FileCode, X, Trash2 } from "lucide-react";
import { askQuestion } from "@/services/repositoryService";

interface Message {
  id: string;
  sender: "user" | "ai";
  text: string;
  sources?: string[];
  timestamp: Date;
}

function DeveloperAssistant() {
  const { repositoryId } = useParams<{ repositoryId: string }>();
  const location = useLocation();
  // Load initial chat history from sessionStorage for this repository
  const storageKey = repositoryId ? `unfoldr_chat_${repositoryId}` : null;

  const [messages, setMessages] = useState<Message[]>(() => {
    if (storageKey) {
      const saved = sessionStorage.getItem(storageKey);
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          return parsed.map((m: any) => ({ ...m, timestamp: new Date(m.timestamp) }));
        } catch (e) {
          console.error("Failed to parse saved chat history:", e);
        }
      }
    }
    return [
      {
        id: "welcome",
        sender: "ai",
        text: "Hello! I am your AI Developer Onboarding Assistant. Ask me anything about the repository files, project structure, technologies used, database schemas, or installation requirements.",
        timestamp: new Date()
      }
    ];
  });

  const [inputValue, setInputValue] = useState("");
  const [fileContext, setFileContext] = useState<string | null>(location.state?.fileContext || null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const chatEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Persist chat history to sessionStorage whenever messages change
  useEffect(() => {
    if (storageKey && messages.length > 0) {
      sessionStorage.setItem(storageKey, JSON.stringify(messages));
    }
  }, [messages, storageKey]);

  const handleClearHistory = () => {
    if (storageKey) {
      sessionStorage.removeItem(storageKey);
    }
    setMessages([
      {
        id: "welcome",
        sender: "ai",
        text: "Hello! I am your AI Developer Onboarding Assistant. Ask me anything about the repository files, project structure, technologies used, database schemas, or installation requirements.",
        timestamp: new Date()
      }
    ]);
  };

  // Keep cursor focused in input box whenever AI finishes loading
  useEffect(() => {
    if (!isLoading) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 50);
    }
  }, [isLoading]);

  // Read fileContext from navigation state without auto-sending any question
  useEffect(() => {
    if (location.state?.fileContext) {
      setFileContext(location.state.fileContext);
      window.history.replaceState({}, document.title);
    }
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  }, [location.state]);

  const handleSend = async (textToSend: string) => {
    const text = textToSend.trim();
    if (!text || !repositoryId) return;

    // Combine user text with file context reference if active
    const queryForAi = fileContext ? `[File Reference: ${fileContext}] ${text}` : text;

    // Add user message to UI
    const userMsg: Message = {
      id: `msg-${Date.now()}-user`,
      sender: "user",
      text: fileContext ? `[Ref: ${fileContext}]\n${text}` : text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMsg]);
    setInputValue("");
    setError("");
    setIsLoading(true);

    try {
      const response = await askQuestion(repositoryId, queryForAi);
      
      const aiMsg: Message = {
        id: `msg-${Date.now()}-ai`,
        sender: "ai",
        text: response.answer,
        sources: response.sources || [],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error("AI Assistant query failed:", err);
      setError("I failed to connect with the AI model. Ensure Uvicorn is running and your GOOGLE_API_KEY is configured.");
    } finally {
      setIsLoading(false);
    }
  };

  const suggestedQuestions = [
    "What technologies and frameworks are used in this codebase?",
    "Explain the folder structure and entry points.",
    "What databases and ORMs are configured?",
    "How do I set up and run this application?"
  ];

  // Helper to format assistant answers with bold, lists, and linebreaks
  const formatText = (text: string) => {
    return text.split("\n").map((line, i) => {
      const trimmed = line.trim();
      if (trimmed === "") return <div key={i} className="h-2" />;
      
      // Headers
      if (trimmed.startsWith("### ")) {
        return <h4 key={i} className="font-bold text-slate-800 mt-3 mb-1 text-sm">{trimmed.replace("### ", "")}</h4>;
      }
      if (trimmed.startsWith("## ")) {
        return <h3 key={i} className="font-bold text-slate-800 mt-4 mb-1.5 text-base">{trimmed.replace("## ", "")}</h3>;
      }
      
      // Bullets
      if (trimmed.startsWith("* ") || trimmed.startsWith("- ")) {
        return (
          <div key={i} className="flex items-start gap-2 text-xs text-slate-600 my-0.5 pl-2 leading-relaxed">
            <span className="h-1 w-1 rounded-full bg-slate-400 mt-1.5 shrink-0" />
            <span>{trimmed.replace(/^(\*\s|-\s)/, "")}</span>
          </div>
        );
      }
      
      // Numbered lists
      if (/^\d+\.\s/.test(trimmed)) {
        return (
          <div key={i} className="text-xs text-slate-600 my-0.5 pl-2 leading-relaxed font-semibold">
            {trimmed}
          </div>
        );
      }

      // Check inline code backticks or bold
      return (
        <p key={i} className="text-xs text-slate-600 leading-relaxed my-1">
          {trimmed.split(" ").map((word, idx) => {
            if (word.startsWith("`") && word.endsWith("`")) {
              return <code key={idx} className="bg-slate-100 px-1 py-0.5 rounded text-[11px] font-mono text-indigo-600">{word.replace(/`/g, "")} </code>;
            }
            if (word.startsWith("**") && word.endsWith("**")) {
              return <strong key={idx} className="font-bold text-slate-800">{word.replace(/\*\*/g, "")} </strong>;
            }
            return word + " ";
          })}
        </p>
      );
    });
  };

  return (
    <div className="h-[calc(100vh-140px)] flex flex-col bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden animate-fade-in">
      {/* Top Banner */}
      <div className="px-6 py-4 border-b flex items-center justify-between bg-slate-50/50">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600">
            <Bot size={22} />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-800 tracking-tight flex items-center gap-2">
              Gemini Repository Agent
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[9px] font-bold bg-indigo-100 text-indigo-700">
                <Sparkles size={8} />
                RAG Active
              </span>
            </h2>
            <p className="text-[10px] text-slate-400 font-semibold tracking-wide">Ready to answers codebase queries</p>
          </div>
        </div>

        {messages.length > 1 && (
          <button
            onClick={handleClearHistory}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-rose-50 hover:border-rose-200 text-[10px] font-bold text-slate-500 hover:text-rose-600 transition cursor-pointer"
            title="Clear Chat History"
          >
            <Trash2 size={12} />
            <span>Clear Chat</span>
          </button>
        )}
      </div>

      {/* Message History Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-50/20">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 max-w-[80%] ${
              msg.sender === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            }`}
          >
            {/* Avatar */}
            <div className={`h-8 w-8 rounded-lg flex items-center justify-center shrink-0 shadow-sm ${
              msg.sender === "user" ? "bg-indigo-600 text-white" : "bg-white text-indigo-600 border border-slate-100"
            }`}>
              {msg.sender === "user" ? <User size={14} /> : <Bot size={14} />}
            </div>

            {/* Text Bubble */}
            <div className="space-y-1.5">
              <div className={`rounded-2xl p-4 text-slate-700 text-xs shadow-sm ${
                msg.sender === "user" 
                  ? "bg-indigo-600 text-white rounded-tr-none font-medium" 
                  : "bg-white border border-slate-100 rounded-tl-none"
              }`}>
                {msg.sender === "user" ? (
                  <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                ) : (
                  <div className="space-y-1">{formatText(msg.text)}</div>
                )}
              </div>

              {/* RAG Sources Display */}
              {msg.sender === "ai" && msg.sources && msg.sources.length > 0 && (
                <div className="flex flex-wrap items-center gap-1.5 pl-1.5 text-[9px] text-slate-400 font-medium">
                  <BookOpen size={10} />
                  <span>Referenced:</span>
                  {msg.sources.map((src) => (
                    <span key={src} className="px-1.5 py-0.5 rounded bg-slate-100 text-slate-500 font-bold border border-slate-200/50">
                      {src}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex gap-3 max-w-[80%] mr-auto items-center">
            <div className="h-8 w-8 rounded-lg bg-white border border-slate-100 text-indigo-600 flex items-center justify-center shadow-sm">
              <Bot size={14} />
            </div>
            <div className="rounded-2xl p-4 bg-white border border-slate-100 rounded-tl-none flex items-center gap-2 shadow-sm text-slate-400 text-xs">
              <Loader2 className="animate-spin text-indigo-500" size={14} />
              <span>Gemini is reading documentation context...</span>
            </div>
          </div>
        )}

        {/* Error Notification */}
        {error && (
          <div className="flex gap-2 max-w-lg mx-auto p-4 rounded-xl border border-rose-100 bg-rose-50 text-rose-800 text-xs items-center shadow-sm">
            <AlertCircle className="text-rose-500 shrink-0" size={16} />
            <p className="font-semibold">{error}</p>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Suggested Questions & Typing Inputs */}
      <div className="p-4 border-t bg-white space-y-4">
        {/* Suggested Prompt Chips */}
        {messages.length === 1 && !isLoading && (
          <div className="flex flex-wrap gap-2 justify-center">
            {suggestedQuestions.map((q) => (
              <button
                key={q}
                onClick={() => handleSend(q)}
                className="px-3 py-1.5 rounded-full border border-slate-100 hover:border-indigo-100 bg-slate-50 hover:bg-indigo-50/50 text-[10px] font-semibold text-slate-500 hover:text-indigo-600 transition shadow-sm cursor-pointer"
              >
                {q}
              </button>
            ))}
          </div>
        )}

        {/* Active File Context Badge */}
        {fileContext && (
          <div className="flex items-center justify-between px-3 py-1.5 bg-indigo-50 border border-indigo-100 rounded-xl text-xs text-indigo-700 max-w-4xl mx-auto shadow-sm">
            <div className="flex items-center gap-2 truncate">
              <FileCode size={14} className="text-indigo-500 shrink-0" />
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400">File Context:</span>
              <span className="font-mono text-[11px] font-semibold text-indigo-900 truncate">{fileContext}</span>
            </div>
            <button
              onClick={() => setFileContext(null)}
              className="p-1 hover:bg-indigo-100 rounded-lg text-indigo-400 hover:text-indigo-600 transition cursor-pointer shrink-0 ml-2"
              title="Remove file context"
            >
              <X size={12} />
            </button>
          </div>
        )}

        {/* Form Input */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend(inputValue);
          }}
          className="flex items-center gap-2 max-w-4xl mx-auto border border-slate-200 rounded-xl p-1 bg-slate-50 focus-within:border-indigo-400 focus-within:bg-white focus-within:ring-2 focus-within:ring-indigo-100 transition-all shadow-inner"
        >
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            placeholder="Type your codebase question..."
            className="flex-1 px-4 py-2.5 text-xs text-slate-700 bg-transparent outline-none disabled:text-slate-400"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="h-9 w-9 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-200 text-white flex items-center justify-center transition shadow-sm shrink-0 cursor-pointer"
          >
            <Send size={14} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default DeveloperAssistant;