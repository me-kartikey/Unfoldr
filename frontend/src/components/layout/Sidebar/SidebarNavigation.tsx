import { useParams } from "react-router-dom";
import SidebarItem from "./SidebarItem";
import { sidebarItems } from "./sidebarData";

function SidebarNavigation() {
  const { repositoryId } = useParams<{ repositoryId: string }>();

  const getPath = (basePath: string) => {
    if (!repositoryId) return basePath;
    if (basePath === "/workspace") return `/workspace/${repositoryId}`;
    return basePath.replace("/workspace", `/workspace/${repositoryId}`);
  };

  return (
    <nav className="flex flex-col gap-1 px-3 py-4">
      {sidebarItems.map((item) => (
        <SidebarItem
          key={item.path}
          label={item.label}
          path={getPath(item.path)}
          icon={item.icon}
          end={item.end} // Edited on 2026-08-11: Map the end property configuration to SidebarItem.
        />
      ))}
    </nav>
  );
}

export default SidebarNavigation;