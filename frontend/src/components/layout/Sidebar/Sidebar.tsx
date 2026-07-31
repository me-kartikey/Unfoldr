import SidebarHeader from "./SidebarHeader";
import SidebarNavigation from "./SidebarNavigation";
import SidebarFooter from "./SidebarFooter";

function Sidebar() {
  return (
    <aside className="flex h-[calc(100vh-64px)] w-72 flex-col border-r bg-white">
      <SidebarHeader />

      <div className="flex-1 overflow-y-auto">
        <SidebarNavigation />
      </div>

      <SidebarFooter />
    </aside>
  );
}

export default Sidebar;