import { Request, Response } from 'express';
import {
  predictionRequest,
  predictionRequestSchema,
} from '../utils/validation';
import { predictSalary, getLabels } from '../utils/subprocess';
import z from 'zod';
export const predict = async (
  req: Request<{}, {}, predictionRequest>,
  res: Response,
) => {
  try {
    let body = z.parse(predictionRequestSchema, req.body);
    const result = await predictSalary(body);
    // console.log(result);
    res.status(200).json(result);
  } catch (err) {
    if (err instanceof z.ZodError) {
      res.status(400).end('Invalid request body');
    } else {
      console.log(err);
      res.status(500).end('Internal server error');
    }
  }
};
export const getFeatures = async (req: Request, res: Response) => {
  try {
    const result = await getLabels();
    res.status(200).json(result);
  } catch (err) {
    res.status(500).end('Internal server error');
  }
};
