import React, { useState } from "react";
import { detectPerson } from "../api";

const Detect = ({ uploadedFilePath }) => {
    const [detectionResult, setDetectionResult] = useState("");
    const [agedImage, setAgedImage] = useState("");

    // const handleDetect = async () => {
    //     if (!uploadedFilePath) {
    //         setDetectionResult("No image uploaded.");
    //         return;
    //     }

    //     const response = await detectPerson(uploadedFilePath);
    //     setDetectionResult(response.message);

    //     if (response.aged_image) {
    //         setAgedImage(`http://127.0.0.1:5000/${response.aged_image}`);
    //     }
    // };

    const handleDetect = async () => {
        if (!uploadedFilePath) {
            // Open webcam capture if no image is uploaded
            const videoElement = document.createElement("video");
            videoElement.setAttribute("autoplay", true);
            document.body.appendChild(videoElement);
    
            navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
                videoElement.srcObject = stream;
            });
    
            return;
        }
    
        const response = await detectPerson(uploadedFilePath);
        setDetectionResult(response.message);
    
        if (response.aged_image) {
            setAgedImage(`http://127.0.0.1:5000/${response.aged_image}`);
        }
    };
    

    return (
        <div>
            <button onClick={handleDetect}>Detect Missing Person</button>
            <p>{detectionResult}</p>
            {agedImage && <img src={agedImage} alt="Aged Face" />}
        </div>
    );
};

export default Detect;
