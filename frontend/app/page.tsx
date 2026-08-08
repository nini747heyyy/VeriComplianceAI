'use client';
// Import React and the useState hook for managing component state
import React, { useState } from 'react';

// Main homepage component
export default function Home() {
  
  // State variable to store the user's query from the input field
  const [query, setQuery] = useState('');

  return (
    <main className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col items-center justify-center p-4 sm:p-6 md:p-12 font-sans antialiased selection:bg-indigo-500 selection:text-white">
      <div className="w-full max-w-4xl space-y-6">
        
         {/* Top Status Bar displaying AI engine status and compliance standards */}
        <header className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 rounded-xl bg-slate-900/50 border border-slate-800/80 backdrop-blur-xl shadow-sm">
         
          {/* Engine status indicator */}
          <div className="flex items-center space-x-2.5">
            <span className="relative flex h-2.5 w-2.5">
               
              {/* Animated green pulse indicating the engine is active */}
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                
              {/* Static green status dot */}
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
             
            {/* AI engine name and reliability mode */}
            <span className="text-xs font-mono font-medium tracking-wide text-slate-300">
              ENGINE: <span className="text-emerald-400 font-semibold">VERIGROUND-V4.2</span>
              <span className="text-slate-500 ml-1.5 hidden sm:inline">(ZERO-HALLUCINATION)</span>
            </span>
          </div>

          
          {/* Compliance certifications badge */}
          <div className="flex items-center space-x-2">
           
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
              SOC 2 & ISO 27001
            </span>
          </div>
        </header>

         {/* Main section displaying the AI-generated compliance response */}
        <section className="rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md p-6 shadow-2xl space-y-6">
           
          {/* AI response content */}
          <div className="flex items-start space-x-4">
             
            {/* Icon representing the AI engine */}
            <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shrink-0">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
             
            
            {/* Generated compliance explanation */}
            <div className="space-y-4 text-slate-200 text-sm md:text-base leading-relaxed">
              <p>
                Our analysis of the newly updated <span className="text-white font-semibold underline decoration-indigo-500/50 underline-offset-4">EU AI Act Article 14</span> indicates mandatory human oversight for high-risk AI deployments. Personnel assigned oversight duties must have the necessary competence, training, and authority.
              </p>

             {/* Confidence score and source citation badges */}
              <div className="flex flex-wrap items-center gap-2 pt-1">
                
                {/* Indicates how strongly the answer is grounded in source documents */}
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  98% Grounded
                </span>
                  
                {/* Citation linking to the EU AI Act source */}
                <a href="#" className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-mono bg-slate-800/80 hover:bg-slate-700 text-indigo-300 border border-slate-700/80 transition-all hover:border-indigo-500/40">
                  <span>📄 [EU_AI_Act_Final_Text_2025.pdf • p.88]</span>
                </a>
                  
                
                {/* Citation linking to the internal governance policy */}
                <a href="#" className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-mono bg-slate-800/80 hover:bg-slate-700 text-indigo-300 border border-slate-700/80 transition-all hover:border-indigo-500/40">
                  <span>📄 [Internal_AI_Governance_Policy.pdf • p.12]</span>
                </a>
              </div>
            </div>
          </div>

           
          
          {/* Query input form where users ask compliance-related questions */}
          <form onSubmit={(e) => e.preventDefault()} className="relative pt-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything about your policies, SOC2 manuals, or contract clauses..."
              className="w-full bg-slate-950/90 border border-slate-800 rounded-xl px-4 py-3.5 pr-36 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all shadow-inner"
            />
            
            
            {/* Button used to submit the user's question */}
            <button 
              type="submit"
              className="absolute right-2 top-3.5 bottom-2 px-4 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition-all shadow-md shadow-indigo-600/20 active:scale-95"
            >
              Generate Answer
            </button>
          </form>
        </section>

            {/* Panel explaining how evidence verification works */}
        <section className="rounded-2xl bg-slate-900/30 border border-slate-800/80 p-5 space-y-3">
            
          
          {/* Panel heading */}
          <div className="flex items-center justify-between pb-3 border-b border-slate-800/60">
            <div className="flex items-center space-x-2">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h2 className="text-xs font-semibold tracking-wider text-slate-300 uppercase">Evidence Verification Panel</h2>
            </div>
             
            
            
            {/* Indicates that the displayed evidence comes from verified audit sources */}
            <span className="text-[10px] font-mono text-slate-500 tracking-widest uppercase">Verified Audit Source</span>
          </div>
          
          
          {/* Instructions for inspecting source citations */}
          <p className="text-xs text-slate-400 leading-relaxed">
            Click any citation badge in the chat answer to inspect exact ground-truth source context.
          </p>
        </section>

      </div>
    </main>
  );
}
