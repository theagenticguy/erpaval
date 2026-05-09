# Visualization: Recharts + D3

## Decision Framework

| Use Recharts when...                                   | Use D3 when...                                                      |
| ------------------------------------------------------ | ------------------------------------------------------------------- |
| Standard charts (line, bar, area, pie, scatter, radar) | Custom/novel visualizations (force graphs, treemaps, Sankey, chord) |
| Dashboard panels, quick iteration                      | Geographic, network, or pixel-level custom viz                      |
| Dataset < 10K points                                   | Dataset > 10K points (Canvas rendering)                             |
| Team has React skills                                  | Team has D3 expertise                                               |

## Recharts Pattern

```tsx
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts'

<ResponsiveContainer width="100%" height={400}>
  <LineChart data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip />
    <Line type="monotone" dataKey="value" stroke="#8884d8" />
  </LineChart>
</ResponsiveContainer>
```

- Always wrap in `<ResponsiveContainer>` with explicit `height`
- Data format: flat array of objects, one object per data point
- Custom tooltips via `<Tooltip content={<CustomTooltip />} />`
- SVG-only rendering — for 10K+ points, switch to D3 with Canvas

## D3 + React Pattern

Recommended: D3 for math, React for DOM.

```tsx
import { useMemo } from 'react'
import { scaleLinear, scaleBand, max } from 'd3'

function BarChart({ data, width, height }: Props) {
  const xScale = useMemo(
    () => scaleBand().domain(data.map(d => d.name)).range([0, width]).padding(0.1),
    [data, width]
  )
  const yScale = useMemo(
    () => scaleLinear().domain([0, max(data, d => d.value) ?? 0]).range([height, 0]),
    [data, height]
  )

  return (
    <svg width={width} height={height}>
      {data.map(d => (
        <rect key={d.name} x={xScale(d.name)} y={yScale(d.value)}
          width={xScale.bandwidth()} height={height - yScale(d.value)} fill="steelblue" />
      ))}
    </svg>
  )
}
```

- Use `useMemo` for scales and layout calculations
- Import only what you need from D3 for tree-shaking: `import { scaleLinear } from 'd3-scale'`
- For advanced D3 behaviors (drag, zoom, brush), use D3 inside `useEffect` with `useRef`
- Never let both D3 and React manipulate the same DOM nodes
