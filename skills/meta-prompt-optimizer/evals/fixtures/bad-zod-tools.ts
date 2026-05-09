import { z } from "zod";

export const searchTool = {
  name: "search",
  description: "Search tool.",
  schema: z.object({
    q: z.string().describe("Query"),
    n: z.number().describe("Number"),
    f: z.string().describe("Filter"),
    sort: z.enum(["asc", "desc", "rel"]).describe("Sort"),
  }),
};

export const userTool = {
  name: "get_user",
  description: "A function that gets a user.",
  schema: z.object({
    id: z.string().describe("The id"),
    include: z.array(z.string()).describe("What to include"),
  }),
};

export const createTool = {
  name: "create_item",
  description: "This function is used to create an item in the system.",
  schema: z.object({
    name: z.string().describe("Name"),
    type: z.enum(["a", "b", "c"]).describe("Type"),
    priority: z.number().describe("Priority"),
    metadata: z.record(z.unknown()).describe("Metadata"),
  }),
};

export const deleteTool = {
  name: "delete_item",
  description: "Deletes an item.",
  schema: z.object({
    id: z.string().describe("ID to delete"),
    force: z.boolean().describe("Force"),
  }),
};
