import { execFile } from 'node:child_process';
import path from 'node:path';
import { promisify } from 'node:util';
import type { predictionRequest } from './validation';

const execFileAsync = promisify(execFile);
const predictionScriptPath = path.resolve(__dirname, '../ml/predict.py');

async function runPredictionScript(args: string[]) {
  try {
    const { stdout } = await execFileAsync('python', [
      predictionScriptPath,
      ...args,
    ]);
    return stdout;
  } catch (err) {
    console.error('Error running prediction script:', err);
    throw err;
  }
}

export async function predictSalary(input: predictionRequest) {
  const output = await runPredictionScript([
    `"${String(input.age)}"`,
    `"${input.gender}"`,
    `"${input.educationLevel}"`,
    `"${input.jobTitle}"`,
    `"${String(input.yearsOfExperience)}"`,
  ]);
  return JSON.parse(output);
}
export async function getLabels() {
  const output = await runPredictionScript(['--features']);
  return JSON.parse(output);
}
