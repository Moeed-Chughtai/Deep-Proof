"use client";

import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [predictions, setPredictions] = useState<number[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("video", file);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to fetch predictions");
      }

      const data = await response.json();
      setPredictions(data.predictions);
    } catch (error) {
      console.log(error);
      setError("An error occurred while uploading the video.");
    } finally {
      setLoading(false);
    }
  };

  const averagePrediction = predictions.length > 0
    ? predictions.reduce((acc, val) => acc + val, 0) / predictions.length
    : 0;

  const percentage = Math.min(Math.max(0, averagePrediction * 100), 100);
  const classification = percentage > 50 ? "Deepfake" : "Real";

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-600">
      <div className="w-full max-w-md p-8 bg-gray-800 rounded-lg shadow-2xl">
        <h1 className="text-3xl font-bold text-center mb-6 text-white">Upload and Predict</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="flex flex-col items-center">
            <label htmlFor="file-upload" className="block text-lg font-medium text-gray-300">
              Choose a video file
            </label>
            <input
              id="file-upload"
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="mt-4 border border-gray-600 rounded-lg p-2 cursor-pointer bg-gray-700 text-gray-300"
            />
          </div>
          <div className="flex justify-center">
            <button
              type="submit"
              className="bg-pink-500 text-white py-2 px-8 rounded-lg hover:bg-pink-600 transition-colors"
              disabled={loading}
            >
              {loading ? "Processing..." : "Submit"}
            </button>
          </div>
        </form>

        {error && <p className="mt-4 text-red-500 text-center">{error}</p>}

        {predictions.length > 0 && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold text-white mb-2">Prediction:</h2>
            <p className={`text-4xl font-extrabold mb-4 text-center ${classification === "Deepfake" ? "text-red-500" : "text-green-500"}`}>{classification}</p>
            <div className="w-full bg-gray-700 rounded-full h-8 mb-4">
              <div
                className="bg-pink-500 h-8 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${percentage}%` }}
              ></div>
            </div>
            <p className="text-lg text-gray-300 text-center">{percentage.toFixed(2)}%</p>
          </div>
        )}
      </div>
    </div>
  );
}
