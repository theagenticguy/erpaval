# TanStack Form

```tsx
import { useForm, type AnyFieldApi } from '@tanstack/react-form'

function MyForm() {
  const form = useForm({
    defaultValues: { firstName: '', email: '' },
    onSubmit: async ({ value }) => {
      console.log(value)
    },
  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); form.handleSubmit() }}>
      <form.Field
        name="firstName"
        validators={{
          onChange: ({ value }) =>
            !value ? 'Required' : value.length < 3 ? 'Min 3 chars' : undefined,
        }}
        children={(field) => (
          <div>
            <input
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(e) => field.handleChange(e.target.value)}
            />
            {field.state.meta.isTouched && !field.state.meta.isValid && (
              <em>{field.state.meta.errors.join(', ')}</em>
            )}
          </div>
        )}
      />
      <form.Subscribe
        selector={(s) => [s.canSubmit, s.isSubmitting]}
        children={([canSubmit, isSubmitting]) => (
          <button type="submit" disabled={!canSubmit}>
            {isSubmitting ? '...' : 'Submit'}
          </button>
        )}
      />
    </form>
  )
}
```

## Key Rules

- Validators can be sync or async, at `onChange`, `onBlur`, or `onSubmit` granularity
- Supports Zod, Valibot, ArkType via adapters
- `form.Subscribe` selectively re-renders based on a selector function
- Always call `e.preventDefault()` and `e.stopPropagation()` before `form.handleSubmit()`
