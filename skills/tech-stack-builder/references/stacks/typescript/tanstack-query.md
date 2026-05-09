# TanStack Query (Server State)

## Setup

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,  // 5 min
      gcTime: 1000 * 60 * 30,    // 30 min garbage collection
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

## queryOptions Pattern (v5 Best Practice)

Co-locate key + fn + options:

```typescript
import { queryOptions } from '@tanstack/react-query'

export const todosQueryOptions = queryOptions({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: 1000 * 60 * 5,
})

export const todoQueryOptions = (id: number) => queryOptions({
  queryKey: ['todos', id],
  queryFn: () => fetchTodo(id),
})

// Usage anywhere:
useQuery(todosQueryOptions)
useSuspenseQuery(todoQueryOptions(42))
queryClient.prefetchQuery(todosQueryOptions)
queryClient.invalidateQueries({ queryKey: todosQueryOptions.queryKey })
```

## Key Rules

- Always use `queryOptions()` to bundle queryKey + queryFn + shared options
- Use `useSuspenseQuery` for Suspense-based data fetching
- Prefetch on hover: `queryClient.prefetchQuery(...)` in `onMouseEnter`
- Invalidate narrowly by queryKey prefix
- `gcTime` replaced `cacheTime` in v5
- Never create `QueryClient` inside a component render
