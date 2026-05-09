# XY Flow (React Flow)

`@xyflow/react` v12.x — the standard library for node-based UIs: workflow editors, diagram builders, data pipelines, mind maps, state machines. Replaces the legacy `reactflow` package.

```tsx
import { useCallback } from 'react';
import {
  ReactFlow, ReactFlowProvider, addEdge, Background, Controls, MiniMap,
  useNodesState, useEdgesState, type OnConnect, type Node, type Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes: Node[] = [
  { id: '1', type: 'input', data: { label: 'Start' }, position: { x: 250, y: 0 } },
  { id: '2', data: { label: 'Process' }, position: { x: 250, y: 150 } },
  { id: '3', type: 'output', data: { label: 'End' }, position: { x: 250, y: 300 } },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e2-3', source: '2', target: '3' },
];

function Flow() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect: OnConnect = useCallback(
    (connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges],
  );

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes} edges={edges}
        onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
        onConnect={onConnect} fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}

export default function App() {
  return (
    <ReactFlowProvider>
      <Flow />
    </ReactFlowProvider>
  );
}
```

## Key Rules

- The `<ReactFlow>` container must have explicit dimensions — it renders `width: 100%; height: 100%`. If parent has no height, nothing renders.
- **Never** define `nodeTypes` or `edgeTypes` inside a component — causes infinite re-renders. Declare outside or `useMemo`.
- Always wrap with `<ReactFlowProvider>` when using `useReactFlow()` or hooks outside the `<ReactFlow>` tree.
- Use `className="nodrag"` on interactive elements (inputs, buttons) inside custom nodes to prevent drag interference.
- Use `className="nopan"` on interactive elements inside edge labels to prevent canvas panning.
- Never use `display: none` on handles — React Flow needs dimensions. Use `visibility: hidden` or `opacity: 0`.
- Parent nodes must appear before children in the `nodes` array for sub-flows.
- Import CSS — forgetting `style.css` or `base.css` is the most common setup error.
- In v12, `node.width`/`node.height` set inline styles (fixed dimensions). Use `node.measured.width`/`node.measured.height` for measured values.
- Wrap event handlers in `useCallback` to prevent unnecessary re-renders.

## Decision Framework

| Use XY Flow when                                             | Use dnd-kit when                     |
| ------------------------------------------------------------ | ------------------------------------ |
| Node-based graph UIs (workflow editors, diagrams, pipelines) | Sortable lists, grids, Kanban boards |
| Edges/connections between elements matter                    | No connection lines needed           |
| Pan/zoom canvas with viewport                                | Fixed-position layouts               |
| Interactive graph manipulation (add/remove/connect nodes)    | Drag-to-reorder items                |

---

## Architecture

### Packages

| Package          | Role                                                                                    | State                              |
| ---------------- | --------------------------------------------------------------------------------------- | ---------------------------------- |
| `@xyflow/system` | Framework-agnostic core — interaction systems, type definitions, edge path calculations | Pure logic (no state)              |
| `@xyflow/react`  | React wrapper with Zustand store                                                        | Zustand via `createWithEqualityFn` |
| `@xyflow/svelte` | Svelte 5 wrapper                                                                        | `$state` / `$derived`              |

### Core Concepts

- **Nodes**: Elements positioned with `{ x, y }` on an infinite canvas. Each has `id`, `type`, `position`, `data`.
- **Edges**: SVG paths connecting `source` to `target`. Each has `id`, `source`, `target`, optional `type`.
- **Handles**: Connection points on nodes (small divs as ports). Type `"source"` or `"target"`, Position `Top`/`Bottom`/`Left`/`Right`.
- **Viewport**: Contains the flow with `x`, `y`, `zoom`. Use `screenToFlowPosition()` / `flowToScreenPosition()` for coordinate conversion.

### Internal Data Flow

1. User `nodes[]` are transformed into `InternalNode` objects with `measured` dimensions, `positionAbsolute`, `handleBounds`, `z-index`.
2. `ResizeObserver` tracks node dimensions; `updateNodeInternals` fires on dimension changes.
3. Internal lookups: `nodeLookup`, `edgeLookup`, `parentLookup`, `connectionLookup` (all Map-based for O(1) access).

---

## Styling

### CSS Imports

| File             | Purpose                                                     | When                                              |
| ---------------- | ----------------------------------------------------------- | ------------------------------------------------- |
| `dist/base.css`  | Structural styles — required for React Flow to function     | Always import at minimum                          |
| `dist/style.css` | `base.css` + default theme (padding, border-radius, colors) | Use for defaults; skip when building custom theme |

```tsx
// Option A: Full defaults
import '@xyflow/react/dist/style.css';

// Option B: Base only (custom theme)
import '@xyflow/react/dist/base.css';
```

### CSS Variables (Complete)

Override under `.react-flow` or `:root`:

**Nodes:**

