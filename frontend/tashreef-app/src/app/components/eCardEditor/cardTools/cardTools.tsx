"use client";

import { useState, useEffect } from 'react';
import { FaSearch, FaFolderOpen, FaCheckCircle} from 'react-icons/fa';
import { useUser } from '@/app/context/userContext';
import CardPrompt from '../cardPrompt/cardPrompt';
import { InferenceService } from '@/app/services/inferenceService';
import { CardPromptModel } from '@/app/models/cardPromptModel';

export default function CardTools() {
  const [search, setSearch] = useState("");
  const [error, setError] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const { user } = useUser();

  // Load Sessions on component mount
  useEffect(() => {
    
  }, [user?.guid]);



  const handleEInvitationCardGeneration = async (userPayload:any ) => {
    try {
      setLoading(true);
      setError(null);
      setSuccessMessage(null);

      console.log("userPayload", userPayload)
      let payload = {
        "text":userPayload.description
      }
      const eInvitationDraftResponse = await InferenceService.generateEInvitationCard(payload);
      
      
    } catch (err) {
      setError('Failed to create session');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 rounded-xl p-4 h-full flex flex-col">
      <div className="h-full flex flex-col">
        {/* Loading Message */}
        {loading && (
          <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg flex items-center gap-2 text-blue-700">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-700"></div>
            <span>Retrieving Sessions...</span>
          </div>
        )}

        {/* Success Message */}
        {successMessage && (
          <div className="mb-3 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2 text-green-700">
            <FaCheckCircle />
            <span>{successMessage}</span>
          </div>
        )}


        {/* Channels Section (Sessions Dropdown) */}
        <div className="pb-4 border-b border-gray-200">
          <h2 className="font-bold text-lg mb-3">
            <div className="flex items-center gap-2">
              <CardPrompt
                onSave={handleEInvitationCardGeneration}
              ></CardPrompt> 
            </div>


          </h2>

          {/* Search input */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FaSearch className="text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search sessions..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

        </div>


      </div>

    </div>

  );
}