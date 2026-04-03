document.addEventListener("DOMContentLoaded", () => {
    const card = document.getElementById('tilt-card');
    const container = document.querySelector('.container');
    const imageInput = document.getElementById('imageInput');
    const fileNameDisplay = document.getElementById('file-name');
    const uploadForm = document.getElementById('uploadForm');
    const loader = document.getElementById('loader');
    const modeSelect = document.getElementById('modeSelect');

    // ===============================
    // 1. Algorithm Briefing Data
    // ===============================
    const algoData = {
        "auto": {
            name: "AI Auto Mode",
            desc: "Neural decision engine. Automatically selects the optimal restoration pipeline based on detected turbidity.",
            latency: "MODERATE",
            type: "ADAPTIVE"
        },
        "quantum_enhance": {
            name: "Quantum Enhancement",
            desc: "Aggressive mathematical transformation. Best for very dull, low-contrast images requiring maximum detail retrieval.",
            latency: "HIGH",
            type: "PROBABILISTIC"
        },
        "wcid": {
            name: "WCID Algorithm",
            desc: "Underwater-specific dehazing. Effective for correcting heavy blue/green color casts and restoring natural clarity.",
            latency: "MODERATE",
            type: "COLOR-FIX"
        },
        "dcp": {
            name: "Dark Channel Prior",
            desc: "Specialized haze removal. Most effective for 'foggy' scenes with low visibility, though it may shift vibrant colors.",
            latency: "LOW",
            type: "DEHAZING"
        },
        "dct": {
            name: "DCT Restoration",
            desc: "Frequency-domain analysis. Ideal for removing digital compression noise and restoring lost textures/patterns.",
            latency: "LOW",
            type: "FREQUENCY"
        },
        "contrast": {
            name: "Contrast Maximization",
            desc: "Dynamic range expansion. Use for flat or faded footage where objects are difficult to distinguish from the background.",
            latency: "MINIMAL",
            type: "CONTRAST"
        },
        "homomorphic": {
            name: "Homomorphic Filtering",
            desc: "Illumination correction. Best for images with uneven lighting or heavy shadows caused by ROV spotlights.",
            latency: "MODERATE",
            type: "LIGHTING"
        },
        "guided": {
            name: "Guided Filter",
            desc: "Edge-preserving smoothing. Removes sensor noise while keeping the sharp outlines of coral and wreckage.",
            latency: "LOW",
            type: "DENOISING"
        },
        "histogram": {
            name: "Histogram Equalization",
            desc: "Global brightness balancing. Effective for images that are consistently too dark or too bright across the entire frame.",
            latency: "MINIMAL",
            type: "STATISTICAL"
        },
        "seathru": {
            name: "Simple SeaThru",
            desc: "Physics-based water correction. Improves depth visibility and counteracts light absorption in deep-sea environments.",
            latency: "HIGH",
            type: "PHYSICS"
        },
        "standard": {
            name: "Standard Enhancement",
            desc: "Baseline restoration protocol. A balanced approach for shallow-water imagery with minor color loss.",
            latency: "LOW",
            type: "LINEAR"
        }
    };

    // Update Briefing Card on Selection
    modeSelect.addEventListener('change', function() {
        const info = algoData[this.value];
        if (info) {
            document.getElementById('algo-name').innerText = info.name;
            document.getElementById('algo-description').innerText = info.desc;
            document.getElementById('algo-complexity').innerText = `LATENCY: ${info.latency}`;
            document.getElementById('algo-tag').innerText = `TYPE: ${info.type}`;
            
            // Visual pulse trigger for the card
            const infoCard = document.getElementById('infoCard');
            infoCard.style.animation = 'none';
            void infoCard.offsetWidth; // Trigger reflow
            infoCard.style.animation = 'slideIn 0.4s ease-out';
        }
    });

    // ===============================
    // 2. 3D Dynamic Tilt
    // ===============================
    container.addEventListener('mousemove', (e) => {
        let xAxis = (window.innerWidth / 2 - e.pageX) / 35;
        let yAxis = (window.innerHeight / 2 - e.pageY) / 35;
        card.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
    });

    container.addEventListener('mouseleave', () => {
        card.style.transition = "all 0.5s ease";
        card.style.transform = `rotateY(0deg) rotateX(0deg)`;
    });

    container.addEventListener('mouseenter', () => {
        card.style.transition = "none";
    });

    // ===============================
    // 3. Update File Name
    // ===============================
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        const name = file ? file.name : "LOAD SUBMERGED DATA";
        fileNameDisplay.textContent = name.toUpperCase();
        fileNameDisplay.style.color = "#00f2ff";
    });

    // ===============================
    // 4. Process Submission
    // ===============================
    uploadForm.addEventListener("submit", async function(e) {
        e.preventDefault();

        loader.style.display = "block";
        // Loader text with themed styling
        loader.querySelector('.loader-text').innerText = "SCANNING TURBIDITY...";

        document.getElementById("resultsSection").style.display = "none";
        document.getElementById("metricsSection").style.display = "none";

        const file = imageInput.files[0];

        if (!file) {
            alert("Please select an image first.");
            loader.style.display = "none";
            return;
        }

        const formData = new FormData();
        formData.append("image", file);
        formData.append("mode", modeSelect.value);

        try {
            const response = await fetch("/enhance", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Server error");
            }

            loader.style.display = "none";

            // Show Results
            document.getElementById("resultsSection").style.display = "flex";
            document.getElementById("metricsSection").style.display = "block";

            document.getElementById("originalImage").src =
                data.original_image_url + "?t=" + new Date().getTime();

            document.getElementById("enhancedImage").src =
                data.enhanced_image_url + "?t=" + new Date().getTime();

            document.getElementById("metricsData").innerHTML =
                `<strong>PSNR:</strong> ${data.psnr} dB<br>
                 <strong>ENTROPY:</strong> ${data.entropy}`;

            document.getElementById("downloadBtn").href = data.download_url;

            // Scroll to view results
            window.scrollTo({
                top: document.getElementById("resultsSection").offsetTop,
                behavior: 'smooth'
            });

        } catch (error) {
            console.error("Enhancement failed:", error);
            loader.style.display = "block";
            loader.querySelector('.loader-text').innerHTML = 
                "<span style='color:#ff4d4d'>DATA LOSS: RECHECK UPLINK</span>";
        }
    });
});