import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

let currentModel = null

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
camera.position.z = 3

const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setSize(window.innerWidth, window.innerHeight)
document.body.appendChild(renderer.domElement)

const ambientLight = new THREE.AmbientLight(0xffffff, 1)
scene.add(ambientLight)
const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
directionalLight.position.set(5, 5, 5)
scene.add(directionalLight)

const loader = new GLTFLoader()
const orbitControls = new OrbitControls(camera, renderer.domElement)

function animate() {
    requestAnimationFrame(animate)
    orbitControls.update()
    renderer.render(scene, camera)
}
animate()

// Test load (remove when API is working)
//loader.load("http://127.0.0.1:5000/test-model", function(gltf) {
//    scene.add(gltf.scene)
//    currentModel = gltf.scene
//    fitCamera(gltf.scene)
//})

function fitCamera(model) {
    const box = new THREE.Box3().setFromObject(model)
    const centre = box.getCenter(new THREE.Vector3())
    const size = box.getSize(new THREE.Vector3())
    const maxDim = Math.max(size.x, size.y, size.z)
    camera.position.set(centre.x, centre.y, centre.z + maxDim * 2)
    orbitControls.target.set(centre.x, centre.y, centre.z)
    orbitControls.update()
}

const statusEl = document.getElementById("status")
const button = document.getElementById("prompt_button")

button.addEventListener("click", async () => {
    const prompt = document.getElementById("prompt").value
    if (!prompt) return

    button.textContent = "Generating..."
    button.disabled = true
    statusEl.textContent = "Generating your 3D model... this may take a minute"
    statusEl.className = ""

    const response = await fetch("http://127.0.0.1:5000/models", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
    })

    if (!response.ok) {
        statusEl.textContent = "Generation failed. Please try again."
        statusEl.className = "error"
        button.textContent = "Generate"
        button.disabled = false
        return
    }
    const data = await response.json()
    pollStatus(data.task_id)
})

async function pollStatus(task_id) {
    while (true) {
        const response = await fetch(`http://127.0.0.1:5000/models/${task_id}`)
        const data = await response.json()
        const status = data.status

        if (status === "PENDING" || status === "IN_PROGRESS") {
            await new Promise(r => setTimeout(r, 5000))
        } else if (status === "FINISHED") {
            statusEl.textContent = ""
            button.textContent = "Generate"
            button.disabled = false
            loader.load(data.file_url, function(gltf) {
                console.log("Model loaded", gltf)
                if (currentModel) scene.remove(currentModel)
                scene.add(gltf.scene)
                currentModel = gltf.scene
                fitCamera(gltf.scene)
            })
            break
        } else if (status === "FAILED") {
            statusEl.textContent = "Generation failed. Please try again."
            statusEl.className = "error"
            button.textContent = "Generate"
            button.disabled = false
            break
        }
    }
}