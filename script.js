const uploadVideo = async () => {
    const file = document.getElementById('fileInput').files[0];
    if (!file) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    alert(result.message);
};

const streamVideo = async () => {
    const filename = document.getElementById('filenameInput').value;

    const response = await fetch(`/stream/${filename}`);
    const result = await response.json();

    if (result.url) {
        const videoPlayer = document.getElementById('videoPlayer');
        videoPlayer.src = result.url;
        videoPlayer.play();
    } else {
        alert(result.error);
    }
};