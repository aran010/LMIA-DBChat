'use client';
import { useState, useRef, useEffect } from 'react';
import styles from './page.module.css';
import Link from 'next/link';

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am the Offline AI Knowledge Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      // Mocking response
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: 'This is a mock response from the RAG pipeline. ' + userMessage 
        }]);
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <h1 className={styles.title}>Knowledge Assistant</h1>
        <Link href="/admin" className={styles.adminLink}>Admin</Link>
      </header>

      <div className={styles.chatContainer}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`${styles.messageRow} ${msg.role === 'user' ? styles.user : styles.assistant}`}>
            <div className={styles.messageContent}>
              <div className={`${styles.avatar} ${msg.role === 'user' ? styles.user : styles.assistant}`}>
                {msg.role === 'user' ? 'U' : 'AI'}
              </div>
              <div className={styles.messageText}>
                <p>{msg.content}</p>
                {msg.role === 'assistant' && idx > 0 && (
                   <div className={styles.citationCard}>
                     Source: sample_policy.pdf
                   </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className={`${styles.messageRow} ${styles.assistant}`}>
             <div className={styles.messageContent}>
               <div className={`${styles.avatar} ${styles.assistant}`}>AI</div>
               <div className={styles.messageText}>
                 <p className="animate-pulse">...</p>
               </div>
             </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>

      <div className={styles.inputWrapper}>
        <form className={styles.inputArea} onSubmit={handleSend}>
          <textarea 
            className={styles.input}
            placeholder="Message Knowledge Assistant..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            rows={1}
          />
          <button type="submit" className={styles.sendButton} disabled={!input.trim() || isLoading}>
            ↑
          </button>
        </form>
      </div>
    </main>
  );
}
