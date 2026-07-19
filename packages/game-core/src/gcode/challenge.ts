/**
 * G-code fill-in-the-blank engine.
 * Answers for RPM/feed/SFM blanks are computed from the ACTIVE JOB'S MATERIAL
 * (NOX catalog sfm + tool context), so ordering different metal changes the
 * correct answers — material awareness is the lesson.
 */
export interface MaterialCut { sfm: number; machinability: number }
export interface ToolCtx { toolDia?: number; flutes?: number; chipLoad?: number }

type BlankDef =
  | { validate: "exact"; answers: string[]; hint: string }
  | { validate: "range"; min?: number; max?: number; compute?: "rpmFromMaterial" | "feedFromRpm" | "sfmFromMaterial"; tolerance?: number; scale?: number; hint: string };

export interface ChallengeDef {
  id: string; tier: number; machineClass: string; lesson: string;
  context: ToolCtx & Record<string, unknown>;
  program: string[];
  blanks: Record<string, BlankDef>;
  zachFail: string[]; zachPass: string[];
}

export function rpmFor(mat: MaterialCut, toolDia: number) { return (mat.sfm * 3.82) / toolDia; }
export function feedFor(rpm: number, flutes: number, chipLoad: number) { return rpm * flutes * chipLoad; }

export interface BlankResult { id: string; ok: boolean; hint?: string }

export function checkAnswers(
  def: ChallengeDef, mat: MaterialCut, answers: Record<string, string>
): { pass: boolean; results: BlankResult[] } {
  const results: BlankResult[] = Object.entries(def.blanks).map(([id, b]) => {
    const raw = (answers[id] ?? "").trim();
    if (b.validate === "exact") {
      const ok = b.answers.some(a => a.toLowerCase() === raw.toLowerCase());
      return { id, ok, hint: ok ? undefined : b.hint };
    }
    const val = Number(raw);
    if (!Number.isFinite(val)) return { id, ok: false, hint: b.hint };
    let center: number | null = null;
    if (b.compute === "rpmFromMaterial") center = rpmFor(mat, def.context.toolDia ?? 0.5);
    if (b.compute === "sfmFromMaterial") center = mat.sfm;
    if (b.compute === "feedFromRpm") {
      const rpm = rpmFor(mat, def.context.toolDia ?? 0.5);
      center = feedFor(rpm, def.context.flutes ?? 4, def.context.chipLoad ?? 0.002) * (b.scale ?? 1);
    }
    let ok: boolean;
    if (center !== null) {
      const tol = b.tolerance ?? 0.25;
      ok = val >= center * (1 - tol) && val <= center * (1 + tol);
    } else {
      ok = val >= (b.min ?? -Infinity) && val <= (b.max ?? Infinity);
    }
    return { id, ok, hint: ok ? undefined : b.hint };
  });
  return { pass: results.every(r => r.ok), results };
}
