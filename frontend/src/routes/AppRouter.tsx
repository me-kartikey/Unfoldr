import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import ProtectedRoute from "./ProtectedRoute";

import Landing from "@/pages/Landing/Landing";
import Login from "@/pages/Auth/Login";
import Register from "@/pages/Auth/Register";
import Upload from "@/pages/Upload/Upload";

import WorkspaceLayout from "@/layouts/WorkspaceLayout";

import Overview from "@/pages/Workspace/Overview/Overview";
import KnowledgeBase from "@/pages/Workspace/KnowledgeBase";
import Architecture from "@/pages/Workspace/Architecture";
import DeveloperAssistant from "@/pages/Workspace/DeveloperAssistant";
import RepositoryFiles from "@/pages/Workspace/RepositoryFiles";
import Settings from "@/pages/Workspace/Settings";

// Edited on 13-08-2026: Integrate AuthProvider session contexts and wrap restricted workspaces in ProtectedRoute guards

function AppRouter() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/upload" element={<Upload />} />

            {/* Workspace Routes */}
            <Route path="/workspace/:repositoryId" element={<WorkspaceLayout />}>
              <Route index element={<Overview />} />
              <Route path="knowledge-base" element={<KnowledgeBase />} />
              <Route path="architecture" element={<Architecture />} />
              <Route path="assistant" element={<DeveloperAssistant />} />
              <Route path="files" element={<RepositoryFiles />} />
              <Route path="settings" element={<Settings />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default AppRouter;