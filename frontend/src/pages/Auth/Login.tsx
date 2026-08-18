import React, { useState } from "react";
import { useNavigate, Link, useLocation } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { ShieldAlert, LogIn, ArrowRight, User, Lock, CheckCircle } from "lucide-react";

// Created on 13-08-2026: Revamped Login view using a professional Split-Screen layout with an interactive simulated developer pipeline preview and glowing background auroras.

const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const registered = location.state?.registered;

  const [usernameOrEmail, setUsernameOrEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(usernameOrEmail, password);
      navigate("/upload");
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        "Failed to log in. Please check your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex selection:bg-indigo-500 selection:text-white relative overflow-hidden">
      
      {/* Left panel: SaaS Premium Brand Hero (Visible on md+) */}
      <div className="hidden lg:flex lg:w-1/2 bg-slate-900 text-white relative overflow-hidden flex-col justify-between p-16 border-r border-slate-800">
         {/* Subtle background grids */}
         <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] pointer-events-none opacity-40" />
         
         {/* Large aura glow blob */}
         <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] rounded-full bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 blur-[120px] pointer-events-none" />

         {/* Header Logo */}
         <div className="flex items-center gap-2.5 relative z-10 cursor-pointer" onClick={() => navigate("/")}>
           <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center font-bold text-white shadow-md shadow-indigo-500/20">
             U
           </div>
           <span className="text-xl font-bold tracking-tight text-slate-100">Unfoldr</span>
         </div>

         {/* Mid content info panel */}
         <div className="relative z-10 my-auto space-y-8 w-full">
            <div className="space-y-4 max-w-lg">
              <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight leading-tight text-slate-100 bg-gradient-to-r from-white via-slate-100 to-indigo-200 bg-clip-text text-transparent">
                Understand any <br />
                codebase in seconds.
              </h1>
              <p className="text-slate-400 text-sm leading-relaxed">
                Upload your repository ZIP to instantly map directories, discover architectural layers, analyze dependencies, and converse with your code via Gemini.
              </p>
            </div>

            {/* Edited on 13-08-2026: Dynamic dashboard product preview mockup, avoiding exposing direct technology secrets */}
            <div className="w-[65%] h-[310px] rounded-2xl border border-slate-800/80 bg-slate-950/60 backdrop-blur-sm p-5 space-y-4 shadow-2xl relative overflow-hidden transition-all hover:border-indigo-500/20 text-slate-300">
                {/* Mockup Header */}
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                    <div className="flex items-center gap-2">
                        <div className="h-2 w-2 rounded-full bg-indigo-500 animate-pulse" />
                        <span className="text-xs font-semibold text-slate-200">my-web-app.zip</span>
                    </div>
                    <span className="text-[10px] font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded-full border border-indigo-500/20">
                        Analyzing
                    </span>
                </div>

                {/* Project Stats Group */}
                <div className="grid grid-cols-2 gap-3 text-[11px]">
                    <div className="bg-slate-900/40 border border-slate-800/60 rounded-xl p-3 space-y-1">
                        <span className="text-slate-500 block">Total Files</span>
                        <div className="flex items-center gap-1.5">
                            <span className="text-emerald-400">✓</span>
                            <span className="font-semibold text-slate-200">1,248 files</span>
                        </div>
                    </div>
                    <div className="bg-slate-900/40 border border-slate-800/60 rounded-xl p-3 space-y-1">
                        <span className="text-slate-500 block">Analysis Status</span>
                        <div className="flex items-center gap-1.5">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                            <span className="font-semibold text-slate-200">92% Complete</span>
                        </div>
                    </div>
                </div>

                {/* Detected Stack Tags */}
                <div className="space-y-1.5">
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Detected Tech Stack</span>
                    <div className="flex gap-2">
                        <span className="text-[10px] font-semibold text-slate-300 bg-indigo-500/5 border border-slate-800 px-2.5 py-1 rounded-lg">React</span>
                        <span className="text-[10px] font-semibold text-slate-300 bg-indigo-500/5 border border-slate-800 px-2.5 py-1 rounded-lg">FastAPI</span>
                        <span className="text-[10px] font-semibold text-slate-300 bg-indigo-500/5 border border-slate-800 px-2.5 py-1 rounded-lg">PostgreSQL</span>
                    </div>
                </div>

                {/* Architecture Mapping & Vector Status */}
                <div className="space-y-2 pt-1">
                    <div className="flex items-center justify-between text-[11px]">
                        <div className="flex items-center gap-2">
                            <span className="text-emerald-400">✓</span>
                            <span className="text-slate-400">Architecture Mapping</span>
                        </div>
                        <span className="text-slate-400 font-medium">MVC Pattern</span>
                    </div>

                    <div className="flex items-center justify-between text-[11px]">
                        <div className="flex items-center gap-2">
                            <span className="h-3 w-3 rounded-full border border-indigo-500 border-t-transparent animate-spin inline-block" />
                            <span className="text-slate-400">Generating AI Insights</span>
                        </div>
                        <span className="text-indigo-400 font-semibold animate-pulse">Running</span>
                    </div>
                </div>
            </div>
         </div>

         {/* Bottom Copyright */}
         <div className="relative z-10 text-xs text-slate-500 font-medium">
           © {new Date().getFullYear()} Unfoldr Inc. Turn Code Into Clarity.
         </div>
      </div>

      {/* Right panel: Centered Login Form panel */}
      <div className="w-full lg:w-1/2 flex items-center justify-center relative px-6 py-12">
        {/* Subtle grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#f1f5f9_1px,transparent_1px),linear-gradient(to_bottom,#f1f5f9_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] pointer-events-none" />
        
        {/* Background glow auras */}
        <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-gradient-to-tr from-indigo-200/20 to-violet-200/20 blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-gradient-to-br from-purple-200/10 to-pink-200/10 blur-[120px] pointer-events-none" />

        <div className="w-full max-w-md bg-white border border-slate-200 rounded-2xl shadow-xl shadow-slate-100 p-8 relative z-10 transition-all hover:shadow-2xl">
          {/* Logo representation on mobile view (hidden on desktop) */}
          <div className="flex flex-col items-center mb-8">
            <div className="h-11 w-11 rounded-2xl bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20 mb-3">
              U
            </div>
            <h2 className="text-2xl font-extrabold text-slate-800 tracking-tight">Sign In to Unfoldr</h2>
            <p className="text-slate-400 text-xs mt-1 font-medium">Get instant clarity on your repository</p>
          </div>

          {registered && (
            <div className="mb-6 p-4 rounded-xl border border-emerald-100 bg-emerald-50 text-emerald-700 text-sm flex items-center gap-3">
              <CheckCircle size={18} className="flex-shrink-0 text-emerald-500" />
              <span className="font-medium">Registration successful! Please sign in.</span>
            </div>
          )}

          {error && (
            <div className="mb-6 p-4 rounded-xl border border-rose-100 bg-rose-50 text-rose-700 text-sm flex items-center gap-3 animate-shake">
              <ShieldAlert size={18} className="flex-shrink-0 text-rose-500" />
              <span className="font-medium">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">
                Username or Email
              </label>
              {/* Interactive wrapper block reacting on hover / focus */}
              <div className="group relative flex items-center border border-slate-200 rounded-xl bg-slate-50 focus-within:bg-white focus-within:border-indigo-500 focus-within:ring-4 focus-within:ring-indigo-500/10 transition-all duration-300 hover:border-slate-300 hover:-translate-y-[1px] hover:shadow-sm pl-3.5">
                <span className="text-slate-400 group-focus-within:text-indigo-500 transition-colors duration-300">
                  <User size={16} />
                </span>
                <input
                  type="text"
                  required
                  value={usernameOrEmail}
                  onChange={(e) => setUsernameOrEmail(e.target.value)}
                  placeholder="e.g. developer_user"
                  className="w-full pl-2.5 pr-4 py-3.5 bg-transparent border-none outline-none focus:outline-none focus:ring-0 text-sm text-slate-800 placeholder-slate-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">
                Password
              </label>
              {/* Interactive wrapper block reacting on hover / focus */}
              <div className="group relative flex items-center border border-slate-200 rounded-xl bg-slate-50 focus-within:bg-white focus-within:border-indigo-500 focus-within:ring-4 focus-within:ring-indigo-500/10 transition-all duration-300 hover:border-slate-300 hover:-translate-y-[1px] hover:shadow-sm pl-3.5">
                <span className="text-slate-400 group-focus-within:text-indigo-500 transition-colors duration-300">
                  <Lock size={16} />
                </span>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-2.5 pr-4 py-3.5 bg-transparent border-none outline-none focus:outline-none focus:ring-0 text-sm text-slate-800 placeholder-slate-400"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-3.5 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold rounded-xl transition-all shadow-md shadow-indigo-500/10 cursor-pointer disabled:opacity-50 active:scale-[0.98] mt-2"
            >
              {loading ? "Signing In..." : "Sign In"}
              <LogIn size={16} />
            </button>
          </form>

          <div className="mt-8 text-center border-t border-slate-100 pt-6">
            <p className="text-slate-500 text-sm">
              Don't have an account?{" "}
              <Link
                to="/register"
                className="text-indigo-600 hover:text-indigo-500 hover:underline font-bold inline-flex items-center gap-1 transition-colors"
              >
                Sign Up
                <ArrowRight size={14} />
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
