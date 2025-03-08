// import React, { useRef, useState } from "react";
// import axios from "axios";

// function Camera() {
//     const videoRef = useRef(null);
//     const [message, setMessage] = useState("");

//     const captureImage = async () => {
//         const canvas = document.createElement("canvas");
//         const context = canvas.getContext("2d");
//         canvas.width = videoRef.current.videoWidth;
//         canvas.height = videoRef.current.videoHeight;
//         context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

//         canvas.toBlob(async (blob) => {
//             const formData = new FormData();
//             formData.append("image", blob, "captured.jpg");

//             const response = await axios.post("http://127.0.0.1:5000/detect", formData);
//             setMessage(response.data.match ? "Person Found!" : "No Match Found.");
//         });
//     };

//     return (
//         <div>
//             <h2>Live Camera Scan</h2>
//             <video ref={videoRef} autoPlay></video>
//             <button onClick={captureImage}>Scan</button>
//             <p>{message}</p>
//         </div>
//     );
// }

// export default Camera;





import React, { useRef, useState, useEffect } from "react";
import axios from "axios";

function Camera() {
    const videoRef = useRef(null);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const startCamera = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            } catch (error) {
                console.error("Error accessing camera:", error);
                setMessage("Camera access denied or unavailable.");
            }
        };

        startCamera();
    }, []);

    const captureImage = async () => {
        if (!videoRef.current) return;

        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append("image", blob, "captured.jpg");

            try {
                const response = await axios.post("http://127.0.0.1:5000/detect", formData);
                setMessage(response.data.match ? "Person Found!" : "No Match Found.");
            } catch (error) {
                console.error("Error sending image to backend:", error);
                setMessage("Error processing image.");
            }
        });
    };

    return (
        <div>
            <h2>Live Camera Scan</h2>
            <video ref={videoRef} autoPlay playsInline></video>
            <button onClick={captureImage}>Scan</button>
            <p>{message}</p>
        </div>
    );
}

export default Camera;