| Variable                                   | Default (Light)                     | Default (Dark)      |
| ------------------------------------------ | ----------------------------------- | ------------------- |
| `--xy-node-color-default`                  | `inherit`                           | `#f8f8f8`           |
| `--xy-node-border-default`                 | `1px solid #1a192b`                 | `1px solid #3c3c3c` |
| `--xy-node-background-color-default`       | `#fff`                              | `#1e1e1e`           |
| `--xy-node-group-background-color-default` | `rgba(240, 240, 240, 0.25)`         | —                   |
| `--xy-node-boxshadow-hover-default`        | `0 1px 4px 1px rgba(0, 0, 0, 0.08)` | —                   |
| `--xy-node-boxshadow-selected-default`     | `0 0 0 0.5px #1a192b`               | —                   |

**Edges:**

| Variable                            | Default (Light) | Default (Dark) |
| ----------------------------------- | --------------- | -------------- |
| `--xy-edge-stroke-default`          | `#b1b1b7`       | `#3e3e3e`      |
| `--xy-edge-stroke-width-default`    | `1`             | `1`            |
| `--xy-edge-stroke-selected-default` | `#555`          | `#727272`      |

**Handles:**

| Variable                               | Default (Light) | Default (Dark) |
| -------------------------------------- | --------------- | -------------- |
| `--xy-handle-background-color-default` | `#1a192b`       | `#bebebe`      |
| `--xy-handle-border-color-default`     | `#fff`          | `#1e1e1e`      |

**Connection Line:**

| Variable                                   | Default   |
| ------------------------------------------ | --------- |
| `--xy-connectionline-stroke-default`       | `#b1b1b7` |
| `--xy-connectionline-stroke-width-default` | `1`       |

**Controls:**

| Variable                                              | Default (Light)                   |
| ----------------------------------------------------- | --------------------------------- |
| `--xy-controls-button-background-color-default`       | `#fefefe`                         |
| `--xy-controls-button-background-color-hover-default` | `#f4f4f4`                         |
| `--xy-controls-button-border-color-default`           | `#eee`                            |
| `--xy-controls-box-shadow-default`                    | `0 0 2px 1px rgba(0, 0, 0, 0.08)` |

**MiniMap:**

| Variable                                     | Default (Light)            | Default (Dark)          |
| -------------------------------------------- | -------------------------- | ----------------------- |
| `--xy-minimap-background-color-default`      | `#fff`                     | `#141414`               |
| `--xy-minimap-mask-background-color-default` | `rgba(240, 240, 240, 0.6)` | `rgba(60, 60, 60, 0.6)` |
| `--xy-minimap-node-background-color-default` | `#e2e2e2`                  | `#2b2b2b`               |

**Background:**

| Variable                                      | Default (Light) | Default (Dark) |
| --------------------------------------------- | --------------- | -------------- |
| `--xy-background-color-default`               | `transparent`   | `#141414`      |
| `--xy-background-pattern-dots-color-default`  | `#91919a`       | `#777`         |
| `--xy-background-pattern-line-color-default`  | `#eee`          | —              |
| `--xy-background-pattern-cross-color-default` | `#e2e2e2`       | —              |

**Selection:**

| Variable                                  | Default                            |
| ----------------------------------------- | ---------------------------------- |
| `--xy-selection-background-color-default` | `rgba(0, 89, 220, 0.08)`           |
| `--xy-selection-border-default`           | `1px dotted rgba(0, 89, 220, 0.8)` |

### Dark Mode

The `colorMode` prop accepts `"light"` (default), `"dark"`, or `"system"`:

```tsx
<ReactFlow colorMode="dark" nodes={nodes} edges={edges} />
```

When `"dark"`, class `"dark"` is added to `.react-flow`. When `"system"`, respects `prefers-color-scheme`.

```css
.dark .react-flow {
  --xy-node-background-color-default: #1a1a2e;
  --xy-node-border-default: 1px solid #444;
  --xy-edge-stroke-default: #555;
}
```

### Tailwind CSS Integration

Import `base.css` (not `style.css`) to avoid conflicts. Override handle styles with `!` prefix:

```tsx
import '@xyflow/react/dist/base.css';

function CustomNode({ data }) {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-stone-400">
      <div className="flex">
        <div className="rounded-full w-12 h-12 flex justify-center items-center bg-gray-100">
          {data.emoji}
        </div>
        <div className="ml-2">
          <div className="text-lg font-bold">{data.name}</div>
          <div className="text-gray-500">{data.job}</div>
        </div>
      </div>
      <Handle type="target" position={Position.Top} className="w-16 !bg-teal-500" />
      <Handle type="source" position={Position.Bottom} className="w-16 !bg-teal-500" />
    </div>
  );
}
```

### CSS Class Overrides

| Class                       | Target             |
| --------------------------- | ------------------ |
| `.react-flow`               | Container          |
| `.react-flow__node`         | All nodes          |
| `.react-flow__node-default` | Default node type  |
| `.react-flow__node-input`   | Input node type    |
| `.react-flow__node-output`  | Output node type   |
| `.react-flow__edge`         | All edges          |
| `.react-flow__edge-path`    | Edge SVG path      |
| `.react-flow__handle`       | All handles        |
| `.react-flow__controls`     | Controls panel     |
| `.react-flow__minimap`      | MiniMap            |
| `.react-flow__background`   | Background pattern |

