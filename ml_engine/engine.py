import cv2
import numpy as np
import os

class NeuroUXEngine:
    def __init__(self):
        # Initialize OpenCV saliency detector
        self.saliency = cv2.saliency.StaticSaliencySpectralResidual_create()

    def process_image(self, image_path: str, output_dir: str):
        """
        Processes an image to generate heatmaps and UX metrics.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image at {image_path}")

        # 1. Generate Saliency Heatmap
        success, saliency_map = self.saliency.computeSaliency(image)
        saliency_map = (saliency_map * 255).astype("uint8")
        
        # Apply colormap for visual heatmap
        heatmap = cv2.applyColorMap(saliency_map, cv2.COLORMAP_JET)
        
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(image_path)
        saliency_path = os.path.join(output_dir, f"saliency_{filename}")
        cv2.imwrite(saliency_path, heatmap)

        # 2. Calculate Custom Metrics
        metrics = self._calculate_metrics(image, saliency_map)
        
        # 3. Generate Recommendations
        recommendations = self._generate_recommendations(metrics)

        return {
            "metrics": metrics,
            "saliency_heatmap_path": saliency_path,
            "recommendations": recommendations
        }

    def _calculate_metrics(self, image, saliency_map):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # CFI - Cognitive Friction Index (Edge Density & Contrast)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        contrast = gray.std() / 128.0 # Normalized contrast
        cfi = min(100, (edge_density * 500) + (contrast * 20))

        # VCS - Visual Competition Score (Peak Saliency)
        # Find number of high saliency regions
        _, thresh = cv2.threshold(saliency_map, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        vcs = min(100, len(contours) * 10)

        # IFS - Interaction Fatigue Score (Complexity)
        # Using laplacian variance as a proxy for structural complexity
        complexity = cv2.Laplacian(gray, cv2.CV_64F).var()
        ifs = min(100, complexity / 50)

        # DDP - Decision Delay Probability (Clutter)
        # Correlation between high edge density areas and saliency
        ddp = min(100, (cfi + vcs) / 2)

        # UX Intelligence Score (Weighted Mean)
        # Higher is better, so we invert friction-based metrics
        base_score = 100 - ((cfi * 0.3) + (vcs * 0.2) + (ifs * 0.3) + (ddp * 0.2))
        ux_score = max(0, min(100, base_score))

        return {
            "cfi_score": float(cfi),
            "vcs_score": float(vcs),
            "ifs_score": float(ifs),
            "ddp_score": float(ddp),
            "ux_intelligence_score": float(ux_score)
        }

    def _generate_recommendations(self, metrics):
        recs = []
        
        # Cognitive Friction Index (CFI)
        if metrics["cfi_score"] > 80:
            recs.append({"text": "Critical visual clutter detected. This layout will significantly slow down user processing. Immediate simplification of edge-heavy elements is required.", "severity": "High"})
        elif metrics["cfi_score"] > 60:
            recs.append({"text": "High visual complexity detected. Consider increasing whitespace and reducing the number of borders/lines to decrease cognitive load.", "severity": "Medium"})
        elif metrics["cfi_score"] < 30:
             recs.append({"text": "Excellent visual clarity. The low edge density allows for fast scanning and minimal cognitive friction.", "severity": "Success"})

        # Visual Competition Score (VCS)
        if metrics["vcs_score"] > 70:
            recs.append({"text": "Too many competing focal points. Use size, color, or weight to establish a clear visual hierarchy and guide the user's eye to the primary CTA.", "severity": "High"})
        elif metrics["vcs_score"] > 40:
            recs.append({"text": "Multiple areas are competing for attention. Consider dimming secondary elements to highlight the main interaction point.", "severity": "Medium"})
        
        # Interaction Fatigue Score (IFS)
        if metrics["ifs_score"] > 75:
            recs.append({"text": "Severe structural complexity. This UI is likely to cause rapid interaction fatigue. Simplify complex components into smaller, more digestible units.", "severity": "High"})
        elif metrics["ifs_score"] > 50:
            recs.append({"text": "Interaction density is high. This may cause fatigue over time; simplify UI elements or use progressive disclosure.", "severity": "Medium"})

        # Decision Delay Probability (DDP)
        if metrics["ddp_score"] > 70:
            recs.append({"text": "High probability of decision paralysis. The combination of clutter and competing signals makes it difficult for users to choose the next action.", "severity": "High"})
        elif metrics["ddp_score"] > 50:
            recs.append({"text": "Potential for delayed user action. Streamline the decision path by removing non-essential information near critical buttons.", "severity": "Medium"})

        # UX Intelligence Score
        if metrics["ux_intelligence_score"] < 40:
            recs.append({"text": "Overall UX Intelligence is low. We recommend a full layout audit to prioritize usability and clear navigation paths.", "severity": "High"})
        elif metrics["ux_intelligence_score"] > 85:
            recs.append({"text": "Outstanding UI design. The layout balances attention, complexity, and clarity exceptionally well.", "severity": "Success"})
        
        if not recs:
            recs.append({"text": "Layout follows good visual hierarchy principles and is well-balanced.", "severity": "Info"})
            
        return recs
