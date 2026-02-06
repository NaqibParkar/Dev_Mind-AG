import React, { useState, useMemo } from 'react';
import { Card, Badge, ProgressBar, Button, Icons } from '../components/UI';
import { CURRENT_STATE, EMOJI_OPTIONS, MOCK_PROJECT_COGNITIVE_DATA, DEFAULT_COGNITIVE_DATA } from '../constants';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Project } from '../types';

interface DashboardProps {
  activeProject: Project | null;
}

export const Dashboard: React.FC<DashboardProps> = ({ activeProject }) => {
  const [journalEmoji, setJournalEmoji] = useState<string | null>(null);
  const [journalNote, setJournalNote] = useState('');

  // Select data based on active project, or fall back to default
  const chartData = useMemo(() => {
    if (activeProject && MOCK_PROJECT_COGNITIVE_DATA[activeProject.id]) {
      return MOCK_PROJECT_COGNITIVE_DATA[activeProject.id];
    }
    return DEFAULT_COGNITIVE_DATA;
  }, [activeProject]);

  return (
    <div className="space-y-6">
      
      {/* Top Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <Icons.Brain className="w-16 h-16 text-indigo-600" />
          </div>
          <div className="relative z-10">
            <p className="text-sm font-medium text-slate-500 mb-1">Current Mental State</p>
            <h3 className="text-2xl font-bold text-slate-800 mb-2">{CURRENT_STATE.currentZone}</h3>
            <Badge color="purple">High Intensity</Badge>
          </div>
        </Card>

        <Card>
          <div className="flex justify-between items-end mb-2">
            <div>
               <p className="text-sm font-medium text-slate-500 mb-1">Focus Score</p>
               <h3 className="text-3xl font-bold text-slate-800">{CURRENT_STATE.focusScore}<span className="text-sm font-normal text-slate-400">/100</span></h3>
            </div>
            <div className="p-2 bg-green-50 rounded-lg">
               <Icons.ArrowUp className="w-4 h-4 text-green-600" />
            </div>
          </div>
          <ProgressBar value={CURRENT_STATE.focusScore} color="bg-gradient-to-r from-teal-400 to-teal-500" />
        </Card>

        <Card>
           <p className="text-sm font-medium text-slate-500 mb-1">Burnout Risk</p>
           <h3 className="text-2xl font-bold text-slate-800 mb-2">{CURRENT_STATE.burnoutRisk}</h3>
           <div className="flex items-center space-x-2 text-sm text-slate-500">
             <div className={`w-2 h-2 rounded-full ${CURRENT_STATE.burnoutRisk === 'Low' ? 'bg-green-500' : 'bg-amber-500'}`}></div>
             <span>Stable levels detected</span>
           </div>
        </Card>

        <Card>
           <p className="text-sm font-medium text-slate-500 mb-1">Deep Work Today</p>
           <h3 className="text-2xl font-bold text-slate-800 mb-2">{Math.floor(CURRENT_STATE.deepWorkMinutes / 60)}h {CURRENT_STATE.deepWorkMinutes % 60}m</h3>
           <p className="text-xs text-slate-400">Target: 4h 00m</p>
        </Card>
      </div>

      {/* Main Content Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Live Metrics */}
        <div className="lg:col-span-2 space-y-6">
          <Card title="Today's Cognitive Load" subtitle={activeProject ? `Mental effort estimation for ${activeProject.name}` : "Mental effort estimation"}>
             <div className="h-64 w-full mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData}>
                    <defs>
                      <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#818cf8" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#818cf8" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                    <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.9)', borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                      itemStyle={{ color: '#4f46e5' }}
                    />
                    <Area type="monotone" dataKey="val" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#colorVal)" />
                  </AreaChart>
                </ResponsiveContainer>
             </div>
          </Card>
        </div>

        {/* Side Panel: Journal & Productivity */}
        <div className="space-y-6">
          <Card title="Productivity Nudge" className="bg-gradient-to-br from-indigo-50 to-purple-50 border-indigo-100/50">
             <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-white rounded-lg shadow-sm">
                    <Icons.Zap className="w-5 h-5 text-indigo-500" />
                  </div>
                  <p className="text-sm text-slate-600">Your focus usually peaks around <span className="font-semibold text-indigo-700">10:00 AM</span>. Great time for complex tasks.</p>
                </div>
                <div className="h-px bg-indigo-100/50 w-full"></div>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-white rounded-lg shadow-sm">
                    <Icons.WifiOff className="w-5 h-5 text-slate-500" />
                  </div>
                  <p className="text-sm text-slate-600">Try <span className="font-semibold text-slate-700">Airplane Mode</span> for your next 30m sprint.</p>
                </div>
             </div>
          </Card>

          <Card title="Reflection Journal" subtitle="How are you feeling right now?">
             <div className="flex justify-between mb-4 px-2">
                {EMOJI_OPTIONS.map(emoji => (
                  <button 
                    key={emoji}
                    onClick={() => setJournalEmoji(emoji)}
                    className={`text-2xl p-2 rounded-xl transition-all hover:bg-slate-100 ${journalEmoji === emoji ? 'bg-indigo-100 scale-110 shadow-sm' : 'grayscale opacity-70 hover:grayscale-0 hover:opacity-100'}`}
                  >
                    {emoji}
                  </button>
                ))}
             </div>
             <textarea 
               value={journalNote}
               onChange={(e) => setJournalNote(e.target.value)}
               placeholder="Briefly note your state of mind..."
               className="w-full text-sm p-3 rounded-xl border border-slate-200 bg-white/50 focus:bg-white focus:ring-2 focus:ring-indigo-200 outline-none resize-none h-24 transition-all mb-3"
             />
             <div className="flex justify-between items-center">
                <span className="text-[10px] text-slate-400 uppercase tracking-wide">Private & Local</span>
                <Button size="sm" variant="secondary" onClick={() => { setJournalEmoji(null); setJournalNote(''); }}>Save Entry</Button>
             </div>
          </Card>
        </div>
      </div>
    </div>
  );
};