---

## Node Types and Custom Nodes

### Built-in Types

| Type        | Description                  | Handles                           |
| ----------- | ---------------------------- | --------------------------------- |
| `"default"` | Standard node with label     | 1 source (bottom), 1 target (top) |
| `"input"`   | Source-only node             | 1 source (bottom)                 |
| `"output"`  | Sink-only node               | 1 target (top)                    |
| `"group"`   | Container for sub-flow nodes | No handles                        |

### Custom Node

```tsx
import { Handle, Position, type NodeProps, type Node } from '@xyflow/react';

type TextUpdaterData = { label: string; value: number };
type TextUpdaterNode = Node<TextUpdaterData, 'textUpdater'>;

function TextUpdaterNode({ data, id }: NodeProps<TextUpdaterNode>) {
  const onChange = useCallback((evt: React.ChangeEvent<HTMLInputElement>) => {
    console.log(evt.target.value);
  }, []);

  return (
    <div className="text-updater-node">
      <Handle type="target" position={Position.Top} />
      <div>
        <label htmlFor="text">Text:</label>
        <input id="text" name="text" onChange={onChange} className="nodrag" />
      </div>
      <Handle type="source" position={Position.Bottom} id="output-a" />
      <Handle type="source" position={Position.Bottom} id="output-b" style={{ left: '75%' }} />
    </div>
  );
}

// MUST be defined outside the component
const nodeTypes = { textUpdater: TextUpdaterNode };

function Flow() {
  return <ReactFlow nodeTypes={nodeTypes} nodes={nodes} edges={edges} />;
}
```

### Multiple Handles

```tsx
<Handle type="target" position={Position.Top} />
<Handle type="source" position={Position.Right} id="a" />
<Handle type="source" position={Position.Bottom} id="b" />
```

Reference specific handles in edges:

```tsx
const edges = [
  { id: 'e1-2', source: 'node-1', sourceHandle: 'a', target: 'node-2' },
  { id: 'e1-3', source: 'node-1', sourceHandle: 'b', target: 'node-3' },
];
```

### Dynamic Handles

When adding/removing handles programmatically, call `useUpdateNodeInternals`:

```tsx
const updateNodeInternals = useUpdateNodeInternals();
updateNodeInternals('node-id');
```

Handle validation classes: `connecting` (connection line nearby), `valid` (connection is valid). For typeless handles, set `connectionMode={ConnectionMode.Loose}`.

### Node Resizing

```tsx
import { NodeResizer } from '@xyflow/react';

function ResizableNode({ data, selected }) {
  return (
    <>
      <NodeResizer minWidth={100} minHeight={30} isVisible={selected} />
      <Handle type="target" position={Position.Top} />
      <div>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </>
  );
}
```

### Sub-Flows / Nested Nodes

```tsx
const nodes = [
  // Parent MUST come before children in the array
  { id: 'group-1', type: 'group', position: { x: 0, y: 0 }, style: { width: 300, height: 200 } },
  { id: 'child-1', data: { label: 'Child' }, position: { x: 10, y: 10 }, parentId: 'group-1', extent: 'parent' },
  { id: 'child-2', data: { label: 'Child 2' }, position: { x: 10, y: 80 }, parentId: 'group-1', extent: 'parent' },
];
```

- `extent: 'parent'` constrains children to parent bounds.
- Without `extent`, children move with parent but can be dragged outside.
- Any node type can be a parent (not just `group`).

### NodeToolbar

```tsx
import { NodeToolbar, Position } from '@xyflow/react';

function ToolbarNode({ data, id }) {
  return (
    <>
      <NodeToolbar position={Position.Top} isVisible={undefined}>
        <button onClick={() => console.log('delete', id)}>Delete</button>
        <button onClick={() => console.log('copy', id)}>Copy</button>
      </NodeToolbar>
      <div>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </>
  );
}
```

`isVisible`: `true` (always), `false` (hidden), `undefined` (visible when selected).

---

## Edge Types and Custom Edges

### Built-in Types

| Type                     | Path Style                     |
| ------------------------ | ------------------------------ |
| `"default"` / `"bezier"` | Cubic bezier curve             |
| `"straight"`             | Direct line                    |
| `"step"`                 | Right-angle steps              |
| `"smoothstep"`           | Rounded right-angle steps      |
| `"simplebezier"`         | Simple bezier (less curvature) |

### Custom Edge

```tsx
import { BaseEdge, getStraightPath, EdgeLabelRenderer, useReactFlow, type EdgeProps } from '@xyflow/react';

function ButtonEdge({ id, sourceX, sourceY, targetX, targetY, style, markerEnd }: EdgeProps) {
  const { deleteElements } = useReactFlow();
  const [edgePath, labelX, labelY] = getStraightPath({ sourceX, sourceY, targetX, targetY });

  return (
    <>
      <BaseEdge id={id} path={edgePath} style={style} markerEnd={markerEnd} />
      <EdgeLabelRenderer>
        <button
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
            pointerEvents: 'all',
          }}
          className="nodrag nopan"
          onClick={() => deleteElements({ edges: [{ id }] })}
        >
          Delete
        </button>
      </EdgeLabelRenderer>
    </>
  );
}

const edgeTypes = { buttonedge: ButtonEdge };
```

