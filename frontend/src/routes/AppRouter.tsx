import { BrowserRouter, Routes, Route } from "react-router-dom";

import Landing from "@/pages/Landing/Landing";
import Upload from "@/pages/Upload/Upload";

import WorkspaceLayout from "@/layouts/WorkspaceLayout";

import Overview from "@/pages/Workspace/Overview/Overview";
import KnowledgeBase from "@/pages/Workspace/KnowledgeBase";
import Architecture from "@/pages/Workspace/Architecture";
import DeveloperAssistant from "@/pages/Workspace/DeveloperAssistant";
import RepositoryFiles from "@/pages/Workspace/RepositoryFiles";
import Settings from "@/pages/Workspace/Settings";

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Landing />} />
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
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;