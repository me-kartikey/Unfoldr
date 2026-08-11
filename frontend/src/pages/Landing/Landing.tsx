import { useNavigate } from "react-router-dom";
import { Sparkles, Cpu, Layers, Shield, ArrowRight } from "lucide-react";

// Edited on 2026-08-11: Redesigned the Landing Page to align with the clean, light-themed SaaS developer workspace aesthetic.

function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between selection:bg-indigo-500 selection:text-white relative overflow-x-hidden">
      {/* Subtle Background grids / patterns */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#e2e8f0_1px,transparent_1px),linear-gradient(to_bottom,#e2e8f0_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none" />

      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur sticky top-0 z-50 px-6 lg:px-16 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center font-bold text-white shadow-md shadow-indigo-500/10">
            U
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-800">
            Unfoldr
          </span>
          <span className="text-xs text-indigo-600 font-medium px-2 py-0.5 rounded-full bg-indigo-50 border border-indigo-100 hidden sm:inline-block">
            Turn Code Into Clarity
          </span>
        </div>
        <button
          onClick={() => navigate("/upload")}
          className="px-4 py-2 text-sm font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer border border-transparent"
        >
          Sign In
        </button>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 text-center max-w-5xl mx-auto py-16 lg:py-24 relative z-10">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-indigo-100 bg-indigo-50 text-indigo-700 text-xs font-semibold mb-6 shadow-sm shadow-indigo-100/10 animate-pulse">
          <Sparkles size={14} />
          <span>Automated Codebase Onboarding & Intelligence</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-6 text-slate-800 max-w-4xl leading-tight">
          Onboard to new repositories <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">in seconds, not weeks.</span>
        </h1>

        <p className="text-slate-500 text-lg sm:text-xl max-w-2xl mb-10 leading-relaxed">
          Upload any project repository ZIP and instantly get visual architecture mappings, dependency insights, auto-generated documentation, and a Gemini-powered chat assistant.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center w-full max-w-sm mb-16">
          <button
            onClick={() => navigate("/upload")}
            className="flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold rounded-xl transition-all shadow-md shadow-indigo-500/15 cursor-pointer"
          >
            Get Started
            <ArrowRight size={18} />
          </button>
        </div>

        {/* Feature Grid */}
        <section className="w-full">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-10">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full text-left">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
              <div className="h-10 w-10 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 mb-4 border border-indigo-100">
                <Cpu size={20} />
              </div>
              <h3 className="text-lg font-bold text-slate-800 mb-2">Automated Code Scanner</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                Detects file patterns, directories, source code layouts, languages, and frameworks using static analysis.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
              <div className="h-10 w-10 rounded-lg bg-violet-50 flex items-center justify-center text-violet-600 mb-4 border border-violet-100">
                <Layers size={20} />
              </div>
              <h3 className="text-lg font-bold text-slate-800 mb-2">Architecture Mapping</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                Extracts project configuration settings, database schemas, configuration files, testing modules, and directories.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
              <div className="h-10 w-10 rounded-lg bg-pink-50 flex items-center justify-center text-pink-600 mb-4 border border-pink-100">
                <Shield size={20} />
              </div>
              <h3 className="text-lg font-bold text-slate-800 mb-2">Developer AI Assistant</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                Query code structures, explain logic blocks, or answer dependency configuration questions using a Gemini RAG agent.
              </p>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="w-full mt-24">
          <h2 className="text-2xl font-bold text-slate-800 mb-2">How It Works</h2>
          <p className="text-slate-500 text-sm max-w-md mx-auto mb-12">Three steps to turn repository source code into clear, interactive developer documentation.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
            <div className="relative p-6 bg-white border border-slate-200 rounded-2xl shadow-sm">
              <div className="absolute -top-4 left-6 h-8 w-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-sm">
                1
              </div>
              <h4 className="text-base font-bold text-slate-800 mb-2 mt-2">Upload ZIP Archive</h4>
              <p className="text-slate-500 text-xs leading-relaxed">
                Compress your repository folder and drop the ZIP archive into our clean onboarding container.
              </p>
            </div>

            <div className="relative p-6 bg-white border border-slate-200 rounded-2xl shadow-sm">
              <div className="absolute -top-4 left-6 h-8 w-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-sm">
                2
              </div>
              <h4 className="text-base font-bold text-slate-800 mb-2 mt-2">Automated Analysis</h4>
              <p className="text-slate-500 text-xs leading-relaxed">
                Our background processes parse file layers, map databases, and generate comprehensive documentation.
              </p>
            </div>

            <div className="relative p-6 bg-white border border-slate-200 rounded-2xl shadow-sm">
              <div className="absolute -top-4 left-6 h-8 w-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-sm">
                3
              </div>
              <h4 className="text-base font-bold text-slate-800 mb-2 mt-2">Explore & Collaborate</h4>
              <p className="text-slate-500 text-xs leading-relaxed">
                Browse file trees, explore architecture setups, and converse with the RAG assistant to answer coding tasks.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white py-8 px-6 lg:px-16 text-center text-slate-400 text-xs">
        <p>&copy; {new Date().getFullYear()} Unfoldr Inc. Turn Code Into Clarity. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Landing;