import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
    const [image, setImage] = useState(null);
    const [message, setMessage] = useState("");

    const handleUpload = async () => {
        if (!image) return;

        const formData = new FormData();
        formData.append("image", image);

        const response = await axios.post("http://127.0.0.1:5000/upload", formData);
        setMessage(response.data.message);
    };

    return (
        <div>
            <h2>Upload Missing Person Image</h2>
            <input type="file" onChange={(e) => setImage(e.target.files[0])} />
            <button onClick={handleUpload}>Upload</button>
            <p>{message}</p>
        </div>
    );
}

export default UploadForm;