### Path Utilities

| Function                     | Returns                                    |
| ---------------------------- | ------------------------------------------ |
| `getBezierPath({...})`       | `[path, labelX, labelY, offsetX, offsetY]` |
| `getSimpleBezierPath({...})` | `[path, labelX, labelY, offsetX, offsetY]` |
| `getSmoothStepPath({...})`   | `[path, labelX, labelY, offsetX, offsetY]` |
| `getStraightPath({...})`     | `[path, labelX, labelY]`                   |

All accept: `sourceX`, `sourceY`, `targetX`, `targetY`, `sourcePosition`, `targetPosition`.

### Edge Labels (EdgeLabelRenderer)

Portal that renders HTML outside the SVG layer. Key rules:

- Add `pointer-events: all` to make labels interactive.
- Add `nodrag nopan` classes to prevent canvas interaction.
- Position with `labelX`, `labelY` from path utilities.

### Animated Edges and Markers

```tsx
const edges = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  {
    id: 'e2-3', source: '2', target: '3',
    markerEnd: { type: MarkerType.ArrowClosed, color: '#f00', width: 20, height: 20 },
  },
];
```

### Edge Reconnection

```tsx
<ReactFlow
  edgesReconnectable={true}
  reconnectRadius={10}
  onReconnect={(oldEdge, newConnection) => { /* handle */ }}
  onReconnectStart={(event, edge, handleType) => { /* handle */ }}
  onReconnectEnd={(event, edge, handleType) => { /* handle */ }}
/>
```

### Connection Line

```tsx
<ReactFlow
  connectionLineType={ConnectionLineType.SmoothStep}
  connectionLineStyle={{ stroke: '#ddd', strokeWidth: 2 }}
  connectionLineComponent={MyCustomConnectionLine}
  connectionRadius={20}
/>
```

---

## Drag and Drop

### Built-in Node Dragging

```tsx
<ReactFlow
  nodesDraggable={true}           // Global toggle
  nodeDragThreshold={1}           // Pixels before drag fires (default: 1)
  autoPanOnNodeDrag={true}        // Pan when dragging to edges
  selectNodesOnDrag={true}        // Select while dragging
  snapToGrid={true}               // Snap positions to grid
  snapGrid={[15, 15]}             // Grid size [x, y]
/>
```

Per-node: `{ id: '1', data: { label: 'Fixed' }, position: { x: 0, y: 0 }, draggable: false }`

### Drag Handles

Use `nodrag` class to disable dragging on elements. Use `dragHandle` to restrict drag to specific area:

```tsx
{ id: '1', data: { label: 'Node' }, position: { x: 0, y: 0 }, dragHandle: '.drag-handle' }
```

Then in custom node: `<div className="drag-handle">Drag here</div>`

### External Drag and Drop (Sidebar to Canvas)

```tsx
function DnDFlow() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const { screenToFlowPosition } = useReactFlow();
  const [type] = useDnD(); // Custom DnD context

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      if (!type) return;
      const position = screenToFlowPosition({ x: event.clientX, y: event.clientY });
      const newNode = { id: getId(), type, position, data: { label: `${type} node` } };
      setNodes((nds) => nds.concat(newNode));
    },
    [screenToFlowPosition, type],
  );

  return (
    <ReactFlow nodes={nodes} edges={edges}
      onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
      onDragOver={onDragOver} onDrop={onDrop} fitView />
  );
}

// Sidebar component
function Sidebar() {
  const [_, setType] = useDnD();
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    setType(nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };
  return (
    <aside>
      <div draggable onDragStart={(e) => onDragStart(e, 'default')}>Default Node</div>
      <div draggable onDragStart={(e) => onDragStart(e, 'input')}>Input Node</div>
    </aside>
  );
}
```

HTML Drag and Drop API does not work on touch. Use Pointer Events or Neodrag for touch support.

---

## Interactivity

### Selection

```tsx
<ReactFlow
  elementsSelectable={true}
  selectionOnDrag={false}            // Selection box on drag (Figma-style)
  selectionMode="full"               // "full" or "partial" (intersect)
  selectionKeyCode="Shift"
  multiSelectionKeyCode="Meta"
  selectNodesOnDrag={true}
  elevateNodesOnSelect={true}
  elevateEdgesOnSelect={false}
/>
```

### Connecting Nodes

```tsx
<ReactFlow
  nodesConnectable={true}
  connectionMode={ConnectionMode.Strict}  // "Strict" or "Loose"
  connectOnClick={true}                   // Click source, then click target
  connectionRadius={20}                   // Snap distance
  autoPanOnConnect={true}
  isValidConnection={(connection) => connection.source !== connection.target}
/>
```

### Pan and Zoom

**Default (slippy map):**

