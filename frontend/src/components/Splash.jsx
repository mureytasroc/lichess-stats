import React, { Suspense, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";

import {
  useGLTF,
  OrbitControls,
  PresentationControls,
} from "@react-three/drei";
import * as THREE from "three";

const GLTF_FILE = "/Chess_Board_v2 (1).gltf";
const ROTATE_SPEED = Math.PI / 50;
const LEFT_MAX_ROTATE = -Math.PI + 0.25;
const RIGHT_MAX_ROTATE = 0.5;
// function Model() {
//   const { scene, animations, nodes, materials } = useGLTF(GLTF_FILE);
//   console.log(scene, animations, nodes, materials);
//   scene.position.y = 2;
//   let flip = false;
//   useFrame(() => {
//     if (scene.rotation.y < LEFT_MAX_ROTATE) {
//       flip = true;
//     }
//     if (scene.rotation.y > RIGHT_MAX_ROTATE) {
//       flip = false;
//     }
//     let modifier =
//       (Math.min(
//         Math.abs(scene.rotation.y - LEFT_MAX_ROTATE),
//         Math.abs(scene.rotation.y - RIGHT_MAX_ROTATE)
//       ) +
//         0.2) /
//       (RIGHT_MAX_ROTATE - LEFT_MAX_ROTATE);

//     scene.rotation.y += (flip ? 1 : -1) * ROTATE_SPEED * modifier * modifier;
//   });
//   return (
//     <Suspense fallback={null}>
//       <primitive object={scene} scale={1} />
//     </Suspense>
//   );
// }

function Model(props) {
  const group = useRef();
  const { scene, nodes, materials } = useGLTF(GLTF_FILE);

  return (
    <group ref={group} {...props} dispose={null}>
      <group position={[0, 1, 0]} scale={[4, 0.5, 4]}>
        <mesh
          castShadow
          receiveShadow
          geometry={nodes.Cube.geometry}
          material={materials.Wood}
        />
        <mesh
          castShadow
          receiveShadow
          geometry={nodes.Cube_1.geometry}
          material={materials.Black_Squares}
        />
      </group>
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn005.geometry}
        material={nodes.Pawn005.material}
        position={[3.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Rook.geometry}
        material={nodes.Rook.material}
        position={[3.5, 1.78, -3.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Rook001.geometry}
        material={nodes.Rook001.material}
        position={[-3.5, 1.78, -3.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Bishop.geometry}
        material={nodes.Bishop.material}
        position={[1.5, 1.78, -3.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Queen.geometry}
        material={nodes.Queen.material}
        position={[0.5, 1.77, -3.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Queen001.geometry}
        material={nodes.Queen001.material}
        position={[-0.5, 1.77, -3.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Bishop001.geometry}
        material={nodes.Bishop001.material}
        position={[-1.5, 1.78, -3.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Knight001.geometry}
        material={nodes.Knight001.material}
        position={[-2.5, 1.78, -3.5]}
        rotation={[0, Math.PI / 2, 0]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Knight002.geometry}
        material={nodes.Knight002.material}
        position={[2.5, 1.78, -3.5]}
        rotation={[0, Math.PI / 2, 0]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn001.geometry}
        material={nodes.Pawn001.material}
        position={[2.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn002.geometry}
        material={nodes.Pawn002.material}
        position={[1.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn004.geometry}
        material={nodes.Pawn004.material}
        position={[-0.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn006.geometry}
        material={nodes.Pawn006.material}
        position={[-1.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn007.geometry}
        material={nodes.Pawn007.material}
        position={[-2.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn008.geometry}
        material={nodes.Pawn008.material}
        position={[-3.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn003.geometry}
        material={nodes.Pawn003.material}
        position={[0.5, 1.78, -2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn009.geometry}
        material={nodes.Pawn009.material}
        position={[3.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn010.geometry}
        material={nodes.Pawn010.material}
        position={[2.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn011.geometry}
        material={nodes.Pawn011.material}
        position={[1.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn012.geometry}
        material={nodes.Pawn012.material}
        position={[-0.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn013.geometry}
        material={nodes.Pawn013.material}
        position={[-1.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn014.geometry}
        material={nodes.Pawn014.material}
        position={[-2.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn015.geometry}
        material={nodes.Pawn015.material}
        position={[-3.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Pawn016.geometry}
        material={nodes.Pawn016.material}
        position={[0.5, 1.78, 2.5]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Rook002.geometry}
        material={nodes.Rook002.material}
        position={[-3.5, 1.78, 3.39]}
        rotation={[-Math.PI, 0.03, -Math.PI]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Rook003.geometry}
        material={nodes.Rook003.material}
        position={[3.5, 1.78, 3.61]}
        rotation={[-Math.PI, 0.03, -Math.PI]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Bishop002.geometry}
        material={nodes.Bishop002.material}
        position={[-1.5, 1.78, 3.45]}
        rotation={[-Math.PI, 0.03, -Math.PI]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Queen002.geometry}
        material={nodes.Queen002.material}
        position={[0.5, 1.77, 3.48]}
        rotation={[-Math.PI, 0.03, -Math.PI]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Queen003.geometry}
        material={nodes.Queen003.material}
        position={[-0.5, 1.77, 3.52]}
        rotation={[-Math.PI, 0.03, -Math.PI]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Bishop003.geometry}
        material={nodes.Bishop003.material}
        position={[1.5, 1.78, 3.55]}
        rotation={[-Math.PI, 0.03, -Math.PI]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Knight003.geometry}
        material={nodes.Knight003.material}
        position={[2.5, 1.78, 3.58]}
        rotation={[-Math.PI, -1.54, -Math.PI]}
        scale={0.32}
      />
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Knight004.geometry}
        material={nodes.Knight004.material}
        position={[-2.5, 1.78, 3.42]}
        rotation={[-Math.PI, -1.54, -Math.PI]}
        scale={0.32}
      />
    </group>
  );
}

useGLTF.preload(GLTF_FILE);

function Splash() {
  return (
    <Canvas
      style={{
        height: 600,
        width: 800,
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
      }}
      camera={{ fov: 80, near: 1, far: 60, position: [0, 5, 10] }}
    >
      <OrbitControls
        autoRotate
        enableZoom={false}
        enablePan={false}
        enableRotate={false}
      />

      <ambientLight intensity={0.25} />
      <pointLight />

      <spotLight
        castShadow
        color="white"
        intensity={1}
        position={[-50, 50, 40]}
        angle={0.25}
        penumbra={1}
        shadow-mapSize={[128, 128]}
        shadow-bias={0.00005}
      />
      <spotLight
        castShadow
        color="#964B00"
        intensity={5}
        position={[-50, 50, 40]}
        angle={0.25}
        penumbra={1}
        shadow-mapSize={[128, 128]}
        shadow-bias={0.00005}
      />

      <Model />
    </Canvas>
  );
}

export default Splash;
