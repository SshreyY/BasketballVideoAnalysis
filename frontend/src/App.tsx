import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [outputVideoUrl, setOutputVideoUrl] = useState('');

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setSelectedFile(file);
      setMessage('');
    } else {
      setMessage('Please select a valid video file');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a video file first');
      return;
    }

    setUploading(true);
    setMessage('Uploading and processing video...');

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/upload-video', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      
      if (response.ok) {
        setMessage(result.message);
        if (result.output_filename) {
          const videoUrl = `http://localhost:8000/output-video/${result.output_filename}`;
          setOutputVideoUrl(videoUrl);
        }
      } else {
        setMessage(`Error: ${result.detail || 'Upload failed'}`);
      }
    } catch (error) {
      setMessage(`Error: ${error instanceof Error ? error.message : 'Upload failed'}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏀 Basketball Video Analysis</h1>
        <p>Upload a basketball video to analyze player movements, ball tracking, and tactical insights</p>
      </header>
      
      <main className="App-main">
        <div className="upload-section">
          <h2>Video Upload</h2>
          <div className="file-input-container">
            <input
              type="file"
              accept="video/*"
              onChange={handleFileSelect}
              className="file-input"
            />
            <button 
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
              className="upload-button"
            >
              {uploading ? 'Processing...' : 'Upload & Analyze'}
            </button>
          </div>
          
          {selectedFile && (
            <p className="file-info">Selected: {selectedFile.name}</p>
          )}
          
          {message && (
            <p className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
              {message}
            </p>
          )}
        </div>

        {outputVideoUrl && (
          <div className="output-section">
            <h2>Processed Video</h2>
            <div className="video-container">
              <video 
                controls 
                width="100%" 
                className="output-video"
              >
                <source src={outputVideoUrl} type="video/mp4" />
                <source src={outputVideoUrl} type="video/avi" />
                <source src={outputVideoUrl} type="video/x-msvideo" />
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="download-container">
              <a 
                href={outputVideoUrl.replace('/output-video/', '/download-video/')} 
                download 
                className="download-link"
              >
                Download Processed Video
              </a>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
