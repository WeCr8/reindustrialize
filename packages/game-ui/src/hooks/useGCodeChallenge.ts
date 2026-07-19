import { useCallback, useMemo, useState } from "react";
import { checkAnswers, type ChallengeDef, type MaterialCut } from "@wecr8/game-core";

/**
 * Drives the <GCodeConsole/> — a green-on-black CRT panel styled like the machine
 * control in the concept art. Program renders with tappable blanks; wrong answers
 * show per-blank hints; 3 fails triggers Zach's teaching dialog (never a hard fail).
 * On pass: act("gcode.challenge_passed", { id, machineId }) -> machine.gcodeCleared = true.
 */
export function useGCodeChallenge(def: ChallengeDef, material: MaterialCut,
  onPass: () => void, onTeach: (lines: string[]) => void) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [attempts, setAttempts] = useState(0);
  const [lastResults, setLastResults] = useState<ReturnType<typeof checkAnswers> | null>(null);

  const blanks = useMemo(() => Object.keys(def.blanks), [def]);
  const setAnswer = useCallback((id: string, v: string) => setAnswers(a => ({ ...a, [id]: v })), []);

  const submit = useCallback(() => {
    const res = checkAnswers(def, material, answers);
    setLastResults(res);
    if (res.pass) { onPass(); return; }
    const n = attempts + 1;
    setAttempts(n);
    if (n >= 3) onTeach(def.zachFail); // teach, reset attempts, let them retry
  }, [answers, attempts, def, material, onPass, onTeach]);

  return { blanks, answers, setAnswer, submit, lastResults, attempts };
}
