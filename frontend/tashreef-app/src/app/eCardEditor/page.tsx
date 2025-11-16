"use client";

import CardDisplay from "../components/eCardEditor/cardDisplay/cardDisplay";
import CardTools from "../components/eCardEditor/cardTools/cardTools";

export default function CopilotWorkflow() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-stone-50 to-neutral-100">
      <div className="max-w-[1800px] mx-auto p-6 lg:p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl lg:text-5xl font-bold text-slate-800 mb-2">
            E-Invitation Card Maker
          </h1>
          <p className="text-slate-600 text-lg">Create stunning mathematical pattern-based invitation cards</p>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 lg:gap-8">
          {/* Card Tools Panel */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
              <div className="bg-slate-700 px-6 py-4 border-b border-slate-300">
                <h2 className="text-xl font-semibold text-white">Design Studio</h2>
              </div>
              <CardTools />
            </div>
          </div>

          {/* Card Display Panel */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden h-[600px] lg:h-[calc(100vh-200px)]">
              <div className="bg-slate-700 px-6 py-4 border-b border-slate-300">
                <h2 className="text-xl font-semibold text-white">Preview</h2>
              </div>
              <CardDisplay />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}