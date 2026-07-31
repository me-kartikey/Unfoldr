import {
  LayoutDashboard,
  BookOpen,
  Network,
  Bot,
  FolderGit2,
  Settings,
} from "lucide-react";

export const sidebarItems = [
  {
    label: "Overview",
    path: "/workspace",
    icon: LayoutDashboard,
  },
  {
    label: "Knowledge Base",
    path: "/workspace/knowledge-base",
    icon: BookOpen,
  },
  {
    label: "Architecture",
    path: "/workspace/architecture",
    icon: Network,
  },
  {
    label: "Developer Assistant",
    path: "/workspace/assistant",
    icon: Bot,
  },
  {
    label: "Repository Files",
    path: "/workspace/files",
    icon: FolderGit2,
  },
  {
    label: "Settings",
    path: "/workspace/settings",
    icon: Settings,
  },
];