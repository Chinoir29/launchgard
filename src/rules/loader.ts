import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { fileURLToPath } from 'url';
import { RuleSet } from '../types/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function loadRules(rulesPath?: string): RuleSet {
  const defaultRulesPath = path.join(__dirname, '../../rules/base.yml');
  const finalPath = rulesPath || defaultRulesPath;

  if (!fs.existsSync(finalPath)) {
    throw new Error(`Rules file not found: ${finalPath}`);
  }

  const content = fs.readFileSync(finalPath, 'utf-8');
  const rules = yaml.load(content) as RuleSet;

  return rules;
}

export function getRuleById(ruleset: RuleSet, ruleId: string) {
  for (const category of Object.values(ruleset.rules)) {
    const rule = category.find((r) => r.id === ruleId);
    if (rule) return rule;
  }
  return null;
}
