# @dnd-kit (Drag & Drop)

Use the classic stable API (`@dnd-kit/core` + `@dnd-kit/sortable`). The new `@dnd-kit/react` adapter (v0.3.x) is pre-1.0 — avoid in production.

```tsx
import {
  DndContext, closestCenter, KeyboardSensor, PointerSensor,
  useSensor, useSensors, type DragEndEvent,
} from '@dnd-kit/core'
import {
  arrayMove, SortableContext, sortableKeyboardCoordinates,
  verticalListSortingStrategy, useSortable,
} from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'

function SortableItem({ id }: { id: string }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id })
  return (
    <li ref={setNodeRef} style={{ transform: CSS.Transform.toString(transform), transition }}
        {...attributes} {...listeners}>
      {id}
    </li>
  )
}

function SortableList() {
  const [items, setItems] = useState(['a', 'b', 'c'])
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  )

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter}
      onDragEnd={({ active, over }: DragEndEvent) => {
        if (over && active.id !== over.id) {
          setItems(items => arrayMove(items, items.indexOf(active.id as string), items.indexOf(over.id as string)))
        }
      }}>
      <SortableContext items={items} strategy={verticalListSortingStrategy}>
        {items.map(id => <SortableItem key={id} id={id} />)}
      </SortableContext>
    </DndContext>
  )
}
```

## Key Rules

- `@dnd-kit/core` (~10kB) is the engine; `@dnd-kit/sortable` adds list reordering
- Built-in keyboard navigation and ARIA screen reader support
- Sensors: PointerSensor, KeyboardSensor, TouchSensor — configurable activation constraints
- Collision detection: `closestCenter`, `closestCorners`, `rectIntersection`, or custom
- `DragOverlay` component for custom drag preview rendering
- Supports nested contexts, variable-sized items, virtualized lists
