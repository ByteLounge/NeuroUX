import { useState } from 'react';
import { motion } from 'framer-motion';
import { Layers, Image as ImageIcon, Sparkles, Download } from 'lucide-react';
import type { AnalysisSession } from '../types';

interface AnalysisResultProps {
  session: AnalysisSession;
  onExport: () => void;
}

export const AnalysisResult = ({ session, onExport }: AnalysisResultProps) => {
  const [viewMode, setViewMode] = useState<'saliency' | 'original'>('saliency');
  const [opacity, setOpacity] = useState(0.7);

  const API_BASE = "http://localhost:8000";

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Visual Intelligence</h2>
          <p className="text-gray-500">Real-time attention and cognitive friction mapping.</p>
        </div>
        <button
          onClick={onExport}
          className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-2xl font-medium transition-all shadow-lg shadow-indigo-500/20 active:scale-95"
        >
          <Download className="w-4 h-4" />
          <span>Export Report</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Heatmap Viewer */}
        <div className="lg:col-span-2 bg-gray-900/50 border border-gray-800 rounded-3xl p-6 overflow-hidden">
          <div className="flex space-x-4 mb-6">
            <button
              onClick={() => setViewMode('saliency')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${viewMode === 'saliency' ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/30' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
            >
              <Sparkles className="w-4 h-4" />
              <span>Attention Heatmap</span>
            </button>
            <button
              onClick={() => setViewMode('original')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${viewMode === 'original' ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/30' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
            >
              <ImageIcon className="w-4 h-4" />
              <span>Original UI</span>
            </button>
          </div>

          <div className="relative aspect-video rounded-2xl overflow-hidden bg-black group">
            <img
              src={`${API_BASE}${session.original_image_path}`}
              alt="Original UI"
              className="absolute inset-0 w-full h-full object-contain"
            />
            {viewMode === 'saliency' && (
              <motion.img
                initial={{ opacity: 0 }}
                animate={{ opacity }}
                src={`${API_BASE}${session.saliency_heatmap_path}`}
                alt="Saliency Heatmap"
                className="absolute inset-0 w-full h-full object-contain mix-blend-screen"
              />
            )}
            
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 w-64 bg-gray-900/90 backdrop-blur-xl border border-gray-800 px-6 py-3 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity flex items-center space-x-4">
              <Layers className="w-4 h-4 text-gray-400" />
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={opacity}
                onChange={(e) => setOpacity(parseFloat(e.target.value))}
                className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-indigo-500"
              />
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-3xl p-8 overflow-y-auto max-h-[600px]">
          <h3 className="text-xl font-bold text-white mb-6 flex items-center">
            <Sparkles className="w-5 h-5 text-indigo-500 mr-2" />
            AI Recommendations
          </h3>
          <div className="space-y-4">
            {session.recommendations.map((rec, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                className={`p-4 rounded-2xl border ${rec.severity === 'High' ? 'bg-red-500/5 border-red-500/20' : 'bg-amber-500/5 border-amber-500/20'}`}
              >
                <div className="flex items-center space-x-2 mb-2">
                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${rec.severity === 'High' ? 'bg-red-500/20 text-red-500' : 'bg-amber-500/20 text-amber-500'}`}>
                    {rec.severity} Severity
                  </span>
                </div>
                <p className="text-sm text-gray-300 leading-relaxed">{rec.text}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
