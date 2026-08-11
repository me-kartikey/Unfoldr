import { NavLink } from "react-router-dom";

// Edited on 2026-08-11: Updated SidebarItem to accept and pass the "end" prop to NavLink for exact path matches.
interface SidebarItemProps {
  label: string;
  path: string;
  icon: React.ElementType;
  end?: boolean;
}

function SidebarItem({
  label,
  path,
  icon: Icon,
  end,
}: SidebarItemProps) {
  return (
    <NavLink
      to={path}
      end={end}
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