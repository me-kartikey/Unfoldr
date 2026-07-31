import { Outlet } from "react-router-dom";

import Navbar from "@/components/layout/Navbar/Navbar";
import Sidebar from "@/components/layout/Sidebar/Sidebar";

function WorkspaceLayout() {
  return (
    <div className="flex h-screen flex-col">

    <Navbar />

    <div className="flex flex-1 overflow-hidden">

        <Sidebar />

        <main className="flex-1 overflow-y-auto bg-slate-50 p-8">

            <Outlet />

        </main>

    </div>

</div>
  );
}

export default WorkspaceLayout;