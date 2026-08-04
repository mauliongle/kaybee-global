/* ==========================================================================
   KayBee Global 3D Interactive WebGL Globe (Three.js Engine)
   ========================================================================== */

let scene, camera, renderer, globeGroup, routeArcs = [], controls;
let targetRotationX = 0, targetRotationY = 0;

// Coordinates for India export hub (Mumbai / Pune)
const INDIA_HUB = { lat: 18.9690, lon: 72.8210, name: "KayBee Global Hub (Pune / JNPT Port)" };

const EXPORT_DESTINATIONS = [
    { code: 'DXB', name: 'Jebel Ali / Dubai', lat: 25.2048, lon: 55.2708, transit: '4-6 Days', rate: '$1,200 / 20ft Reefer' },
    { code: 'RTM', name: 'Rotterdam / Hamburg', lat: 51.9244, lon: 4.4777, transit: '18-22 Days', rate: '$2,800 / 40ft Reefer' },
    { code: 'NYC', name: 'New York / Los Angeles', lat: 40.7128, lon: -74.0060, transit: '25-30 Days', rate: '$4,200 / 40ft Reefer' },
    { code: 'SIN', name: 'Singapore / Port Klang', lat: 1.3521, lon: 103.8198, transit: '7-10 Days', rate: '$1,100 / 20ft Reefer' },
    { code: 'MBA', name: 'Mombasa / Durban', lat: -4.0435, lon: 39.6682, transit: '12-15 Days', rate: '$2,100 / 20ft Reefer' },
    { code: 'SYD', name: 'Sydney / Melbourne', lat: -33.8688, lon: 151.2093, transit: '16-20 Days', rate: '$2,400 / 40ft Reefer' }
];

function init3DGlobe() {
    const container = document.getElementById('globe-canvas-container');
    if (!container) return;

    const width = container.clientWidth;
    const height = container.clientHeight;

    // 1. Scene Setup
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.0015);

    // 2. Camera Setup
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 0, 260);

    // 3. Renderer Setup
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 4. Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xB8860B, 1.2);
    dirLight1.position.set(150, 100, 150);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x6B46C1, 0.8);
    dirLight2.position.set(-150, -100, -150);
    scene.add(dirLight2);

    // 4.5 Starfield Background
    const starsGeometry = new THREE.BufferGeometry();
    const starsMaterial = new THREE.PointsMaterial({
        color: 0xffffff,
        size: 0.8,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true
    });
    const starsVertices = [];
    for (let i = 0; i < 3000; i++) {
        const x = THREE.MathUtils.randFloatSpread(2000);
        const y = THREE.MathUtils.randFloatSpread(2000);
        const z = THREE.MathUtils.randFloatSpread(2000);
        // Keep stars outside the globe radius
        if (Math.abs(x) > 120 || Math.abs(y) > 120 || Math.abs(z) > 120) {
            starsVertices.push(x, y, z);
        }
    }
    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
    const starField = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(starField);

    // 5. Globe Group
    globeGroup = new THREE.Group();
    scene.add(globeGroup);

    // Earth Sphere Geometry
    const radius = 80;
    const globeGeometry = new THREE.SphereGeometry(radius, 64, 64);

    // Realistic Earth Texture from CDN
    const textureLoader = new THREE.TextureLoader();
    const texture = textureLoader.load('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg');
    const bumpMap = textureLoader.load('https://unpkg.com/three-globe/example/img/earth-topology.png');
    const specMap = textureLoader.load('https://unpkg.com/three-globe/example/img/earth-water.png');
    
    const globeMaterial = new THREE.MeshPhongMaterial({
        map: texture,
        bumpMap: bumpMap,
        bumpScale: 1.2,
        specularMap: specMap,
        specular: new THREE.Color('grey'),
        shininess: 35
    });

    const earthMesh = new THREE.Mesh(globeGeometry, globeMaterial);
    globeGroup.add(earthMesh);

    // Outer Glowing Atmosphere Ring (Realistic Blue)
    const atmosphereGeom = new THREE.SphereGeometry(radius + 3, 64, 64);
    const atmosphereMat = new THREE.MeshBasicMaterial({
        color: 0x3399FF,
        transparent: true,
        opacity: 0.15,
        side: THREE.BackSide
    });
    const atmosphere = new THREE.Mesh(atmosphereGeom, atmosphereMat);
    globeGroup.add(atmosphere);

    // 7. Add India Export Pin & Destination Pins + Trade Arcs
    addHubPin(radius);
    EXPORT_DESTINATIONS.forEach(dest => {
        addDestinationPin(dest, radius);
        createTradeArc(INDIA_HUB, dest, radius);
    });

    // 8. Orbit Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.6;
    controls.zoomSpeed = 0.8;
    controls.minDistance = 140;
    controls.maxDistance = 380;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.8;

    // 9. Animation Loop
    function animate() {
        requestAnimationFrame(animate);
        controls.update();

        // Smoothly rotate globe towards target if autoRotate is off
        if (!controls.autoRotate) {
            globeGroup.rotation.y += (targetRotationY - globeGroup.rotation.y) * 0.05;
            globeGroup.rotation.x += (targetRotationX - globeGroup.rotation.x) * 0.05;
        }

        // Animate glowing light particles along trade arcs
        routeArcs.forEach(arc => {
            if (arc.pulseMesh) {
                arc.progress = (arc.progress + 0.008) % 1;
                const point = arc.curve.getPoint(arc.progress);
                arc.pulseMesh.position.copy(point);
            }
        });

        renderer.render(scene, camera);
    }
    animate();

    // Resize Handler
    window.addEventListener('resize', () => {
        if (!container) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    });
}

