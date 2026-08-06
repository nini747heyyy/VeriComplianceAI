export interface Citation {
  id: string;
  documentId: string;
  documentTitle: string;
  pageNumber: number;
  exactSnippet: string;
  relevanceScore: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  confidenceScore?: number;
  isGrounded?: boolean;
  citations?: Citation[];
}

export interface ChatResponse {
  id: string;
  role: 'assistant';
  content: string;
  confidenceScore: number;
  citations: Citation[];
}