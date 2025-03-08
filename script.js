// async function uploadImage() {
//     let fileInput = document.getElementById("imageInput");
//     if (fileInput.files.length === 0) {
//         alert("Please select an image first!");
//         return;
//     }

//     let formData = new FormData();
//     formData.append("image", fileInput.files[0]);

//     try {
//         // Upload image
//         let uploadResponse = await fetch("/upload", {
//             method: "POST",
//             body: formData,
//         });

//         let uploadData = await uploadResponse.json();
//         if (uploadData.error) {
//             alert(uploadData.error);
//             return;
//         }

//         // Face detection
//         let detectResponse = await fetch("/detect", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ image: uploadData.file_path }),
//         });

//         let detectData = await detectResponse.json();
//         if (detectData.error) {
//             alert(detectData.error);
//             return;
//         }

//         document.getElementById("agedImage").src = detectData.aged_image;

//         // Face recognition
//         let recognizeResponse = await fetch("/recognize", {
//             method: "POST",
//             body: formData,
//         });

//         let recognizeData = await recognizeResponse.json();
//         document.getElementById("recognitionResult").innerText = recognizeData.message;

//     } catch (error) {
//         console.error("Error:", error);
//         alert("Something went wrong!");
//     }
// }


function uploadImage() {
    let input = document.getElementById("imageInput");
    if (input.files.length === 0) {
        alert("Please select an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", input.files[0]);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Image Uploaded!") {
            document.getElementById("uploadStatus").innerText = "Image uploaded successfully!";
        } else {
            document.getElementById("uploadStatus").innerText = "Upload failed!";
        }
    })
    .catch(error => console.error("Error:", error));
}

function detectAndSaveFace() {
    fetch("/detect", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("detectStatus").innerText = data.message;
    })
    .catch(error => console.error("Error:", error));
}

function startRecognition() {
    fetch("/recognize", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("recognitionResult").innerText = data.message;
    })
    .catch(error => console.error("Error:", error));
}

console.log("script.js loaded successfully!");