// Convert Lat/Lon to 3D Sphere Coordinates
function latLonToVector3(lat, lon, radius) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const z = radius * Math.sin(phi) * Math.sin(theta);
    const y = radius * Math.cos(phi);
    return new THREE.Vector3(x, y, z);
}

// Draw Canvas Texture for Earth Continents
function createEarthCanvas() {
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');

    // Light Gray/Blue Gradient Ocean
    const grad = ctx.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0, '#E2E8F0');
    grad.addColorStop(1, '#CBD5E0');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1024, 512);

    // Stylized Glowing Continents grid lines
    ctx.strokeStyle = 'rgba(184, 134, 11, 0.4)';
    ctx.lineWidth = 1;

    for (let i = 0; i < 1024; i += 32) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, 512);
        ctx.stroke();
    }
    for (let j = 0; j < 512; j += 32) {
        ctx.beginPath();
        ctx.moveTo(0, j);
        ctx.lineTo(1024, j);
        ctx.stroke();
    }

    // Highlighting major trade nodes
    ctx.fillStyle = '#B8860B';
    ctx.font = '24px Outfit';
    ctx.fillText('KAYBEE GLOBAL TRADE NETWORK', 320, 60);

    return canvas;
}

function addHubPin(radius) {
    const pos = latLonToVector3(INDIA_HUB.lat, INDIA_HUB.lon, radius);
    const pinGeom = new THREE.SphereGeometry(2.5, 16, 16);
    const pinMat = new THREE.MeshBasicMaterial({ color: 0xFFD700 });
    const pinMesh = new THREE.Mesh(pinGeom, pinMat);
    pinMesh.position.copy(pos);
    globeGroup.add(pinMesh);

    // Glowing Pulse Ring around India Hub
    const ringGeom = new THREE.RingGeometry(3, 5, 32);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xFFD700, side: THREE.DoubleSide, transparent: true, opacity: 0.8 });
    const ringMesh = new THREE.Mesh(ringGeom, ringMat);
    ringMesh.position.copy(pos);
    ringMesh.lookAt(new THREE.Vector3(0,0,0));
    globeGroup.add(ringMesh);
}

function addDestinationPin(dest, radius) {
    const pos = latLonToVector3(dest.lat, dest.lon, radius);
    const pinGeom = new THREE.SphereGeometry(1.8, 16, 16);
    const pinMat = new THREE.MeshBasicMaterial({ color: 0x48BB78 });
    const pinMesh = new THREE.Mesh(pinGeom, pinMat);
    pinMesh.position.copy(pos);
    globeGroup.add(pinMesh);
}

// Create Curved 3D Shipping Trade Arc between India & Port
function createTradeArc(source, dest, radius) {
    const start = latLonToVector3(source.lat, source.lon, radius);
    const end = latLonToVector3(dest.lat, dest.lon, radius);

    // Midpoint elevated away from sphere center
    const mid = start.clone().add(end).multiplyScalar(0.5);
    const distance = start.distanceTo(end);
    mid.normalize().multiplyScalar(radius + distance * 0.35);

    const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
    const points = curve.getPoints(50);
    const geometry = new THREE.BufferGeometry().setFromPoints(points);

    const material = new THREE.LineBasicMaterial({
        color: 0xB8860B,
        transparent: true,
        opacity: 0.6
    });

    const arcLine = new THREE.Line(geometry, material);
    globeGroup.add(arcLine);

    // Animated Light Pulse
    const pulseGeom = new THREE.SphereGeometry(1.4, 8, 8);
    const pulseMat = new THREE.MeshBasicMaterial({ color: 0xFFD700 });
    const pulseMesh = new THREE.Mesh(pulseGeom, pulseMat);
    globeGroup.add(pulseMesh);

    routeArcs.push({ curve, pulseMesh, progress: Math.random() });
}

function focusDestination(destCode) {
    const dest = EXPORT_DESTINATIONS.find(d => d.code === destCode);
    if (!dest) return;

    document.querySelectorAll('.dest-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    document.getElementById('dest-name').innerText = dest.name;
    document.getElementById('dest-transit').innerText = dest.transit;
    document.getElementById('dest-rate').innerText = dest.rate;
    
    // Stop auto-rotation when user clicks a destination
    if (controls) controls.autoRotate = false;
    
    // Update destination image with pop animation
    const imgEl = document.getElementById('dest-image');
    if (imgEl) {
        imgEl.style.animation = 'none';
        imgEl.offsetHeight; // Trigger reflow to restart animation
        imgEl.src = `/static/images/dest_${destCode.toLowerCase()}.jpg`;
        imgEl.style.animation = 'modalPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards';
    }

    // Smoothly rotate globe towards target destination lat/lon
    const pos = latLonToVector3(dest.lat, dest.lon, 80);
    targetRotationY = -(dest.lon * (Math.PI / 180));
    targetRotationX = (dest.lat * (Math.PI / 180));
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    init3DGlobe();
});
