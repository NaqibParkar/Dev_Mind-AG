import React from 'react';
import { NavigationPage } from '../types';
import { Icons } from './UI';

interface LayoutProps {
  children: React.ReactNode;
  activePage: NavigationPage;
  onNavigate: (page: NavigationPage) => void;
  onLogout: () => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, activePage, onNavigate, onLogout }) => {
  
  const NavItem = ({ page, icon: Icon, label }: { page: NavigationPage; icon: any; label: string }) => {
    const isActive = activePage === page;
    return (
      <button
        onClick={() => onNavigate(page)}
        className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 mb-1 group ${
          isActive 
            ? 'bg-white shadow-sm text-indigo-600' 
            : 'text-slate-500 hover:bg-white/50 hover:text-slate-700'
        }`}
      >
        <Icon className={`w-5 h-5 ${isActive ? 'text-indigo-600' : 'text-slate-400 group-hover:text-slate-600'}`} />
        <span className="font-medium">{label}</span>
      </button>
    );
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50/50">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 border-r border-slate-200/60 bg-white/40 backdrop-blur-xl flex flex-col">
        <div className="p-6 flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Icons.Brain className="text-white w-6 h-6" />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600">
            DevMind
          </span>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
          <NavItem page="dashboard" icon={Icons.LayoutDashboard} label="Overview" />
          <NavItem page="live-detection" icon={Icons.Activity} label="Live Detection" />
          <NavItem page="analytics" icon={Icons.BarChart2} label="Analytics" />
          <NavItem page="projects" icon={Icons.FolderKanban} label="Projects" />
          <NavItem page="settings" icon={Icons.Settings} label="Settings" />
        </nav>

        <div className="p-4 border-t border-slate-200/60">
           <div className="bg-slate-100/50 rounded-xl p-3 mb-3">
              <div className="flex items-center space-x-2 text-xs text-slate-500 mb-1">
                 <Icons.ShieldCheck className="w-3 h-3 text-teal-600" />
                 <span className="font-semibold text-teal-700">Privacy Active</span>
              </div>
              <p className="text-[10px] text-slate-400 leading-tight">Data stored locally. No cloud upload.</p>
           </div>
           <button 
             onClick={onLogout}
             className="flex items-center space-x-3 px-4 py-2 w-full rounded-lg text-slate-500 hover:bg-red-50 hover:text-red-600 transition-colors text-sm"
           >
             <Icons.LogOut className="w-4 h-4" />
             <span>Sign Out</span>
           </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative">
        <header className="sticky top-0 z-20 px-8 py-4 bg-slate-50/80 backdrop-blur-md border-b border-slate-200/50 flex justify-between items-center">
          <div>
            <h1 className="text-xl font-semibold text-slate-800 capitalize">{activePage.replace('-', ' ')}</h1>
            <p className="text-sm text-slate-500">Welcome back, Developer.</p>
          </div>
          <div className="flex items-center space-x-4">
             <div className="flex items-center space-x-2 px-3 py-1.5 bg-white/60 rounded-full border border-slate-200/50 shadow-sm">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-teal-500"></span>
                </span>
                <span className="text-xs font-medium text-slate-600">System Monitoring Active</span>
             </div>
             <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-100 to-purple-100 border border-white shadow-sm"></div>
          </div>
        </header>

        <div className="p-8 max-w-7xl mx-auto space-y-8 pb-20">
          {children}
        </div>
      </main>
    </div>
  );
};
