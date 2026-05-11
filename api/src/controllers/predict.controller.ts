import { Request, Response } from 'express';

export const predict = async (req: Request, res: Response) => {
  res.status(200).send('hello').end();
};
