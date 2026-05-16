import React, { useState } from 'react'
// import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://driver-behaviour-dev-alb-2021137735.ap-southeast-2.elb.amazonaws.com';

interface PredictionResponse {
  label: string;
  confidence: number;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    setFile(selected);
    setPrediction(null);
    setError(null);

    if (selected) {
      setPreviewUrl(URL.createObjectURL(selected));
    } else {
      setPreviewUrl(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select an image first.');
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch(`${API_BASE_URL}/api/v1/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
      }

      const data: PredictionResponse = await res.json();
      setPrediction(data);
    } catch (err: any) {
      setError(err.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Driver Behaviour Classifier</h1>
        <p style={styles.subtitle}>Upload an image to get a real-time prediction.</p>

        <form onSubmit={handleSubmit} style={styles.form}>
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button type="submit" disabled={loading || !file} style={styles.button}>
            {loading ? 'Predicting…' : 'Run Prediction'}
          </button>
        </form>

        {previewUrl && (
          <div style={styles.previewContainer}>
            <p style={styles.sectionTitle}>Preview</p>
            <img src={previewUrl} alt="preview" style={styles.previewImage} />
          </div>
        )}

        {error && (
          <div style={styles.error}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {prediction && (
          <div style={styles.result}>
            <p style={styles.sectionTitle}>Prediction</p>
            <p><strong>Label:</strong> {prediction.label}</p>
            <p><strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(2)}%</p>
          </div>
        )}
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: '100vh',
    padding: '2rem',
    background: '#0f172a',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    color: '#e5e7eb',
  },
  card: {
    width: '100%',
    maxWidth: '720px',
    background: '#020617',
    borderRadius: '1rem',
    padding: '2rem',
    border: '1px solid #1f2937',
  },
  title: { marginBottom: '0.5rem', fontSize: '1.8rem' },
  subtitle: { marginBottom: '1.5rem', color: '#9ca3af' },
  form: { display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' },
  button: {
    background: '#2563eb',
    color: '#e5e7eb',
    border: 'none',
    padding: '0.6rem 1.2rem',
    borderRadius: '999px',
    cursor: 'pointer',
    fontWeight: 600,
  },
  previewContainer: { marginBottom: '1.5rem' },
  previewImage: {
    maxWidth: '100%',
    borderRadius: '0.75rem',
    border: '1px solid #1f2937',
  },
  sectionTitle: { marginBottom: '0.5rem', fontWeight: 600 },
  error: {
    marginTop: '1rem',
    padding: '0.75rem 1rem',
    borderRadius: '0.75rem',
    background: '#7f1d1d',
    color: '#fecaca',
  },
  result: {
    marginTop: '1rem',
    padding: '0.75rem 1rem',
    borderRadius: '0.75rem',
    border: '1px solid #1f2937',
  },
};

export default App
