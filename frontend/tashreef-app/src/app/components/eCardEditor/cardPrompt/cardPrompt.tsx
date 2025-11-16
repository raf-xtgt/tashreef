"use client";
import { useState } from 'react';
import { FaMagic, FaLightbulb } from 'react-icons/fa';

interface CardPromptProps {
  onSave: (data: any) => void;
  loading?: boolean;
}

const initialFormData = {
  guid: '',
  description: '',
  created_date: '',
  last_update: ''
};

const examplePrompts = [
  "Create a wedding invitation with elegant Islamic geometric patterns in gold and navy blue",
  "Design a birthday card with fractal patterns inspired by Moroccan architecture",
  "Generate a formal event invitation with tessellated patterns in emerald and silver"
];

export default function CardPrompt({ onSave, loading = false }: CardPromptProps) {
  const [formData, setFormData] = useState<any>(initialFormData);
  const [charCount, setCharCount] = useState(0);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setCharCount(value.length);
    setFormData((prev: any) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!loading && formData.description.trim()) {
      onSave(formData);
    }
  };

  const handleExampleClick = (example: string) => {
    setFormData((prev: any) => ({
      ...prev,
      description: example
    }));
    setCharCount(example.length);
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Prompt Input */}
        <div>
          <label className="block text-sm font-semibold text-slate-800 mb-3">
            Describe Your Card
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            disabled={loading}
            className="w-full p-4 border-2 border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-slate-400 resize-none transition-all duration-200 disabled:bg-slate-50 disabled:cursor-not-allowed"
            placeholder="Describe the style, colors, and theme for your e-invitation card..."
            rows={6}
            required
            maxLength={500}
          />
          <div className="flex justify-between items-center mt-2">
            <p className="text-xs text-slate-500">Be specific about patterns, colors, and occasion</p>
            <span className={`text-xs font-medium ${charCount > 450 ? 'text-amber-600' : 'text-slate-400'}`}>
              {charCount}/500
            </span>
          </div>
        </div>

        {/* Example Prompts */}
        <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
          <div className="flex items-center gap-2 mb-3">
            <FaLightbulb className="text-amber-500" />
            <h4 className="text-sm font-semibold text-slate-800">Need inspiration?</h4>
          </div>
          <div className="space-y-2">
            {examplePrompts.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => handleExampleClick(example)}
                disabled={loading}
                className="w-full text-left p-3 bg-white rounded-lg text-sm text-slate-700 hover:bg-slate-100 hover:border-slate-300 transition-all duration-200 border border-slate-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {/* Generate Button */}
        <button
          type="submit"
          disabled={loading || !formData.description.trim()}
          className="w-full py-4 bg-slate-700 text-white rounded-lg font-semibold hover:bg-slate-800 transition-all duration-200 flex items-center justify-center gap-3 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-md"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
              <span>Generating...</span>
            </>
          ) : (
            <>
              <FaMagic className="text-lg" />
              <span>Generate Card</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}