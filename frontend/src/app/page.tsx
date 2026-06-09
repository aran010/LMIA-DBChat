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
  const [token, setToken] = useState<string | null>(null);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Auto-login to get JWT token for testing
    const fetchToken = async () => {
      try {
        const formData = new URLSearchParams();
        formData.append('username', 'user');
        formData.append('password', 'user123');

        const res = await fetch('http://localhost:8000/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData.toString()
        });
        if (res.ok) {
          const data = await res.json();
          setToken(data.access_token);
        } else {
          console.error("Failed to authenticate");
        }
      } catch (err) {
        console.error("Auth error", err);
      }
    };
    fetchToken();
  }, []);

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

    if (!token) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Not authenticated. Is the backend running?' }]);
      setIsLoading(false);
      return;
    }

    try {
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      const res = await fetch('http://localhost:8000/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message: userMessage, stream: true })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const reader = res.body?.getReader();
      const decoder = new TextDecoder('utf-8');

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              let text = line.replace('data: ', '');
              
              setMessages(prev => {
                const newMsgs = [...prev];
                newMsgs[newMsgs.length - 1].content += text;
                return newMsgs;
              });
            }
          }
        }
      }
      
    } catch (error) {
      console.error(error);
      setMessages(prev => {
        const newMsgs = [...prev];
        if (newMsgs[newMsgs.length - 1].content === '') {
           newMsgs[newMsgs.length - 1].content = "Error: Failed to connect to the backend or AI model.";
        }
        return newMsgs;
      });
    } finally {
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
                {msg.role === 'assistant' && idx > 0 && msg.content !== '' && !msg.content.startsWith('Error:') && !isLoading && (
                   <div className={styles.citationCard}>
                     Source: sample_policy.pdf
                   </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {isLoading && messages[messages.length - 1].role === 'user' && (
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
