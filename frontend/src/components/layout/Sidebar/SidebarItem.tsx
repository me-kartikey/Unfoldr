import { NavLink } from "react-router-dom";

interface SidebarItemProps {
  label: string;
  path: string;
  icon: React.ElementType;
}

function SidebarItem({
  label,
  path,
  icon: Icon,
}: SidebarItemProps) {
  return (
    <NavLink
      to={path}
      className={({ isActive }) =>
        `
        flex
        items-center
        gap-3
        rounded-lg
        px-3
        py-2
        transition-colors
        ${
          isActive
            ? "bg-slate-900 text-white"
            : "text-slate-600 hover:bg-slate-100"
        }
      `
      }
    >
      <Icon size={18} />

      <span>{label}</span>
    </NavLink>
  );
}

export default SidebarItem;