```tsx
<ReactFlow
  panOnDrag={true} zoomOnScroll={true} zoomOnPinch={true} zoomOnDoubleClick={true}
  minZoom={0.5} maxZoom={2} preventScrolling={true}
  panActivationKeyCode="Space" zoomActivationKeyCode="Meta"
/>
```

**Design tool style (Figma):**

```tsx
<ReactFlow panOnScroll={true} selectionOnDrag={true} panOnDrag={false} selectionMode="partial" />
```

### Built-in Components

```tsx
import { Background, BackgroundVariant, Controls, MiniMap, Panel } from '@xyflow/react';

<ReactFlow ...>
  <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
  <Controls showInteractive={true} showZoom={true} showFitView={true} />
  <MiniMap zoomable pannable nodeColor={(n) => n.type === 'input' ? '#6ede87' : '#eee'} />
  <Panel position="top-left"><button>Save</button></Panel>
</ReactFlow>
```

Panel positions: `top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`.

### Context Menus

```tsx
const onNodeContextMenu = useCallback((event: React.MouseEvent, node: Node) => {
  event.preventDefault();
  setMenu({ id: node.id, top: event.clientY, left: event.clientX });
}, []);

<ReactFlow onNodeContextMenu={onNodeContextMenu} onPaneContextMenu={onPaneContextMenu} />
```

### Keyboard Shortcuts

| Key                    | Action                         |
| ---------------------- | ------------------------------ |
| `Backspace` / `Delete` | Delete selected                |
| `Shift` + drag         | Selection box                  |
| `Meta`/`Ctrl` + click  | Multi-select                   |
| `Space` + drag         | Pan                            |
| `Meta`/`Ctrl` + scroll | Zoom                           |
| `Tab`                  | Navigate focusable nodes/edges |
| Arrow keys             | Move selected nodes            |
| `Escape`               | Clear selection                |

All configurable: `deleteKeyCode`, `selectionKeyCode`, `multiSelectionKeyCode`, `zoomActivationKeyCode`, `panActivationKeyCode`.

---

## Event Hooks (Exhaustive)

### Node Events

| Callback            | Signature                         |
| ------------------- | --------------------------------- |
| `onNodesChange`     | `(changes: NodeChange[]) => void` |
| `onNodeClick`       | `(event, node) => void`           |
| `onNodeDoubleClick` | `(event, node) => void`           |
| `onNodeContextMenu` | `(event, node) => void`           |
| `onNodeDragStart`   | `(event, node, nodes) => void`    |
| `onNodeDrag`        | `(event, node, nodes) => void`    |
| `onNodeDragStop`    | `(event, node, nodes) => void`    |
| `onNodeMouseEnter`  | `(event, node) => void`           |
| `onNodeMouseMove`   | `(event, node) => void`           |
| `onNodeMouseLeave`  | `(event, node) => void`           |
| `onNodesDelete`     | `(nodes: Node[]) => void`         |

### Edge Events

| Callback            | Signature                           |
| ------------------- | ----------------------------------- |
| `onEdgesChange`     | `(changes: EdgeChange[]) => void`   |
| `onEdgeClick`       | `(event, edge) => void`             |
| `onEdgeDoubleClick` | `(event, edge) => void`             |
| `onEdgeContextMenu` | `(event, edge) => void`             |
| `onEdgeMouseEnter`  | `(event, edge) => void`             |
| `onEdgeMouseMove`   | `(event, edge) => void`             |
| `onEdgeMouseLeave`  | `(event, edge) => void`             |
| `onEdgesDelete`     | `(edges: Edge[]) => void`           |
| `onReconnect`       | `(oldEdge, newConnection) => void`  |
| `onReconnectStart`  | `(event, edge, handleType) => void` |
| `onReconnectEnd`    | `(event, edge, handleType) => void` |

### Connection Events

| Callback              | Signature                          |
| --------------------- | ---------------------------------- |
| `onConnect`           | `(connection: Connection) => void` |
| `onConnectStart`      | `(event, params) => void`          |
| `onConnectEnd`        | `(event) => void`                  |
| `onClickConnectStart` | `(event, params) => void`          |
| `onClickConnectEnd`   | `(event) => void`                  |
| `isValidConnection`   | `(connection) => boolean`          |

### Pane Events

| Callback            | Signature         |
| ------------------- | ----------------- |
| `onPaneClick`       | `(event) => void` |
| `onPaneContextMenu` | `(event) => void` |
| `onPaneScroll`      | `(event) => void` |
| `onPaneMouseEnter`  | `(event) => void` |
| `onPaneMouseMove`   | `(event) => void` |
| `onPaneMouseLeave`  | `(event) => void` |

### Viewport Events

| Callback           | Signature                      |
| ------------------ | ------------------------------ |
| `onMoveStart`      | `(event, viewport) => void`    |
| `onMove`           | `(event, viewport) => void`    |
| `onMoveEnd`        | `(event, viewport) => void`    |
| `onViewportChange` | `(viewport: Viewport) => void` |

### Selection Events

