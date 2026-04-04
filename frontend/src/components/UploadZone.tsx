import { motion } from 'framer-motion';
import { Upload, Loader2 } from 'lucide-react';
import { useState, useRef } from 'react';

interface UploadZoneProps {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

export const UploadZone = ({ onUpload, isLoading }: UploadZoneProps) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      onUpload(file);
    }
  };

  return (
    <motion.div
      whileHover={{ scale: 1.005 }}
      whileTap={{ scale: 0.995 }}
      onClick={() => fileInputRef.current?.click()}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        relative h-80 w-full flex flex-col items-center justify-center
        border-2 border-dashed rounded-3xl cursor-pointer transition-all duration-300
        ${isDragOver ? 'border-indigo-500 bg-indigo-500/5' : 'border-gray-800 hover:border-gray-700 bg-gray-900/50'}
      `}
    >
      <input
        type="file"
        ref={fileInputRef}
        className="hidden"
        accept="image/*"
        onChange={(e) => e.target.files && onUpload(e.target.files[0])}
      />
      
      {isLoading ? (
        <div className="flex flex-col items-center">
          <Loader2 className="w-12 h-12 text-indigo-500 animate-spin mb-4" />
          <p className="text-gray-300 font-medium">Analyzing Visual Patterns...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center p-8">
          <div className="w-20 h-20 bg-gray-800 rounded-2xl flex items-center justify-center mb-6 shadow-2xl">
            <Upload className="w-8 h-8 text-gray-400" />
          </div>
          <h2 className="text-2xl font-semibold text-white mb-2 text-center">
            Upload UI Screenshot
          </h2>
          <p className="text-gray-500 text-center max-w-sm">
            Drag and drop your UI design (JPG, PNG, WebP) to analyze cognitive load and attention.
          </p>
        </div>
      )}

      {/* Background Glow */}
      <div className="absolute inset-0 -z-10 bg-indigo-500/5 blur-3xl rounded-full" />
    </motion.div>
  );
};
