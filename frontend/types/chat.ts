// Defines the structure of a citation used to reference source documents
export interface Citation {
  // Unique identifier for the citation
  id: string;
  // Identifier of the document containing the evidence
  documentId: string;
   // Name or title of the source document
  documentTitle: string;
  // Page number where the relevant information is located
  pageNumber: number;
  // Exact section of text extracted from the source document

  exactSnippet: string;
  // Score indicating how relevant the citation is to the user's query

  relevanceScore: number;
}

// Defines the structure of a message in the compliance chat
export interface ChatMessage {
   // Unique identifier for the chat message
  id: string;
   // Specifies whether the message was sent by the user or AI assistant
  role: 'user' | 'assistant';
  // Actual text content of the message

  content: string;
   // Optional confidence score indicating how reliable the AI response is
  confidenceScore?: number;
   // Optional flag indicating whether the response is supported by source evidence
  isGrounded?: boolean;
  // Optional list of citations supporting the AI response
  citations?: Citation[];
}

// Defines the structure of an AI-generated chat response
export interface ChatResponse {
  // Unique identifier for the response
  id: string;
  // This response can only come from the AI assistant
  role: 'assistant';
   // Generated response content
  content: string;
   // Confidence score associated with the AI-generated answer
  confidenceScore: number;
  // Source citations used to support the response
  citations: Citation[];
}
