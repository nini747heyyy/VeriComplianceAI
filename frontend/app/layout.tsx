// Import React to use React types and functionality
import React from 'react';
// Ignore TypeScript checking for the CSS import
// @ts-ignore
import './globals.css';

// Define the metadata for the application
// This information is used for the webpage title and description
export const metadata = {
  title: 'VeriCompliance AI',
  description: 'Zero-Hallucination Compliance & Governance Engine',
};

// Root layout component that wraps all pages in the application
export default function RootLayout({
   // Render the content of the current page
  children,
}: {
  // Define children as valid React elements
  children: React.ReactNode;
}) {
  return (
    // Set the document language to English and enable dark mode
    <html lang="en" className="dark">
      {/* Apply global styling to the webpage body */}
      <body className="bg-slate-950 text-slate-100 antialiased min-h-screen">
         {/* Render the page content inside the layout */}
        {children}
      </body>
    </html>
  );
}
