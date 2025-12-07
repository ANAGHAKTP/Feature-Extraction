import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [processedImages, setProcessedImages] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0])
    setProcessedImages(null)
    setError(null)
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

    try {
      const response = await axios.post('http://localhost:5000/process', formData, {
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
      <h1>Image Feature Extraction</h1>

      <div className="upload-section">
        <input type="file" onChange={handleFileChange} accept="image/*" />
        <button onClick={handleUpload} disabled={!selectedFile || loading}>
          {loading ? "Processing..." : "Upload & Process"}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {processedImages && (
        <div className="results">
          <div className="image-card">
            <h3>Original Image</h3>
            <img src={processedImages.original} alt="Original" />
          </div>
          <div className="image-card">
            <h3>Edges</h3>
            <img src={processedImages.edges} alt="Edges" />
          </div>
          <div className="image-card">
            <h3>Contours</h3>
            <img src={processedImages.contours} alt="Contours" />
          </div>
        </div>
      )}
    </div>
  )
}

export default App
