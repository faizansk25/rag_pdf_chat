import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { useDropzone } from 'react-dropzone';
import { Send, Upload, FileText, Loader2 } from 'lucide-react';

const API_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hello! Upload some PDFs and ask me anything about them.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const onDrop = async (acceptedFiles) => {
    setUploading(true);
    const formData = new FormData();
    acceptedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setFiles(prev => [...prev, ...acceptedFiles]);
      setMessages(prev => [...prev, { role: 'ai', content: `Successfully uploaded ${acceptedFiles.length} files.` }]);
    } catch (error) {
      console.error('Upload failed:', error);
      setMessages(prev => [...prev, { role: 'ai', content: 'Failed to upload files. Please try again.' }]);
    } finally {
      setUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: {'application/pdf': ['.pdf']} });

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const chatHistory = messages.map(m => [m.role === 'user' ? m.content : '', m.role === 'ai' ? m.content : ''])
                                  .filter(pair => pair[0] || pair[1]); // Simple formatting, backend handles better

      const response = await axios.post(`${API_URL}/chat`, {
        question: userMessage.content,
        chat_history: chatHistory
      });

      const aiMessage = { 
        role: 'ai', 
        content: response.data.answer,
        sources: response.data.sources 
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Chat failed:', error);
      setMessages(prev => [...prev, { role: 'ai', content: 'Sorry, I encountered an error. Please check your API key and backend connection.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <h2>RAG PDF Chat</h2>
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          {uploading ? (
            <Loader2 className="animate-spin" />
          ) : (
            <>
              <Upload size={24} />
              <p>Drop PDFs here</p>
            </>
          )}
        </div>
        <div className="file-list">
          <h3>Uploaded Files</h3>
          {files.map((file, i) => (
            <div key={i} className="file-item">
              <FileText size={16} />
              <span className="truncate">{file.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="main-chat">
        <div className="chat-history">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <ReactMarkdown>{msg.content}</ReactMarkdown>
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  Sources: {msg.sources.join(', ')}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="message ai">
              <Loader2 className="animate-spin" size={20} />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask a question about your documents..."
            disabled={isLoading}
          />
          <button onClick={sendMessage} disabled={isLoading || !input.trim()}>
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