| Callback                 | Signature                            |
| ------------------------ | ------------------------------------ |
| `onSelectionChange`      | `(params: { nodes, edges }) => void` |
| `onSelectionStart`       | `(event) => void`                    |
| `onSelectionEnd`         | `(event) => void`                    |
| `onSelectionDragStart`   | `(event, nodes) => void`             |
| `onSelectionDrag`        | `(event, nodes) => void`             |
| `onSelectionDragStop`    | `(event, nodes) => void`             |
| `onSelectionContextMenu` | `(event, nodes) => void`             |

### Lifecycle Events

| Callback         | Signature                               |
| ---------------- | --------------------------------------- |
| `onInit`         | `(instance: ReactFlowInstance) => void` |
| `onError`        | `(code, message) => void`               |
| `onBeforeDelete` | `(params) => Promise<boolean>`          |
| `onDelete`       | `(params: { nodes, edges }) => void`    |

---

## State Management

### Controlled (Recommended)

```tsx
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
const onConnect = useCallback(
  (connection) => setEdges((eds) => addEdge(connection, eds)), [setEdges],
);

<ReactFlow nodes={nodes} edges={edges}
  onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} />
```

### Manual Controlled

```tsx
import { applyNodeChanges, applyEdgeChanges } from '@xyflow/react';

const [nodes, setNodes] = useState(initialNodes);
const [edges, setEdges] = useState(initialEdges);
const onNodesChange = useCallback(
  (changes) => setNodes((nds) => applyNodeChanges(changes, nds)), [],
);
const onEdgesChange = useCallback(
  (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)), [],
);
```

### Uncontrolled

```tsx
<ReactFlow defaultNodes={initialNodes} defaultEdges={initialEdges} />
```

### Hooks Reference

| Hook                                  | Returns                            | Purpose                                      |
| ------------------------------------- | ---------------------------------- | -------------------------------------------- |
| `useNodesState(init)`                 | `[nodes, setNodes, onNodesChange]` | Convenience node state                       |
| `useEdgesState(init)`                 | `[edges, setEdges, onEdgesChange]` | Convenience edge state                       |
| `useReactFlow()`                      | `ReactFlowInstance`                | Programmatic control                         |
| `useNodes()`                          | `Node[]`                           | Subscribe to all nodes (triggers re-renders) |
| `useEdges()`                          | `Edge[]`                           | Subscribe to all edges (triggers re-renders) |
| `useViewport()`                       | `{ x, y, zoom }`                   | Subscribe to viewport                        |
| `useNodesInitialized()`               | `boolean`                          | True when all nodes measured                 |
| `useOnSelectionChange(cb)`            | `void`                             | Selection changes                            |
| `useOnViewportChange(cbs)`            | `void`                             | Viewport changes                             |
| `useHandleConnections({ type, id? })` | `Connection[]`                     | Connections to a handle                      |
| `useNodeConnections({ handleType })`  | `Connection[]`                     | Connections for current node                 |
| `useNodesData(nodeIds)`               | `{ id, type, data }[]`             | Reactive node data access                    |
| `useInternalNode(id)`                 | `InternalNode`                     | Internal node data                           |
| `useConnection()`                     | `ConnectionState`                  | Ongoing connection state                     |
| `useNodeId()`                         | `string`                           | Current node ID (inside custom node)         |
| `useUpdateNodeInternals()`            | `(id) => void`                     | Force node re-measurement                    |
| `useKeyPress(keyCode)`                | `boolean`                          | Track key press                              |
| `useStore(selector)`                  | `T`                                | Direct Zustand store access                  |
| `useStoreApi()`                       | `StoreApi`                         | Zustand API (no re-renders)                  |

### useReactFlow() API

```tsx
const {
  // Node operations
  getNodes, getNode, setNodes, addNodes, updateNode, updateNodeData,
  // Edge operations
  getEdges, getEdge, setEdges, addEdges, updateEdge, updateEdgeData,
  // Deletion
  deleteElements,
  // Viewport
  getViewport, setViewport, fitView, fitBounds, zoomIn, zoomOut, setCenter,
  // Coordinate conversion
  screenToFlowPosition, flowToScreenPosition,
  // Intersection
  getIntersectingNodes, isNodeIntersecting,
  // Serialization
  toObject,  // () => { nodes, edges, viewport }
} = useReactFlow();
```

### External State (Zustand)

```tsx
import { create } from 'zustand';
import { applyNodeChanges, applyEdgeChanges, addEdge } from '@xyflow/react';

const useFlowStore = create((set, get) => ({
  nodes: initialNodes,
  edges: initialEdges,
  onNodesChange: (changes) => set({ nodes: applyNodeChanges(changes, get().nodes) }),
  onEdgesChange: (changes) => set({ edges: applyEdgeChanges(changes, get().edges) }),
  onConnect: (connection) => set({ edges: addEdge(connection, get().edges) }),
}));

function Flow() {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect } = useFlowStore();
  return (
    <ReactFlow nodes={nodes} edges={edges}
      onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} />
  );
}
```

Same pattern works with Redux, Jotai, or any state library.

### useStore / useStoreApi (Performance)

```tsx
// Subscribe to slice (re-renders only when output changes)
const selectedNodeIds = useStore((state) =>
  state.nodes.filter((n) => n.selected).map((n) => n.id),
);

// Direct store API (no re-renders, imperative access)
const store = useStoreApi();
const nodes = store.getState().nodes;
```

