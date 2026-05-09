# Motion (formerly Framer Motion)

The package was rebranded from `framer-motion` to `motion` in November 2024. Always import from `"motion/react"`.

```tsx
import { motion, AnimatePresence } from 'motion/react'

// Basic animation
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Hello
</motion.div>

// Variants for orchestration
const cardVariants = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.5 } },
  hover: { scale: 1.05 },
}

<motion.div variants={cardVariants} initial="hidden" animate="visible" whileHover="hover" />

// Enter/exit animations
<AnimatePresence mode="wait">
  <motion.div
    key={currentKey}
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    exit={{ opacity: 0 }}
  />
</AnimatePresence>

// Layout animations (auto-FLIP)
<motion.div layout />

// Shared element transitions
<motion.div layoutId="shared-card" />
```

## Key Rules

- Import from `"motion/react"`, not `"motion"` directly
- `AnimatePresence` children must have unique `key` props
- Use `mode="wait"` for sequential page transitions, `mode="popLayout"` for lists
- `layoutId` creates shared-element transitions (card-to-modal, tab underlines)
- `useScroll` + `useTransform` for scroll-linked animations
- Duration: 150-250ms for micro-interactions, 250-400ms for page transitions
- Prefer animating `transform` and `opacity` only for 60fps GPU-accelerated performance
- Honors `prefers-reduced-motion` via `useReducedMotion` hook
