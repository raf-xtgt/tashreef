"use client";

import { useState, useEffect } from 'react';
import { FaCheckCircle, FaExclamationCircle } from 'react-icons/fa';
import { useUser } from '@/app/context/userContext';
import { useStateController } from '@/app/context/stateController';
import CardPrompt from '../cardPrompt/cardPrompt';
import { InferenceService } from '@/app/services/inferenceService';

export default function CardTools() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const { user } = useUser();
  const { setCardResponse } = useStateController();

  useEffect(() => {
    // Clear messages after 5 seconds
    if (successMessage || error) {
      const timer = setTimeout(() => {
        setSuccessMessage(null);
        setError(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage, error]);

  const handleEInvitationCardGeneration = async (userPayload: any) => {
    try {
      setLoading(true);
      setError(null);
      setSuccessMessage(null);

      const payload = {
        text: userPayload.description
      };
      const eInvitationDraftResponse = await InferenceService.generateEInvitationCard(payload);

      setCardResponse(eInvitationDraftResponse);
      setSuccessMessage('Card generated successfully!');
    } catch (err) {
      setError('Failed to generate card. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      {/* Status Messages */}
      <div className="space-y-3 mb-6">
        {loading && (
          <div className="p-4 bg-blue-50 border border-blue-300 rounded-lg flex items-center gap-3">
            <div className="flex-shrink-0">
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-slate-600 border-t-transparent"></div>
            </div>
            <div>
              <p className="font-medium text-slate-800">Generating your card...</p>
              <p className="text-sm text-slate-600">This may take a few moments</p>
            </div>
          </div>
        )}

        {successMessage && (
          <div className="p-4 bg-emerald-50 border border-emerald-300 rounded-lg flex items-center gap-3">
            <FaCheckCircle className="text-emerald-600 text-xl flex-shrink-0" />
            <div>
              <p className="font-medium text-slate-800">{successMessage}</p>
              <p className="text-sm text-slate-600">Check the preview panel</p>
            </div>
          </div>
        )}

        {error && (
          <div className="p-4 bg-red-50 border border-red-300 rounded-lg flex items-center gap-3">
            <FaExclamationCircle className="text-red-600 text-xl flex-shrink-0" />
            <div>
              <p className="font-medium text-slate-800">{error}</p>
              <p className="text-sm text-slate-600">Please check your input and try again</p>
            </div>
          </div>
        )}
      </div>

      {/* Card Prompt Form */}
      <CardPrompt onSave={handleEInvitationCardGeneration} loading={loading} />
    </div>
  );
}