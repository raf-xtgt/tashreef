"use client";

import CardTools from "../components/eCardEditor/cardTools/cardTools";

export default function CopilotWorkflow() {

  return (
    <div className="p-5 h-full bg-gradient-to-br from-gray-50 to-gray-100 overflow-y-auto overflow-x-hidden" >
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">E-Invitation Card maker</h1>
      </div>
      <div className="flex flex-col lg:flex-row gap-5 h-[calc(100%-6rem)]">
        {/* Image editing tools */}
        <div className="w-full lg:w-2/5 bg-white rounded-2xl shadow-lg p-1 border border-gray-200">
          <h1>Image editing tools</h1>
          <CardTools></CardTools>
        </div>

        {/* Main E-Invitation card display */}
        <div className="hidden lg:block w-3/5 bg-white rounded-2xl shadow-lg p-1 border border-gray-200">
          <h1>SVG appears here</h1>
        </div>

        {/* Mobile Editor Placeholder */}
        <div className="lg:hidden w-full bg-white rounded-2xl shadow-lg p-1 border border-gray-200 mb-5 h-96">
          <div className="p-4 h-full flex flex-col items-center justify-center text-center">
            <h3 className="text-lg font-medium text-gray-700 mb-2">Editor</h3>
            <p className="text-gray-500">Available on larger screens</p>
          </div>
        </div>


      </div>
    </div>
  );
}