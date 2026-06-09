'use client';
import styles from './page.module.css';
import Link from 'next/link';

export default function Admin() {
  const triggerReindex = async () => {
    // In a real implementation this would call the backend API
    alert('Re-indexing triggered successfully.');
  };

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <h1 className={styles.title}>Admin Dashboard</h1>
        <Link href="/" className={styles.backLink}>&larr; Back to Chat</Link>
      </header>

      <div className={styles.grid}>
        <div className={`${styles.card} glass-panel animate-fade-in`}>
          <h2 className={styles.cardTitle}>System Status</h2>
          <div className={styles.stat}>Online</div>
          <div className={styles.statLabel}>Backend and RAG pipeline are connected</div>
        </div>
        
        <div className={`${styles.card} glass-panel animate-fade-in`} style={{ animationDelay: '0.1s' }}>
          <h2 className={styles.cardTitle}>Index Statistics</h2>
          <div className={styles.stat}>1,248</div>
          <div className={styles.statLabel}>Total document chunks indexed</div>
        </div>

        <div className={`${styles.card} glass-panel animate-fade-in`} style={{ animationDelay: '0.2s' }}>
          <h2 className={styles.cardTitle}>Data Sources</h2>
          <p className={styles.statLabel}>2 Database Connections</p>
          <p className={styles.statLabel}>1 Document Folder</p>
          <button className={styles.button} onClick={triggerReindex}>
            Trigger Full Re-index
          </button>
        </div>
      </div>
    </main>
  );
}
