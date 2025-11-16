"use client";

import { useStateController } from '@/app/context/stateController';

export default function CardDisplay() {
  const { cardResponse } = useStateController();

  return (
    <div className="h-full flex items-center justify-center p-4 bg-gray-50">
      {cardResponse?.card_svg ? (
        <div className="h-full flex items-center justify-center">
          <div 
            dangerouslySetInnerHTML={{ __html: cardResponse.card_svg }}
            className="[&>svg]:h-full [&>svg]:w-auto [&>svg]:max-h-[calc(100vh-12rem)] border border-gray-300 rounded-lg shadow-lg bg-white"
          />
        </div>
      ) : (
        <div className="text-center text-gray-500">
          <p className="text-lg">No card generated yet</p>
          <p className="text-sm mt-2">Enter a prompt to generate your e-invitation card</p>
        </div>
      )}
    </div>
  );
}