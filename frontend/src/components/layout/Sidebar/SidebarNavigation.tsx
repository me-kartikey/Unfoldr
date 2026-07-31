import SidebarItem from "./SidebarItem";
import { sidebarItems } from "./sidebarData";

function SidebarNavigation() {
  return (
    <nav className="flex flex-col gap-1 px-3 py-4">
      {sidebarItems.map((item) => (
        <SidebarItem
          key={item.path}
          label={item.label}
          path={item.path}
          icon={item.icon}
        />
      ))}
    </nav>
  );
}

export default SidebarNavigation;