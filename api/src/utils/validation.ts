import { z } from 'zod';
export const predictionRequestSchema = z.object({
  age: z.coerce.number().positive().min(16).max(120),
  gender: z.enum(['Male', 'Female']),
  educationLevel: z.enum(['High School', "Bachelor's", "Master's", 'PhD']),
  jobTitle: z.string().min(2).max(100),
  yearsOfExperience: z.coerce.number().positive().max(80),
});

export type predictionRequest = z.infer<typeof predictionRequestSchema>;
