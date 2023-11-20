import React, { useState } from 'react';
import { Lightbulb, RefreshCw, Send } from 'lucide-react';
import { Button } from '@/shared/components/atoms/Button';
import { Spinner } from '@/shared/components/atoms/Spinner';
import { Input } from '@/shared/components/atoms/Input';
import { SuggestionCard } from './SuggestionCard';
import { useInsights } from '../hooks/useInsights';

/**
 * Main insights panel with AI-generated suggestions and Q&A.
 */
export const InsightPanel: React.FC = () => {
  const {
    insights,
    modelUsed,
    isLoading,
    regenerate,
    askQuestion,
    questionAnswer,
    isAsking,
  } = useInsights();

  const [question, setQuestion] = useState('');

  const handleAsk = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim().length >= 10) {
      askQuestion(question.trim());
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Lightbulb size={24} className="text-yellow-500" />
          <h2 className="text-xl font-bold text-gray-900">AI Insights</h2>
        </div>
        <div className="flex items-center gap-3">
          {modelUsed && (
            <span className="text-xs text-gray-400">Powered by {modelUsed}</span>
          )}
          <Button variant="ghost" size="sm" onClick={() => regenerate()}>
            <RefreshCw size={16} className="mr-1" />
            Regenerate
          </Button>
        </div>
      </div>

      {isLoading ? (
        <Spinner size="lg" className="py-12" />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {insights.map((insight, idx) => (
            <SuggestionCard key={idx} insight={insight} />
          ))}
        </div>
      )}

      {/* Q&A Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <h3 className="text-base font-semibold text-gray-900 mb-4">
          Ask about your business
        </h3>

        <form onSubmit={handleAsk} className="flex gap-3">
          <div className="flex-1">
            <Input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What's causing our churn rate to increase?"
              minLength={10}
            />
          </div>
          <Button type="submit" isLoading={isAsking}>
            <Send size={16} />
          </Button>
        </form>

        {questionAnswer && (
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-gray-900">{questionAnswer.answer}</p>
            {questionAnswer.data_points_referenced.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {questionAnswer.data_points_referenced.map((dp, i) => (
                  <span key={i} className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
                    {dp}
                  </span>
                ))}
              </div>
            )}
            <p className="mt-2 text-xs text-gray-400">
              Confidence: {(questionAnswer.confidence_score * 100).toFixed(0)}%
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