---

## Layout and Positioning

### Auto-Layout with dagre

```tsx
import Dagre from '@dagrejs/dagre';

function getLayoutedElements(nodes, edges, direction = 'TB') {
  const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    g.setNode(node.id, {
      width: node.measured?.width ?? 150,
      height: node.measured?.height ?? 50,
    });
  });
  edges.forEach((edge) => g.setEdge(edge.source, edge.target));
  Dagre.layout(g);

  return {
    nodes: nodes.map((node) => {
      const pos = g.node(node.id);
      return { ...node, position: {
        x: pos.x - (node.measured?.width ?? 150) / 2,
        y: pos.y - (node.measured?.height ?? 50) / 2,
      }};
    }),
    edges,
  };
}
```

Use `node.measured?.width` / `node.measured?.height` (not `node.width`/`node.height` in v12).

### Auto-Layout with ELK

```tsx
import ELK from 'elkjs/lib/elk.bundled.js';
const elk = new ELK();

async function getLayoutedElements(nodes, edges) {
  const graph = {
    id: 'root',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': 'DOWN',
      'elk.spacing.nodeNode': '50',
    },
    children: nodes.map((n) => ({
      id: n.id, width: n.measured?.width ?? 150, height: n.measured?.height ?? 50,
    })),
    edges: edges.map((e) => ({ id: e.id, sources: [e.source], targets: [e.target] })),
  };

  const layout = await elk.layout(graph);
  return {
    nodes: nodes.map((n) => {
      const ln = layout.children?.find((c) => c.id === n.id);
      return { ...n, position: { x: ln?.x ?? 0, y: ln?.y ?? 0 } };
    }),
    edges,
  };
}
```

### fitView and Viewport

```tsx
<ReactFlow fitView fitViewOptions={{ padding: 0.2, maxZoom: 1.5 }} />

// Programmatic
const { fitView, setViewport, setCenter, fitBounds, zoomIn, zoomOut } = useReactFlow();
fitView({ padding: 0.2, includeHiddenNodes: false, maxZoom: 1.5, duration: 200 });
setViewport({ x: 0, y: 0, zoom: 1 }, { duration: 800 });
setCenter(250, 250, { zoom: 1.5, duration: 800 });
```

`nodeOrigin` controls which point is placed at position: `[0, 0]` = top-left (default), `[0.5, 0.5]` = center.

---

## Performance

1. **Memoize custom nodes** with `memo()` and define `nodeTypes`/`edgeTypes` **outside** components.
2. **Memoize callbacks** with `useCallback`.
3. **Avoid `useNodes()`/`useEdges()` for derived state** — use `useStore(selector)` instead.
4. **`onlyRenderVisibleElements={true}`** skips offscreen nodes/edges (useful for 1000+ nodes, may flicker during fast pan).
5. **Collapse node trees** with `hidden: true` instead of removing.
6. **Simplify styles at scale** — avoid complex shadows, animations, gradients.
7. **Use `useStoreApi()`** for reads in event handlers.
8. **Increase `nodeDragThreshold`** for touch devices.

---

## Advanced Patterns

### Save and Restore

```tsx
const onSave = useCallback(() => {
  const flow = rfInstance.toObject(); // { nodes, edges, viewport }
  localStorage.setItem('flow', JSON.stringify(flow));
}, [rfInstance]);

const onRestore = useCallback(() => {
  const flow = JSON.parse(localStorage.getItem('flow'));
  if (flow) {
    setNodes(flow.nodes || []);
    setEdges(flow.edges || []);
    setViewport(flow.viewport);
  }
}, [setNodes, setEdges, setViewport]);
```

### Undo/Redo

Snapshot-based history stack:

```tsx
function useUndoRedo(initialNodes, initialEdges) {
  const [past, setPast] = useState([]);
  const [future, setFuture] = useState([]);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const takeSnapshot = useCallback(() => {
    setPast((p) => [...p, { nodes, edges }]);
    setFuture([]);
  }, [nodes, edges]);

  const undo = useCallback(() => {
    if (!past.length) return;
    const prev = past[past.length - 1];
    setPast((p) => p.slice(0, -1));
    setFuture((f) => [...f, { nodes, edges }]);
    setNodes(prev.nodes);
    setEdges(prev.edges);
  }, [past, nodes, edges]);

  const redo = useCallback(() => {
    if (!future.length) return;
    const next = future[future.length - 1];
    setFuture((f) => f.slice(0, -1));
    setPast((p) => [...p, { nodes, edges }]);
    setNodes(next.nodes);
    setEdges(next.edges);
  }, [future, nodes, edges]);

  return { nodes, edges, setNodes, setEdges, onNodesChange, onEdgesChange,
    undo, redo, takeSnapshot, canUndo: past.length > 0, canRedo: future.length > 0 };
}
```

### Computing Flows (Reactive Data Propagation)

