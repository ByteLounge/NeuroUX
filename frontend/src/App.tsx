import { useState } from 'react';
import axios from 'axios';
import { 
  LayoutDashboard, 
  BrainCircuit, 
  ChevronRight,
  TrendingUp,
  AlertCircle,
  MousePointer2
} from 'lucide-react';
import { UploadZone } from './components/UploadZone';
import { MetricCard } from './components/MetricCard';
import { AnalysisResult } from './components/AnalysisResult';
import type { AnalysisSession } from './types';

const API_BASE = "http://localhost:8000";

function App() {
  const [session, setSession] = useState<AnalysisSession | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [view, setView] = useState<'upload' | 'results'>('upload');

  const handleUpload = async (file: File) => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/api/v1/analyze`, formData);
      setSession(response.data);
      setView('results');
    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Analysis failed. Please ensure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = () => {
    if (session) {
      window.open(`${API_BASE}/api/v1/export/${session.id}`, '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-[#030712] text-gray-100 flex font-sans selection:bg-indigo-500/30">
      {/* Sidebar */}
      <aside className="w-72 border-r border-gray-800 bg-[#030712] flex flex-col p-6 sticky top-0 h-screen">
        <div className="flex items-center space-x-3 mb-12 px-2">
          <div className="bg-indigo-600 p-2 rounded-xl shadow-lg shadow-indigo-500/20">
            <BrainCircuit className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            NeuroUX
          </span>
        </div>

        <nav className="space-y-2 flex-1">
          {[
            { id: 'upload', icon: LayoutDashboard, label: 'Analyze UI' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setView(item.id as any)}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-2xl transition-all ${view === item.id ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-gray-500 hover:text-gray-300 hover:bg-gray-900'}`}
            >
              <div className="flex items-center space-x-3">
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </div>
              {view === item.id && <div className="h-1.5 w-1.5 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.8)]" />}
            </button>
          ))}
        </nav>

        <div className="mt-auto p-4 bg-gray-900/50 rounded-2xl border border-gray-800">
          <p className="text-xs text-gray-500 mb-2 uppercase font-bold tracking-widest">System Status</p>
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-sm font-medium text-gray-300">ML Engine Ready</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-12 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          {view === 'upload' && (
            <div className="space-y-12">
              <div className="space-y-4">
                <h1 className="text-5xl font-bold text-white tracking-tight">
                  Design with <span className="text-indigo-500">Intelligence</span>.
                </h1>
                <p className="text-xl text-gray-500 max-w-2xl leading-relaxed">
                  Predict how users will see and interact with your interface using our advanced visual saliency and cognitive load models.
                </p>
              </div>

              <UploadZone onUpload={handleUpload} isLoading={isLoading} />

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="p-6 bg-gray-900/30 border border-gray-800 rounded-2xl">
                  <TrendingUp className="w-6 h-6 text-indigo-500 mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Saliency Mapping</h3>
                  <p className="text-sm text-gray-500">Visualize exactly where a user's eyes will land in the first 500ms of interaction.</p>
                </div>
                <div className="p-6 bg-gray-900/30 border border-gray-800 rounded-2xl">
                  <AlertCircle className="w-6 h-6 text-amber-500 mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Friction Analysis</h3>
                  <p className="text-sm text-gray-500">Detect cluttered regions that increase cognitive load and cause interaction fatigue.</p>
                </div>
                <div className="p-6 bg-gray-900/30 border border-gray-800 rounded-2xl">
                  <MousePointer2 className="w-6 h-6 text-emerald-500 mb-4" />
                  <h3 className="text-lg font-semibold mb-2">UX Scoring</h3>
                  <p className="text-sm text-gray-500">Get a quantitative intelligence score for your UI based on established vision science.</p>
                </div>
              </div>
            </div>
          )}

          {view === 'results' && session && (
            <div className="space-y-12">
              <button 
                onClick={() => setView('upload')}
                className="flex items-center text-gray-500 hover:text-white transition-colors group"
              >
                <ChevronRight className="w-4 h-4 rotate-180 mr-1 group-hover:-translate-x-1 transition-transform" />
                Back to Dashboard
              </button>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard 
                  label="Cognitive Friction" 
                  value={session.cfi_score || 0} 
                  description="Measures effort required to parse information."
                  color="bg-red-500"
                />
                <MetricCard 
                  label="Visual Competition" 
                  value={session.vcs_score || 0} 
                  description="Conflict between different focal points."
                  color="bg-amber-500"
                />
                <MetricCard 
                  label="Fatigue Score" 
                  value={session.ifs_score || 0} 
                  description="Predicted interaction burnout probability."
                  color="bg-indigo-500"
                />
                <MetricCard 
                  label="UX Intelligence" 
                  value={session.ux_intelligence_score || 0} 
                  description="Overall design effectiveness rating."
                  color="bg-emerald-500"
                />
              </div>

              <AnalysisResult session={session} onExport={handleExport} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
