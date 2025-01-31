let renderer, camera, scene, sphere;
const planets = {};

// Performance tracking variables
let lastTime = 0;
let accumulatedTime = 0;
let frameCount = 0;

// Planet configurations
const planetsConfig = [
    { texture: 'assets/sun/sun.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 0, speed: 2293200 },
    { texture: 'assets/mercury/mercury.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 0.1, speed: 5068800 },
    { texture: 'assets/venus/surface.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 177, speed: 21088800 },
    { texture: 'assets/earth/earth.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 23, speed: 86160 },
    { texture: 'assets/mars/mars.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 25, speed: 88560 },
    { texture: 'assets/jupiter/jupiter.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 3, speed: 35700 },
    { texture: 'assets/saturn/saturn.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 27, speed: 37980 },
    { texture: 'assets/uranus/uranus.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 98, speed: 62040 },
    { texture: 'assets/neptune/neptune.png', size: 2, position: { x: 0, y: 0, z: 0 }, initial_axis: 30, speed: 57600 }
];

function init() {
    // Setup renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Setup camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 5);

    // Setup scene
    scene = new THREE.Scene();

    // Add Directional Light (simulating the sun)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 0, 5); // Position it as needed
    scene.add(directionalLight);

    // Create performance display
    const perfDiv = document.createElement('div');
    perfDiv.id = 'performance';
    Object.assign(perfDiv.style, {
        position: 'fixed',
        top: '10px',
        left: '10px',
        color: 'white',
        fontFamily: 'Arial',
        fontSize: '16px',
        zIndex: '1000',
        backgroundColor: 'rgba(1,0,0,1)',
        padding: '5px'
    });
    document.body.appendChild(perfDiv);

    // Create skybox sphere
    const geometry = new THREE.SphereGeometry(500, 60, 60);
    const texture = new THREE.TextureLoader().load('assets/skybox.png');
    const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.BackSide });
    sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    // Create planets
    planetsConfig.forEach((config) => {
        const texture = new THREE.TextureLoader().load(config.texture);
        const planetMaterial = new THREE.MeshStandardMaterial({ map: texture });
        const planetGeometry = new THREE.SphereGeometry(config.size, 32, 32);
        const planet = new THREE.Mesh(planetGeometry, planetMaterial);
        planet.position.set(config.position.x, config.position.y, config.position.z);
        planet.visible = false;

        // Apply axial tilt (initial_axis) by rotating around the x-axis
        planet.rotation.x = THREE.MathUtils.degToRad(config.initial_axis);

        // Convert speed from degrees per second to radians per millisecond
        planet.rotationSpeed = THREE.MathUtils.degToRad(config.speed) / 1000;

        scene.add(planet);
        
        const name = config.texture.split('/')[1];
        planets[name] = planet;
    });

    const guiContainer = document.getElementById('gui-container');

    planetsConfig.forEach((config) => {
        const name = config.texture.split('/')[1];
        const button = document.createElement('button');
        button.className = 'gui-button';
        button.textContent = name.charAt(0).toUpperCase() + name.slice(1);
        button.addEventListener('click', () => showPlanet(name));
        guiContainer.appendChild(button);
    });

    window.addEventListener('resize', onWindowResize);
}

function showPlanet(name) {
    Object.values(planets).forEach(planet => planet.visible = false);
    if (planets[name]) {
        planets[name].visible = true;
        console.log(`${name} is now visible`);
    } else {
        console.error(`Planet ${name} not found!`);
    }
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

    let deltaTime = timestamp - lastTime;
    lastTime = timestamp;

    // Ensure accumulatedTime is always a valid number
    if (isNaN(accumulatedTime) || accumulatedTime === undefined) {
        console.error("accumulatedTime was NaN or undefined! Resetting.");
        accumulatedTime = 0;
    }

    accumulatedTime += deltaTime; // Safe update

    frameCount++;

    if (accumulatedTime >= 500) {
        const averageDelta = accumulatedTime / frameCount;
        const averageFPS = 1000 / averageDelta;
        updatePerformanceDisplay(averageDelta, averageFPS);
        accumulatedTime = 0;
        frameCount = 0;
    }

    // Rotate visible planets based on their rotationSpeed
    Object.values(planets).forEach(planet => {
        if (planet.visible) {
            planet.rotation.y += planet.rotationSpeed * deltaTime;
        }
    });

    renderer.render(scene, camera);
}

init();
animate();