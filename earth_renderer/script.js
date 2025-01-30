// script.js
let renderer, camera, scene, sphere;
let isBound = false;
let moveX = 0, moveY = 0;
const sensitivity = 0.002;

// Performance tracking variables
let lastTime = 0;
let accumulatedTime = 0;
let frameCount = 0;

function init() {
    // Setup renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Setup camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 0.1);

    // Setup scene
    scene = new THREE.Scene();

    // Create performance display
    const perfDiv = document.createElement('div');
    perfDiv.id = 'performance';
    Object.assign(perfDiv.style, {
        position: 'fixed',
        top: '10px',
        left: '10px',
        color: 'white',
        fontFamily: 'Arial',
        zIndex: '1000',
        backgroundColor: 'rgba(0,0,0,0.5)',
        padding: '5px'
    });
    document.body.appendChild(perfDiv);

    // Create skybox sphere
    const geometry = new THREE.SphereGeometry(500, 60, 60);
    const texture = new THREE.TextureLoader().load('assets/skybox.png');
    const material = new THREE.MeshBasicMaterial({
        map: texture,
        side: THREE.BackSide
    });
    sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    // Event listeners
    document.addEventListener('mousemove', onMouseMove);
    document.getElementById('bind-button').addEventListener('click', togglePointerLock);
    document.addEventListener('pointerlockchange', onPointerLockChange);
    window.addEventListener('resize', onWindowResize);
}

function togglePointerLock() {
    if (document.pointerLockElement) {
        document.exitPointerLock();
    } else {
        renderer.domElement.requestPointerLock();
    }
}

function onPointerLockChange() {
    isBound = document.pointerLockElement === renderer.domElement;
    document.getElementById('bind-button').style.display = isBound ? 'none' : 'block';
}

function onMouseMove(e) {
    if (!isBound) return;
    
    moveX += -e.movementX * sensitivity;
    moveY += e.movementY * sensitivity;
    
    moveY = Math.max(-Math.PI/2, Math.min(Math.PI/2, moveY));
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function updatePerformanceDisplay(delta, fps) {
    const perfElement = document.getElementById('performance');
    if (perfElement) {
        perfElement.textContent = `Avg Delta: ${delta.toFixed(2)}ms | FPS: ${fps.toFixed(1)}`;
    }
}

function animate(timestamp) {
    requestAnimationFrame(animate);

    if (lastTime === 0) {
        lastTime = timestamp;
        return;
    }

    const deltaTime = timestamp - lastTime;
    lastTime = timestamp;

    accumulatedTime += deltaTime;
    frameCount++;

    if (accumulatedTime >= 500) {
        const averageDelta = accumulatedTime / frameCount;
        const averageFPS = 1000 / averageDelta;
        updatePerformanceDisplay(averageDelta, averageFPS);
        accumulatedTime = 0;
        frameCount = 0;
    }

    if (isBound) {
        camera.rotation.set(-moveY, moveX, 0, 'YXZ');
    }

    renderer.render(scene, camera);
}

init();
animate();