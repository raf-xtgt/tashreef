"use client";

import { useStateController } from '@/app/context/stateController';
import { FaImage } from 'react-icons/fa';

export default function CardDisplay() {
    const { cardResponse } = useStateController();

    return (
        /* This parent container is tall, provides vertical centering (items-center) 
          and prevents any overflow (overflow-hidden) 
        */
        <div className="h-[calc(100%-4rem)] flex items-center justify-center p-4 bg-slate-50 overflow-hidden">
            {cardResponse?.card_svg ? (
                /* This is the card itself. We removed the extra wrapper.
                  It is set to w-full (to fill the parent's width).
                  The flex parent above will auto-center it vertically.
                */
                <div
                    dangerouslySetInnerHTML={{ __html: cardResponse.card_svg }}
                    /* This is the key:
                      1. w-full: The card container fills the available width.
                      2. [&>svg]:w-full: The SVG element inside fills its container's width.
                      3. [&>svg]:h-auto: The SVG's height adjusts automatically to maintain its aspect ratio.
                    */
                    className="w-full [&>svg]:w-full [&>svg]:h-auto rounded-lg shadow-xl border border-slate-200 bg-white p-2"
                />
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