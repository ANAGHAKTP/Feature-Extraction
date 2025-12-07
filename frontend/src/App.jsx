import { useState } from 'react'
import axios from 'axios'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [processedImages, setProcessedImages] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [preview, setPreview] = useState(null)

  const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
      setProcessedImages(null)
      setError(null)
      setPreview(URL.createObjectURL(file))
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!")
      return
    }

    const formData = new FormData()
    formData.append("image", selectedFile)

    setLoading(true)
    setError(null)

    // Determine API URL (supports local dev and Vercel environment)
    let apiUrl;
    if (import.meta.env.VITE_API_URL) {
      apiUrl = `${import.meta.env.VITE_API_URL}/process`;
    } else if (import.meta.env.DEV) {
      apiUrl = 'http://localhost:5000/process';
    } else {
      apiUrl = '/process'; // Relative path for production with rewrites
    }

    try {
      const response = await axios.post(apiUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setProcessedImages(response.data)
    } catch (err) {
      console.error(err)
      setError("Error processing image. Ensure the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Feature Extraction Engine</h1>
      <p style={{ color: 'var(--text-secondary)', marginTop: '-1rem', marginBottom: '2rem' }}>
        Advanced Canny Edge Detection & Contour Analysis
      </p>

      <div className="upload-section">
        {!preview ? (
          <>
            <div style={{ fontSize: '4rem', color: 'var(--text-secondary)', opacity: 0.5 }}>
              📷
            </div>
            <p className="file-label">Select an image to analyze</p>
          </>
        ) : (
          <img
            src={preview}
            alt="Preview"
            style={{ maxHeight: '200px', borderRadius: '0.5rem', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
          />
        )}

        <div className="file-input-wrapper">
          <button className="btn-upload" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
            {selectedFile ? 'Change File' : 'Choose File'}
          </button>
          <input
            type="file"
            onChange={handleFileChange}
            accept="image/*"
            className="file-input"
          />
        </div>

        {selectedFile && (
          <button
            className="btn-upload"
            onClick={handleUpload}
            disabled={loading}
            style={{ width: '100%', maxWidth: '300px' }}
          >
            {loading ? <div className="loading-spinner" style={{ width: '20px', height: '20px', margin: '0 auto', borderTopColor: 'white' }}></div> : "extract features ✨"}
          </button>
        )}
      </div>

      {error && <div className="error">{error}</div>}

      {processedImages && (
        <div className="results">
          <div className="image-card">
            <h3>Original Input</h3>
            <img src={processedImages.original} alt="Original" />
          </div>
          <div className="image-card">
            <h3>Edge Map</h3>
            <img src={processedImages.edges} alt="Edges" />
          </div>
          <div className="image-card">
            <h3>Contour Overlay</h3>
            <img src={processedImages.contours} alt="Contours" />
          </div>
        </div>
      )}
    </div>
  )
}

export default App
