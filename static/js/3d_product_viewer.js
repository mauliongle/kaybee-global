/* ==========================================================================
   KayBee Global 3D Interactive Product Inspector Modal (Three.js Engine)
   ========================================================================== */

let productScene, productCamera, productRenderer, currentProductMesh;

function initProduct3DViewer(productData) {
    const container = document.getElementById('product-canvas-container');
    if (!container) return;

    // Clear previous canvas
    container.innerHTML = '';

    const width = container.clientWidth;
    const height = container.clientHeight;

    // 1. Scene
    productScene = new THREE.Scene();

    // 2. Camera
    productCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    productCamera.position.set(0, 30, 80);

    // 3. Renderer
    productRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    productRenderer.setSize(width, height);
    productRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(productRenderer.domElement);

    // 4. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    productScene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xFFD700, 1.5, 100);
    pointLight.position.set(20, 40, 30);
    productScene.add(pointLight);

    // 5. Construct 3D Export Container / Crate Geometry based on Category
    const group = new THREE.Group();

    // Load Product Image Texture
    const textureLoader = new THREE.TextureLoader();
    textureLoader.load(productData.image, (texture) => {
        let geom, mat;

        if (productData.category === 'onions' || productData.category === 'vegetables') {
            // 3D Wooden Export Produce Crate
            geom = new THREE.BoxGeometry(32, 22, 22);
            mat = [
                new THREE.MeshStandardMaterial({ map: texture, roughness: 0.5 }),
                new THREE.MeshStandardMaterial({ map: texture, roughness: 0.5 }),
                new THREE.MeshStandardMaterial({ color: 0x8B5A2B, roughness: 0.8 }), // Top
                new THREE.MeshStandardMaterial({ color: 0x8B5A2B, roughness: 0.8 }), // Bottom
                new THREE.MeshStandardMaterial({ map: texture, roughness: 0.5 }),
                new THREE.MeshStandardMaterial({ map: texture, roughness: 0.5 })
            ];
        } else if (productData.category === 'rice' || productData.category === 'wheat') {
            // 3D Burlap Grain Export Sack
            geom = new THREE.CylinderGeometry(14, 16, 36, 32);
            mat = new THREE.MeshStandardMaterial({ map: texture, roughness: 0.7 });
        } else {
            // 3D Gold Embossed Export Display Box
            geom = new THREE.BoxGeometry(28, 28, 28);
            mat = new THREE.MeshStandardMaterial({ map: texture, metalness: 0.2, roughness: 0.4 });
        }

        currentProductMesh = new THREE.Mesh(geom, mat);
        group.add(currentProductMesh);

        // Add Gold Metallic Edge Borders
        const wireGeom = new THREE.EdgesGeometry(geom);
        const wireMat = new THREE.LineBasicMaterial({ color: 0xE5CB9E, linewidth: 2 });
        const wireframe = new THREE.LineSegments(wireGeom, wireMat);
        group.add(wireframe);
    });

    productScene.add(group);

    // 6. Orbit Controls
    const controls = new THREE.OrbitControls(productCamera, productRenderer.domElement);
    controls.enableDamping = true;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 2.0;

    // 7. Animation Loop
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        if (currentProductMesh) {
            currentProductMesh.rotation.y += 0.003;
        }
        productRenderer.render(productScene, productCamera);
    }
    animate();
}
