import { motion } from 'framer-motion';

interface MetricCardProps {
  label: string;
  value: number;
  description: string;
  color: string;
}

export const MetricCard = ({ label, value, description, color }: MetricCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-900 border border-gray-800 p-6 rounded-2xl shadow-xl hover:border-indigo-500 transition-colors"
    >
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-gray-400 font-medium text-sm tracking-wider uppercase">{label}</h3>
        <div className={`h-2 w-2 rounded-full ${color}`} />
      </div>
      <div className="flex items-baseline space-x-2">
        <span className="text-4xl font-bold text-white">{value.toFixed(1)}</span>
        <span className="text-gray-500 text-sm">/ 100</span>
      </div>
      <p className="mt-4 text-sm text-gray-500 leading-relaxed">{description}</p>
      
      {/* Progress Bar */}
      <div className="mt-6 h-1.5 w-full bg-gray-800 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`h-full ${color.replace('bg-', 'bg-')}`}
          style={{ backgroundColor: color.startsWith('bg-') ? undefined : color }}
        />
      </div>
    </motion.div>
  );
};
