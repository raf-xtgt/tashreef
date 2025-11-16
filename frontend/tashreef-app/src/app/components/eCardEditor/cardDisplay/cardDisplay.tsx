"use client";

import { useStateController } from '@/app/context/stateController';
import { FaImage } from 'react-icons/fa';

export default function CardDisplay() {
    const { cardResponse } = useStateController();

    return (
        <div className="h-[calc(100%-4rem)] flex items-center justify-center p-4 bg-slate-50 overflow-auto">
            {cardResponse?.card_svg ? (
                <div className="w-full h-full flex items-center justify-center">
                    <div
                        dangerouslySetInnerHTML={{ __html: cardResponse.card_svg }}
                        className="[&>svg]:w-full [&>svg]:h-full [&>svg]:object-contain rounded-lg shadow-xl border border-slate-200 bg-white p-2"
                    />
                </div>
            ) : (
                <div className="text-center">
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-slate-100 mb-6">
                        <FaImage className="text-3xl text-slate-400" />
                    </div>
                    <h3 className="text-xl font-semibold text-slate-700 mb-3">No Card Yet</h3>
                    <p className="text-slate-500 max-w-md mx-auto leading-relaxed">
                        Enter a creative prompt in the Design Studio to generate your unique mathematical pattern-based e-invitation card
                    </p>
                </div>
            )}
        </div>
    );
}