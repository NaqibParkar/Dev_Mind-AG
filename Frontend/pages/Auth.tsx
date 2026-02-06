import React, { useState } from 'react';
import { Card, Button, Icons } from '../components/UI';

interface AuthProps {
  onLogin: () => void;
}

export const Auth: React.FC<AuthProps> = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-200/30 rounded-full blur-[100px]"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-200/30 rounded-full blur-[100px]"></div>

      <div className="w-full max-w-md relative z-10">
        <div className="text-center mb-8">
           <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl mx-auto flex items-center justify-center mb-4 shadow-xl shadow-indigo-500/20">
              <Icons.Brain className="text-white w-8 h-8" />
           </div>
           <h1 className="text-3xl font-bold text-slate-800 mb-2">DevMind</h1>
           <p className="text-slate-500">Cognitive analytics for the modern developer.</p>
        </div>

        <Card className="backdrop-blur-2xl bg-white/70 shadow-2xl">
          <div className="space-y-6">
             <div className="flex border-b border-slate-200/60 mb-6">
                <button 
                  onClick={() => setIsLogin(true)}
                  className={`flex-1 pb-3 text-sm font-medium transition-all ${isLogin ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-slate-400 hover:text-slate-600'}`}
                >
                  Sign In
                </button>
                <button 
                  onClick={() => setIsLogin(false)}
                  className={`flex-1 pb-3 text-sm font-medium transition-all ${!isLogin ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-slate-400 hover:text-slate-600'}`}
                >
                  Create Account
                </button>
             </div>

             <form onSubmit={(e) => { e.preventDefault(); onLogin(); }} className="space-y-4">
                {!isLogin && (
                  <div>
                    <label className="block text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wide">Full Name</label>
                    <input type="text" className="w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-white/50 focus:bg-white focus:ring-2 focus:ring-indigo-200 outline-none transition-all" placeholder="John Doe" />
                  </div>
                )}
                
                <div>
                   <label className="block text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wide">Email Address</label>
                   <input type="email" className="w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-white/50 focus:bg-white focus:ring-2 focus:ring-indigo-200 outline-none transition-all" placeholder="dev@example.com" />
                </div>

                <div>
                   <label className="block text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wide">Password</label>
                   <input type="password" className="w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-white/50 focus:bg-white focus:ring-2 focus:ring-indigo-200 outline-none transition-all" placeholder="••••••••" />
                </div>

                {!isLogin && (
                   <div className="flex items-start space-x-2 mt-4">
                     <input type="checkbox" className="mt-1 rounded border-slate-300 text-indigo-600 focus:ring-indigo-200" />
                     <p className="text-xs text-slate-500">I agree to process my data <span className="font-bold text-slate-700">locally</span> and understand the privacy policy.</p>
                   </div>
                )}

                <Button type="submit" className="w-full mt-2" size="lg">
                  {isLogin ? 'Enter Dashboard' : 'Start Analytics Journey'}
                </Button>
             </form>

             {isLogin && (
               <div className="text-center">
                 <a href="#" className="text-sm text-indigo-500 hover:text-indigo-600 font-medium">Forgot your password?</a>
               </div>
             )}
          </div>
        </Card>
        
        <p className="text-center text-xs text-slate-400 mt-8">
          &copy; 2024 DevMind Labs. Offline-First Architecture.
        </p>
      </div>
    </div>
  );
};
