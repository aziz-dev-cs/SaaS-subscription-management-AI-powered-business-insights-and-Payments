/** TypeScript interfaces for the AI insights feature. */

export interface Insight {
  title: string;
  description: string;
  category: 'revenue' | 'churn' | 'growth' | 'optimization' | 'alert';
  priority: 'low' | 'medium' | 'high' | 'critical';
  suggested_action: string;
  confidence_score: number;
  generated_at: string;
}

export interface InsightsList {
  insights: Insight[];
  generated_at: string;
  model_used: string;
}

export interface InsightQuery {
  question: string;
  answer: string;
  data_points_referenced: string[];
  confidence_score: number;
}
