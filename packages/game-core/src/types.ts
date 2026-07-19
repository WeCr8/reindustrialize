/** Engine-agnostic core types. No DOM, no React. Deterministic sim. */
export type Tick = number; // 1 tick = 1s game time

export type SkillId = "cnc_programming" | "automation" | "software_dev" | "problem_solving" | "communication";

export interface PlayerState {
  name: string;
  avatarId: string;        // -> data/avatars.json (male/female presets); cosmetic only
  accentColor?: string;    // brand palette hex for avatar trim
  level: number;
  xp: number;
  coins: number;
  skills: Record<SkillId, number>;
  reputation: number; // 0..100, gates contracts
  tier: 1 | 2 | 3 | 4 | 5 | 6;
}

export interface MachineInstance {
  defId: string;          // -> data/machines.json
  pos: [number, number];  // tile coords
  state: "idle" | "running" | "alarm" | "setup" | "off";
  connected: boolean;     // MTConnect
  live?: boolean;         // Shop Mode: mirrors a real machine
  tendedBy?: string;      // operator, robot, or player avatar
  gcodeCleared: boolean;  // CNC machines: player must pass the G-code challenge before first run
  wearTicks: number;
}

export interface Job {
  id: string;
  part: string;
  qty: number; done: number; scrapped: number;
  route: string[];        // ordered machine classes
  payout: number;
  dueTick: Tick;
  status: "open" | "wip" | "shipped" | "late" | "rejected";
}

export interface GameEvent { t: Tick; type: string; data?: Record<string, unknown>; }

export interface GameState {
  seed: number;
  tick: Tick;
  mode: "arcade" | "shop";
  player: PlayerState;
  bay: { id: string; machines: MachineInstance[] };
  staff: string[];        // character ids
  jobs: Job[];
  activeQuests: string[];
  completedQuests: string[];
  eventLog: GameEvent[];  // input log for deterministic replay / anti-cheat
}
