"use client";
import { useState } from 'react';
import { FaMagic } from 'react-icons/fa';

interface CardPromptProps {
    onSave: (data: any) => void;
  }

const initialFormData = {
    guid:'',
    description: '',
    created_date: '',
    last_update: ''
  };
  

export default function CardPrompt({onSave}:CardPromptProps) {
  const [formData, setFormData] = useState<any>(initialFormData);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev:any) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);

    console.log("the prompt")
  };


  return (
    <div className="flex items-center justify-center">
        <div className="p-6">
          <form onSubmit={handleSubmit}>
            <div className="space-y-5 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Prompt</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-y min-h-[120px]"
                  placeholder="Enter your card idea..."
                  required
                ></textarea>
              </div>
            </div>
            <div className="flex justify-end space-x-3 pt-4  border-gray-200">
              <button
                type="submit"
                className="px-5 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors flex items-center gap-2"
              >
                <FaMagic /> Inference
              </button>
            </div>

          </form>
        </div>
    </div>
  );
}