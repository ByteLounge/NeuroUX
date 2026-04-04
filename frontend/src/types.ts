export interface Recommendation {
  id: number;
  session_id: number;
  text: string;
  severity: 'High' | 'Medium' | 'Low' | 'Info';
}

export interface AnalysisSession {
  id: number;
  created_at: string;
  original_image_path: string;
  cfi_score?: number;
  vcs_score?: number;
  ifs_score?: number;
  ddp_score?: number;
  ux_intelligence_score?: number;
  saliency_heatmap_path?: string;
  cognitive_load_heatmap_path?: string;
  recommendations: Recommendation[];
}