```tsx
// Source node: push data
const { updateNodeData } = useReactFlow();
updateNodeData(id, { value: 42 });

// Downstream node: read upstream data reactively
const connections = useNodeConnections({ handleType: 'target' });
const sourceData = useNodesData(connections?.[0]?.source);
// sourceData.data.value === 42
```

### SSR (v12)

Provide `width` and `height` on nodes for server-side rendering:

```tsx
const nodes = [
  { id: '1', data: { label: 'SSR Node' }, position: { x: 0, y: 0 }, width: 200, height: 50 },
];
```

### Accessibility

```tsx
<ReactFlow
  nodesFocusable={true}
  edgesFocusable={true}
  disableKeyboardA11y={false}
  ariaLabelConfig={{
    'node.a11yDescription.default': 'Press Enter to select this node',
    'controls.zoomIn.ariaLabel': 'Zoom In',
    'minimap.ariaLabel': 'Mini Map',
  }}
/>
```

Custom ARIA on nodes: `ariaRole`, `domAttributes` with `aria-roledescription`, etc.

---

## TypeScript

### Custom Node Types

```typescript
import { type Node, type NodeProps, type BuiltInNode } from '@xyflow/react';

type NumberNode = Node<{ number: number }, 'number'>;
type TextNode = Node<{ text: string }, 'text'>;
type AppNode = NumberNode | TextNode | BuiltInNode;
```

### Type-safe Hooks

```typescript
const { getNodes, setNodes } = useReactFlow<AppNode, AppEdge>();
const nodesData = useNodesData<AppNode>(nodeIds);
```

### Type Guards

```typescript
function isNumberNode(node: AppNode): node is NumberNode {
  return node.type === 'number';
}
```

Use `type` (not `interface`) for node data definitions.

---

## Key Types

| Type                 | Description                                                |
| -------------------- | ---------------------------------------------------------- |
| `Node<T, S>`         | Node with data type T, string literal type S               |
| `Edge<T>`            | Edge with data type T                                      |
| `NodeProps<T>`       | Props for custom node components                           |
| `EdgeProps<T>`       | Props for custom edge components                           |
| `Connection`         | Connection object (source, target, handles)                |
| `NodeChange`         | Union of all node changes                                  |
| `EdgeChange`         | Union of all edge changes                                  |
| `Viewport`           | `{ x, y, zoom }`                                           |
| `Position`           | `Top`, `Bottom`, `Left`, `Right`                           |
| `MarkerType`         | `Arrow`, `ArrowClosed`                                     |
| `BackgroundVariant`  | `Dots`, `Lines`, `Cross`                                   |
| `ConnectionMode`     | `"Strict"`, `"Loose"`                                      |
| `ConnectionLineType` | `Bezier`, `SmoothStep`, `Step`, `Straight`, `SimpleBezier` |
| `SelectionMode`      | `"full"`, `"partial"`                                      |
| `ColorMode`          | `"light"`, `"dark"`, `"system"`                            |
| `ReactFlowInstance`  | Return type of `useReactFlow()`                            |

---

## Built-in Components

| Component               | Purpose                                |
| ----------------------- | -------------------------------------- |
| `<Background />`        | Canvas background (Dots, Lines, Cross) |
| `<Controls />`          | Zoom/fit/interactive toggle            |
| `<ControlButton />`     | Custom button for Controls             |
| `<MiniMap />`           | Bird's-eye navigation                  |
| `<Panel />`             | Fixed overlay container                |
| `<NodeToolbar />`       | Toolbar near a node                    |
| `<NodeResizer />`       | Resize handles                         |
| `<NodeResizeControl />` | Custom resize handle                   |
| `<Handle />`            | Connection point                       |
| `<BaseEdge />`          | SVG edge rendering                     |
| `<EdgeLabelRenderer />` | HTML portal for edge labels            |
| `<EdgeText />`          | Simple text on edges                   |
| `<ViewportPortal />`    | Render HTML in viewport coordinates    |

## Utility Functions

| Function                           | Purpose                   |
| ---------------------------------- | ------------------------- |
| `addEdge(connection, edges)`       | Add edge to array         |
| `applyNodeChanges(changes, nodes)` | Apply changes to nodes    |
| `applyEdgeChanges(changes, edges)` | Apply changes to edges    |
| `getConnectedEdges(nodes, edges)`  | Edges connected to nodes  |
| `getIncomers(node, nodes, edges)`  | Nodes pointing to node    |
| `getOutgoers(node, nodes, edges)`  | Nodes that node points to |
| `isNode(element)`                  | Type guard                |
| `isEdge(element)`                  | Type guard                |

## Multiplayer

CRDT-based solutions for real-time collaboration:

| Library   | Type                 | Offline | Best For                             |
| --------- | -------------------- | ------- | ------------------------------------ |
| Yjs       | CRDT                 | Full    | Collaborative editing, offline-first |
| Automerge | CRDT                 | Full    | Local-first apps                     |
| Loro      | CRDT (WASM)          | Full    | Version control                      |
| Supabase  | Server-authoritative | No      | Simple sync                          |

State to sync: **Durable** (nodes, edges) vs **Ephemeral** (cursors, viewport, selection).
