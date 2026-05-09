# React Three Fiber + Drei (3D)

Requires React 19. For React 18, pin to `@react-three/fiber@8.x` and `@react-three/drei@9.x`.

```tsx
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Environment, useGLTF, Stage } from '@react-three/drei'
import { useRef, Suspense } from 'react'

function RotatingBox() {
  const ref = useRef<THREE.Mesh>(null!)
  useFrame((_, delta) => { ref.current.rotation.x += delta })
  return (
    <mesh ref={ref}>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="royalblue" />
    </mesh>
  )
}

function Scene() {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <RotatingBox />
      <OrbitControls />
    </Canvas>
  )
}

// Model loading
useGLTF.preload('/model.glb') // module scope
function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

// Product viewer shortcut
<Canvas shadows>
  <Suspense fallback={null}>
    <Stage environment="city" shadows="contact">
      <Model url="/product.glb" />
    </Stage>
  </Suspense>
  <OrbitControls makeDefault />
</Canvas>
```

## Key Rules

- `useFrame` runs every frame (~60fps). Always mutate via refs, never via setState
- Never allocate objects (`new THREE.Vector3()`) inside `useFrame` — preallocate with `useMemo`
- Use `e.stopPropagation()` on click/pointer events (raycasting pierces through objects)
- `frameloop="demand"` stops continuous rendering for static scenes
- Next.js: Use `next/dynamic` with `{ ssr: false }` — Three.js requires browser APIs
- Always wrap model components in `<Suspense fallback={...}>`
- `useGLTF.preload()` at module scope for early loading
- Environment presets: `"apartment"`, `"city"`, `"dawn"`, `"forest"`, `"lobby"`, `"night"`, `"park"`, `"studio"`, `"sunset"`, `"warehouse"`
